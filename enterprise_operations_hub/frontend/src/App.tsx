import React, { useState, useEffect } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Paper,
  Grid,
  Card,
  CardContent,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  TextField,
  Chip,
  Stack,
  Alert,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Badge,
} from '@mui/material';
import {
  Dashboard,
  Assignment,
  Warning,
  Visibility,
  Add,
  Refresh,
  Logout,
  Notifications,
  FileDownload,
} from '@mui/icons-material';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LoginPage } from './components/LoginPage';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_EOH_API_URL || 'http://localhost:9020';

function createApi() {
  const api = axios.create({ baseURL: API_BASE });
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('eoh_access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  });
  return api;
}
const api = createApi();

interface DashboardData {
  observations: { total: number; by_domain: Record<string, number> };
  tasks: { total: number; by_domain: Record<string, number> };
  risks: { total: number; by_domain: Record<string, number> };
}

const DOMAIN_LABELS: Record<string, string> = {
  manufacturing: '製造',
  security: 'セキュリティ',
  customer: '顧客',
  hr: '人・組織',
  compliance: '規制',
  finance: '財務',
  supply_chain: 'サプライチェーン',
  public_sector: '公共・官公庁',
  retail: '小売・EC',
  education: '教育',
  legal: '法務',
  general: '汎用',
};

function MainApp() {
  const { isAuthenticated, isLoading, user, logout } = useAuth();
  const [tabValue, setTabValue] = useState(0);
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [observations, setObservations] = useState<any[]>([]);
  const [tasks, setTasks] = useState<any[]>([]);
  const [risks, setRisks] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDomain, setNewTaskDomain] = useState('general');
  const [searchObs, setSearchObs] = useState('');
  const [searchTask, setSearchTask] = useState('');
  const [searchRisk, setSearchRisk] = useState('');
  const [industryTemplate, setIndustryTemplate] = useState(() => {
    try {
      return localStorage.getItem('eoh_industry_template') || 'general';
    } catch { return 'general'; }
  });

  const loadAll = async () => {
    setLoading(true);
    setError('');
    try {
      const [dRes, oRes, tRes, rRes, aRes] = await Promise.all([
        api.get<DashboardData>('/api/v1/dashboard'),
        api.get<{ items: any[] }>('/api/v1/observations', { params: searchObs ? { q: searchObs } : {} }),
        api.get<{ items: any[] }>('/api/v1/tasks', { params: searchTask ? { search: searchTask } : {} }),
        api.get<{ items: any[] }>('/api/v1/risks', { params: searchRisk ? { search: searchRisk } : {} }),
        api.get<{ items: any[] }>('/api/v1/alerts'),
      ]);
      setDashboard(dRes.data);
      setObservations(oRes.data.items);
      setTasks(tRes.data.items);
      setRisks(rRes.data.items);
      setAlerts(aRes.data.items);
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || 'データ取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) loadAll();
  }, [isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated && (searchObs || searchTask || searchRisk)) {
      const t = setTimeout(() => loadAll(), 300);
      return () => clearTimeout(t);
    }
  }, [searchObs, searchTask, searchRisk]);

  const handleAddTask = async () => {
    if (!newTaskTitle.trim()) return;
    try {
      await api.post('/api/v1/tasks', { domain: newTaskDomain, title: newTaskTitle.trim(), status: '未着手' });
      setNewTaskTitle('');
      loadAll();
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || 'タスク追加に失敗しました');
    }
  };

  const handleTaskStatus = async (id: number, status: string) => {
    try {
      await api.patch(`/api/v1/tasks/${id}`, { status });
      loadAll();
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || '更新に失敗しました');
    }
  };

  const handleMarkAlertRead = async (id: number) => {
    try {
      await api.patch(`/api/v1/alerts/${id}/read`);
      loadAll();
    } catch { /* ignore */ }
  };

  const handleExport = (format: 'csv' | 'excel', type: string) => {
    const url = `${API_BASE}/api/v1/export/${format}?type=${type}`;
    const token = localStorage.getItem('eoh_access_token');
    const a = document.createElement('a');
    a.href = url;
    a.setAttribute('download', '');
    a.style.display = 'none';
    if (token) {
      fetch(url, { headers: { Authorization: `Bearer ${token}` } })
        .then((r) => r.blob())
        .then((blob) => {
          const u = URL.createObjectURL(blob);
          a.href = u;
          a.download = `eoh_export_${type}_${new Date().toISOString().slice(0, 10)}.${format === 'csv' ? 'csv' : 'xlsx'}`;
          a.click();
          URL.revokeObjectURL(u);
        });
    }
  };

  const unreadAlerts = alerts.filter((a) => !a.read);

  if (isLoading) return null;
  if (!isAuthenticated) return <LoginPage />;

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static">
        <Toolbar>
          <Dashboard sx={{ mr: 2 }} />
          <Typography variant="h6" sx={{ flexGrow: 1 }}>企業横断オペレーション基盤</Typography>
          <Chip label={user?.role || '-'} size="small" sx={{ mr: 2, color: 'inherit', borderColor: 'inherit' }} variant="outlined" />
          <Button color="inherit" startIcon={<Logout />} onClick={logout}>ログアウト</Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 3 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}

        <Paper variant="outlined" sx={{ p: 2, mb: 3, bgcolor: 'action.hover' }}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>要対応・タスク・リスク サマリ</Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Card variant="outlined">
                <CardContent>
                  <Stack direction="row" alignItems="center" spacing={1}>
                    <Visibility color="warning" />
                    <Typography variant="h4">{dashboard?.observations.total ?? '-'}</Typography>
                  </Stack>
                  <Typography variant="body2" color="text.secondary">観測（要対応）</Typography>
                  <Stack direction="row" spacing={0.5} flexWrap="wrap" sx={{ mt: 1 }}>
                    {dashboard?.observations.by_domain && Object.entries(dashboard.observations.by_domain).map(([d, c]) => (
                      <Chip key={d} label={`${DOMAIN_LABELS[d] || d} ${c}`} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                    ))}
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card variant="outlined">
                <CardContent>
                  <Stack direction="row" alignItems="center" spacing={1}>
                    <Assignment color="primary" />
                    <Typography variant="h4">{dashboard?.tasks.total ?? '-'}</Typography>
                  </Stack>
                  <Typography variant="body2" color="text.secondary">タスク（未完了）</Typography>
                  <Stack direction="row" spacing={0.5} flexWrap="wrap" sx={{ mt: 1 }}>
                    {dashboard?.tasks.by_domain && Object.entries(dashboard.tasks.by_domain).map(([d, c]) => (
                      <Chip key={d} label={`${DOMAIN_LABELS[d] || d} ${c}`} size="small" color="primary" variant="outlined" sx={{ mr: 0.5, mb: 0.5 }} />
                    ))}
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card variant="outlined">
                <CardContent>
                  <Stack direction="row" alignItems="center" spacing={1}>
                    <Warning color="error" />
                    <Typography variant="h4">{dashboard?.risks.total ?? '-'}</Typography>
                  </Stack>
                  <Typography variant="body2" color="text.secondary">リスク（監視中）</Typography>
                  <Stack direction="row" spacing={0.5} flexWrap="wrap" sx={{ mt: 1 }}>
                    {dashboard?.risks.by_domain && Object.entries(dashboard.risks.by_domain).map(([d, c]) => (
                      <Chip key={d} label={`${DOMAIN_LABELS[d] || d} ${c}`} size="small" color="error" variant="outlined" sx={{ mr: 0.5, mb: 0.5 }} />
                    ))}
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
          <Stack direction="row" spacing={1} sx={{ mt: 2 }} flexWrap="wrap">
            <Button startIcon={<Refresh />} onClick={loadAll} disabled={loading}>更新</Button>
            <Button startIcon={<FileDownload />} size="small" onClick={() => handleExport('csv', 'dashboard')}>CSV</Button>
            <Button startIcon={<FileDownload />} size="small" onClick={() => handleExport('excel', 'dashboard')}>Excel</Button>
          </Stack>
        </Paper>

        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tab icon={<Visibility />} label="観測" iconPosition="start" />
          <Tab icon={<Assignment />} label="タスク" iconPosition="start" />
          <Tab icon={<Warning />} label="リスク" iconPosition="start" />
          <Tab
            icon={unreadAlerts.length > 0 ? <Badge badgeContent={unreadAlerts.length} color="error"><Notifications /></Badge> : <Notifications />}
            label={`アラート${unreadAlerts.length ? ` (${unreadAlerts.length})` : ''}`}
            iconPosition="start"
          />
        </Tabs>

        {tabValue === 0 && (
          <Box>
            <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap" sx={{ mb: 2 }}>
              <TextField size="small" label="検索" placeholder="タイトル・種別" value={searchObs} onChange={(e) => setSearchObs(e.target.value)} sx={{ minWidth: 200 }} />
              <FormControl size="small" sx={{ minWidth: 140 }}>
                <InputLabel>業種テンプレート</InputLabel>
                <Select value={industryTemplate} label="業種テンプレート" onChange={(e) => { setIndustryTemplate(e.target.value); localStorage.setItem('eoh_industry_template', e.target.value); }}>
                  <MenuItem value="general">汎用</MenuItem>
                  <MenuItem value="manufacturing">製造業</MenuItem>
                  <MenuItem value="medical">医療</MenuItem>
                  <MenuItem value="financial">金融</MenuItem>
                  <MenuItem value="sier">SIer</MenuItem>
                  <MenuItem value="public_sector">公共・官公庁</MenuItem>
                  <MenuItem value="retail">小売・EC</MenuItem>
                  <MenuItem value="education">教育</MenuItem>
                  <MenuItem value="legal">法務</MenuItem>
                </Select>
              </FormControl>
            </Stack>
            <Stack direction="row" justifyContent="flex-end" sx={{ mb: 1 }}>
              <Button size="small" startIcon={<FileDownload />} onClick={() => handleExport('csv', 'observations')}>CSV</Button>
              <Button size="small" startIcon={<FileDownload />} onClick={() => handleExport('excel', 'observations')}>Excel</Button>
            </Stack>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>ドメイン</TableCell>
                    <TableCell>種別</TableCell>
                    <TableCell>タイトル</TableCell>
                    <TableCell>重要度</TableCell>
                    <TableCell>状態</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {observations.map((o) => (
                    <TableRow key={o.id}>
                      <TableCell><Chip size="small" label={DOMAIN_LABELS[o.domain] || o.domain} /></TableCell>
                      <TableCell>{o.type}</TableCell>
                      <TableCell>{o.title}</TableCell>
                      <TableCell><Chip size="small" label={o.severity} color={o.severity === '高' ? 'error' : 'default'} /></TableCell>
                      <TableCell>{o.status}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {tabValue === 1 && (
          <Box>
            <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
              <TextField size="small" label="タスク検索" placeholder="タイトル・担当" value={searchTask} onChange={(e) => setSearchTask(e.target.value)} sx={{ minWidth: 200 }} />
            </Stack>
            {(user?.role === 'admin' || user?.role === 'operator') && (
              <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>タスク追加</Typography>
                <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap">
                  <TextField size="small" label="タイトル" value={newTaskTitle} onChange={(e) => setNewTaskTitle(e.target.value)} sx={{ minWidth: 200 }} />
                  <FormControl size="small" sx={{ minWidth: 140 }}>
                    <InputLabel>ドメイン</InputLabel>
                    <Select value={newTaskDomain} label="ドメイン" onChange={(e) => setNewTaskDomain(e.target.value)}>
                      {Object.entries(DOMAIN_LABELS).map(([k, v]) => (
                        <MenuItem key={k} value={k}>{v}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <Button variant="contained" startIcon={<Add />} onClick={handleAddTask}>追加</Button>
                </Stack>
              </Paper>
            )}
            <Stack direction="row" justifyContent="flex-end" sx={{ mb: 1 }}>
              <Button size="small" startIcon={<FileDownload />} onClick={() => handleExport('csv', 'tasks')}>CSV</Button>
              <Button size="small" startIcon={<FileDownload />} onClick={() => handleExport('excel', 'tasks')}>Excel</Button>
            </Stack>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>ドメイン</TableCell>
                    <TableCell>タイトル</TableCell>
                    <TableCell>担当</TableCell>
                    <TableCell>状態</TableCell>
                    <TableCell>操作</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {tasks.map((t) => (
                    <TableRow key={t.id}>
                      <TableCell><Chip size="small" label={DOMAIN_LABELS[t.domain] || t.domain} /></TableCell>
                      <TableCell>{t.title}</TableCell>
                      <TableCell>{t.assignee || '-'}</TableCell>
                      <TableCell>{t.status}</TableCell>
                      <TableCell>
                        {(user?.role === 'admin' || user?.role === 'operator') && (
                          <>
                            {t.status === '未着手' && <Button size="small" onClick={() => handleTaskStatus(t.id, '対応中')}>着手</Button>}
                            {t.status === '対応中' && <Button size="small" onClick={() => handleTaskStatus(t.id, '完了')}>完了</Button>}
                          </>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {tabValue === 2 && (
          <Box>
            <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
              <TextField size="small" label="リスク検索" placeholder="タイトル・種別" value={searchRisk} onChange={(e) => setSearchRisk(e.target.value)} sx={{ minWidth: 200 }} />
            </Stack>
            <Stack direction="row" justifyContent="flex-end" sx={{ mb: 1 }}>
              <Button size="small" startIcon={<FileDownload />} onClick={() => handleExport('csv', 'risks')}>CSV</Button>
              <Button size="small" startIcon={<FileDownload />} onClick={() => handleExport('excel', 'risks')}>Excel</Button>
            </Stack>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>ドメイン</TableCell>
                    <TableCell>種別</TableCell>
                    <TableCell>タイトル</TableCell>
                    <TableCell>レベル</TableCell>
                    <TableCell>状態</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {risks.map((r) => (
                    <TableRow key={r.id}>
                      <TableCell><Chip size="small" label={DOMAIN_LABELS[r.domain] || r.domain} /></TableCell>
                      <TableCell>{r.type}</TableCell>
                      <TableCell>{r.title}</TableCell>
                      <TableCell><Chip size="small" label={r.level} color={r.level === '高' ? 'error' : 'default'} /></TableCell>
                      <TableCell>{r.status}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {tabValue === 3 && (
          <TableContainer component={Paper} variant="outlined">
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>ドメイン</TableCell>
                  <TableCell>種別</TableCell>
                  <TableCell>タイトル</TableCell>
                  <TableCell>重要度</TableCell>
                  <TableCell>既読</TableCell>
                  <TableCell>操作</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {alerts.map((a) => (
                  <TableRow key={a.id} sx={{ bgcolor: a.read ? undefined : 'action.hover' }}>
                    <TableCell><Chip size="small" label={DOMAIN_LABELS[a.domain] || a.domain} /></TableCell>
                    <TableCell>{a.type}</TableCell>
                    <TableCell>{a.title}</TableCell>
                    <TableCell><Chip size="small" label={a.severity} color={a.severity === '高' || a.severity === '緊急' ? 'error' : 'default'} /></TableCell>
                    <TableCell>{a.read ? '既読' : '未読'}</TableCell>
                    <TableCell>
                      {!a.read && <Button size="small" onClick={() => handleMarkAlertRead(a.id)}>既読にする</Button>}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Container>
    </Box>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}
