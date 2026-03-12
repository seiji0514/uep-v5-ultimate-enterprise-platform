/**
 * セッションタイムアウト警告
 */
import { useEffect, useState, useCallback } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';

const TOKEN_KEY = 'uep_standalone_token';
const WARN_BEFORE_MS = 5 * 60 * 1000;
const CHECK_INTERVAL_MS = 60 * 1000;

export const SessionTimeoutWarning: React.FC<{ onExtend?: () => void; onLogout?: () => void }> = ({
  onExtend,
  onLogout,
}) => {
  const [open, setOpen] = useState(false);
  const [tokenExpiry, setTokenExpiry] = useState<number | null>(null);

  const checkToken = useCallback(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) return;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const exp = payload.exp ? payload.exp * 1000 : null;
      if (exp) setTokenExpiry(exp);
    } catch {
      // ignore
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
      if (tokenExpiry - now <= WARN_BEFORE_MS && tokenExpiry > now) setOpen(true);
    };
    check();
    const id = setInterval(check, 30 * 1000);
    return () => clearInterval(id);
  }, [tokenExpiry]);

  return (
    <Dialog open={open} onClose={() => setOpen(false)} aria-labelledby="session-timeout-title">
      <DialogTitle id="session-timeout-title">セッションの有効期限が近づいています</DialogTitle>
      <DialogContent>
        <Typography variant="body2" color="text.secondary">
          セッションの有効期限がまもなく切れます。このまま作業を続けますか？
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => { setOpen(false); onLogout?.(); }} color="inherit">ログアウト</Button>
        <Button onClick={() => { setOpen(false); onExtend?.(); }} variant="contained" autoFocus>続ける</Button>
      </DialogActions>
    </Dialog>
  );
};
