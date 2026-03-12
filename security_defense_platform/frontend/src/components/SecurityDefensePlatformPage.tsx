/**
 * 統合セキュリティ・防衛プラットフォーム
 * 充実版: ダッシュボード・フィルタ・詳細表示・SIEM検索
 */
import React, { useState, useEffect, useCallback } from 'react';
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
  FormControl,
  InputLabel,
  Select,
  Divider,
  LinearProgress,
  Tooltip,
} from '@mui/material';
import {
  Security,
  Warning,
  Assessment,
  Search,
  Shield,
  Description,
  Timeline,
  FilterList,
  Refresh,
  Info,
  Storage,
  Gavel,
} from '@mui/icons-material';
import {
  securityCenterApi,
  cyberDefenseApi,
  type SecurityEvent,
  type Incident,
  type Risk,
  type SuricataAlert,
  type WazuhAlert,
  type ThreatIntelResult,
} from '../api';

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

const CATEGORY_LABELS: Record<string, string> = {
  technical: '技術',
  operational: '運用',
  compliance: 'コンプライアンス',
  security: 'セキュリティ',
};

export const SecurityDefensePlatformPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [risks, setRisks] = useState<Risk[]>([]);
  const [overview, setOverview] = useState<any>(null);
  const [posture, setPosture] = useState<any>(null);
  const [suricataAlerts, setSuricataAlerts] = useState<SuricataAlert[]>([]);
  const [wazuhAlerts, setWazuhAlerts] = useState<WazuhAlert[]>([]);
  const [complianceReport, setComplianceReport] = useState<any>(null);
  const [threatIntelResult, setThreatIntelResult] = useState<ThreatIntelResult | null>(null);
  const [siemResults, setSiemResults] = useState<any[]>([]);
  const [siemQuery, setSiemQuery] = useState('');
  const [iocType, setIocType] = useState('ip');
  const [iocValue, setIocValue] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [eventFilter, setEventFilter] = useState<{ threat_level?: string }>({});
  const [incidentFilter, setIncidentFilter] = useState<{ severity?: string; status?: string }>({});

  const loadData = useCallback(async (siemQueryOverride?: string) => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) {
        setEvents(await securityCenterApi.getEvents(eventFilter));
      } else if (tabValue === 1) {
        setIncidents(await securityCenterApi.getIncidents(incidentFilter));
      } else if (tabValue === 2) {
        setRisks(await securityCenterApi.getRisks());
      } else if (tabValue === 3) {
        const [ov, pos] = await Promise.all([
          cyberDefenseApi.getOverview(),
          securityCenterApi.getSecurityPosture().catch(() => null),
        ]);
        setOverview(ov);
        setPosture(pos);
      } else if (tabValue === 4) {
        setSuricataAlerts(await cyberDefenseApi.getSuricataAlerts());
      } else if (tabValue === 5) {
        setWazuhAlerts(await cyberDefenseApi.getWazuhAlerts());
      } else if (tabValue === 6) {
        setThreatIntelResult(null);
      } else if (tabValue === 7) {
        setComplianceReport(await cyberDefenseApi.getComplianceReport(30));
      } else if (tabValue === 8) {
        const q = siemQueryOverride !== undefined ? siemQueryOverride : siemQuery;
        const res = await cyberDefenseApi.siemSearch(q || undefined, undefined, 50);
        setSiemResults(res?.results ?? []);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  }, [tabValue, eventFilter, incidentFilter, siemQuery]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // ダッシュボードKPI用に概要を先行取得（マウント時）
  useEffect(() => {
    Promise.all([
      securityCenterApi.getEvents().then(setEvents).catch(() => {}),
      securityCenterApi.getIncidents().then(setIncidents).catch(() => {}),
      securityCenterApi.getRisks().then(setRisks).catch(() => {}),
      cyberDefenseApi.getOverview().then((ov) => ov && setOverview(ov)).catch(() => {}),
    ]);
  }, []);

  const handleThreatIntelCheck = async () => {
    if (!iocValue.trim()) return;
    try {
      setLoading(true);
      setError('');
      setThreatIntelResult(await cyberDefenseApi.checkThreatIntel(iocType, iocValue.trim()));
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '照合に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleSiemSearch = () => {
    loadData(siemQuery);
  };

  const getThreatLevelColor = (level: string) =>
    ['critical', 'high'].includes((level || '').toLowerCase()) ? 'error' : (level || '').toLowerCase() === 'medium' ? 'warning' : 'info';
  const getSeverityColor = (s: string) =>
    ['critical', 'high'].includes((s || '').toLowerCase()) ? 'error' : (s || '').toLowerCase() === 'medium' ? 'warning' : 'info';

  const criticalCount = events.filter((e) => (e.threat_level || '').toLowerCase() === 'critical').length;
  const highCount = events.filter((e) => (e.threat_level || '').toLowerCase() === 'high').length;

  const EmptyState = ({ message, hint }: { message: string; hint?: string }) => (
    <Paper sx={{ p: 4, textAlign: 'center' }}>
      <Typography color="text.secondary">{message}</Typography>
      {hint && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {hint}
        </Typography>
      )}
    </Paper>
  );

  return (
    <Box>
      {/* ダッシュボード概要（常時表示） */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">セキュリティイベント</Typography>
              <Typography variant="h4">{events.length}</Typography>
              <Box sx={{ mt: 1 }}>
                {criticalCount > 0 && <Chip label={`Critical ${criticalCount}`} color="error" size="small" sx={{ mr: 0.5 }} />}
                {highCount > 0 && <Chip label={`High ${highCount}`} color="warning" size="small" />}
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">インシデント</Typography>
              <Typography variant="h4">{incidents.length}</Typography>
              <Typography variant="caption" color="text.secondary">
                未対応: {incidents.filter((i) => (i.status || '').toLowerCase() !== 'resolved').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">登録リスク</Typography>
              <Typography variant="h4">{risks.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">IDS/IPS + EDR</Typography>
              <Typography variant="h4">{(overview?.suricata?.alerts_count ?? 0) + (overview?.wazuh?.alerts_count ?? 0)}</Typography>
              <Typography variant="caption" color="text.secondary">Suricata / Wazuh</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Typography variant="h5" component="h1" gutterBottom>
        セキュリティ監視・インシデント対応・リスク分析
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        IDS/IPS（Suricata）, EDR（Wazuh）, SIEM, 脅威インテリジェンス（MISP）, コンプライアンス, SOAR連携
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} variant="scrollable" scrollButtons="auto">
          <Tab icon={<Security />} label="イベント" />
          <Tab icon={<Warning />} label="インシデント" />
          <Tab icon={<Assessment />} label="リスク" />
          <Tab icon={<Shield />} label="サイバー概要" />
          <Tab icon={<Storage />} label="IDS/IPS" />
          <Tab icon={<Gavel />} label="EDR" />
          <Tab icon={<Search />} label="脅威インテリ" />
          <Tab icon={<Description />} label="コンプライアンス" />
          <Tab icon={<Timeline />} label="SIEM検索" />
        </Tabs>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}

      {loading && tabValue !== 6 ? (
        <Box sx={{ p: 4 }}><LinearProgress /></Box>
      ) : (
        <>
          <TabPanel value={tabValue} index={0}>
            <Stack direction="row" spacing={2} sx={{ mb: 2 }} alignItems="center">
              <FormControl size="small" sx={{ minWidth: 140 }}>
                <InputLabel>脅威レベル</InputLabel>
                <Select
                  value={eventFilter.threat_level || ''}
                  label="脅威レベル"
                  onChange={(e) => setEventFilter({ ...eventFilter, threat_level: e.target.value || undefined })}
                >
                  <MenuItem value="">すべて</MenuItem>
                  <MenuItem value="critical">Critical</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="low">Low</MenuItem>
                </Select>
              </FormControl>
              <Button size="small" startIcon={<Refresh />} onClick={() => loadData()}>更新</Button>
            </Stack>
            <Stack spacing={2}>
              {events.length === 0 ? (
                <EmptyState message="セキュリティイベントがありません" hint="Falco Webhook や IDS/EDR からイベントが取り込まれると表示されます" />
              ) : (
                events.map((e) => (
                  <Card key={e.id} variant="outlined">
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap', mb: 1 }}>
                        <Typography variant="subtitle1" fontWeight={600}>{e.event_type}</Typography>
                        <Chip label={e.threat_level} color={getThreatLevelColor(e.threat_level) as any} size="small" />
                        {e.status && <Chip label={e.status} size="small" variant="outlined" />}
                      </Box>
                      <Typography variant="body2" color="text.secondary" paragraph>{e.description}</Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={4}><Typography variant="caption">送信元:</Typography> <Typography variant="body2" component="span">{e.source}</Typography></Grid>
                        <Grid item xs={12} sm={4}><Typography variant="caption">送信先:</Typography> <Typography variant="body2" component="span">{e.target}</Typography></Grid>
                        <Grid item xs={12} sm={4}><Typography variant="caption">発生日時:</Typography> <Typography variant="body2" component="span">{e.created_at ? new Date(e.created_at).toLocaleString('ja-JP') : '-'}</Typography></Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                ))
              )}
            </Stack>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Stack direction="row" spacing={2} sx={{ mb: 2 }} alignItems="center">
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>重大度</InputLabel>
                <Select value={incidentFilter.severity || ''} label="重大度" onChange={(e) => setIncidentFilter({ ...incidentFilter, severity: e.target.value || undefined })}>
                  <MenuItem value="">すべて</MenuItem>
                  <MenuItem value="critical">Critical</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="low">Low</MenuItem>
                </Select>
              </FormControl>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>ステータス</InputLabel>
                <Select value={incidentFilter.status || ''} label="ステータス" onChange={(e) => setIncidentFilter({ ...incidentFilter, status: e.target.value || undefined })}>
                  <MenuItem value="">すべて</MenuItem>
                  <MenuItem value="open">Open</MenuItem>
                  <MenuItem value="investigating">Investigating</MenuItem>
                  <MenuItem value="resolved">Resolved</MenuItem>
                </Select>
              </FormControl>
              <Button size="small" startIcon={<Refresh />} onClick={() => loadData()}>更新</Button>
            </Stack>
            <Stack spacing={2}>
              {incidents.length === 0 ? (
                <EmptyState message="インシデントがありません" />
              ) : (
                incidents.map((i) => (
                  <Card key={i.id} variant="outlined">
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap', mb: 1 }}>
                        <Typography variant="subtitle1" fontWeight={600}>{i.title}</Typography>
                        <Chip label={i.severity} color={getSeverityColor(i.severity) as any} size="small" />
                        <Chip label={i.status} size="small" variant="outlined" />
                      </Box>
                      <Typography variant="body2" color="text.secondary" paragraph>{i.description}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        作成: {i.created_at ? new Date(i.created_at).toLocaleString('ja-JP') : '-'}
                        {i.updated_at && ` ｜ 更新: ${new Date(i.updated_at).toLocaleString('ja-JP')}`}
                      </Typography>
                    </CardContent>
                  </Card>
                ))
              )}
            </Stack>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <Stack spacing={2}>
              {risks.length === 0 ? (
                <EmptyState message="登録リスクがありません" hint="リスク分析モジュールでリスクを登録できます" />
              ) : (
                risks.map((r) => (
                  <Card key={r.id} variant="outlined">
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap', mb: 1 }}>
                        <Typography variant="subtitle1" fontWeight={600}>{(r as any).name ?? r.title ?? '-'}</Typography>
                        <Chip label={(r as any).risk_level ?? r.level ?? '-'} color={getSeverityColor((r as any).risk_level ?? r.level ?? '') as any} size="small" />
                        {(r as any).category && <Chip label={CATEGORY_LABELS[(r as any).category] ?? (r as any).category} size="small" variant="outlined" />}
                      </Box>
                      <Typography variant="body2" color="text.secondary" paragraph>{r.description}</Typography>
                      {(r as any).likelihood !== undefined && (
                        <Box sx={{ mb: 1 }}>
                          <Typography variant="caption">発生確率: {((r as any).likelihood * 100).toFixed(0)}% ｜ 影響度: {((r as any).impact * 100).toFixed(0)}%</Typography>
                        </Box>
                      )}
                      {(r as any).mitigation && (
                        <Paper variant="outlined" sx={{ p: 1.5, mt: 1, bgcolor: 'action.hover' }}>
                          <Typography variant="caption" color="text.secondary">対策:</Typography>
                          <Typography variant="body2">{(r as any).mitigation}</Typography>
                        </Paper>
                      )}
                    </CardContent>
                  </Card>
                ))
              )}
            </Stack>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            {overview && (
              <Stack spacing={3}>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="text.secondary">Suricata（IDS/IPS）</Typography>
                        <Typography variant="h4">{overview.suricata?.alerts_count ?? 0}</Typography>
                        <Typography variant="caption">アラート数</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="text.secondary">Wazuh（EDR）</Typography>
                        <Typography variant="h4">{overview.wazuh?.alerts_count ?? 0}</Typography>
                        <Typography variant="caption">アラート数</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="text.secondary">セキュリティイベント</Typography>
                        <Typography variant="h4">{overview.security_events?.total ?? 0}</Typography>
                        <Typography variant="caption">Critical: {overview.security_events?.critical ?? 0} / High: {overview.security_events?.high ?? 0}</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
                {posture && (
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle1" fontWeight={600} gutterBottom>セキュリティ態勢</Typography>
                      <Typography variant="body2" color="text.secondary">{JSON.stringify(posture, null, 2)}</Typography>
                    </CardContent>
                  </Card>
                )}
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>連携ステータス</Typography>
                    <Stack direction="row" spacing={2}>
                      <Chip icon={<Shield />} label="脅威インテリジェンス" color={overview.threat_intel?.status === 'available' ? 'success' : 'default'} size="small" />
                      <Chip icon={<Description />} label="コンプライアンス" color={overview.compliance?.status === 'available' ? 'success' : 'default'} size="small" />
                    </Stack>
                  </CardContent>
                </Card>
              </Stack>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 2 }}>
              Suricata IDS/IPS アラート（ネットワーク侵入検知・防止）
            </Typography>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>時刻</TableCell>
                    <TableCell>重大度</TableCell>
                    <TableCell>ルールID</TableCell>
                    <TableCell>ルール</TableCell>
                    <TableCell>送信元</TableCell>
                    <TableCell>送信先</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {suricataAlerts.map((a) => (
                    <TableRow key={a.id} hover>
                      <TableCell>{new Date(a.timestamp).toLocaleString('ja-JP')}</TableCell>
                      <TableCell><Chip label={a.severity} color={getSeverityColor(a.severity) as any} size="small" /></TableCell>
                      <TableCell>{a.rule_id || '-'}</TableCell>
                      <TableCell><Tooltip title={a.rule_msg}><Typography variant="body2" sx={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>{a.rule_msg}</Typography></Tooltip></TableCell>
                      <TableCell>{a.src_ip}</TableCell>
                      <TableCell>{a.dest_ip}</TableCell>
                    </TableRow>
                  ))}
                  {suricataAlerts.length === 0 && <TableRow><TableCell colSpan={6} align="center">アラートがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={5}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 2 }}>
              Wazuh EDR アラート（エンドポイント検知・対応）
            </Typography>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>時刻</TableCell>
                    <TableCell>レベル</TableCell>
                    <TableCell>ルールID</TableCell>
                    <TableCell>ルール</TableCell>
                    <TableCell>エージェント</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {wazuhAlerts.map((a) => (
                    <TableRow key={a.id} hover>
                      <TableCell>{new Date(a.timestamp).toLocaleString('ja-JP')}</TableCell>
                      <TableCell><Chip label={a.rule_level} color={a.rule_level >= 10 ? 'error' : 'warning'} size="small" /></TableCell>
                      <TableCell>{a.rule_id}</TableCell>
                      <TableCell>{a.rule_description}</TableCell>
                      <TableCell>{a.agent_name || a.agent_id || '-'}</TableCell>
                    </TableRow>
                  ))}
                  {wazuhAlerts.length === 0 && <TableRow><TableCell colSpan={5} align="center">アラートがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={6}>
            <Stack spacing={2} sx={{ maxWidth: 560 }}>
              <Typography variant="subtitle1" fontWeight={600}>IOC 照合（脅威インテリジェンス）</Typography>
              <Typography variant="body2" color="text.secondary">
                IPアドレス・ドメイン・ファイルハッシュを照合し、既知の脅威か判定します。MISP 等と連携可能。
              </Typography>
              <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap">
                <TextField select size="small" value={iocType} onChange={(e) => setIocType(e.target.value)} sx={{ minWidth: 120 }}>
                  <MenuItem value="ip">IP</MenuItem>
                  <MenuItem value="domain">ドメイン</MenuItem>
                  <MenuItem value="hash">ハッシュ</MenuItem>
                </TextField>
                <TextField size="small" placeholder={iocType === 'ip' ? '192.168.1.1' : iocType === 'domain' ? 'example.com' : 'sha256...'} value={iocValue} onChange={(e) => setIocValue(e.target.value)} sx={{ flex: 1, minWidth: 200 }} />
                <Button variant="contained" onClick={handleThreatIntelCheck} disabled={!iocValue.trim() || loading}>照合</Button>
              </Stack>
              <Typography variant="caption" color="text.secondary">デモ: 192.168.1.100, 10.0.0.99, malware.example.com は悪意ありと判定</Typography>
              {threatIntelResult && (
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      <Typography fontWeight={600}>照合結果</Typography>
                      <Chip label={threatIntelResult.is_malicious ? '悪意あり' : '悪意なし'} color={threatIntelResult.is_malicious ? 'error' : 'success'} size="small" />
                    </Box>
                    <Typography variant="body2">IOC: {threatIntelResult.ioc_type} = {threatIntelResult.ioc_value}</Typography>
                    <Typography variant="body2">信頼度: {(threatIntelResult.confidence * 100).toFixed(0)}%</Typography>
                    {threatIntelResult.sources?.length > 0 && (
                      <Typography variant="caption" color="text.secondary">ソース: {threatIntelResult.sources.join(', ')}</Typography>
                    )}
                  </CardContent>
                </Card>
              )}
            </Stack>
          </TabPanel>

          <TabPanel value={tabValue} index={7}>
            {complianceReport && (
              <Stack spacing={3}>
                <Typography variant="subtitle2">レポート期間: {new Date(complianceReport.period_start).toLocaleDateString('ja-JP')} 〜 {new Date(complianceReport.period_end).toLocaleDateString('ja-JP')}</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="text.secondary">総イベント数</Typography>
                        <Typography variant="h4">{complianceReport.summary?.total_events ?? 0}</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="text.secondary">Critical</Typography>
                        <Typography variant="h4" color="error">{complianceReport.summary?.critical_count ?? complianceReport.security_events_summary?.critical ?? 0}</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="text.secondary">High</Typography>
                        <Typography variant="h4" color="warning.main">{complianceReport.summary?.high_count ?? complianceReport.security_events_summary?.high ?? 0}</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>推奨事項</Typography>
                    <Stack spacing={0.5}>
                      {(complianceReport.recommendations ?? []).map((r: string, i: number) => (
                        <Box key={i} sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                          <Info fontSize="small" color="action" sx={{ mt: 0.3 }} />
                          <Typography variant="body2">{r}</Typography>
                        </Box>
                      ))}
                    </Stack>
                  </CardContent>
                </Card>
              </Stack>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={8}>
            <Stack spacing={2} sx={{ mb: 2 }}>
              <Typography variant="subtitle2">SIEM ログ検索（OpenSearch/Elasticsearch 連携時は本番データを検索）</Typography>
              <Stack direction="row" spacing={1}>
                <TextField size="small" placeholder="キーワード検索（説明・送信元）" value={siemQuery} onChange={(e) => setSiemQuery(e.target.value)} sx={{ flex: 1 }} onKeyDown={(e) => e.key === 'Enter' && handleSiemSearch()} />
                <Button variant="contained" onClick={handleSiemSearch} disabled={loading}>検索</Button>
              </Stack>
            </Stack>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>時刻</TableCell>
                    <TableCell>種別</TableCell>
                    <TableCell>脅威レベル</TableCell>
                    <TableCell>送信元</TableCell>
                    <TableCell>送信先</TableCell>
                    <TableCell>説明</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {siemResults.map((r: any, i: number) => (
                    <TableRow key={r.id || i} hover>
                      <TableCell>{r.timestamp ? new Date(r.timestamp).toLocaleString('ja-JP') : '-'}</TableCell>
                      <TableCell>{r.event_type}</TableCell>
                      <TableCell><Chip label={r.threat_level} color={getThreatLevelColor(r.threat_level) as any} size="small" /></TableCell>
                      <TableCell>{r.source}</TableCell>
                      <TableCell>{r.target}</TableCell>
                      <TableCell><Typography variant="body2" sx={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis' }}>{r.description}</Typography></TableCell>
                    </TableRow>
                  ))}
                  {siemResults.length === 0 && !loading && <TableRow><TableCell colSpan={6} align="center">検索キーワードを入力して検索してください</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>
        </>
      )}
    </Box>
  );
};
