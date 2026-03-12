/**
 * 宇宙・航空 ページ
 * 衛星軌道追跡、航空宇宙システム、時空操作。
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
} from '@mui/material';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import {
  Satellite,
  RocketLaunch,
  Schedule,
} from '@mui/icons-material';
import {
  spaceApi,
  SatelliteTracking,
  AerospaceSystem,
  SpacetimeOperation,
} from '../../api/space';

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

export const SpacePage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [satellites, setSatellites] = useState<SatelliteTracking[]>([]);
  const [systems, setSystems] = useState<AerospaceSystem[]>([]);
  const [operations, setOperations] = useState<SpacetimeOperation[]>([]);
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
        const data = await spaceApi.getSatelliteTracking();
        setSatellites(data);
      } else if (tabValue === 1) {
        const data = await spaceApi.getAerospaceSystems();
        setSystems(data);
      } else if (tabValue === 2) {
        const data = await spaceApi.getSpacetimeOperations();
        setOperations(data);
      }
    } catch (err: any) {
      console.error('Space API Error:', err);
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

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          宇宙・航空
        </Typography>
        <Typography variant="body2" color="text.secondary">
          衛星軌道追跡、航空宇宙システム、時空操作。
        </Typography>
      </Box>

      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<Satellite />} iconPosition="start" label="衛星軌道追跡" />
          <Tab icon={<RocketLaunch />} iconPosition="start" label="航空宇宙システム" />
          <Tab icon={<Schedule />} iconPosition="start" label="時空操作" />
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
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>衛星 ステータス構成</Typography>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart margin={{ top: 20, right: 40, bottom: 20, left: 40 }}>
                    <Pie
                      data={(() => {
                        const m: Record<string, number> = {};
                        satellites.forEach((s) => { m[s.status] = (m[s.status] || 0) + 1; });
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
                        satellites.forEach((s) => { m[s.status] = (m[s.status] || 0) + 1; });
                        return Object.entries(m).map((_, i) => (
                          <Cell key={i} fill={['#73BF69', '#F46800', '#5794F2'][i % 3]} />
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
                      <TableCell>衛星名</TableCell>
                      <TableCell>軌道</TableCell>
                      <TableCell>高度(km)</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>次回通過</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {satellites.map((s) => (
                      <TableRow key={s.id}>
                        <TableCell>{s.name}</TableCell>
                        <TableCell>{s.orbit}</TableCell>
                        <TableCell>{s.altitude_km.toLocaleString()}</TableCell>
                        <TableCell><Chip size="small" label={s.status} color={s.status === '正常' ? 'success' : 'warning'} /></TableCell>
                        <TableCell>{s.next_pass ? new Date(s.next_pass).toLocaleString() : '-'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>システム稼働率</Typography>
                <ResponsiveContainer width="100%" height={160}>
                  <BarChart data={systems.map((s) => ({ name: s.system, 稼働率: s.uptime_percent }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                    <YAxis tick={{ fontSize: 11 }} domain={[99.5, 100]} />
                    <Tooltip formatter={(v: number | undefined) => [v != null ? `${v}%` : '', '稼働率']} />
                    <Bar dataKey="稼働率" fill="#5794F2" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>システム</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>稼働率(%)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {systems.map((s) => (
                      <TableRow key={s.id}>
                        <TableCell>{s.system}</TableCell>
                        <TableCell><Chip size="small" label={s.status} color="success" /></TableCell>
                        <TableCell>{s.uptime_percent}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>操作</TableCell>
                      <TableCell>衛星</TableCell>
                      <TableCell>予定日時</TableCell>
                      <TableCell>ステータス</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {operations.map((o) => (
                      <TableRow key={o.id}>
                        <TableCell>{o.operation}</TableCell>
                        <TableCell>{o.satellite}</TableCell>
                        <TableCell>{new Date(o.scheduled).toLocaleString()}</TableCell>
                        <TableCell><Chip size="small" label={o.status} /></TableCell>
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
        <Typography variant="overline" color="text.secondary">技術スタック</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
          <Chip size="small" label="軌道計算" />
          <Chip size="small" label="テレメトリ" />
          <Chip size="small" label="時系列分析" />
          <Chip size="small" label="リアルタイム制御" />
        </Box>
      </Paper>
    </Box>
  );
};
