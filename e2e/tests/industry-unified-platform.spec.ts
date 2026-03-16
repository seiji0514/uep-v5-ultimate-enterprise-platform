/**
 * 産業統合プラットフォーム E2E テスト
 * 前提: バックエンド(9010)・フロントエンド(3010)を起動しておくこと
 * 実行: E2E_RUN_EXTERNAL_APPS=1 PLAYWRIGHT_BASE_URL=http://localhost:3010 npx playwright test industry-unified-platform
 */
import { test, expect } from '@playwright/test';

test.use({ baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3010' });

test.describe('産業統合プラットフォーム', () => {
  test.skip(
    () => process.env.E2E_RUN_EXTERNAL_APPS !== '1',
    '産業統合(3010)は別起動が必要。E2E_RUN_EXTERNAL_APPS=1 で実行'
  );

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const isLogin = await page.getByRole('heading', { name: /産業統合プラットフォーム/i }).isVisible().catch(() => false);
    if (isLogin) {
      await page.getByLabel('ユーザー名').fill('kaho0525');
      await page.getByLabel('パスワード').fill('0525');
      await page.getByRole('button', { name: /ログイン/ }).click();
      await expect(page.getByText(/製造・IoT|医療|金融|セキュリティ/)).toBeVisible({ timeout: 10000 });
    }
  });

  test('ログインページが表示される', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: /産業統合プラットフォーム/i })).toBeVisible();
    await expect(page.getByLabel('ユーザー名')).toBeVisible();
    await expect(page.getByLabel('パスワード')).toBeVisible();
  });

  test('ログイン後にメイン画面が表示される', async ({ page }) => {
    await page.goto('/');
    await page.getByLabel('ユーザー名').fill('kaho0525');
    await page.getByLabel('パスワード').fill('0525');
    await page.getByRole('button', { name: /ログイン/ }).click();
    await expect(page.getByText(/製造・IoT|要対応サマリ|シミュレーション/)).toBeVisible({ timeout: 10000 });
  });

  test('ドメインタブが表示される', async ({ page }) => {
    await expect(page.getByText(/製造|医療|金融|セキュリティ|要対応/).first()).toBeVisible({ timeout: 5000 });
  });

  test('タブ切り替えができる', async ({ page }) => {
    const tab = page.getByRole('tab').first();
    await expect(tab).toBeVisible({ timeout: 5000 });
    await tab.click();
    await expect(page.getByRole('tabpanel')).toBeVisible({ timeout: 3000 });
  });

  test('シミュレーションモードが表示される', async ({ page }) => {
    await expect(page.getByText(/シミュレーション|手動|自動/).first()).toBeVisible({ timeout: 5000 });
  });

  test('ログアウトボタンが表示される', async ({ page }) => {
    await expect(page.getByRole('button', { name: /ログアウト/ })).toBeVisible();
  });
});
