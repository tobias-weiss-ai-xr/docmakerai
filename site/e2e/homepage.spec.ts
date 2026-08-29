/**
 * End-to-end tests for the docmakerai homepage and root routing.
 * Tests the landing page behavior and basic site structure.
 */

import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('root path redirects to /sogo5/', async ({ page }) => {
    await page.goto('/');
    // Should redirect to /sogo5/
    await expect(page).toHaveURL('/sogo5/');
  });

  test('redirect page shows SOGo User Guide loader', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('body')).toHaveCSS('background', 'rgb(27, 27, 47)');
    await expect(page.locator('p')).toContainText('Redirecting to');
    await expect(page.locator('a[href="./sogo5/"]')).toHaveText('SOGo User Guide');
  });

  test('SOGo 5 page loads successfully', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page).toHaveTitle(/SOGo/);
    // Should have main content
    await expect(page.locator('.theme-doc-markdown')).toBeVisible();
  });

  test('SOGo 6 page loads successfully', async ({ page }) => {
    await page.goto('/sogo6/');
    await expect(page).toHaveTitle(/SOGo/);
    await expect(page.locator('.theme-doc-markdown')).toBeVisible();
  });

  test('German (de) locale pages load', async ({ page }) => {
    await page.goto('/de/sogo5/');
    await expect(page).toHaveTitle(/SOGo/);
    // Should have sidebars and content
    await expect(page.locator('html')).toHaveAttribute('lang', 'de');
  });
});
