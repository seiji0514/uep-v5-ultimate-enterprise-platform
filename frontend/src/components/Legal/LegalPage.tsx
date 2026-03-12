/**
 * 法務 ページ
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
} from '@mui/material';
import { Gavel, Policy, Lightbulb } from '@mui/icons-material';
import { legalApi, ContractReview, RegulatoryItem, IpPortfolio } from '../../api/legal';

function TabPanel({ children, value, index }: { children?: React.ReactNode; index: number; value: number }) {
  return <div role="tabpanel" hidden={value !== index}>{value === index && <Box sx={{ p: 2 }}>{children}</Box>}</div>;
}

export const LegalPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [contracts, setContracts] = useState<ContractReview[]>([]);
  const [regulatory, setRegulatory] = useState<RegulatoryItem[]>([]);
  const [ip, setIp] = useState<IpPortfolio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) setContracts(await legalApi.getContractReviews());
      else if (tabValue === 1) setRegulatory(await legalApi.getRegulatory());
      else setIp(await legalApi.getIpPortfolio());
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>法務</Typography>
        <Typography variant="body2" color="text.secondary">契約書レビュー、規制対応、知的財産、コンプライアンス</Typography>
      </Box>
      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<Gavel />} iconPosition="start" label="契約書レビュー" />
          <Tab icon={<Policy />} iconPosition="start" label="規制対応" />
          <Tab icon={<Lightbulb />} iconPosition="start" label="知的財産" />
        </Tabs>
        {error && <Alert severity="error" sx={{ m: 2 }} onClose={() => setError('')}>{error}</Alert>}
        {loading ? <Box sx={{ p: 4, textAlign: 'center' }}><CircularProgress /></Box> : (
          <>
            <TabPanel value={tabValue} index={0}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>タイトル</TableCell><TableCell>ステータス</TableCell><TableCell>リスク</TableCell></TableRow></TableHead>
                  <TableBody>
                    {contracts.map((c) => (
                      <TableRow key={c.id}><TableCell>{c.title}</TableCell><TableCell><Chip label={c.status} size="small" /></TableCell><TableCell><Chip label={c.risk_level} size="small" color={c.risk_level === '高' ? 'error' : 'default'} /></TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>規制名</TableCell><TableCell>期限</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
                  <TableBody>
                    {regulatory.map((r) => (
                      <TableRow key={r.id}><TableCell>{r.name}</TableCell><TableCell>{new Date(r.deadline).toLocaleDateString('ja-JP')}</TableCell><TableCell><Chip label={r.status} size="small" color={r.status === '完了' ? 'success' : 'default'} /></TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>種別</TableCell><TableCell>タイトル</TableCell><TableCell>ステータス</TableCell><TableCell>出願日</TableCell></TableRow></TableHead>
                  <TableBody>
                    {ip.map((i) => (
                      <TableRow key={i.id}><TableCell>{i.type}</TableCell><TableCell>{i.title}</TableCell><TableCell><Chip label={i.status} size="small" /></TableCell><TableCell>{i.filing_date}</TableCell></TableRow>
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
