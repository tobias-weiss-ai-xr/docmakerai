/**
 * End-to-end tests for sidebar navigation.
 * Verifies that sidebar categories and links work correctly.
 */

import { test, expect } from '@playwright/test';

test.describe('Sidebar navigation', () => {
  test('sidebar is visible on SOGo 5 docs', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('.theme-doc-sidebar-container')).toBeVisible();
  });

  test('sidebar has Getting Started category', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('text=Getting Started')).toBeVisible();
  });

  test('sidebar has Calendar category', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('text=Calendar')).toBeVisible();
  });

  test('sidebar has Mail category', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('text=Mail')).toBeVisible();
  });

  test('sidebar has Contacts category', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('text=Contacts')).toBeVisible();
  });

  test('sidebar links navigate to correct pages', async ({ page }) => {
    await page.goto('/sogo5/');
    
    // Click on a sidebar link
    await page.locator('text=Getting Started').first().click();
    await page.waitForURL('/sogo5/sogo-login/');
    
    // Verify we're on the correct page
    await expect(page).toHaveURL('/sogo5/sogo-login/');
    await expect(page.locator('.theme-doc-markdown')).toContainText('Getting Started');
  });

  test('sidebar collapses categories', async ({ page }) => {
    await page.goto('/sogo5/');
    
    // Find a collapsed category (should have the collapsed class)
    const category = page.locator('.menu__list-item--collapsed').first();
    expect(await category.count()).toBeGreaterThan(0);
  });

  test('sidebar On This Page TOC is visible', async ({ page }) => {
    await page.goto('/sogo5/sogo-login/');
    await expect(page.locator('.theme-doc-toc-desktop')).toBeVisible();
  });

  test('TOC has heading links', async ({ page }) => {
    await page.goto('/sogo5/sogo-login/');
    const tocLinks = page.locator('.table-of-contents__link');
    await expect(tocLinks).toHaveCount(1);
  });
});
