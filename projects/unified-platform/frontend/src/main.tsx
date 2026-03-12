import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './i18n';
import { ThemeProvider, CssBaseline } from '@mui/material';
import App from './App';
import { ThemeProvider as CustomThemeProvider, useThemeMode } from './contexts/ThemeContext';

function AppWithTheme() {
  const { theme } = useThemeMode();
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ThemeProvider>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <CustomThemeProvider>
      <AppWithTheme />
    </CustomThemeProvider>
  </React.StrictMode>
);
