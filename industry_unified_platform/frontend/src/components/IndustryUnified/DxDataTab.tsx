/**
 * DX・データ系 タブ
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
import { Storage, Science, Psychology, Timeline, School } from '@mui/icons-material';
import type { DataLakeCatalog, MlModel, GenerativeAiUsage, DataPipeline } from '../../api';
import { LearnPanel } from './LearnPanel';
import { loadLearnProgress } from './utils';
import {
  DX_DATA_LEARN_LAKE,
  DX_DATA_LEARN_ML,
  DX_DATA_LEARN_GENAI,
  DX_DATA_LEARN_PIPELINE,
} from './learnSteps';

export interface DxDataTabProps {
  dataLakeCatalogs: DataLakeCatalog[];
  mlModels: MlModel[];
  genaiUsage: GenerativeAiUsage[];
  dataPipelines: DataPipeline[];
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

export function DxDataTab({
  dataLakeCatalogs,
  mlModels,
  genaiUsage,
  dataPipelines,
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
}: DxDataTabProps) {
  const steps = learnType === 0 ? DX_DATA_LEARN_LAKE : learnType === 1 ? DX_DATA_LEARN_ML : learnType === 2 ? DX_DATA_LEARN_GENAI : DX_DATA_LEARN_PIPELINE;

  return (
    <>
      <Typography variant="h6" gutterBottom>DX・データ系</Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        データレイク、AI/ML、生成AI、パイプライン。失敗・待機中のパイプラインは要対応です。
      </Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">データレイク(GB)</Typography><Typography variant="h5">{dataLakeCatalogs.reduce((s, c) => s + c.size_gb, 0)}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">MLモデル</Typography><Typography variant="h5">{mlModels.length}</Typography><Typography variant="caption" color="text.secondary">本番: {mlModels.filter((m) => m.status === '本番').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">生成AI(トークン/日)</Typography><Typography variant="h5">{genaiUsage.reduce((s, g) => s + g.tokens_today, 0).toLocaleString()}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">パイプライン</Typography><Typography variant="h5">{dataPipelines.length}</Typography><Typography variant="caption" color="error">実行中: {dataPipelines.filter((p) => p.status === '実行中').length}</Typography></CardContent></Card></Grid>
      </Grid>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip icon={<Storage />} label="データレイク" onClick={() => setSubTab(0)} color={subTab === 0 ? 'primary' : 'default'} />
        <Chip icon={<Science />} label="MLモデル" onClick={() => setSubTab(1)} color={subTab === 1 ? 'primary' : 'default'} />
        <Chip icon={<Psychology />} label="生成AI" onClick={() => setSubTab(2)} color={subTab === 2 ? 'primary' : 'default'} />
        <Chip icon={<Timeline />} label="パイプライン" onClick={() => setSubTab(3)} color={subTab === 3 ? 'primary' : 'default'} />
        <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSubTab(4); setLearnType(0); setLearnStep(p['dxData_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={subTab === 4 ? 'primary' : 'default'} />
      </Stack>
      {subTab === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>カタログ</TableCell><TableCell>サイズ(GB)</TableCell><TableCell>レコード数</TableCell><TableCell>最終取り込み</TableCell></TableRow></TableHead>
            <TableBody>
              {dataLakeCatalogs.map((c) => (
                <TableRow key={c.id} hover>
                  <TableCell>{c.name}</TableCell>
                  <TableCell>{c.size_gb.toLocaleString()}</TableCell>
                  <TableCell>{c.records.toLocaleString()}</TableCell>
                  <TableCell>{c.last_ingest ? new Date(c.last_ingest).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {dataLakeCatalogs.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>モデル</TableCell><TableCell>精度</TableCell><TableCell>ステータス</TableCell><TableCell>推論数(今日)</TableCell></TableRow></TableHead>
            <TableBody>
              {mlModels.map((m) => (
                <TableRow key={m.id} hover>
                  <TableCell>{m.name}</TableCell>
                  <TableCell>{(m.accuracy * 100).toFixed(0)}%</TableCell>
                  <TableCell><Chip label={m.status} size="small" /></TableCell>
                  <TableCell>{m.inference_count_today.toLocaleString()}</TableCell>
                </TableRow>
              ))}
              {mlModels.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 2 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>操作</TableCell><TableCell>モデル</TableCell><TableCell>トークン(今日)</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
            <TableBody>
              {genaiUsage.map((g) => (
                <TableRow key={g.id} hover>
                  <TableCell>{g.operation}</TableCell>
                  <TableCell>{g.model}</TableCell>
                  <TableCell>{g.tokens_today.toLocaleString()}</TableCell>
                  <TableCell><Chip label={g.status} size="small" /></TableCell>
                </TableRow>
              ))}
              {genaiUsage.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 3 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>パイプライン</TableCell><TableCell>スケジュール</TableCell><TableCell>ステータス</TableCell><TableCell>最終実行</TableCell></TableRow></TableHead>
            <TableBody>
              {dataPipelines.map((p) => (
                <TableRow key={p.id} hover>
                  <TableCell>{p.name}</TableCell>
                  <TableCell>{p.schedule}</TableCell>
                  <TableCell><Chip label={p.status} size="small" color={p.status === '失敗' ? 'error' : p.status === '実行中' ? 'success' : 'default'} /></TableCell>
                  <TableCell>{p.last_run ? new Date(p.last_run).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {dataPipelines.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 4 && (
        <Box>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip label="データレイク" onClick={() => { const p = loadLearnProgress(); setLearnType(0); setLearnStep(p['dxData_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 0 ? 'primary' : 'default'} variant={learnType === 0 ? 'filled' : 'outlined'} />
            <Chip label="MLモデル" onClick={() => { const p = loadLearnProgress(); setLearnType(1); setLearnStep(p['dxData_1'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 1 ? 'primary' : 'default'} variant={learnType === 1 ? 'filled' : 'outlined'} />
            <Chip label="生成AI" onClick={() => { const p = loadLearnProgress(); setLearnType(2); setLearnStep(p['dxData_2'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 2 ? 'primary' : 'default'} variant={learnType === 2 ? 'filled' : 'outlined'} />
            <Chip label="パイプライン" onClick={() => { const p = loadLearnProgress(); setLearnType(3); setLearnStep(p['dxData_3'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 3 ? 'primary' : 'default'} variant={learnType === 3 ? 'filled' : 'outlined'} />
          </Stack>
          <LearnPanel steps={steps} stepIndex={learnStep} setStepIndex={setLearnStep} selected={learnSelected} setSelected={setLearnSelected} feedback={learnFeedback} setFeedback={setLearnFeedback} onReset={() => { setLearnStep(0); setLearnSelected(null); setLearnFeedback(null); }} />
        </Box>
      )}
    </>
  );
}
