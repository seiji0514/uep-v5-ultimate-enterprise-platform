/**
 * 医療ページ - サブタブ（患者一覧 / AI診断 / バイタルモニター / ベッドマップ / サマリ）
 */
import React, { useState, useMemo } from 'react';
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  TableCell,
  Table,
  TableBody,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  TextField,
  InputAdornment,
  Button,
  LinearProgress,
} from '@mui/material';
import { People, Psychology, MonitorHeart, Summarize, GridView, Search, Download, Upload, Timeline } from '@mui/icons-material';
import { MedicalVitalMonitor } from '../components/MedicalVitalMonitor';
import { MedicalBedMap } from '../components/MedicalBedMap';
import { MedicalPatientTimeline } from '../components/MedicalPatientTimeline';
import { SortableTable } from '../components/SortableTable';
import { downloadCsv } from '../utils/exportCsv';
import { downloadJson } from '../utils/exportJson';
import { downloadExcel } from '../utils/exportExcel';
import { useToast } from '../contexts/ToastContext';
import { useSettings } from '../contexts/SettingsContext';

function TabPanel({ children, value, index }: { children: React.ReactNode; value: number; index: number }) {
  return <div hidden={value !== index}>{value === index && <Box sx={{ pt: 2 }}>{children}</Box>}</div>;
}

interface MedicalPageProps {
  patients?: any[];
  ai: any[];
  vital: any[];
  onRefresh?: () => void;
}

export const MedicalPage: React.FC<MedicalPageProps> = ({ patients = [], ai, vital, onRefresh }) => {
  const { settings } = useSettings();
  const [subTab, setSubTab] = useState(0);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(settings.itemsPerPage);
  const toast = useToast();

  const paginatedPatients = useMemo(() => {
    const list = patients || [];
    const start = page * rowsPerPage;
    return list.slice(start, start + rowsPerPage);
  }, [patients, page, rowsPerPage]);

  const patientMap = useMemo(() => {
    const m: Record<string, any> = {};
    (patients || []).forEach((p: any) => { m[p.id] = p; });
    return m;
  }, [patients]);

  const filteredAi = useMemo(() => {
    if (!search.trim()) return ai || [];
    const q = search.toLowerCase();
    return (ai || []).filter((r: any) => {
      const name = patientMap[r.patient_id] ? `${patientMap[r.patient_id].family_name}${patientMap[r.patient_id].given_name}` : '';
      return (r.patient_id + name + r.finding + r.status).toLowerCase().includes(q);
    });
  }, [ai, search, patientMap]);

  const aiStatusMap = useMemo(() => {
    const m: Record<string, string> = {};
    (ai || []).forEach((r: any) => { m[r.patient_id] = r.status; });
    return m;
  }, [ai]);

  const riskScores = useMemo(() => {
    const m: Record<string, number> = {};
    (vital || []).forEach((v: any) => {
      let s = 0;
      if (v.heart_rate > 100 || v.heart_rate < 50) s += 30;
      else if (v.heart_rate > 80) s += 10;
      if (v.spo2 < 95) s += 40;
      else if (v.spo2 < 97) s += 15;
      const bp = v.blood_pressure?.match(/(\d+)\/(\d+)/);
      if (bp) {
        const sys = +bp[1], dia = +bp[2];
        if (sys > 160 || dia > 100) s += 25;
      }
      m[v.patient_id] = Math.min(100, (m[v.patient_id] || 0) + s);
    });
    (ai || []).forEach((r: any) => {
      if (r.status === 'Review') m[r.patient_id] = Math.min(100, (m[r.patient_id] || 0) + 20);
      if ((r.confidence || 0) < 0.8) m[r.patient_id] = Math.min(100, (m[r.patient_id] || 0) + 15);
    });
    return m;
  }, [vital, ai]);

  return (
    <Box component="section" sx={{ minHeight: 400, width: '100%', display: 'block', pt: 1 }}>
      <Typography variant="h5" fontWeight={600} gutterBottom>医療</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        FHIR準拠の患者管理・AI診断支援・リアルタイムバイタルモニター・病棟ベッドマップ
      </Typography>
      <Paper elevation={0}>
        <Tabs value={subTab} onChange={(_, v) => setSubTab(v)}>
          <Tab icon={<People />} iconPosition="start" label="患者一覧" />
          <Tab icon={<Psychology />} iconPosition="start" label="AI診断" />
          <Tab icon={<MonitorHeart />} iconPosition="start" label="バイタルモニター" />
          <Tab icon={<GridView />} iconPosition="start" label="ベッドマップ" />
          <Tab icon={<Timeline />} iconPosition="start" label="タイムライン" />
          <Tab icon={<Summarize />} iconPosition="start" label="サマリ" />
        </Tabs>
        <Box sx={{ p: 2 }}>
          <TabPanel value={subTab} index={0}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>患者一覧（FHIR Patient）</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              登録患者の基本情報。IDはHL7 FHIR準拠の識別子です。
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
              <Button size="small" startIcon={<Download />} onClick={() => { downloadCsv(patients || [], 'medical_patients.csv'); toast.show('CSVをダウンロードしました'); }}>CSV</Button>
              <Button size="small" startIcon={<Download />} onClick={() => { downloadExcel(patients || [], 'medical_patients.xlsx'); toast.show('Excelをダウンロードしました'); }}>Excel</Button>
              <Button size="small" startIcon={<Download />} onClick={() => { downloadJson(patients || [], 'medical_patients.json'); toast.show('JSONをダウンロードしました'); }}>JSON</Button>
              <Button size="small" component="label" startIcon={<Upload />}>CSVインポート<input type="file" accept=".csv" hidden onChange={async (e) => { const f = e.target.files?.[0]; if (!f) return; try { const { unifiedApi } = await import('../api/unified'); const r = await unifiedApi.medical.importPatientsCsv(f); toast.show(`${r.data.imported}件をインポートしました`, 'success'); onRefresh?.(); } catch (err: any) { toast.show(err?.response?.data?.detail || 'インポートに失敗しました', 'error'); } e.target.value = ''; }} /></Button>
            </Box>
            <TableContainer>
              <Table size="small">
                <TableHead><TableRow><TableCell>ID</TableCell><TableCell>氏名</TableCell><TableCell>性別</TableCell><TableCell>生年月日</TableCell><TableCell>AI診断</TableCell></TableRow></TableHead>
                <TableBody>
                  {paginatedPatients.map((p: any) => (
                    <TableRow key={p.id}><TableCell>{p.identifier}</TableCell><TableCell>{p.family_name} {p.given_name}</TableCell><TableCell>{p.gender === 'male' ? '男' : p.gender === 'female' ? '女' : p.gender}</TableCell><TableCell>{p.birth_date}</TableCell><TableCell><Chip size="small" label={aiStatusMap[p.id] || '-'} variant="outlined" /></TableCell></TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              component="div"
              count={patients?.length ?? 0}
              page={page}
              onPageChange={(_, p) => setPage(p)}
              rowsPerPage={rowsPerPage}
              onRowsPerPageChange={(e) => { setRowsPerPage(parseInt(e.target.value, 10)); setPage(0); }}
              rowsPerPageOptions={[5, 10, 25, 50]}
              labelDisplayedRows={({ from, to, count }) => `${from}-${to} / ${count}`}
              labelRowsPerPage="表示件数:"
            />
          </TabPanel>
          <TabPanel value={subTab} index={1}>
            <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
              <TextField size="small" placeholder="検索 (患者ID・所見・ステータス)" value={search} onChange={(e) => setSearch(e.target.value)} InputProps={{ startAdornment: <InputAdornment position="start"><Search fontSize="small" /></InputAdornment> }} sx={{ minWidth: 220 }} />
              <Button size="small" startIcon={<Download />} onClick={() => { downloadCsv(filteredAi.map((r: any) => ({ id: r.id, patient_id: r.patient_id, finding: r.finding, confidence: r.confidence, status: r.status })), 'medical_ai_diagnosis.csv'); toast.show('CSVをダウンロードしました'); }}>CSV</Button>
            </Box>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>AI診断結果（所見・信頼度・レビュー状態）</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              画像・波形AIによる所見。Confidence が低い場合は医師レビューを推奨します。
            </Typography>
            <SortableTable
              data={filteredAi}
              columns={[{ key: 'id', label: 'ID' }, { key: 'patient_id', label: '患者' }, { key: 'summary', label: '要約' }, { key: 'finding', label: '所見' }, { key: 'confidence', label: '信頼度' }, { key: 'status', label: '状態' }]}
              defaultOrderBy="id"
              getRowKey={(r: any) => r.id}
              renderRow={(r: any) => {
                const name = patientMap[r.patient_id] ? `${patientMap[r.patient_id].family_name} ${patientMap[r.patient_id].given_name}` : r.patient_id;
                const confColor = r.confidence >= 0.9 ? 'success' : r.confidence >= 0.75 ? 'warning' : 'error';
                return (<><TableCell>{r.id}</TableCell><TableCell>{name} ({r.patient_id})</TableCell><TableCell>{r.summary || r.finding?.slice(0, 20) || '-'}</TableCell><TableCell>{r.finding}</TableCell><TableCell><Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}><LinearProgress variant="determinate" value={(r.confidence || 0) * 100} color={confColor as any} sx={{ width: 60, height: 6, borderRadius: 1 }} /><Typography variant="caption">{(r.confidence * 100).toFixed(0)}%</Typography></Box></TableCell><TableCell><Chip size="small" label={r.status} color={r.status === 'Review' ? 'warning' : r.status === 'Done' ? 'success' : 'default'} /></TableCell></>);
              }}
            />
          </TabPanel>
          <TabPanel value={subTab} index={2}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ color: '#00e676' }}>
              バイタルモニター（HR / BP / SpO2）
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              心拍・血圧・酸素飽和度のリアルタイム表示。異常値は要観察としてサマリに集計されます。
            </Typography>
            <MedicalVitalMonitor vitals={vital || []} />
          </TabPanel>
          <TabPanel value={subTab} index={3}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ color: '#00e676' }}>WARD STATUS | BED MAP</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              病棟ベッド配置と患者ステータス。AI診断のレビュー状態を色で表示。
            </Typography>
            <MedicalBedMap patients={vital || []} aiStatus={aiStatusMap} />
          </TabPanel>
          <TabPanel value={subTab} index={4}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>患者タイムライン</Typography>
            <MedicalPatientTimeline ai={ai || []} vital={vital || []} patientMap={patientMap} />
          </TabPanel>
          <TabPanel value={subTab} index={5}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>サマリ</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              患者数・AI診断数・レビュー待ち・要観察・リスクスコア（バイタル+AI信頼度から算出）。
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 3 }}>
              <Paper elevation={0} sx={{ p: 2, minWidth: 180 }}><Typography variant="h6" color="primary.main">{patients?.length ?? 0}</Typography><Typography variant="caption">登録患者</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 180 }}><Typography variant="h6" color="success.main">{ai?.length ?? 0}</Typography><Typography variant="caption">AI診断</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 180 }}><Typography variant="h6" color="info.main">{vital?.length ?? 0}</Typography><Typography variant="caption">バイタル記録</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 180 }}><Typography variant="h6" color="warning.main">{(ai || []).filter((r: any) => r.status === 'Review').length}</Typography><Typography variant="caption">レビュー待ち</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 180 }}><Typography variant="h6" color="secondary.main">{(vital || []).filter((v: any) => (v.heart_rate > 80 || v.spo2 < 97)).length}</Typography><Typography variant="caption">要観察</Typography></Paper>
              <Paper elevation={0} sx={{ p: 2, minWidth: 180 }}><Typography variant="h6" color="error.main">{Object.values(riskScores).filter((s: number) => s >= 30).length}</Typography><Typography variant="caption">リスク高（≥30）</Typography></Paper>
            </Box>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>患者別リスクスコア・ステータス</Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {(patients || []).map((p: any) => (
                <Chip key={p.id} size="small" label={`${p.family_name}${p.given_name}: リスク${riskScores[p.id] ?? 0} / ${aiStatusMap[p.id] || '-'}`} variant="outlined" color={(riskScores[p.id] || 0) >= 30 ? 'error' : 'default'} sx={{ mb: 0.5 }} />
              ))}
            </Box>
          </TabPanel>
        </Box>
      </Paper>
    </Box>
  );
};
