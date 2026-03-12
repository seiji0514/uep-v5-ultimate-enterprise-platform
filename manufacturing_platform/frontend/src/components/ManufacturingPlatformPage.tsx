/**
 * 製造・IoTプラットフォーム
 * 予知保全・センサーデータ・異常検知
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  Stack,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  PrecisionManufacturing,
  Sensors,
  Warning,
  Refresh,
} from '@mui/icons-material';
import { manufacturingApi, type PredictiveMaintenance, type SensorData, type Anomaly } from '../api';

export const ManufacturingPlatformPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [predictive, setPredictive] = useState<PredictiveMaintenance[]>([]);
  const [sensors, setSensors] = useState<SensorData[]>([]);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [pm, sd, an] = await Promise.all([
        manufacturingApi.getPredictiveMaintenance(),
        manufacturingApi.getSensorData(),
        manufacturingApi.getAnomalies(),
      ]);
      setPredictive(pm.items || []);
      setSensors(sd.items || []);
      setAnomalies(an.items || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const getSeverityColor = (s: string) =>
    ['高', 'critical', 'high'].includes(s || '') ? 'error' : s === '中' ? 'warning' : 'info';

  return (
    <Box>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={4}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">予知保全</Typography>
              <Typography variant="h4">{predictive.length}</Typography>
              <Typography variant="caption" color="text.secondary">
                要メンテ: {predictive.filter((p) => p.status === '要メンテナンス').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">センサーデータ</Typography>
              <Typography variant="h4">{sensors.length}</Typography>
              <Typography variant="caption" color="text.secondary">リアルタイム</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">異常検知</Typography>
              <Typography variant="h4">{anomalies.length}</Typography>
              <Typography variant="caption" color="text.secondary">
                高: {anomalies.filter((a) => a.severity === '高').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Typography variant="h5" component="h1" gutterBottom>
        製造・IoTプラットフォーム
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        予知保全・センサーデータ（OPC-UA）・異常検知
      </Typography>

      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip
          icon={<PrecisionManufacturing />}
          label="予知保全"
          onClick={() => setTabValue(0)}
          color={tabValue === 0 ? 'primary' : 'default'}
          variant={tabValue === 0 ? 'filled' : 'outlined'}
        />
        <Chip
          icon={<Sensors />}
          label="センサーデータ"
          onClick={() => setTabValue(1)}
          color={tabValue === 1 ? 'primary' : 'default'}
          variant={tabValue === 1 ? 'filled' : 'outlined'}
        />
        <Chip
          icon={<Warning />}
          label="異常検知"
          onClick={() => setTabValue(2)}
          color={tabValue === 2 ? 'primary' : 'default'}
          variant={tabValue === 2 ? 'filled' : 'outlined'}
        />
        <Chip icon={<Refresh />} label="更新" onClick={loadData} variant="outlined" />
      </Stack>

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}

      {loading ? (
        <Box sx={{ p: 4, textAlign: 'center' }}><CircularProgress /></Box>
      ) : (
        <>
          {tabValue === 0 && (
            <TableContainer component={Paper} variant="outlined">
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
                  {predictive.map((p) => (
                    <TableRow key={p.id} hover>
                      <TableCell>{p.equipment}</TableCell>
                      <TableCell>{p.predicted_failure}</TableCell>
                      <TableCell>{(p.confidence * 100).toFixed(0)}%</TableCell>
                      <TableCell><Chip label={p.status} size="small" color={p.status === '要メンテナンス' ? 'error' : 'default'} /></TableCell>
                    </TableRow>
                  ))}
                  {predictive.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {tabValue === 1 && (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>センサーID</TableCell>
                    <TableCell>値</TableCell>
                    <TableCell>単位</TableCell>
                    <TableCell>タイムスタンプ</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {sensors.map((s) => (
                    <TableRow key={s.sensor_id} hover>
                      <TableCell>{s.sensor_id}</TableCell>
                      <TableCell>{s.value}</TableCell>
                      <TableCell>{s.unit}</TableCell>
                      <TableCell>{s.timestamp ? new Date(s.timestamp).toLocaleString('ja-JP') : '-'}</TableCell>
                    </TableRow>
                  ))}
                  {sensors.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {tabValue === 2 && (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>種別</TableCell>
                    <TableCell>設備</TableCell>
                    <TableCell>重大度</TableCell>
                    <TableCell>検知日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {anomalies.map((a) => (
                    <TableRow key={a.id} hover>
                      <TableCell>{a.type}</TableCell>
                      <TableCell>{a.equipment}</TableCell>
                      <TableCell><Chip label={a.severity} color={getSeverityColor(a.severity) as any} size="small" /></TableCell>
                      <TableCell>{a.detected_at ? new Date(a.detected_at).toLocaleString('ja-JP') : '-'}</TableCell>
                    </TableRow>
                  ))}
                  {anomalies.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </>
      )}
    </Box>
  );
};
