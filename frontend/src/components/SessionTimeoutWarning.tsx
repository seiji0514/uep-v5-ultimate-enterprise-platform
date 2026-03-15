/**
 * セッションタイムアウト警告
 * トークン期限切れ前にダイアログを表示
 */
import React, { useEffect, useState, useCallback } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';

const WARN_BEFORE_MS = 5 * 60 * 1000; // 5分前に警告
const CHECK_INTERVAL_MS = 60 * 1000;   // 1分ごとにチェック

export const SessionTimeoutWarning: React.FC<{ onExtend?: () => void; onLogout?: () => void }> = ({
  onExtend,
  onLogout,
}) => {
  const [open, setOpen] = useState(false);
  const [tokenExpiry, setTokenExpiry] = useState<number | null>(null);

  const checkToken = useCallback(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const exp = payload.exp ? payload.exp * 1000 : null;
      if (exp) setTokenExpiry(exp);
    } catch {
      // JWT解析失敗時は無視
    }
  }, []);

  useEffect(() => {
    checkToken();
    const id = setInterval(checkToken, CHECK_INTERVAL_MS);
    return () => clearInterval(id);
  }, [checkToken]);

  useEffect(() => {
    if (!tokenExpiry) return;
    const check = () => {
      const now = Date.now();
      if (tokenExpiry - now <= WARN_BEFORE_MS && tokenExpiry > now) {
        setOpen(true);
      }
    };
    check();
    const id = setInterval(check, 30 * 1000);
    return () => clearInterval(id);
  }, [tokenExpiry]);

  const handleExtend = () => {
    setOpen(false);
    onExtend?.();
  };

  const handleLogout = () => {
    setOpen(false);
    onLogout?.();
  };

  return (
    <Dialog open={open} onClose={handleExtend} aria-labelledby="session-timeout-title">
      <DialogTitle id="session-timeout-title">セッションの有効期限が近づいています</DialogTitle>
      <DialogContent>
        <Typography variant="body2" color="text.secondary">
          セッションの有効期限がまもなく切れます。このまま作業を続けますか？
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleLogout} color="inherit">
          ログアウト
        </Button>
        <Button onClick={handleExtend} variant="contained" autoFocus aria-label="セッションを延長">
          続ける
        </Button>
      </DialogActions>
    </Dialog>
  );
};
