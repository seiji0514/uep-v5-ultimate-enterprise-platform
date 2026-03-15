/**
 * ユーザー設定コンテキスト
 * テーマ・お気に入り・最近使ったページをlocalStorageに永続化
 */
import React, { createContext, useContext, useCallback, useEffect, useState } from 'react';

export type ThemeMode = 'dark' | 'light';
export type Language = 'ja' | 'en';

interface UserSettings {
  themeMode: ThemeMode;
  language: Language;
  favorites: string[];
  recentPages: { path: string; label: string }[];
}

const STORAGE_KEY = 'uep_user_settings';
const RECENT_MAX = 10;
const FAVORITES_MAX = 20;

const defaultSettings: UserSettings = {
  themeMode: 'dark',
  language: 'ja',
  favorites: [],
  recentPages: [],
};

function loadSettings(): UserSettings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultSettings;
    const parsed = JSON.parse(raw);
    return {
      themeMode: parsed.themeMode === 'light' ? 'light' : 'dark',
      language: parsed.language === 'en' ? 'en' : 'ja',
      favorites: Array.isArray(parsed.favorites) ? parsed.favorites.slice(0, FAVORITES_MAX) : [],
      recentPages: Array.isArray(parsed.recentPages) ? parsed.recentPages.slice(0, RECENT_MAX) : [],
    };
  } catch {
    return defaultSettings;
  }
}

function saveSettings(s: UserSettings) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
  } catch {
    // ignore
  }
}

interface UserSettingsContextValue {
  themeMode: ThemeMode;
  setThemeMode: (mode: ThemeMode) => void;
  toggleTheme: () => void;
  language: Language;
  setLanguage: (lang: Language) => void;
  favorites: string[];
  addFavorite: (path: string) => void;
  removeFavorite: (path: string) => void;
  isFavorite: (path: string) => boolean;
  recentPages: { path: string; label: string }[];
  addRecentPage: (path: string, label: string) => void;
}

const UserSettingsContext = createContext<UserSettingsContextValue | null>(null);

export const UserSettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [settings, setSettings] = useState<UserSettings>(loadSettings);

  useEffect(() => {
    saveSettings(settings);
  }, [settings]);

  const setThemeMode = useCallback((mode: ThemeMode) => {
    setSettings((s) => ({ ...s, themeMode: mode }));
  }, []);

  const toggleTheme = useCallback(() => {
    setSettings((s) => ({ ...s, themeMode: s.themeMode === 'dark' ? 'light' : 'dark' }));
  }, []);

  const setLanguage = useCallback((lang: Language) => {
    setSettings((s) => ({ ...s, language: lang }));
  }, []);

  const addFavorite = useCallback((path: string) => {
    setSettings((s) => {
      if (s.favorites.includes(path)) return s;
      return { ...s, favorites: [...s.favorites, path].slice(0, FAVORITES_MAX) };
    });
  }, []);

  const removeFavorite = useCallback((path: string) => {
    setSettings((s) => ({ ...s, favorites: s.favorites.filter((p) => p !== path) }));
  }, []);

  const isFavorite = useCallback(
    (path: string) => settings.favorites.includes(path),
    [settings.favorites]
  );

  const addRecentPage = useCallback((path: string, label: string) => {
    setSettings((s) => {
      const filtered = s.recentPages.filter((p) => p.path !== path);
      return {
        ...s,
        recentPages: [{ path, label }, ...filtered].slice(0, RECENT_MAX),
      };
    });
  }, []);

  const value: UserSettingsContextValue = {
    themeMode: settings.themeMode,
    setThemeMode,
    toggleTheme,
    language: settings.language,
    setLanguage,
    favorites: settings.favorites,
    addFavorite,
    removeFavorite,
    isFavorite,
    recentPages: settings.recentPages,
    addRecentPage,
  };

  return (
    <UserSettingsContext.Provider value={value}>
      {children}
    </UserSettingsContext.Provider>
  );
};

export function useUserSettings(): UserSettingsContextValue {
  const ctx = useContext(UserSettingsContext);
  if (!ctx) throw new Error('useUserSettings must be used within UserSettingsProvider');
  return ctx;
}
