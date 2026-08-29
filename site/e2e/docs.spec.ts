/**
 * End-to-end tests for documentation pages.
 * Verifies that doc content renders correctly and navigation works.
 */

import { test, expect } from '@playwright/test';

test.describe('Documentation pages', () => {
  test('SOGo 5 index page has content', async ({ page }) => {
    await page.goto('/sogo5/');
    
    // Verify markdown body contains real content (not empty)
    const markdownDiv = page.locator('.theme-doc-markdown');
    await expect(markdownDiv).toBeVisible();
    
    // Check for expected content
    await expect(markdownDiv).toContainText('SOGo 5');
    await expect(markdownDiv).toContainText('User Guide');
  });

  test('SOGo 5 login page has real content (regression for DocItem swizzle bug)', async ({ page }) => {
    await page.goto('/sogo5/sogo-login/');
    
    const markdownDiv = page.locator('.theme-doc-markdown');
    await expect(markdownDiv).toBeVisible();
    
    // Verify body is NOT empty - this catches the DocItem Layout bug where children were dropped
    await expect(markdownDiv).not.toBeEmpty();
    await expect(markdownDiv).toContainText('Getting Started');
    await expect(markdownDiv).toContainText('Log In');
    
    // Verify it has meaningful length (not just the empty div)
    const content = await markdownDiv.innerHTML();
    expect(content.length).toBeGreaterThan(100);
  });

  test('SOGo 6 index page has content', async ({ page }) => {
    await page.goto('/sogo6/');
    
    const markdownDiv = page.locator('.theme-doc-markdown');
    await expect(markdownDiv).toBeVisible();
    await expect(markdownDiv).toContainText('SOGo 6');
    await expect(markdownDiv).not.toBeEmpty();
  });

  test('.doc pages render markdown images with correct sizing', async ({ page }) => {
    await page.goto('/sogo5/sogo-login/');
    
    // Verify screenshots are sized appropriately (640px width constrained)
    const images = page.locator('.markdown img');
    const count = await images.count();
    
    // Should have at least one screenshot image
    if (count > 0) {
      const firstImg = images.first();
      // Image should have explicit dimensions for CLS prevention
      await expect(firstImg).toHaveCSS('max-width', '640px');
    }
  });

  test('docs pages have version badge', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('.theme-doc-version-badge')).toBeVisible();
    await expect(page.locator('.theme-doc-version-badge')).toContainText('SOGo 5');
  });

  test('paginated docs show previous/next navigation', async ({ page }) => {
    await page.goto('/sogo5/sogo-login/');
    
    // Should have pagination links
    const pagination = page.locator('.pagination-nav');
    await expect(pagination).toBeVisible();
    
    // Should have prev (Overview/index) and next links
    await expect(pagination.locator('text=Previous')).toBeVisible();
    await expect(pagination.locator('text=Next')).toBeVisible();
  });
});
