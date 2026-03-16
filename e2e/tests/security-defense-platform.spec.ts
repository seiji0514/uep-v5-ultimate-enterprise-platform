/**
 * 統合セキュリティ・防衛プラットフォーム E2E テスト
 * 前提: バックエンド(9001)・フロントエンド(3001)を起動しておくこと
 * 実行: E2E_RUN_EXTERNAL_APPS=1 PLAYWRIGHT_BASE_URL=http://localhost:3001 npx playwright test security-defense-platform
 */
import { test, expect } from '@playwright/test';

test.use({ baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3001' });

test.describe('統合セキュリティ・防衛プラットフォーム', () => {
  test.skip(
    () => process.env.E2E_RUN_EXTERNAL_APPS !== '1',
    'セキュリティ防衛(3001)は別起動が必要。E2E_RUN_EXTERNAL_APPS=1 で実行'
  );

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const isLogin = await page.getByRole('heading', { name: /統合セキュリティ・防衛/i }).isVisible().catch(() => false);
    if (isLogin) {
      await page.getByLabel('ユーザー名').fill('kaho0525');
      await page.getByLabel('パスワード').fill('0525');
      await page.getByRole('button', { name: /ログイン/ }).click();
      await expect(page.getByText(/セキュリティ監視|イベント|インシデント/)).toBeVisible({ timeout: 10000 });
    }
  });

  test('ログインページが表示される', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: /統合セキュリティ・防衛/i })).toBeVisible();
    await expect(page.getByLabel('ユーザー名')).toBeVisible();
    await expect(page.getByLabel('パスワード')).toBeVisible();
  });

  test('ログイン後にダッシュボードが表示される', async ({ page }) => {
    await page.goto('/');
    await page.getByLabel('ユーザー名').fill('kaho0525');
    await page.getByLabel('パスワード').fill('0525');
    await page.getByRole('button', { name: /ログイン/ }).click();
    await expect(page.getByText(/セキュリティ監視・インシデント対応・リスク分析/)).toBeVisible({ timeout: 10000 });
  });

  test('イベントタブが表示される', async ({ page }) => {
    await expect(page.getByRole('tab', { name: /イベント/ })).toBeVisible();
  });

  test('インシデントタブに切り替えられる', async ({ page }) => {
    await page.getByRole('tab', { name: /インシデント/ }).click();
    await expect(page.getByRole('tabpanel')).toBeVisible();
  });

  test('脅威インテリタブでIOC照合が表示される', async ({ page }) => {
    await page.getByRole('tab', { name: /脅威インテリ/ }).click();
    await expect(page.getByText(/IOC 照合|脅威インテリジェンス/)).toBeVisible({ timeout: 5000 });
  });

  test('ログアウトボタンが表示される', async ({ page }) => {
    await expect(page.getByRole('button', { name: /ログアウト/ })).toBeVisible();
  });
});
