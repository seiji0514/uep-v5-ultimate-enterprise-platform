import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/UEP|Enterprise|Platform/i);
});

test('login page accessible', async ({ page }) => {
  await page.goto('/login');
  await expect(page.getByRole('heading', { name: /ログイン|login/i })).toBeVisible({ timeout: 10000 });
});
