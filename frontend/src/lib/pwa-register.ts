/**
 * PWA Service Worker 登録
 * オフライン対応・オフライン時のメッセージ表示
 */
export function registerSW(): void {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/service-worker.js')
        .then((reg) => console.log('[UEP] Service Worker registered', reg.scope))
        .catch((err) => console.warn('[UEP] Service Worker registration failed', err));
    });
  }
}
