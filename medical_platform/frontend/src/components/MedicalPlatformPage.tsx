/**
 * 医療・ヘルスケアプラットフォーム
 * AI診断・音声応答・異常検知・プラットフォーム統計
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
  LocalHospital,
  Psychology,
  RecordVoiceOver,
  Warning,
  Refresh,
} from '@mui/icons-material';
import {
  medicalApi,
  type AIDiagnosis,
  type VoiceResponse,
  type MedicalAnomaly,
  type PlatformStats,
} from '../api';

export const MedicalPlatformPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [aiDiagnosis, setAiDiagnosis] = useState<AIDiagnosis[]>([]);
  const [voiceResponse, setVoiceResponse] = useState<VoiceResponse[]>([]);
  const [anomalies, setAnomalies] = useState<MedicalAnomaly[]>([]);
  const [stats, setStats] = useState<PlatformStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [diag, voice, anom, st] = await Promise.all([
        medicalApi.getAIDiagnosis(),
        medicalApi.getVoiceResponse(),
        medicalApi.getAnomalyDetection(),
        medicalApi.getPlatformStats(),
      ]);
      setAiDiagnosis(diag.items || []);
      setVoiceResponse(voice.items || []);
      setAnomalies(anom.items || []);
      setStats(st);
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
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">アクティブ患者</Typography>
              <Typography variant="h4">{stats?.active_patients ?? '-'}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">AI診断（本日）</Typography>
              <Typography variant="h4">{stats?.ai_diagnosis_today ?? '-'}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">音声処理（本日）</Typography>
              <Typography variant="h4">{stats?.voice_processed_today ?? '-'}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">異常検知（本日）</Typography>
              <Typography variant="h4">{stats?.anomalies_detected_today ?? '-'}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Typography variant="h5" component="h1" gutterBottom>
        医療・ヘルスケアプラットフォーム
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        AI診断・音声応答（問診・ナースコール）・異常検知・FHIR連携
      </Typography>

      <Stack direction="row" spacing={1} sx={{ mb: 2 }} flexWrap="wrap">
        <Chip
          icon={<Psychology />}
          label="AI診断"
          onClick={() => setTabValue(0)}
          color={tabValue === 0 ? 'primary' : 'default'}
          variant={tabValue === 0 ? 'filled' : 'outlined'}
        />
        <Chip
          icon={<RecordVoiceOver />}
          label="音声応答"
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
                    <TableCell>患者ID</TableCell>
                    <TableCell>所見</TableCell>
                    <TableCell>信頼度</TableCell>
                    <TableCell>ステータス</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {aiDiagnosis.map((d) => (
                    <TableRow key={d.id} hover>
                      <TableCell>{d.patient_id}</TableCell>
                      <TableCell>{d.finding}</TableCell>
                      <TableCell>{(d.confidence * 100).toFixed(0)}%</TableCell>
                      <TableCell><Chip label={d.status} size="small" color={d.status === '要確認' ? 'warning' : 'default'} /></TableCell>
                    </TableRow>
                  ))}
                  {aiDiagnosis.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {tabValue === 1 && (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>種別</TableCell>
                    <TableCell>時間(秒)</TableCell>
                    <TableCell>文字起こし</TableCell>
                    <TableCell>ステータス</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {voiceResponse.map((v) => (
                    <TableRow key={v.id} hover>
                      <TableCell>{v.type}</TableCell>
                      <TableCell>{v.duration_sec}</TableCell>
                      <TableCell><Typography variant="body2" sx={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis' }}>{v.transcription}</Typography></TableCell>
                      <TableCell><Chip label={v.status} size="small" /></TableCell>
                    </TableRow>
                  ))}
                  {voiceResponse.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
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
                    <TableCell>患者ID</TableCell>
                    <TableCell>指標</TableCell>
                    <TableCell>値</TableCell>
                    <TableCell>閾値</TableCell>
                    <TableCell>重大度</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {anomalies.map((a) => (
                    <TableRow key={a.id} hover>
                      <TableCell>{a.type}</TableCell>
                      <TableCell>{a.patient_id}</TableCell>
                      <TableCell>{a.metric}</TableCell>
                      <TableCell>{a.value}</TableCell>
                      <TableCell>{a.threshold}</TableCell>
                      <TableCell><Chip label={a.severity} color={getSeverityColor(a.severity) as any} size="small" /></TableCell>
                    </TableRow>
                  ))}
                  {anomalies.length === 0 && <TableRow><TableCell colSpan={6} align="center">データがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </>
      )}
    </Box>
  );
};
