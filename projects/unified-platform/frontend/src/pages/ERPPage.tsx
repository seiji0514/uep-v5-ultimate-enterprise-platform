/**
 * ERP（統合基幹業務システム）ページ
 * 販売管理・購買管理・データ連携基盤
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
  CircularProgress,
  Alert,
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
  Chip,
} from '@mui/material';
import { ShoppingCart } from '@mui/icons-material';
import { unifiedApi, ERPSummary } from '../api/unified';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  const isActive = value === index;
  return (
    <div role="tabpanel" hidden={!isActive} style={{ display: isActive ? 'block' : 'none' }} {...other}>
      <Box sx={{ p: 2 }}>{children}</Box>
    </div>
  );
}

export const ERPPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [summary, setSummary] = useState<ERPSummary | null>(null);
  const [salesOrders, setSalesOrders] = useState<any[]>([]);
  const [purchaseOrders, setPurchaseOrders] = useState<any[]>([]);
  const [syncRules, setSyncRules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [salesDialogOpen, setSalesDialogOpen] = useState(false);
  const [purchaseDialogOpen, setPurchaseDialogOpen] = useState(false);
  const [salesForm, setSalesForm] = useState({ customer_id: '', customer_name: '', total_amount: 0, notes: '' });
  const [purchaseForm, setPurchaseForm] = useState({ supplier_id: '', supplier_name: '', total_amount: 0, notes: '' });

  useEffect(() => {
    loadSummary();
  }, []);

  useEffect(() => {
    if (tabValue === 0) loadSummary();
    else if (tabValue === 1) loadSalesOrders();
    else if (tabValue === 2) loadPurchaseOrders();
    else if (tabValue === 3) loadDataIntegration();
  }, [tabValue]);

  const loadSummary = async () => {
    try {
      setLoading(true);
      setError('');
      const { data } = await unifiedApi.erp.getSummary();
      setSummary(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const loadSalesOrders = async () => {
    try {
      setLoading(true);
      setError('');
      const { data } = await unifiedApi.erp.getSalesOrders();
      setSalesOrders(Array.isArray(data) ? data : []);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const loadPurchaseOrders = async () => {
    try {
      setLoading(true);
      setError('');
      const { data } = await unifiedApi.erp.getPurchasingOrders();
      setPurchaseOrders(Array.isArray(data) ? data : []);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const loadDataIntegration = async () => {
    try {
      setLoading(true);
      setError('');
      const { data } = await unifiedApi.erp.getDataIntegrationRules();
      setSyncRules(Array.isArray(data) ? data : []);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSalesOrder = async () => {
    try {
      await unifiedApi.erp.createSalesOrder({
        customer_id: salesForm.customer_id,
        customer_name: salesForm.customer_name,
        items: [],
        total_amount: salesForm.total_amount,
        notes: salesForm.notes || undefined,
      });
      setSalesDialogOpen(false);
      setSalesForm({ customer_id: '', customer_name: '', total_amount: 0, notes: '' });
      loadSalesOrders();
      if (tabValue === 0) loadSummary();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '作成に失敗しました');
    }
  };

  const handleCreatePurchaseOrder = async () => {
    try {
      await unifiedApi.erp.createPurchasingOrder({
        supplier_id: purchaseForm.supplier_id,
        supplier_name: purchaseForm.supplier_name,
        items: [],
        total_amount: purchaseForm.total_amount,
        notes: purchaseForm.notes || undefined,
      });
      setPurchaseDialogOpen(false);
      setPurchaseForm({ supplier_id: '', supplier_name: '', total_amount: 0, notes: '' });
      loadPurchaseOrders();
      if (tabValue === 0) loadSummary();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '作成に失敗しました');
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
        <ShoppingCart /> ERP（統合基幹業務システム）
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        販売管理・購買管理・データ連携基盤
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} sx={{ mb: 2 }}>
        <Tab label="サマリー" />
        <Tab label="販売管理" />
        <Tab label="購買管理" />
        <Tab label="データ連携" />
      </Tabs>

      <TabPanel value={tabValue} index={0}>
        {summary && (
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    販売管理
                  </Typography>
                  <Typography variant="h4">{summary.modules.販売管理.order_count}</Typography>
                  <Typography variant="body2">受注件数</Typography>
                  <Typography variant="h6">{summary.modules.販売管理.total_sales.toLocaleString()}円</Typography>
                  <Typography variant="body2">売上合計</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    購買管理
                  </Typography>
                  <Typography variant="h4">{summary.modules.購買管理.order_count}</Typography>
                  <Typography variant="body2">発注件数</Typography>
                  <Typography variant="h6">{summary.modules.購買管理.total_purchases.toLocaleString()}円</Typography>
                  <Typography variant="body2">仕入合計</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    データ連携
                  </Typography>
                  <Typography variant="h4">{summary.modules.データ連携.rules_count}</Typography>
                  <Typography variant="body2">連携ルール数</Typography>
                  <Typography variant="body2">連携対象: {summary.modules.データ連携.systems.join(', ')}</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box sx={{ mb: 2 }}>
          <Button variant="contained" onClick={() => setSalesDialogOpen(true)}>受注を新規作成</Button>
        </Box>
        <Dialog open={salesDialogOpen} onClose={() => setSalesDialogOpen(false)} maxWidth="sm" fullWidth>
          <DialogTitle>受注作成</DialogTitle>
          <DialogContent>
            <TextField fullWidth label="顧客ID" value={salesForm.customer_id} onChange={(e) => setSalesForm({ ...salesForm, customer_id: e.target.value })} sx={{ mt: 1, mb: 1 }} />
            <TextField fullWidth label="顧客名" value={salesForm.customer_name} onChange={(e) => setSalesForm({ ...salesForm, customer_name: e.target.value })} sx={{ mb: 1 }} />
            <TextField fullWidth type="number" label="金額" value={salesForm.total_amount || ''} onChange={(e) => setSalesForm({ ...salesForm, total_amount: Number(e.target.value) || 0 })} sx={{ mb: 1 }} />
            <TextField fullWidth label="備考" value={salesForm.notes} onChange={(e) => setSalesForm({ ...salesForm, notes: e.target.value })} />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSalesDialogOpen(false)}>キャンセル</Button>
            <Button variant="contained" onClick={handleCreateSalesOrder}>作成</Button>
          </DialogActions>
        </Dialog>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>受注ID</TableCell>
                <TableCell>顧客名</TableCell>
                <TableCell>明細</TableCell>
                <TableCell>金額</TableCell>
                <TableCell>ステータス</TableCell>
                <TableCell>請求番号</TableCell>
                <TableCell>作成日</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {salesOrders.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    受注データがありません
                  </TableCell>
                </TableRow>
              ) : (
                salesOrders.map((o) => (
                  <TableRow key={o.id}>
                    <TableCell>{o.id}</TableCell>
                    <TableCell>{o.customer_name}</TableCell>
                    <TableCell>{(o.items || []).length}行</TableCell>
                    <TableCell>{o.total_amount?.toLocaleString()}円</TableCell>
                    <TableCell><Chip size="small" label={o.status} color={o.status === 'paid' ? 'success' : o.status === 'draft' ? 'default' : 'primary'} /></TableCell>
                    <TableCell>{o.invoice_no || '-'}</TableCell>
                    <TableCell>{o.created_at?.slice(0, 10)}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Box sx={{ mb: 2 }}>
          <Button variant="contained" onClick={() => setPurchaseDialogOpen(true)}>発注を新規作成</Button>
        </Box>
        <Dialog open={purchaseDialogOpen} onClose={() => setPurchaseDialogOpen(false)} maxWidth="sm" fullWidth>
          <DialogTitle>発注作成</DialogTitle>
          <DialogContent>
            <TextField fullWidth label="仕入先ID" value={purchaseForm.supplier_id} onChange={(e) => setPurchaseForm({ ...purchaseForm, supplier_id: e.target.value })} sx={{ mt: 1, mb: 1 }} />
            <TextField fullWidth label="仕入先名" value={purchaseForm.supplier_name} onChange={(e) => setPurchaseForm({ ...purchaseForm, supplier_name: e.target.value })} sx={{ mb: 1 }} />
            <TextField fullWidth type="number" label="金額" value={purchaseForm.total_amount || ''} onChange={(e) => setPurchaseForm({ ...purchaseForm, total_amount: Number(e.target.value) || 0 })} sx={{ mb: 1 }} />
            <TextField fullWidth label="備考" value={purchaseForm.notes} onChange={(e) => setPurchaseForm({ ...purchaseForm, notes: e.target.value })} />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setPurchaseDialogOpen(false)}>キャンセル</Button>
            <Button variant="contained" onClick={handleCreatePurchaseOrder}>作成</Button>
          </DialogActions>
        </Dialog>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>発注ID</TableCell>
                <TableCell>仕入先</TableCell>
                <TableCell>明細</TableCell>
                <TableCell>金額</TableCell>
                <TableCell>ステータス</TableCell>
                <TableCell>入荷日</TableCell>
                <TableCell>作成日</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {purchaseOrders.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    発注データがありません
                  </TableCell>
                </TableRow>
              ) : (
                purchaseOrders.map((o) => (
                  <TableRow key={o.id}>
                    <TableCell>{o.id}</TableCell>
                    <TableCell>{o.supplier_name}</TableCell>
                    <TableCell>{(o.items || []).length}行</TableCell>
                    <TableCell>{o.total_amount?.toLocaleString()}円</TableCell>
                    <TableCell><Chip size="small" label={o.status} color={o.status === 'paid' ? 'success' : o.status === 'draft' ? 'default' : 'primary'} /></TableCell>
                    <TableCell>{o.received_at ? o.received_at.slice(0, 10) : '-'}</TableCell>
                    <TableCell>{o.created_at?.slice(0, 10)}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={3}>
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>ルールID</TableCell>
                <TableCell>ソース</TableCell>
                <TableCell>ターゲット</TableCell>
                <TableCell>連携タイプ</TableCell>
                <TableCell>スケジュール</TableCell>
                <TableCell>有効</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {syncRules.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    連携ルールがありません
                  </TableCell>
                </TableRow>
              ) : (
                syncRules.map((r) => (
                  <TableRow key={r.id}>
                    <TableCell>{r.id}</TableCell>
                    <TableCell>{r.source_system}</TableCell>
                    <TableCell>{r.target_system}</TableCell>
                    <TableCell>{r.sync_type}</TableCell>
                    <TableCell>{r.schedule || '-'}</TableCell>
                    <TableCell><Chip size="small" label={r.enabled ? '有効' : '無効'} color={r.enabled ? 'success' : 'default'} /></TableCell>
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
