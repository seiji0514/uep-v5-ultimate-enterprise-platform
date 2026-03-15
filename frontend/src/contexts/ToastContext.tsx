/**
 * トースト通知コンテキスト
 * MUI Snackbar によるユーザーフレンドリーなエラー・成功メッセージ
 */
import React, { createContext, useContext, useCallback, useState, useEffect } from 'react';
import { Snackbar, Alert, AlertColor } from '@mui/material';

interface ToastMessage {
  id: string;
  message: string;
  severity: AlertColor;
  duration?: number;
}

interface ToastContextValue {
  showSuccess: (message: string, duration?: number) => void;
  showError: (message: string, duration?: number) => void;
  showWarning: (message: string, duration?: number) => void;
  showInfo: (message: string, duration?: number) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

let toastId = 0;
function nextId() {
  return `toast-${Date.now()}-${++toastId}`;
}

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [open, setOpen] = useState(false);
  const [current, setCurrent] = useState<ToastMessage | null>(null);
  const [queue, setQueue] = useState<ToastMessage[]>([]);

  useEffect(() => {
    if (!current && queue.length > 0) {
      setCurrent(queue[0]);
      setQueue((q) => q.slice(1));
      setOpen(true);
    }
  }, [current, queue]);

  const show = useCallback((message: string, severity: AlertColor, duration = 6000) => {
    const item: ToastMessage = { id: nextId(), message, severity, duration };
    setQueue((prev) => [...prev, item]);
  }, []);

  const handleClose = useCallback(() => {
    setOpen(false);
    setTimeout(() => {
      setCurrent(null);
    }, 300);
  }, []);

  const showSuccess = useCallback((message: string, duration?: number) => {
    show(message, 'success', duration);
  }, [show]);

  const showError = useCallback((message: string, duration?: number) => {
    show(message, 'error', duration ?? 8000);
  }, [show]);

  const showWarning = useCallback((message: string, duration?: number) => {
    show(message, 'warning', duration);
  }, [show]);

  const showInfo = useCallback((message: string, duration?: number) => {
    show(message, 'info', duration);
  }, [show]);

  const value: ToastContextValue = { showSuccess, showError, showWarning, showInfo };

  return (
    <ToastContext.Provider value={value}>
      {children}
      <Snackbar
        open={open}
        autoHideDuration={current?.duration ?? 6000}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        sx={{ '& .MuiSnackbar-root': { bottom: 24 } }}
      >
        {current ? (
          <Alert
            onClose={handleClose}
            severity={current.severity}
            variant="filled"
            sx={{ width: '100%' }}
            role="alert"
          >
            {current.message}
          </Alert>
        ) : (
          <span />
        )}
      </Snackbar>
    </ToastContext.Provider>
  );
};

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used within ToastProvider');
  return ctx;
}
