/**
 * End-to-end tests for the docmakerai homepage and root routing.
 * Site-level behavior (redirect shell, locales) stays single;
 * per-version landing pages are checked for both versions.
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

test.describe('Homepage', () => {
  test('root path redirects to /sogo5/', async ({ page }) => {
    await page.goto('.');
    // Shell redirects (meta refresh) into the project base path
    await page.waitForURL('**/docmakerai/sogo5/');
    await expect(page).toHaveURL(/docmakerai\/sogo5\/$/);
  });

  test('redirect page shows SOGo User Guide loader', async ({ page }) => {
    // The meta refresh fires instantly in a browser — verify the shell HTML
    // deterministically via the response body instead of racing the redirect.
    const response = await page.request.get('.');
    const html = await response.text();
    expect(html).toContain('Redirecting to');
    expect(html).toContain('href="./sogo5/"');
    expect(html).toContain('SOGo User Guide');
    expect(html).toContain('background: #1b1b2f');
  });

  test('German (de) locale pages load', async ({ page }) => {
    await page.goto('de/sogo5/');
    await expect(page).toHaveTitle(/SOGo/);
    // Should have sidebars and content
    await expect(page.locator('html')).toHaveAttribute('lang', 'de');
  });
});

for (const v of VERSIONS) {
  test.describe(`Homepage (sogo${v})`, () => {
    test('version landing page loads with content', async ({ page }) => {
      await page.goto(`sogo${v}/`);
      await expect(page).toHaveTitle(/SOGo/);
      await expect(page.locator('.theme-doc-markdown')).toBeVisible();
    });
  });
}
