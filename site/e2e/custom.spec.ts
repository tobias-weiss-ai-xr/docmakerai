/**
 * End-to-end tests for custom components.
 * Verifies that custom React components render without breaking the page.
 */

import { test, expect } from '@playwright/test';

test.describe('Custom components', () => {
  test('DocVoteWidget renders on doc pages that use it', async ({ page }) => {
    // DocVoteWidget may be used in some doc pages
    // If it exists, it should not cause errors
    const voteWidget = page.locator('.DocVoteWidget');
    
    // Try a page that might use DocVoteWidget
    await page.goto('sogo5/sogo-calendar-create-event/');
    
    // If the widget is on the page, verify it renders
    const count = await voteWidget.count();
    if (count > 0) {
      await expect(voteWidget).toBeVisible();
    }
    
    // Main content should still render regardless
    await expect(page.locator('.theme-doc-markdown')).not.toBeEmpty();
  });

  test('pages with PageSEO component don\'t have rendering errors', async ({ page }) => {
    // Documents that use PageSEO (most of them) should render fine
    await page.goto('sogo5/sogo-login/');
    
    // Check that meta tags are present (PageSEO adds them)
    const metaDescription = page.locator('meta[name="description"]');
    await expect(metaDescription).toHaveAttribute('content', /SOGo/);
    
    // Page should render normally
    await expect(page.locator('.theme-doc-markdown')).toBeVisible();
  });

  test('VideoFallback component (if present) renders without errors', async ({ page }) => {
    // If any page uses VideoFallback, it should not break
    await page.goto('sogo5/');
    
    // The page should still be functional
    await expect(page.locator('body')).not.toHaveText('Error');
  });

  test('SEO meta tags are present on doc pages', async ({ page }) => {
    await page.goto('sogo5/');

    // Head elements are never "visible" — assert attachment.
    await expect(page.locator('meta[name="description"]')).toBeAttached();
    await expect(page.locator('meta[property="og:title"]')).toBeAttached();
    await expect(page.locator('meta[property="og:image"]')).toBeAttached();
    await expect(page.locator('meta[name="twitter:card"]')).toBeAttached();
  });
});
