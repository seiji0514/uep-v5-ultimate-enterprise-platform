/**
 * 医療 ページ
 * AI診断、音声応答、異常検知、医療プラットフォーム。MLOps、医療プラットフォームとの相性が良い。
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
  LocalHospital,
  RecordVoiceOver,
  Warning,
  MedicalServices,
} from '@mui/icons-material';
import {
  medicalApi,
  AIDiagnosis,
  VoiceResponse,
  MedicalAnomaly,
  PlatformStats,
} from '../../api/medical';
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
      {value === index && <Box sx={{ p: 1.5 }}>{children}</Box>}
    </div>
  );
}

export const MedicalPage: React.FC = () => {
  useAutoPlayNarration(4);
  const [tabValue, setTabValue] = useState(0);
  const [aiDiagnosis, setAIDiagnosis] = useState<AIDiagnosis[]>([]);
  const [voiceResponse, setVoiceResponse] = useState<VoiceResponse[]>([]);
  const [anomalies, setAnomalies] = useState<MedicalAnomaly[]>([]);
  const [platformStats, setPlatformStats] = useState<PlatformStats | null>(null);
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
        const data = await medicalApi.getAIDiagnosis();
        setAIDiagnosis(data);
      } else if (tabValue === 1) {
        const data = await medicalApi.getVoiceResponse();
        setVoiceResponse(data);
      } else if (tabValue === 2) {
        const data = await medicalApi.getAnomalyDetection();
        setAnomalies(data);
      } else if (tabValue === 3) {
        const data = await medicalApi.getPlatformStats();
        setPlatformStats(data);
      }
    } catch (err: any) {
      console.error('Medical API Error:', err);
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

  const getSeverityColor = (severity: string) => {
    if (severity === '高') return 'error';
    if (severity === '中') return 'warning';
    return 'success';
  };

  return (
    <Box sx={{ p: 0, transform: 'scale(0.94)', transformOrigin: 'top left' }}>
      <Box sx={{ mb: 2 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          医療
        </Typography>
        <Typography variant="body2" color="text.secondary">
          AI診断、音声応答、異常検知、医療プラットフォーム。MLOps、医療プラットフォームとの相性が良い。
        </Typography>
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
          公開データ: MIMIC-III、PhysioNet など匿名化医療データでPoC検証可能。デモはサンプル、顧客環境では実データに置換。
        </Typography>
      </Box>

      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<LocalHospital />} iconPosition="start" label="AI診断" />
          <Tab icon={<RecordVoiceOver />} iconPosition="start" label="音声応答" />
          <Tab icon={<Warning />} iconPosition="start" label="異常検知" />
          <Tab icon={<MedicalServices />} iconPosition="start" label="医療プラットフォーム" />
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
              <Box sx={{ mb: 1.5 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>AI診断 ステータス構成</Typography>
                <ResponsiveContainer width="100%" height={160}>
                  <PieChart margin={{ top: 20, right: 40, bottom: 20, left: 40 }}>
                    <Pie
                      data={(() => {
                        const m: Record<string, number> = {};
                        aiDiagnosis.forEach((d) => { m[d.status] = (m[d.status] || 0) + 1; });
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
                        aiDiagnosis.forEach((d) => { m[d.status] = (m[d.status] || 0) + 1; });
                        return Object.entries(m).map((_, i) => (
                          <Cell key={i} fill={['#E02F44', '#5794F2', '#73BF69'][i % 3]} />
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
                      <TableCell>患者ID</TableCell>
                      <TableCell>所見</TableCell>
                      <TableCell>信頼度</TableCell>
                      <TableCell>ステータス</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {aiDiagnosis.map((d) => (
                      <TableRow key={d.id}>
                        <TableCell>{d.patient_id}</TableCell>
                        <TableCell>{d.finding}</TableCell>
                        <TableCell>{(d.confidence * 100).toFixed(0)}%</TableCell>
                        <TableCell><Chip size="small" label={d.status} /></TableCell>
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
                      <TableCell>種別</TableCell>
                      <TableCell>長さ(秒)</TableCell>
                      <TableCell>転写</TableCell>
                      <TableCell>ステータス</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {voiceResponse.map((v) => (
                      <TableRow key={v.id}>
                        <TableCell>{v.type}</TableCell>
                        <TableCell>{v.duration_sec}</TableCell>
                        <TableCell>{v.transcription}</TableCell>
                        <TableCell><Chip size="small" label={v.status} /></TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <Box sx={{ mb: 1.5 }}>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>異常検知 深刻度構成</Typography>
                <ResponsiveContainer width="100%" height={160}>
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
              </Box>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>種別</TableCell>
                      <TableCell>患者ID</TableCell>
                      <TableCell>指標</TableCell>
                      <TableCell>値/閾値</TableCell>
                      <TableCell>深刻度</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {anomalies.map((a) => (
                      <TableRow key={a.id}>
                        <TableCell>{a.type}</TableCell>
                        <TableCell>{a.patient_id}</TableCell>
                        <TableCell>{a.metric}</TableCell>
                        <TableCell>{a.value} / {a.threshold}</TableCell>
                        <TableCell>
                          <Chip size="small" label={a.severity} color={getSeverityColor(a.severity)} />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={3}>
              {platformStats && (
                <>
                <Box sx={{ mb: 1.5 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>本日の統計</Typography>
                  <ResponsiveContainer width="100%" height={140}>
                    <BarChart data={[
                      { name: 'AI診断', 件数: platformStats.ai_diagnosis_today },
                      { name: '音声処理', 件数: platformStats.voice_processed_today },
                      { name: '異常検知', 件数: platformStats.anomalies_detected_today },
                    ]}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                      <YAxis tick={{ fontSize: 11 }} />
                      <Tooltip />
                      <Bar dataKey="件数" fill="#5794F2" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
                <Grid container spacing={1.5}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">アクティブ患者数</Typography>
                      <Typography variant="h6">{platformStats.active_patients}</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">本日のAI診断</Typography>
                      <Typography variant="h6">{platformStats.ai_diagnosis_today}</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">本日の音声処理</Typography>
                      <Typography variant="h6">{platformStats.voice_processed_today}</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                      <Typography variant="overline" color="text.secondary">本日の異常検知</Typography>
                      <Typography variant="h6">{platformStats.anomalies_detected_today}</Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="caption" color="text.secondary">
                      最終更新: {new Date(platformStats.last_updated).toLocaleString()}
                    </Typography>
                  </Grid>
                </Grid>
                </>
              )}
            </TabPanel>
          </>
        )}
      </Paper>

      <Paper sx={{ p: 1.5, mt: 1.5 }} elevation={0}>
        <Typography variant="overline" color="text.secondary">技術スタック</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
          <Chip size="small" label="MLOps" />
          <Chip size="small" label="音声認識" />
          <Chip size="small" label="異常検知" />
          <Chip size="small" label="医療プラットフォーム" />
        </Box>
      </Paper>
    </Box>
  );
};
