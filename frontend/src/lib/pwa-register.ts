/**
 * PWA Service Worker 登録（Workbox）
 * 補強スキル: PWA、オフライン対応
 */
export function registerSW(): void {
  if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/service-worker.js')
        .then((reg) => console.log('SW registered', reg.scope))
        .catch((err) => console.warn('SW registration failed', err));
    });
  }
}
