/**
 * 産業統合プラットフォーム
 * 製造・IoT + 医療・ヘルスケア + 金融・FinTech + 統合セキュリティ・防衛 を1つに統合
 */
import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  Box,
  Typography,
  Paper,
  Stack,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Tab,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tooltip,
  useTheme,
  useMediaQuery,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormGroup,
  FormControlLabel,
  Checkbox,
  IconButton,
  Slider,
} from '@mui/material';
import {
  PrecisionManufacturing,
  LocalHospital,
  AccountBalance,
  Shield,
  Refresh,
  PlayArrow,
  TouchApp,
  FormatListNumbered,
  Cloud,
  Storage,
  Gavel,
  LocalShipping,
  Settings,
  UploadFile,
  Stop,
} from '@mui/icons-material';
import { speakSequence, cancelSpeech } from '../lib/speech';
import {
  manufacturingApi,
  medicalApi,
  fintechApi,
  securityCenterApi,
  infraOpsApi,
  dxDataApi,
  complianceGovernanceApi,
  supplyChainApi,
  dataIntegrationApi,
  getApiBaseUrl,
  type PredictiveMaintenance,
  type SensorData,
  type Anomaly,
  type AIDiagnosis,
  type VoiceResponse,
  type MedicalAnomaly,
  type PlatformStats,
  type Payment as PaymentType,
  type RiskScore,
  type TransactionMonitoring,
  type SecurityEvent,
  type SecurityIncident,
  type SecurityRisk,
  type IacProject,
  type MonitoringAlert,
  type OrchestrationDeployment,
  type OptimizationRecommendation,
  type DataLakeCatalog,
  type MlModel,
  type GenerativeAiUsage,
  type DataPipeline,
  type RegulatoryItem,
  type AuditLog,
  type GovernancePolicy,
  type AuditFinding,
  type LogisticsShipment,
  type InventoryItem,
  type ProcurementOrder,
  type DemandForecast,
} from '../api';
import {
  TabPanel,
  ManufacturingTab,
  MedicalTab,
  FintechTab,
  SecurityTab,
  InfraOpsTab,
  DxDataTab,
  ComplianceTab,
  SupplyChainTab,
  loadLearnProgress,
  saveLearnProgress,
} from './IndustryUnified';

type SimMode = 'auto' | 'manual';
const AUTO_INTERVAL_OPTIONS = [5, 10, 30] as const;
const PRACTICE_INTERVAL_OPTIONS = [5, 10, 15, 30] as const;

const DOMAIN_LABELS: Record<number, string> = {
  0: 'manufacturing', 1: 'medical', 2: 'fintech', 3: 'security',
  4: 'infra_ops', 5: 'dx_data', 6: 'compliance_governance', 7: 'supply_chain',
};

const DEMO_NARRATION_INTRO = '本データはデモ用サンプルです。実データの連携は、CSVや既存DBからの取り込みは比較的容易ですが、実機センサーや医療・金融の本番システムとの連携は、規制やセキュリティの観点から難易度が高くなります。';

const DEMO_NARRATION: string[] = [
  '製造・IoTです。予知保全、センサーデータ、異常検知を提供しています。',
  '医療・ヘルスケアです。AI診断、音声応答、異常検知を提供しています。',
  '金融・FinTechです。決済、リスクスコア、取引監視、ストレステストを提供しています。',
  '統合セキュリティ・防衛です。イベント、インシデント、リスクを管理しています。',
  'インフラ・運用系です。IaC、オーケストレーション、監視、FinOpsを提供しています。',
  'DX・データ系です。データレイク、MLモデル、生成AI、パイプラインを管理しています。',
  'コンプライアンス・ガバナンスです。規制対応、監査ログ、ポリシー、監査指摘を管理しています。',
  'サプライチェーンです。物流、在庫、調達、需要予測を提供しています。',
];

type IndustryType = 'general' | 'manufacturing' | 'medical' | 'financial' | 'sier' | 'dx';
const INDUSTRY_DEFAULT_TAB: Record<IndustryType, number> = {
  general: 0, manufacturing: 0, medical: 1, financial: 2, sier: 4, dx: 5,
};

export const IndustryUnifiedPlatformPage: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [industryType, setIndustryType] = useState<IndustryType>(() => {
    try {
      const v = localStorage.getItem('industry_type') as IndustryType | null;
      if (v && ['general', 'manufacturing', 'medical', 'financial', 'sier', 'dx'].includes(v)) return v;
    } catch { /* ignore */ }
    return 'general';
  });
  const [domainTab, setDomainTab] = useState(() => {
    try {
      const v = localStorage.getItem('industry_type') as IndustryType | null;
      if (v && ['general', 'manufacturing', 'medical', 'financial', 'sier', 'dx'].includes(v)) return INDUSTRY_DEFAULT_TAB[v];
    } catch { /* ignore */ }
    return 0;
  });
  const [simMode, setSimMode] = useState<SimMode>('manual');
  const [autoIntervalSec, setAutoIntervalSec] = useState(5);
  const [practiceMode, setPracticeMode] = useState(false);
  const [practiceIntervalSec, setPracticeIntervalSec] = useState(10);
  const [practiceDomainIndices, setPracticeDomainIndices] = useState<number[]>(() => {
    try {
      const raw = localStorage.getItem('industry_unified_practice_domains');
      if (raw) {
        const arr = JSON.parse(raw);
        if (Array.isArray(arr) && arr.length > 0) return arr;
      }
    } catch { /* ignore */ }
    return [0, 1, 2, 3, 4, 5, 6, 7];
  });
  const [practiceConfigOpen, setPracticeConfigOpen] = useState(false);
  const [apiConfigOpen, setApiConfigOpen] = useState(false);
  const [apiBaseUrlInput, setApiBaseUrlInput] = useState('');
  const [csvImportOpen, setCsvImportOpen] = useState(false);
  const [csvData, setCsvData] = useState<string[][]>([]);
  const [csvError, setCsvError] = useState('');
  const [csvSaving, setCsvSaving] = useState(false);
  const [csvSaved, setCsvSaved] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isDemoPlaying, setIsDemoPlaying] = useState(false);
  const [demoNarrationEnabled, setDemoNarrationEnabled] = useState(true);
  const [demoScaleDown, setDemoScaleDown] = useState(false);
  const [demoNarrationRate, setDemoNarrationRate] = useState(() => {
    try {
      const v = parseFloat(localStorage.getItem('demo_narration_rate') || '0.9');
      return Math.max(0.5, Math.min(2, v)) || 0.9;
    } catch { return 0.9; }
  });
  const [demoIntervalSec, setDemoIntervalSec] = useState(() => {
    try {
      const v = parseInt(localStorage.getItem('demo_interval_sec') || '15', 10);
      return [10, 15, 20].includes(v) ? v : 15;
    } catch { return 15; }
  });
  const demoIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // 製造
  const [predictive, setPredictive] = useState<PredictiveMaintenance[]>([]);
  const [sensors, setSensors] = useState<SensorData[]>([]);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);

  // 医療
  const [aiDiagnosis, setAiDiagnosis] = useState<AIDiagnosis[]>([]);
  const [voiceResponse, setVoiceResponse] = useState<VoiceResponse[]>([]);
  const [medicalAnomalies, setMedicalAnomalies] = useState<MedicalAnomaly[]>([]);
  const [stats, setStats] = useState<PlatformStats | null>(null);

  // 金融
  const [payments, setPayments] = useState<PaymentType[]>([]);
  const [riskScores, setRiskScores] = useState<RiskScore[]>([]);
  const [monitoring, setMonitoring] = useState<TransactionMonitoring[]>([]);
  const [stressResult, setStressResult] = useState<any>(null);
  const [portfolioValue, setPortfolioValue] = useState(1000000);
  const [fintechSubTab, setFintechSubTab] = useState(0);
  const [manufacturingSubTab, setManufacturingSubTab] = useState(0);
  const [manufacturingLearnType, setManufacturingLearnType] = useState<0 | 1 | 2>(0); // 0=予知保全, 1=センサーデータ, 2=異常検知
  const [manufacturingLearnStep, setManufacturingLearnStep] = useState(0);
  const [manufacturingLearnSelected, setManufacturingLearnSelected] = useState<number | null>(null);
  const [manufacturingLearnFeedback, setManufacturingLearnFeedback] = useState<'correct' | 'wrong' | null>(null);
  const [medicalSubTab, setMedicalSubTab] = useState(0);
  const [medicalLearnType, setMedicalLearnType] = useState<0 | 1 | 2>(0);
  const [medicalLearnStep, setMedicalLearnStep] = useState(0);
  const [medicalLearnSelected, setMedicalLearnSelected] = useState<number | null>(null);
  const [medicalLearnFeedback, setMedicalLearnFeedback] = useState<'correct' | 'wrong' | null>(null);
  const [securitySubTab, setSecuritySubTab] = useState(0);
  const [fintechLearnType, setFintechLearnType] = useState<0 | 1 | 2 | 3>(0);
  const [fintechLearnStep, setFintechLearnStep] = useState(0);
  const [fintechLearnSelected, setFintechLearnSelected] = useState<number | null>(null);
  const [fintechLearnFeedback, setFintechLearnFeedback] = useState<'correct' | 'wrong' | null>(null);
  const [securityLearnType, setSecurityLearnType] = useState<0 | 1 | 2>(0);
  const [securityLearnStep, setSecurityLearnStep] = useState(0);
  const [securityLearnSelected, setSecurityLearnSelected] = useState<number | null>(null);
  const [securityLearnFeedback, setSecurityLearnFeedback] = useState<'correct' | 'wrong' | null>(null);

  // 統合セキュリティ・防衛
  const [securityEvents, setSecurityEvents] = useState<SecurityEvent[]>([]);
  const [securityIncidents, setSecurityIncidents] = useState<SecurityIncident[]>([]);
  const [securityRisks, setSecurityRisks] = useState<SecurityRisk[]>([]);

  // インフラ・運用系
  const [iacProjects, setIacProjects] = useState<IacProject[]>([]);
  const [monitoringAlerts, setMonitoringAlerts] = useState<MonitoringAlert[]>([]);
  const [orchestrationDeployments, setOrchestrationDeployments] = useState<OrchestrationDeployment[]>([]);
  const [optimizationRecs, setOptimizationRecs] = useState<OptimizationRecommendation[]>([]);
  const [infraOpsSubTab, setInfraOpsSubTab] = useState(0);
  const [infraOpsLearnType, setInfraOpsLearnType] = useState<0 | 1 | 2 | 3>(0);
  const [infraOpsLearnStep, setInfraOpsLearnStep] = useState(0);
  const [infraOpsLearnSelected, setInfraOpsLearnSelected] = useState<number | null>(null);
  const [infraOpsLearnFeedback, setInfraOpsLearnFeedback] = useState<'correct' | 'wrong' | null>(null);

  // DX・データ系
  const [dataLakeCatalogs, setDataLakeCatalogs] = useState<DataLakeCatalog[]>([]);
  const [mlModels, setMlModels] = useState<MlModel[]>([]);
  const [genaiUsage, setGenaiUsage] = useState<GenerativeAiUsage[]>([]);
  const [dataPipelines, setDataPipelines] = useState<DataPipeline[]>([]);
  const [dxDataSubTab, setDxDataSubTab] = useState(0);
  const [dxDataLearnType, setDxDataLearnType] = useState<0 | 1 | 2 | 3>(0);
  const [dxDataLearnStep, setDxDataLearnStep] = useState(0);
  const [dxDataLearnSelected, setDxDataLearnSelected] = useState<number | null>(null);
  const [dxDataLearnFeedback, setDxDataLearnFeedback] = useState<'correct' | 'wrong' | null>(null);

  // コンプライアンス・ガバナンス系
  const [regulatoryItems, setRegulatoryItems] = useState<RegulatoryItem[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [governancePolicies, setGovernancePolicies] = useState<GovernancePolicy[]>([]);
  const [auditFindings, setAuditFindings] = useState<AuditFinding[]>([]);
  const [complianceSubTab, setComplianceSubTab] = useState(0);
  const [complianceLearnType, setComplianceLearnType] = useState<0 | 1 | 2 | 3>(0);
  const [complianceLearnStep, setComplianceLearnStep] = useState(0);
  const [complianceLearnSelected, setComplianceLearnSelected] = useState<number | null>(null);
  const [complianceLearnFeedback, setComplianceLearnFeedback] = useState<'correct' | 'wrong' | null>(null);

  // サプライチェーン系
  const [logisticsShipments, setLogisticsShipments] = useState<LogisticsShipment[]>([]);
  const [inventoryItems, setInventoryItems] = useState<InventoryItem[]>([]);
  const [procurementOrders, setProcurementOrders] = useState<ProcurementOrder[]>([]);
  const [demandForecast, setDemandForecast] = useState<DemandForecast[]>([]);
  const [supplyChainSubTab, setSupplyChainSubTab] = useState(0);
  const [supplyChainLearnType, setSupplyChainLearnType] = useState<0 | 1 | 2 | 3>(0);
  const [supplyChainLearnStep, setSupplyChainLearnStep] = useState(0);
  const [supplyChainLearnSelected, setSupplyChainLearnSelected] = useState<number | null>(null);
  const [supplyChainLearnFeedback, setSupplyChainLearnFeedback] = useState<'correct' | 'wrong' | null>(null);

  // 実務学習の進捗保存: 初回マウント時にlocalStorageから復元
  const [progressLoaded, setProgressLoaded] = useState(false);
  useEffect(() => {
    if (progressLoaded) return;
    const p = loadLearnProgress();
    const get = (k: string) => Math.max(0, p[k] ?? 0);
    setManufacturingLearnStep(get('manufacturing_0'));
    setMedicalLearnStep(get('medical_0'));
    setFintechLearnStep(get('fintech_0'));
    setSecurityLearnStep(get('security_0'));
    setInfraOpsLearnStep(get('infraOps_0'));
    setDxDataLearnStep(get('dxData_0'));
    setComplianceLearnStep(get('compliance_0'));
    setSupplyChainLearnStep(get('supplyChain_0'));
    setProgressLoaded(true);
  }, [progressLoaded]);

  // 実務学習の進捗保存: ステップ変更時にlocalStorageへ保存
  const saveStep = useCallback((key: string, step: number) => {
    const p = loadLearnProgress();
    p[key] = step;
    saveLearnProgress(p);
  }, []);
  useEffect(() => {
    if (!progressLoaded) return;
    saveStep('manufacturing_' + manufacturingLearnType, manufacturingLearnStep);
  }, [progressLoaded, manufacturingLearnType, manufacturingLearnStep, saveStep]);
  useEffect(() => {
    if (!progressLoaded) return;
    saveStep('medical_' + medicalLearnType, medicalLearnStep);
  }, [progressLoaded, medicalLearnType, medicalLearnStep, saveStep]);
  useEffect(() => {
    if (!progressLoaded) return;
    saveStep('fintech_' + fintechLearnType, fintechLearnStep);
  }, [progressLoaded, fintechLearnType, fintechLearnStep, saveStep]);
  useEffect(() => {
    if (!progressLoaded) return;
    saveStep('security_' + securityLearnType, securityLearnStep);
  }, [progressLoaded, securityLearnType, securityLearnStep, saveStep]);
  useEffect(() => {
    if (!progressLoaded) return;
    saveStep('infraOps_' + infraOpsLearnType, infraOpsLearnStep);
  }, [progressLoaded, infraOpsLearnType, infraOpsLearnStep, saveStep]);
  useEffect(() => {
    if (!progressLoaded) return;
    saveStep('dxData_' + dxDataLearnType, dxDataLearnStep);
  }, [progressLoaded, dxDataLearnType, dxDataLearnStep, saveStep]);
  useEffect(() => {
    if (!progressLoaded) return;
    saveStep('compliance_' + complianceLearnType, complianceLearnStep);
  }, [progressLoaded, complianceLearnType, complianceLearnStep, saveStep]);
  useEffect(() => {
    if (!progressLoaded) return;
    saveStep('supplyChain_' + supplyChainLearnType, supplyChainLearnStep);
  }, [progressLoaded, supplyChainLearnType, supplyChainLearnStep, saveStep]);

  const loadedDomainsRef = useRef<Set<number>>(new Set());

  const loadDomain = useCallback(async (domainIndex: number, silent = false) => {
    try {
      if (!silent) setLoading(true);
      setError('');
      if (domainIndex === 0) {
        const [pm, sd, an] = await Promise.all([
          manufacturingApi.getPredictiveMaintenance(),
          manufacturingApi.getSensorData(),
          manufacturingApi.getAnomalies(),
        ]);
        setPredictive(pm.items || []);
        setSensors(sd.items || []);
        setAnomalies(an.items || []);
      } else if (domainIndex === 1) {
        const [diag, voice, anom, st] = await Promise.all([
          medicalApi.getAIDiagnosis(),
          medicalApi.getVoiceResponse(),
          medicalApi.getAnomalyDetection(),
          medicalApi.getPlatformStats(),
        ]);
        setAiDiagnosis(diag.items || []);
        setVoiceResponse(voice.items || []);
        setMedicalAnomalies(anom.items || []);
        setStats(st);
      } else if (domainIndex === 2) {
        const [pay, risk, mon] = await Promise.all([
          fintechApi.getPayments(),
          fintechApi.getRiskScores(),
          fintechApi.getTransactionMonitoring(),
        ]);
        setPayments(pay.items || []);
        setRiskScores(risk.items || []);
        setMonitoring(mon.items || []);
      } else if (domainIndex === 3) {
        const [secEv, secInc, secRisk] = await Promise.all([
          securityCenterApi.getEvents().catch(() => []),
          securityCenterApi.getIncidents().catch(() => []),
          securityCenterApi.getRisks().catch(() => []),
        ]);
        setSecurityEvents(Array.isArray(secEv) ? secEv : []);
        setSecurityIncidents(Array.isArray(secInc) ? secInc : []);
        setSecurityRisks(Array.isArray(secRisk) ? secRisk : []);
      } else if (domainIndex === 4) {
        const [iac, orch, alerts, opt] = await Promise.all([
          infraOpsApi.getIacProjects().catch(() => ({ items: [], total: 0 })),
          infraOpsApi.getOrchestrationDeployments().catch(() => ({ items: [], total: 0 })),
          infraOpsApi.getMonitoringAlerts().catch(() => ({ items: [], total: 0 })),
          infraOpsApi.getOptimizationRecommendations().catch(() => ({ items: [], total: 0 })),
        ]);
        setIacProjects(iac.items || []);
        setOrchestrationDeployments(orch.items || []);
        setMonitoringAlerts(alerts.items || []);
        setOptimizationRecs(opt.items || []);
      } else if (domainIndex === 5) {
        const [dl, ml, genai, pipes] = await Promise.all([
          dxDataApi.getDataLakeCatalogs().catch(() => ({ items: [], total: 0 })),
          dxDataApi.getMlModels().catch(() => ({ items: [], total: 0 })),
          dxDataApi.getGenerativeAiUsage().catch(() => ({ items: [], total: 0 })),
          dxDataApi.getDataPipelines().catch(() => ({ items: [], total: 0 })),
        ]);
        setDataLakeCatalogs(dl.items || []);
        setMlModels(ml.items || []);
        setGenaiUsage(genai.items || []);
        setDataPipelines(pipes.items || []);
      } else if (domainIndex === 6) {
        const [reg, audit, pol, find] = await Promise.all([
          complianceGovernanceApi.getRegulatoryItems().catch(() => ({ items: [], total: 0 })),
          complianceGovernanceApi.getAuditLogs().catch(() => ({ items: [], total: 0 })),
          complianceGovernanceApi.getGovernancePolicies().catch(() => ({ items: [], total: 0 })),
          complianceGovernanceApi.getAuditFindings().catch(() => ({ items: [], total: 0 })),
        ]);
        setRegulatoryItems(reg.items || []);
        setAuditLogs(audit.items || []);
        setGovernancePolicies(pol.items || []);
        setAuditFindings(find.items || []);
      } else if (domainIndex === 7) {
        const [ship, inv, proc, dem] = await Promise.all([
          supplyChainApi.getLogisticsShipments().catch(() => ({ items: [], total: 0 })),
          supplyChainApi.getInventoryItems().catch(() => ({ items: [], total: 0 })),
          supplyChainApi.getProcurementOrders().catch(() => ({ items: [], total: 0 })),
          supplyChainApi.getDemandForecast().catch(() => ({ items: [], total: 0 })),
        ]);
        setLogisticsShipments(ship.items || []);
        setInventoryItems(inv.items || []);
        setProcurementOrders(proc.items || []);
        setDemandForecast(dem.items || []);
      }
      loadedDomainsRef.current.add(domainIndex);
      setLastUpdated(new Date());
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      if (!silent) setLoading(false);
    }
  }, []);

  const loadAll = useCallback(async (silent = false) => {
    try {
      if (!silent) setLoading(true);
      setError('');
      const [
        pm, sd, an, diag, voice, anom, st, pay, risk, mon,
        secEv, secInc, secRisk,
        iac, orch, alerts, opt,
        dl, ml, genai, pipes,
        reg, audit, pol, find,
        ship, inv, proc, dem,
      ] = await Promise.all([
        manufacturingApi.getPredictiveMaintenance(),
        manufacturingApi.getSensorData(),
        manufacturingApi.getAnomalies(),
        medicalApi.getAIDiagnosis(),
        medicalApi.getVoiceResponse(),
        medicalApi.getAnomalyDetection(),
        medicalApi.getPlatformStats(),
        fintechApi.getPayments(),
        fintechApi.getRiskScores(),
        fintechApi.getTransactionMonitoring(),
        securityCenterApi.getEvents().catch(() => []),
        securityCenterApi.getIncidents().catch(() => []),
        securityCenterApi.getRisks().catch(() => []),
        infraOpsApi.getIacProjects().catch(() => ({ items: [], total: 0 })),
        infraOpsApi.getOrchestrationDeployments().catch(() => ({ items: [], total: 0 })),
        infraOpsApi.getMonitoringAlerts().catch(() => ({ items: [], total: 0 })),
        infraOpsApi.getOptimizationRecommendations().catch(() => ({ items: [], total: 0 })),
        dxDataApi.getDataLakeCatalogs().catch(() => ({ items: [], total: 0 })),
        dxDataApi.getMlModels().catch(() => ({ items: [], total: 0 })),
        dxDataApi.getGenerativeAiUsage().catch(() => ({ items: [], total: 0 })),
        dxDataApi.getDataPipelines().catch(() => ({ items: [], total: 0 })),
        complianceGovernanceApi.getRegulatoryItems().catch(() => ({ items: [], total: 0 })),
        complianceGovernanceApi.getAuditLogs().catch(() => ({ items: [], total: 0 })),
        complianceGovernanceApi.getGovernancePolicies().catch(() => ({ items: [], total: 0 })),
        complianceGovernanceApi.getAuditFindings().catch(() => ({ items: [], total: 0 })),
        supplyChainApi.getLogisticsShipments().catch(() => ({ items: [], total: 0 })),
        supplyChainApi.getInventoryItems().catch(() => ({ items: [], total: 0 })),
        supplyChainApi.getProcurementOrders().catch(() => ({ items: [], total: 0 })),
        supplyChainApi.getDemandForecast().catch(() => ({ items: [], total: 0 })),
      ]);
      setPredictive(pm.items || []);
      setSensors(sd.items || []);
      setAnomalies(an.items || []);
      setAiDiagnosis(diag.items || []);
      setVoiceResponse(voice.items || []);
      setMedicalAnomalies(anom.items || []);
      setStats(st);
      setPayments(pay.items || []);
      setRiskScores(risk.items || []);
      setMonitoring(mon.items || []);
      setSecurityEvents(Array.isArray(secEv) ? secEv : []);
      setSecurityIncidents(Array.isArray(secInc) ? secInc : []);
      setSecurityRisks(Array.isArray(secRisk) ? secRisk : []);
      setIacProjects(iac.items || []);
      setOrchestrationDeployments(orch.items || []);
      setMonitoringAlerts(alerts.items || []);
      setOptimizationRecs(opt.items || []);
      setDataLakeCatalogs(dl.items || []);
      setMlModels(ml.items || []);
      setGenaiUsage(genai.items || []);
      setDataPipelines(pipes.items || []);
      setRegulatoryItems(reg.items || []);
      setAuditLogs(audit.items || []);
      setGovernancePolicies(pol.items || []);
      setAuditFindings(find.items || []);
      setLogisticsShipments(ship.items || []);
      setInventoryItems(inv.items || []);
      setProcurementOrders(proc.items || []);
      setDemandForecast(dem.items || []);
      setLastUpdated(new Date());
      loadedDomainsRef.current = new Set([0, 1, 2, 3, 4, 5, 6, 7]);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      if (!silent) setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!loadedDomainsRef.current.has(domainTab)) {
      loadDomain(domainTab, domainTab > 0);
    }
  }, [domainTab, loadDomain]);

  // 自動シミュレーションモード: 一定間隔でデータを再取得（silent=trueでローディング非表示）
  useEffect(() => {
    if (simMode !== 'auto') return;
    const id = setInterval(() => {
      loadAll(true);
    }, autoIntervalSec * 1000);
    return () => clearInterval(id);
  }, [simMode, autoIntervalSec, loadAll]);

  // 順番ガイド: タブを順番に自動切り替え（カスタマイズ可能なドメイン順）
  useEffect(() => {
    if (!practiceMode || practiceDomainIndices.length === 0 || isDemoPlaying) return;
    const id = setInterval(() => {
      setDomainTab((prev) => {
        const idx = practiceDomainIndices.indexOf(prev);
        const nextIdx = idx < 0 ? 0 : (idx + 1) % practiceDomainIndices.length;
        return practiceDomainIndices[nextIdx];
      });
    }, practiceIntervalSec * 1000);
    return () => clearInterval(id);
  }, [practiceMode, practiceIntervalSec, practiceDomainIndices, isDemoPlaying]);

  // デモモード: ▶ボタンで8ドメインを自動切替＋ナレーション
  const handleDemoPlay = useCallback(() => {
    if (demoIntervalRef.current) {
      clearInterval(demoIntervalRef.current);
      demoIntervalRef.current = null;
    }
    setPracticeMode(false);
    setIsDemoPlaying(true);
    setDomainTab(0);
    const hasSpeech = typeof window !== 'undefined' && 'speechSynthesis' in window;
    const domainItems = DEMO_NARRATION.map((text, i) => ({
      text,
      onBefore: () => setDomainTab(i),
    }));
    const items = demoNarrationEnabled && hasSpeech
      ? [{ text: DEMO_NARRATION_INTRO, onBefore: () => setDomainTab(0) }, ...domainItems]
      : domainItems;
    if (demoNarrationEnabled && hasSpeech) {
      speakSequence(items, 'ja-JP', () => setIsDemoPlaying(false), demoNarrationRate);
    } else {
      let idx = 0;
      const ms = demoIntervalSec * 1000;
      demoIntervalRef.current = setInterval(() => {
        setDomainTab(idx);
        idx++;
        if (idx >= 8) {
          if (demoIntervalRef.current) {
            clearInterval(demoIntervalRef.current);
            demoIntervalRef.current = null;
          }
          setIsDemoPlaying(false);
        }
      }, ms);
    }
  }, [demoNarrationEnabled, demoNarrationRate, demoIntervalSec]);
  const handleDemoStop = useCallback(() => {
    cancelSpeech();
    if (demoIntervalRef.current) {
      clearInterval(demoIntervalRef.current);
      demoIntervalRef.current = null;
    }
    setIsDemoPlaying(false);
  }, []);

  useEffect(() => {
    return () => {
      if (isDemoPlaying) {
        cancelSpeech();
        if (demoIntervalRef.current) {
          clearInterval(demoIntervalRef.current);
          demoIntervalRef.current = null;
        }
      }
    };
  }, [isDemoPlaying]);

  const handleStressTest = async () => {
    try {
      setLoading(true);
      setError('');
      const result = await fintechApi.runStressTest(portfolioValue);
      setStressResult(result);
      setDomainTab(2);
      setFintechSubTab(3);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'ストレステストに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  // 要対応・要確認の集計（実用的なダッシュボード用）
  const manufacturingActionCount = predictive.filter((p) => p.status === '要メンテナンス').length + anomalies.filter((a) => a.severity === '高').length;
  const medicalActionCount = aiDiagnosis.filter((d) => d.status === '要確認').length + medicalAnomalies.filter((a) => a.severity === '高').length;
  const fintechActionCount = riskScores.filter((r) => r.level === '高').length + monitoring.filter((m) => m.status === '要確認').length;
  const securityActionCount = securityEvents.filter((e) => ['critical', 'high'].includes((e.threat_level || '').toLowerCase())).length;
  const infraOpsActionCount = monitoringAlerts.filter((a) => a.status !== '対応済').length + orchestrationDeployments.filter((d) => d.status === 'Pending').length;
  const dxDataActionCount = dataPipelines.filter((p) => p.status === '失敗' || p.status === '待機').length;
  const complianceActionCount = auditFindings.filter((f) => f.status !== '対応済').length + regulatoryItems.filter((r) => r.status === '要対応').length;
  const supplyChainActionCount = inventoryItems.filter((i) => i.status === '要発注').length;
  const totalActionCount = manufacturingActionCount + medicalActionCount + fintechActionCount + securityActionCount +
    infraOpsActionCount + dxDataActionCount + complianceActionCount + supplyChainActionCount;

  return (
    <Box sx={{ px: isMobile ? 0 : undefined }}>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 2, mb: 2 }}>
        <Typography variant={isMobile ? 'h6' : 'h5'} component="h1" gutterBottom sx={{ flex: 1, mb: 0 }}>
          産業統合プラットフォーム
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Tooltip title={isDemoPlaying ? '停止' : '8ドメインを自動切替・ナレーションでご覧ください'}>
            <IconButton
              onClick={isDemoPlaying ? handleDemoStop : handleDemoPlay}
              color={isDemoPlaying ? 'error' : 'primary'}
              aria-label={isDemoPlaying ? 'デモ停止' : 'デモ開始'}
            >
              {isDemoPlaying ? <Stop /> : <PlayArrow />}
            </IconButton>
          </Tooltip>
          <FormControlLabel
            control={
              <Checkbox
                checked={demoNarrationEnabled}
                onChange={(_, v) => setDemoNarrationEnabled(v)}
                disabled={isDemoPlaying}
                size="small"
              />
            }
            label={<Typography variant="caption">ナレーション</Typography>}
          />
          <Tooltip title="製造・IoTなどデータ量の多いタブで全体を確認しやすくします">
            <FormControlLabel
              control={
                <Checkbox
                  checked={demoScaleDown}
                  onChange={(_, v) => setDemoScaleDown(v)}
                  size="small"
                />
              }
              label={<Typography variant="caption">縮小表示</Typography>}
            />
          </Tooltip>
          {!isMobile && (
            <>
              <Tooltip title="ナレーションの読み上げ速度">
                <Box sx={{ width: 80, display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Typography variant="caption" color="text.secondary">速度</Typography>
                  <Slider
                    size="small"
                    value={demoNarrationRate}
                    min={0.7}
                    max={1.3}
                    step={0.1}
                    valueLabelDisplay="auto"
                    valueLabelFormat={(v) => `${v.toFixed(1)}x`}
                    onChange={(_, v) => {
                      const n = Array.isArray(v) ? v[0] : v;
                      setDemoNarrationRate(n);
                      localStorage.setItem('demo_narration_rate', String(n));
                    }}
                    disabled={isDemoPlaying}
                    sx={{ mt: 0.5 }}
                  />
                </Box>
              </Tooltip>
              <FormControl size="small" sx={{ minWidth: 90 }}>
                <InputLabel>タブ間隔</InputLabel>
                <Select
                  value={demoIntervalSec}
                  label="タブ間隔"
                  onChange={(e) => {
                    const v = Number(e.target.value);
                    setDemoIntervalSec(v);
                    localStorage.setItem('demo_interval_sec', String(v));
                  }}
                  disabled={isDemoPlaying || demoNarrationEnabled}
                >
                  <MenuItem value={10}>10秒</MenuItem>
                  <MenuItem value={15}>15秒</MenuItem>
                  <MenuItem value={20}>20秒</MenuItem>
                </Select>
              </FormControl>
            </>
          )}
        </Box>
      </Box>
      <Typography variant="body2" color="text.secondary" paragraph sx={{ fontSize: isMobile ? '0.8rem' : undefined, mt: -1 }}>
        製造・IoT / 医療・ヘルスケア / 金融・FinTech / 統合セキュリティ・防衛等 を1つの画面でシミュレーション。▶で8ドメインを自動切替・ナレーション付きでご覧いただけます。
      </Typography>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 2, mb: 2 }}>
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>業種</InputLabel>
          <Select
            value={industryType}
            label="業種"
            onChange={(e) => {
              const v = e.target.value as IndustryType;
              setIndustryType(v);
              localStorage.setItem('industry_type', v);
              setDomainTab(INDUSTRY_DEFAULT_TAB[v]);
            }}
          >
            <MenuItem value="general">汎用</MenuItem>
            <MenuItem value="manufacturing">製造業</MenuItem>
            <MenuItem value="medical">医療</MenuItem>
            <MenuItem value="financial">金融</MenuItem>
            <MenuItem value="sier">SIer</MenuItem>
            <MenuItem value="dx">DX</MenuItem>
          </Select>
        </FormControl>
        <Paper variant="outlined" sx={{ px: 2, py: 1, display: 'flex', alignItems: 'center', gap: 1, bgcolor: 'primary.main', color: 'primary.contrastText' }}>
          <UploadFile />
          <Typography variant="body2">実データ連携:</Typography>
          <Button
            size="small"
            variant="contained"
            color="inherit"
            startIcon={<UploadFile />}
            onClick={() => { setCsvImportOpen(true); setCsvData([]); setCsvError(''); }}
            sx={{ color: 'primary.main', bgcolor: 'white', '&:hover': { bgcolor: 'grey.100' } }}
          >
            CSV取り込み
          </Button>
        </Paper>
      </Box>

      {/* 要対応サマリ（実用的なダッシュボード） */}
      <Paper variant="outlined" sx={{ p: isMobile ? 1.5 : 2, mb: 2, bgcolor: 'action.hover' }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Typography variant="subtitle2" color="text.secondary">要対応・要確認</Typography>
            <Typography variant="h4" color={totalActionCount > 0 ? 'error.main' : 'text.primary'}>
              {totalActionCount} 件
            </Typography>
          </Grid>
          <Grid item xs>
            <Stack direction="row" spacing={1} flexWrap="wrap">
              <Chip 
                label={`製造 ${manufacturingActionCount}`} 
                size="small" 
                color={manufacturingActionCount > 0 ? 'warning' : 'default'}
                onClick={() => setDomainTab(0)}
              />
              <Chip 
                label={`医療 ${medicalActionCount}`} 
                size="small" 
                color={medicalActionCount > 0 ? 'warning' : 'default'}
                onClick={() => setDomainTab(1)}
              />
              <Chip 
                label={`金融 ${fintechActionCount}`} 
                size="small" 
                color={fintechActionCount > 0 ? 'warning' : 'default'}
                onClick={() => setDomainTab(2)}
              />
              <Chip 
                label={`セキュリティ ${securityActionCount}`} 
                size="small" 
                color={securityActionCount > 0 ? 'error' : 'default'}
                onClick={() => setDomainTab(3)}
              />
              <Chip 
                label={`インフラ ${infraOpsActionCount}`} 
                size="small" 
                color={infraOpsActionCount > 0 ? 'warning' : 'default'}
                onClick={() => setDomainTab(4)}
              />
              <Chip 
                label={`DX ${dxDataActionCount}`} 
                size="small" 
                color={dxDataActionCount > 0 ? 'warning' : 'default'}
                onClick={() => setDomainTab(5)}
              />
              <Chip 
                label={`コンプライアンス ${complianceActionCount}`} 
                size="small" 
                color={complianceActionCount > 0 ? 'warning' : 'default'}
                onClick={() => setDomainTab(6)}
              />
              <Chip 
                label={`サプライチェーン ${supplyChainActionCount}`} 
                size="small" 
                color={supplyChainActionCount > 0 ? 'warning' : 'default'}
                onClick={() => setDomainTab(7)}
              />
            </Stack>
          </Grid>
          <Grid item>
            <Tooltip title="要対応サマリをCSVでエクスポート">
              <Button
                size="small"
                variant="outlined"
                onClick={() => {
                  const rows = [
                    ['ドメイン', '要対応件数', '最終更新'],
                    ['製造・IoT', String(manufacturingActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                    ['医療・ヘルスケア', String(medicalActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                    ['金融・FinTech', String(fintechActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                    ['統合セキュリティ・防衛', String(securityActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                    ['インフラ・運用系', String(infraOpsActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                    ['DX・データ系', String(dxDataActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                    ['コンプライアンス・ガバナンス', String(complianceActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                    ['サプライチェーン', String(supplyChainActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                    ['合計', String(totalActionCount), lastUpdated?.toLocaleString('ja-JP') || '-'],
                  ];
                  const csv = rows.map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n');
                  const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8' });
                  const a = document.createElement('a');
                  a.href = URL.createObjectURL(blob);
                  a.download = `要対応サマリ_${new Date().toISOString().slice(0, 10)}.csv`;
                  a.click();
                  URL.revokeObjectURL(a.href);
                }}
              >
                エクスポート
              </Button>
            </Tooltip>
          </Grid>
          <Grid item>
            <Typography variant="caption" color="text.secondary">
              最終更新: {lastUpdated ? lastUpdated.toLocaleTimeString('ja-JP') : '-'}
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      <Box
        sx={{
          transform: demoScaleDown ? 'scale(0.75)' : 'none',
          transformOrigin: 'top center',
        }}
      >
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }} role="region" aria-label="業種ドメイン選択">
        <Tabs
          value={domainTab}
          onChange={(_, v) => setDomainTab(v)}
          variant="scrollable"
          scrollButtons="auto"
          aria-label="8業種ドメインのタブ（矢印キーで切り替え）"
        >
          <Tab icon={<PrecisionManufacturing />} iconPosition="start" label="製造・IoT" id="domain-tab-0" aria-controls="domain-panel-0" />
          <Tab icon={<LocalHospital />} iconPosition="start" label="医療・ヘルスケア" id="domain-tab-1" aria-controls="domain-panel-1" />
          <Tab icon={<AccountBalance />} iconPosition="start" label="金融・FinTech" id="domain-tab-2" aria-controls="domain-panel-2" />
          <Tab icon={<Shield />} iconPosition="start" label="統合セキュリティ・防衛" id="domain-tab-3" aria-controls="domain-panel-3" />
          <Tab icon={<Cloud />} iconPosition="start" label="インフラ・運用系" id="domain-tab-4" aria-controls="domain-panel-4" />
          <Tab icon={<Storage />} iconPosition="start" label="DX・データ系" id="domain-tab-5" aria-controls="domain-panel-5" />
          <Tab icon={<Gavel />} iconPosition="start" label="コンプライアンス・ガバナンス" id="domain-tab-6" aria-controls="domain-panel-6" />
          <Tab icon={<LocalShipping />} iconPosition="start" label="サプライチェーン" id="domain-tab-7" aria-controls="domain-panel-7" />
        </Tabs>
      </Box>

      <Stack direction="row" spacing={1} sx={{ mb: 2 }} alignItems="center" flexWrap="wrap">
        <Typography variant="body2" color="text.secondary" sx={{ mr: 1, fontSize: isMobile ? '0.8rem' : undefined }}>シミュレーションモード:</Typography>
        <Tooltip title="一定間隔で自動的にデータを再取得">
          <Chip
            size={isMobile ? 'small' : 'medium'}
            icon={<PlayArrow />}
            label="自動"
            onClick={() => setSimMode('auto')}
            color={simMode === 'auto' ? 'primary' : 'default'}
            variant={simMode === 'auto' ? 'filled' : 'outlined'}
          />
        </Tooltip>
        {simMode === 'auto' && (
          <FormControl size="small" sx={{ minWidth: 100 }}>
            <InputLabel>間隔</InputLabel>
            <Select
              value={autoIntervalSec}
              label="間隔"
              onChange={(e) => setAutoIntervalSec(Number(e.target.value))}
            >
              {AUTO_INTERVAL_OPTIONS.map((n) => (
                <MenuItem key={n} value={n}>{n}秒</MenuItem>
              ))}
            </Select>
          </FormControl>
        )}
        <Tooltip title="手動で更新ボタンをクリックしたときのみ更新">
          <Chip
            size={isMobile ? 'small' : 'medium'}
            icon={<TouchApp />}
            label="手動"
            onClick={() => setSimMode('manual')}
            color={simMode === 'manual' ? 'primary' : 'default'}
            variant={simMode === 'manual' ? 'filled' : 'outlined'}
          />
        </Tooltip>
        <Tooltip title="全ドメインのデータを即時再取得">
          <Chip size={isMobile ? 'small' : 'medium'} icon={<Refresh />} label="全データ更新" onClick={() => loadAll()} variant="outlined" color="primary" />
        </Tooltip>
        <Tooltip title="APIベースURLを設定（既存システム連携用）">
          <Chip icon={<Settings />} label="API連携設定" onClick={() => { setApiConfigOpen(true); setApiBaseUrlInput(getApiBaseUrl()); }} variant="outlined" />
        </Tooltip>
        <Tooltip title="CSVファイルをアップロードして実データを取り込み（実データ連携の入口）">
          <Chip icon={<UploadFile />} label="CSV取り込み" onClick={() => { setCsvImportOpen(true); setCsvData([]); setCsvError(''); }} variant="outlined" color="primary" />
        </Tooltip>
        <Tooltip title="タブを順番に自動切り替え。製造→医療→金融→…の順で、確認すべきドメインの目印になります">
          <Chip
            icon={<FormatListNumbered />}
            label="順番ガイド"
            onClick={() => setPracticeMode((p) => !p)}
            color={practiceMode ? 'secondary' : 'default'}
            variant={practiceMode ? 'filled' : 'outlined'}
          />
        </Tooltip>
        {practiceMode && (
          <>
            <FormControl size="small" sx={{ minWidth: 100 }}>
              <InputLabel>切り替え間隔</InputLabel>
              <Select
                value={practiceIntervalSec}
              label="切り替え間隔"
              onChange={(e) => setPracticeIntervalSec(Number(e.target.value))}
            >
              {PRACTICE_INTERVAL_OPTIONS.map((n) => (
                <MenuItem key={n} value={n}>{n}秒</MenuItem>
              ))}
            </Select>
          </FormControl>
            <Tooltip title="巡回するドメインを選択">
              <Chip
                icon={<Settings />}
                label="ドメイン選択"
                onClick={() => setPracticeConfigOpen(true)}
                variant="outlined"
                size="small"
              />
            </Tooltip>
          </>
        )}
        {simMode === 'auto' && (
          <Typography variant="caption" color="primary" sx={{ ml: 1 }}>
            自動更新中（{autoIntervalSec}秒ごと）
          </Typography>
        )}
        {practiceMode && (
          <Typography variant="caption" color="secondary" sx={{ ml: 1 }}>
            順番ガイド中（{practiceIntervalSec}秒ごとに次のドメインへ）
          </Typography>
        )}
      </Stack>

      <Dialog open={csvImportOpen} onClose={() => setCsvImportOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>CSVデータ取り込み（実データ連携の基盤）</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            CSVファイルをアップロードすると、プレビュー表示されます。将来的にAPI連携で実データを取り込む基盤として利用できます。
          </Typography>
          <Button variant="outlined" component="label" startIcon={<UploadFile />} sx={{ mb: 2 }}>
            ファイルを選択
            <input
              type="file"
              hidden
              accept=".csv"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (!file) return;
                setCsvError('');
                const reader = new FileReader();
                reader.onload = () => {
                  try {
                    const text = String(reader.result);
                    const rows = text.split(/\r?\n/).filter(Boolean).map((row) => row.split(',').map((c) => c.trim()));
                    setCsvData(rows);
                  } catch (err: any) {
                    setCsvError(err.message || 'パースに失敗しました');
                  }
                };
                reader.readAsText(file, 'UTF-8');
              }}
            />
          </Button>
          {csvError && <Alert severity="error" sx={{ mb: 2 }}>{csvError}</Alert>}
          {csvSaved && <Alert severity="success" sx={{ mb: 2 }}>DBに保存しました</Alert>}
          {csvData.length > 0 && (
            <TableContainer component={Paper} variant="outlined" sx={{ maxHeight: 300 }}>
              <Table size="small" stickyHeader>
                <TableHead>
                  <TableRow>
                    {csvData[0]?.map((h, i) => (
                      <TableCell key={i}>{h}</TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {csvData.slice(1, 21).map((row, ri) => (
                    <TableRow key={ri}>
                      {row.map((cell, ci) => (
                        <TableCell key={ci}>{cell}</TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              {csvData.length > 21 && (
                <Typography variant="caption" color="text.secondary" sx={{ p: 1, display: 'block' }}>
                  他 {csvData.length - 21} 行（先頭20行のみ表示）
                </Typography>
              )}
            </TableContainer>
          )}
        </DialogContent>
        <DialogActions>
          {csvData.length > 0 && (
            <Button
              variant="contained"
              disabled={csvSaving}
              onClick={async () => {
                setCsvSaving(true);
                setCsvSaved(false);
                try {
                  const domain = DOMAIN_LABELS[domainTab] || 'general';
                  await dataIntegrationApi.importCsv(csvData, domain);
                  setCsvSaved(true);
                  setCsvError('');
                } catch (e: any) {
                  setCsvError(e?.response?.data?.detail || e?.message || '保存に失敗しました');
                } finally {
                  setCsvSaving(false);
                }
              }}
            >
              {csvSaving ? '保存中...' : 'DBに保存'}
            </Button>
          )}
          <Button onClick={() => { setCsvImportOpen(false); setCsvSaved(false); }}>閉じる</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={apiConfigOpen} onClose={() => setApiConfigOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>API連携設定</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            既存システムのAPIベースURLを設定します。空の場合は環境変数のデフォルトを使用します。
          </Typography>
          <TextField
            fullWidth
            label="API ベース URL"
            placeholder="http://localhost:9010"
            value={apiBaseUrlInput}
            onChange={(e) => setApiBaseUrlInput(e.target.value)}
            helperText="例: http://localhost:9010 または https://api.example.com"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setApiConfigOpen(false)}>閉じる</Button>
          <Button
            variant="contained"
            onClick={() => {
              const v = apiBaseUrlInput?.trim();
              if (v) localStorage.setItem('industry_api_base_url', v);
              else localStorage.removeItem('industry_api_base_url');
              setApiConfigOpen(false);
              loadAll();
            }}
          >
            保存して再取得
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={practiceConfigOpen} onClose={() => setPracticeConfigOpen(false)} maxWidth="xs" fullWidth>
        <DialogTitle>順番ガイド - ドメイン選択</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            巡回するドメインを選択してください。選択した順番でタブが切り替わります。
          </Typography>
          <FormGroup>
            {[
              { i: 0, label: '製造・IoT' },
              { i: 1, label: '医療・ヘルスケア' },
              { i: 2, label: '金融・FinTech' },
              { i: 3, label: '統合セキュリティ・防衛' },
              { i: 4, label: 'インフラ・運用系' },
              { i: 5, label: 'DX・データ系' },
              { i: 6, label: 'コンプライアンス・ガバナンス' },
              { i: 7, label: 'サプライチェーン' },
            ].map(({ i, label }) => (
              <FormControlLabel
                key={i}
                control={
                  <Checkbox
                    checked={practiceDomainIndices.includes(i)}
                    onChange={(_, checked) => {
                      const next = checked
                        ? [...practiceDomainIndices, i].sort((a, b) => a - b)
                        : practiceDomainIndices.filter((x) => x !== i);
                      setPracticeDomainIndices(next);
                      localStorage.setItem('industry_unified_practice_domains', JSON.stringify(next));
                    }}
                  />
                }
                label={label}
              />
            ))}
          </FormGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPracticeConfigOpen(false)}>閉じる</Button>
          <Button onClick={() => { setPracticeDomainIndices([0, 1, 2, 3, 4, 5, 6, 7]); localStorage.setItem('industry_unified_practice_domains', JSON.stringify([0, 1, 2, 3, 4, 5, 6, 7])); }}>全て選択</Button>
        </DialogActions>
      </Dialog>

      {error && (
        <Alert
          severity="error"
          sx={{ mb: 2 }}
          onClose={() => setError('')}
          action={
            <Button color="inherit" size="small" onClick={() => loadAll(false)}>
              再試行
            </Button>
          }
        >
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ p: 4, textAlign: 'center' }}>
          <CircularProgress />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>読み込み中...</Typography>
        </Box>
      ) : (
        <>
          <TabPanel value={domainTab} index={0}>
            <ManufacturingTab
              predictive={predictive}
              sensors={sensors}
              anomalies={anomalies}
              subTab={manufacturingSubTab}
              setSubTab={setManufacturingSubTab}
              learnType={manufacturingLearnType}
              setLearnType={setManufacturingLearnType}
              learnStep={manufacturingLearnStep}
              setLearnStep={setManufacturingLearnStep}
              learnSelected={manufacturingLearnSelected}
              setLearnSelected={setManufacturingLearnSelected}
              learnFeedback={manufacturingLearnFeedback}
              setLearnFeedback={setManufacturingLearnFeedback}
            />
          </TabPanel>

          <TabPanel value={domainTab} index={1}>
            <MedicalTab
              aiDiagnosis={aiDiagnosis}
              voiceResponse={voiceResponse}
              medicalAnomalies={medicalAnomalies}
              stats={stats}
              subTab={medicalSubTab}
              setSubTab={setMedicalSubTab}
              learnType={medicalLearnType}
              setLearnType={setMedicalLearnType}
              learnStep={medicalLearnStep}
              setLearnStep={setMedicalLearnStep}
              learnSelected={medicalLearnSelected}
              setLearnSelected={setMedicalLearnSelected}
              learnFeedback={medicalLearnFeedback}
              setLearnFeedback={setMedicalLearnFeedback}
            />
          </TabPanel>

          <TabPanel value={domainTab} index={2}>
            <FintechTab
              payments={payments}
              riskScores={riskScores}
              monitoring={monitoring}
              stressResult={stressResult}
              portfolioValue={portfolioValue}
              setPortfolioValue={setPortfolioValue}
              loading={loading}
              onStressTest={handleStressTest}
              subTab={fintechSubTab}
              setSubTab={setFintechSubTab}
              learnType={fintechLearnType}
              setLearnType={setFintechLearnType}
              learnStep={fintechLearnStep}
              setLearnStep={setFintechLearnStep}
              learnSelected={fintechLearnSelected}
              setLearnSelected={setFintechLearnSelected}
              learnFeedback={fintechLearnFeedback}
              setLearnFeedback={setFintechLearnFeedback}
            />
          </TabPanel>

          <TabPanel value={domainTab} index={3}>
            <SecurityTab
              securityEvents={securityEvents}
              securityIncidents={securityIncidents}
              securityRisks={securityRisks}
              subTab={securitySubTab}
              setSubTab={setSecuritySubTab}
              learnType={securityLearnType}
              setLearnType={setSecurityLearnType}
              learnStep={securityLearnStep}
              setLearnStep={setSecurityLearnStep}
              learnSelected={securityLearnSelected}
              setLearnSelected={setSecurityLearnSelected}
              learnFeedback={securityLearnFeedback}
              setLearnFeedback={setSecurityLearnFeedback}
            />
          </TabPanel>

          <TabPanel value={domainTab} index={4}>
            <InfraOpsTab
              iacProjects={iacProjects}
              monitoringAlerts={monitoringAlerts}
              orchestrationDeployments={orchestrationDeployments}
              optimizationRecs={optimizationRecs}
              subTab={infraOpsSubTab}
              setSubTab={setInfraOpsSubTab}
              learnType={infraOpsLearnType}
              setLearnType={setInfraOpsLearnType}
              learnStep={infraOpsLearnStep}
              setLearnStep={setInfraOpsLearnStep}
              learnSelected={infraOpsLearnSelected}
              setLearnSelected={setInfraOpsLearnSelected}
              learnFeedback={infraOpsLearnFeedback}
              setLearnFeedback={setInfraOpsLearnFeedback}
            />
          </TabPanel>

          <TabPanel value={domainTab} index={5}>
            <DxDataTab
              dataLakeCatalogs={dataLakeCatalogs}
              mlModels={mlModels}
              genaiUsage={genaiUsage}
              dataPipelines={dataPipelines}
              subTab={dxDataSubTab}
              setSubTab={setDxDataSubTab}
              learnType={dxDataLearnType}
              setLearnType={setDxDataLearnType}
              learnStep={dxDataLearnStep}
              setLearnStep={setDxDataLearnStep}
              learnSelected={dxDataLearnSelected}
              setLearnSelected={setDxDataLearnSelected}
              learnFeedback={dxDataLearnFeedback}
              setLearnFeedback={setDxDataLearnFeedback}
            />
          </TabPanel>

          <TabPanel value={domainTab} index={6}>
            <ComplianceTab
              regulatoryItems={regulatoryItems}
              auditLogs={auditLogs}
              governancePolicies={governancePolicies}
              auditFindings={auditFindings}
              subTab={complianceSubTab}
              setSubTab={setComplianceSubTab}
              learnType={complianceLearnType}
              setLearnType={setComplianceLearnType}
              learnStep={complianceLearnStep}
              setLearnStep={setComplianceLearnStep}
              learnSelected={complianceLearnSelected}
              setLearnSelected={setComplianceLearnSelected}
              learnFeedback={complianceLearnFeedback}
              setLearnFeedback={setComplianceLearnFeedback}
            />
          </TabPanel>

          <TabPanel value={domainTab} index={7}>
            <SupplyChainTab
              logisticsShipments={logisticsShipments}
              inventoryItems={inventoryItems}
              procurementOrders={procurementOrders}
              demandForecast={demandForecast}
              subTab={supplyChainSubTab}
              setSubTab={setSupplyChainSubTab}
              learnType={supplyChainLearnType}
              setLearnType={setSupplyChainLearnType}
              learnStep={supplyChainLearnStep}
              setLearnStep={setSupplyChainLearnStep}
              learnSelected={supplyChainLearnSelected}
              setLearnSelected={setSupplyChainLearnSelected}
              learnFeedback={supplyChainLearnFeedback}
              setLearnFeedback={setSupplyChainLearnFeedback}
            />
          </TabPanel>
        </>
      )}
      </Box>
    </Box>
  );
};
