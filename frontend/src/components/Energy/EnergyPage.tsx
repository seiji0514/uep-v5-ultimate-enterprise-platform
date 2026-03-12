/**
 * エネルギー ページ
 * 需給予測API・スマートグリッド制御・メトリクス。時系列予測・リアルタイム制御・監視基盤の経験を活かせる。
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
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
  Grid,
} from '@mui/material';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import {
  Bolt,
  ShowChart,
  GridOn,
  Speed,
} from '@mui/icons-material';
import {
  energyApi,
  DemandForecast,
  SmartGridControl,
  EnergyMetrics,
} from '../../api/energy';

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

export const EnergyPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [demandForecast, setDemandForecast] = useState<DemandForecast[]>([]);
  const [smartGrid, setSmartGrid] = useState<SmartGridControl[]>([]);
  const [metrics, setMetrics] = useState<EnergyMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) {
        const data = await energyApi.getDemandForecast();
        setDemandForecast(data);
      } else if (tabValue === 1) {
        const data = await energyApi.getSmartGridControl();
        setSmartGrid(data);
      } else if (tabValue === 2) {
        const data = await energyApi.getMetrics();
        setMetrics(data);
      }
    } catch (err: any) {
      console.error('Energy API Error:', err);
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

  const getZoneStatusColor = (status: string) => {
    if (status === '調整中') return 'warning';
    return 'success';
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          エネルギー
        </Typography>
        <Typography variant="body2" color="text.secondary">
          需給予測API・スマートグリッド制御・メトリクス。時系列予測・リアルタイム制御・監視基盤の経験を活かせる。
        </Typography>
      </Box>

      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<ShowChart />} iconPosition="start" label="需給予測API" />
          <Tab icon={<GridOn />} iconPosition="start" label="スマートグリッド制御" />
          <Tab icon={<Speed />} iconPosition="start" label="メトリクス" />
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
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>需給予測 時系列</Typography>
                <ResponsiveContainer width="100%" height={180}>
                  <BarChart data={demandForecast.map((d) => ({ name: d.hour, 予測: d.predicted_kwh, 実績: d.actual_kwh ?? 0 }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Bar dataKey="予測" fill="#5794F2" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="実績" fill="#73BF69" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>時刻</TableCell>
                      <TableCell>予測(kWh)</TableCell>
                      <TableCell>実績(kWh)</TableCell>
                      <TableCell>精度</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {demandForecast.map((d, i) => (
                      <TableRow key={i}>
                        <TableCell>{d.hour}</TableCell>
                        <TableCell>{d.predicted_kwh.toLocaleString()}</TableCell>
                        <TableCell>{d.actual_kwh != null ? d.actual_kwh.toLocaleString() : '-'}</TableCell>
                        <TableCell>{d.accuracy != null ? `${(d.accuracy * 100).toFixed(0)}%` : '-'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>ゾーン別 負荷率・再エネ比率</Typography>
                <ResponsiveContainer width="100%" height={180}>
                  <BarChart data={smartGrid.map((s) => ({ name: s.zone, 負荷率: s.load_percent, 再エネ: s.renewable_percent }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Bar dataKey="負荷率" fill="#F46800" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="再エネ" fill="#73BF69" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>ゾーン</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>負荷率(%)</TableCell>
                      <TableCell>再エネ比率(%)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {smartGrid.map((s) => (
                      <TableRow key={s.zone}>
                        <TableCell>{s.zone}</TableCell>
                        <TableCell>
                          <Chip size="small" label={s.status} color={getZoneStatusColor(s.status)} />
                        </TableCell>
                        <TableCell>{s.load_percent}</TableCell>
                        <TableCell>{s.renewable_percent}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              {metrics && (
                <>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>発電・消費 構成</Typography>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart margin={{ top: 20, right: 40, bottom: 20, left: 40 }}>
                      <Pie
                        data={[
                          { name: '発電量', value: metrics.total_generation_kwh },
                          { name: '消費量', value: metrics.total_consumption_kwh },
                        ]}
                        cx="50%"
                        cy="50%"
                        innerRadius={50}
                        outerRadius={80}
                        paddingAngle={2}
                        dataKey="value"
                        label={({ name, value }) => `${name}: ${(value / 1000).toFixed(1)}k kWh`}
                      >
                        <Cell fill="#5794F2" />
                        <Cell fill="#F46800" />
                      </Pie>
                      <Tooltip formatter={(v: number | undefined) => [v != null ? `${v.toLocaleString()} kWh` : '', '']} />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">発電量</Typography>
                      <Typography variant="h6">{metrics.total_generation_kwh.toLocaleString()} kWh</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">消費量</Typography>
                      <Typography variant="h6">{metrics.total_consumption_kwh.toLocaleString()} kWh</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">再エネ比率</Typography>
                      <Typography variant="h6">{(metrics.renewable_ratio * 100).toFixed(1)}%</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">系統安定性</Typography>
                      <Typography variant="h6">{metrics.grid_stability}%</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="caption" color="text.secondary">
                      最終更新: {new Date(metrics.last_updated).toLocaleString()}
                    </Typography>
                  </Grid>
                </Grid>
                </>
              )}
            </TabPanel>
          </>
        )}
      </Paper>

      <Paper sx={{ p: 2, mt: 2 }} elevation={0}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <Bolt color="primary" />
          <Typography variant="overline" color="text.secondary">技術スタック</Typography>
        </Box>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          <Chip size="small" label="時系列予測" />
          <Chip size="small" label="Kafka" />
          <Chip size="small" label="Prometheus" />
          <Chip size="small" label="Grafana" />
          <Chip size="small" label="リアルタイム制御" />
        </Box>
      </Paper>
    </Box>
  );
};
