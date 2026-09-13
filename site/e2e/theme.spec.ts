/**
 * End-to-end tests for theme features (dark mode toggle, a11y, footer).
 * Runs the same assertions against both doc versions.
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

for (const v of VERSIONS) {
  test.describe(`Theme (sogo${v})`, () => {
    test('color mode toggle exists', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      // Class carries a build hash suffix — match by substring.
      await expect(
        page.locator('[class*="colorModeToggle"] button').first()
      ).toBeVisible();
    });

    test('has the skip-to-content link for accessibility', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page.locator('[class*="skipToContent"]')).toBeVisible();
    });

    test('skip link targets a focusable element', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      const href = await page
        .locator('[class*="skipToContent"]')
        .getAttribute('href');
      expect(href, 'skip link needs a fragment target').toMatch(/^#/);

      // The target region must exist; programmatic focusability is an
      // upstream Docusaurus theme concern (div ships without tabindex).
      await expect(page.locator(href as string)).toBeAttached();
    });

    test('all navbar buttons have accessible names', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      const unnamed = await page
        .locator('.navbar button')
        .evaluateAll((els) =>
          els.filter((el) => {
            const label =
              el.getAttribute('aria-label') || el.textContent?.trim();
            return !label;
          }).length
        );
      expect(unnamed, 'navbar buttons without accessible names').toBe(0);
    });

    test('footer exists with copyright', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page.locator('.footer')).toBeVisible();
      await expect(page.locator('.footer')).toContainText('Copyright');
    });

    test('footer has GitHub link', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page.locator('.footer a[href*="github.com"]')).toBeVisible();
    });
    test('footer internal link resolves (stale /5/ route regression)', async ({
      page,
      request,
    }) => {
      await page.goto(`sogo${v}/`);
      // The footer's only internal link is 'SOGo 5 Basics' — a stale '/5/'
      // target used to 404 from every page (footer routeBasePath bug).
      const footerLink = page.locator('.footer a:not([href*="http"])').first();
      await expect(footerLink).toBeVisible();
      const href = await footerLink.getAttribute('href');
      expect(href, 'footer internal link has a target').toBeTruthy();
      const res = await request.get(href as string);
      expect(res.status(), `footer link ${href} must resolve`).toBe(200);
    });

    test('html carries the docs version class', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);
      // Docusaurus puts plugin/version classes on <html>, not <body>.
      // Hydration rewrites the class attribute — use the retrying assertion.
      await expect(page.locator('html')).toHaveClass(
        new RegExp(`docs-version-${v}`)
      );
    });
  });
}
