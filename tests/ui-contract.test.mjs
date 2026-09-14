import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const html = await readFile(new URL('../index.html', import.meta.url), 'utf8');

test('implements the approved accessible UI contract', () => {
  assert.match(html, /--focus\s*:\s*#7cc4ff/);
  assert.match(html, /--sp-1\s*:\s*4px/);
  assert.match(html, /--r-md\s*:\s*16px/);
  assert.doesNotMatch(html, /user-scalable=no/);
  assert.match(html, /document\.createElement/);
  assert.match(html, /hashchange/);
  assert.doesNotMatch(html, /\sonclick\s*=/);
  assert.doesNotMatch(html, /innerHTML\s*=/);
});

test('uses cents for club fees and renders semantic interactive controls', () => {
  assert.match(html, /priceCents\s*:\s*28500/);
  assert.match(html, /function formatMoney\(cents\)/);
  assert.match(html, /document\.createElement/);
  assert.match(html, /aria-current="page"/);
  assert.match(html, /role="tablist"/);
});
