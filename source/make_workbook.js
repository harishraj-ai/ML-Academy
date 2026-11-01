// Render workbook.html to a PDF with Chromium (run after build.py): node make_workbook.js <out_dir>
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const out = process.argv[2]; const b = await chromium.launch(); const ctx = await b.newContext(); await ctx.route(/^https?:/, r => r.abort());
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(out, 'workbook.html')); await p.waitForSelector('html[data-wb-ready]', { timeout: 60000 });
  await p.evaluate(async () => { await document.fonts.ready; }); await p.emulateMedia({ media: 'print' });
  const info = await p.evaluate(() => ({ katexErr: document.querySelectorAll('.katex-error').length, rawDollar: [...document.querySelectorAll('.wb-body p, .wb-body li, .wb-body td')].filter(x => /\$[^$]+\$/.test(x.textContent) && !x.querySelector('.katex')).length,
    lessons: document.querySelectorAll('.wb-lesson').length, work: document.querySelectorAll('.wb-work').length, answers: document.querySelectorAll('.wb-ans-lesson').length, demos: document.querySelectorAll('.wb-note').length, buttons: document.querySelectorAll('.wb-body button').length }));
  fs.mkdirSync(path.resolve(out, 'workbook'), { recursive: true });
  const pdf = path.resolve(out, 'workbook', 'ML-Academy-workbook.pdf');
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, outline: true, tagged: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>', footerTemplate: '<div style="width:100%;font:8px sans-serif;color:#777;text-align:center">ML Academy workbook · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' } });
  console.log(JSON.stringify(info), 'errors:', errs, 'pdf bytes:', fs.statSync(pdf).size);
  await b.close();
})();
