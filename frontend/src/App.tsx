/**
 * UEP v5.0 - メインアプリケーションコンポーネント
 * 次世代エンタープライズ統合プラットフォーム v5.0
 * React.lazy コード分割・エラーバウンダリ・アクセシビリティ対応
 */
import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider, createTheme, CssBaseline, Box, CircularProgress } from '@mui/material';
import { queryClient } from './lib/queryClient';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { MainLayout } from './components/Layout/MainLayout';
import { ErrorBoundary } from './components/ErrorBoundary';
import { SessionTimeoutWarning } from './components/SessionTimeoutWarning';
import { useAuth } from './contexts/AuthContext';

const LoginPage = lazy(() => import('./components/Auth/LoginPage').then((m) => ({ default: m.LoginPage })));
const DashboardPage = lazy(() => import('./components/Dashboard/DashboardPage').then((m) => ({ default: m.DashboardPage })));
const MLOpsPage = lazy(() => import('./components/MLOps/MLOpsPage').then((m) => ({ default: m.MLOpsPage })));
const GenerativeAIPage = lazy(() => import('./components/GenerativeAI/GenerativeAIPage').then((m) => ({ default: m.GenerativeAIPage })));
const CloudInfraPage = lazy(() => import('./components/CloudInfra/CloudInfraPage').then((m) => ({ default: m.CloudInfraPage })));
const InfraBuilderPage = lazy(() => import('./components/InfraBuilder/InfraBuilderPage').then((m) => ({ default: m.InfraBuilderPage })));
const IDOPPage = lazy(() => import('./components/IDOP/IDOPPage').then((m) => ({ default: m.IDOPPage })));
const AIDevPage = lazy(() => import('./components/AIDev/AIDevPage').then((m) => ({ default: m.AIDevPage })));
const PlatformPage = lazy(() => import('./components/Platform/PlatformPage').then((m) => ({ default: m.PlatformPage })));
const EcosystemPage = lazy(() => import('./components/Ecosystem/EcosystemPage').then((m) => ({ default: m.EcosystemPage })));
const IndustryLeaderPage = lazy(() => import('./components/IndustryLeader/IndustryLeaderPage').then((m) => ({ default: m.IndustryLeaderPage })));
const GlobalEnterprisePage = lazy(() => import('./components/GlobalEnterprise/GlobalEnterprisePage').then((m) => ({ default: m.GlobalEnterprisePage })));
const UnifiedBusinessPage = lazy(() => import('./components/UnifiedBusiness/UnifiedBusinessPage').then((m) => ({ default: m.UnifiedBusinessPage })));
const ChaosPage = lazy(() => import('./components/Chaos/ChaosPage').then((m) => ({ default: m.ChaosPage })));
const InclusiveWorkPage = lazy(() => import('./components/InclusiveWork/InclusiveWorkPage').then((m) => ({ default: m.InclusiveWorkPage })));
const GraphQLPage = lazy(() => import('./components/GraphQL/GraphQLPage').then((m) => ({ default: m.GraphQLPage })));
const WasmPage = lazy(() => import('./components/Wasm/WasmPage').then((m) => ({ default: m.WasmPage })));
const SettingsPage = lazy(() => import('./components/Settings/SettingsPage').then((m) => ({ default: m.SettingsPage })));
const ProjectsPage = lazy(() => import('./components/Projects/ProjectsPage').then((m) => ({ default: m.ProjectsPage })));
const TestsPage = lazy(() => import('./components/Tests/TestsPage').then((m) => ({ default: m.TestsPage })));
const ManufacturingPage = lazy(() => import('./components/Manufacturing/ManufacturingPage').then((m) => ({ default: m.ManufacturingPage })));
const FinTechPage = lazy(() => import('./components/FinTech/FinTechPage').then((m) => ({ default: m.FinTechPage })));
const EnergyPage = lazy(() => import('./components/Energy/EnergyPage').then((m) => ({ default: m.EnergyPage })));
const MedicalPage = lazy(() => import('./components/Medical/MedicalPage').then((m) => ({ default: m.MedicalPage })));
const SpacePage = lazy(() => import('./components/Space/SpacePage').then((m) => ({ default: m.SpacePage })));
const TrafficPage = lazy(() => import('./components/Traffic/TrafficPage').then((m) => ({ default: m.TrafficPage })));
const OptimizationPage = lazy(() => import('./components/Optimization/OptimizationPage').then((m) => ({ default: m.OptimizationPage })));
const PersonalAccountingPage = lazy(() => import('./components/PersonalAccounting/PersonalAccountingPage').then((m) => ({ default: m.PersonalAccountingPage })));
const ERPPage = lazy(() => import('./components/ERP/ERPPage').then((m) => ({ default: m.ERPPage })));
const PublicSectorPage = lazy(() => import('./components/PublicSector/PublicSectorPage').then((m) => ({ default: m.PublicSectorPage })));
const RetailPage = lazy(() => import('./components/Retail/RetailPage').then((m) => ({ default: m.RetailPage })));
const EducationPage = lazy(() => import('./components/Education/EducationPage').then((m) => ({ default: m.EducationPage })));
const LegalPage = lazy(() => import('./components/Legal/LegalPage').then((m) => ({ default: m.LegalPage })));
const SupplyChainPage = lazy(() => import('./components/SupplyChain/SupplyChainPage').then((m) => ({ default: m.SupplyChainPage })));

const PageFallback = () => (
  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 200 }}>
    <CircularProgress aria-label="読み込み中" />
  </Box>
);

// エンタープライズ向けテーマ（近代的・データ重視・アクセシビリティ対応）
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#F46800', // アクセントオレンジ
    },
    secondary: {
      main: '#5794F2', // アクセントブルー
    },
    background: {
      default: '#0b0c0e',
      paper: '#181b1f',
    },
    text: {
      primary: '#d8d9da',
      secondary: '#9e9e9e',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#1e1e1e',
          border: '1px solid #2d2d2d',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#1e1e1e',
          border: '1px solid #2d2d2d',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#0b0c0e',
          borderBottom: '1px solid #2d2d2d',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#0b0c0e',
          borderRight: '1px solid #2d2d2d',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          '&:focus-visible': {
            outline: '2px solid',
            outlineColor: 'primary.main',
          },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          '&:focus-visible': {
            outline: '2px solid',
            outlineColor: 'primary.main',
          },
        },
      },
    },
  },
});

const AppRoutes: React.FC = () => {
  const { logout } = useAuth();
  return (
    <>
      <SessionTimeoutWarning onLogout={logout} />
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
        <Route path="/projects" element={<ProtectedRoute><MainLayout><ProjectsPage /></MainLayout></ProtectedRoute>} />
        <Route path="/mlops" element={<ProtectedRoute><MainLayout><MLOpsPage /></MainLayout></ProtectedRoute>} />
        <Route path="/generative-ai" element={<ProtectedRoute><MainLayout><GenerativeAIPage /></MainLayout></ProtectedRoute>} />
        {/* 統合セキュリティ・防衛プラットフォームは個別システム（ポート9001）のため UEP には含めない */}
        <Route path="/cloud-infra" element={<ProtectedRoute><MainLayout><CloudInfraPage /></MainLayout></ProtectedRoute>} />
        <Route path="/infra-builder" element={<ProtectedRoute><MainLayout><InfraBuilderPage /></MainLayout></ProtectedRoute>} />
        <Route path="/idop" element={<ProtectedRoute><MainLayout><IDOPPage /></MainLayout></ProtectedRoute>} />
        <Route path="/ai-dev" element={<ProtectedRoute><MainLayout><AIDevPage /></MainLayout></ProtectedRoute>} />
        <Route path="/platform" element={<ProtectedRoute><MainLayout><PlatformPage /></MainLayout></ProtectedRoute>} />
        <Route path="/ecosystem" element={<ProtectedRoute><MainLayout><EcosystemPage /></MainLayout></ProtectedRoute>} />
        <Route path="/industry-leader" element={<ProtectedRoute><MainLayout><IndustryLeaderPage /></MainLayout></ProtectedRoute>} />
        <Route path="/global-enterprise" element={<ProtectedRoute><MainLayout><GlobalEnterprisePage /></MainLayout></ProtectedRoute>} />
        <Route path="/unified-business" element={<ProtectedRoute><MainLayout><UnifiedBusinessPage /></MainLayout></ProtectedRoute>} />
        <Route path="/chaos" element={<ProtectedRoute><MainLayout><ChaosPage /></MainLayout></ProtectedRoute>} />
        <Route path="/inclusive-work" element={<ProtectedRoute><MainLayout><InclusiveWorkPage /></MainLayout></ProtectedRoute>} />
        <Route path="/graphql" element={<ProtectedRoute><MainLayout><GraphQLPage /></MainLayout></ProtectedRoute>} />
        <Route path="/wasm" element={<ProtectedRoute><MainLayout><WasmPage /></MainLayout></ProtectedRoute>} />
        <Route path="/settings" element={<ProtectedRoute><MainLayout><SettingsPage /></MainLayout></ProtectedRoute>} />
        <Route path="/tests" element={<ProtectedRoute><MainLayout><TestsPage /></MainLayout></ProtectedRoute>} />
        <Route path="/manufacturing" element={<ProtectedRoute><MainLayout><ManufacturingPage /></MainLayout></ProtectedRoute>} />
        <Route path="/fintech" element={<ProtectedRoute><MainLayout><FinTechPage /></MainLayout></ProtectedRoute>} />
        <Route path="/energy" element={<ProtectedRoute><MainLayout><EnergyPage /></MainLayout></ProtectedRoute>} />
        <Route path="/medical" element={<ProtectedRoute><MainLayout><MedicalPage /></MainLayout></ProtectedRoute>} />
        <Route path="/space" element={<ProtectedRoute><MainLayout><SpacePage /></MainLayout></ProtectedRoute>} />
        <Route path="/traffic" element={<ProtectedRoute><MainLayout><TrafficPage /></MainLayout></ProtectedRoute>} />
        <Route path="/optimization" element={<ProtectedRoute><MainLayout><OptimizationPage /></MainLayout></ProtectedRoute>} />
        <Route path="/personal-accounting" element={<ProtectedRoute><MainLayout><PersonalAccountingPage /></MainLayout></ProtectedRoute>} />
        <Route path="/erp" element={<ProtectedRoute><MainLayout><ERPPage /></MainLayout></ProtectedRoute>} />
        <Route path="/public-sector" element={<ProtectedRoute><MainLayout><PublicSectorPage /></MainLayout></ProtectedRoute>} />
        <Route path="/retail" element={<ProtectedRoute><MainLayout><RetailPage /></MainLayout></ProtectedRoute>} />
        <Route path="/education" element={<ProtectedRoute><MainLayout><EducationPage /></MainLayout></ProtectedRoute>} />
        <Route path="/legal" element={<ProtectedRoute><MainLayout><LegalPage /></MainLayout></ProtectedRoute>} />
        <Route path="/supply-chain" element={<ProtectedRoute><MainLayout><SupplyChainPage /></MainLayout></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <ErrorBoundary>
          <AuthProvider>
            <Router>
              <Suspense fallback={<PageFallback />}>
                <AppRoutes />
              </Suspense>
            </Router>
          </AuthProvider>
        </ErrorBoundary>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
