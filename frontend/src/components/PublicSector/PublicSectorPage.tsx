/**
 * 公共・官公庁 ページ
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
import { AccountBalance, Assignment, Assessment } from '@mui/icons-material';
import { publicSectorApi, Application, ApprovalWorkflow } from '../../api/publicSector';

function TabPanel({ children, value, index }: { children?: React.ReactNode; index: number; value: number }) {
  return <div role="tabpanel" hidden={value !== index}>{value === index && <Box sx={{ p: 2 }}>{children}</Box>}</div>;
}

export const PublicSectorPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [applications, setApplications] = useState<Application[]>([]);
  const [workflows, setWorkflows] = useState<ApprovalWorkflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) setApplications(await publicSectorApi.getApplications());
      else setWorkflows(await publicSectorApi.getApprovalWorkflow());
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>公共・官公庁</Typography>
        <Typography variant="body2" color="text.secondary">申請・承認ワークフロー、マイナンバー連携、自治体向け</Typography>
      </Box>
      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<Assignment />} iconPosition="start" label="申請一覧" />
          <Tab icon={<Assessment />} iconPosition="start" label="承認ワークフロー" />
        </Tabs>
        {error && <Alert severity="error" sx={{ m: 2 }} onClose={() => setError('')}>{error}</Alert>}
        {loading ? <Box sx={{ p: 4, textAlign: 'center' }}><CircularProgress /></Box> : (
          <>
            <TabPanel value={tabValue} index={0}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>ID</TableCell><TableCell>種別</TableCell><TableCell>申請者</TableCell><TableCell>ステータス</TableCell><TableCell>窓口</TableCell></TableRow></TableHead>
                  <TableBody>
                    {applications.map((a) => (
                      <TableRow key={a.id}>
                        <TableCell>{a.id}</TableCell><TableCell>{a.type}</TableCell><TableCell>{a.applicant}</TableCell>
                        <TableCell><Chip label={a.status} size="small" color={a.status === '承認済' ? 'success' : a.status === '差し戻し' ? 'error' : 'default'} /></TableCell>
                        <TableCell>{a.office}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>タイトル</TableCell><TableCell>現在ステップ</TableCell><TableCell>ステータス</TableCell><TableCell>期限</TableCell></TableRow></TableHead>
                  <TableBody>
                    {workflows.map((w) => (
                      <TableRow key={w.id}>
                        <TableCell>{w.title}</TableCell><TableCell>{w.current_step}</TableCell>
                        <TableCell><Chip label={w.status} size="small" color={w.status === '完了' ? 'success' : 'default'} /></TableCell>
                        <TableCell>{new Date(w.deadline).toLocaleDateString('ja-JP')}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
          </>
        )}
      </Paper>
    </Box>
  );
};
