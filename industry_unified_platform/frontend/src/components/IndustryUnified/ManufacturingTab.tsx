/**
 * 製造・IoT タブ
 */
import React from 'react';
import {
  Typography,
  Paper,
  Card,
  CardContent,
  Stack,
  Grid,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
} from '@mui/material';
import { PrecisionManufacturing, Sensors, Warning, School } from '@mui/icons-material';
import type { PredictiveMaintenance, SensorData, Anomaly } from '../../api';
import { LearnPanel } from './LearnPanel';
import { loadLearnProgress } from './utils';
import { getSeverityColor } from './utils';
import {
  MANUFACTURING_LEARN_PREDICTIVE,
  MANUFACTURING_LEARN_SENSOR,
  MANUFACTURING_LEARN_ANOMALY,
} from './learnSteps';

export interface ManufacturingTabProps {
  predictive: PredictiveMaintenance[];
  sensors: SensorData[];
  anomalies: Anomaly[];
  subTab: number;
  setSubTab: (v: number) => void;
  learnType: 0 | 1 | 2;
  setLearnType: (v: 0 | 1 | 2) => void;
  learnStep: number;
  setLearnStep: (v: number | ((s: number) => number)) => void;
  learnSelected: number | null;
  setLearnSelected: (v: number | null) => void;
  learnFeedback: 'correct' | 'wrong' | null;
  setLearnFeedback: (v: 'correct' | 'wrong' | null) => void;
}

export function ManufacturingTab({
  predictive,
  sensors,
  anomalies,
  subTab,
  setSubTab,
  learnType,
  setLearnType,
  learnStep,
  setLearnStep,
  learnSelected,
  setLearnSelected,
  learnFeedback,
  setLearnFeedback,
}: ManufacturingTabProps) {
  const steps = learnType === 0 ? MANUFACTURING_LEARN_PREDICTIVE : learnType === 1 ? MANUFACTURING_LEARN_SENSOR : MANUFACTURING_LEARN_ANOMALY;

  return (
    <>
      <Typography variant="h6" gutterBottom>製造・IoT</Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        予知保全・OPC-UAセンサーデータ・異常検知。要メンテナンス設備や高重大度の異常は要対応です。
      </Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={4}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">予知保全</Typography><Typography variant="h5">{predictive.length}</Typography><Typography variant="caption" color="error">要メンテ: {predictive.filter((p) => p.status === '要メンテナンス').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={4}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">センサー</Typography><Typography variant="h5">{sensors.length}</Typography><Typography variant="caption" color="text.secondary">リアルタイム</Typography></CardContent></Card></Grid>
        <Grid item xs={4}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">異常検知</Typography><Typography variant="h5">{anomalies.length}</Typography><Typography variant="caption" color="error">高: {anomalies.filter((a) => a.severity === '高').length}</Typography></CardContent></Card></Grid>
      </Grid>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip icon={<PrecisionManufacturing />} label="予知保全" onClick={() => setSubTab(0)} color={subTab === 0 ? 'primary' : 'default'} />
        <Chip icon={<Sensors />} label="センサーデータ" onClick={() => setSubTab(1)} color={subTab === 1 ? 'primary' : 'default'} />
        <Chip icon={<Warning />} label="異常検知" onClick={() => setSubTab(2)} color={subTab === 2 ? 'primary' : 'default'} />
        <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSubTab(3); setLearnType(0); setLearnStep(p['manufacturing_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={subTab === 3 ? 'primary' : 'default'} />
      </Stack>
      {subTab === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>設備</TableCell><TableCell>予測故障日</TableCell><TableCell>信頼度</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
            <TableBody>
              {predictive.map((p) => (
                <TableRow key={p.id} hover>
                  <TableCell>{p.equipment}</TableCell>
                  <TableCell>{p.predicted_failure}</TableCell>
                  <TableCell>{(p.confidence * 100).toFixed(0)}%</TableCell>
                  <TableCell><Chip label={p.status} size="small" color={p.status === '要メンテナンス' ? 'error' : 'default'} /></TableCell>
                </TableRow>
              ))}
              {predictive.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>センサーID</TableCell><TableCell>値</TableCell><TableCell>単位</TableCell><TableCell>タイムスタンプ</TableCell></TableRow></TableHead>
            <TableBody>
              {sensors.map((s) => (
                <TableRow key={s.sensor_id} hover>
                  <TableCell>{s.sensor_id}</TableCell>
                  <TableCell>{s.value}</TableCell>
                  <TableCell>{s.unit}</TableCell>
                  <TableCell>{s.timestamp ? new Date(s.timestamp).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {sensors.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 2 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>種別</TableCell><TableCell>設備</TableCell><TableCell>重大度</TableCell><TableCell>検知日時</TableCell></TableRow></TableHead>
            <TableBody>
              {anomalies.map((a) => (
                <TableRow key={a.id} hover>
                  <TableCell>{a.type}</TableCell>
                  <TableCell>{a.equipment}</TableCell>
                  <TableCell><Chip label={a.severity} color={getSeverityColor(a.severity) as any} size="small" /></TableCell>
                  <TableCell>{a.detected_at ? new Date(a.detected_at).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {anomalies.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 3 && (
        <Box>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip label="予知保全" onClick={() => { const p = loadLearnProgress(); setLearnType(0); setLearnStep(p['manufacturing_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 0 ? 'primary' : 'default'} variant={learnType === 0 ? 'filled' : 'outlined'} />
            <Chip label="センサーデータ" onClick={() => { const p = loadLearnProgress(); setLearnType(1); setLearnStep(p['manufacturing_1'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 1 ? 'primary' : 'default'} variant={learnType === 1 ? 'filled' : 'outlined'} />
            <Chip label="異常検知" onClick={() => { const p = loadLearnProgress(); setLearnType(2); setLearnStep(p['manufacturing_2'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 2 ? 'primary' : 'default'} variant={learnType === 2 ? 'filled' : 'outlined'} />
          </Stack>
          <LearnPanel
            steps={steps}
            stepIndex={learnStep}
            setStepIndex={setLearnStep}
            selected={learnSelected}
            setSelected={setLearnSelected}
            feedback={learnFeedback}
            setFeedback={setLearnFeedback}
            onReset={() => { setLearnStep(0); setLearnSelected(null); setLearnFeedback(null); }}
          />
        </Box>
      )}
    </>
  );
}
