/**
 * 宇宙ページ - サブタブ（追跡 / Satellites / Launches）+ 詳細ビュー
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
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  TextField,
  InputAdornment,
  Button,
} from '@mui/material';
import { TrackChanges, Satellite, RocketLaunch, Close, Search, Download, ThreeDRotation, Image } from '@mui/icons-material';
import { SpaceTrackingPanel } from '../components/SpaceTrackingPanel';
import { SpaceOrbit3D } from '../components/SpaceOrbit3D';
import { downloadCsv } from '../utils/exportCsv';
import { useToast } from '../contexts/ToastContext';

function TabPanel({ children, value, index }: { children: React.ReactNode; value: number; index: number }) {
  return <div hidden={value !== index}>{value === index && <Box sx={{ pt: 2 }}>{children}</Box>}</div>;
}

interface SpacePageProps {
  satellites: any[];
  launches: any[];
  apod?: { title?: string; explanation?: string; url?: string; date?: string; media_type?: string };
}

function orbitType(km: number): string {
  if (km < 2000) return 'LEO';
  if (km < 36000) return 'MEO';
  return 'GEO';
}

function countdownTo(dateStr: string): string {
  const d = new Date(dateStr);
  const now = new Date();
  if (d <= now) return '打ち上げ済';
  const diff = d.getTime() - now.getTime();
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor((diff % 86400000) / 3600000);
  const mins = Math.floor((diff % 3600000) / 60000);
  if (days > 0) return `${days}日 ${hours}時間 ${mins}分`;
  if (hours > 0) return `${hours}時間 ${mins}分`;
  return `${mins}分`;
}

export const SpacePage: React.FC<SpacePageProps> = ({ satellites, launches, apod }) => {
  const [subTab, setSubTab] = useState(0);
  const [selectedSat, setSelectedSat] = useState<any | null>(null);
  const [selectedLaunch, setSelectedLaunch] = useState<any | null>(null);
  const [search, setSearch] = useState('');
  const toast = useToast();

  const filteredSats = useMemo(() => {
    if (!search.trim()) return satellites || [];
    const q = search.toLowerCase();
    return (satellites || []).filter((r: any) => (r.id + r.name + r.status).toLowerCase().includes(q));
  }, [satellites, search]);

  return (
    <Box component="section" sx={{ minHeight: 400, width: '100%', display: 'block', pt: 1 }}>
      <Typography variant="h5" fontWeight={600} gutterBottom>宇宙</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        衛星追跡（LEO/MEO/GEO）・打ち上げマニフェスト・ミッション管理
      </Typography>
      <Paper elevation={0}>
        <Tabs value={subTab} onChange={(_, v) => setSubTab(v)}>
          <Tab icon={<TrackChanges />} iconPosition="start" label="追跡" />
          <Tab icon={<ThreeDRotation />} iconPosition="start" label="3D軌道" />
          <Tab icon={<Satellite />} iconPosition="start" label="Satellites" />
          <Tab icon={<RocketLaunch />} iconPosition="start" label="Launches" />
          <Tab icon={<Image />} iconPosition="start" label="APOD" />
        </Tabs>
        <Box sx={{ p: 2 }}>
          <TabPanel value={subTab} index={0}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ color: '#00d4ff' }}>MISSION CONTROL | SATELLITE TRACKING</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              衛星の軌道・位置を可視化。LEO（低軌道）、MEO、GEO（静止軌道）を色分け表示。
            </Typography>
            <SpaceTrackingPanel satellites={satellites || []} launches={launches || []} />
          </TabPanel>
          <TabPanel value={subTab} index={1}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ color: '#00d4ff' }}>3D ORBIT VISUALIZATION</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              衛星軌道をThree.jsで3D表示。LEO=緑/MEO=シアン/GEO=琥珀。
            </Typography>
            <SpaceOrbit3D satellites={satellites || []} />
          </TabPanel>
          <TabPanel value={subTab} index={2}>
            <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
              <TextField size="small" placeholder="検索 (ID・名前・ステータス)" value={search} onChange={(e) => setSearch(e.target.value)} InputProps={{ startAdornment: <InputAdornment position="start"><Search fontSize="small" /></InputAdornment> }} sx={{ minWidth: 220 }} />
              <Button size="small" startIcon={<Download />} onClick={() => { downloadCsv(filteredSats, 'space_satellites.csv'); toast.show('CSVをダウンロードしました'); }}>CSV</Button>
            </Box>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
              <Paper elevation={0} sx={{ p: 1.5 }}><Typography variant="body2" color="success.main">{satellites?.length ?? 0}</Typography><Typography variant="caption">追跡中</Typography></Paper>
              <Paper elevation={0} sx={{ p: 1.5 }}><Typography variant="body2" color="info.main">{launches?.filter((l: any) => l.status === 'Scheduled').length ?? 0}</Typography><Typography variant="caption">予定打ち上げ</Typography></Paper>
            </Box>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>Satellites</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              軌道高度・傾斜角・周期。LEO（&lt;2000km）、MEO、GEO（静止）で軌道種別を表示。行クリックで詳細。
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead><TableRow><TableCell>ID</TableCell><TableCell>Name</TableCell><TableCell>Orbit (km)</TableCell><TableCell>Type</TableCell><TableCell>Incl.</TableCell><TableCell>Period</TableCell><TableCell>Status</TableCell><TableCell></TableCell></TableRow></TableHead>
                <TableBody>
                  {filteredSats.map((r: any) => (
                    <TableRow key={r.id} hover sx={{ cursor: 'pointer' }} onClick={() => setSelectedSat(r)}>
                      <TableCell>{r.id}</TableCell><TableCell>{r.name}</TableCell><TableCell>{r.orbit_km}</TableCell><TableCell><Chip size="small" label={orbitType(r.orbit_km || 0)} variant="outlined" /></TableCell><TableCell>{r.inclination ?? '-'}°</TableCell><TableCell>{r.period_min ?? '-'}min</TableCell><TableCell><Chip size="small" label={r.status} color="success" /></TableCell><TableCell>詳細</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>
          <TabPanel value={subTab} index={3}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>Launches</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              打ち上げ予定・完了ミッション。ロケット・日付・ステータス。行クリックで詳細表示。
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
              <Paper elevation={0} sx={{ p: 1.5 }}><Typography variant="body2" color="info.main">{launches?.filter((l: any) => l.status === 'Scheduled').length ?? 0}</Typography><Typography variant="caption">予定</Typography></Paper>
              <Paper elevation={0} sx={{ p: 1.5 }}><Typography variant="body2" color="success.main">{launches?.filter((l: any) => l.status === 'Completed').length ?? 0}</Typography><Typography variant="caption">完了</Typography></Paper>
            </Box>
            <TableContainer>
              <Table size="small">
                <TableHead><TableRow><TableCell>ID</TableCell><TableCell>Mission</TableCell><TableCell>Date</TableCell><TableCell>Countdown</TableCell><TableCell>Vehicle</TableCell><TableCell>Status</TableCell><TableCell></TableCell></TableRow></TableHead>
                <TableBody>
                  {(launches || []).map((r: any) => (
                    <TableRow key={r.id} hover sx={{ cursor: 'pointer' }} onClick={() => setSelectedLaunch(r)}><TableCell>{r.id}</TableCell><TableCell>{r.mission}</TableCell><TableCell>{r.date}</TableCell><TableCell><Typography variant="caption" color={r.status === 'Scheduled' ? 'primary' : 'text.secondary'}>{countdownTo(r.date)}</Typography></TableCell><TableCell>{r.vehicle}</TableCell><TableCell><Chip size="small" label={r.status} color={r.status === 'Completed' ? 'success' : 'default'} /></TableCell><TableCell>詳細</TableCell></TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>
          <TabPanel value={subTab} index={4}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>NASA Astronomy Picture of the Day</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              NASA_API_KEY を環境変数に設定すると実画像を表示。未設定時はサンプル表示。
            </Typography>
            {apod?.url ? (
              <Box sx={{ maxWidth: 600 }}>
                <img src={apod.url} alt={apod.title} style={{ width: '100%', borderRadius: 8 }} />
                <Typography variant="subtitle2" sx={{ mt: 1 }}>{apod.title}</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>{apod.explanation?.slice(0, 200)}...</Typography>
                <Typography variant="caption" color="text.secondary">{apod.date}</Typography>
              </Box>
            ) : (
              <Paper elevation={0} sx={{ p: 3, bgcolor: 'action.hover' }}>
                <Typography variant="body2" color="text.secondary">{apod?.explanation || 'NASA APOD を表示するには、バックエンドの環境変数に NASA_API_KEY を設定してください。'}</Typography>
                <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>https://api.nasa.gov で無料APIキー取得</Typography>
              </Paper>
            )}
          </TabPanel>
        </Box>
      </Paper>

      {/* 打ち上げ詳細ダイアログ */}
      <Dialog open={!!selectedLaunch} onClose={() => setSelectedLaunch(null)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          打ち上げ詳細
          <IconButton onClick={() => setSelectedLaunch(null)}><Close /></IconButton>
        </DialogTitle>
        <DialogContent>
          {selectedLaunch && (
            <Box sx={{ display: 'grid', gap: 1 }}>
              <Typography><strong>ミッションID:</strong> {selectedLaunch.id}</Typography>
              <Typography><strong>ミッション:</strong> {selectedLaunch.mission}</Typography>
              <Typography><strong>打ち上げ日:</strong> {selectedLaunch.date}</Typography>
              {selectedLaunch.status === 'Scheduled' && <Typography><strong>カウントダウン:</strong> <Typography component="span" color="primary" fontWeight={600}>{countdownTo(selectedLaunch.date)}</Typography></Typography>}
              <Typography><strong>ロケット:</strong> {selectedLaunch.vehicle}</Typography>
              <Typography><strong>ステータス:</strong> <Chip size="small" label={selectedLaunch.status} color={selectedLaunch.status === 'Completed' ? 'success' : 'default'} /></Typography>
            </Box>
          )}
        </DialogContent>
      </Dialog>

      {/* 衛星詳細ダイアログ */}
      <Dialog open={!!selectedSat} onClose={() => setSelectedSat(null)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          衛星詳細
          <IconButton onClick={() => setSelectedSat(null)}><Close /></IconButton>
        </DialogTitle>
        <DialogContent>
          {selectedSat && (
            <Box sx={{ display: 'grid', gap: 1 }}>
              <Typography><strong>ID:</strong> {selectedSat.id}</Typography>
              <Typography><strong>Name:</strong> {selectedSat.name}</Typography>
              <Typography><strong>軌道高度:</strong> {selectedSat.orbit_km} km</Typography>
              <Typography><strong>軌道種別:</strong> <Chip size="small" label={orbitType(selectedSat.orbit_km || 0)} variant="outlined" /></Typography>
              <Typography><strong>傾斜角:</strong> {selectedSat.inclination ?? '-'}°</Typography>
              <Typography><strong>周期:</strong> {selectedSat.period_min ?? '-'} min</Typography>
              <Typography><strong>ステータス:</strong> <Chip size="small" label={selectedSat.status} /></Typography>
            </Box>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
};
