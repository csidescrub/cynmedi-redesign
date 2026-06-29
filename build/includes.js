#!/usr/bin/env node
/**
 * Tiny build-time HTML include system.
 *
 * Single source of truth for shared chrome (currently the footer) lives in
 * partials/. Each target page carries a marker pair:
 *
 *   <!-- include:footer -->  ...injected content...  <!-- /include:footer -->
 *
 * Running this script re-injects the partial between every marker pair, so you
 * edit partials/footer.html once and regenerate all pages. It is idempotent.
 *
 * First-time adoption: if a page has no marker pair yet but does contain a
 * <footer>...</footer> block, that block is replaced with a wrapped marker pair
 * so subsequent runs stay in sync.
 *
 * Usage: node build/includes.js   (or: npm run build:html)
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

// Pages that share the canonical footer. Landing pages (lp/, aesthetic-clinic/,
// dental-clinic/) intentionally keep their own minimal footer.
const TARGETS = [
  'index.html',
  'services.html',
  'about.html',
  'contact.html',
  'work.html',
  '404.html',
  'work/astell.html',
  'work/cside.html',
  'work/home-369.html',
  'work/natural-joy-vision.html',
  'work/online-booking.html',
  'work/resort-business.html',
  'work/social-growth.html',
  'work/the-bloom.html',
  'work/varinpat.html',
];

const PARTIALS = {
  footer: fs.readFileSync(path.join(ROOT, 'partials', 'footer.html'), 'utf8').trimEnd(),
};

function injectMarker(html, name, content) {
  const start = `<!-- include:${name} -->`;
  const end = `<!-- /include:${name} -->`;
  const block = `${start}\n    ${content}\n    ${end}`;
  const markerRe = new RegExp(`${start}[\\s\\S]*?${end}`);

  if (markerRe.test(html)) {
    return { html: html.replace(markerRe, block), changed: true };
  }
  // First-time adoption: wrap the existing <footer>...</footer> block.
  if (name === 'footer') {
    const footerRe = /<footer[\s\S]*?<\/footer>/;
    if (footerRe.test(html)) {
      return { html: html.replace(footerRe, block), changed: true };
    }
  }
  return { html, changed: false };
}

let updated = 0;
let skipped = [];
for (const rel of TARGETS) {
  const file = path.join(ROOT, rel);
  if (!fs.existsSync(file)) { skipped.push(`${rel} (missing)`); continue; }
  let html = fs.readFileSync(file, 'utf8');
  const orig = html;
  for (const [name, content] of Object.entries(PARTIALS)) {
    const res = injectMarker(html, name, content);
    if (!res.changed) skipped.push(`${rel} (no ${name} target)`);
    html = res.html;
  }
  if (html !== orig) {
    fs.writeFileSync(file, html);
    updated++;
    console.log(`  ✓ ${rel}`);
  }
}
console.log(`\nIncludes: ${updated} page(s) updated.`);
if (skipped.length) console.log('Skipped:', skipped.join(', '));
