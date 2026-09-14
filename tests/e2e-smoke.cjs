const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const html = fs.readFileSync('index.html', 'utf8');
const errors = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'http://localhost/#/discover', pretendToBeVisual: true,
  beforeParse(window) { window.HTMLElement.prototype.focus = function () {}; },
  virtualConsole: new VirtualConsole().on('jsdomError', error => errors.push(String(error)))
});
const { document } = dom.window;
const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const chipState = () => $$('.chip').map(c => c.textContent.trim() + ':' + c.getAttribute('aria-pressed'));
const failures = [];
const check = (cond, msg) => { if (!cond) failures.push(msg); };

// Discover: real controls, photo layer on card bands
check($$('.card').length === 5, 'expected 5 club cards');
check($$('input').length === 1, 'expected 1 real search input');
check($$('[role=tab]').length === 4, 'expected 4 nav tabs');
check($$('[onclick]').length === 0, 'no inline handlers');
// Requirement: every club card must use its OWN photo. Assert distinctness, not just presence.
const bandPhotos = $$('.band').map(b => (b.getAttribute('style') || '').match(/--photo:url\(([^)]+)\)/)?.[1] || null);
check(bandPhotos.every(p => p && /^assets\/club-\d+\.jpg$/.test(p)), 'every band has a club photo: ' + bandPhotos);
check(new Set(bandPhotos).size === bandPhotos.length, 'every club card photo is unique: ' + bandPhotos);
check(JSON.stringify(chipState()) === JSON.stringify(['All tiers:true', 'Trophy:false', 'National:false', 'Regional:false', 'Caddie:false']), 'initial aria-pressed must be literal true/false: ' + chipState());

// Filters
$$('.chip').find(c => c.textContent.trim() === 'Trophy').click();
check($$('.card').length === 2, 'Trophy filter should leave 2 cards');
check(chipState()[0] === 'All tiers:false' && chipState()[1] === 'Trophy:true', 'aria-pressed follows filter state: ' + chipState());
$$('.chip').find(c => c.textContent.trim() === 'All tiers').click();
check($$('.card').length === 5, 'All tiers restores 5 cards');

// Search empty state
const search = $('input[type=search]');
search.value = 'zzzz'; search.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
check($('.empty')?.textContent.includes('No clubs match'), 'empty state renders');
search.value = ''; search.dispatchEvent(new dom.window.Event('input', { bubbles: true }));

// Detail + booking confirmation
$('.card').click();
setTimeout(() => {
  check(dom.window.location.hash === '#/club/0', 'card click routes to #/club/0');
  check($('h1')?.textContent === 'Cypress Hollow G&CC', 'detail heading');
  check(/--photo:url\(assets\/club-1\.jpg\)/.test($('.detail-hero').getAttribute('style')), 'detail hero has its own club photo layer');
  const request = $$('button').find(b => b.textContent.includes('Request to book'));
  check(request?.textContent === 'Request to book · $324', 'cents-based total $285 + $39');
  request.click();
  check($('.confirm h3')?.textContent === 'Request sent', 'inline confirmation after request');

  // Sheets: publish has no email field, upgrade does
  dom.window.location.hash = '#/host';
  setTimeout(() => {
    $$('button').find(b => b.textContent.includes('Publish this spot')).click();
    check($('[role=dialog]') && $$('[role=dialog] input').length === 0, 'publish sheet has no demo email field');
    $$('[role=dialog] button').find(b => b.textContent === 'Done').click();
    dom.window.location.hash = '#/profile';
    setTimeout(() => {
      $$('button').find(b => b.textContent.includes('Upgrade to Plus')).click();
      check($$('[role=dialog] input').length === 1, 'upgrade sheet keeps demo email field');
      $$('[role=dialog] button').find(b => b.textContent === 'Close').click();
      check(!$('[role=dialog]'), 'sheet closes');
      const result = { errors, failures, ok: !errors.length && !failures.length };
      console.log(JSON.stringify(result, null, 2));
      if (!result.ok) process.exitCode = 1;
    }, 10);
  }, 10);
}, 10);
