/**
 * Zustand グローバル状態ストア
 * 補強スキル: 軽量状態管理
 */
import { create } from 'zustand';

interface AppState {
  sidebarOpen: boolean;
  language: string;
  setSidebarOpen: (open: boolean) => void;
  setLanguage: (lang: string) => void;
}

export const useAppStore = create<AppState>((set) => ({
  sidebarOpen: true,
  language: 'ja',
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setLanguage: (lang) => set({ language: lang }),
}));
