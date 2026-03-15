/**
 * サイバー対策ページ（レベル4）
 * IDS/IPS, EDR, SIEM, 脅威インテリジェンス, コンプライアンス
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Chip,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Stack,
  Grid,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  MenuItem,
} from '@mui/material';
import { EmptyState } from '../common/EmptyState';
import {
  Security,
  Warning,
  Assessment,
  Search,
  Shield,
  Description,
} from '@mui/icons-material';
import { cyberDefenseApi, SuricataAlert, WazuhAlert, ThreatIntelResult } from '../../api/cyberDefense';

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

export const CyberDefensePage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [overview, setOverview] = useState<any>(null);
  const [suricataAlerts, setSuricataAlerts] = useState<SuricataAlert[]>([]);
  const [wazuhAlerts, setWazuhAlerts] = useState<WazuhAlert[]>([]);
  const [complianceReport, setComplianceReport] = useState<any>(null);
  const [threatIntelResult, setThreatIntelResult] = useState<ThreatIntelResult | null>(null);
  const [iocType, setIocType] = useState('ip');
  const [iocValue, setIocValue] = useState('');
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
        const data = await cyberDefenseApi.getOverview();
        setOverview(data);
      } else if (tabValue === 1) {
        const data = await cyberDefenseApi.getSuricataAlerts();
        setSuricataAlerts(data);
      } else if (tabValue === 2) {
        const data = await cyberDefenseApi.getWazuhAlerts();
        setWazuhAlerts(data);
      } else if (tabValue === 3) {
        setThreatIntelResult(null);
      } else if (tabValue === 4) {
        const data = await cyberDefenseApi.getComplianceReport(30);
        setComplianceReport(data);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleThreatIntelCheck = async () => {
    if (!iocValue.trim()) return;
    try {
      setLoading(true);
      setError('');
      const result = await cyberDefenseApi.checkThreatIntel(iocType, iocValue.trim());
      setThreatIntelResult(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '照合に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (s: string) => {
    switch ((s || '').toLowerCase()) {
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
        サイバー対策（レベル4）
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        IDS/IPS (Suricata), EDR (Wazuh), SIEM, 脅威インテリジェンス (MISP), コンプライアンスレポート
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<Security />} label="概要" />
          <Tab icon={<Shield />} label="IDS/IPS (Suricata)" />
          <Tab icon={<Warning />} label="EDR (Wazuh)" />
          <Tab icon={<Search />} label="脅威インテリ" />
          <Tab icon={<Description />} label="コンプライアンス" />
        </Tabs>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {loading && tabValue !== 3 ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress aria-label="読み込み中" />
        </Box>
      ) : (
        <>
          <TabPanel value={tabValue} index={0}>
            {overview && (
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="text.secondary" gutterBottom>Suricata</Typography>
                      <Typography variant="h4">{overview.suricata?.alerts_count ?? 0}</Typography>
                      <Typography variant="caption">アラート</Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="text.secondary" gutterBottom>Wazuh</Typography>
                      <Typography variant="h4">{overview.wazuh?.alerts_count ?? 0}</Typography>
                      <Typography variant="caption">アラート</Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="text.secondary" gutterBottom>セキュリティイベント</Typography>
                      <Typography variant="h4">{overview.security_events?.total ?? 0}</Typography>
                      <Typography variant="caption">
                        Critical: {overview.security_events?.critical ?? 0} / High: {overview.security_events?.high ?? 0}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" gutterBottom>直近アラート (Suricata)</Typography>
                  <Stack spacing={1}>
                    {(overview.suricata?.recent ?? []).map((a: any) => (
                      <Card key={a.id} variant="outlined" sx={{ py: 1, px: 2 }}>
                        <Stack direction="row" spacing={2} alignItems="center" flexWrap="wrap">
                          <Chip label={a.severity} color={getSeverityColor(a.severity) as any} size="small" />
                          <Typography variant="body2">{a.rule_msg}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {a.src_ip} → {a.dest_ip}
                          </Typography>
                        </Stack>
                      </Card>
                    ))}
                    {(!overview.suricata?.recent || overview.suricata.recent.length === 0) && (
                      <Typography variant="body2" color="text.secondary">直近のアラートはありません</Typography>
                    )}
                  </Stack>
                </Grid>
              </Grid>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>時刻</TableCell>
                    <TableCell>重大度</TableCell>
                    <TableCell>ルール</TableCell>
                    <TableCell>送信元</TableCell>
                    <TableCell>送信先</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {suricataAlerts.map((a) => (
                    <TableRow key={a.id}>
                      <TableCell>{new Date(a.timestamp).toLocaleString('ja-JP')}</TableCell>
                      <TableCell><Chip label={a.severity} color={getSeverityColor(a.severity) as any} size="small" /></TableCell>
                      <TableCell>{a.rule_msg}</TableCell>
                      <TableCell>{a.src_ip}</TableCell>
                      <TableCell>{a.dest_ip}</TableCell>
                    </TableRow>
                  ))}
                  {suricataAlerts.length === 0 && (
                    <TableRow><TableCell colSpan={5} sx={{ border: 'none', py: 4 }}><EmptyState message="Suricataアラートがありません" subMessage="アラートが検知されるとここに表示されます" /></TableCell></TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>時刻</TableCell>
                    <TableCell>レベル</TableCell>
                    <TableCell>ルール</TableCell>
                    <TableCell>エージェント</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {wazuhAlerts.map((a) => (
                    <TableRow key={a.id}>
                      <TableCell>{new Date(a.timestamp).toLocaleString('ja-JP')}</TableCell>
                      <TableCell><Chip label={a.rule_level} color={a.rule_level >= 10 ? 'error' : 'warning'} size="small" /></TableCell>
                      <TableCell>{a.rule_description}</TableCell>
                      <TableCell>{a.agent_name || a.agent_id || '-'}</TableCell>
                    </TableRow>
                  ))}
                  {wazuhAlerts.length === 0 && (
                    <TableRow><TableCell colSpan={4} sx={{ border: 'none', py: 4 }}><EmptyState message="Wazuhアラートがありません" subMessage="アラートが検知されるとここに表示されます" /></TableCell></TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Stack spacing={2} sx={{ maxWidth: 480 }}>
              <Typography variant="subtitle2">IOC 照合（IP / ドメイン / ハッシュ）</Typography>
              <Stack direction="row" spacing={1} alignItems="center">
                <TextField
                  select
                  size="small"
                  value={iocType}
                  onChange={(e) => setIocType(e.target.value)}
                  sx={{ minWidth: 120 }}
                >
                  <MenuItem value="ip">IP</MenuItem>
                  <MenuItem value="domain">ドメイン</MenuItem>
                  <MenuItem value="hash">ハッシュ</MenuItem>
                </TextField>
                <TextField
                  size="small"
                  placeholder={iocType === 'ip' ? '192.168.1.1' : iocType === 'domain' ? 'example.com' : 'sha256...'}
                  value={iocValue}
                  onChange={(e) => setIocValue(e.target.value)}
                  fullWidth
                />
                <Button variant="contained" onClick={handleThreatIntelCheck} disabled={!iocValue.trim() || loading} aria-label="IOC照合を実行">
                  照合
                </Button>
              </Stack>
              {threatIntelResult && (
                <Card variant="outlined">
                  <CardContent>
                    <Stack spacing={1}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography fontWeight={600}>結果</Typography>
                        <Chip
                          label={threatIntelResult.is_malicious ? '悪意あり' : '悪意なし'}
                          color={threatIntelResult.is_malicious ? 'error' : 'success'}
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2">信頼度: {(threatIntelResult.confidence * 100).toFixed(0)}%</Typography>
                      <Typography variant="caption">ソース: {threatIntelResult.sources.join(', ')}</Typography>
                    </Stack>
                  </CardContent>
                </Card>
              )}
            </Stack>
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            {complianceReport && (
              <Stack spacing={2}>
                <Typography variant="subtitle2">レポート期間: {new Date(complianceReport.period_start).toLocaleDateString('ja-JP')} 〜 {new Date(complianceReport.period_end).toLocaleDateString('ja-JP')}</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="text.secondary" gutterBottom>サマリ</Typography>
                        <Typography variant="body2">総イベント: {complianceReport.summary?.total_events ?? 0}</Typography>
                        <Typography variant="body2">Critical: {complianceReport.summary?.critical_count ?? 0}</Typography>
                        <Typography variant="body2">High: {complianceReport.summary?.high_count ?? 0}</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="text.secondary" gutterBottom>推奨事項</Typography>
                        <Stack spacing={0.5}>
                          {(complianceReport.recommendations ?? []).map((r: string, i: number) => (
                            <Typography key={i} variant="body2">• {r}</Typography>
                          ))}
                        </Stack>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Stack>
            )}
          </TabPanel>
        </>
      )}
    </Box>
  );
};
