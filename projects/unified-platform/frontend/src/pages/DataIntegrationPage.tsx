/**
 * データ連携基盤ページ
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { Sync } from '@mui/icons-material';
import { unifiedApi } from '../api/unified';

export const DataIntegrationPage: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [rules, setRules] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [form, setForm] = useState({ source_system: 'erp_sales', target_system: 'accounting', sync_type: 'batch' });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [summaryRes, rulesRes, logsRes] = await Promise.all([
        unifiedApi.dataIntegration.getSummary(),
        unifiedApi.dataIntegration.getRules(),
        unifiedApi.dataIntegration.getLogs().catch(() => ({ data: { items: [] } })),
      ]);
      setSummary(summaryRes.data);
      setRules(Array.isArray(rulesRes.data) ? rulesRes.data : []);
      setLogs(logsRes.data?.items || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRule = async () => {
    try {
      await unifiedApi.dataIntegration.createRule(form);
      setDialogOpen(false);
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '作成に失敗しました');
    }
  };

  const handleExecuteSync = async (ruleId: string) => {
    try {
      await unifiedApi.dataIntegration.executeSync(ruleId);
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '同期実行に失敗しました');
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 300 }}>
        <CircularProgress aria-label="読み込み中" />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Sync /> データ連携基盤
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        基幹システムと周辺システムの連携・データ統合
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ mb: 2 }}>
        <Button variant="contained" onClick={() => setDialogOpen(true)}>連携ルールを作成</Button>
      </Box>
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>連携ルール作成</DialogTitle>
        <DialogContent>
          <TextField select fullWidth label="ソース" value={form.source_system} onChange={(e) => setForm({ ...form, source_system: e.target.value })} SelectProps={{ native: true }} sx={{ mt: 1, mb: 1 }}>
            <option value="erp_sales">erp_sales</option>
            <option value="erp_purchasing">erp_purchasing</option>
            <option value="accounting">accounting</option>
            <option value="hr">hr</option>
          </TextField>
          <TextField select fullWidth label="ターゲット" value={form.target_system} onChange={(e) => setForm({ ...form, target_system: e.target.value })} SelectProps={{ native: true }} sx={{ mb: 1 }}>
            <option value="accounting">accounting</option>
            <option value="erp_sales">erp_sales</option>
            <option value="erp_purchasing">erp_purchasing</option>
            <option value="hr">hr</option>
          </TextField>
          <TextField select fullWidth label="連携タイプ" value={form.sync_type} onChange={(e) => setForm({ ...form, sync_type: e.target.value })} SelectProps={{ native: true }}>
            <option value="realtime">realtime</option>
            <option value="batch">batch</option>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>キャンセル</Button>
          <Button variant="contained" onClick={handleCreateRule}>作成</Button>
        </DialogActions>
      </Dialog>

      {summary && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>連携ルール数</Typography>
                <Typography variant="h4">{summary.rules_count ?? 0}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>連携対象システム</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1 }}>
                  {(summary.systems || []).map((s: string) => (
                    <Chip key={s} label={s} size="small" variant="outlined" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Typography variant="subtitle1" sx={{ mb: 1 }}>連携ルール一覧</Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ルールID</TableCell>
              <TableCell>ソース</TableCell>
              <TableCell>ターゲット</TableCell>
              <TableCell>連携タイプ</TableCell>
              <TableCell>操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rules.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center">連携ルールがありません</TableCell>
              </TableRow>
            ) : (
              rules.map((r) => (
                <TableRow key={r.id}>
                  <TableCell>{r.id}</TableCell>
                  <TableCell>{r.source_system}</TableCell>
                  <TableCell>{r.target_system}</TableCell>
                  <TableCell>{r.sync_type}</TableCell>
                  <TableCell>
                    <Button size="small" variant="outlined" onClick={() => handleExecuteSync(r.id)}>同期実行</Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="subtitle1" sx={{ mt: 3, mb: 1 }}>同期実行ログ</Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ルールID</TableCell>
              <TableCell>ソース→ターゲット</TableCell>
              <TableCell>実行日時</TableCell>
              <TableCell>同期件数</TableCell>
              <TableCell>ステータス</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {logs.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center">ログがありません</TableCell>
              </TableRow>
            ) : (
              logs.map((l, i) => (
                <TableRow key={i}>
                  <TableCell>{l.rule_id}</TableCell>
                  <TableCell>{l.source_system} → {l.target_system}</TableCell>
                  <TableCell>{l.executed_at?.slice(0, 19)}</TableCell>
                  <TableCell>{l.records_synced ?? 0}件</TableCell>
                  <TableCell>{l.status}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
