/**
 * End-to-end tests for navbar behavior.
 * Verifies logo sizing and navigation links work correctly.
 */

import { test, expect } from '@playwright/test';

test.describe('Navbar', () => {
  test('navbar is visible on all pages', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('.navbar')).toBeVisible();
  });

  test('logo is not oversized (regression for global img rule)') , async ({ page }) => {
    await page.goto('/sogo5/');
    
    const logo = page.locator('.navbar__logo img');
    await expect(logo).toBeVisible();
    
    // Logo must be constrained to reasonable size (max-height: 2rem = 32px)
    // This catches the bug where global img {width:640px; height:400px} blew up the logo
    const { width, height } = await logo.boundingBox();
    
    // Logo should be at most ~40px (2rem) in either dimension
    expect(width, 'Logo width should be <= 40px').toBeLessThanOrEqual(40);
    expect(height, 'Logo height should be <= 40px').toBeLessThanOrEqual(40);
    
    // Should never be the 640px that the old global rule forced
    expect(width, 'Logo width should not be 640px').not.toBe(640);
    expect(height, 'Logo height should not be 400px').not.toBe(400);
  });

  test('logo alt text refers to SOGo', async ({ page }) => {
    await page.goto('/sogo5/');
    const logo = page.locator('.navbar__logo img');
    await expect(logo).toHaveAttribute('alt', /SOGo/);
  });

  test('navbar brand links to SOGo 5 docs', async ({ page }) => {
    await page.goto('/sogo5/');
    const brandLink = page.locator('.navbar__brand');
    await expect(brandLink).toHaveAttribute('href', '/sogo5/');
  });

  test('navbar has Docs/Tutorials links', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('text=Docs')).toBeVisible();
    await expect(page.locator('text=Tutorials')).toBeVisible();
  });

  test('navbar has GitHub link', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('text=GitHub')).toBeVisible();
  });

  test('navbar has version dropdown', async ({ page }) => {
    await page.goto('/sogo5/');
    
    // Version dropdown should show SOGo 5 and SOGo 6
    await expect(page.locator('text=SOGo 5')).toBeVisible();
    await expect(page.locator('text=SOGo 6')).toBeVisible();
  });

  test('navbar has language dropdown', async ({ page }) => {
    await page.goto('/sogo5/');
    await expect(page.locator('text=English')).toBeVisible();
    await expect(page.locator('text=Deutsch')).toBeVisible();
  });

  test('navbar toggle exists on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // Mobile
    await page.goto('/sogo5/');
    await expect(page.locator('.navbar__toggle')).toBeVisible();
  });
});
