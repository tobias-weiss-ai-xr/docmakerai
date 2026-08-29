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

    test('footer exists with copyright', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page.locator('.footer')).toBeVisible();
      await expect(page.locator('.footer')).toContainText('Copyright');
    });

    test('footer has GitHub link', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page.locator('.footer a[href*="github.com"]')).toBeVisible();
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
