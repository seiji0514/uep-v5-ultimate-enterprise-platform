/**
 * レガシー刷新・クラウド移行ページ
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
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import { Storage } from '@mui/icons-material';
import { unifiedApi } from '../api/unified';

export const LegacyMigrationPage: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [jobs, setJobs] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [form, setForm] = useState({ name: '', source_type: 'csv', target_system: 'erp_sales' });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [summaryRes, jobsRes, logsRes] = await Promise.all([
        unifiedApi.legacyMigration.getSummary(),
        unifiedApi.legacyMigration.getJobs(),
        unifiedApi.legacyMigration.getLogs().catch(() => ({ data: { items: [] } })),
      ]);
      setSummary(summaryRes.data);
      setJobs(Array.isArray(jobsRes.data) ? jobsRes.data : []);
      setLogs(logsRes.data?.items || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateJob = async () => {
    try {
      await unifiedApi.legacyMigration.createJob({
        name: form.name || undefined,
        source_type: form.source_type,
        source_config: {},
        target_system: form.target_system,
      });
      setDialogOpen(false);
      setForm({ name: '', source_type: 'csv', target_system: 'erp_sales' });
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '作成に失敗しました');
    }
  };

  const handleRunJob = async (jobId: string) => {
    try {
      await unifiedApi.legacyMigration.runJob(jobId);
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '実行に失敗しました');
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
        <Storage /> レガシー刷新・クラウド移行
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        メインフレーム・オンプレからクラウドERPへの移行支援
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ mb: 2 }}>
        <Button variant="contained" onClick={() => setDialogOpen(true)}>移行ジョブを作成</Button>
      </Box>
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>移行ジョブ作成</DialogTitle>
        <DialogContent>
          <TextField fullWidth label="ジョブ名" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="例: 旧販売DB移行" sx={{ mt: 1, mb: 1 }} />
          <TextField select fullWidth label="ソースタイプ" value={form.source_type} onChange={(e) => setForm({ ...form, source_type: e.target.value })} SelectProps={{ native: true }} sx={{ mb: 1 }}>
            <option value="csv">CSV</option>
            <option value="excel">Excel</option>
            <option value="db">DB</option>
            <option value="api">API</option>
          </TextField>
          <TextField select fullWidth label="ターゲット" value={form.target_system} onChange={(e) => setForm({ ...form, target_system: e.target.value })} SelectProps={{ native: true }}>
            <option value="erp_sales">ERP 販売</option>
            <option value="erp_purchasing">ERP 購買</option>
            <option value="accounting">会計</option>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>キャンセル</Button>
          <Button variant="contained" onClick={handleCreateJob}>作成</Button>
        </DialogActions>
      </Dialog>

      {summary && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>移行ジョブ</Typography>
                <Typography variant="h4">{summary.jobs ?? 0}</Typography>
                <Typography variant="body2">総件数</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>完了</Typography>
                <Typography variant="h4">{summary.completed ?? 0}</Typography>
                <Typography variant="body2">件</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>ツール</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1 }}>
                  {(summary.tools || []).map((t: string) => (
                    <Chip key={t} label={t} size="small" variant="outlined" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Typography variant="subtitle1" sx={{ mb: 1 }}>移行ジョブ一覧</Typography>
      <TableContainer component={Paper}>
        <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>ジョブ名</TableCell>
                <TableCell>ソース</TableCell>
                <TableCell>ターゲット</TableCell>
                <TableCell>ステータス</TableCell>
                <TableCell>移行件数</TableCell>
                <TableCell>操作</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {jobs.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">ジョブがありません</TableCell>
                </TableRow>
              ) : (
                jobs.map((j) => (
                  <TableRow key={j.id}>
                    <TableCell>{j.name || j.id}</TableCell>
                    <TableCell>{j.source_type}</TableCell>
                    <TableCell>{j.target_system}</TableCell>
                    <TableCell>{j.status}</TableCell>
                    <TableCell>{j.records_migrated != null ? `${j.records_migrated}件` : '-'}</TableCell>
                    <TableCell>
                      {j.status === 'pending' && (
                        <Button size="small" variant="outlined" onClick={() => handleRunJob(j.id)}>実行</Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))
              )}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="subtitle1" sx={{ mt: 3, mb: 1 }}>移行実行ログ</Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ジョブID</TableCell>
              <TableCell>実行日時</TableCell>
              <TableCell>移行件数</TableCell>
              <TableCell>ステータス</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {logs.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} align="center">ログがありません</TableCell>
              </TableRow>
            ) : (
              logs.map((l, i) => (
                <TableRow key={i}>
                  <TableCell>{l.job_id}</TableCell>
                  <TableCell>{l.executed_at?.slice(0, 19)}</TableCell>
                  <TableCell>{l.records_migrated ?? 0}件</TableCell>
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
