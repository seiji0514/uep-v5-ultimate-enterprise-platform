/**
 * セキュリティコマンドセンターページ
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Security,
  Warning,
  Assessment,
} from '@mui/icons-material';
import { securityCenterApi, SecurityEvent, Incident, Risk } from '../../api/securityCenter';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export const SecurityCenterPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [risks, setRisks] = useState<Risk[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) {
        const data = await securityCenterApi.getEvents();
        setEvents(data);
      } else if (tabValue === 1) {
        const data = await securityCenterApi.getIncidents();
        setIncidents(data);
      } else if (tabValue === 2) {
        const data = await securityCenterApi.getRisks();
        setRisks(data);
      }
    } catch (err: any) {
      console.error('Security Center API Error:', err);
      if (err.code === 'ECONNREFUSED' || err.message?.includes('Network Error')) {
        setError('バックエンドサーバーに接続できません。バックエンドが起動しているか確認してください。');
      } else if (err.response?.status === 404) {
        setError('APIエンドポイントが見つかりません。');
      } else if (err.response?.status === 403) {
        setError('アクセス権限がありません。');
      } else if (err.response?.status === 422) {
        // バリデーションエラーの詳細を表示
        const errorData = err.response?.data;
        if (errorData?.error?.errors && Array.isArray(errorData.error.errors)) {
          const validationErrors = errorData.error.errors
            .map((e: any) => `${e.field}: ${e.message}`)
            .join(', ');
          setError(`バリデーションエラー: ${validationErrors}`);
        } else {
          setError(errorData?.error?.message || errorData?.detail || 'バリデーションエラーが発生しました');
        }
      } else if (err.response?.status === 500) {
        setError('サーバーエラーが発生しました。');
      } else {
        setError(err.response?.data?.error?.message || err.response?.data?.detail || err.message || 'データの取得に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const getThreatLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical':
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'default';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        セキュリティコマンドセンター
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        セキュリティ監視、インシデント対応、リスク分析
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab icon={<Security />} label="セキュリティイベント" />
          <Tab icon={<Warning />} label="インシデント" />
          <Tab icon={<Assessment />} label="リスク分析" />
        </Tabs>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
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
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>イベントタイプ</TableCell>
                    <TableCell>脅威レベル</TableCell>
                    <TableCell>送信元</TableCell>
                    <TableCell>送信先</TableCell>
                    <TableCell>説明</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>発生日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {events.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={7} align="center">
                        セキュリティイベントがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    events.map((event) => (
                      <TableRow key={event.id}>
                        <TableCell>{event.event_type}</TableCell>
                        <TableCell>
                          <Chip
                            label={event.threat_level}
                            color={getThreatLevelColor(event.threat_level) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{event.source}</TableCell>
                        <TableCell>{event.target}</TableCell>
                        <TableCell>{event.description}</TableCell>
                        <TableCell>{event.status}</TableCell>
                        <TableCell>
                          {new Date(event.created_at).toLocaleString('ja-JP')}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>タイトル</TableCell>
                    <TableCell>説明</TableCell>
                    <TableCell>深刻度</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>作成日時</TableCell>
                    <TableCell>更新日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {incidents.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        インシデントがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    incidents.map((incident) => (
                      <TableRow key={incident.id}>
                        <TableCell>{incident.title}</TableCell>
                        <TableCell>{incident.description}</TableCell>
                        <TableCell>
                          <Chip
                            label={incident.severity}
                            color={getSeverityColor(incident.severity) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{incident.status}</TableCell>
                        <TableCell>
                          {new Date(incident.created_at).toLocaleString('ja-JP')}
                        </TableCell>
                        <TableCell>
                          {incident.updated_at
                            ? new Date(incident.updated_at).toLocaleString('ja-JP')
                            : '-'}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>タイトル</TableCell>
                    <TableCell>説明</TableCell>
                    <TableCell>リスクレベル</TableCell>
                    <TableCell>作成日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {risks.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4} align="center">
                        リスクがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    risks.map((risk) => (
                      <TableRow key={risk.id}>
                        <TableCell>{risk.title}</TableCell>
                        <TableCell>{risk.description}</TableCell>
                        <TableCell>
                          <Chip
                            label={risk.level}
                            color={getSeverityColor(risk.level) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(risk.created_at).toLocaleString('ja-JP')}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>
        </>
      )}
    </Box>
  );
};
