/**
 * End-to-end tests for asset loading.
 * Verifies that CSS, JS, images, and fonts load correctly.
 */

import { test, expect } from '@playwright/test';

test.describe('Static assets', () => {
  test('main CSS loads', async ({ page }) => {
    await page.goto('/sogo5/');
    
    // Check that the main stylesheet is loaded
    const stylesheet = page.locator('link[rel="stylesheet"][href*="styles."]');
    await expect(stylesheet).toBeVisible();
    
    // Verify it doesn't return 404
    const href = await stylesheet.getAttribute('href');
    const response = await page.request.get(href);
    expect(response.status()).toBe(200);
  });

  test('main JS bundle loads', async ({ page }) => {
    await page.goto('/sogo5/');
    
    // Check that JS bundle is loaded
    const script = page.locator('script[src*="main."]');
    await expect(script).toBeVisible();
  });

  test('logo image loads', async ({ page }) => {
    await page.goto('/sogo5/');
    
    const logo = page.locator('.navbar__logo img');
    await expect(logo).toHaveAttribute('src', /logo\.svg/);
    
    const src = await logo.getAttribute('src');
    const response = await page.request.get(src);
    expect(response.status()).toBe(200);
  });

  test('favicon loads', async ({ page }) => {
    await page.goto('/sogo5/');
    
    const favicon = page.locator('link[rel="icon"]');
    await expect(favicon).toBeVisible();
    
    const href = await favicon.getAttribute('href');
    if (href) {
      const response = await page.request.get(href);
      expect(response.status()).toBeLessThan(400);
    }
  });

  test('social card image loads', async ({ page }) => {
    await page.goto('/sogo5/');
    
    const meta = page.locator('meta[property="og:image"]');
    await expect(meta).toBeVisible();
    
    const content = await meta.getAttribute('content');
    if (content && content.includes('http')) {
      const response = await page.request.get(content);
      expect(response.status()).toBeLessThan(400);
    }
  });
});
