const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const html = fs.readFileSync('index.html', 'utf8');
const errors = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'http://localhost/#/discover', pretendToBeVisual: true,
  beforeParse(window) { window.HTMLElement.prototype.focus = function () {}; },
  virtualConsole: new VirtualConsole().on('jsdomError', error => errors.push(String(error)))
});
const document = dom.window.document;
const initial = { heading: document.querySelector('h1')?.textContent, cards: document.querySelectorAll('.card').length, inputs: document.querySelectorAll('input').length, tabs: document.querySelectorAll('[role=tab]').length };
const search = document.querySelector('input[type=search]');
search.value = 'zzzz';
search.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
const empty = document.querySelector('.empty')?.textContent.includes('No clubs match');
search.value = '';
search.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
document.querySelector('.card').click();
setTimeout(() => {
  const detail = { route: dom.window.location.hash, heading: document.querySelector('h1')?.textContent, request: [...document.querySelectorAll('button')].find(button => button.textContent.includes('Request to book'))?.textContent };
  const result = { errors, initial, empty, detail, inlineHandlers: document.querySelectorAll('[onclick]').length };
  console.log(JSON.stringify(result, null, 2));
  if (errors.length || initial.cards !== 5 || initial.inputs !== 1 || !empty || !detail.request || result.inlineHandlers) process.exitCode = 1;
}, 10);
