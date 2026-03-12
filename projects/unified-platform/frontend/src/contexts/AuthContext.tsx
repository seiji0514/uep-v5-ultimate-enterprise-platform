import { createContext, useContext, useState, useCallback, ReactNode } from 'react';

interface AuthContextType {
  user: string | null;
  token: string | null;
  login: (username: string, password: string) => Promise<{ ok: boolean; error?: string }>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

const TOKEN_KEY = 'uep_standalone_token';
const USER_KEY = 'uep_standalone_user';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY));
  const [user, setUser] = useState<string | null>(() => localStorage.getItem(USER_KEY));

  const login = useCallback(async (username: string, password: string): Promise<{ ok: boolean; error?: string }> => {
    try {
      const form = new FormData();
      form.append('username', username);
      form.append('password', password);
      const res = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/v1/auth/login`, {
        method: 'POST',
        body: form,
      });
      const data = res.ok ? await res.json() : await res.json().catch(() => ({}));
      if (res.ok) {
        setToken(data.access_token);
        setUser(username);
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem(USER_KEY, username);
        return { ok: true };
      }
      return { ok: false, error: data.detail || (res.status === 429 ? 'アカウントが一時ロックされています。しばらくお待ちください。' : 'ユーザー名・パスワードを確認してください。') };
    } catch {
      return { ok: false, error: 'ログインに失敗しました。' };
    }
  }, []);

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
