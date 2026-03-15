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
      search: 'ページを検索...',
      notifications: '通知',
      themeDark: 'ダークモード',
      themeLight: 'ライトモード',
      offline: 'オフラインです',
      saveSuccess: '設定を保存しました',
    },
  },
  en: {
    translation: {
      welcome: 'Welcome to UEP v5.0',
      login: 'Login',
      logout: 'Logout',
      dashboard: 'Dashboard',
      settings: 'Settings',
      search: 'Search pages...',
      notifications: 'Notifications',
      themeDark: 'Dark mode',
      themeLight: 'Light mode',
      offline: 'You are offline',
      saveSuccess: 'Settings saved',
    },
  },
};

const savedLang = (() => {
  try {
    const raw = localStorage.getItem('uep_user_settings');
    if (!raw) return 'ja';
    const parsed = JSON.parse(raw);
    return parsed.language === 'en' ? 'en' : 'ja';
  } catch {
    return 'ja';
  }
})();

i18n.use(initReactI18next).init({
  resources,
  lng: savedLang,
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;
