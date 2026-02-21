/**
 * Level 2 プラットフォームページ
 * マルチテナント、SaaS化、APIマーケットプレイス
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
  Business,
  CardMembership,
  Store,
  Settings,
} from '@mui/icons-material';
import { platformApi, Level2Overview, Tenant, SubscriptionPlan, ApiListing } from '../../api/platform';

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

export const PlatformPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [overview, setOverview] = useState<Level2Overview | null>(null);
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [apiListings, setApiListings] = useState<ApiListing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [overviewRes, tenantsRes, plansRes, apiRes] = await Promise.all([
        platformApi.getOverview(),
        platformApi.getTenants(),
        platformApi.getPlans(),
        platformApi.getApiMarketplace(),
      ]);
      setOverview(overviewRes);
      setTenants(tenantsRes);
      setPlans(plansRes);
      setApiListings(apiRes);
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
        Level 2 プラットフォーム
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
        マルチテナント、SaaS化、APIマーケットプレイス
      </Typography>

      {overview && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>テナント</Typography>
                <Typography variant="h4">{overview.features.multi_tenant.tenants_count}</Typography>
                <Typography variant="caption">分離: {overview.features.multi_tenant.isolation_mode}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>サブスクリプション</Typography>
                <Typography variant="h4">{overview.features.saas.plans_count}</Typography>
                <Typography variant="caption">セルフサービス: {overview.features.saas.self_service ? '有効' : '無効'}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>APIマーケットプレイス</Typography>
                <Typography variant="h4">{overview.features.api_marketplace.listings_count}</Typography>
                <Typography variant="caption">API登録数</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
        <Tab icon={<Business />} iconPosition="start" label="マルチテナント" />
        <Tab icon={<CardMembership />} iconPosition="start" label="サブスクリプション" />
        <Tab icon={<Store />} iconPosition="start" label="APIマーケットプレイス" />
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
                    <TableCell>組織</TableCell>
                    <TableCell>プラン</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>API制限</TableCell>
                    <TableCell>ストレージ</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {tenants.map((t) => (
                    <TableRow key={t.id}>
                      <TableCell>{t.organization}</TableCell>
                      <TableCell>{t.plan_id}</TableCell>
                      <TableCell><Chip label={t.status} color="success" size="small" /></TableCell>
                      <TableCell>{t.resource_limits?.api_calls ?? '-'}</TableCell>
                      <TableCell>{t.resource_limits?.storage_gb ?? '-'} GB</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={2}>
              {plans.map((plan) => (
                <Grid item xs={12} sm={6} md={3} key={plan.id}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">{plan.name}</Typography>
                      <Typography variant="h4" color="primary">¥{plan.price_monthly.toLocaleString()}/月</Typography>
                      <Typography variant="body2" sx={{ mt: 1 }}>API: {plan.api_calls_limit === -1 ? '無制限' : plan.api_calls_limit.toLocaleString()}回</Typography>
                      <Typography variant="body2">ストレージ: {plan.storage_gb}GB</Typography>
                      <Box sx={{ mt: 1 }}>
                        {plan.features.map((f) => (
                          <Chip key={f} label={f} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                        ))}
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <Grid container spacing={2}>
              {apiListings.map((api) => (
                <Grid item xs={12} sm={6} md={4} key={api.id}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">{api.name}</Typography>
                      <Typography variant="body2" color="text.secondary">{api.description}</Typography>
                      <Typography variant="caption" sx={{ display: 'block', mt: 1 }}>エンドポイント: {api.endpoint}</Typography>
                      <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                        <Chip label={api.category} size="small" />
                        <Chip label={`¥${api.price_per_call}/call`} size="small" color="primary" />
                        <Typography variant="caption">呼出: {api.call_count}回</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </TabPanel>
        </>
      )}
    </Box>
  );
};
