/**
 * Playwright E2E テスト設定
 * UEP v5.0 + 統合セキュリティ・防衛・産業統合・EOH
 */
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
  // PLAYWRIGHT_BASE_URL が設定されている場合は既存サーバー利用（webServer を起動しない）
  webServer: process.env.PLAYWRIGHT_BASE_URL
    ? undefined
    : {
        command: 'cd ../frontend && npm run start',
        url: 'http://localhost:3000',
        reuseExistingServer: !process.env.CI,
        timeout: 120 * 1000,
      },
});
