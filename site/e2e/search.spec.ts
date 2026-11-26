/**
 * End-to-end tests for the offline local search.
 */
import { test, expect } from '@playwright/test';

test.describe('Local search', () => {
  test('search page loads for English', async ({ page }) => {
    await page.goto('search/?q=calendar');
    await expect(page.locator('h1')).toContainText(/Search results for "calendar"/i);
    await expect(page.locator('body')).toContainText(/documents found/i);
    await expect(page.locator('a[href*="/sogo5/"]').first()).toBeVisible();
  });

  test('search page loads for German', async ({ page }) => {
    await page.goto('de/search/?q=kalender');
    await expect(page.locator('h1')).toContainText(/kalender/i);
    await expect(page.locator('body')).toContainText(/Treffer|Ergebnisse|Dokumente/i);
  });

  test('navbar exposes the search input', async ({ page }) => {
    await page.goto('sogo5/');
    await expect(page.locator('input[aria-label="Search"]')).toBeVisible();
  });
});
