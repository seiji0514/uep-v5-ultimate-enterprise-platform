/**
 * ダッシュボード・メインレイアウト E2E テスト
 * グローバル検索・テーマ切替・通知センター
 */
import { test, expect } from '@playwright/test';

test.describe('ダッシュボード（認証済み）', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/ユーザー名|username/i).fill('developer');
    await page.getByLabel(/パスワード|password/i).fill('dev123');
    await page.getByRole('button', { name: /ログイン|Login/i }).click();
    await expect(page).toHaveURL(/\/(?!login)/, { timeout: 10000 });
  });

  test('グローバル検索が表示される', async ({ page }) => {
    await expect(page.getByPlaceholder('ページを検索...')).toBeVisible({ timeout: 5000 });
  });

  test('グローバル検索でページを検索できる', async ({ page }) => {
    const searchInput = page.getByPlaceholder('ページを検索...');
    await searchInput.fill('MLOps');
    await expect(page.getByRole('listbox')).toBeVisible({ timeout: 3000 });
    await expect(page.getByText('MLOps')).toBeVisible();
  });

  test('テーマ切替ボタンが表示される', async ({ page }) => {
    const themeButton = page.getByRole('button', { name: /ライトモード|ダークモード/ });
    await expect(themeButton).toBeVisible({ timeout: 5000 });
  });

  test('通知センターが表示される', async ({ page }) => {
    const notifyButton = page.getByRole('button', { name: /通知/ });
    await expect(notifyButton).toBeVisible({ timeout: 5000 });
  });

  test('通知センターを開ける', async ({ page }) => {
    await page.getByRole('button', { name: /通知/ }).click();
    await expect(page.getByText('通知')).toBeVisible();
  });

  test('サイドバー折りたたみが動作する', async ({ page }) => {
    const collapseButton = page.getByRole('button', { name: /サイドバーを折りたたむ|サイドバーを展開/ });
    await expect(collapseButton).toBeVisible({ timeout: 5000 });
    await collapseButton.click();
    await expect(page.getByRole('navigation', { name: 'メインメニュー' })).toBeVisible();
  });
});
