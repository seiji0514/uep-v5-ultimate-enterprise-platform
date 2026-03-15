/**
 * インフラ・運用系 タブ
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
import { Build, Cloud, Visibility, Science, School } from '@mui/icons-material';
import type { IacProject, MonitoringAlert, OrchestrationDeployment, OptimizationRecommendation } from '../../api';
import { LearnPanel } from './LearnPanel';
import { loadLearnProgress } from './utils';
import { getSeverityColor } from './utils';
import {
  INFRA_OPS_LEARN_IAC,
  INFRA_OPS_LEARN_ORCH,
  INFRA_OPS_LEARN_MONITOR,
  INFRA_OPS_LEARN_OPT,
} from './learnSteps';

export interface InfraOpsTabProps {
  iacProjects: IacProject[];
  monitoringAlerts: MonitoringAlert[];
  orchestrationDeployments: OrchestrationDeployment[];
  optimizationRecs: OptimizationRecommendation[];
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

export function InfraOpsTab({
  iacProjects,
  monitoringAlerts,
  orchestrationDeployments,
  optimizationRecs,
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
}: InfraOpsTabProps) {
  const steps = learnType === 0 ? INFRA_OPS_LEARN_IAC : learnType === 1 ? INFRA_OPS_LEARN_ORCH : learnType === 2 ? INFRA_OPS_LEARN_MONITOR : INFRA_OPS_LEARN_OPT;

  return (
    <>
      <Typography variant="h6" gutterBottom>インフラ・運用系（SIer・クラウドベンダー）</Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        IaC、オーケストレーション、監視、FinOps最適化。未対応アラート・ドリフト検知・Pendingデプロイは要対応です。
      </Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">IaCプロジェクト</Typography><Typography variant="h5">{iacProjects.length}</Typography><Typography variant="caption" color="warning.main">ドリフト: {iacProjects.filter((p) => p.status === 'ドリフト検知').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">デプロイメント</Typography><Typography variant="h5">{orchestrationDeployments.length}</Typography><Typography variant="caption" color="error">Pending: {orchestrationDeployments.filter((d) => d.status === 'Pending').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">監視アラート</Typography><Typography variant="h5">{monitoringAlerts.length}</Typography><Typography variant="caption" color="error">未対応: {monitoringAlerts.filter((a) => a.status !== '対応済').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">最適化推奨</Typography><Typography variant="h5">{optimizationRecs.length}</Typography><Typography variant="caption" color="success.main">節約見込: ¥{optimizationRecs.reduce((s, r) => s + r.saving_estimate, 0).toLocaleString()}</Typography></CardContent></Card></Grid>
      </Grid>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip icon={<Build />} label="IaC" onClick={() => setSubTab(0)} color={subTab === 0 ? 'primary' : 'default'} />
        <Chip icon={<Cloud />} label="オーケストレーション" onClick={() => setSubTab(1)} color={subTab === 1 ? 'primary' : 'default'} />
        <Chip icon={<Visibility />} label="監視アラート" onClick={() => setSubTab(2)} color={subTab === 2 ? 'primary' : 'default'} />
        <Chip icon={<Science />} label="最適化推奨" onClick={() => setSubTab(3)} color={subTab === 3 ? 'primary' : 'default'} />
        <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSubTab(4); setLearnType(0); setLearnStep(p['infraOps_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={subTab === 4 ? 'primary' : 'default'} />
      </Stack>
      {subTab === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>プロジェクト</TableCell><TableCell>プロバイダー</TableCell><TableCell>ステータス</TableCell><TableCell>最終デプロイ</TableCell></TableRow></TableHead>
            <TableBody>
              {iacProjects.map((p) => (
                <TableRow key={p.id} hover>
                  <TableCell>{p.name}</TableCell>
                  <TableCell>{p.provider}</TableCell>
                  <TableCell><Chip label={p.status} size="small" color={p.status === 'ドリフト検知' ? 'warning' : 'default'} /></TableCell>
                  <TableCell>{p.last_deploy ? new Date(p.last_deploy).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {iacProjects.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>アプリ</TableCell><TableCell>環境</TableCell><TableCell>ステータス</TableCell><TableCell>レプリカ</TableCell><TableCell>更新</TableCell></TableRow></TableHead>
            <TableBody>
              {orchestrationDeployments.map((d) => (
                <TableRow key={d.id} hover>
                  <TableCell>{d.app}</TableCell>
                  <TableCell>{d.env}</TableCell>
                  <TableCell><Chip label={d.status} size="small" color={d.status === 'Pending' ? 'warning' : 'default'} /></TableCell>
                  <TableCell>{d.replicas}</TableCell>
                  <TableCell>{d.updated ? new Date(d.updated).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {orchestrationDeployments.length === 0 && <TableRow><TableCell colSpan={5} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 2 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>サービス</TableCell><TableCell>メトリクス</TableCell><TableCell>値/閾値</TableCell><TableCell>重大度</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
            <TableBody>
              {monitoringAlerts.map((a) => (
                <TableRow key={a.id} hover>
                  <TableCell>{a.service}</TableCell>
                  <TableCell>{a.metric}</TableCell>
                  <TableCell>{a.value} / {a.threshold}</TableCell>
                  <TableCell><Chip label={a.severity} color={getSeverityColor(a.severity) as any} size="small" /></TableCell>
                  <TableCell><Chip label={a.status} size="small" color={a.status !== '対応済' ? 'warning' : 'default'} /></TableCell>
                </TableRow>
              ))}
              {monitoringAlerts.length === 0 && <TableRow><TableCell colSpan={5} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 3 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>種別</TableCell><TableCell>リソース</TableCell><TableCell>節約見込(円)</TableCell><TableCell>アクション</TableCell></TableRow></TableHead>
            <TableBody>
              {optimizationRecs.map((r) => (
                <TableRow key={r.id} hover>
                  <TableCell>{r.type}</TableCell>
                  <TableCell>{r.resource}</TableCell>
                  <TableCell>¥{r.saving_estimate.toLocaleString()}</TableCell>
                  <TableCell>{r.action}</TableCell>
                </TableRow>
              ))}
              {optimizationRecs.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 4 && (
        <Box>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip label="IaC" onClick={() => { const p = loadLearnProgress(); setLearnType(0); setLearnStep(p['infraOps_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 0 ? 'primary' : 'default'} variant={learnType === 0 ? 'filled' : 'outlined'} />
            <Chip label="オーケストレーション" onClick={() => { const p = loadLearnProgress(); setLearnType(1); setLearnStep(p['infraOps_1'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 1 ? 'primary' : 'default'} variant={learnType === 1 ? 'filled' : 'outlined'} />
            <Chip label="監視" onClick={() => { const p = loadLearnProgress(); setLearnType(2); setLearnStep(p['infraOps_2'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 2 ? 'primary' : 'default'} variant={learnType === 2 ? 'filled' : 'outlined'} />
            <Chip label="最適化" onClick={() => { const p = loadLearnProgress(); setLearnType(3); setLearnStep(p['infraOps_3'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 3 ? 'primary' : 'default'} variant={learnType === 3 ? 'filled' : 'outlined'} />
          </Stack>
          <LearnPanel steps={steps} stepIndex={learnStep} setStepIndex={setLearnStep} selected={learnSelected} setSelected={setLearnSelected} feedback={learnFeedback} setFeedback={setLearnFeedback} onReset={() => { setLearnStep(0); setLearnSelected(null); setLearnFeedback(null); }} />
        </Box>
      )}
    </>
  );
}
