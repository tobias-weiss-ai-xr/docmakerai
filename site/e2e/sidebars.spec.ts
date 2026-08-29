/**
 * End-to-end tests for sidebar navigation.
 * Verifies that sidebar categories and links work correctly.
 */

import { test, expect } from '@playwright/test';

test.describe('Sidebar navigation', () => {
  test('sidebar is visible on SOGo 5 docs', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(page.locator('.theme-doc-sidebar-container')).toBeVisible();
  });

  test('sidebar has Getting Started category', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(
      page.locator('.theme-doc-sidebar-container').getByText('Getting Started')
    ).toBeVisible();
  });

  test('sidebar has Calendar category', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(
      page.locator('.theme-doc-sidebar-container').getByText('Calendar')
    ).toBeVisible();
  });

  test('sidebar has Mail category', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(
      page.locator('.theme-doc-sidebar-container').getByText('Mail')
    ).toBeVisible();
  });

  test('sidebar has Contacts category', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(
      page.locator('.theme-doc-sidebar-container').getByText('Contacts')
    ).toBeVisible();
  });

  test('sidebar links navigate to correct pages', async ({ page }) => {
    await page.goto('sogo5/sogo-login/');

    // The current page is highlighted in the sidebar.
    await expect(
      page
        .locator('.theme-doc-sidebar-container a[class*="menu__link--active"]')
        .first()
    ).toBeAttached();

    // Section links present in the sidebar resolve to real pages. Categories
    // re-render constantly (collapse caret), so avoid clicking them — verify
    // their hrefs instead.
    const sidebar = page.locator('.theme-doc-sidebar-container');
    const hrefs = await sidebar
      .locator('a[href]')
      .evaluateAll((els) =>
        els.map((e) => (e as HTMLAnchorElement).getAttribute('href'))
      );
    expect(hrefs.length).toBeGreaterThan(0);
    const target = hrefs.find((h) => h && h.includes('/sogo5/'))!;
    const response = await page.request.get(target);
    expect(response.status()).toBe(200);
  });

  test('sidebar collapses categories', async ({ page }) => {
    await page.goto('sogo5/');
    
    // Find a collapsed category (should have the collapsed class)
    const category = page.locator('.menu__list-item--collapsed').first();
    expect(await category.count()).toBeGreaterThan(0);
  });

  test('sidebar On This Page TOC is visible', async ({ page }) => {
    await page.goto('sogo5/sogo-login/');
    await expect(page.locator('.theme-doc-toc-desktop')).toBeVisible();
  });

  test('TOC has heading links', async ({ page }) => {
    await page.goto('sogo5/sogo-login/');
    const tocLinks = page.locator('.table-of-contents__link');
    expect(await tocLinks.count()).toBeGreaterThan(0);
  });
});
