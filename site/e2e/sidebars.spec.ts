/**
 * End-to-end tests for sidebar navigation.
 * The two versions use different information architectures, so the
 * category names are per-version data; the structural checks are shared.
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

/** Core categories each version's sidebar must expose. */
const CATEGORIES: Record<(typeof VERSIONS)[number], string[]> = {
  '5': ['Getting Started', 'Basics', 'Calendar', 'Mail', 'Contacts'],
  '6': [
    '🚀 Quick Start',
    '📧 Daily Workflows',
    '📅 Calendar Management',
    '📨 Mail Organization',
    '👥 Contacts Management',
  ],
};

for (const v of VERSIONS) {
  test.describe(`Sidebar navigation (sogo${v})`, () => {
    test('sidebar is visible', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page.locator('.theme-doc-sidebar-container')).toBeVisible();
    });

    test('sidebar shows the core categories', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      const sidebar = page.locator('.theme-doc-sidebar-container');
      for (const category of CATEGORIES[v]) {
        await expect(sidebar.getByText(category)).toBeVisible();
      }
    });

    test('sidebar links point to real pages and mark the active one', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);

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
      const target = hrefs.find((h) => h && h.includes(`/sogo${v}/`))!;
      const response = await page.request.get(target);
      expect(response.status()).toBe(200);
    });

    test('sidebar has collapsed categories', async ({ page }) => {
      await page.goto(`sogo${v}/`);

      // Find a collapsed category (should have the collapsed class)
      const category = page.locator('.menu__list-item--collapsed').first();
      expect(await category.count()).toBeGreaterThan(0);
    });

    test('On This Page TOC is visible', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);
      await expect(page.locator('.theme-doc-toc-desktop')).toBeVisible();
    });

    test('TOC has heading links', async ({ page }) => {
      await page.goto(`sogo${v}/sogo-login/`);
      const tocLinks = page.locator('.table-of-contents__link');
      expect(await tocLinks.count()).toBeGreaterThan(0);
    });
  });
}
