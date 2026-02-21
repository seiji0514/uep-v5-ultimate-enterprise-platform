/**
 * Level 5 グローバルエンタープライズページ
 * マルチリージョン、高可用性、ゼロダウンタイムデプロイ、コンプライアンス、DR
 * ※組織・運用（認証取得、大規模実運用）は除外
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Public,
  Security,
  Update,
  Backup,
  Gavel,
} from '@mui/icons-material';
import { globalEnterpriseApi, Level5Overview, Region, ComplianceItem } from '../../api/globalEnterprise';

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

export const GlobalEnterprisePage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [overview, setOverview] = useState<Level5Overview | null>(null);
  const [regions, setRegions] = useState<Region[]>([]);
  const [haConfig, setHaConfig] = useState<any>(null);
  const [deployConfig, setDeployConfig] = useState<any>(null);
  const [drConfig, setDrConfig] = useState<any>(null);
  const [compliance, setCompliance] = useState<Record<string, ComplianceItem[]>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [overviewRes, multiRegionRes, haRes, deployRes, drRes, complianceRes] = await Promise.all([
        globalEnterpriseApi.getOverview(),
        globalEnterpriseApi.getMultiRegionConfig(),
        globalEnterpriseApi.getHighAvailabilityConfig(),
        globalEnterpriseApi.getZeroDowntimeDeployConfig(),
        globalEnterpriseApi.getDisasterRecoveryConfig(),
        globalEnterpriseApi.getComplianceChecklist(),
      ]);
      setOverview(overviewRes);
      setRegions(multiRegionRes.regions || []);
      setHaConfig(haRes);
      setDeployConfig(deployRes);
      setDrConfig(drRes);
      setCompliance(complianceRes);
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } }; message?: string };
      setError(e.response?.data?.detail || e.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Level 5 グローバルエンタープライズ
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 1 }}>
        マルチリージョン、高可用性、ゼロダウンタイムデプロイ、コンプライアンス、DR
      </Typography>
      <Chip label="設計・アーキテクチャ（組織・運用は除外）" size="small" color="info" sx={{ mb: 2 }} />

      {overview && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={2}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>リージョン</Typography>
                <Typography variant="h4">{overview.features.multi_region.regions_count}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={2}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>SLA</Typography>
                <Typography variant="h4">{overview.features.high_availability.target_sla}%</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={2}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>デプロイ戦略</Typography>
                <Typography variant="h4">{overview.features.zero_downtime_deploy.strategies}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={2}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>RPO</Typography>
                <Typography variant="h6">{overview.features.disaster_recovery.rpo_seconds}秒</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={2}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>コンプライアンス</Typography>
                <Typography variant="h6">{overview.features.compliance.frameworks.join(', ')}</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
        <Tab icon={<Public />} iconPosition="start" label="マルチリージョン" />
        <Tab icon={<Security />} iconPosition="start" label="高可用性" />
        <Tab icon={<Update />} iconPosition="start" label="ゼロダウンタイム" />
        <Tab icon={<Backup />} iconPosition="start" label="災害復旧" />
        <Tab icon={<Gavel />} iconPosition="start" label="コンプライアンス" />
      </Tabs>

      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {loading && <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>}

      {!loading && (
        <>
          <TabPanel value={tabValue} index={0}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>リージョン</TableCell>
                    <TableCell>プロバイダ</TableCell>
                    <TableCell>データ主権</TableCell>
                    <TableCell>ステータス</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {regions.map((r) => (
                    <TableRow key={r.id}>
                      <TableCell>{r.name}</TableCell>
                      <TableCell>{r.provider}</TableCell>
                      <TableCell>{r.data_residency}</TableCell>
                      <TableCell><Chip label={r.status} color="success" size="small" /></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            {haConfig && (
              <Box>
                <Typography variant="h6" gutterBottom>目標SLA: {haConfig.target_sla}%</Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  最大ダウンタイム: 年間 {haConfig.max_downtime_per_year_minutes} 分
                </Typography>
                <TableContainer component={Paper} sx={{ mt: 2 }}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>コンポーネント</TableCell>
                        <TableCell>レプリカ数</TableCell>
                        <TableCell>戦略</TableCell>
                        <TableCell>自動フェイルオーバー</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {haConfig.components?.map((c: any) => (
                        <TableRow key={c.name}>
                          <TableCell>{c.name}</TableCell>
                          <TableCell>{c.replicas}</TableCell>
                          <TableCell>{c.strategy}</TableCell>
                          <TableCell>{c.auto_failover ? '✓' : '-'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Box>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            {deployConfig && (
              <Grid container spacing={2}>
                {deployConfig.strategies?.map((s: any) => (
                  <Grid item xs={12} md={4} key={s.name}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6">{s.name}</Typography>
                        <Typography variant="body2" color="text.secondary">{s.description}</Typography>
                        <Chip label={s.enabled ? '有効' : '無効'} size="small" color={s.enabled ? 'success' : 'default'} sx={{ mt: 1 }} />
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            {drConfig && (
              <Card>
                <CardContent>
                  <Typography variant="h6">RPO (Recovery Point Objective)</Typography>
                  <Typography>{drConfig.rpo_seconds}秒（{drConfig.rpo_seconds / 60}分）</Typography>
                  <Typography variant="h6" sx={{ mt: 2 }}>RTO (Recovery Time Objective)</Typography>
                  <Typography>{drConfig.rto_seconds}秒（{drConfig.rto_seconds / 60}分）</Typography>
                  <Typography variant="h6" sx={{ mt: 2 }}>バックアップ</Typography>
                  <Typography variant="body2">頻度: {drConfig.backup?.frequency} / 保持: {drConfig.backup?.retention_days}日 / クロスリージョン: {drConfig.backup?.cross_region ? '有' : '無'}</Typography>
                  <Typography variant="h6" sx={{ mt: 2 }}>フェイルオーバー</Typography>
                  <Typography variant="body2">自動: {drConfig.failover?.automatic ? '有' : '無'}</Typography>
                </CardContent>
              </Card>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            {Object.entries(compliance).map(([framework, items]) => (
              <Box key={framework} sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>{framework.toUpperCase()}</Typography>
                <TableContainer component={Paper}>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>項目</TableCell>
                        <TableCell>ステータス</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {items.map((item) => (
                        <TableRow key={item.id}>
                          <TableCell>{item.item}</TableCell>
                          <TableCell><Chip label={item.status} size="small" /></TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Box>
            ))}
          </TabPanel>
        </>
      )}
    </Box>
  );
};
