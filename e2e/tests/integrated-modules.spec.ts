/**
 * 6モジュール概要・現場AIエージェント E2E テスト
 */
import { test, expect } from '@playwright/test';

test.describe('6モジュール概要・現場AIエージェント', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/ユーザー名|username/i).fill('developer');
    await page.getByLabel(/パスワード|password/i).fill('dev123');
    await page.getByRole('button', { name: /ログイン|Login/i }).click();
    await expect(page).toHaveURL(/\/(?!login)/, { timeout: 10000 });
  });

  test('6モジュール概要ページに遷移できる', async ({ page }) => {
    await page.goto('/integrated-modules');
    await expect(page).toHaveURL(/integrated-modules/);
    await expect(page.getByText(/統合基盤モジュール|6つのモジュール/)).toBeVisible({ timeout: 5000 });
  });

  test('6モジュール概要で製造・医療・金融が表示される', async ({ page }) => {
    await page.goto('/integrated-modules');
    await expect(page.getByText(/製造|医療|金融|障害者雇用|契約|物流/)).toBeVisible({ timeout: 5000 });
  });

  test('現場AIエージェントページに遷移できる', async ({ page }) => {
    await page.goto('/field-agent');
    await expect(page).toHaveURL(/field-agent/);
    await expect(page.getByText(/現場AIエージェント|製造|医療|物流/)).toBeVisible({ timeout: 5000 });
  });

  test('現場AIエージェントでタブ切り替えができる', async ({ page }) => {
    await page.goto('/field-agent');
    await expect(page.getByRole('tab', { name: /製造|医療|物流/ })).toBeVisible({ timeout: 5000 });
    await page.getByRole('tab', { name: /医療/ }).click();
    await expect(page.getByText(/医療|異常|プラットフォーム/)).toBeVisible({ timeout: 3000 });
  });
});
