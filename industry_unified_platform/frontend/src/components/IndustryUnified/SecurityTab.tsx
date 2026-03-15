/**
 * 統合セキュリティ・防衛 タブ
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
import { Shield, Warning, Security, School } from '@mui/icons-material';
import type { SecurityEvent, SecurityIncident, SecurityRisk } from '../../api';
import { LearnPanel } from './LearnPanel';
import { loadLearnProgress } from './utils';
import { getSeverityColor } from './utils';
import { SECURITY_LEARN_EVENT, SECURITY_LEARN_INCIDENT, SECURITY_LEARN_RISK } from './learnSteps';

export interface SecurityTabProps {
  securityEvents: SecurityEvent[];
  securityIncidents: SecurityIncident[];
  securityRisks: SecurityRisk[];
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

export function SecurityTab({
  securityEvents,
  securityIncidents,
  securityRisks,
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
}: SecurityTabProps) {
  const steps = learnType === 0 ? SECURITY_LEARN_EVENT : learnType === 1 ? SECURITY_LEARN_INCIDENT : SECURITY_LEARN_RISK;

  return (
    <>
      <Typography variant="h6" gutterBottom>統合セキュリティ・防衛</Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        IDS/IPS, EDR, SIEM, 脅威インテリジェンス, コンプライアンス。Critical/High イベントは要対応です。
      </Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={4}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">セキュリティイベント</Typography><Typography variant="h5">{securityEvents.length}</Typography><Typography variant="caption" color="error">Critical/High: {securityEvents.filter((e) => ['critical', 'high'].includes((e.threat_level || '').toLowerCase())).length}</Typography></CardContent></Card></Grid>
        <Grid item xs={4}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">インシデント</Typography><Typography variant="h5">{securityIncidents.length}</Typography><Typography variant="caption" color="error">未対応: {securityIncidents.filter((i) => (i.status || '').toLowerCase() !== 'resolved').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={4}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">リスク</Typography><Typography variant="h5">{securityRisks.length}</Typography></CardContent></Card></Grid>
      </Grid>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip icon={<Shield />} label="イベント" onClick={() => setSubTab(0)} color={subTab === 0 ? 'primary' : 'default'} />
        <Chip icon={<Warning />} label="インシデント" onClick={() => setSubTab(1)} color={subTab === 1 ? 'primary' : 'default'} />
        <Chip icon={<Security />} label="リスク" onClick={() => setSubTab(2)} color={subTab === 2 ? 'primary' : 'default'} />
        <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSubTab(3); setLearnType(0); setLearnStep(p['security_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={subTab === 3 ? 'primary' : 'default'} />
      </Stack>
      {subTab === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>種別</TableCell><TableCell>脅威レベル</TableCell><TableCell>送信元</TableCell><TableCell>送信先</TableCell><TableCell>ステータス</TableCell><TableCell>発生日時</TableCell><TableCell>説明</TableCell></TableRow></TableHead>
            <TableBody>
              {securityEvents.map((e) => (
                <TableRow key={e.id} hover>
                  <TableCell>{e.event_type}</TableCell>
                  <TableCell><Chip label={(e.threat_level || '').toUpperCase()} color={getSeverityColor(e.threat_level) as any} size="small" /></TableCell>
                  <TableCell>{e.source}</TableCell>
                  <TableCell>{e.target}</TableCell>
                  <TableCell><Chip label={e.status || '-'} size="small" variant="outlined" /></TableCell>
                  <TableCell>{(e.timestamp || e.created_at) ? new Date(e.timestamp || e.created_at!).toLocaleString('ja-JP') : '-'}</TableCell>
                  <TableCell><Typography variant="body2" sx={{ maxWidth: 220, overflow: 'hidden', textOverflow: 'ellipsis' }} title={e.description}>{e.description}</Typography></TableCell>
                </TableRow>
              ))}
              {securityEvents.length === 0 && <TableRow><TableCell colSpan={7} align="center">データがありません（権限確認またはイベントを登録してください）</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>タイトル</TableCell><TableCell>重大度</TableCell><TableCell>ステータス</TableCell><TableCell>説明</TableCell></TableRow></TableHead>
            <TableBody>
              {securityIncidents.map((i) => (
                <TableRow key={i.id} hover>
                  <TableCell>{i.title}</TableCell>
                  <TableCell><Chip label={i.severity} color={getSeverityColor(i.severity) as any} size="small" /></TableCell>
                  <TableCell><Chip label={i.status} size="small" variant="outlined" /></TableCell>
                  <TableCell><Typography variant="body2" sx={{ maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis' }}>{i.description}</Typography></TableCell>
                </TableRow>
              ))}
              {securityIncidents.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 2 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>名称</TableCell><TableCell>レベル</TableCell><TableCell>説明</TableCell></TableRow></TableHead>
            <TableBody>
              {securityRisks.map((r) => (
                <TableRow key={r.id} hover>
                  <TableCell>{(r as any).name ?? r.title ?? '-'}</TableCell>
                  <TableCell><Chip label={(r as any).risk_level ?? r.level ?? '-'} color={getSeverityColor((r as any).risk_level ?? r.level ?? '') as any} size="small" /></TableCell>
                  <TableCell><Typography variant="body2" sx={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis' }}>{r.description}</Typography></TableCell>
                </TableRow>
              ))}
              {securityRisks.length === 0 && <TableRow><TableCell colSpan={3} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 3 && (
        <Box>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip label="イベント" onClick={() => { const p = loadLearnProgress(); setLearnType(0); setLearnStep(p['security_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 0 ? 'primary' : 'default'} variant={learnType === 0 ? 'filled' : 'outlined'} />
            <Chip label="インシデント" onClick={() => { const p = loadLearnProgress(); setLearnType(1); setLearnStep(p['security_1'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 1 ? 'primary' : 'default'} variant={learnType === 1 ? 'filled' : 'outlined'} />
            <Chip label="リスク" onClick={() => { const p = loadLearnProgress(); setLearnType(2); setLearnStep(p['security_2'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 2 ? 'primary' : 'default'} variant={learnType === 2 ? 'filled' : 'outlined'} />
          </Stack>
          <LearnPanel steps={steps} stepIndex={learnStep} setStepIndex={setLearnStep} selected={learnSelected} setSelected={setLearnSelected} feedback={learnFeedback} setFeedback={setLearnFeedback} onReset={() => { setLearnStep(0); setLearnSelected(null); setLearnFeedback(null); }} />
        </Box>
      )}
    </>
  );
}
