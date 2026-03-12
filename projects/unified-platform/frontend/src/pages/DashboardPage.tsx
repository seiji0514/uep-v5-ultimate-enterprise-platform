/**
 * 統合ダッシュボード - 3ドメイン横断KPI・アラート・グラフ・ウィジェット（カスタマイズ可能）
 */
import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Grid, Chip, Alert, IconButton, Button, FormControlLabel, Switch, Collapse, List, ListItem, ListItemText, Checkbox } from '@mui/material';
import { LocalHospital, Flight, Satellite, Warning, Refresh, PictureAsPdf, Settings, ArrowUpward, ArrowDownward, ChevronRight, WbSunny, CalendarMonth, CheckCircle } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { downloadPdfReport } from '../utils/exportPdf';
import { useToast } from '../contexts/ToastContext';
import { useDashboard, type WidgetId } from '../contexts/DashboardContext';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { unifiedApi } from '../api/unified';

const TODO_STORAGE = 'uep_dashboard_todo';

interface DashboardPageProps {
  unified: { medical_patients: number; aviation_flights: number; space_satellites: number } | null;
  medical?: { patients?: any[]; ai?: any[]; vital?: any[] };
  aviation?: { flights?: any[]; airports?: any[] };
  space?: { satellites?: any[]; launches?: any[] };
  error: string;
  onRefresh?: () => void;
}

const WIDGET_LABELS: Record<WidgetId, string> = { kpi: 'KPIカード', chart: 'グラフ', alerts: 'アラート', weather: '天気', calendar: 'カレンダー', todo: 'TODO' };

export const DashboardPage: React.FC<DashboardPageProps> = ({ unified, medical, aviation, space, error, onRefresh }) => {
  const toast = useToast();
  const navigate = useNavigate();
  const { layout, setWidgetVisible, moveWidget, resetLayout } = useDashboard();
  const [showSettings, setShowSettings] = React.useState(false);
  const [weather, setWeather] = useState<{ city?: string; temp?: number; desc?: string } | null>(null);
  const [calendar, setCalendar] = useState<{ today?: string; weekday?: string } | null>(null);
  const [todos, setTodos] = useState<{ id: string; text: string; done: boolean }[]>(() => {
    try {
      const s = localStorage.getItem(TODO_STORAGE);
      return s ? JSON.parse(s) : [];
    } catch { return []; }
  });

  useEffect(() => {
    unifiedApi.widgets.weather().then(r => setWeather(r.data)).catch(() => {});
    unifiedApi.widgets.calendar().then(r => setCalendar(r.data)).catch(() => {});
  }, []);

  useEffect(() => {
    localStorage.setItem(TODO_STORAGE, JSON.stringify(todos));
  }, [todos]);

  const addTodo = (text: string) => {
    if (!text.trim()) return;
    setTodos(prev => [...prev, { id: Date.now().toString(), text: text.trim(), done: false }]);
  };
  const toggleTodo = (id: string) => setTodos(prev => prev.map(t => t.id === id ? { ...t, done: !t.done } : t));

  const handleRefresh = () => {
    onRefresh?.();
    toast.show('データを更新しました', 'success');
  };
  const alerts = [
    { id: 1, severity: 'info' as const, msg: 'Medical: AI診断 2件 レビュー待ち' },
    { id: 2, severity: 'success' as const, msg: 'Aviation: 定時率 92%' },
    { id: 3, severity: 'info' as const, msg: 'Space: ISS 軌道正常' },
  ];

  const data = [
    { name: 'Medical', value: unified?.medical_patients ?? 0, fill: '#22c55e' },
    { name: 'Aviation', value: unified?.aviation_flights ?? 0, fill: '#3b82f6' },
    { name: 'Space', value: unified?.space_satellites ?? 0, fill: '#8b5cf6' },
  ];

  return (
    <Box component="section" sx={{ minHeight: 400, width: '100%', display: 'block', pt: 1 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
        <Typography variant="h5" fontWeight={600}>
          統合ダッシュボード
        </Typography>
        {onRefresh && <IconButton onClick={handleRefresh} size="small" aria-label="データを更新"><Refresh /></IconButton>}
        <Button size="small" startIcon={<PictureAsPdf />} aria-label="PDFレポートをダウンロード" onClick={() => downloadPdfReport({
          title: '統合基盤 Report',
          generatedAt: new Date().toLocaleString('ja-JP'),
          medical: { patients: medical?.patients?.length ?? unified?.medical_patients ?? 0, ai: medical?.ai?.length ?? 0, vitals: medical?.vital?.length ?? 0 },
          aviation: { flights: aviation?.flights?.length ?? unified?.aviation_flights ?? 0, airports: aviation?.airports?.length ?? 0 },
          space: { satellites: space?.satellites?.length ?? unified?.space_satellites ?? 0, launches: space?.launches?.length ?? 0 },
        })}>PDF</Button>
      </Box>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        医療・航空・宇宙の横断KPIとアラート（Ctrl+R で更新・WebSocketでリアルタイム）
      </Typography>
      <IconButton size="small" onClick={() => setShowSettings(!showSettings)} aria-label="レイアウト設定"><Settings /></IconButton>
      <Collapse in={showSettings}>
        <Paper elevation={0} sx={{ p: 2, mb: 2, bgcolor: 'action.hover' }}>
          <Typography variant="subtitle2" gutterBottom>ウィジェット表示・並び順</Typography>
          {layout.order.map((id, i) => (
            <Box key={id} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <FormControlLabel control={<Switch checked={layout.visible[id]} onChange={(_, v) => setWidgetVisible(id, v)} size="small" />} label={WIDGET_LABELS[id]} />
              <IconButton size="small" onClick={() => moveWidget(i, Math.max(0, i - 1))} disabled={i === 0}><ArrowUpward fontSize="small" /></IconButton>
              <IconButton size="small" onClick={() => moveWidget(i, Math.min(layout.order.length - 1, i + 1))} disabled={i === layout.order.length - 1}><ArrowDownward fontSize="small" /></IconButton>
            </Box>
          ))}
          <Button size="small" onClick={resetLayout}>リセット</Button>
        </Paper>
      </Collapse>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      {/* KPI カード（クリックで各ドメインへ） */}
      {layout.visible.kpi && (
      <Grid container spacing={3} style={{ order: layout.order.indexOf('kpi') + 1 }}>
        <Grid item xs={12} sm={4}>
          <Paper elevation={0} sx={{ p: 2, height: '100%', cursor: 'pointer', '&:hover': { borderColor: 'success.main', bgcolor: 'action.hover' } }} onClick={() => navigate('/medical')}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocalHospital color="success" />
                <Typography variant="subtitle2">Medical</Typography>
              </Box>
              <ChevronRight fontSize="small" color="action" />
            </Box>
            <Typography variant="h4" fontWeight={700} color="success.main">
              {unified?.medical_patients ?? '-'}
            </Typography>
            <Typography variant="caption" color="text.secondary">アクティブ患者</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Paper elevation={0} sx={{ p: 2, height: '100%', cursor: 'pointer', '&:hover': { borderColor: 'info.main', bgcolor: 'action.hover' } }} onClick={() => navigate('/aviation')}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Flight color="info" />
                <Typography variant="subtitle2">Aviation</Typography>
              </Box>
              <ChevronRight fontSize="small" color="action" />
            </Box>
            <Typography variant="h4" fontWeight={700} color="info.main">
              {unified?.aviation_flights ?? '-'}
            </Typography>
            <Typography variant="caption" color="text.secondary">本日フライト</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Paper elevation={0} sx={{ p: 2, height: '100%', cursor: 'pointer', '&:hover': { borderColor: 'secondary.main', bgcolor: 'action.hover' } }} onClick={() => navigate('/space')}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Satellite color="secondary" />
                <Typography variant="subtitle2">Space</Typography>
              </Box>
              <ChevronRight fontSize="small" color="action" />
            </Box>
            <Typography variant="h4" fontWeight={700} color="secondary.main">
              {unified?.space_satellites ?? '-'}
            </Typography>
            <Typography variant="caption" color="text.secondary">追跡衛星</Typography>
          </Paper>
        </Grid>
      </Grid>
      )}

      {/* KPI グラフ */}
      {layout.visible.chart && (
      <Paper elevation={0} sx={{ p: 3, minHeight: 220 }} style={{ order: layout.order.indexOf('chart') + 1 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>ドメイン別サマリ</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={8}>
            <Box sx={{ width: '100%', height: 200, minHeight: 200, minWidth: 100 }}>
              <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey="name" stroke="#9e9e9e" />
            <YAxis stroke="#9e9e9e" />
            <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #2d2d2d' }} />
            <Bar dataKey="value" radius={[4, 4, 0, 0]} />
          </BarChart>
              </ResponsiveContainer>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ width: '100%', height: 200, minHeight: 200, minWidth: 100 }}>
              <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={40} outerRadius={70} label>
              <Cell fill="#22c55e" /><Cell fill="#3b82f6" /><Cell fill="#8b5cf6" />
            </Pie>
            <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', border: '1px solid #2d2d2d' }} />
          </PieChart>
              </ResponsiveContainer>
            </Box>
          </Grid>
        </Grid>
      </Paper>
      )}

      {/* アラートパネル */}
      {layout.visible.alerts && (
      <Paper elevation={0} sx={{ p: 3 }} style={{ order: layout.order.indexOf('alerts') }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Warning fontSize="small" /> アラート・通知
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
          {alerts.map((a) => (
            <Chip key={a.id} label={a.msg} color={a.severity} size="small" variant="outlined" />
          ))}
        </Box>
      </Paper>
      )}

      {/* 天気ウィジェット */}
      {layout.visible.weather && (
      <Paper elevation={0} sx={{ p: 3 }} style={{ order: layout.order.indexOf('weather') + 1 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <WbSunny fontSize="small" /> 天気
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography variant="h5">{weather?.temp ?? '-'}°C</Typography>
          <Box>
            <Typography variant="body2">{weather?.city ?? 'Tokyo'}</Typography>
            <Typography variant="caption" color="text.secondary">{weather?.desc ?? '取得中...'}</Typography>
          </Box>
        </Box>
      </Paper>
      )}

      {/* カレンダーウィジェット */}
      {layout.visible.calendar && (
      <Paper elevation={0} sx={{ p: 3 }} style={{ order: layout.order.indexOf('calendar') + 1 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CalendarMonth fontSize="small" /> カレンダー
        </Typography>
        <Typography variant="h6">{calendar?.today ?? new Date().toISOString().slice(0, 10)}</Typography>
        <Typography variant="body2" color="text.secondary">{calendar?.weekday ?? ''}</Typography>
      </Paper>
      )}

      {/* TODOウィジェット */}
      {layout.visible.todo && (
      <Paper elevation={0} sx={{ p: 3 }} style={{ order: layout.order.indexOf('todo') + 1 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CheckCircle fontSize="small" /> TODO
        </Typography>
        <List dense>
          {todos.slice(0, 5).map((t) => (
            <ListItem key={t.id} dense>
              <Checkbox size="small" checked={t.done} onChange={() => toggleTodo(t.id)} />
              <ListItemText primary={t.text} sx={{ textDecoration: t.done ? 'line-through' : 'none' }} />
            </ListItem>
          ))}
        </List>
        <Button size="small" onClick={() => addTodo(prompt('TODOを追加') || '')}>追加</Button>
      </Paper>
      )}

      {/* クイックプレビュー（各ドメインの直近データ） */}
      <Paper elevation={0} sx={{ p: 3 }} style={{ order: 10 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>クイックプレビュー</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Paper elevation={0} sx={{ p: 1.5, cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }} onClick={() => navigate('/medical')}>
              <Typography variant="caption" color="text.secondary">医療</Typography>
              {(medical?.patients ?? []).slice(0, 3).map((p: any) => (
                <Typography key={p.id} variant="body2" sx={{ display: 'block', mt: 0.5 }}>{[p.family_name, p.given_name].filter(Boolean).join(' ') || p.identifier || p.id}</Typography>
              ))}
              {(!medical?.patients?.length) && <Typography variant="body2" color="text.secondary">データなし</Typography>}
              <Button size="small" endIcon={<ChevronRight />} sx={{ mt: 1 }}>詳細</Button>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={0} sx={{ p: 1.5, cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }} onClick={() => navigate('/aviation')}>
              <Typography variant="caption" color="text.secondary">航空</Typography>
              {(aviation?.flights ?? []).slice(0, 3).map((f: any) => (
                <Typography key={f.flight_id ?? f.id} variant="body2" sx={{ display: 'block', mt: 0.5 }}>{f.flight_id ?? f.id} {f.route ?? ''}</Typography>
              ))}
              {(!aviation?.flights?.length) && <Typography variant="body2" color="text.secondary">データなし</Typography>}
              <Button size="small" endIcon={<ChevronRight />} sx={{ mt: 1 }}>詳細</Button>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={0} sx={{ p: 1.5, cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }} onClick={() => navigate('/space')}>
              <Typography variant="caption" color="text.secondary">宇宙</Typography>
              {(space?.satellites ?? []).slice(0, 3).map((s: any) => (
                <Typography key={s.id} variant="body2" sx={{ display: 'block', mt: 0.5 }}>{s.name ?? s.id}</Typography>
              ))}
              {(!space?.satellites?.length) && <Typography variant="body2" color="text.secondary">データなし</Typography>}
              <Button size="small" endIcon={<ChevronRight />} sx={{ mt: 1 }}>詳細</Button>
            </Paper>
          </Grid>
        </Grid>
      </Paper>
      </Box>
    </Box>
  );
};
