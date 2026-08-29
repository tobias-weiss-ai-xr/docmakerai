/**
 * End-to-end tests for theme features (dark mode, colors).
 */

import { test, expect } from '@playwright/test';

test.describe('Theme', () => {
  test('color mode toggle exists', async ({ page }) => {
    await page.goto('sogo5/');
    // Class carries a build hash suffix — match by substring.
    await expect(
      page.locator('[class*="colorModeToggle"] button').first()
    ).toBeVisible();
  });

  test('has the skip-to-content link for accessibility', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(page.locator('[class*="skipToContent"]')).toBeVisible();
  });

  test('footer exists', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(page.locator('.footer')).toBeVisible();
    await expect(page.locator('.footer')).toContainText('Copyright');
  });

  test('footer has GitHub link', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(page.locator('.footer a[href*="github.com"]')).toBeVisible();
  });

  test('body has proper styling classes', async ({ page }) => {
    await page.goto('sogo5/sogo-login/');
    // Docusaurus puts plugin/version classes on <html>, not <body>.
    // Hydration rewrites the class attribute — use the retrying assertion.
    await expect(page.locator('html')).toHaveClass(/docs-version/);
  });
});
