import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import './i18n';
import App from './App';
import { registerSW } from './lib/pwa-register';
import { initSentry } from './lib/sentry';
import reportWebVitals, { sendToAnalytics } from './reportWebVitals';
import { ErrorBoundary } from './components/ErrorBoundary';
import { OfflineBanner } from './components/common/OfflineBanner';

initSentry();

// MSW モック（REACT_APP_ENABLE_MSW=true のときのみ）
if (process.env.NODE_ENV === 'development' && process.env.REACT_APP_ENABLE_MSW === 'true') {
  import('./mocks/browser').then(({ worker }) => {
    worker.start({ onUnhandledRequest: 'bypass' });
  });
}

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <ErrorBoundary>
    <OfflineBanner />
    <App />
  </ErrorBoundary>
);

// PWA Service Worker 登録
registerSW();

// Web Vitals パフォーマンス計測（コンソール・将来はダッシュボード送信）
reportWebVitals(sendToAnalytics);
