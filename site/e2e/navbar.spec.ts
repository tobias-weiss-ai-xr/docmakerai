/**
 * End-to-end tests for navbar behavior.
 * Runs the same assertions against both doc versions (SOGo 5 and SOGo 6).
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

for (const v of VERSIONS) {
  test.describe(`Navbar (sogo${v})`, () => {
    test('navbar is visible', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page.locator('.navbar')).toBeVisible();
    });

    test('logo is not oversized (regression for global img rule)', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      // Light + dark themed variants both match — measure the visible one.
      const logo = page.locator('.navbar__logo img').first();
      await expect(logo).toBeVisible();

      // Logo must be constrained to reasonable size (max-height: 2rem = 32px)
      // This catches the bug where global img {width:640px; height:400px} blew up the logo
      const { width, height } = await logo.boundingBox();

      // Logo should be at most ~40px (2rem) in either dimension
      expect(width, 'Logo width should be <= 40px').toBeLessThanOrEqual(40);
      expect(height, 'Logo height should be <= 40px').toBeLessThanOrEqual(40);

      // Should never be the 640px that the old global rule forced
      expect(width, 'Logo width should not be 640px').not.toBe(640);
      expect(height, 'Logo height should not be 400px').not.toBe(400);
    });

    test('logo alt text refers to SOGo', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      const logo = page.locator('.navbar__logo img').first();
      await expect(logo).toHaveAttribute('alt', /SOGo/);
    });

    test('navbar brand links to the guide home', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      const brandLink = page.locator('.navbar__brand');
      // The brand intentionally points at the site's canonical entry (SOGo 5)
      // from every version — same target as the root redirect shell.
      await expect(brandLink).toHaveAttribute('href', /sogo5\/$/);
    });

    test('navbar has Docs/Tutorials links', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      const navbar = page.locator('.navbar');
      await expect(navbar.getByRole('link', { name: 'Docs' })).toBeVisible();
      await expect(navbar.getByRole('link', { name: 'Tutorials' })).toBeVisible();
    });

    test('navbar has GitHub link', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(
        page.locator('.navbar').getByRole('link', { name: /GitHub/ })
      ).toBeVisible();
    });

    test('navbar has version dropdown showing the current version', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      // The dropdown trigger shows the current version; alternatives are hidden.
      await expect(
        page.locator('.navbar').getByRole('button', { name: `SOGo ${v}` })
      ).toBeVisible();
    });

    test('navbar has language dropdown', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      // Locale picker is an icon-only dropdown trigger.
      await expect(
        page.locator('.navbar a[href="#"][aria-haspopup]').first()
      ).toBeVisible();
    });

    test('navbar toggle exists on mobile viewport', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 }); // Mobile
      await page.goto(`sogo${v}/`);
      await expect(page.locator('.navbar__toggle')).toBeVisible();
    });
  });
}
