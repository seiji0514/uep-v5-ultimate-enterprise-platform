import { createContext, useContext, useState, useCallback, useMemo, ReactNode } from 'react';
import { createTheme, ThemeOptions, PaletteMode } from '@mui/material';

const STORAGE_KEY = 'uep_standalone_theme';

const getThemeOptions = (mode: PaletteMode): ThemeOptions => ({
  palette: {
    mode,
    primary: { main: '#F46800' },
    secondary: { main: '#5794F2' },
    ...(mode === 'dark'
      ? { background: { default: '#0b0c0e', paper: '#181b1f' }, text: { primary: '#d8d9da', secondary: '#9e9e9e' } }
      : { background: { default: '#f5f5f5', paper: '#ffffff' }, text: { primary: '#1a1a1a', secondary: '#666666' } }),
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          ...(mode === 'dark'
            ? { backgroundColor: '#1e1e1e', border: '1px solid #2d2d2d' }
            : { backgroundColor: '#ffffff', border: '1px solid #e0e0e0' }),
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          ...(mode === 'dark'
            ? { backgroundColor: '#0b0c0e', borderBottom: '1px solid #2d2d2d' }
            : { backgroundColor: '#ffffff', borderBottom: '1px solid #e0e0e0', color: '#1a1a1a' }),
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:hover': { backgroundColor: mode === 'dark' ? 'rgba(244, 104, 0, 0.08)' : 'rgba(244, 104, 0, 0.04)' },
        },
      },
    },
  },
});

interface ThemeContextType {
  mode: PaletteMode;
  toggleTheme: () => void;
  theme: ReturnType<typeof createTheme>;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [mode, setMode] = useState<PaletteMode>(() => (localStorage.getItem(STORAGE_KEY) as PaletteMode) || 'dark');

  const toggleTheme = useCallback(() => {
    setMode((m) => {
      const next = m === 'dark' ? 'light' : 'dark';
      localStorage.setItem(STORAGE_KEY, next);
      return next;
    });
  }, []);

  const theme = useMemo(() => createTheme(getThemeOptions(mode)), [mode]);

  return (
    <ThemeContext.Provider value={{ mode, toggleTheme, theme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useThemeMode() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useThemeMode must be used within ThemeProvider');
  return ctx;
}
