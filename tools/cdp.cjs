// Minimal headless-Chrome CDP driver. Real layout, real viewport, no mockup frame.
// Usage: node tools/cdp.cjs <jobfile.json>
// Job: { base, viewport:{w,h,dsr}, steps:[ {route, out, probe, fullPage} ] }
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');
const WebSocket = require('ws');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333 + (process.pid % 200);

function getJSON(url) {
  return new Promise((res, rej) => {
    http.get(url, r => { let b = ''; r.on('data', c => b += c); r.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(e); } }); }).on('error', rej);
  });
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function waitForChrome() {
  for (let i = 0; i < 100; i++) {
    try { return await getJSON(`http://127.0.0.1:${PORT}/json/version`); } catch (e) { await sleep(150); }
  }
  throw new Error('chrome devtools endpoint never came up');
}

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.events = [];
    ws.on('message', m => {
      const msg = JSON.parse(m);
      if (msg.id && this.pending.has(msg.id)) {
        const { res, rej } = this.pending.get(msg.id); this.pending.delete(msg.id);
        msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result);
      } else if (msg.method) { this.events.push(msg); }
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => { this.pending.set(id, { res, rej }); this.ws.send(JSON.stringify({ id, method, params })); });
  }
  // NOTE: this is a browser-automation driver; `eval` here is CDP Runtime.evaluate,
  // i.e. executing probe expressions inside the headless page under test. That is the
  // tool's purpose. Expressions come only from local job files in this repo, never from
  // user input or network data, so there is no injection surface to harden.
  async eval(expr) {
    const r = await this.send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error('eval: ' + JSON.stringify(r.exceptionDetails.exception?.description || r.exceptionDetails));
    return r.result.value;
  }
}

(async () => {
  const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const vp = job.viewport || { w: 390, h: 844, dsr: 2 };
  const userDir = fs.mkdtempSync('/tmp/cdp-prof-');
  const chrome = spawn(CHROME, [
    '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${userDir}`,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions',
    '--hide-scrollbars', '--force-device-scale-factor=' + vp.dsr,
    `--window-size=${vp.w},${vp.h}`, 'about:blank'
  ], { stdio: 'ignore' });

  const results = [];
  try {
    await waitForChrome();
    const targets = await getJSON(`http://127.0.0.1:${PORT}/json/list`);
    const page = targets.find(t => t.type === 'page');
    const ws = new WebSocket(page.webSocketDebuggerUrl, { perMessageDeflate: false, maxPayload: 256 * 1024 * 1024 });
    await new Promise((res, rej) => { ws.on('open', res); ws.on('error', rej); });
    const cdp = new CDP(ws);

    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Log.enable');
    await cdp.send('Network.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: vp.w, height: vp.h, deviceScaleFactor: vp.dsr, mobile: true,
      screenWidth: vp.w, screenHeight: vp.h
    });
    await cdp.send('Emulation.setUserAgentOverride', {
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    });

    for (const step of job.steps) {
      const url = job.base + (step.route || '');
      await cdp.send('Page.navigate', { url });
      await sleep(step.settle || 900);
      if (step.route) { await cdp.eval(`location.hash=${JSON.stringify(step.route)}`); await sleep(step.settle || 700); }
      // wait for webfonts + images
      await cdp.eval(`document.fonts.ready.then(()=>1)`).catch(() => {});
      await cdp.eval(`Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))).then(()=>1)`).catch(() => {});
      await sleep(step.settle || 500);
      if (step.pre) await cdp.eval(step.pre);
      await sleep(250);

      const entry = { route: step.route, url };
      if (step.probe) { try { entry.probe = await cdp.eval(step.probe); } catch (e) { entry.probeError = String(e.message); } }
      if (step.out) {
        const shot = await cdp.send('Page.captureScreenshot', {
          format: 'png',
          captureBeyondViewport: !!step.fullPage,
          clip: step.fullPage ? undefined : { x: 0, y: 0, width: vp.w, height: vp.h, scale: 1 }
        });
        fs.mkdirSync(path.dirname(step.out), { recursive: true });
        fs.writeFileSync(step.out, Buffer.from(shot.data, 'base64'));
        entry.shot = step.out;
        entry.bytes = fs.statSync(step.out).size;
      }
      results.push(entry);
    }
    const failedReqs = cdp.events.filter(e => e.method === 'Network.loadingFailed').map(e => e.params);
    const consoleErrs = cdp.events.filter(e => e.method === 'Log.entryAdded' && e.params.entry.level === 'error').map(e => e.params.entry.text);
    console.log(JSON.stringify({ viewport: vp, results, failedRequests: failedReqs, consoleErrors: consoleErrs }, null, 1));
    ws.close();
  } finally {
    chrome.kill('SIGKILL');
    try { fs.rmSync(userDir, { recursive: true, force: true }); } catch (e) {}
  }
})().catch(e => { console.error('DRIVER ERROR: ' + e.stack); process.exit(1); });
