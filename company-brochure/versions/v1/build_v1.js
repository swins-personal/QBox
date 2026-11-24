// 회사소개서 PDF 생성: A4 4쪽(읽는 순서) + A3 2장(접지 인쇄용 터잡기)
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

  for (const n of [1, 2, 3, 4, 5, 6]) {
    await page.locator(`.page[data-p="${n}"]`).screenshot({ path: path.join(dir, 'preview', `p${n}.png`) });
  }

  await page.pdf({
    path: path.join(dir, '스테디윈스_회사소개서_A4_6p.pdf'),
    width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true,
  });

  // 3단 접지 터잡기(630×297mm): 바깥면 = 5쪽 | 6쪽 | 1쪽, 안쪽면 = 2쪽 | 3쪽 | 4쪽
  await page.addStyleTag({ content: '@page{size:630mm 297mm;margin:0}' });
  await page.evaluate(() => {
    const get = (n) => document.querySelector(`.page[data-p="${n}"]`);
    const mk = (...ns) => {
      const s = document.createElement('div');
      s.className = 'sheet';
      s.append(...ns.map(get));
      return s;
    };
    document.body.classList.add('impose');
    document.body.append(mk(5, 6, 1), mk(2, 3, 4));
  });
  await page.pdf({
    path: path.join(dir, '스테디윈스_회사소개서_3단접지_인쇄용.pdf'),
    width: '630mm', height: '297mm', printBackground: true,
  });
  await browser.close();
})();
