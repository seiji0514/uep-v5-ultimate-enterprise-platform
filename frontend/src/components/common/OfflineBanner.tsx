/**
 * オフライン時のバナー表示
 * Service Worker と連携
 */
import React, { useState, useEffect } from 'react';
import { Alert, AlertTitle } from '@mui/material';
import { WifiOff } from '@mui/icons-material';

export const OfflineBanner: React.FC = () => {
  const [online, setOnline] = useState(true);

  useEffect(() => {
    setOnline(navigator.onLine);
    const handleOnline = () => setOnline(true);
    const handleOffline = () => setOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (online) return null;

  return (
    <Alert
      severity="warning"
      icon={<WifiOff />}
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 9999,
        borderRadius: 0,
      }}
      role="alert"
    >
      <AlertTitle>オフラインです</AlertTitle>
      接続を確認してから再試行してください。一部の機能は利用できません。
    </Alert>
  );
};
