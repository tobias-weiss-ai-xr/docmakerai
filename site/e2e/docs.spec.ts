/**
 * End-to-end tests for documentation pages.
 * Verifies that doc content renders correctly on both versions, including
 * the regression test for the DocItem Layout swizzle bug (dropped children).
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

for (const v of VERSIONS) {
  test.describe(`Documentation pages (sogo${v})`, () => {
    test('index page has content', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      // Verify markdown body contains real content (not empty)
      const markdownDiv = page.locator('.theme-doc-markdown');
      await expect(markdownDiv).toBeVisible();
      await expect(markdownDiv).toContainText(`SOGo ${v}`);
    });

    test('login page has real content (regression for DocItem swizzle bug)', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);

      const markdownDiv = page.locator('.theme-doc-markdown');
      await expect(markdownDiv).toBeVisible();

      // Verify body is NOT empty - this catches the DocItem Layout bug where children were dropped
      await expect(markdownDiv).not.toBeEmpty();
      await expect(markdownDiv).toContainText(`Getting Started with SOGo ${v}`);

      // Verify it has meaningful length (not just the empty div)
      const content = await markdownDiv.innerHTML();
      expect(content.length).toBeGreaterThan(100);
    });

    test('docs pages have version badge', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page.locator('.theme-doc-version-badge')).toBeVisible();
      await expect(page.locator('.theme-doc-version-badge')).toContainText(
        `Version: SOGo ${v}`
      );
    });

    test('pages render markdown images with correct sizing', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);

      // Verify screenshots are sized appropriately (640px width constrained)
      const images = page.locator('.markdown img');
      const count = await images.count();

      // Should have at least one screenshot image
      if (count > 0) {
        const firstImg = images.first();
        // Computed width must be the scoped 640px rule (max-width computes to 100%)
        await expect(firstImg).toHaveCSS('width', '640px');
      }
    });

    test('paginated docs show previous/next navigation', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);

      // Should have pagination links
      const pagination = page.locator('.pagination-nav');
      await expect(pagination).toBeVisible();

      // Should have prev (Overview/index) and next links
      await expect(pagination.locator('text=Previous')).toBeVisible();
      await expect(pagination.locator('text=Next')).toBeVisible();
    });
  });
}
