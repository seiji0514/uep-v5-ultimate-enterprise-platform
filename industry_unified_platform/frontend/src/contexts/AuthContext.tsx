import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authApi, LoginRequest } from '../api/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // SSO: UEPから ?token=xxx でリダイレクトされた場合、トークンを保存して認証
    const params = new URLSearchParams(window.location.search);
    const ssoToken = params.get('token');
    if (ssoToken) {
      localStorage.setItem('access_token', ssoToken);
      sessionStorage.setItem('industry_sso_origin', 'uep');
      window.history.replaceState({}, '', window.location.pathname);
    }
    setIsAuthenticated(!!localStorage.getItem('access_token'));
    setIsLoading(false);
  }, []);

  const login = async (credentials: LoginRequest) => {
    const response = await authApi.login(credentials);
    localStorage.setItem('access_token', response.access_token);
    if (response.user) localStorage.setItem('user', JSON.stringify(response.user));
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    sessionStorage.removeItem('industry_sso_origin');
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
