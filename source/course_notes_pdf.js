// Make workbook/ML-Academy-study-notes.pdf from course-notes.html.
// Run from the ML folder:  node source/course_notes_pdf.js .
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const root = path.resolve(process.argv[2] || '.');
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.emulateMedia({ colorScheme: 'light' });
  await p.goto('file://' + path.join(root, 'course-notes.html'));
  await p.waitForFunction(() => document.querySelectorAll('.katex').length > 0, null, { timeout: 15000 }).catch(() => {});
  await p.evaluate(() => document.documentElement.setAttribute('data-theme', 'light'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  await p.evaluate(() => document.querySelectorAll('.hn details').forEach(d => d.open = true));
  fs.mkdirSync(path.join(root, 'workbook'), { recursive: true });
  await p.pdf({
    path: path.join(root, 'workbook', 'ML-Academy-study-notes.pdf'), format: 'A4', printBackground: true,
    margin: { top: '8mm', bottom: '12mm', left: '8mm', right: '8mm' }, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:8px;color:#888;width:100%;text-align:center">ML Academy · Study notes · <span class="pageNumber"></span> / <span class="totalPages"></span></div>'
  });
  await b.close();
  console.log('PDF written');
})();
