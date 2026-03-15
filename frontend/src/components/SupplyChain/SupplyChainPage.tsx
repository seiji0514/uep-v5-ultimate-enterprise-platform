/**
 * サプライチェーン ページ
 * 統合基盤モジュール（6モジュール）の1つ
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
import { LocalShipping, Inventory, ShoppingBag } from '@mui/icons-material';
import { supplyChainApi, LogisticsShipment, InventoryItem, ProcurementOrder } from '../../api/supplyChain';
import { useAutoPlayNarration } from '../../hooks/useAutoPlayNarration';

function TabPanel({ children, value, index }: { children?: React.ReactNode; index: number; value: number }) {
  return <div role="tabpanel" hidden={value !== index}>{value === index && <Box sx={{ p: 2 }}>{children}</Box>}</div>;
}

export const SupplyChainPage: React.FC = () => {
  useAutoPlayNarration(7);
  const [tabValue, setTabValue] = useState(0);
  const [logistics, setLogistics] = useState<LogisticsShipment[]>([]);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [procurement, setProcurement] = useState<ProcurementOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) setLogistics(await supplyChainApi.getLogistics());
      else if (tabValue === 1) setInventory(await supplyChainApi.getInventory());
      else setProcurement(await supplyChainApi.getProcurement());
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>サプライチェーン</Typography>
        <Typography variant="body2" color="text.secondary">物流、在庫、調達、需要予測</Typography>
      </Box>
      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<LocalShipping />} iconPosition="start" label="物流" />
          <Tab icon={<Inventory />} iconPosition="start" label="在庫" />
          <Tab icon={<ShoppingBag />} iconPosition="start" label="調達" />
        </Tabs>
        {error && <Alert severity="error" sx={{ m: 2 }} onClose={() => setError('')}>{error}</Alert>}
        {loading ? <Box sx={{ p: 4, textAlign: 'center' }}><CircularProgress aria-label="読み込み中" /></Box> : (
          <>
            <TabPanel value={tabValue} index={0}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>ID</TableCell><TableCell>発地→着地</TableCell><TableCell>ステータス</TableCell><TableCell>配送業者</TableCell><TableCell>ETA</TableCell></TableRow></TableHead>
                  <TableBody>
                    {logistics.map((l) => (
                      <TableRow key={l.id}><TableCell>{l.id}</TableCell><TableCell>{l.origin} → {l.destination}</TableCell><TableCell><Chip label={l.status} size="small" /></TableCell><TableCell>{l.carrier}</TableCell><TableCell>{new Date(l.eta).toLocaleString('ja-JP')}</TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>SKU</TableCell><TableCell>品名</TableCell><TableCell>在庫</TableCell><TableCell>発注点</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
                  <TableBody>
                    {inventory.map((i) => (
                      <TableRow key={i.id}><TableCell>{i.sku}</TableCell><TableCell>{i.name}</TableCell><TableCell>{i.qty}</TableCell><TableCell>{i.reorder_level}</TableCell><TableCell><Chip label={i.status} size="small" color={i.status === '要発注' ? 'error' : 'default'} /></TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>ID</TableCell><TableCell>サプライヤー</TableCell><TableCell>金額</TableCell><TableCell>ステータス</TableCell><TableCell>納期</TableCell></TableRow></TableHead>
                  <TableBody>
                    {procurement.map((p) => (
                      <TableRow key={p.id}><TableCell>{p.id}</TableCell><TableCell>{p.supplier}</TableCell><TableCell>¥{p.amount.toLocaleString()}</TableCell><TableCell><Chip label={p.status} size="small" /></TableCell><TableCell>{new Date(p.delivery_date).toLocaleDateString('ja-JP')}</TableCell></TableRow>
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
