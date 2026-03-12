import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import ja from './locales/ja.json';
import en from './locales/en.json';

const STORAGE_KEY = 'uep_lang';

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: { ja: { translation: ja }, en: { translation: en } },
    fallbackLng: 'ja',
    supportedLngs: ['ja', 'en'],
    interpolation: { escapeValue: false },
    detection: {
      order: ['localStorage', 'navigator'],
      lookupLocalStorage: STORAGE_KEY,
      caches: ['localStorage'],
    },
  });

export default i18n;
