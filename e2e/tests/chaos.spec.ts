/**
 * Chaos Engineering ページ E2E テスト
 */
import { test, expect } from '@playwright/test';

test.describe('Chaos Engineering ページ', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/ユーザー名|username/i).fill('developer');
    await page.getByLabel(/パスワード|password/i).fill('dev123');
    await page.getByRole('button', { name: /ログイン|Login/i }).click();
    await expect(page).toHaveURL(/\/(?!login)/, { timeout: 10000 });
  });

  test('Chaos ページに遷移できる', async ({ page }) => {
    await page.goto('/chaos');
    await expect(page.getByText(/カオスエンジニアリング|Chaos/i)).toBeVisible({ timeout: 10000 });
  });

  test('遅延シナリオのUIが表示される', async ({ page }) => {
    await page.goto('/chaos');
    await expect(page.getByText(/遅延注入|遅延|delay/i)).toBeVisible({ timeout: 10000 });
  });
});
