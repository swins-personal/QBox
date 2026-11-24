// 회사소개서 PDF 생성: A4 6쪽(읽는 순서). 인쇄용 접지 대지는 최종 단계에서 따로 만든다.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const dir = __dirname;
  const url = 'file://' + path.join(dir, 'brochure.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);

  // 넘침 검사: 각 쪽의 내용이 안쪽 여백을 벗어나면 알린다
  const overflow = await page.evaluate(() =>
    [...document.querySelectorAll('.page')].map((p) => {
      const pad = p.querySelector('.pad');
      return { p: p.dataset.p, over: pad.scrollHeight - pad.clientHeight };
    })
  );
  console.log('overflow(px):', JSON.stringify(overflow));

  // 글자 크기 검사: 8.5pt보다 작은 글자가 있으면 알린다
  const small = await page.evaluate(() => {
    const out = new Set();
    for (const el of document.querySelectorAll('.page *')) {
      if (!el.childNodes.length || el.closest('.draft')) continue;
      const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
      if (!hasText) continue;
      const pt = parseFloat(getComputedStyle(el).fontSize) * 0.75;
      if (pt < 8.45) out.add(`${el.className || el.tagName}:${pt.toFixed(1)}`);
    }
    return [...out];
  });
  console.log('below 8.5pt:', JSON.stringify(small));

  const pages = await page.locator('.page').count();
  for (let n = 1; n <= pages; n++) {
    await page.locator(`.page[data-p="${n}"]`).screenshot({ path: path.join(dir, 'preview', `p${n}.png`) });
  }

  await page.pdf({
    path: path.join(dir, '스테디윈스_회사소개서_A4_6p.pdf'),
    width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true,
  });
  await browser.close();
})();
