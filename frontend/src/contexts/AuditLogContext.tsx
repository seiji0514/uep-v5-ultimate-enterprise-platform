/**
 * 監査ログコンテキスト
 * フロントの重要操作をAPIで永続化
 */
import React, { createContext, useContext, useCallback } from 'react';
import { apiClient } from '../api/client';

export type AuditAction =
  | 'login'
  | 'logout'
  | 'navigate'
  | 'favorite_add'
  | 'favorite_remove'
  | 'settings_change'
  | 'export'
  | 'delete';

interface AuditEntry {
  action: AuditAction;
  detail?: string;
  path?: string;
  timestamp: number;
}

interface AuditLogContextValue {
  log: (action: AuditAction, detail?: string, path?: string) => void;
}

const AuditLogContext = createContext<AuditLogContextValue | null>(null);

export const AuditLogProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const log = useCallback((action: AuditAction, detail?: string, path?: string) => {
    const entry: AuditEntry = {
      action,
      detail,
      path,
      timestamp: Date.now(),
    };
    if (process.env.NODE_ENV === 'development') {
      console.debug('[UEP Audit]', entry);
    }
    apiClient.post('/api/v1/audit', { action, detail, path }).catch(() => {
      // 監査ログ送信失敗は静かに無視（ユーザー体験を損なわない）
    });
  }, []);

  return (
    <AuditLogContext.Provider value={{ log }}>
      {children}
    </AuditLogContext.Provider>
  );
};

export function useAuditLog(): AuditLogContextValue {
  const ctx = useContext(AuditLogContext);
  if (!ctx) return { log: () => {} };
  return ctx;
}
