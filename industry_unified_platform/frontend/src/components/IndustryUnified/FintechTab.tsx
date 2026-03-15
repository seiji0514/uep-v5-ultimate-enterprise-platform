/**
 * 金融・FinTech タブ
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
  TextField,
  Button,
} from '@mui/material';
import { Payment, Security, Visibility, Science, School } from '@mui/icons-material';
import type { Payment as PaymentType, RiskScore, TransactionMonitoring } from '../../api';
import { LearnPanel } from './LearnPanel';
import { loadLearnProgress } from './utils';
import { getStatusColor, getRiskColor } from './utils';
import {
  FINTECH_LEARN_PAYMENT,
  FINTECH_LEARN_RISK,
  FINTECH_LEARN_MONITOR,
  FINTECH_LEARN_STRESS,
} from './learnSteps';

export interface FintechTabProps {
  payments: PaymentType[];
  riskScores: RiskScore[];
  monitoring: TransactionMonitoring[];
  stressResult: any;
  portfolioValue: number;
  setPortfolioValue: (v: number) => void;
  loading: boolean;
  onStressTest: () => void;
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

export function FintechTab({
  payments,
  riskScores,
  monitoring,
  stressResult,
  portfolioValue,
  setPortfolioValue,
  loading,
  onStressTest,
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
}: FintechTabProps) {
  const steps = learnType === 0 ? FINTECH_LEARN_PAYMENT : learnType === 1 ? FINTECH_LEARN_RISK : learnType === 2 ? FINTECH_LEARN_MONITOR : FINTECH_LEARN_STRESS;

  return (
    <>
      <Typography variant="h6" gutterBottom>金融・FinTech</Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        決済・リスクスコア・取引監視・ストレステスト（規制対応）。高リスク・要確認取引は要対応です。
      </Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">決済</Typography><Typography variant="h5">{payments.length}</Typography><Typography variant="caption" color="error">処理中: {payments.filter((p) => p.status === '処理中').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">リスクスコア</Typography><Typography variant="h5">{riskScores.length}</Typography><Typography variant="caption" color="error">高: {riskScores.filter((r) => r.level === '高').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">取引監視</Typography><Typography variant="h5">{monitoring.length}</Typography><Typography variant="caption" color="error">要確認: {monitoring.filter((m) => m.status === '要確認').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">ストレステスト</Typography><Typography variant="body2">規制対応</Typography></CardContent></Card></Grid>
      </Grid>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip icon={<Payment />} label="決済" onClick={() => setSubTab(0)} color={subTab === 0 ? 'primary' : 'default'} />
        <Chip icon={<Security />} label="リスクスコア" onClick={() => setSubTab(1)} color={subTab === 1 ? 'primary' : 'default'} />
        <Chip icon={<Visibility />} label="取引監視" onClick={() => setSubTab(2)} color={subTab === 2 ? 'primary' : 'default'} />
        <Chip icon={<Science />} label="ストレステスト" onClick={() => setSubTab(3)} color={subTab === 3 ? 'primary' : 'default'} />
        <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSubTab(4); setLearnType(0); setLearnStep(p['fintech_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={subTab === 4 ? 'primary' : 'default'} />
      </Stack>
      {subTab === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>ID</TableCell><TableCell>金額</TableCell><TableCell>通貨</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
            <TableBody>
              {payments.map((p) => (
                <TableRow key={p.id} hover>
                  <TableCell>{p.id}</TableCell>
                  <TableCell>{p.amount.toLocaleString()}</TableCell>
                  <TableCell>{p.currency}</TableCell>
                  <TableCell><Chip label={p.status} size="small" color={getStatusColor(p.status) as any} /></TableCell>
                </TableRow>
              ))}
              {payments.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>取引ID</TableCell><TableCell>リスクスコア</TableCell><TableCell>レベル</TableCell><TableCell>要因</TableCell></TableRow></TableHead>
            <TableBody>
              {riskScores.map((r) => (
                <TableRow key={r.transaction_id} hover>
                  <TableCell>{r.transaction_id}</TableCell>
                  <TableCell>{(r.risk_score * 100).toFixed(0)}%</TableCell>
                  <TableCell><Chip label={r.level} color={getRiskColor(r.level) as any} size="small" /></TableCell>
                  <TableCell>{r.factors?.join(', ') || '-'}</TableCell>
                </TableRow>
              ))}
              {riskScores.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 2 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>種別</TableCell><TableCell>金額</TableCell><TableCell>ステータス</TableCell><TableCell>アラート</TableCell></TableRow></TableHead>
            <TableBody>
              {monitoring.map((m) => (
                <TableRow key={m.id} hover>
                  <TableCell>{m.type}</TableCell>
                  <TableCell>¥{m.amount.toLocaleString()}</TableCell>
                  <TableCell><Chip label={m.status} size="small" color={getStatusColor(m.status) as any} /></TableCell>
                  <TableCell>{m.alert || '-'}</TableCell>
                </TableRow>
              ))}
              {monitoring.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 3 && (
        <Stack spacing={2}>
          <Stack direction="row" spacing={2} alignItems="center">
            <TextField type="number" label="ポートフォリオ価値（円）" value={portfolioValue} onChange={(e) => setPortfolioValue(Number(e.target.value) || 1000000)} size="small" sx={{ width: 220 }} />
            <Button variant="contained" onClick={onStressTest} disabled={loading}>ストレステスト実行</Button>
          </Stack>
          {stressResult && (
            <Card variant="outlined">
              <CardContent>
                <Typography variant="subtitle1" fontWeight={600} gutterBottom>結果</Typography>
                <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>{JSON.stringify(stressResult, null, 2)}</Typography>
              </CardContent>
            </Card>
          )}
        </Stack>
      )}
      {subTab === 4 && (
        <Box>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip label="決済" onClick={() => { const p = loadLearnProgress(); setLearnType(0); setLearnStep(p['fintech_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 0 ? 'primary' : 'default'} variant={learnType === 0 ? 'filled' : 'outlined'} />
            <Chip label="リスクスコア" onClick={() => { const p = loadLearnProgress(); setLearnType(1); setLearnStep(p['fintech_1'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 1 ? 'primary' : 'default'} variant={learnType === 1 ? 'filled' : 'outlined'} />
            <Chip label="取引監視" onClick={() => { const p = loadLearnProgress(); setLearnType(2); setLearnStep(p['fintech_2'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 2 ? 'primary' : 'default'} variant={learnType === 2 ? 'filled' : 'outlined'} />
            <Chip label="ストレステスト" onClick={() => { const p = loadLearnProgress(); setLearnType(3); setLearnStep(p['fintech_3'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 3 ? 'primary' : 'default'} variant={learnType === 3 ? 'filled' : 'outlined'} />
          </Stack>
          <LearnPanel steps={steps} stepIndex={learnStep} setStepIndex={setLearnStep} selected={learnSelected} setSelected={setLearnSelected} feedback={learnFeedback} setFeedback={setLearnFeedback} onReset={() => { setLearnStep(0); setLearnSelected(null); setLearnFeedback(null); }} />
        </Box>
      )}
    </>
  );
}
