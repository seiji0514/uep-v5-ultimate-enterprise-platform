/**
 * UEP v5.0 - メインアプリケーションコンポーネント
 * 次世代エンタープライズ統合プラットフォーム v5.0
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { MainLayout } from './components/Layout/MainLayout';
import { LoginPage } from './components/Auth/LoginPage';
import { DashboardPage } from './components/Dashboard/DashboardPage';
import { MLOpsPage } from './components/MLOps/MLOpsPage';
import { GenerativeAIPage } from './components/GenerativeAI/GenerativeAIPage';
import { SecurityCenterPage } from './components/SecurityCenter/SecurityCenterPage';
import { CloudInfraPage } from './components/CloudInfra/CloudInfraPage';
import { IDOPPage } from './components/IDOP/IDOPPage';
import { AIDevPage } from './components/AIDev/AIDevPage';
import { PlatformPage } from './components/Platform/PlatformPage';
import { EcosystemPage } from './components/Ecosystem/EcosystemPage';
import { IndustryLeaderPage } from './components/IndustryLeader/IndustryLeaderPage';
import { GlobalEnterprisePage } from './components/GlobalEnterprise/GlobalEnterprisePage';
import { UnifiedBusinessPage } from './components/UnifiedBusiness/UnifiedBusinessPage';
import { ChaosPage } from './components/Chaos/ChaosPage';
import { InclusiveWorkPage } from './components/InclusiveWork/InclusiveWorkPage';
import { GraphQLPage } from './components/GraphQL/GraphQLPage';
import { WasmPage } from './components/Wasm/WasmPage';
import { SettingsPage } from './components/Settings/SettingsPage';

// Material-UIテーマの設定
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#9c27b0',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <DashboardPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/mlops"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <MLOpsPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/generative-ai"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <GenerativeAIPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/security-center"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <SecurityCenterPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/cloud-infra"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <CloudInfraPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/idop"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <IDOPPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/ai-dev"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <AIDevPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/platform"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <PlatformPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/ecosystem"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <EcosystemPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/industry-leader"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <IndustryLeaderPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/global-enterprise"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <GlobalEnterprisePage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/unified-business"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <UnifiedBusinessPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/chaos"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <ChaosPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/inclusive-work"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <InclusiveWorkPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/graphql"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <GraphQLPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/wasm"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <WasmPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route
              path="/settings"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <SettingsPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
