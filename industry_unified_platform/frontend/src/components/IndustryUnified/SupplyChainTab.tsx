/**
 * サプライチェーン系 タブ
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
import { LocalShipping, Inventory, Payment, Timeline, School } from '@mui/icons-material';
import type { LogisticsShipment, InventoryItem, ProcurementOrder, DemandForecast } from '../../api';
import { LearnPanel } from './LearnPanel';
import { loadLearnProgress } from './utils';
import {
  SUPPLY_CHAIN_LEARN_LOGISTICS,
  SUPPLY_CHAIN_LEARN_INV,
  SUPPLY_CHAIN_LEARN_PROC,
  SUPPLY_CHAIN_LEARN_DEMAND,
} from './learnSteps';

export interface SupplyChainTabProps {
  logisticsShipments: LogisticsShipment[];
  inventoryItems: InventoryItem[];
  procurementOrders: ProcurementOrder[];
  demandForecast: DemandForecast[];
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

export function SupplyChainTab({
  logisticsShipments,
  inventoryItems,
  procurementOrders,
  demandForecast,
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
}: SupplyChainTabProps) {
  const steps = learnType === 0 ? SUPPLY_CHAIN_LEARN_LOGISTICS : learnType === 1 ? SUPPLY_CHAIN_LEARN_INV : learnType === 2 ? SUPPLY_CHAIN_LEARN_PROC : SUPPLY_CHAIN_LEARN_DEMAND;

  return (
    <>
      <Typography variant="h6" gutterBottom>サプライチェーン系</Typography>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
        物流、在庫、調達、需要予測。要発注の在庫は要対応です。
      </Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">配送中</Typography><Typography variant="h5">{logisticsShipments.filter((s) => s.status !== '入荷済').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">在庫SKU</Typography><Typography variant="h5">{inventoryItems.length}</Typography><Typography variant="caption" color="error">要発注: {inventoryItems.filter((i) => i.status === '要発注').length}</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">調達金額</Typography><Typography variant="h5">¥{(procurementOrders.reduce((s, p) => s + p.amount, 0) / 10000).toFixed(0)}万</Typography></CardContent></Card></Grid>
        <Grid item xs={3}><Card variant="outlined"><CardContent><Typography variant="body2" color="text.secondary">在庫総数</Typography><Typography variant="h5">{inventoryItems.reduce((s, i) => s + i.qty, 0).toLocaleString()}</Typography></CardContent></Card></Grid>
      </Grid>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip icon={<LocalShipping />} label="物流" onClick={() => setSubTab(0)} color={subTab === 0 ? 'primary' : 'default'} />
        <Chip icon={<Inventory />} label="在庫" onClick={() => setSubTab(1)} color={subTab === 1 ? 'primary' : 'default'} />
        <Chip icon={<Payment />} label="調達" onClick={() => setSubTab(2)} color={subTab === 2 ? 'primary' : 'default'} />
        <Chip icon={<Timeline />} label="需要予測" onClick={() => setSubTab(3)} color={subTab === 3 ? 'primary' : 'default'} />
        <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSubTab(4); setLearnType(0); setLearnStep(p['supplyChain_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={subTab === 4 ? 'primary' : 'default'} />
      </Stack>
      {subTab === 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>発送元</TableCell><TableCell>宛先</TableCell><TableCell>ステータス</TableCell><TableCell>到着予定</TableCell></TableRow></TableHead>
            <TableBody>
              {logisticsShipments.map((s) => (
                <TableRow key={s.id} hover>
                  <TableCell>{s.origin}</TableCell>
                  <TableCell>{s.destination}</TableCell>
                  <TableCell><Chip label={s.status} size="small" /></TableCell>
                  <TableCell>{s.eta ? new Date(s.eta).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {logisticsShipments.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>SKU</TableCell><TableCell>品名</TableCell><TableCell>在庫数</TableCell><TableCell>発注点</TableCell><TableCell>ステータス</TableCell></TableRow></TableHead>
            <TableBody>
              {inventoryItems.map((i) => (
                <TableRow key={i.id} hover>
                  <TableCell>{i.sku}</TableCell>
                  <TableCell>{i.name}</TableCell>
                  <TableCell>{i.qty.toLocaleString()}</TableCell>
                  <TableCell>{i.reorder_level}</TableCell>
                  <TableCell><Chip label={i.status} size="small" color={i.status === '要発注' ? 'error' : 'default'} /></TableCell>
                </TableRow>
              ))}
              {inventoryItems.length === 0 && <TableRow><TableCell colSpan={5} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 2 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>サプライヤー</TableCell><TableCell>金額</TableCell><TableCell>ステータス</TableCell><TableCell>納期</TableCell></TableRow></TableHead>
            <TableBody>
              {procurementOrders.map((p) => (
                <TableRow key={p.id} hover>
                  <TableCell>{p.supplier}</TableCell>
                  <TableCell>¥{p.amount.toLocaleString()}</TableCell>
                  <TableCell><Chip label={p.status} size="small" /></TableCell>
                  <TableCell>{p.delivery_date ? new Date(p.delivery_date).toLocaleString('ja-JP') : '-'}</TableCell>
                </TableRow>
              ))}
              {procurementOrders.length === 0 && <TableRow><TableCell colSpan={4} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 3 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead><TableRow><TableCell>SKU</TableCell><TableCell>期間</TableCell><TableCell>予測</TableCell><TableCell>前回実績</TableCell><TableCell>精度</TableCell></TableRow></TableHead>
            <TableBody>
              {demandForecast.map((d, idx) => (
                <TableRow key={idx} hover>
                  <TableCell>{d.sku}</TableCell>
                  <TableCell>{d.period}</TableCell>
                  <TableCell>{d.forecast.toLocaleString()}</TableCell>
                  <TableCell>{d.actual_last.toLocaleString()}</TableCell>
                  <TableCell>{(d.accuracy * 100).toFixed(0)}%</TableCell>
                </TableRow>
              ))}
              {demandForecast.length === 0 && <TableRow><TableCell colSpan={5} align="center">データがありません</TableCell></TableRow>}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      {subTab === 4 && (
        <Box>
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip label="物流" onClick={() => { const p = loadLearnProgress(); setLearnType(0); setLearnStep(p['supplyChain_0'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 0 ? 'primary' : 'default'} variant={learnType === 0 ? 'filled' : 'outlined'} />
            <Chip label="在庫" onClick={() => { const p = loadLearnProgress(); setLearnType(1); setLearnStep(p['supplyChain_1'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 1 ? 'primary' : 'default'} variant={learnType === 1 ? 'filled' : 'outlined'} />
            <Chip label="調達" onClick={() => { const p = loadLearnProgress(); setLearnType(2); setLearnStep(p['supplyChain_2'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 2 ? 'primary' : 'default'} variant={learnType === 2 ? 'filled' : 'outlined'} />
            <Chip label="需要予測" onClick={() => { const p = loadLearnProgress(); setLearnType(3); setLearnStep(p['supplyChain_3'] ?? 0); setLearnSelected(null); setLearnFeedback(null); }} color={learnType === 3 ? 'primary' : 'default'} variant={learnType === 3 ? 'filled' : 'outlined'} />
          </Stack>
          <LearnPanel steps={steps} stepIndex={learnStep} setStepIndex={setLearnStep} selected={learnSelected} setSelected={setLearnSelected} feedback={learnFeedback} setFeedback={setLearnFeedback} onReset={() => { setLearnStep(0); setLearnSelected(null); setLearnFeedback(null); }} />
        </Box>
      )}
    </>
  );
}
