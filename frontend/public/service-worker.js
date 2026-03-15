/**
 * UEP v5.0 Service Worker
 * オフライン時のメッセージ表示・キャッシュ
 */
const CACHE_NAME = 'uep-v5-cache-v1';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// ナビゲーションリクエストのみオフライン時に対応（APIは通常のfetchで失敗）
self.addEventListener('fetch', (event) => {
  if (event.request.mode !== 'navigate') return;
  event.respondWith(
    fetch(event.request).catch(() => {
      return new Response(
        '<!DOCTYPE html><html><head><meta charset="utf-8"><title>オフライン</title></head><body>オフラインです。接続を確認してから再試行してください。</body></html>',
        { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
      );
    })
  );
});
