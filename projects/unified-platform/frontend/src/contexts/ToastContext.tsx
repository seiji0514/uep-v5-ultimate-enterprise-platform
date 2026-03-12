/**
 * トースト通知コンテキスト
 */
import { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Snackbar, Alert, AlertColor } from '@mui/material';

interface ToastContextType {
  show: (msg: string, severity?: AlertColor) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  const [msg, setMsg] = useState('');
  const [severity, setSeverity] = useState<AlertColor>('info');

  const show = useCallback((m: string, s: AlertColor = 'info') => {
    setMsg(m);
    setSeverity(s);
    setOpen(true);
  }, []);

  return (
    <ToastContext.Provider value={{ show }}>
      {children}
      <Snackbar open={open} autoHideDuration={4000} onClose={() => setOpen(false)} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert onClose={() => setOpen(false)} severity={severity}>{msg}</Alert>
      </Snackbar>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  return ctx ?? { show: () => {} };
}
