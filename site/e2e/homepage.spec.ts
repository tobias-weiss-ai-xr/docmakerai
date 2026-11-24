/**
 * End-to-end tests for the docmakerai homepage and root routing.
 * Site-level behavior (landing page, locales) stays single;
 * per-version landing pages are checked for both versions.
 */

import { test, expect } from '@playwright/test';
import { VERSIONS } from './versions';

test.describe('Homepage', () => {
  test('root serves the project landing page (no redirect)', async ({ page }) => {
    await page.goto('.');
    await expect(page).toHaveURL(/docmakerai\/$/);
    await expect(page.locator('.landing')).toBeVisible();
    await expect(page).toHaveTitle(/SOGo User Guide/);
  });

  test('landing page introduces the project and links to its nucleus + suite', async ({ page }) => {
    await page.goto('.');
    const landing = page.locator('.landing');

    // The lead introduces DocMaker AI / the project
    await expect(landing.getByText(/DocMaker AI/i).first()).toBeVisible();

    // SOGo 5 is the nucleus of the project
    const nucleus = landing.getByRole('link', { name: /SOGo 5 User Guide/ });
    await expect(nucleus).toBeVisible();
    await expect(nucleus).toHaveAttribute('href', /\/docmakerai\/sogo5\/$/);
    await expect(landing.getByText(/nucleus of this project/i).first()).toBeVisible();

    // openEduSuite card links to the suite
    const suite = landing.getByRole('link', { name: /openEduSuite/ });
    await expect(suite).toBeVisible();
    await expect(suite).toHaveAttribute('href', /\/docmakerai\/suite\/?$/);

    // Secondary entry: SOGo 6
    await expect(
      landing.getByRole('link', { name: /SOGo 6/ })
    ).toBeVisible();
  });

  test('landing page cards navigate to their destinations', async ({ page }) => {
    await page.goto('.');
    await page.locator('.landing-card--nucleus').click();
    await page.waitForURL('**/docmakerai/sogo5/');
    await expect(page.locator('.theme-doc-markdown')).toBeVisible();

    await page.goto('.');
    await page.locator('.landing-card--suite').click();
    await page.waitForURL('**/docmakerai/suite/');
    await expect(page.locator('.theme-doc-markdown')).toBeVisible();
  });

  test('German landing page loads', async ({ page }) => {
    await page.goto('de/');
    await expect(page.locator('.landing')).toBeVisible();
    await expect(page.locator('html')).toHaveAttribute('lang', 'de');
    // Same two doors in German
    await expect(
      page.locator('.landing').getByRole('link', { name: /SOGo 5 Benutzerhandbuch/ })
    ).toBeVisible();
    await expect(
      page.locator('.landing').getByRole('link', { name: /openEduSuite/ })
    ).toBeVisible();
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
