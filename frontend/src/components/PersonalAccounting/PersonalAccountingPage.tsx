/**
 * 個人会計ページ（freee・マネーフォワード風）
 * 経費・売上管理、経費判定、月次レポート
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Button,
  Tabs,
  Tab,
  Alert,
  Chip,
  CircularProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Add, Delete, Receipt, AttachMoney } from '@mui/icons-material';
import {
  personalAccountingApi,
  Expense,
  Income,
  ExpenseCategory,
  DashboardSummary,
} from '../../api/personalAccounting';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  );
}

const formatYen = (n: number) => `¥${n.toLocaleString()}`;

export const PersonalAccountingPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [dashboard, setDashboard] = useState<DashboardSummary | null>(null);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [income, setIncome] = useState<Income[]>([]);
  const [categories, setCategories] = useState<ExpenseCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expenseOpen, setExpenseOpen] = useState(false);
  const [incomeOpen, setIncomeOpen] = useState(false);
  const [expenseForm, setExpenseForm] = useState({ date: new Date().toISOString().slice(0, 10), category_id: 'communication', amount: 0, description: '' });
  const [incomeForm, setIncomeForm] = useState({ date: new Date().toISOString().slice(0, 10), amount: 0, description: '', client_name: '' });

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [dash, exp, inc, cat] = await Promise.all([
        personalAccountingApi.getDashboard(),
        personalAccountingApi.getExpenses(),
        personalAccountingApi.getIncome(),
        personalAccountingApi.getCategories(),
      ]);
      setDashboard(dash);
      setExpenses(exp.items);
      setIncome(inc.items);
      setCategories(cat.categories);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '読み込みに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const handleAddExpense = async () => {
    try {
      await personalAccountingApi.createExpense({
        date: expenseForm.date,
        category_id: expenseForm.category_id,
        amount: expenseForm.amount,
        description: expenseForm.description,
      });
      setExpenseOpen(false);
      setExpenseForm({ date: new Date().toISOString().slice(0, 10), category_id: 'communication', amount: 0, description: '' });
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || '登録に失敗しました');
    }
  };

  const handleAddIncome = async () => {
    try {
      await personalAccountingApi.createIncome({
        date: incomeForm.date,
        amount: incomeForm.amount,
        description: incomeForm.description,
        client_name: incomeForm.client_name || undefined,
      });
      setIncomeOpen(false);
      setIncomeForm({ date: new Date().toISOString().slice(0, 10), amount: 0, description: '', client_name: '' });
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || '登録に失敗しました');
    }
  };

  const handleDeleteExpense = async (id: string) => {
    if (!window.confirm('削除しますか？')) return;
    try {
      await personalAccountingApi.deleteExpense(id);
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || '削除に失敗しました');
    }
  };

  const handleDeleteIncome = async (id: string) => {
    if (!window.confirm('削除しますか？')) return;
    try {
      await personalAccountingApi.deleteIncome(id);
      loadData();
    } catch (err: any) {
      setError(err.response?.data?.detail || '削除に失敗しました');
    }
  };

  if (loading && !dashboard) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress aria-label="読み込み中" />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }} component="h1">
        個人会計
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        freee・マネーフォワード風の個人用経費・売上管理。経費判定付き。
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* ダッシュボード */}
      {dashboard && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="text.secondary">今月の売上</Typography>
                <Typography variant="h5" color="success.main">{formatYen(dashboard.this_month_income)}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="text.secondary">今月の経費</Typography>
                <Typography variant="h5" color="error.main">{formatYen(dashboard.this_month_expense)}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="text.secondary">今月の利益</Typography>
                <Typography variant="h5" color={dashboard.this_month_profit >= 0 ? 'primary' : 'error'}>
                  {formatYen(dashboard.this_month_profit)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="text.secondary">今年の累計（売上 - 経費）</Typography>
                <Typography variant="h6">{formatYen(dashboard.ytd_profit)}</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* タブ */}
      <Card>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab label="経費" icon={<Receipt />} iconPosition="start" />
          <Tab label="売上" icon={<AttachMoney />} iconPosition="start" />
          <Tab label="カテゴリ（経費判定）" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button variant="contained" startIcon={<Add />} onClick={() => setExpenseOpen(true)}>
              経費を追加
            </Button>
          </Box>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>日付</TableCell>
                <TableCell>カテゴリ</TableCell>
                <TableCell>内容</TableCell>
                <TableCell align="right">金額</TableCell>
                <TableCell>経費</TableCell>
                <TableCell></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {expenses.map((e) => (
                <TableRow key={e.id}>
                  <TableCell>{e.date}</TableCell>
                  <TableCell>{e.category_name}</TableCell>
                  <TableCell>{e.description || '-'}</TableCell>
                  <TableCell align="right">{formatYen(e.amount)}</TableCell>
                  <TableCell>
                    <Chip
                      label={e.is_expense ? '経費' : '経費外'}
                      size="small"
                      color={e.is_expense ? 'success' : 'default'}
                    />
                  </TableCell>
                  <TableCell>
                    <IconButton size="small" onClick={() => handleDeleteExpense(e.id)} aria-label="削除">
                      <Delete fontSize="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
              {expenses.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6} align="center" sx={{ py: 4 }}>経費がありません</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button variant="contained" startIcon={<Add />} onClick={() => setIncomeOpen(true)}>
              売上を追加
            </Button>
          </Box>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>日付</TableCell>
                <TableCell>内容</TableCell>
                <TableCell>取引先</TableCell>
                <TableCell align="right">金額</TableCell>
                <TableCell></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {income.map((i) => (
                <TableRow key={i.id}>
                  <TableCell>{i.date}</TableCell>
                  <TableCell>{i.description || '-'}</TableCell>
                  <TableCell>{i.client_name || '-'}</TableCell>
                  <TableCell align="right">{formatYen(i.amount)}</TableCell>
                  <TableCell>
                    <IconButton size="small" onClick={() => handleDeleteIncome(i.id)} aria-label="削除">
                      <Delete fontSize="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
              {income.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5} align="center" sx={{ py: 4 }}>売上がありません</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            カテゴリを選ぶと経費かどうかが自動判定されます。
          </Typography>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>カテゴリ</TableCell>
                <TableCell>経費判定</TableCell>
                <TableCell>備考</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {categories.map((c) => (
                <TableRow key={c.id}>
                  <TableCell>{c.name}</TableCell>
                  <TableCell>
                    <Chip
                      label={c.is_expense ? '経費' : '経費外'}
                      size="small"
                      color={c.is_expense ? 'success' : 'default'}
                    />
                  </TableCell>
                  <TableCell>{c.note || '-'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TabPanel>
      </Card>

      {/* 経費追加ダイアログ */}
      <Dialog open={expenseOpen} onClose={() => setExpenseOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>経費を追加</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
            <TextField
              label="日付"
              type="date"
              value={expenseForm.date}
              onChange={(e) => setExpenseForm({ ...expenseForm, date: e.target.value })}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
            <TextField
              select
              label="カテゴリ"
              value={expenseForm.category_id}
              onChange={(e) => setExpenseForm({ ...expenseForm, category_id: e.target.value })}
              SelectProps={{ native: true }}
              fullWidth
            >
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}{c.is_expense ? '' : '（経費外）'}
                </option>
              ))}
            </TextField>
            <TextField
              label="金額"
              type="number"
              value={expenseForm.amount || ''}
              onChange={(e) => setExpenseForm({ ...expenseForm, amount: parseInt(e.target.value) || 0 })}
              fullWidth
            />
            <TextField
              label="内容"
              value={expenseForm.description}
              onChange={(e) => setExpenseForm({ ...expenseForm, description: e.target.value })}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setExpenseOpen(false)}>キャンセル</Button>
          <Button variant="contained" onClick={handleAddExpense} disabled={expenseForm.amount <= 0}>
            登録
          </Button>
        </DialogActions>
      </Dialog>

      {/* 売上追加ダイアログ */}
      <Dialog open={incomeOpen} onClose={() => setIncomeOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>売上を追加</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
            <TextField
              label="日付"
              type="date"
              value={incomeForm.date}
              onChange={(e) => setIncomeForm({ ...incomeForm, date: e.target.value })}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
            <TextField
              label="金額"
              type="number"
              value={incomeForm.amount || ''}
              onChange={(e) => setIncomeForm({ ...incomeForm, amount: parseInt(e.target.value) || 0 })}
              fullWidth
            />
            <TextField
              label="内容"
              value={incomeForm.description}
              onChange={(e) => setIncomeForm({ ...incomeForm, description: e.target.value })}
              fullWidth
            />
            <TextField
              label="取引先"
              value={incomeForm.client_name}
              onChange={(e) => setIncomeForm({ ...incomeForm, client_name: e.target.value })}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIncomeOpen(false)}>キャンセル</Button>
          <Button variant="contained" onClick={handleAddIncome} disabled={incomeForm.amount <= 0}>
            登録
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
