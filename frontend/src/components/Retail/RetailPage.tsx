/**
 * 小売・EC ページ
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
import { Store, ShoppingCart, Inventory } from '@mui/icons-material';
import { retailApi, PosTransaction, EcOrder, InventoryItem } from '../../api/retail';

function TabPanel({ children, value, index }: { children?: React.ReactNode; index: number; value: number }) {
  return <div role="tabpanel" hidden={value !== index}>{value === index && <Box sx={{ p: 2 }}>{children}</Box>}</div>;
}

export const RetailPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [pos, setPos] = useState<PosTransaction[]>([]);
  const [ec, setEc] = useState<EcOrder[]>([]);
  const [inv, setInv] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) setPos(await retailApi.getPosTransactions());
      else if (tabValue === 1) setEc(await retailApi.getEcOrders());
      else setInv(await retailApi.getInventory());
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>小売・EC</Typography>
        <Typography variant="body2" color="text.secondary">POS、EC、在庫、顧客分析</Typography>
      </Box>
      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<Store />} iconPosition="start" label="POS取引" />
          <Tab icon={<ShoppingCart />} iconPosition="start" label="EC注文" />
          <Tab icon={<Inventory />} iconPosition="start" label="在庫" />
        </Tabs>
        {error && <Alert severity="error" sx={{ m: 2 }} onClose={() => setError('')}>{error}</Alert>}
        {loading ? <Box sx={{ p: 4, textAlign: 'center' }}><CircularProgress /></Box> : (
          <>
            <TabPanel value={tabValue} index={0}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>ID</TableCell><TableCell>店舗</TableCell><TableCell>金額</TableCell><TableCell>支払</TableCell><TableCell>日時</TableCell></TableRow></TableHead>
                  <TableBody>
                    {pos.map((p) => (
                      <TableRow key={p.id}><TableCell>{p.id}</TableCell><TableCell>{p.store}</TableCell><TableCell>¥{p.amount.toLocaleString()}</TableCell><TableCell>{p.payment}</TableCell><TableCell>{new Date(p.timestamp).toLocaleString('ja-JP')}</TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>ID</TableCell><TableCell>顧客</TableCell><TableCell>金額</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
                  <TableBody>
                    {ec.map((e) => (
                      <TableRow key={e.id}><TableCell>{e.id}</TableCell><TableCell>{e.customer_id}</TableCell><TableCell>¥{e.amount.toLocaleString()}</TableCell><TableCell><Chip label={e.status} size="small" /></TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>SKU</TableCell><TableCell>商品名</TableCell><TableCell>在庫</TableCell><TableCell>発注点</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
                  <TableBody>
                    {inv.map((i) => (
                      <TableRow key={i.sku}><TableCell>{i.sku}</TableCell><TableCell>{i.name}</TableCell><TableCell>{i.qty}</TableCell><TableCell>{i.reorder_level}</TableCell><TableCell><Chip label={i.status} size="small" color={i.status === '要発注' ? 'error' : 'default'} /></TableCell></TableRow>
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
