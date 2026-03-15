/**
 * Sentry エラー収集
 * REACT_APP_SENTRY_DSN が設定されている場合のみ有効
 */
export function initSentry(): void {
  const dsn = process.env.REACT_APP_SENTRY_DSN;
  if (!dsn || process.env.NODE_ENV !== 'production') return;

  import('@sentry/react').then((Sentry) => {
    Sentry.init({
      dsn,
      environment: process.env.REACT_APP_ENV || 'production',
      tracesSampleRate: 0.1,
      integrations: [Sentry.browserTracingIntegration()],
    });
  });
}

export function captureException(error: Error, context?: Record<string, unknown>): void {
  if (process.env.REACT_APP_SENTRY_DSN) {
    import('@sentry/react').then((Sentry) => {
      Sentry.captureException(error, { extra: context });
    });
  }
}
