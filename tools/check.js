/* FORME — automated layout + interaction checks (headless Chromium via Playwright). */
const { chromium } = require('playwright');
const path = require('path');

const URL = 'file://' + path.resolve(__dirname, '..', 'index.html');
const OUT = process.env.SHOT_DIR || '/tmp/shots';
const SIZES = [[375, 812, 'mobile'], [768, 1024, 'tablet'], [1440, 900, 'desktop']];

(async () => {
  const browser = await chromium.launch();
  const report = [];

  for (const [w, h, label] of SIZES) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));

    await page.goto(URL + '?debug=1', { waitUntil: 'load' });
    await page.waitForTimeout(400);

    const overflow = await page.evaluate(() => ({
      scrollW: document.documentElement.scrollWidth,
      clientW: document.documentElement.clientWidth,
      brokenImgs: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src),
    }));

    await page.screenshot({ path: `${OUT}/${label}-fold.png` });
    await page.screenshot({ path: `${OUT}/${label}-full.png`, fullPage: true });

    const r = { label, viewport: `${w}x${h}`, ...overflow, errors };

    // --- mobile menu (only where the toggle is shown) ---
    const toggle = page.locator('.nav-toggle');
    if (await toggle.isVisible()) {
      await toggle.click();
      await page.waitForTimeout(250);
      r.menuOpens = await page.locator('#site-menu').isVisible();
      r.menuAria = await toggle.getAttribute('aria-expanded');
      await page.screenshot({ path: `${OUT}/${label}-menu.png` });
      await page.keyboard.press('Escape');
      await page.waitForTimeout(200);
      r.menuClosesOnEsc = !(await page.locator('#site-menu').isVisible());
    }

    // --- product dialog ---
    await page.locator('[data-open-product]').nth(1).click();
    await page.waitForTimeout(350);
    r.dialogOpen = await page.locator('#product-modal').isVisible();
    r.dialogTitle = await page.locator('#modal-title').textContent();
    r.dialogFocus = await page.evaluate(() => document.activeElement && document.activeElement.id);
    await page.screenshot({ path: `${OUT}/${label}-dialog.png` });
    await page.keyboard.press('Escape');
    await page.waitForTimeout(250);
    r.dialogClosedOnEsc = !(await page.locator('#product-modal').isVisible());
    r.focusReturned = await page.evaluate(() =>
      document.activeElement && document.activeElement.closest('.product')
        ? document.activeElement.closest('.product').dataset.id : null);

    // --- offer copy ---
    await page.locator('#offer').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await page.locator('#copy-code').click();
    await page.waitForTimeout(350);
    r.copyStatus = (await page.locator('#copy-status').textContent()).trim();
    await page.screenshot({ path: `${OUT}/${label}-offer.png` });

    r.events = await page.evaluate(() => window.FORME.events.map(e => e.event));

    // --- keyboard: first tab should reach the skip link ---
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.locator('body').click({ position: { x: 5, y: 5 } });
    await page.keyboard.press('Tab');
    r.firstTabStop = await page.evaluate(() => { const a=document.activeElement; return a.tagName + '.' + (a.className||'-') + ' :: ' + (a.textContent||'').trim().slice(0,28); });

    report.push(r);
    await ctx.close();
  }

  // --- no-JS pass ---
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, javaScriptEnabled: false });
  const page = await ctx.newPage();
  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForTimeout(300);
  report.push({
    label: 'desktop-nojs',
    navVisible: await page.locator('#site-menu').isVisible(),
    descVisible: await page.locator('.product__desc').first().isVisible(),
    toggleVisible: await page.locator('.nav-toggle').isVisible(),
  });
  await page.screenshot({ path: `${OUT}/desktop-nojs-full.png`, fullPage: true });
  await ctx.close();

  const ctx2 = await browser.newContext({ viewport: { width: 375, height: 812 }, javaScriptEnabled: false });
  const p2 = await ctx2.newPage();
  await p2.goto(URL, { waitUntil: 'load' });
  await p2.waitForTimeout(300);
  report.push({
    label: 'mobile-nojs',
    navVisible: await p2.locator('#site-menu').isVisible(),
    linksReachable: await p2.locator('#site-menu a').count(),
    scrollW: await p2.evaluate(() => document.documentElement.scrollWidth),
  });
  await p2.screenshot({ path: `${OUT}/mobile-nojs-fold.png` });
  await ctx2.close();

  console.log(JSON.stringify(report, null, 2));
  await browser.close();
})();
