import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  username: string;
  role: string;
  full_name?: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE = process.env.REACT_APP_EOH_API_URL || 'http://localhost:9020';

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // UEP連携: ?token= でリダイレクトされた場合、SSOでEOHトークン取得
    const params = new URLSearchParams(window.location.search);
    const uepToken = params.get('token');
    if (uepToken) {
      setIsLoading(true);
      const apiBase = process.env.REACT_APP_EOH_API_URL || 'http://localhost:9020';
      fetch(`${apiBase}/api/v1/auth/sso`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uep_token: uepToken }),
      })
        .then((r) => r.ok ? r.json() : Promise.reject())
        .then((data) => {
          localStorage.setItem('eoh_access_token', data.access_token);
          setUser(data.user || { username: 'kaho0525', role: 'admin' });
          setIsAuthenticated(true);
          window.history.replaceState({}, '', window.location.pathname);
        })
        .catch(() => {})
        .finally(() => setIsLoading(false));
      return;
    }
    const token = localStorage.getItem('eoh_access_token');
    if (token) {
      fetch(`${API_BASE}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((r) => (r.ok ? r.json() : Promise.reject()))
        .then((u) => {
          setUser(u);
          setIsAuthenticated(true);
        })
        .catch(() => {
          localStorage.removeItem('eoh_access_token');
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (username: string, password: string) => {
    const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
      const e = await res.json().catch(() => ({}));
      throw new Error(e.detail || 'ログインに失敗しました');
    }
    const data = await res.json();
    localStorage.setItem('eoh_access_token', data.access_token);
    setUser(data.user || { username, role: 'viewer' });
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('eoh_access_token');
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
