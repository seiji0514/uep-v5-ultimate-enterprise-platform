/**
 * 製造・IoT ページ
 * 予知保全・センサーデータ・異常検知。インフラ・監視・MLOpsとの相性が良く、製造業DXの需要が高い。
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Chip,
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
} from '@mui/material';
import { PieChart, Pie, Cell, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import {
  PrecisionManufacturing,
  Build,
  Sensors,
  Warning,
} from '@mui/icons-material';
import {
  manufacturingApi,
  PredictiveMaintenance,
  SensorData,
  Anomaly,
} from '../../api/manufacturing';
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

export const ManufacturingPage: React.FC = () => {
  useAutoPlayNarration(1);
  const [tabValue, setTabValue] = useState(0);
  const [predictiveMaintenance, setPredictiveMaintenance] = useState<PredictiveMaintenance[]>([]);
  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
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
        const [pmData, anomData] = await Promise.all([
          manufacturingApi.getPredictiveMaintenance(),
          manufacturingApi.getAnomalies(),
        ]);
        setPredictiveMaintenance(pmData);
        setAnomalies(anomData);
      } else if (tabValue === 1) {
        const data = await manufacturingApi.getSensorData();
        setSensorData(data);
      } else if (tabValue === 2) {
        const data = await manufacturingApi.getAnomalies();
        setAnomalies(data);
      }
    } catch (err: any) {
      console.error('Manufacturing API Error:', err);
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

  const getStatusColor = (status: string) => {
    if (status.includes('要メンテナンス')) return 'error';
    if (status.includes('監視中')) return 'info';
    return 'success';
  };

  const getSeverityColor = (severity: string) => {
    if (severity === '高') return 'error';
    if (severity === '中') return 'warning';
    return 'success';
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          製造・IoT
        </Typography>
        <Typography variant="body2" color="text.secondary">
          予知保全・センサーデータ・異常検知。インフラ・監視・MLOpsとの相性が良く、製造業DXの需要が高い。
        </Typography>
      </Box>

      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<PrecisionManufacturing />} iconPosition="start" label="予知保全API" />
          <Tab icon={<Sensors />} iconPosition="start" label="センサーデータ" />
          <Tab icon={<Warning />} iconPosition="start" label="異常検知" />
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
              <Grid container spacing={2} sx={{ mb: 2 }}>
                <Grid item xs={6} sm={4} md={2}>
                  <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                    <Typography variant="caption" color="text.secondary">機器数</Typography>
                    <Typography variant="h6">{predictiveMaintenance.length}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} sm={4} md={2}>
                  <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                    <Typography variant="caption" color="text.secondary">要メンテ</Typography>
                    <Typography variant="h6" color="error">{predictiveMaintenance.filter((p) => p.status === '要メンテナンス').length}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} sm={4} md={2}>
                  <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                    <Typography variant="caption" color="text.secondary">監視中</Typography>
                    <Typography variant="h6" color="success.main">{predictiveMaintenance.filter((p) => p.status === '監視中').length}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} sm={4} md={2}>
                  <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                    <Typography variant="caption" color="text.secondary">異常件数</Typography>
                    <Typography variant="h6" color="error">{anomalies.length}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} sm={4} md={2}>
                  <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                    <Typography variant="caption" color="text.secondary">平均 RUL</Typography>
                    <Typography variant="h6">-</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} sm={4} md={2}>
                  <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                    <Typography variant="caption" color="text.secondary">モデル推移</Typography>
                    <Typography variant="h6">&nbsp;</Typography>
                  </Paper>
                </Grid>
              </Grid>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>設備別 RUL (相対寿命)</Typography>
                <ResponsiveContainer width="100%" height={140}>
                  <LineChart data={predictiveMaintenance.map((p, i) => ({ name: p.equipment, RUL: 2 - i * 0.3 }))} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                    <YAxis domain={[0, 4]} tick={{ fontSize: 10 }} />
                    <Tooltip />
                    <Line type="monotone" dataKey="RUL" stroke="#5794F2" strokeWidth={2} dot={{ r: 3 }} />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
              <Grid container spacing={2}>
                <Grid item xs={12} md={5}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>予知保全ステータス概況</Typography>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart margin={{ top: 20, right: 40, bottom: 20, left: 40 }}>
                      <Pie
                        data={(() => {
                          const m: Record<string, number> = {};
                          predictiveMaintenance.forEach((pm) => { m[pm.status] = (m[pm.status] || 0) + 1; });
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
                          predictiveMaintenance.forEach((pm) => { m[pm.status] = (m[pm.status] || 0) + 1; });
                          return Object.entries(m).map((_, i) => (
                            <Cell key={i} fill={['#E02F44', '#F46800', '#73BF69'][i % 3]} />
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
                          <TableCell>設備</TableCell>
                          <TableCell>予測故障日</TableCell>
                          <TableCell>信頼度</TableCell>
                          <TableCell>ステータス</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {predictiveMaintenance.map((pm) => (
                          <TableRow key={pm.id}>
                            <TableCell>{pm.equipment}</TableCell>
                            <TableCell>{pm.predicted_failure.replace(/-/g, '/')}</TableCell>
                            <TableCell>{(pm.confidence * 100).toFixed(0)}%</TableCell>
                            <TableCell>
                              <Chip size="small" label={pm.status} color={getStatusColor(pm.status)} />
                            </TableCell>
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
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>センサー値 比較</Typography>
                <ResponsiveContainer width="100%" height={160}>
                  <BarChart data={sensorData.map((s) => ({ name: s.sensor_id, 値: s.value, 単位: s.unit }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip formatter={(v: unknown, _: unknown, props: { payload?: { 単位?: string } }) => [v != null && props?.payload?.単位 != null ? `${v} ${props.payload.単位}` : '', '値']} />
                    <Bar dataKey="値" fill="#5794F2" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>センサーID</TableCell>
                      <TableCell>値</TableCell>
                      <TableCell>単位</TableCell>
                      <TableCell>取得時刻</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {sensorData.map((s) => (
                      <TableRow key={s.sensor_id}>
                        <TableCell>{s.sensor_id}</TableCell>
                        <TableCell>{s.value}</TableCell>
                        <TableCell>{s.unit}</TableCell>
                        <TableCell>{new Date(s.timestamp).toLocaleString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={5}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>異常検知 深刻度構成</Typography>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart margin={{ top: 20, right: 40, bottom: 20, left: 40 }}>
                      <Pie
                        data={(() => {
                          const m: Record<string, number> = {};
                          anomalies.forEach((a) => { m[a.severity] = (m[a.severity] || 0) + 1; });
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
                          anomalies.forEach((a) => { m[a.severity] = (m[a.severity] || 0) + 1; });
                          return Object.entries(m).map((_, i) => (
                            <Cell key={i} fill={['#E02F44', '#F46800', '#73BF69'][i % 3]} />
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
                          <TableCell>種別</TableCell>
                          <TableCell>設備</TableCell>
                          <TableCell>深刻度</TableCell>
                          <TableCell>検知時刻</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {anomalies.map((a) => (
                      <TableRow key={a.id}>
                        <TableCell>{a.type}</TableCell>
                        <TableCell>{a.equipment}</TableCell>
                        <TableCell>
                          <Chip size="small" label={a.severity} color={getSeverityColor(a.severity)} />
                        </TableCell>
                        <TableCell>{new Date(a.detected_at).toLocaleString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
                </Grid>
              </Grid>
            </TabPanel>
          </>
        )}
      </Paper>

      <Paper sx={{ p: 2, mt: 2 }} elevation={0}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <Build color="primary" />
          <Typography variant="overline" color="text.secondary">連携スタック</Typography>
        </Box>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          <Chip size="small" label="MLOps" />
          <Chip size="small" label="Prometheus" />
          <Chip size="small" label="Grafana" />
          <Chip size="small" label="熱流体解析" />
          <Chip size="small" label="IoT" />
        </Box>
      </Paper>
    </Box>
  );
};
