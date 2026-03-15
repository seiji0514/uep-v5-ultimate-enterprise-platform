/**
 * コンプライアンス・ガバナンス系 タブ
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
import { Gavel, Visibility, Policy, Warning, School } from '@mui/icons-material';
import type { RegulatoryItem, AuditLog, GovernancePolicy, AuditFinding } from '../../api';
import { LearnPanel } from './LearnPanel';
import { loadLearnProgress } from './utils';
import { getSeverityColor } from './utils';
import {
  COMPLIANCE_LEARN_REG,
  COMPLIANCE_LEARN_AUDITLOG,
  COMPLIANCE_LEARN_POLICY,
  COMPLIANCE_LEARN_FINDING,
} from './learnSteps';

export interface ComplianceTabProps {
  regulatoryItems: RegulatoryItem[];
  auditLogs: AuditLog[];
  governancePolicies: GovernancePolicy[];
  auditFindings: AuditFinding[];
  subTab: number;
  setSubTab: (v: number) => void;
  learnType: 0 | 1 | 2 | 3;
  setLearnType: (v: 0 | 1 | 2 | 3) => void;
  learnStep: number;
  setLearnStep: (v: number | ((s: number) => number)) => void;
  learnSelected: number | null;
  setLearnSelected: (v: number | null) => void;
  learnFeedback: 'correct' | 'wrong' | null;
  setLearnFeedback: (v: 'correct' | 'wrong' | null) => void;
}

export function ComplianceTab({
  regulatoryItems,
  auditLogs,
  governancePolicies,
  auditFindings,
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
}: ComplianceTabProps) {
  const steps = learnType === 0 ? COMPLIANCE_LEARN_REG : learnType === 1 ? COMPLIANCE_LEARN_AUDITLOG : learnType === 2 ? COMPLIANCE_LEARN_POLICY : COMPLIANCE_LEARN_FINDING;

  return (
    <>
      <Typography variant="h6" gutterBottom>コンプライアンス・ガバナンス系</Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        規制対応、監査ログ、ポリシー、監査指摘。未対応の指摘・要対応の規制は要対応です。
      </Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">規制対応</Typography><Typography variant="h5">{regulatoryItems.length}</Typography><Typography variant="caption" color="error">要対応: {regulatoryItems.filter((r) => r.status === '要対応').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">監査指摘</Typography><Typography variant="h5">{auditFindings.length}</Typography><Typography variant="caption" color="error">未対応: {auditFindings.filter((f) => f.status !== '対応済').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">ポリシー</Typography><Typography variant="h5">{governancePolicies.length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">監査ログ(今日)</Typography><Typography variant="h5">{auditLogs.length}</Typography></CardContent></Card></Grid>
      </Grid>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip icon={<Gavel />} label="規制対応" onClick={() => setSubTab(0)} color={subTab === 0 ? 'primary' : 'default'} />
        <Chip icon={<Visibility />} label="監査ログ" onClick={() => setSubTab(1)} color={subTab === 1 ? 'primary' : 'default'} />
        <Chip icon={<Policy />} label="ポリシー" onClick={() => setSubTab(2)} color={subTab === 2 ? 'primary' : 'default'} />
        <Chip icon={<Warning />} label="監査指摘" onClick={() => setSubTab(3)} color={subTab === 3 ? 'primary' : 'default'} />
        <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSubTab(4); setLearnType(0); setLearnStep(p['compliance_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={subTab === 4 ? 'primary' : 'default'} />
      </Stack>
      {subTab === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>規制</TableCell><TableCell>ステータス</TableCell><TableCell>コンプライアンススコア</TableCell><TableCell>最終監査</TableCell></TableRow></TableHead>
            <TableBody>
              {regulatoryItems.map((r) => (
                <TableRow key={r.id} hover>
                  <TableCell>{r.regulation}</TableCell>
                  <TableCell><Chip label={r.status} size="small" color={r.status === '要対応' ? 'error' : 'default'} /></TableCell>
                  <TableCell>{r.compliance_score}%</TableCell>
                  <TableCell>{r.last_audit ? new Date(r.last_audit).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {regulatoryItems.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>アクション</TableCell><TableCell>ユーザー</TableCell><TableCell>リソース</TableCell><TableCell>結果</TableCell><TableCell>日時</TableCell></TableRow></TableHead>
            <TableBody>
              {auditLogs.map((a) => (
                <TableRow key={a.id} hover>
                  <TableCell>{a.action}</TableCell>
                  <TableCell>{a.user}</TableCell>
                  <TableCell>{a.resource}</TableCell>
                  <TableCell>{a.result}</TableCell>
                  <TableCell>{a.timestamp ? new Date(a.timestamp).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {auditLogs.length === 0 && <TableRow><TableCell colSpan={5} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 2 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>ポリシー</TableCell><TableCell>バージョン</TableCell><TableCell>ステータス</TableCell><TableCell>更新日</TableCell></TableRow></TableHead>
            <TableBody>
              {governancePolicies.map((p) => (
                <TableRow key={p.id} hover>
                  <TableCell>{p.name}</TableCell>
                  <TableCell>{p.version}</TableCell>
                  <TableCell><Chip label={p.status} size="small" /></TableCell>
                  <TableCell>{p.updated ? new Date(p.updated).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {governancePolicies.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 3 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>重大度</TableCell><TableCell>説明</TableCell><TableCell>ステータス</TableCell><TableCell>期限</TableCell></TableRow></TableHead>
            <TableBody>
              {auditFindings.map((f) => (
                <TableRow key={f.id} hover>
                  <TableCell><Chip label={f.severity} color={getSeverityColor(f.severity) as any} size="small" /></TableCell>
                  <TableCell>{f.description}</TableCell>
                  <TableCell><Chip label={f.status} size="small" color={f.status !== '対応済' ? 'warning' : 'default'} /></TableCell>
                  <TableCell>{f.due_date ? new Date(f.due_date).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {auditFindings.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 4 && (
        <Box>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip label="規制対応" onClick={() => { const p = loadLearnProgress(); setLearnType(0); setLearnStep(p['compliance_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 0 ? 'primary' : 'default'} variant={learnType === 0 ? 'filled' : 'outlined'} />
            <Chip label="監査ログ" onClick={() => { const p = loadLearnProgress(); setLearnType(1); setLearnStep(p['compliance_1'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 1 ? 'primary' : 'default'} variant={learnType === 1 ? 'filled' : 'outlined'} />
            <Chip label="ポリシー" onClick={() => { const p = loadLearnProgress(); setLearnType(2); setLearnStep(p['compliance_2'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 2 ? 'primary' : 'default'} variant={learnType === 2 ? 'filled' : 'outlined'} />
            <Chip label="監査指摘" onClick={() => { const p = loadLearnProgress(); setLearnType(3); setLearnStep(p['compliance_3'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 3 ? 'primary' : 'default'} variant={learnType === 3 ? 'filled' : 'outlined'} />
          </Stack>
          <LearnPanel steps={steps} stepIndex={learnStep} setStepIndex={setLearnStep} selected={learnSelected} setSelected={setLearnSelected} feedback={learnFeedback} setFeedback={setLearnFeedback} onReset={() => { setLearnStep(0); setLearnSelected(null); setLearnFeedback(null); }} />
        </Box>
      )}
    </>
  );
}
