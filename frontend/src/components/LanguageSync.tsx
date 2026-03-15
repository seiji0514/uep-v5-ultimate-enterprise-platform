/**
 * ユーザー設定の言語を i18n に同期
 */
import { useEffect } from 'react';
import { useUserSettings } from '../contexts/UserSettingsContext';
import i18n from '../i18n';

export const LanguageSync: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { language } = useUserSettings();

  useEffect(() => {
    if (i18n.language !== language) {
      i18n.changeLanguage(language);
    }
  }, [language]);

  return <>{children}</>;
};
