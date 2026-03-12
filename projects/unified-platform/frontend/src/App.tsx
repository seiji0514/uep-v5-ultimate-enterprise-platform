import { useState, useEffect, useCallback, useRef } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { unifiedApi } from './api/unified';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ToastProvider } from './contexts/ToastContext';
import { SettingsProvider, useSettings } from './contexts/SettingsContext';
import { DashboardProvider } from './contexts/DashboardContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './components/Auth/LoginPage';
import { ErrorBoundary } from './components/ErrorBoundary';
import { SessionTimeoutWarning } from './components/SessionTimeoutWarning';
import { AppShell } from './components/Layout/AppShell';
import { DashboardPage } from './pages/DashboardPage';
import { MedicalPage } from './pages/MedicalPage';
import { AviationPage } from './pages/AviationPage';
import { SpacePage } from './pages/SpacePage';
import { ERPPage } from './pages/ERPPage';
import { LegacyMigrationPage } from './pages/LegacyMigrationPage';
import { DataIntegrationPage } from './pages/DataIntegrationPage';
import { DXPage } from './pages/DXPage';
import { SettingsPage } from './pages/SettingsPage';

export default function App() {
  const [error, setError] = useState('');
  const [medical, setMedical] = useState<any>({ ai: [], vital: [], stats: null });
  const [aviation, setAviation] = useState<any>({ flights: [], airports: [], stats: null, delays: null });
  const [space, setSpace] = useState<any>({ satellites: [], launches: [], stats: null });
  const [unified, setUnified] = useState<any>(null);

  const initialLoadDone = useRef(false);
  const loadAll = useCallback(async () => {
    try {
      setError('');
      const [patients, ai, vital, mStats, flights, airports, aStats, sats, launches, sStats, uStats, delays, delayPred, apod] = await Promise.all([
        unifiedApi.medical.getPatients(),
        unifiedApi.medical.getAIDiagnosis(),
        unifiedApi.medical.getVitalSigns(),
        unifiedApi.medical.getStats(),
        unifiedApi.aviation.getFlights(),
        unifiedApi.aviation.getAirports(),
        unifiedApi.aviation.getStats(),
        unifiedApi.space.getSatellites(),
        unifiedApi.space.getLaunches(),
        unifiedApi.space.getStats(),
        unifiedApi.unified.getStats(),
        unifiedApi.aviation.getDelays().catch(() => ({ data: {} })),
        unifiedApi.aviation.getDelayPrediction().catch(() => ({ data: {} })),
        unifiedApi.space.getApod().catch(() => ({ data: {} })),
      ]);
      setMedical({ patients: patients.data.items, ai: ai.data.items, vital: vital.data.items, stats: mStats.data });
      setAviation({ flights: flights.data.items, airports: airports.data.items, stats: aStats.data, delays: delays.data, delayPrediction: delayPred.data });
      setSpace({ satellites: sats.data.items, launches: launches.data.items, stats: sStats.data, apod: apod.data });
      setUnified(uStats.data);
    } catch (e: any) {
      setError(e?.message || 'API 接続エラー。バックエンド(localhost:8000)の起動を確認してください。');
    } finally {
      initialLoadDone.current = true;
    }
  }, []);

  return (
    <ErrorBoundary>
      <AuthProvider>
        <ToastProvider>
          <SettingsProvider>
          <DashboardProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/*" element={<ProtectedRoute><AppContent error={error} medical={medical} aviation={aviation} space={space} unified={unified} loadAll={loadAll} /></ProtectedRoute>} />
          </Routes>
          </DashboardProvider>
          </SettingsProvider>
        </ToastProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
}

function AppContent({ error, medical, aviation, space, unified, loadAll }: {
  error: string; medical: any; aviation: any; space: any; unified: any; loadAll: () => void;
}) {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const { settings } = useSettings();

  useWebSocket(loadAll, isAuthenticated);

  useEffect(() => {
    if (isAuthenticated) loadAll();
  }, [isAuthenticated, loadAll]);

  useEffect(() => {
    if (!isAuthenticated) return;
    const id = setInterval(loadAll, settings.pollIntervalMs);
    return () => clearInterval(id);
  }, [isAuthenticated, loadAll, settings.pollIntervalMs]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        loadAll();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [loadAll]);

  return (
    <>
      <SessionTimeoutWarning onLogout={() => { logout(); navigate('/login'); }} />
      <AppShell>
      <Box sx={{ width: '100%', minWidth: 0, display: 'block' }}>
        <Routes>
          <Route path="/" element={<DashboardPage unified={unified} medical={medical} aviation={aviation} space={space} error={error} onRefresh={loadAll} />} />
          <Route path="/medical" element={<MedicalPage patients={medical.patients} ai={medical.ai} vital={medical.vital} onRefresh={loadAll} />} />
          <Route path="/aviation" element={<AviationPage flights={aviation.flights} airports={aviation.airports} delays={aviation.delays} delayPrediction={aviation.delayPrediction} onRefresh={loadAll} />} />
          <Route path="/space" element={<SpacePage satellites={space.satellites} launches={space.launches} apod={space.apod} />} />
          <Route path="/erp" element={<ERPPage />} />
          <Route path="/legacy-migration" element={<LegacyMigrationPage />} />
          <Route path="/data-integration" element={<DataIntegrationPage />} />
          <Route path="/dx" element={<DXPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Box>
    </AppShell>
    </>
  );
}
