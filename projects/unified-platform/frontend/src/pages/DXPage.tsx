/**
 * DX推進基盤ページ
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
  Tabs,
  Tab,
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
  IconButton,
} from '@mui/material';
import { TrendingUp, Add, Edit, Delete } from '@mui/icons-material';
import { unifiedApi } from '../api/unified';

function TabPanel({ children, value, index }: { children: React.ReactNode; value: number; index: number }) {
  return <div hidden={value !== index} style={{ display: value === index ? 'block' : 'none' }}>{children}</div>;
}

export const DXPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [summary, setSummary] = useState<any>(null);
  const [documents, setDocuments] = useState<any[]>([]);
  const [workflows, setWorkflows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [docDialogOpen, setDocDialogOpen] = useState(false);
  const [wfDialogOpen, setWfDialogOpen] = useState(false);
  const [editingDoc, setEditingDoc] = useState<any>(null);
  const [editingWf, setEditingWf] = useState<any>(null);
  const [docForm, setDocForm] = useState({ title: '', content: '', category: 'general' });
  const [wfForm, setWfForm] = useState({ name: '', description: '', status: 'draft' });

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (tabValue === 0) loadData();
    else if (tabValue === 1) loadDocuments();
    else if (tabValue === 2) loadWorkflows();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const { data } = await unifiedApi.dx.getSummary();
      setSummary(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const loadDocuments = async () => {
    try {
      const { data } = await unifiedApi.dx.getDocuments();
      setDocuments(data?.items || []);
    } catch {
      setDocuments([]);
    }
  };

  const loadWorkflows = async () => {
    try {
      const { data } = await unifiedApi.dx.getWorkflows();
      setWorkflows(data?.items || []);
    } catch {
      setWorkflows([]);
    }
  };

  const handleCreateDocument = async () => {
    try {
      await unifiedApi.dx.createDocument(docForm);
      setDocDialogOpen(false);
      setDocForm({ title: '', content: '', category: 'general' });
      loadDocuments();
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '作成に失敗しました');
    }
  };

  const handleUpdateDocument = async () => {
    if (!editingDoc) return;
    try {
      await unifiedApi.dx.updateDocument(editingDoc.id, docForm);
      setDocDialogOpen(false);
      setEditingDoc(null);
      setDocForm({ title: '', content: '', category: 'general' });
      loadDocuments();
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '更新に失敗しました');
    }
  };

  const handleDeleteDocument = async (id: string) => {
    try {
      await unifiedApi.dx.deleteDocument(id);
      loadDocuments();
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '削除に失敗しました');
    }
  };

  const handleCreateWorkflow = async () => {
    try {
      await unifiedApi.dx.createWorkflow(wfForm);
      setWfDialogOpen(false);
      setWfForm({ name: '', description: '', status: 'draft' });
      loadWorkflows();
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '作成に失敗しました');
    }
  };

  const handleUpdateWorkflow = async () => {
    if (!editingWf) return;
    try {
      await unifiedApi.dx.updateWorkflow(editingWf.id, wfForm);
      setWfDialogOpen(false);
      setEditingWf(null);
      setWfForm({ name: '', description: '', status: 'draft' });
      loadWorkflows();
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '更新に失敗しました');
    }
  };

  const handleDeleteWorkflow = async (id: string) => {
    try {
      await unifiedApi.dx.deleteWorkflow(id);
      loadWorkflows();
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '削除に失敗しました');
    }
  };

  if (loading && !summary) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 300 }}>
        <CircularProgress aria-label="読み込み中" />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <TrendingUp /> DX推進基盤
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        ペーパーレス化、データ利活用、業務標準化を支える基盤
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} sx={{ mb: 2 }}>
        <Tab label="サマリー" />
        <Tab label="ドキュメント" />
        <Tab label="ワークフロー" />
      </Tabs>

      <TabPanel value={tabValue} index={0}>
        {summary && (
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>ドキュメント</Typography>
                  <Typography variant="h4">{summary.documents ?? 0}</Typography>
                  <Typography variant="body2">件</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>ワークフロー</Typography>
                  <Typography variant="h4">{summary.workflows ?? 0}</Typography>
                  <Typography variant="body2">件</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>機能</Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1 }}>
                    {(summary.features || []).map((f: string) => (
                      <Chip key={f} label={f} size="small" variant="outlined" />
                    ))}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box sx={{ mb: 2 }}>
          <Button variant="contained" startIcon={<Add />} onClick={() => { setEditingDoc(null); setDocForm({ title: '', content: '', category: 'general' }); setDocDialogOpen(true); }}>ドキュメント作成</Button>
        </Box>
        <Dialog open={docDialogOpen} onClose={() => setDocDialogOpen(false)} maxWidth="sm" fullWidth>
          <DialogTitle>{editingDoc ? 'ドキュメント編集' : 'ドキュメント作成'}</DialogTitle>
          <DialogContent>
            <TextField fullWidth label="タイトル" value={docForm.title} onChange={(e) => setDocForm({ ...docForm, title: e.target.value })} sx={{ mt: 1, mb: 1 }} />
            <TextField fullWidth multiline rows={3} label="内容" value={docForm.content} onChange={(e) => setDocForm({ ...docForm, content: e.target.value })} sx={{ mb: 1 }} />
            <TextField select fullWidth label="カテゴリ" value={docForm.category} onChange={(e) => setDocForm({ ...docForm, category: e.target.value })} SelectProps={{ native: true }}>
              <option value="general">general</option>
              <option value="contract">contract</option>
              <option value="report">report</option>
              <option value="manual">manual</option>
              <option value="policy">policy</option>
            </TextField>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDocDialogOpen(false)}>キャンセル</Button>
            <Button variant="contained" onClick={editingDoc ? handleUpdateDocument : handleCreateDocument}>{editingDoc ? '更新' : '作成'}</Button>
          </DialogActions>
        </Dialog>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>タイトル</TableCell>
                <TableCell>カテゴリ</TableCell>
                <TableCell>更新日</TableCell>
                <TableCell>操作</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {documents.length === 0 ? (
                <TableRow><TableCell colSpan={4} align="center">ドキュメントがありません</TableCell></TableRow>
              ) : (
                documents.map((d) => (
                  <TableRow key={d.id}>
                    <TableCell>{d.title}</TableCell>
                    <TableCell>{d.category}</TableCell>
                    <TableCell>{d.updated_at?.slice(0, 10)}</TableCell>
                    <TableCell>
                      <IconButton size="small" onClick={() => { setEditingDoc(d); setDocForm({ title: d.title, content: d.content || '', category: d.category || 'general' }); setDocDialogOpen(true); }}><Edit /></IconButton>
                      <IconButton size="small" onClick={() => handleDeleteDocument(d.id)}><Delete /></IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Box sx={{ mb: 2 }}>
          <Button variant="contained" startIcon={<Add />} onClick={() => { setEditingWf(null); setWfForm({ name: '', description: '', status: 'draft' }); setWfDialogOpen(true); }}>ワークフロー作成</Button>
        </Box>
        <Dialog open={wfDialogOpen} onClose={() => setWfDialogOpen(false)} maxWidth="sm" fullWidth>
          <DialogTitle>{editingWf ? 'ワークフロー編集' : 'ワークフロー作成'}</DialogTitle>
          <DialogContent>
            <TextField fullWidth label="名前" value={wfForm.name} onChange={(e) => setWfForm({ ...wfForm, name: e.target.value })} sx={{ mt: 1, mb: 1 }} />
            <TextField fullWidth multiline label="説明" value={wfForm.description} onChange={(e) => setWfForm({ ...wfForm, description: e.target.value })} sx={{ mb: 1 }} />
            <TextField select fullWidth label="ステータス" value={wfForm.status} onChange={(e) => setWfForm({ ...wfForm, status: e.target.value })} SelectProps={{ native: true }}>
              <option value="draft">draft</option>
              <option value="active">active</option>
              <option value="archived">archived</option>
            </TextField>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setWfDialogOpen(false)}>キャンセル</Button>
            <Button variant="contained" onClick={editingWf ? handleUpdateWorkflow : handleCreateWorkflow}>{editingWf ? '更新' : '作成'}</Button>
          </DialogActions>
        </Dialog>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>名前</TableCell>
                <TableCell>説明</TableCell>
                <TableCell>ステップ数</TableCell>
                <TableCell>ステータス</TableCell>
                <TableCell>更新日</TableCell>
                <TableCell>操作</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {workflows.length === 0 ? (
                <TableRow><TableCell colSpan={6} align="center">ワークフローがありません</TableCell></TableRow>
              ) : (
                workflows.map((w) => (
                  <TableRow key={w.id}>
                    <TableCell>{w.name}</TableCell>
                    <TableCell>{w.description || '-'}</TableCell>
                    <TableCell>{(w.steps || []).length}段階</TableCell>
                    <TableCell>{w.status}</TableCell>
                    <TableCell>{w.updated_at?.slice(0, 10)}</TableCell>
                    <TableCell>
                      <IconButton size="small" onClick={() => { setEditingWf(w); setWfForm({ name: w.name, description: w.description || '', status: w.status || 'draft' }); setWfDialogOpen(true); }}><Edit /></IconButton>
                      <IconButton size="small" onClick={() => handleDeleteWorkflow(w.id)}><Delete /></IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>
    </Box>
  );
};
