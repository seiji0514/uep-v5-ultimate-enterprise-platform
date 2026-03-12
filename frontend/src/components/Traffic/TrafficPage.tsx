/**
 * 交通 ページ
 * 交通管理、航空管制、スマートシティ持続可能性プラットフォーム。
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
  Traffic,
  Flight,
  Park,
} from '@mui/icons-material';
import {
  trafficApi,
  TrafficManagement,
  AirTrafficControl,
  SmartCitySustainability,
} from '../../api/traffic';

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

export const TrafficPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [trafficMgmt, setTrafficMgmt] = useState<TrafficManagement[]>([]);
  const [atc, setAtc] = useState<AirTrafficControl[]>([]);
  const [sustainability, setSustainability] = useState<SmartCitySustainability | null>(null);
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
        const data = await trafficApi.getTrafficManagement();
        setTrafficMgmt(data);
      } else if (tabValue === 1) {
        const data = await trafficApi.getAirTrafficControl();
        setAtc(data);
      } else if (tabValue === 2) {
        const data = await trafficApi.getSmartCitySustainability();
        setSustainability(data);
      }
    } catch (err: any) {
      console.error('Traffic API Error:', err);
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

  const getCongestionColor = (status: string) => {
    if (status === '渋滞') return 'error';
    if (status === '混雑') return 'warning';
    return 'success';
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          交通
        </Typography>
        <Typography variant="body2" color="text.secondary">
          交通管理、航空管制、スマートシティ持続可能性プラットフォーム。
        </Typography>
      </Box>

      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<Traffic />} iconPosition="start" label="交通管理" />
          <Tab icon={<Flight />} iconPosition="start" label="航空管制" />
          <Tab icon={<Park />} iconPosition="start" label="スマートシティ持続可能性" />
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
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>ゾーン別 混雑度</Typography>
                <ResponsiveContainer width="100%" height={180}>
                  <BarChart data={trafficMgmt.map((t) => ({ name: t.zone, 混雑度: Math.round(t.congestion_level * 100) }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `${v}%`} domain={[0, 100]} />
                    <Tooltip formatter={(v: number | undefined) => [v != null ? `${v}%` : '', '混雑度']} />
                    <Bar dataKey="混雑度" fill="#F46800" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>ゾーン</TableCell>
                      <TableCell>混雑度</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>信号調整</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {trafficMgmt.map((t) => (
                      <TableRow key={t.id}>
                        <TableCell>{t.zone}</TableCell>
                        <TableCell>{(t.congestion_level * 100).toFixed(0)}%</TableCell>
                        <TableCell>
                          <Chip size="small" label={t.status} color={getCongestionColor(t.status)} />
                        </TableCell>
                        <TableCell>{t.signal_adjustment}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>便名</TableCell>
                      <TableCell>高度(ft)</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>到着(分)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {atc.map((a) => (
                      <TableRow key={a.id}>
                        <TableCell>{a.flight}</TableCell>
                        <TableCell>{a.altitude_ft.toLocaleString()}</TableCell>
                        <TableCell><Chip size="small" label={a.status} /></TableCell>
                        <TableCell>{a.eta_minutes}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              {sustainability && (
                <>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>持続可能性 メトリクス</Typography>
                  <ResponsiveContainer width="100%" height={180}>
                    <BarChart data={[
                      { name: 'CO2削減(kg)', 値: sustainability.co2_reduction_today_kg },
                      { name: 'EV充電', 値: sustainability.ev_charging_sessions },
                      { name: '公共交通(千)', 値: Math.round(sustainability.public_transit_ridership / 1000) },
                      { name: '最適化(×100)', 値: Math.round(sustainability.traffic_flow_optimization * 100) },
                    ]}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                      <YAxis tick={{ fontSize: 11 }} />
                      <Tooltip />
                      <Bar dataKey="値" fill="#73BF69" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">本日のCO2削減</Typography>
                      <Typography variant="h6">{sustainability.co2_reduction_today_kg.toLocaleString()} kg</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">EV充電セッション</Typography>
                      <Typography variant="h6">{sustainability.ev_charging_sessions}</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">公共交通利用者数</Typography>
                      <Typography variant="h6">{sustainability.public_transit_ridership.toLocaleString()}</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">交通流最適化</Typography>
                      <Typography variant="h6">{(sustainability.traffic_flow_optimization * 100).toFixed(0)}%</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="caption" color="text.secondary">
                      最終更新: {new Date(sustainability.last_updated).toLocaleString()}
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
        <Typography variant="overline" color="text.secondary">技術スタック</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
          <Chip size="small" label="交通制御" />
          <Chip size="small" label="航空管制" />
          <Chip size="small" label="スマートシティ" />
          <Chip size="small" label="持続可能性" />
        </Box>
      </Paper>
    </Box>
  );
};
