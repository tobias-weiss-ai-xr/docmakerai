/**
 * End-to-end tests for asset loading.
 * Verifies that CSS, JS, images, and fonts load correctly on both versions.
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

for (const v of VERSIONS) {
  test.describe(`Static assets (sogo${v})`, () => {
    test('main CSS loads', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      // <link> lives in <head> — never "visible", assert attachment instead.
      const stylesheet = page.locator('link[rel="stylesheet"][href*="styles."]');
      await expect(stylesheet).toBeAttached();

      // Verify it doesn't return 404
      const href = await stylesheet.getAttribute('href');
      const response = await page.request.get(href);
      expect(response.status()).toBe(200);
    });

    test('main JS bundle loads', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      // Docusaurus 3 emits hashed bundles under /assets/js/ (no more main.*.js).
      const script = page.locator('script[src*="/assets/js/"]');
      await expect(script.first()).toBeAttached();
    });

    test('logo image loads', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      const logo = page.locator('.navbar__logo img').first();
      await expect(logo).toHaveAttribute('src', /logo\.svg/);

      const src = await logo.getAttribute('src');
      const response = await page.request.get(src);
      expect(response.status()).toBe(200);
    });

    test('favicon loads', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      const favicon = page.locator('link[rel*="icon"]');
      await expect(favicon.first()).toBeAttached();

      const href = await favicon.first().getAttribute('href');
      if (href) {
        const response = await page.request.get(href);
        expect(response.status()).toBeLessThan(400);
      }
    });

    test('social card image loads', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      const meta = page.locator('meta[property="og:image"]');
      await expect(meta).toBeAttached();

      const content = await meta.getAttribute('content');
      if (content && content.includes('http')) {
        const response = await page.request.get(content);
        expect(response.status()).toBeLessThan(400);
      }
    });
  });
}
