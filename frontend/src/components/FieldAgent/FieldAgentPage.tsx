/**
 * 現場AIエージェント ページ
 * 製造・医療・物流の現場向け簡易UI（タブレット・スマホ対応）
 * 6モジュール統合基盤のAPIを利用
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Chip,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  PrecisionManufacturing,
  LocalHospital,
  LocalShipping,
  Warning,
  CheckCircle,
  Schedule,
} from '@mui/icons-material';
import { manufacturingApi, Anomaly, PredictiveMaintenance } from '../../api/manufacturing';
import { medicalApi, MedicalAnomaly, PlatformStats } from '../../api/medical';
import { supplyChainApi, LogisticsShipment, InventoryItem } from '../../api/supplyChain';
import { useAutoPlayNarration } from '../../hooks/useAutoPlayNarration';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  );
}

export const FieldAgentPage: React.FC = () => {
  useAutoPlayNarration(8);
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // 製造
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [predictive, setPredictive] = useState<PredictiveMaintenance[]>([]);

  // 医療
  const [medicalAnomalies, setMedicalAnomalies] = useState<MedicalAnomaly[]>([]);
  const [platformStats, setPlatformStats] = useState<PlatformStats | null>(null);

  // 物流
  const [logistics, setLogistics] = useState<LogisticsShipment[]>([]);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) {
        const [anom, pm] = await Promise.all([
          manufacturingApi.getAnomalies(),
          manufacturingApi.getPredictiveMaintenance(),
        ]);
        setAnomalies(anom);
        setPredictive(pm);
      } else if (tabValue === 1) {
        const [anom, stats] = await Promise.all([
          medicalApi.getAnomalyDetection(),
          medicalApi.getPlatformStats(),
        ]);
        setMedicalAnomalies(anom);
        setPlatformStats(stats);
      } else {
        const [log, inv] = await Promise.all([
          supplyChainApi.getLogistics(),
          supplyChainApi.getInventory(),
        ]);
        setLogistics(log);
        setInventory(inv);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : '読み込みに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const criticalAnomalies = anomalies.filter((a) => a.severity === 'critical' || a.severity === 'high');
  const urgentPredictive = predictive.filter((p) => p.status === 'urgent' || p.confidence > 0.8);
  const criticalMedical = medicalAnomalies.filter((m) => m.severity === 'critical' || m.severity === 'high');
  const lowStock = inventory.filter((i) => i.qty <= i.reorder_level);
  const inTransitLogistics = logistics.filter((l) => l.status === '通関中' || l.status === '配送中');

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto' }}>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
        現場AIエージェント
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        製造・医療・物流の現場向け簡易ビュー（タブレット・スマホ対応）
      </Typography>

      <Paper sx={{ mb: 2 }}>
        <Tabs
          value={tabValue}
          onChange={(_, v) => setTabValue(v)}
          variant="fullWidth"
          sx={{ minHeight: 56, '& .MuiTab-root': { minHeight: 56, py: 1.5 } }}
        >
          <Tab icon={<PrecisionManufacturing />} iconPosition="start" label="製造" />
          <Tab icon={<LocalHospital />} iconPosition="start" label="医療" />
          <Tab icon={<LocalShipping />} iconPosition="start" label="物流" />
        </Tabs>

        {error && (
          <Alert severity="error" sx={{ mx: 2, mt: 1 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress aria-label="読み込み中" />
          </Box>
        ) : (
          <>
            <TabPanel value={tabValue} index={0}>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {criticalAnomalies.length > 0 && (
                  <Card variant="outlined" sx={{ borderColor: 'error.main', borderWidth: 2 }}>
                    <CardContent>
                      <Typography variant="subtitle2" color="error" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                        <Warning /> 異常検知（{criticalAnomalies.length}件）
                      </Typography>
                      <List dense>
                        {criticalAnomalies.slice(0, 5).map((a) => (
                          <ListItem key={a.id}>
                            <ListItemIcon sx={{ minWidth: 36 }}>
                              <Warning color="error" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText
                              primary={`${a.equipment} - ${a.type}`}
                              secondary={`${a.severity} / ${new Date(a.detected_at).toLocaleString('ja-JP')}`}
                            />
                            <Chip label={a.severity} size="small" color="error" />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                )}
                {urgentPredictive.length > 0 && (
                  <Card variant="outlined" sx={{ borderColor: 'warning.main', borderWidth: 1 }}>
                    <CardContent>
                      <Typography variant="subtitle2" color="warning.main" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                        <Schedule /> 予知保全（要対応 {urgentPredictive.length}件）
                      </Typography>
                      <List dense>
                        {urgentPredictive.slice(0, 5).map((p) => (
                          <ListItem key={p.id}>
                            <ListItemIcon sx={{ minWidth: 36 }}>
                              <PrecisionManufacturing fontSize="small" />
                            </ListItemIcon>
                            <ListItemText
                              primary={p.equipment}
                              secondary={`${p.predicted_failure} / 信頼度 ${(p.confidence * 100).toFixed(0)}%`}
                            />
                            <Chip label={p.status} size="small" color="warning" />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                )}
                {criticalAnomalies.length === 0 && urgentPredictive.length === 0 && (
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <CheckCircle color="success" /> 異常・要対応なし
                      </Typography>
                    </CardContent>
                  </Card>
                )}
              </Box>
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {platformStats && (
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="subtitle2" sx={{ mb: 1 }}>本日の統計</Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        <Chip label={`AI診断 ${platformStats.ai_diagnosis_today}件`} size="small" />
                        <Chip label={`音声処理 ${platformStats.voice_processed_today}件`} size="small" />
                        <Chip label={`異常検知 ${platformStats.anomalies_detected_today}件`} size="small" color="warning" />
                      </Box>
                    </CardContent>
                  </Card>
                )}
                {criticalMedical.length > 0 && (
                  <Card variant="outlined" sx={{ borderColor: 'error.main', borderWidth: 2 }}>
                    <CardContent>
                      <Typography variant="subtitle2" color="error" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                        <Warning /> 医療異常検知（{criticalMedical.length}件）
                      </Typography>
                      <List dense>
                        {criticalMedical.slice(0, 5).map((a) => (
                          <ListItem key={a.id}>
                            <ListItemIcon sx={{ minWidth: 36 }}>
                              <Warning color="error" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText
                              primary={`患者 ${a.patient_id} - ${a.type}`}
                              secondary={`${a.metric}: ${a.value} (閾値 ${a.threshold})`}
                            />
                            <Chip label={a.severity} size="small" color="error" />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                )}
                {criticalMedical.length === 0 && (
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <CheckCircle color="success" /> 医療異常なし
                      </Typography>
                    </CardContent>
                  </Card>
                )}
              </Box>
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {inTransitLogistics.length > 0 && (
                  <Card variant="outlined" sx={{ borderColor: 'info.main', borderWidth: 1 }}>
                    <CardContent>
                      <Typography variant="subtitle2" color="info.main" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                        <LocalShipping /> 配送中・監視対象（{inTransitLogistics.length}件）
                      </Typography>
                      <List dense>
                        {inTransitLogistics.slice(0, 5).map((l) => (
                          <ListItem key={l.id}>
                            <ListItemIcon sx={{ minWidth: 36 }}>
                              <LocalShipping fontSize="small" />
                            </ListItemIcon>
                            <ListItemText
                              primary={`${l.origin} → ${l.destination}`}
                              secondary={`${l.carrier} / ETA ${new Date(l.eta).toLocaleString('ja-JP')}`}
                            />
                            <Chip label={l.status} size="small" color="info" />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                )}
                {lowStock.length > 0 && (
                  <Card variant="outlined" sx={{ borderColor: 'error.main', borderWidth: 1 }}>
                    <CardContent>
                      <Typography variant="subtitle2" color="error" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                        <Warning /> 在庫切れ・要発注（{lowStock.length}件）
                      </Typography>
                      <List dense>
                        {lowStock.slice(0, 5).map((i) => (
                          <ListItem key={i.id}>
                            <ListItemIcon sx={{ minWidth: 36 }}>
                              <Warning color="error" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText
                              primary={`${i.name} (${i.sku})`}
                              secondary={`在庫 ${i.qty} / 発注点 ${i.reorder_level} - ${i.warehouse}`}
                            />
                            <Chip label={i.status} size="small" color="error" />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                )}
                {inTransitLogistics.length === 0 && lowStock.length === 0 && (
                  <Card variant="outlined">
                    <CardContent>
                      <Typography color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <CheckCircle color="success" /> 物流・在庫に問題なし
                      </Typography>
                    </CardContent>
                  </Card>
                )}
              </Box>
            </TabPanel>
          </>
        )}
      </Paper>
    </Box>
  );
};
