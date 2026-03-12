/**
 * i18n 設定（react-i18next）
 * 補強スキル: 多言語対応（日本語/英語）
 */
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  ja: {
    translation: {
      welcome: 'UEP v5.0 へようこそ',
      login: 'ログイン',
      logout: 'ログアウト',
      dashboard: 'ダッシュボード',
      settings: '設定',
    },
  },
  en: {
    translation: {
      welcome: 'Welcome to UEP v5.0',
      login: 'Login',
      logout: 'Logout',
      dashboard: 'Dashboard',
      settings: 'Settings',
    },
  },
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'ja',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;
