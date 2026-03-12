/**
 * 航空ページ - サブタブ（レーダー / Flights / Airports / Delays）+ 詳細ビュー
 */
import React, { useState, useMemo } from 'react';
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  TextField,
  InputAdornment,
  Button,
} from '@mui/material';
import { Radar, FlightTakeoff, FlightLand, Schedule, Close, Search, Download, Upload, Map } from '@mui/icons-material';
import { AviationRadarPanel } from '../components/AviationRadarPanel';
import { AviationFlightMap } from '../components/AviationFlightMap';
import { AirportMatrix } from '../components/AviationAirportMatrix';
import { downloadCsv } from '../utils/exportCsv';
import { downloadJson } from '../utils/exportJson';
import { downloadExcel } from '../utils/exportExcel';
import { useToast } from '../contexts/ToastContext';
import { useSettings } from '../contexts/SettingsContext';

function TabPanel({ children, value, index }: { children: React.ReactNode; value: number; index: number }) {
  return <div hidden={value !== index}>{value === index && <Box sx={{ pt: 2 }}>{children}</Box>}</div>;
}

interface AviationPageProps {
  flights: any[];
  airports: any[];
  delays?: any;
  delayPrediction?: { risk_score?: number; level?: string; weather?: string; weather_risk?: number; congestion_risk?: number };
  onRefresh?: () => void;
}

export const AviationPage: React.FC<AviationPageProps> = ({ flights, airports, delays, delayPrediction, onRefresh }) => {
  const { settings } = useSettings();
  const [subTab, setSubTab] = useState(0);
  const [selectedFlight, setSelectedFlight] = useState<any | null>(null);
  const [selectedAirport, setSelectedAirport] = useState<any | null>(null);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(settings.itemsPerPage);
  const toast = useToast();

  const filteredFlights = useMemo(() => {
    if (!search.trim()) return flights || [];
    const q = search.toLowerCase();
    return (flights || []).filter((r: any) => (r.flight_id + r.route + r.status).toLowerCase().includes(q));
  }, [flights, search]);

  const paginatedFlights = useMemo(() => {
    const list = filteredFlights;
    const start = page * rowsPerPage;
    return list.slice(start, start + rowsPerPage);
  }, [filteredFlights, page, rowsPerPage]);

  return (
    <Box component="section" sx={{ minHeight: 400, width: '100%', display: 'block', pt: 1 }}>
      <Typography variant="h5" fontWeight={600} gutterBottom>航空</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        ATCレーダー・フライトスケジュール・空港混雑・遅延状況の一元管理
      </Typography>
      <Paper elevation={0}>
        <Tabs value={subTab} onChange={(_, v) => setSubTab(v)}>
          <Tab icon={<Radar />} iconPosition="start" label="レーダー" />
          <Tab icon={<Map />} iconPosition="start" label="経路" />
          <Tab icon={<FlightTakeoff />} iconPosition="start" label="Flights" />
          <Tab icon={<FlightLand />} iconPosition="start" label="Airports" />
          <Tab icon={<Schedule />} iconPosition="start" label="Delays" />
        </Tabs>
        <Box sx={{ p: 2 }}>
          <TabPanel value={subTab} index={0}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ color: '#00ff41' }}>ATC RADAR DISPLAY</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              管制レーダー表示。便の位置・空港との関係を可視化します。
            </Typography>
            <AviationRadarPanel flights={flights || []} airports={airports || []} />
          </TabPanel>
          <TabPanel value={subTab} index={1}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>フライト経路マップ</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              出発・到着空港を地図上にプロット。ルートを線で表示。
            </Typography>
            <AviationFlightMap flights={flights || []} />
          </TabPanel>
          <TabPanel value={subTab} index={2}>
            <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
              <TextField size="small" placeholder="検索 (便名・ルート・ステータス)" value={search} onChange={(e) => setSearch(e.target.value)} InputProps={{ startAdornment: <InputAdornment position="start"><Search fontSize="small" /></InputAdornment> }} sx={{ minWidth: 220 }} />
              <Button size="small" startIcon={<Download />} onClick={() => { downloadCsv(filteredFlights, 'aviation_flights.csv'); toast.show('CSVをダウンロードしました'); }}>CSV</Button>
              <Button size="small" startIcon={<Download />} onClick={() => { downloadExcel(filteredFlights, 'aviation_flights.xlsx'); toast.show('Excelをダウンロードしました'); }}>Excel</Button>
              <Button size="small" startIcon={<Download />} onClick={() => { downloadJson(filteredFlights, 'aviation_flights.json'); toast.show('JSONをダウンロードしました'); }}>JSON</Button>
              <Button size="small" component="label" startIcon={<Upload />}>CSVインポート<input type="file" accept=".csv" hidden onChange={async (e) => { const f = e.target.files?.[0]; if (!f) return; try { const { unifiedApi } = await import('../api/unified'); const r = await unifiedApi.aviation.importFlightsCsv(f); toast.show(`${r.data.imported}件をインポートしました`, 'success'); onRefresh?.(); } catch (err: any) { toast.show(err?.response?.data?.detail || 'インポートに失敗しました', 'error'); } e.target.value = ''; }} /></Button>
            </Box>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>Flights</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              本日のフライト一覧。便名・ルート・出発/到着時刻・ステータス。行クリックで詳細表示。
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead><TableRow><TableCell>Flight</TableCell><TableCell>Route</TableCell><TableCell>Departure</TableCell><TableCell>Arrival</TableCell><TableCell>Status</TableCell><TableCell></TableCell></TableRow></TableHead>
                <TableBody>
                  {paginatedFlights.map((r: any) => (
                    <TableRow key={r.flight_id} hover sx={{ cursor: 'pointer' }} onClick={() => setSelectedFlight(r)}>
                      <TableCell>{r.flight_id}</TableCell><TableCell>{r.route}</TableCell><TableCell>{r.departure}</TableCell><TableCell>{r.arrival}</TableCell><TableCell><Chip size="small" label={r.status} /></TableCell><TableCell>詳細</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              component="div"
              count={filteredFlights.length}
              page={page}
              onPageChange={(_, p) => setPage(p)}
              rowsPerPage={rowsPerPage}
              onRowsPerPageChange={(e) => { setRowsPerPage(parseInt(e.target.value, 10)); setPage(0); }}
              rowsPerPageOptions={[5, 10, 25, 50]}
              labelRowsPerPage="表示件数:"
              labelDisplayedRows={({ from, to, count }) => `${from}-${to} / ${count}`}
            />
          </TabPanel>
          <TabPanel value={subTab} index={3}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>Airports</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              空港別の本日出発/到着便数・混雑度・気象。行クリックで詳細表示。
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead><TableRow><TableCell>Code</TableCell><TableCell>Departures</TableCell><TableCell>Arrivals</TableCell><TableCell>Congestion</TableCell><TableCell>Weather</TableCell><TableCell></TableCell></TableRow></TableHead>
                <TableBody>
                  {(airports || []).map((r: any) => (
                    <TableRow key={r.airport} hover sx={{ cursor: 'pointer' }} onClick={() => setSelectedAirport(r)}><TableCell>{r.airport}</TableCell><TableCell>{r.departures_today}</TableCell><TableCell>{r.arrivals_today}</TableCell><TableCell><Chip size="small" label={r.congestion} color={r.congestion === 'High' ? 'warning' : 'default'} /></TableCell><TableCell>{r.weather ?? '-'}</TableCell><TableCell>詳細</TableCell></TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>
          <TabPanel value={subTab} index={4}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>Delays</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              定時率・平均遅延時間・本日遅延便数。ステータス別の内訳を表示。
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
              <Paper elevation={0} sx={{ p: 2, minWidth: 140 }}><Typography variant="h6" color="success.main">{((delays as any)?.on_time_rate ?? 0.92) * 100}%</Typography><Typography variant="caption">定時率</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 140 }}><Typography variant="h6" color="info.main">{(delays as any)?.avg_delay_minutes ?? 8}分</Typography><Typography variant="caption">平均遅延</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 140 }}><Typography variant="h6" color="warning.main">{(delays as any)?.delayed_flights_today ?? 12}</Typography><Typography variant="caption">本日遅延便</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 140 }}><Typography variant="h6" color={delayPrediction?.level === 'high' ? 'error' : delayPrediction?.level === 'medium' ? 'warning' : 'success'}>{delayPrediction?.risk_score ?? '?'}</Typography><Typography variant="caption">遅延予測スコア</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 140 }}><Typography variant="body2" color="text.secondary">{delayPrediction?.weather ?? '-'}</Typography><Typography variant="caption">天候（東京）</Typography></Paper>
            </Box>
            {delayPrediction && <Typography variant="caption" color="text.secondary">天候: {delayPrediction.weather_risk ?? 0}pt / 混雑: {delayPrediction.congestion_risk ?? 0}pt → リスク{delayPrediction.level === 'high' ? '高' : delayPrediction.level === 'medium' ? '中' : '低'}</Typography>}
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>ステータス別: OnTime {(flights || []).filter((f: any) => f.status === 'OnTime').length} / Delayed {(flights || []).filter((f: any) => f.status === 'Delayed').length} / Boarding {(flights || []).filter((f: any) => f.status === 'Boarding').length}</Typography>
            <Typography variant="subtitle2" fontWeight={600} gutterBottom sx={{ mt: 2 }}>空港間便数マトリクス</Typography>
            <AirportMatrix flights={flights || []} />
          </TabPanel>
        </Box>
      </Paper>

      {/* 空港詳細ダイアログ */}
      <Dialog open={!!selectedAirport} onClose={() => setSelectedAirport(null)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          空港詳細
          <IconButton onClick={() => setSelectedAirport(null)}><Close /></IconButton>
        </DialogTitle>
        <DialogContent>
          {selectedAirport && (
            <Box sx={{ display: 'grid', gap: 1 }}>
              <Typography><strong>空港コード:</strong> {selectedAirport.airport}</Typography>
              <Typography><strong>本日出発便:</strong> {selectedAirport.departures_today} 便</Typography>
              <Typography><strong>本日到着便:</strong> {selectedAirport.arrivals_today} 便</Typography>
              <Typography><strong>混雑度:</strong> <Chip size="small" label={selectedAirport.congestion} color={selectedAirport.congestion === 'High' ? 'warning' : 'default'} /></Typography>
              <Typography><strong>気象:</strong> {selectedAirport.weather ?? '-'}</Typography>
            </Box>
          )}
        </DialogContent>
      </Dialog>

      {/* 便詳細ダイアログ */}
      <Dialog open={!!selectedFlight} onClose={() => setSelectedFlight(null)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          便詳細
          <IconButton onClick={() => setSelectedFlight(null)}><Close /></IconButton>
        </DialogTitle>
        <DialogContent>
          {selectedFlight && (
            <Box sx={{ display: 'grid', gap: 1 }}>
              <Typography><strong>便名:</strong> {selectedFlight.flight_id}</Typography>
              <Typography><strong>ルート:</strong> {selectedFlight.route}</Typography>
              <Typography><strong>出発:</strong> {selectedFlight.departure}</Typography>
              <Typography><strong>到着:</strong> {selectedFlight.arrival}</Typography>
              <Typography><strong>ステータス:</strong> <Chip size="small" label={selectedFlight.status} /></Typography>
              {selectedFlight.aircraft && <Typography><strong>機材:</strong> {selectedFlight.aircraft}</Typography>}
            </Box>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
};
