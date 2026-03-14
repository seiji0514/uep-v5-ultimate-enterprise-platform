/**
 * 金融・FinTech ページ
 * 決済API・リスクスコア・取引監視。高可用性・低レイテンシ・監視の経験をそのまま活かせる。
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import {
  Security,
  Payment,
  Assessment,
  Visibility,
} from '@mui/icons-material';
import {
  fintechApi,
  Payment as PaymentType,
  RiskScore,
  TransactionMonitoring,
} from '../../api/fintech';
import { useAutoPlayNarration } from '../../hooks/useAutoPlayNarration';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  );
}

export const FinTechPage: React.FC = () => {
  useAutoPlayNarration(4);
  const [tabValue, setTabValue] = useState(0);
  const [payments, setPayments] = useState<PaymentType[]>([]);
  const [riskScores, setRiskScores] = useState<RiskScore[]>([]);
  const [monitoring, setMonitoring] = useState<TransactionMonitoring[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [p, r, m] = await Promise.all([
        fintechApi.getPayments(),
        fintechApi.getRiskScores(),
        fintechApi.getTransactionMonitoring(),
      ]);
      setPayments(p);
      setRiskScores(r);
      setMonitoring(m);
    } catch (err: any) {
      console.error('FinTech API Error:', err);
      if (err.code === 'ECONNREFUSED' || err.message?.includes('Network Error')) {
        setError('バックエンドサーバーに接続できません。');
      } else if (err.response?.status === 401) {
        setError('ログインが必要です。');
      } else {
        setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelColor = (level: string) => {
    if (level === '高') return 'error';
    if (level === '中') return 'warning';
    return 'success';
  };

  const getMonitoringStatusColor = (status: string) => {
    if (status === '要確認') return 'error';
    if (status === '監視中') return 'warning';
    return 'success';
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          金融・FinTech
        </Typography>
        <Typography variant="body2" color="text.secondary">
          決済API・リスクスコア・取引監視。高可用性・低レイテンシ・監視の経験をそのまま活かせる。
        </Typography>
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
          公開データ: Kaggle 不正検知、取引シミュレーションなどでリスクモデル・異常検知の検証が可能。
        </Typography>
      </Box>

      {!loading && (
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6} sm={3}>
            <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">決済件数</Typography>
              <Typography variant="h6">{payments.length}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">決済合計</Typography>
              <Typography variant="h6">¥{(payments.reduce((s, p) => s + p.amount, 0) / 10000).toFixed(0)}万</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">リスク高</Typography>
              <Typography variant="h6" color="error.main">{riskScores.filter((r) => r.level === '高').length}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">監視要確認</Typography>
              <Typography variant="h6" color="warning.main">{monitoring.filter((m) => m.status === '要確認').length}</Typography>
            </Paper>
          </Grid>
        </Grid>
      )}

      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<Payment />} iconPosition="start" label="決済API" />
          <Tab icon={<Assessment />} iconPosition="start" label="リスクスコア" />
          <Tab icon={<Visibility />} iconPosition="start" label="取引監視" />
        </Tabs>

        {error && (
          <Alert severity="error" sx={{ m: 2 }} onClose={() => setError('')}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <TabPanel value={tabValue} index={0}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={5}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>決済 ステータス構成</Typography>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart margin={{ top: 20, right: 40, bottom: 20, left: 40 }}>
                      <Pie
                        data={(() => {
                          const m: Record<string, number> = {};
                          payments.forEach((p) => { m[p.status] = (m[p.status] || 0) + 1; });
                          return Object.entries(m).map(([name, value]) => ({ name, value }));
                        })()}
                        cx="50%"
                        cy="50%"
                        innerRadius={40}
                        outerRadius={70}
                        paddingAngle={2}
                        dataKey="value"
                        label={({ name, value }) => `${name}: ${value}`}
                      >
                        {(() => {
                          const m: Record<string, number> = {};
                          payments.forEach((p) => { m[p.status] = (m[p.status] || 0) + 1; });
                          return Object.entries(m).map((_, i) => (
                            <Cell key={i} fill={['#73BF69', '#5794F2', '#F46800'][i % 3]} />
                          ));
                        })()}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </Grid>
                <Grid item xs={12} md={7}>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>ID</TableCell>
                      <TableCell>金額</TableCell>
                      <TableCell>通貨</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>作成日時</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {payments.map((p) => (
                      <TableRow key={p.id}>
                        <TableCell>{p.id}</TableCell>
                        <TableCell>{p.amount.toLocaleString()}</TableCell>
                        <TableCell>{p.currency}</TableCell>
                        <TableCell>
                          <Chip size="small" label={p.status} color={p.status === '完了' ? 'success' : 'default'} />
                        </TableCell>
                        <TableCell>{new Date(p.created_at).toLocaleString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
                </Grid>
              </Grid>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>リスクスコア レベル構成</Typography>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart margin={{ top: 20, right: 40, bottom: 20, left: 40 }}>
                    <Pie
                      data={(() => {
                        const m: Record<string, number> = {};
                        riskScores.forEach((r) => { m[r.level] = (m[r.level] || 0) + 1; });
                        return Object.entries(m).map(([name, value]) => ({ name, value }));
                      })()}
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={70}
                      paddingAngle={2}
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}`}
                    >
                      {(() => {
                        const m: Record<string, number> = {};
                        riskScores.forEach((r) => { m[r.level] = (m[r.level] || 0) + 1; });
                        return Object.entries(m).map((_, i) => (
                          <Cell key={i} fill={['#E02F44', '#F46800', '#73BF69'][i % 3]} />
                        ));
                      })()}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>取引ID</TableCell>
                      <TableCell>リスクスコア</TableCell>
                      <TableCell>レベル</TableCell>
                      <TableCell>要因</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {riskScores.map((r) => (
                      <TableRow key={r.transaction_id}>
                        <TableCell>{r.transaction_id}</TableCell>
                        <TableCell>{(r.risk_score * 100).toFixed(0)}%</TableCell>
                        <TableCell>
                          <Chip size="small" label={r.level} color={getRiskLevelColor(r.level)} />
                        </TableCell>
                        <TableCell>{r.factors.join(', ')}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>取引金額 比較</Typography>
                <ResponsiveContainer width="100%" height={160}>
                  <BarChart data={monitoring.map((m) => ({ name: m.type, 金額: m.amount }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `¥${(v / 10000).toFixed(0)}万`} />
                    <Tooltip formatter={(v: number | undefined) => [v != null ? `¥${v.toLocaleString()}` : '', '金額']} />
                    <Bar dataKey="金額" fill="#F46800" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>種別</TableCell>
                      <TableCell>金額</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>アラート</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {monitoring.map((m) => (
                      <TableRow key={m.id}>
                        <TableCell>{m.type}</TableCell>
                        <TableCell>¥{m.amount.toLocaleString()}</TableCell>
                        <TableCell>
                          <Chip size="small" label={m.status} color={getMonitoringStatusColor(m.status)} />
                        </TableCell>
                        <TableCell>{m.alert || '-'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
          </>
        )}
      </Paper>

      <Paper sx={{ p: 2, mt: 2 }} elevation={0}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <Security color="primary" />
          <Typography variant="overline" color="text.secondary">技術スタック</Typography>
        </Box>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          <Chip size="small" label="高可用性" />
          <Chip size="small" label="低レイテンシ" />
          <Chip size="small" label="Zero Trust" />
          <Chip size="small" label="mTLS" />
          <Chip size="small" label="監視基盤" />
        </Box>
      </Paper>
    </Box>
  );
};
