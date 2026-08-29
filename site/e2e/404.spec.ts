/**
 * End-to-end tests for 404 handling.
 * Per-version 404s (unknown docs path) plus the site-level root 404.
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

for (const v of VERSIONS) {
  test.describe(`404 pages (sogo${v})`, () => {
    test('non-existent page returns 404', async ({ page }) => {
      const response = await page.goto(`sogo${v}/this-page-does-not-exist/`);
      expect(response?.status()).toBe(404);
    });

    test('404 page has helpful content', async ({ page }) => {
      await page.goto(`sogo${v}/non-existent/`);
      // Docusaurus renders its own 404 content
      await expect(page.locator('main')).toContainText(/not be found|Page Not Found/i);
    });

    test('404 page has navbar', async ({ page }) => {
      await page.goto(`sogo${v}/non-existent/`);
      await expect(page.locator('.navbar')).toBeVisible();
    });
  });
}

test.describe('404 pages (site root)', () => {
  test('404 page has back-to-home link', async ({ page }) => {
    await page.goto('non-existent/');

    // Should have a way to get back — the navbar brand links to the docs home
    const homeLinks = page.locator('.navbar__brand[href*="/sogo"]');
    expect(await homeLinks.count()).toBeGreaterThan(0);
  });
});
