// node to_pdf.js in.html out.pdf [out.png]
const { chromium } = require('playwright');
(async () => {
  const [inp, out, png] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(inp), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, format: 'A4', preferCSSPageSize: true, printBackground: true });
  if (png) { await p.setViewportSize({ width: 794, height: 1123 }); await p.screenshot({ path: png, fullPage: true }); }
  await b.close();
})();
