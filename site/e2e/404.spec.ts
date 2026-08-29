/**
 * End-to-end tests for 404 page handling.
 * Verifies that non-existent pages show a helpful 404 page.
 */

import { test, expect } from '@playwright/test';

test.describe('404 pages', () => {
  test('non-existent page returns 404', async ({ page }) => {
    const response = await page.goto('sogo5/this-page-does-not-exist/');
    expect(response?.status()).toBe(404);
  });

  test('404 page has helpful content', async ({ page }) => {
    await page.goto('sogo5/non-existent/');
    
    // Docusaurus 404 page should have some content
    await expect(page.locator('h1')).toBeVisible();
  });

  test('404 page has navbar', async ({ page }) => {
    await page.goto('sogo5/non-existent/');
    
    // Even 404 pages should have navigation
    await expect(page.locator('.navbar')).toBeVisible();
  });

  test('404 page has back-to-home link', async ({ page }) => {
    await page.goto('non-existent/');

    // Should have a way to get back — the navbar brand links to the docs home
    const homeLinks = page.locator('.navbar__brand[href*="/sogo5"]');
    expect(await homeLinks.count()).toBeGreaterThan(0);
  });
});
