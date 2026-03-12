import { createContext, useContext, useState, useCallback, ReactNode } from 'react';

const STORAGE_KEY = 'uep_standalone_settings';
const DEFAULT_POLL_MS = 30000;
const DEFAULT_ITEMS_PER_PAGE = 10;
const DEFAULT_COMPACT_MODE = false;

interface Settings {
  pollIntervalMs: number;
  itemsPerPage: number;
  compactMode: boolean;
}

const loadSettings = (): Settings => {
  try {
    const s = localStorage.getItem(STORAGE_KEY);
    if (s) {
      const parsed = JSON.parse(s);
      return {
        pollIntervalMs: parsed.pollIntervalMs >= 5000 ? parsed.pollIntervalMs : DEFAULT_POLL_MS,
        itemsPerPage: [5, 10, 25, 50].includes(parsed.itemsPerPage) ? parsed.itemsPerPage : DEFAULT_ITEMS_PER_PAGE,
        compactMode: !!parsed.compactMode,
      };
    }
  } catch {}
  return { pollIntervalMs: DEFAULT_POLL_MS, itemsPerPage: DEFAULT_ITEMS_PER_PAGE, compactMode: DEFAULT_COMPACT_MODE };
};

interface SettingsContextType {
  settings: Settings;
  setPollInterval: (ms: number) => void;
  setItemsPerPage: (n: number) => void;
  setCompactMode: (v: boolean) => void;
}

const SettingsContext = createContext<SettingsContextType | null>(null);

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<Settings>(loadSettings);

  const setPollInterval = useCallback((ms: number) => {
    const v = Math.max(5000, Math.min(300000, ms));
    setSettings((s) => {
      const next = { ...s, pollIntervalMs: v };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const setItemsPerPage = useCallback((n: number) => {
    const v = [5, 10, 25, 50].includes(n) ? n : DEFAULT_ITEMS_PER_PAGE;
    setSettings((s) => {
      const next = { ...s, itemsPerPage: v };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const setCompactMode = useCallback((v: boolean) => {
    setSettings((s) => {
      const next = { ...s, compactMode: v };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  return (
    <SettingsContext.Provider value={{ settings, setPollInterval, setItemsPerPage, setCompactMode }}>
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings() {
  const ctx = useContext(SettingsContext);
  return ctx ?? {
    settings: { pollIntervalMs: DEFAULT_POLL_MS, itemsPerPage: DEFAULT_ITEMS_PER_PAGE, compactMode: false },
    setPollInterval: () => {},
    setItemsPerPage: () => {},
    setCompactMode: () => {},
  };
}
