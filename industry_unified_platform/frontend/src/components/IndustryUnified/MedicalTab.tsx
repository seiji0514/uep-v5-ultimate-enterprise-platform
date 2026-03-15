/**
 * 医療・ヘルスケア タブ
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
import { Psychology, RecordVoiceOver, Warning, School } from '@mui/icons-material';
import type { AIDiagnosis, VoiceResponse, MedicalAnomaly, PlatformStats } from '../../api';
import { LearnPanel } from './LearnPanel';
import { loadLearnProgress } from './utils';
import { getSeverityColor } from './utils';
import { MEDICAL_LEARN_AI, MEDICAL_LEARN_VOICE, MEDICAL_LEARN_ANOMALY } from './learnSteps';

export interface MedicalTabProps {
  aiDiagnosis: AIDiagnosis[];
  voiceResponse: VoiceResponse[];
  medicalAnomalies: MedicalAnomaly[];
  stats: PlatformStats | null;
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

export function MedicalTab({
  aiDiagnosis,
  voiceResponse,
  medicalAnomalies,
  stats,
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
}: MedicalTabProps) {
  const steps = learnType === 0 ? MEDICAL_LEARN_AI : learnType === 1 ? MEDICAL_LEARN_VOICE : MEDICAL_LEARN_ANOMALY;

  return (
    <>
      <Typography variant="h6" gutterBottom>医療・ヘルスケア</Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        AI診断・音声応答・FHIR連携。要確認の所見や高重大度の異常は要対応です。
      </Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">患者</Typography><Typography variant="h5">{stats?.active_patients ?? '-'}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">AI診断</Typography><Typography variant="h5">{stats?.ai_diagnosis_today ?? '-'}</Typography><Typography variant="caption" color="error">要確認: {aiDiagnosis.filter((d) => d.status === '要確認').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">音声処理</Typography><Typography variant="h5">{stats?.voice_processed_today ?? '-'}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">異常検知</Typography><Typography variant="h5">{stats?.anomalies_detected_today ?? '-'}</Typography><Typography variant="caption" color="error">高: {medicalAnomalies.filter((a) => a.severity === '高').length}</Typography></CardContent></Card></Grid>
      </Grid>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip icon={<Psychology />} label="AI診断" onClick={() => setSubTab(0)} color={subTab === 0 ? 'primary' : 'default'} />
        <Chip icon={<RecordVoiceOver />} label="音声応答" onClick={() => setSubTab(1)} color={subTab === 1 ? 'primary' : 'default'} />
        <Chip icon={<Warning />} label="異常検知" onClick={() => setSubTab(2)} color={subTab === 2 ? 'primary' : 'default'} />
        <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSubTab(3); setLearnType(0); setLearnStep(p['medical_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={subTab === 3 ? 'primary' : 'default'} />
      </Stack>
      {subTab === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>患者ID</TableCell><TableCell>所見</TableCell><TableCell>信頼度</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
            <TableBody>
              {aiDiagnosis.map((d) => (
                <TableRow key={d.id} hover>
                  <TableCell>{d.patient_id}</TableCell>
                  <TableCell>{d.finding}</TableCell>
                  <TableCell>{(d.confidence * 100).toFixed(0)}%</TableCell>
                  <TableCell><Chip label={d.status} size="small" color={d.status === '要確認' ? 'warning' : 'default'} /></TableCell>
                </TableRow>
              ))}
              {aiDiagnosis.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>種別</TableCell><TableCell>時間(秒)</TableCell><TableCell>文字起こし</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
            <TableBody>
              {voiceResponse.map((v) => (
                <TableRow key={v.id} hover>
                  <TableCell>{v.type}</TableCell>
                  <TableCell>{v.duration_sec}</TableCell>
                  <TableCell><Typography variant="body2" sx={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis' }}>{v.transcription}</Typography></TableCell>
                  <TableCell><Chip label={v.status} size="small" /></TableCell>
                </TableRow>
              ))}
              {voiceResponse.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 2 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>種別</TableCell><TableCell>患者ID</TableCell><TableCell>指標</TableCell><TableCell>値</TableCell><TableCell>閾値</TableCell><TableCell>重大度</TableCell></TableRow></TableHead>
            <TableBody>
              {medicalAnomalies.map((a) => (
                <TableRow key={a.id} hover>
                  <TableCell>{a.type}</TableCell>
                  <TableCell>{a.patient_id}</TableCell>
                  <TableCell>{a.metric}</TableCell>
                  <TableCell>{a.value}</TableCell>
                  <TableCell>{a.threshold}</TableCell>
                  <TableCell><Chip label={a.severity} color={getSeverityColor(a.severity) as any} size="small" /></TableCell>
                </TableRow>
              ))}
              {medicalAnomalies.length === 0 && <TableRow><TableCell colSpan={6} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 3 && (
        <Box>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip label="AI診断" onClick={() => { const p = loadLearnProgress(); setLearnType(0); setLearnStep(p['medical_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 0 ? 'primary' : 'default'} variant={learnType === 0 ? 'filled' : 'outlined'} />
            <Chip label="音声応答" onClick={() => { const p = loadLearnProgress(); setLearnType(1); setLearnStep(p['medical_1'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 1 ? 'primary' : 'default'} variant={learnType === 1 ? 'filled' : 'outlined'} />
            <Chip label="異常検知" onClick={() => { const p = loadLearnProgress(); setLearnType(2); setLearnStep(p['medical_2'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 2 ? 'primary' : 'default'} variant={learnType === 2 ? 'filled' : 'outlined'} />
          </Stack>
          <LearnPanel steps={steps} stepIndex={learnStep} setStepIndex={setLearnStep} selected={learnSelected} setSelected={setLearnSelected} feedback={learnFeedback} setFeedback={setLearnFeedback} onReset={() => { setLearnStep(0); setLearnSelected(null); setLearnFeedback(null); }} />
        </Box>
      )}
    </>
  );
}
