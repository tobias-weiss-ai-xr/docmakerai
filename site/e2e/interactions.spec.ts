/**
 * Interaction edge cases: version switching, theme toggle, mobile nav,
 * locale switching, and URL robustness (query strings, hash links,
 * unknown locales).
 */

import { test, expect } from '@playwright/test';
import { ON_PROD_DEPLOY, VERSIONS } from './versions';

for (const v of VERSIONS) {
  const other = v === '5' ? '6' : '5';

  test.describe(`Interactions (sogo${v})`, () => {
    test('version switcher navigates to the other version', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      await page.locator('.navbar').getByRole('button', { name: `SOGo ${v}` }).click();
      // Scope to the navbar dropdown: the page body may also mention the
      // other version (e.g. cross-links on the index page).
      const item = page
        .locator('.navbar .dropdown__link')
        .filter({ hasText: `SOGo ${other}` });
      await expect(item).toBeVisible();
      await item.click();

      await page.waitForURL(new RegExp(`sogo${other}\\/`));
      await expect(page.locator('.theme-doc-version-badge')).toContainText(
        `Version: SOGo ${other}`
      );
    });

    test('dark mode toggle flips the color scheme', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      const html = page.locator('html');
      const before = await html.getAttribute('data-theme');
      expect(before).toBeTruthy();

      // The toggle cycles system -> light -> dark; from "system" the first
      // click may resolve to the same theme. Cycle until the theme flips.
      const toggle = page.locator('[class*="colorModeToggle"] button').first();
      for (let i = 0; i < 3; i++) {
        if ((await html.getAttribute('data-theme')) !== before) break;
        await toggle.click();
        await page.waitForTimeout(300);
      }

      expect(
        await html.getAttribute('data-theme'),
        'toggle must change the resolved color scheme'
      ).not.toBe(before);
    });

    test('mobile hamburger opens the navigation sidebar', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.goto(`sogo${v}/`);

      await page.locator('.navbar__toggle').click();
      const sidebar = page.locator('.navbar-sidebar');
      await expect(sidebar).toBeVisible();
      await expect(sidebar.locator('.menu__link').first()).toBeVisible();
    });

    test('query strings do not break doc pages', async ({ page }) => {
      const res = await page.goto(`sogo${v}/?utm_source=e2e&utm_campaign=edge`);
      expect(res?.status()).toBe(200);
      await expect(page.locator('.theme-doc-markdown')).toBeVisible();
    });

    test('URL without trailing slash lands on the version root', async ({ page }) => {
      test.skip(!ON_PROD_DEPLOY, 'trailing-slash 308s are GitHub Pages semantics');
      const res = await page.goto(`sogo${v}`);
      expect(res?.status()).toBe(200);
      expect(page.url()).toMatch(new RegExp(`sogo${v}\\/$`));
    });

    test('explicit index.html path serves the page', async ({ request }) => {
      test.skip(!ON_PROD_DEPLOY, 'file-level index.html serving is GitHub Pages semantics');
      const res = await request.get(`sogo${v}/index.html`);
      expect(res.status()).toBe(200);
      const html = await res.text();
      expect(html).toContain('theme-doc-markdown');
    });

    test('theme choice persists across reload', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      const html = page.locator('html');
      const toggle = page.locator('[class*="colorModeToggle"] button').first();
      for (let i = 0; i < 3; i++) {
        if ((await html.getAttribute('data-theme')) === 'dark') break;
        await toggle.click();
        await page.waitForTimeout(300);
      }
      expect(await html.getAttribute('data-theme')).toBe('dark');

      await page.reload();
      await expect(html).toHaveAttribute('data-theme', 'dark');
    });

    test('switching version preserves the current page', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);

      await page.locator('.navbar').getByRole('button', { name: `SOGo ${v}` }).click();
      await page
        .locator('.navbar .dropdown__link')
        .filter({ hasText: `SOGo ${other}` })
        .click();

      // Docusaurus client-side routing lands on the non-trailing-slash form.
      await page.waitForURL(new RegExp(`sogo${other}\\/sogo-login\\/?$`));
      await expect(page.locator('.theme-doc-markdown')).toContainText(
        `Getting Started with SOGo ${other}`
      );
    });

    test('browser back navigation returns to the previous doc', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);
      await page.goto(`sogo${v}/`);
      await page.goBack();

      await expect(page).toHaveURL(new RegExp(`sogo${v}\\/sogo-login\\/$`));
      await expect(page.locator('.theme-doc-markdown')).toBeVisible();
    });
  });
}

test.describe('Interactions (site)', () => {
  test('language switcher navigates to the German pages', async ({ page }) => {
    await page.goto('sogo5/');

    await page.locator('.navbar a[href="#"][aria-haspopup]').first().click();
    await page.getByRole('link', { name: 'Deutsch' }).click();

    await page.waitForURL('**/de/sogo5/**');
    await expect(page.locator('html')).toHaveAttribute('lang', 'de');
  });

  test('unknown locale returns 404', async ({ page }) => {
    const res = await page.goto('fr/sogo5/');
    expect(res?.status()).toBe(404);
  });

  test('switching locale preserves the current page', async ({ page }) => {
    test.skip(!ON_PROD_DEPLOY, 'locale redirects are GitHub Pages semantics');
    await page.goto('sogo5/sogo-login/');

    await page.locator('.navbar a[href="#"][aria-haspopup]').first().click();
    await page.getByRole('link', { name: 'Deutsch' }).click();

    await page.waitForURL('**/de/sogo5/sogo-login/');
    await expect(page.locator('html')).toHaveAttribute('lang', 'de');
    await expect(page.locator('.theme-doc-markdown')).toBeVisible();
  });

  test('hash deep-links target an existing heading', async ({ page }) => {
    // Pull the first real TOC fragment from the rendered page, then load it.
    const res = await page.request.get('sogo5/sogo-login/');
    const html = await res.text();
    // Served HTML puts href before class and may drop quotes:
    // <a href=#logging-in class=table-of-contents__link ...>
    const tocHref = html.match(
      /href="?#([^" >]+)"?[^>]*class="?[^" >]*table-of-contents__link/
    )?.[1];
    expect(tocHref, 'login page should expose TOC anchors').toBeTruthy();

    await page.goto(`sogo5/sogo-login#${tocHref}`);
    await expect(page.locator(`#${tocHref}`)).toBeAttached();
    await expect(page.locator('.theme-doc-markdown')).toBeVisible();
  });
});
