/**
 * 統合ビジネスプラットフォーム ページ
 * 業務効率化・DX / 人材・組織 / 顧客対応・CX の3システム統合
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import {
  AccountTree,
  People,
  Support,
  Assignment,
  SmartToy,
  Accessibility,
  Checklist,
} from '@mui/icons-material';
import { unifiedBusinessApi, PlatformSummary } from '../../api/unifiedBusiness';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  const isActive = value === index;
  return (
    <div
      role="tabpanel"
      hidden={!isActive}
      style={{ display: isActive ? 'block' : 'none' }}
      {...other}
    >
      <Box sx={{ p: 2 }}>{children}</Box>
    </div>
  );
}

export const UnifiedBusinessPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [summary, setSummary] = useState<PlatformSummary | null>(null);
  const [workflows, setWorkflows] = useState<any[]>([]);
  const [approvalRequests, setApprovalRequests] = useState<any[]>([]);
  const [rpaJobs, setRpaJobs] = useState<any[]>([]);
  const [disabilitySupports, setDisabilitySupports] = useState<any[]>([]);
  const [checklist, setChecklist] = useState<any[]>([]);
  const [onboardingTasks, setOnboardingTasks] = useState<any[]>([]);
  const [tickets, setTickets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadSummary();
  }, []);

  useEffect(() => {
    if (tabValue === 0) loadSummary();
    else if (tabValue === 1) loadWorkflowData();
    else if (tabValue === 2) loadHrData();
    else if (tabValue === 3) loadCustomerData();
  }, [tabValue]);

  const loadSummary = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await unifiedBusinessApi.getSummary();
      setSummary(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const loadWorkflowData = async () => {
    try {
      setLoading(true);
      setError('');
      const [w, a, r] = await Promise.all([
        unifiedBusinessApi.getWorkflows(),
        unifiedBusinessApi.getApprovalRequests(),
        unifiedBusinessApi.getRpaJobs(),
      ]);
      setWorkflows(w);
      setApprovalRequests(a);
      setRpaJobs(r);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const loadHrData = async () => {
    try {
      setLoading(true);
      setError('');
      const [supports, cl, tasks] = await Promise.all([
        unifiedBusinessApi.getDisabilitySupports(),
        unifiedBusinessApi.getAccommodationChecklist(),
        unifiedBusinessApi.getOnboardingTasks(),
      ]);
      setDisabilitySupports(supports);
      setChecklist(cl);
      setOnboardingTasks(tasks);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const loadCustomerData = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await unifiedBusinessApi.getTickets();
      setTickets(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <AccountTree /> 統合ビジネスプラットフォーム
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
        業務効率化・DX / 人材・組織 / 顧客対応・CX の3システムを統合
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} sx={{ mb: 2 }}>
        <Tab label="サマリー" icon={<Assignment />} iconPosition="start" />
        <Tab label="業務効率化・DX" icon={<AccountTree />} iconPosition="start" />
        <Tab label="人材・組織" icon={<People />} iconPosition="start" />
        <Tab label="顧客対応・CX" icon={<Support />} iconPosition="start" />
      </Tabs>

      <TabPanel value={tabValue} index={0}>
        {loading ? (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        ) : summary ? (
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <AccountTree /> 業務効率化・DX
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    ワークフロー: {summary.modules['業務効率化・DX'].workflows}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    申請・承認: {summary.modules['業務効率化・DX'].approval_requests}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    RPAジョブ: {summary.modules['業務効率化・DX'].rpa_jobs}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <People /> 人材・組織
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    障害者雇用支援: {summary.modules['人材・組織'].disability_supports}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    オンボーディングタスク: {summary.modules['人材・組織'].onboarding_tasks}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Support /> 顧客対応・CX
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    チケット: {summary.modules['顧客対応・CX'].tickets}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        ) : null}
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        {loading ? (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>ワークフロー</Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>名前</TableCell>
                          <TableCell>ステータス</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {workflows.length === 0 ? (
                          <TableRow><TableCell colSpan={2}>データなし</TableCell></TableRow>
                        ) : (
                          workflows.map((w) => (
                            <TableRow key={w.id}>
                              <TableCell>{w.name}</TableCell>
                              <TableCell><Chip label={w.status} size="small" /></TableCell>
                            </TableRow>
                          ))
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>申請・承認</Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>タイトル</TableCell>
                          <TableCell>ステータス</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {approvalRequests.length === 0 ? (
                          <TableRow><TableCell colSpan={2}>データなし</TableCell></TableRow>
                        ) : (
                          approvalRequests.map((a) => (
                            <TableRow key={a.id}>
                              <TableCell>{a.title}</TableCell>
                              <TableCell><Chip label={a.status} size="small" /></TableCell>
                            </TableRow>
                          ))
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <SmartToy /> RPAジョブ
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>名前</TableCell>
                          <TableCell>ステータス</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {rpaJobs.length === 0 ? (
                          <TableRow><TableCell colSpan={2}>データなし</TableCell></TableRow>
                        ) : (
                          rpaJobs.map((j) => (
                            <TableRow key={j.id}>
                              <TableCell>{j.name}</TableCell>
                              <TableCell><Chip label={j.status} size="small" /></TableCell>
                            </TableRow>
                          ))
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        {loading ? (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Accessibility /> 障害者雇用支援
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>社員ID</TableCell>
                          <TableCell>配慮事項</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {disabilitySupports.length === 0 ? (
                          <TableRow><TableCell colSpan={2}>データなし</TableCell></TableRow>
                        ) : (
                          disabilitySupports.map((s) => (
                            <TableRow key={s.id}>
                              <TableCell>{s.employee_id}</TableCell>
                              <TableCell>{s.accommodations?.join(', ') || '-'}</TableCell>
                            </TableRow>
                          ))
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Checklist /> 合理的配慮チェックリスト
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>カテゴリ</TableCell>
                          <TableCell>項目</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {checklist.map((c) => (
                          <TableRow key={c.id}>
                            <TableCell>{c.category}</TableCell>
                            <TableCell>{c.name}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>オンボーディングタスク</Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>タスク名</TableCell>
                          <TableCell>カテゴリ</TableCell>
                          <TableCell>ステータス</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {onboardingTasks.length === 0 ? (
                          <TableRow><TableCell colSpan={3}>データなし</TableCell></TableRow>
                        ) : (
                          onboardingTasks.map((t) => (
                            <TableRow key={t.id}>
                              <TableCell>{t.task_name}</TableCell>
                              <TableCell>{t.category}</TableCell>
                              <TableCell><Chip label={t.status} size="small" /></TableCell>
                            </TableRow>
                          ))
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </TabPanel>

      <TabPanel value={tabValue} index={3}>
        {loading ? (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        ) : (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>チケット一覧</Typography>
              <TableContainer component={Paper}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>件名</TableCell>
                      <TableCell>優先度</TableCell>
                      <TableCell>ステータス</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {tickets.length === 0 ? (
                      <TableRow><TableCell colSpan={3}>データなし</TableCell></TableRow>
                    ) : (
                      tickets.map((t) => (
                        <TableRow key={t.id}>
                          <TableCell>{t.subject}</TableCell>
                          <TableCell><Chip label={t.priority} size="small" /></TableCell>
                          <TableCell><Chip label={t.status} size="small" /></TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        )}
      </TabPanel>
    </Box>
  );
};
