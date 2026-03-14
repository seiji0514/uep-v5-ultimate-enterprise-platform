/**
 * 契約ワークフロー ページ
 * 見積・契約・納品・請求の一気通貫（DB化・PDF出力・実データ運用）
 * 統合基盤モジュール（5モジュール）の1つ
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
  Button,
} from '@mui/material';
import {
  RequestQuote,
  Description,
  LocalShipping,
  Receipt,
  PictureAsPdf,
  VerifiedUser,
} from '@mui/icons-material';
import { contractWorkflowApi } from '../../api/contractWorkflow';
import { useAutoPlayNarration } from '../../hooks/useAutoPlayNarration';

function TabPanel({ children, value, index }: { children?: React.ReactNode; index: number; value: number }) {
  return <div role="tabpanel" hidden={value !== index}>{value === index && <Box sx={{ p: 2 }}>{children}</Box>}</div>;
}

export const ContractWorkflowPage: React.FC = () => {
  useAutoPlayNarration(6);
  const [tabValue, setTabValue] = useState(0);
  const [estimates, setEstimates] = useState<any[]>([]);
  const [contracts, setContracts] = useState<any[]>([]);
  const [deliveries, setDeliveries] = useState<any[]>([]);
  const [invoices, setInvoices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [e, c, d, i] = await Promise.all([
        contractWorkflowApi.getEstimates(),
        contractWorkflowApi.getContracts(),
        contractWorkflowApi.getDeliveries(),
        contractWorkflowApi.getInvoices(),
      ]);
      setEstimates(e.data?.items || []);
      setContracts(c.data?.items || []);
      setDeliveries(d.data?.items || []);
      setInvoices(i.data?.items || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleExportPdf = async (type: string, id: string) => {
    try {
      const blob = await contractWorkflowApi.exportPdf(type, id);
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'PDF出力に失敗しました');
    }
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box
        sx={{
          mb: 2,
          p: 2,
          borderRadius: 1,
          bgcolor: 'rgba(76, 175, 80, 0.2)',
          borderLeft: '4px solid',
          borderColor: 'success.main',
          display: 'flex',
          alignItems: 'center',
          gap: 2,
        }}
      >
        <VerifiedUser sx={{ fontSize: 32, color: 'success.main' }} />
        <Box>
          <Typography variant="subtitle1" fontWeight={700} color="success.main">
            実データ運用中
          </Typography>
          <Typography variant="body2" color="text.secondary">
            見積・契約・納品・請求を一気通貫で実運用。DB化・PDF出力に対応し、デモではなく本番データで稼働しています。
          </Typography>
        </Box>
      </Box>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>契約ワークフロー</Typography>
        <Typography variant="body2" color="text.secondary">
          見積・契約・納品・請求の一気通貫。DB化・PDF出力・実データ運用に対応。
        </Typography>
      </Box>
      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<RequestQuote />} iconPosition="start" label="見積" />
          <Tab icon={<Description />} iconPosition="start" label="契約" />
          <Tab icon={<LocalShipping />} iconPosition="start" label="納品" />
          <Tab icon={<Receipt />} iconPosition="start" label="請求" />
        </Tabs>
        {error && <Alert severity="error" sx={{ m: 2 }} onClose={() => setError('')}>{error}</Alert>}
        {loading ? (
          <Box sx={{ p: 4, textAlign: 'center' }}><CircularProgress /></Box>
        ) : (
          <>
            <TabPanel value={tabValue} index={0}>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>見積No</TableCell>
                      <TableCell>案件名</TableCell>
                      <TableCell>金額</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>操作</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {estimates.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell>{row.estimate_no}</TableCell>
                        <TableCell>{row.title}</TableCell>
                        <TableCell>¥{row.amount?.toLocaleString()}</TableCell>
                        <TableCell><Chip label={row.status} size="small" color={row.status === '承認済' ? 'success' : 'default'} /></TableCell>
                        <TableCell>
                          <Button size="small" startIcon={<PictureAsPdf />} onClick={() => handleExportPdf('estimate', row.id)}>PDF</Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>契約No</TableCell>
                      <TableCell>案件名</TableCell>
                      <TableCell>契約日</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>操作</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {contracts.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell>{row.contract_no}</TableCell>
                        <TableCell>{row.title}</TableCell>
                        <TableCell>{row.contract_date}</TableCell>
                        <TableCell><Chip label={row.status} size="small" color={row.status === '締結済' ? 'success' : 'default'} /></TableCell>
                        <TableCell>
                          <Button size="small" startIcon={<PictureAsPdf />} onClick={() => handleExportPdf('contract', row.id)}>PDF</Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>納品No</TableCell>
                      <TableCell>案件名</TableCell>
                      <TableCell>納品日</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>操作</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {deliveries.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell>{row.delivery_no}</TableCell>
                        <TableCell>{row.title}</TableCell>
                        <TableCell>{row.delivery_date}</TableCell>
                        <TableCell><Chip label={row.status} size="small" color={row.status === '完了' ? 'success' : 'default'} /></TableCell>
                        <TableCell>
                          <Button size="small" startIcon={<PictureAsPdf />} onClick={() => handleExportPdf('delivery', row.id)}>PDF</Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={3}>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>請求No</TableCell>
                      <TableCell>案件名</TableCell>
                      <TableCell>金額</TableCell>
                      <TableCell>支払期限</TableCell>
                      <TableCell>ステータス</TableCell>
                      <TableCell>操作</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {invoices.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell>{row.invoice_no}</TableCell>
                        <TableCell>{row.title}</TableCell>
                        <TableCell>¥{row.amount?.toLocaleString()}</TableCell>
                        <TableCell>{row.due_date}</TableCell>
                        <TableCell><Chip label={row.status} size="small" color={row.status === '入金済' ? 'success' : 'default'} /></TableCell>
                        <TableCell>
                          <Button size="small" startIcon={<PictureAsPdf />} onClick={() => handleExportPdf('invoice', row.id)}>PDF</Button>
                        </TableCell>
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
