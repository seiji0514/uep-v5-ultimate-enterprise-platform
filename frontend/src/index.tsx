import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import './i18n';
import App from './App';
import { registerSW } from './lib/pwa-register';
import reportWebVitals from './reportWebVitals';
import { ErrorBoundary } from './components/ErrorBoundary';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);

// PWA Service Worker 登録
registerSW();

// Web Vitals パフォーマンス計測
reportWebVitals();
