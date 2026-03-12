/**
 * 金融・FinTechプラットフォーム
 * 決済・リスクスコア・取引監視・ストレステスト
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
  Button,
  TextField,
} from '@mui/material';
import {
  AccountBalance,
  Payment,
  Security,
  Visibility,
  Science,
  Refresh,
} from '@mui/icons-material';
import {
  fintechApi,
  type Payment as PaymentType,
  type RiskScore,
  type TransactionMonitoring,
} from '../api';

export const FinTechPlatformPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [payments, setPayments] = useState<PaymentType[]>([]);
  const [riskScores, setRiskScores] = useState<RiskScore[]>([]);
  const [monitoring, setMonitoring] = useState<TransactionMonitoring[]>([]);
  const [stressResult, setStressResult] = useState<any>(null);
  const [portfolioValue, setPortfolioValue] = useState(1000000);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [pay, risk, mon] = await Promise.all([
        fintechApi.getPayments(),
        fintechApi.getRiskScores(),
        fintechApi.getTransactionMonitoring(),
      ]);
      setPayments(pay.items || []);
      setRiskScores(risk.items || []);
      setMonitoring(mon.items || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleStressTest = async () => {
    try {
      setLoading(true);
      setError('');
      const result = await fintechApi.runStressTest(portfolioValue);
      setStressResult(result);
      setTabValue(3);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'ストレステストに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level: string) =>
    ['高', 'high'].includes(level || '') ? 'error' : level === '中' ? 'warning' : 'success';
  const getStatusColor = (s: string) =>
    s === '要確認' || s === '監視中' ? 'warning' : s === '完了' ? 'success' : 'default';

  return (
    <Box>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">決済</Typography>
              <Typography variant="h4">{payments.length}</Typography>
              <Typography variant="caption" color="text.secondary">
                完了: {payments.filter((p) => p.status === '完了').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">リスクスコア</Typography>
              <Typography variant="h4">{riskScores.length}</Typography>
              <Typography variant="caption" color="text.secondary">
                高リスク: {riskScores.filter((r) => r.level === '高').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">取引監視</Typography>
              <Typography variant="h4">{monitoring.length}</Typography>
              <Typography variant="caption" color="text.secondary">
                要確認: {monitoring.filter((m) => m.status === '要確認').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography color="text.secondary" variant="body2">ストレステスト</Typography>
              <Typography variant="body2">規制対応</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Typography variant="h5" component="h1" gutterBottom>
        金融・FinTechプラットフォーム
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        決済・リスクスコア・取引監視・ストレステスト（規制対応）
      </Typography>

      <Stack direction="row" spacing={1} sx={{ mb: 2 }} flexWrap="wrap">
        <Chip
          icon={<Payment />}
          label="決済"
          onClick={() => setTabValue(0)}
          color={tabValue === 0 ? 'primary' : 'default'}
          variant={tabValue === 0 ? 'filled' : 'outlined'}
        />
        <Chip
          icon={<Security />}
          label="リスクスコア"
          onClick={() => setTabValue(1)}
          color={tabValue === 1 ? 'primary' : 'default'}
          variant={tabValue === 1 ? 'filled' : 'outlined'}
        />
        <Chip
          icon={<Visibility />}
          label="取引監視"
          onClick={() => setTabValue(2)}
          color={tabValue === 2 ? 'primary' : 'default'}
          variant={tabValue === 2 ? 'filled' : 'outlined'}
        />
        <Chip
          icon={<Science />}
          label="ストレステスト"
          onClick={() => setTabValue(3)}
          color={tabValue === 3 ? 'primary' : 'default'}
          variant={tabValue === 3 ? 'filled' : 'outlined'}
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
                    <TableCell>ID</TableCell>
                    <TableCell>金額</TableCell>
                    <TableCell>通貨</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>作成日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {payments.map((p) => (
                    <TableRow key={p.id} hover>
                      <TableCell>{p.id}</TableCell>
                      <TableCell>{p.amount.toLocaleString()}</TableCell>
                      <TableCell>{p.currency}</TableCell>
                      <TableCell><Chip label={p.status} size="small" color={getStatusColor(p.status) as any} /></TableCell>
                      <TableCell>{p.created_at ? new Date(p.created_at).toLocaleString('ja-JP') : '-'}</TableCell>
                    </TableRow>
                  ))}
                  {payments.length === 0 && <TableRow><TableCell colSpan={5} align="center">データがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {tabValue === 1 && (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>取引ID</TableCell>
                    <TableCell>リスクスコア</TableCell>
                    <TableCell>レベル</TableCell>
                    <TableCell>要因</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {riskScores.map((r) => (
                    <TableRow key={r.transaction_id} hover>
                      <TableCell>{r.transaction_id}</TableCell>
                      <TableCell>{(r.risk_score * 100).toFixed(0)}%</TableCell>
                      <TableCell><Chip label={r.level} color={getRiskColor(r.level) as any} size="small" /></TableCell>
                      <TableCell>{r.factors?.join(', ') || '-'}</TableCell>
                    </TableRow>
                  ))}
                  {riskScores.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
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
                    <TableCell>金額</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>アラート</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {monitoring.map((m) => (
                    <TableRow key={m.id} hover>
                      <TableCell>{m.type}</TableCell>
                      <TableCell>¥{m.amount.toLocaleString()}</TableCell>
                      <TableCell><Chip label={m.status} size="small" color={getStatusColor(m.status) as any} /></TableCell>
                      <TableCell>{m.alert || '-'}</TableCell>
                    </TableRow>
                  ))}
                  {monitoring.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {tabValue === 3 && (
            <Stack spacing={2}>
              <Stack direction="row" spacing={2} alignItems="center">
                <TextField
                  type="number"
                  label="ポートフォリオ価値（円）"
                  value={portfolioValue}
                  onChange={(e) => setPortfolioValue(Number(e.target.value) || 1000000)}
                  size="small"
                  sx={{ width: 220 }}
                />
                <Button variant="contained" onClick={handleStressTest} disabled={loading}>
                  ストレステスト実行
                </Button>
              </Stack>
              {stressResult && (
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle1" fontWeight={600} gutterBottom>結果</Typography>
                    <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
                      {JSON.stringify(stressResult, null, 2)}
                    </Typography>
                  </CardContent>
                </Card>
              )}
            </Stack>
          )}
        </>
      )}
    </Box>
  );
};
