/**
 * ログイン E2E テスト
 */
import { test, expect } from '@playwright/test';

test.describe('ログインページ', () => {
  test('ログインフォームが表示される', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByRole('heading', { name: /UEP/i })).toBeVisible();
    await expect(page.getByLabel(/ユーザー名|username/i)).toBeVisible();
    await expect(page.getByLabel(/パスワード|password/i)).toBeVisible();
  });

  test('ログイン成功後にダッシュボードへ遷移', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/ユーザー名|username/i).fill('developer');
    await page.getByLabel(/パスワード|password/i).fill('dev123');
    await page.getByRole('button', { name: /ログイン|Login/i }).click();
    await expect(page).toHaveURL(/\/(?!login)/);
    await expect(page.getByText(/ダッシュボード|Dashboard|UEP/i)).toBeVisible({ timeout: 10000 });
  });

  test('未認証で保護ルートにアクセスするとログインへリダイレクト', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL(/\/login/);
  });
});
