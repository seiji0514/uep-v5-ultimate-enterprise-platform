/**
 * 企業横断オペレーション基盤（EOH）E2E テスト
 * 前提: バックエンド(9020)・フロントエンド(3020)を起動しておくこと
 * 実行: E2E_RUN_EXTERNAL_APPS=1 PLAYWRIGHT_BASE_URL=http://localhost:3020 npx playwright test enterprise-operations-hub
 */
import { test, expect } from '@playwright/test';

test.use({ baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3020' });

test.describe('企業横断オペレーション基盤（EOH）', () => {
  test.skip(
    () => process.env.E2E_RUN_EXTERNAL_APPS !== '1',
    'EOH(3020)は別起動が必要。E2E_RUN_EXTERNAL_APPS=1 で実行'
  );

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const isLogin = await page.getByRole('heading', { name: /企業横断オペレーション基盤/i }).isVisible().catch(() => false);
    if (isLogin) {
      await page.getByLabel('ユーザー名').fill('kaho0525');
      await page.getByLabel('パスワード').fill('0525');
      await page.getByRole('button', { name: /ログイン/ }).click();
      await expect(page.getByText(/観測|タスク|リスク|要対応/)).toBeVisible({ timeout: 10000 });
    }
  });

  test('ログインページが表示される', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: /企業横断オペレーション基盤/i })).toBeVisible();
    await expect(page.getByLabel('ユーザー名')).toBeVisible();
    await expect(page.getByLabel('パスワード')).toBeVisible();
  });

  test('ログイン後にダッシュボードが表示される', async ({ page }) => {
    await page.goto('/');
    await page.getByLabel('ユーザー名').fill('kaho0525');
    await page.getByLabel('パスワード').fill('0525');
    await page.getByRole('button', { name: /ログイン/ }).click();
    await expect(page.getByText(/要対応・タスク・リスク サマリ|観測|タスク|リスク/)).toBeVisible({ timeout: 10000 });
  });

  test('観測タブが表示される', async ({ page }) => {
    await expect(page.getByRole('tab', { name: /観測/ })).toBeVisible();
  });

  test('タスクタブに切り替えられる', async ({ page }) => {
    await page.getByRole('tab', { name: /タスク/ }).click();
    await expect(page.getByRole('tabpanel')).toBeVisible();
  });

  test('タスク追加フォームが表示される（admin/operator）', async ({ page }) => {
    await page.getByRole('tab', { name: /タスク/ }).click();
    const addForm = page.getByText(/タスク追加|タイトル/);
    await expect(addForm.first()).toBeVisible({ timeout: 5000 });
  });

  test('リスクタブに切り替えられる', async ({ page }) => {
    await page.getByRole('tab', { name: /リスク/ }).click();
    await expect(page.getByRole('tabpanel')).toBeVisible();
  });

  test('アラートタブが表示される', async ({ page }) => {
    await expect(page.getByRole('tab', { name: /アラート/ })).toBeVisible();
  });

  test('ログアウトボタンが表示される', async ({ page }) => {
    await expect(page.getByRole('button', { name: /ログアウト/ })).toBeVisible();
  });
});
