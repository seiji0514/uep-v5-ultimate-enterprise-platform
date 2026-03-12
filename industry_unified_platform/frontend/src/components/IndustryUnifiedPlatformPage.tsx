/**
 * 産業統合プラットフォーム
 * 製造・IoT + 医療・ヘルスケア + 金融・FinTech + 統合セキュリティ・防衛 を1つに統合
 */
import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
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
} from '@mui/material';
import {
  PrecisionManufacturing,
  LocalHospital,
  AccountBalance,
  Shield,
  Sensors,
  Warning,
  Psychology,
  RecordVoiceOver,
  Payment,
  Security,
  Visibility,
  Science,
  Refresh,
  PlayArrow,
  TouchApp,
  FormatListNumbered,
  Cloud,
  Storage,
  Gavel,
  LocalShipping,
  Build,
  Timeline,
  Policy,
  Inventory,
  School,
  CheckCircle,
  ArrowForward,
  Settings,
  UploadFile,
} from '@mui/icons-material';
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

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}
function TabPanel({ children, value, index }: TabPanelProps) {
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  );
}

// 実務学習パネル（共通コンポーネント）
function LearnPanel({
  steps,
  stepIndex,
  setStepIndex,
  selected,
  setSelected,
  feedback,
  setFeedback,
  onReset,
}: {
  steps: LearnStep[];
  stepIndex: number;
  setStepIndex: (v: number | ((s: number) => number)) => void;
  selected: number | null;
  setSelected: (v: number | null) => void;
  feedback: 'correct' | 'wrong' | null;
  setFeedback: (v: 'correct' | 'wrong' | null) => void;
  onReset: () => void;
}) {
  const step = steps[stepIndex];
  const isComplete = stepIndex >= steps.length;
  return (
    <Paper variant="outlined" sx={{ p: 2, bgcolor: 'action.hover' }}>
      <Typography variant="subtitle2" color="primary" gutterBottom>
        順番通りに進めれば実務が学べます（ステップ {Math.min(stepIndex + 1, steps.length)} / {steps.length}）
      </Typography>
      {!isComplete && step ? (
        <>
          <Typography variant="body1" sx={{ mb: 2 }}>{step.q}</Typography>
          <Stack spacing={1}>
            {step.opts.map((opt, i) => (
              <Button
                key={i}
                variant={selected === i ? 'contained' : 'outlined'}
                onClick={() => {
                  if (feedback === 'correct') return;
                  setSelected(i);
                  setFeedback(i === step.correct ? 'correct' : 'wrong');
                }}
                color={feedback === 'correct' && selected === i ? 'success' : feedback === 'wrong' && selected === i ? 'error' : 'primary'}
                startIcon={feedback && selected === i && i === step.correct ? <CheckCircle /> : undefined}
              >
                {i + 1}. {opt}
              </Button>
            ))}
          </Stack>
          {feedback === 'correct' && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="success.main" fontWeight={600}>正解です。</Typography>
              {step.correctReason && <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>【なぜ正解か】{step.correctReason}</Typography>}
              <Button size="small" variant="contained" endIcon={<ArrowForward />} sx={{ mt: 2 }} onClick={() => { setStepIndex((s) => s + 1); setSelected(null); setFeedback(null); }}>
                次へ
              </Button>
            </Box>
          )}
          {feedback === 'wrong' && selected !== null && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="error" fontWeight={600}>不正解です。</Typography>
              {step.wrongReasons && step.wrongReasons[selected] && <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>【なぜ間違いか】{step.wrongReasons[selected]}</Typography>}
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>もう一度選んでください。</Typography>
            </Box>
          )}
        </>
      ) : (
        <Box>
          <Typography variant="h6" color="success.main" gutterBottom><CheckCircle /> 完了</Typography>
          <Typography variant="body2">順番通りに進めることで実務が身につきます。</Typography>
          <Button sx={{ mt: 2 }} variant="outlined" onClick={onReset}>最初からやり直す</Button>
        </Box>
      )}
    </Paper>
  );
}

type SimMode = 'auto' | 'manual';
const AUTO_INTERVAL_OPTIONS = [5, 10, 30] as const;
const PRACTICE_INTERVAL_OPTIONS = [5, 10, 15, 30] as const;
const LEARN_PROGRESS_KEY = 'industry_unified_learn_progress';

function loadLearnProgress(): Record<string, number> {
  try {
    const raw = localStorage.getItem(LEARN_PROGRESS_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveLearnProgress(progress: Record<string, number>) {
  try {
    localStorage.setItem(LEARN_PROGRESS_KEY, JSON.stringify(progress));
  } catch {
    /* ignore */
  }
}

// 実務学習シナリオ型（正解・不正解の説明付き）
type LearnStep = {
  q: string;
  opts: string[];
  correct: number;
  correctReason?: string;
  wrongReasons?: string[]; // opts[i]が不正解のときの説明（i !== correct）
};

// 製造・IoT 実務学習（予知保全・センサーデータ・異常検知を分離）
const MANUFACTURING_LEARN_PREDICTIVE: LearnStep[] = [
  { q: 'CNC旋盤Aが「要メンテナンス」と表示されています。最初に確認すべきは？', opts: ['予測故障日と信頼度', 'センサーデータ', '即時停止'], correct: 0, correctReason: '予測故障日と信頼度を確認することで、いつまで稼働可能か・どの程度の確度かが分かり、対応の優先度やスケジュールを決められます。', wrongReasons: ['', 'センサーデータは次の確認ステップ。まず予測の根拠を把握するのが先です。', '即時停止は、緊急時以外は過剰対応。まず状況把握が優先です。'] },
  { q: '点検予約を登録しました。次に記録すべきは？', opts: ['点検日時・担当者', '部品発注', '運転再開'], correct: 0, correctReason: '点検日時・担当者を記録することで、実施状況の追跡と再発防止の分析が可能になります。', wrongReasons: ['', '部品発注は点検結果を確認してから判断します。', '運転再開は点検完了後の判断です。'] },
  { q: '予知保全モデルの精度が低下しています。最初に確認すべきは？', opts: ['学習データの鮮度・ドリフト', 'モデル削除', '閾値の引き上げ'], correct: 0, correctReason: 'データドリフトや学習データの古さが精度低下の主因であることが多いため、まず確認します。', wrongReasons: ['', 'モデル削除は過剰対応。原因特定が先です。', '閾値変更は根本対応にならず、見逃しリスクを高めます。'] },
];
const MANUFACTURING_LEARN_SENSOR: LearnStep[] = [
  { q: 'OPC-UAセンサーの温度値が急上昇しています。まず確認すべきは？', opts: ['同一設備の他センサー（振動・圧力）', '他設備の温度', 'ログのみ'], correct: 0, correctReason: '同一設備の他センサーを確認することで、温度上昇が局所的か・振動異常を伴うかなど、故障原因の切り分けができます。', wrongReasons: ['', '他設備は別要因。まず同一設備内で関連データを確認します。', 'ログのみではリアルタイムの状況把握が不十分です。'] },
  { q: 'センサーデータで振動値が閾値を超えています。適切な対応は？', opts: ['点検予約を入れる', '即時停止', '放置して様子見'], correct: 0, correctReason: '閾値超過は故障の前兆の可能性が高いため、点検予約で計画的に対応するのが適切です。', wrongReasons: ['', '即時停止は重大度が高い場合のみ。まず点検で状況確認が先です。', '放置は故障リスクを高めます。必ず点検・対応が必要です。'] },
  { q: '複数センサー（温度・振動・圧力）の値を比較する目的は？', opts: ['故障原因の切り分け・傾向把握', '見た目だけ確認', '記録のみ'], correct: 0, correctReason: '複数センサーの相関を分析することで、故障モードの特定や予知保全の精度向上につながります。', wrongReasons: ['', '見た目だけでは傾向や相関は分かりません。', '記録は手段であり、目的は分析・活用です。'] },
];
const MANUFACTURING_LEARN_ANOMALY: LearnStep[] = [
  { q: '異常検知で「振動異常」と「温度上昇」が同時に出ました。優先すべきは？', opts: ['振動異常（機械的故障の可能性）', '温度上昇', '両方同時対応'], correct: 0, correctReason: '振動異常は軸受け・ベアリングなど機械的故障の前兆であることが多く、放置すると重大事故につながりやすいため優先します。', wrongReasons: ['', '温度上昇は振動異常の結果である場合が多いです。原因である振動を先に確認します。', '同時対応は効率が悪く、優先度の高い方から順に対応します。'] },
  { q: '異常検知で「高」重大度のアラートが出ました。優先すべきは？', opts: ['該当設備の稼働停止確認', 'ログのみ確認', '後日対応'], correct: 0, correctReason: '高重大度は即時対応が必要です。まず稼働状況を確認し、必要なら停止判断をします。', wrongReasons: ['', 'ログのみでは現状の安全確認ができません。', '後日対応では事故リスクが高まります。'] },
  { q: '異常検知のアラートを対応済みにした後、記録すべきは？', opts: ['対応内容・時刻・担当者', 'アラート削除のみ', '記録不要'], correct: 0, correctReason: '対応内容・時刻・担当者を記録することで、監査対応や再発防止の分析に活用できます。', wrongReasons: ['', '削除のみでは履歴が残らず、分析・監査に使えません。', '記録は再発防止と監査のため必須です。'] },
];

// 医療・ヘルスケア 実務学習（AI診断・音声応答・異常検知を分離）
const MEDICAL_LEARN_AI: LearnStep[] = [
  { q: 'AI診断で「要確認」の所見が出ました。最初にすべきは？', opts: ['所見内容と信頼度の確認', '即時再検査', '放置'], correct: 0, correctReason: '所見内容と信頼度を確認することで、医師の判断材料となり、適切な次のアクション（再検査・経過観察など）を決められます。', wrongReasons: ['', '再検査は所見確認後の判断です。まず内容を把握します。', '放置は患者リスクを高めます。必ず確認が必要です。'] },
  { q: 'AI診断の信頼度が70%の場合、適切な対応は？', opts: ['医師による所見の確認・補足判断', '自動で診断確定', '無視'], correct: 0, correctReason: '中程度の信頼度では医師の確認が必須です。AIは補助であり、最終判断は医師が行います。', wrongReasons: ['', '自動確定は医療過誤のリスクがあります。', '無視は患者安全を損ないます。'] },
  { q: 'AI診断の複数所見が矛盾しています。適切な対応は？', opts: ['医師による統合判断・追加検査の検討', '最初の所見のみ採用', 'AIを無効化'], correct: 0, correctReason: '矛盾する所見は医師が統合し、追加検査で確定診断を補完するのが適切です。', wrongReasons: ['', '最初の所見のみでは誤診のリスクがあります。', 'AI無効化は過剰対応。医師の判断補助として活用します。'] },
];
const MEDICAL_LEARN_VOICE: LearnStep[] = [
  { q: '音声応答の文字起こしで誤認識がありました。適切な対応は？', opts: ['手動で修正しログに記録', '無視', 'システム停止'], correct: 0, correctReason: '修正とログ記録により、診療の正確性を保ちつつ、音声認識の改善フィードバックにもなります。', wrongReasons: ['', '無視すると診療記録の誤りにつながります。', 'システム停止は過剰対応。修正と記録で対応します。'] },
  { q: 'ナースコールの音声が雑音で聞き取りにくい場合、優先すべきは？', opts: ['聞き取れた部分を記録し、必要なら再収録', '推測で記録', '記録しない'], correct: 0, correctReason: '聞き取れた部分を確実に記録し、不明部分は再収録で補完することで、正確性を保てます。', wrongReasons: ['', '推測記録は誤りの原因になります。', '記録しないと診療に支障が出ます。'] },
];
const MEDICAL_LEARN_ANOMALY: LearnStep[] = [
  { q: 'バイタル異常検知で「高」重大度です。優先すべきは？', opts: ['担当者への即時通知・確認', '後日確認', 'ログのみ記録'], correct: 0, correctReason: '高重大度は患者の安全に直結するため、担当者への即時通知で迅速な対応を促します。', wrongReasons: ['', '後日では手遅れになる可能性があります。', 'ログのみでは患者への対応が遅れます。'] },
  { q: '複数のバイタル異常が同時検出されました。最初にすべきは？', opts: ['生命に直結する指標（SpO2、心拍など）を優先確認', 'すべて同時対応', '軽い方から対応'], correct: 0, correctReason: '生命に直結する指標を優先することで、重篤化を防ぎます。', wrongReasons: ['', '同時対応は非効率で、重要な見逃しのリスクがあります。', '軽い方からでは重篤化のリスクがあります。'] },
];
// 金融・FinTech 実務学習（決済・リスクスコア・取引監視・ストレステストを分離）
const FINTECH_LEARN_PAYMENT: LearnStep[] = [
  { q: '決済が「処理中」で長時間滞留しています。最初にすべきは？', opts: ['トランザクション状態・エラーログの確認', '即時キャンセル', '放置'], correct: 0, correctReason: '状態とログを確認することで、再試行・手動決済・キャンセルなど適切な対応を決められます。', wrongReasons: ['', '即時キャンセルは二重決済のリスクがあります。まず状態確認が先です。', '放置は顧客クレームや資金決済法違反のリスクがあります。'] },
  { q: '決済の失敗が多発しています。最初に確認すべきは？', opts: ['失敗パターン・エラー種別の分析', '再実行のみ', '無視'], correct: 0, correctReason: 'パターン分析により、システム障害・カード不正・ネットワーク問題などを切り分けできます。', wrongReasons: ['', '再実行のみでは同じ失敗を繰り返す可能性があります。', '無視は顧客離脱と収益損失につながります。'] },
  { q: '決済のリトライ上限に達しました。適切な対応は？', opts: ['手動確認・例外処理フローの起動', '自動再試行継続', '顧客に連絡のみ'], correct: 0, correctReason: '手動確認で二重決済を防ぎつつ、例外フローで適切に処理します。', wrongReasons: ['', '再試行継続は二重決済のリスクがあります。', '連絡のみでは決済完了の保証ができません。'] },
];
const FINTECH_LEARN_RISK: LearnStep[] = [
  { q: 'リスクスコアが「高」の取引があります。最初にすべきは？', opts: ['取引詳細と要因の確認', '即時ブロック', '放置'], correct: 0, correctReason: '詳細と要因を確認することで、不正か正常かを判断し、適切な対応（ブロック・許可）を決められます。', wrongReasons: ['', '即時ブロックは誤検知の場合に顧客に影響します。まず確認が先です。', '放置は不正取引のリスクを高めます。'] },
  { q: 'リスクスコアの要因に「新規宛先・高額」が含まれています。適切な対応は？', opts: ['本人確認・二重チェック', '自動ブロック', '自動承認'], correct: 0, correctReason: '本人確認により、なりすましを防ぎつつ、正当な取引はスムーズに進められます。', wrongReasons: ['', '自動ブロックは正当な取引を阻害する可能性があります。', '自動承認は不正リスクが高い取引には不適切です。'] },
];
const FINTECH_LEARN_MONITOR: LearnStep[] = [
  { q: '取引監視で「高額送金・新規宛先」のアラートが出ました。適切な対応は？', opts: ['本人確認・二重チェック', '自動承認', '無視'], correct: 0, correctReason: '本人確認により、なりすましや不正送金を防ぎつつ、正当な取引はスムーズに進められます。', wrongReasons: ['', '自動承認は不正リスクが高い取引には不適切です。', '無視は不正送金のリスクを高めます。'] },
  { q: '海外送金のアラートが複数出ています。優先すべきは？', opts: ['制裁リスト・送金先の確認', 'すべて同時対応', '後回し'], correct: 0, correctReason: '制裁リスト・送金先の確認により、規制違反を防ぎます。', wrongReasons: ['', '同時対応は非効率で、重要な見逃しのリスクがあります。', '後回しは規制違反のリスクを高めます。'] },
];
const FINTECH_LEARN_STRESS: LearnStep[] = [
  { q: 'ストレステストで損失率が閾値を超えました。次にすべきは？', opts: ['リスクレポート作成・対策検討', '無視', 'テスト中止'], correct: 0, correctReason: 'レポートと対策検討により、規制対応とリスク管理の改善につながります。', wrongReasons: ['', '無視は規制違反や経営リスクにつながります。', 'テスト中止では対策が立てられません。'] },
  { q: 'ストレステスト結果を経営に報告する際、含めるべきは？', opts: ['シナリオ別損失・資本充足率・対策案', '数値のみ', '報告不要'], correct: 0, correctReason: 'シナリオ・対策案を含めることで、経営判断の材料になります。', wrongReasons: ['', '数値のみでは判断材料が不足します。', '報告は規制上求められる場合があります。'] },
];
// 統合セキュリティ・防衛 実務学習（イベント・インシデント・リスクを分離）
const SECURITY_LEARN_EVENT: LearnStep[] = [
  { q: 'セキュリティイベントで「Critical」が検出されました。最初にすべきは？', opts: ['送信元・送信先・影響範囲の確認', 'ログのみ保存', '後日対応'], correct: 0, correctReason: '送信元・送信先・影響範囲を確認することで、インシデント対応の優先度と対策方針を決められます。', wrongReasons: ['', 'ログ保存は必須ですが、まず状況把握が先です。', '後日対応では被害拡大のリスクがあります。'] },
  { q: 'IDS/IPSで複数のイベントが検出されています。優先すべきは？', opts: ['Critical/Highを優先し、影響範囲を特定', 'すべて同時対応', 'ログのみ保存'], correct: 0, correctReason: '重大度順に対応し、影響範囲を特定することで効率的に封じ込められます。', wrongReasons: ['', '同時対応は非効率で、重要な見逃しのリスクがあります。', '保存のみでは被害拡大を防げません。'] },
  { q: 'イベントの誤検知（False Positive）が多発しています。適切な対応は？', opts: ['ルール・閾値の見直し・チューニング', 'アラート無効化', '放置'], correct: 0, correctReason: 'ルール見直しにより、重要なイベントを見逃さずノイズを減らせます。', wrongReasons: ['', '無効化は本当の攻撃を見逃すリスクがあります。', '放置はアラート疲れで重要な見逃しにつながります。'] },
];
const SECURITY_LEARN_INCIDENT: LearnStep[] = [
  { q: 'インシデントが「未対応」のままです。適切な対応は？', opts: ['優先度付けして対応開始', '放置', '自動クローズ'], correct: 0, correctReason: '優先度付けにより、影響の大きいものから効率的に対応できます。', wrongReasons: ['', '放置は被害拡大や再発のリスクを高めます。', '自動クローズは未対応のまま残るため不適切です。'] },
  { q: 'インシデント対応を完了した後、記録すべきは？', opts: ['対応内容・根因・再発防止策', 'クローズのみ', '記録不要'], correct: 0, correctReason: '対応内容・根因・再発防止策を記録することで、同様事象の防止に活用できます。', wrongReasons: ['', 'クローズのみでは再発防止の分析ができません。', '記録はインシデント管理の基本です。'] },
];
const SECURITY_LEARN_RISK: LearnStep[] = [
  { q: 'リスク分析で高レベルが複数あります。優先すべきは？', opts: ['影響範囲が広いものから対応', 'すべて同時', '後回し'], correct: 0, correctReason: '影響範囲が広いものから対応することで、リスク低減効果を最大化できます。', wrongReasons: ['', 'すべて同時はリソース分散で非効率です。', '後回しはリスクを放置することになります。'] },
  { q: 'リスク対策を実施した後、確認すべきは？', opts: ['対策の有効性・残存リスクの評価', '実施のみ', '評価不要'], correct: 0, correctReason: '有効性と残存リスクの評価により、追加対策の要否を判断できます。', wrongReasons: ['', '実施のみでは効果が不明です。', '評価はリスク管理の継続改善に必要です。'] },
];
// インフラ・運用系 実務学習（IaC・オーケストレーション・監視・最適化を分離）
const INFRA_OPS_LEARN_IAC: LearnStep[] = [
  { q: 'IaCで「ドリフト検知」が出ました。最初にすべきは？', opts: ['差分確認・原因調査', '即時上書き', '無視'], correct: 0, correctReason: '差分と原因を確認することで、意図的な変更か不正変更かを判断し、適切な是正ができます。', wrongReasons: ['', '即時上書きは意図しない変更を上書きするリスクがあります。', '無視は設定の不整合を放置することになります。'] },
  { q: 'ドリフトの原因が手動変更だった場合、適切な対応は？', opts: ['IaCに反映し、手動変更を禁止する運用に', 'そのまま放置', 'IaCを手動に合わせて上書き'], correct: 0, correctReason: 'IaCに反映することで、設定の一元管理と再現性を保てます。', wrongReasons: ['', '放置はドリフトが再発します。', '上書きは意図しない変更を固定化するリスクがあります。'] },
  { q: 'IaCのapplyが失敗しました。最初にすべきは？', opts: ['エラーメッセージ・状態の確認', '再実行のみ', '手動で修正'], correct: 0, correctReason: 'エラー内容を確認することで、依存関係・権限・リソース制限などを切り分けできます。', wrongReasons: ['', '再実行のみでは同じ失敗を繰り返します。', '手動修正はドリフトの原因になります。'] },
];
const INFRA_OPS_LEARN_ORCH: LearnStep[] = [
  { q: 'デプロイメントが「Pending」のままです。次にすべきは？', opts: ['承認フロー確認・実行', 'キャンセル', '放置'], correct: 0, correctReason: '承認フローを確認し実行することで、適切なリリース管理ができます。', wrongReasons: ['', 'キャンセルは必要なデプロイを止める可能性があります。', '放置はデプロイが滞留し、運用に支障が出ます。'] },
  { q: 'K8sのレプリカ数が期待値と異なります。最初にすべきは？', opts: ['デプロイメント・Pod状態の確認', '即時スケール', '無視'], correct: 0, correctReason: '状態確認により、オートスケーラー・障害・設定ミスなどを切り分けできます。', wrongReasons: ['', '即時スケールは原因不明のままでは不適切です。', '無視は可用性に影響する可能性があります。'] },
];
const INFRA_OPS_LEARN_MONITOR: LearnStep[] = [
  { q: '監視アラートが「未対応」です。適切な対応は？', opts: ['重大度順に確認・対応', '一括無視', '自動解除'], correct: 0, correctReason: '重大度順に対応することで、影響の大きい問題を優先的に解消できます。', wrongReasons: ['', '一括無視は障害の見逃しにつながります。', '自動解除は根本対応になっていません。'] },
  { q: 'アラートが多発してノイズになっています。適切な対応は？', opts: ['閾値・アラートルールの見直し', 'すべて無効化', 'そのまま放置'], correct: 0, correctReason: '閾値・ルールの見直しにより、重要なアラートを見逃さず、ノイズを減らせます。', wrongReasons: ['', '無効化は重要なアラートも見逃します。', '放置はアラート疲れで本当に重要なものを見逃します。'] },
];
const INFRA_OPS_LEARN_OPT: LearnStep[] = [
  { q: 'FinOpsで「アイドルリソース」の推奨が出ました。最初にすべきは？', opts: ['使用状況・依存関係の確認', '即時削除', '無視'], correct: 0, correctReason: '使用状況を確認することで、本当に不要か・他から参照されていないかを判断できます。', wrongReasons: ['', '即時削除は稼働中リソースを止めるリスクがあります。', '無視はコスト削減の機会を逃します。'] },
  { q: '最適化推奨を実施した後、確認すべきは？', opts: ['コスト削減効果・パフォーマンス影響', '実施のみ', '確認不要'], correct: 0, correctReason: '効果と影響を確認することで、追加の最適化やロールバックの要否を判断できます。', wrongReasons: ['', '実施のみでは効果が不明です。', '確認は継続的な最適化に必要です。'] },
];
// DX・データ系 実務学習（データレイク・MLモデル・生成AI・パイプラインを分離）
const DX_DATA_LEARN_LAKE: LearnStep[] = [
  { q: 'データレイクの取り込みが遅延しています。最初にすべきは？', opts: ['パイプライン・ソースの状態確認', '再実行のみ', '無視'], correct: 0, correctReason: '状態確認により、ソース障害・ネットワーク・リソース不足などを切り分けできます。', wrongReasons: ['', '再実行のみでは同じ遅延を繰り返す可能性があります。', '無視はデータ鮮度の低下につながります。'] },
  { q: 'データレイクのスキーマが変更されました。適切な対応は？', opts: ['パイプライン・ダウンストリームの影響確認', '即時反映', '無視'], correct: 0, correctReason: '影響確認により、破壊的変更を防ぎ、段階的な移行ができます。', wrongReasons: ['', '即時反映はダウンストリームを壊す可能性があります。', '無視はデータ不整合の原因になります。'] },
];
const DX_DATA_LEARN_ML: LearnStep[] = [
  { q: 'MLモデルの精度が低下しています。適切な対応は？', opts: ['再学習・データドリフト確認', 'モデルそのまま', '削除'], correct: 0, correctReason: '再学習・データドリフト確認により、データの変化を把握し、モデルの再適合ができます。', wrongReasons: ['', 'そのままでは精度低下が続きます。', '削除は過剰対応。まず原因確認が先です。'] },
  { q: '本番モデルの推論遅延が増加しています。最初にすべきは？', opts: ['リソース・入力データ量・モデルサイズの確認', '即時スケールアップ', '無視'], correct: 0, correctReason: '確認により、ボトルネックを特定し、適切な対策（スケール・最適化）を決められます。', wrongReasons: ['', '即時スケールは原因不明のままではコスト増の可能性があります。', '無視はSLA違反のリスクがあります。'] },
];
const DX_DATA_LEARN_GENAI: LearnStep[] = [
  { q: '生成AIの利用量が急増しています。確認すべきは？', opts: ['利用目的・コスト・ガバナンス', '制限のみ', '無視'], correct: 0, correctReason: '利用目的・コスト・ガバナンスを確認することで、適切な運用とコスト管理ができます。', wrongReasons: ['', '制限のみでは正当な利用を阻害する可能性があります。', '無視はコスト超過やガバナンス違反のリスクがあります。'] },
  { q: '生成AIの出力にハルシネーションが含まれています。適切な対応は？', opts: ['RAG・プロンプトの改善・人間レビューの強化', '出力をそのまま使用', '利用中止'], correct: 0, correctReason: 'RAG・プロンプト改善により精度向上、人間レビューで最終確認ができます。', wrongReasons: ['', 'そのまま使用は誤情報の拡散リスクがあります。', '利用中止は過剰対応。改善で対応可能です。'] },
];
const DX_DATA_LEARN_PIPELINE: LearnStep[] = [
  { q: 'データパイプラインが「失敗」です。最初にすべきは？', opts: ['エラーログ・失敗ステップの確認', '再実行のみ', '無視'], correct: 0, correctReason: 'エラーログと失敗ステップを確認することで、原因を特定し、適切な修正ができます。', wrongReasons: ['', '再実行のみでは同じ原因で再失敗する可能性があります。', '無視はデータ品質の低下につながります。'] },
  { q: 'パイプラインの依存関係が複雑になっています。適切な対応は？', opts: ['DAGの整理・モジュール化・ドキュメント化', 'そのまま継続', 'すべて統合'], correct: 0, correctReason: '整理・モジュール化により、保守性と可観測性が向上します。', wrongReasons: ['', 'そのままでは障害時の切り分けが困難になります。', '統合は単一障害点のリスクを高めます。'] },
];
// コンプライアンス・ガバナンス系 実務学習（規制・監査ログ・ポリシー・監査指摘を分離）
const COMPLIANCE_LEARN_REG: LearnStep[] = [
  { q: '規制対応スコアが閾値を下回りました。最初にすべきは？', opts: ['該当規制・ギャップの特定', 'スコアのみ更新', '無視'], correct: 0, correctReason: '該当規制とギャップを特定することで、具体的な是正措置を策定できます。', wrongReasons: ['', 'スコア更新だけでは実態の改善になりません。', '無視は規制違反のリスクを高めます。'] },
  { q: '新規制が施行されました。適切な対応は？', opts: ['影響範囲の洗い出し・ギャップ分析・対策計画', '後日対応', '無視'], correct: 0, correctReason: '影響範囲の洗い出しにより、必要な対応を漏れなく実施できます。', wrongReasons: ['', '後日では施行日に違反するリスクがあります。', '無視は規制違反につながります。'] },
];
const COMPLIANCE_LEARN_AUDITLOG: LearnStep[] = [
  { q: '監査ログに不整合があります。次にすべきは？', opts: ['原因調査・是正', 'ログ削除', '無視'], correct: 0, correctReason: '原因調査と是正により、整合性を回復し、監査の信頼性を保てます。', wrongReasons: ['', 'ログ削除は証跡の改ざんになり、規制違反の可能性があります。', '無視は監査上の問題を放置することになります。'] },
  { q: '監査ログの保持期間が近づいています。適切な対応は？', opts: ['アーカイブ・保持ポリシーの確認', '即時削除', 'そのまま放置'], correct: 0, correctReason: 'アーカイブにより規制要件を満たしつつ、ストレージを最適化できます。', wrongReasons: ['', '即時削除は保持期間違反の可能性があります。', '放置はストレージ逼迫のリスクがあります。'] },
];
const COMPLIANCE_LEARN_POLICY: LearnStep[] = [
  { q: 'ポリシー改定が必要です。適切な手順は？', opts: ['影響分析・ステークホルダー合意・改定・周知', '即時改定', '改定不要'], correct: 0, correctReason: '影響分析と合意により、実効性のあるポリシーにできます。', wrongReasons: ['', '即時改定は現場の混乱を招く可能性があります。', '改定不要は規制変更に対応できません。'] },
  { q: 'ポリシー違反が検出されました。最初にすべきは？', opts: ['違反内容・影響範囲の確認', '即時懲戒', '無視'], correct: 0, correctReason: '確認により、意図的か偶発的か・再発防止策を判断できます。', wrongReasons: ['', '即時懲戒は調査不足で不当な処分になる可能性があります。', '無視は違反の常態化につながります。'] },
];
const COMPLIANCE_LEARN_FINDING: LearnStep[] = [
  { q: '監査指摘が「未対応」です。適切な対応は？', opts: ['対策計画策定・実施', '指摘のみ記録', '後回し'], correct: 0, correctReason: '対策計画の策定と実施により、指摘事項の解消と再発防止ができます。', wrongReasons: ['', '記録のみでは指摘は解消されません。', '後回しは次回監査で問題になります。'] },
  { q: '監査指摘の対応完了後、確認すべきは？', opts: ['再発防止策の有効性・証跡の整備', '完了のみ', '確認不要'], correct: 0, correctReason: '有効性確認により、フォローアップ監査で指摘されないようにできます。', wrongReasons: ['', '完了のみでは再発の可能性が残ります。', '確認は監査対応の基本です。'] },
];
// サプライチェーン系 実務学習（物流・在庫・調達・需要予測を分離）
const SUPPLY_CHAIN_LEARN_LOGISTICS: LearnStep[] = [
  { q: '物流配送が遅延しています。適切な対応は？', opts: ['追跡・顧客への連絡', '放置', 'キャンセル'], correct: 0, correctReason: '追跡と顧客連絡により、状況把握と顧客満足の維持ができます。', wrongReasons: ['', '放置は顧客クレームや信頼低下につながります。', 'キャンセルは過剰対応。まず追跡と連絡が先です。'] },
  { q: '複数便の配送が遅延しています。優先すべきは？', opts: ['緊急度・顧客重要度の高い順に連絡', 'すべて同時連絡', '後回し'], correct: 0, correctReason: '優先度付けにより、影響の大きい顧客から迅速に対応できます。', wrongReasons: ['', '同時連絡は非効率で、重要な顧客への対応が遅れます。', '後回しは顧客離脱のリスクがあります。'] },
];
const SUPPLY_CHAIN_LEARN_INV: LearnStep[] = [
  { q: '在庫で「要発注」のアイテムがあります。最初にすべきは？', opts: ['発注点・リードタイムの確認', '即時発注', '無視'], correct: 0, correctReason: '発注点・リードタイムを確認することで、適切な発注量とタイミングを決められます。', wrongReasons: ['', '即時発注は過剰在庫や在庫切れのリスクがあります。まず確認が先です。', '無視は在庫切れのリスクを高めます。'] },
  { q: '在庫の実地棚卸で差異が出ました。適切な対応は？', opts: ['差異原因の調査・在庫修正・プロセス改善', '数値のみ修正', '無視'], correct: 0, correctReason: '原因調査により、盗難・記録ミス・ロット不良などを特定し、再発防止ができます。', wrongReasons: ['', '数値のみでは同じ差異が再発する可能性があります。', '無視は在庫精度の低下につながります。'] },
];
const SUPPLY_CHAIN_LEARN_PROC: LearnStep[] = [
  { q: '調達発注の納期が遅延しそうです。適切な対応は？', opts: ['サプライヤーへの確認・代替調達の検討', 'そのまま待つ', '即時キャンセル'], correct: 0, correctReason: '確認と代替検討により、生産計画への影響を最小化できます。', wrongReasons: ['', '待つのみでは生産停止のリスクがあります。', '即時キャンセルは過剰対応。まず確認が先です。'] },
  { q: '調達単価が急騰しています。最初にすべきは？', opts: ['要因分析・複数サプライヤーの比較・交渉', '即時発注', '調達中止'], correct: 0, correctReason: '要因分析により、一時的要因か構造的要因かを判断し、適切な調達戦略を決められます。', wrongReasons: ['', '即時発注は高値掴みのリスクがあります。', '調達中止は生産停止につながります。'] },
];
const SUPPLY_CHAIN_LEARN_DEMAND: LearnStep[] = [
  { q: '需要予測の精度が低下しています。次にすべきは？', opts: ['モデル・入力データの見直し', '予測無視', '在庫増のみ'], correct: 0, correctReason: 'モデル・入力データの見直しにより、予測精度の改善と適正在庫の維持ができます。', wrongReasons: ['', '予測無視は在庫計画が崩れます。', '在庫増のみは過剰在庫のリスクがあります。'] },
  { q: '需要予測と実績の乖離が続いています。適切な対応は？', opts: ['モデル再学習・外れ値除外・説明変数の見直し', '予測を実績に合わせる', 'そのまま継続'], correct: 0, correctReason: 'モデル見直しにより、市場変化に対応した予測ができます。', wrongReasons: ['', '実績に合わせるだけでは将来予測になりません。', '継続では乖離が拡大します。'] },
];

const DOMAIN_LABELS: Record<number, string> = {
  0: 'manufacturing', 1: 'medical', 2: 'fintech', 3: 'security',
  4: 'infra_ops', 5: 'dx_data', 6: 'compliance_governance', 7: 'supply_chain',
};

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
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      if (!silent) setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

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
    if (!practiceMode || practiceDomainIndices.length === 0) return;
    const id = setInterval(() => {
      setDomainTab((prev) => {
        const idx = practiceDomainIndices.indexOf(prev);
        const nextIdx = idx < 0 ? 0 : (idx + 1) % practiceDomainIndices.length;
        return practiceDomainIndices[nextIdx];
      });
    }, practiceIntervalSec * 1000);
    return () => clearInterval(id);
  }, [practiceMode, practiceIntervalSec, practiceDomainIndices]);

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

  const getSeverityColor = (s: string) => {
    const v = (s || '').toLowerCase();
    return ['高', 'critical', 'high'].includes(v) ? 'error' : ['中', 'medium'].includes(v) ? 'warning' : 'info';
  };
  const getStatusColor = (s: string) =>
    s === '要確認' || s === '監視中' ? 'warning' : s === '完了' ? 'success' : 'default';
  const getRiskColor = (level: string) =>
    ['高', 'high'].includes(level || '') ? 'error' : level === '中' ? 'warning' : 'success';

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
      <Typography variant={isMobile ? 'h6' : 'h5'} component="h1" gutterBottom>
        産業統合プラットフォーム
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph sx={{ fontSize: isMobile ? '0.8rem' : undefined }}>
        製造・IoT / 医療・ヘルスケア / 金融・FinTech / 統合セキュリティ・防衛等 を1つの画面でシミュレーション
      </Typography>

      <FormControl size="small" sx={{ minWidth: 140, mb: 2 }}>
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

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={domainTab} onChange={(_, v) => setDomainTab(v)} variant="scrollable" scrollButtons="auto">
          <Tab icon={<PrecisionManufacturing />} label="製造・IoT" iconPosition="start" />
          <Tab icon={<LocalHospital />} label="医療・ヘルスケア" iconPosition="start" />
          <Tab icon={<AccountBalance />} label="金融・FinTech" iconPosition="start" />
          <Tab icon={<Shield />} label="統合セキュリティ・防衛" iconPosition="start" />
          <Tab icon={<Cloud />} label="インフラ・運用系" iconPosition="start" />
          <Tab icon={<Storage />} label="DX・データ系" iconPosition="start" />
          <Tab icon={<Gavel />} label="コンプライアンス・ガバナンス" iconPosition="start" />
          <Tab icon={<LocalShipping />} label="サプライチェーン" iconPosition="start" />
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
        <Tooltip title="CSVファイルをアップロードしてデータを取り込み">
          <Chip icon={<UploadFile />} label="CSV取り込み" onClick={() => { setCsvImportOpen(true); setCsvData([]); setCsvError(''); }} variant="outlined" />
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
                  const res = await dataIntegrationApi.importCsv(csvData, domain);
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

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>{error}</Alert>}

      {loading ? (
        <Box sx={{ p: 4, textAlign: 'center' }}><CircularProgress /></Box>
      ) : (
        <>
          <TabPanel value={domainTab} index={0}>
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
              <Chip icon={<PrecisionManufacturing />} label="予知保全" onClick={() => setManufacturingSubTab(0)} color={manufacturingSubTab === 0 ? 'primary' : 'default'} />
              <Chip icon={<Sensors />} label="センサーデータ" onClick={() => setManufacturingSubTab(1)} color={manufacturingSubTab === 1 ? 'primary' : 'default'} />
              <Chip icon={<Warning />} label="異常検知" onClick={() => setManufacturingSubTab(2)} color={manufacturingSubTab === 2 ? 'primary' : 'default'} />
              <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setManufacturingSubTab(3); setManufacturingLearnType(0); setManufacturingLearnStep(p['manufacturing_0'] ?? 0); setManufacturingLearnSelected(null); setManufacturingLearnFeedback(null); }} color={manufacturingSubTab === 3 ? 'primary' : 'default'} />
            </Stack>
            {manufacturingSubTab === 0 && (
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
            {manufacturingSubTab === 1 && (
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
            {manufacturingSubTab === 2 && (
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
            {manufacturingSubTab === 3 && (
              <Box>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip label="予知保全" onClick={() => { const p = loadLearnProgress(); setManufacturingLearnType(0); setManufacturingLearnStep(p['manufacturing_0'] ?? 0); setManufacturingLearnSelected(null); setManufacturingLearnFeedback(null); }} color={manufacturingLearnType === 0 ? 'primary' : 'default'} variant={manufacturingLearnType === 0 ? 'filled' : 'outlined'} />
                  <Chip label="センサーデータ" onClick={() => { const p = loadLearnProgress(); setManufacturingLearnType(1); setManufacturingLearnStep(p['manufacturing_1'] ?? 0); setManufacturingLearnSelected(null); setManufacturingLearnFeedback(null); }} color={manufacturingLearnType === 1 ? 'primary' : 'default'} variant={manufacturingLearnType === 1 ? 'filled' : 'outlined'} />
                  <Chip label="異常検知" onClick={() => { const p = loadLearnProgress(); setManufacturingLearnType(2); setManufacturingLearnStep(p['manufacturing_2'] ?? 0); setManufacturingLearnSelected(null); setManufacturingLearnFeedback(null); }} color={manufacturingLearnType === 2 ? 'primary' : 'default'} variant={manufacturingLearnType === 2 ? 'filled' : 'outlined'} />
                </Stack>
                <LearnPanel
                  steps={manufacturingLearnType === 0 ? MANUFACTURING_LEARN_PREDICTIVE : manufacturingLearnType === 1 ? MANUFACTURING_LEARN_SENSOR : MANUFACTURING_LEARN_ANOMALY}
                  stepIndex={manufacturingLearnStep}
                  setStepIndex={setManufacturingLearnStep}
                  selected={manufacturingLearnSelected}
                  setSelected={setManufacturingLearnSelected}
                  feedback={manufacturingLearnFeedback}
                  setFeedback={setManufacturingLearnFeedback}
                  onReset={() => { setManufacturingLearnStep(0); setManufacturingLearnSelected(null); setManufacturingLearnFeedback(null); }}
                />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={domainTab} index={1}>
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
              <Chip icon={<Psychology />} label="AI診断" onClick={() => setMedicalSubTab(0)} color={medicalSubTab === 0 ? 'primary' : 'default'} />
              <Chip icon={<RecordVoiceOver />} label="音声応答" onClick={() => setMedicalSubTab(1)} color={medicalSubTab === 1 ? 'primary' : 'default'} />
              <Chip icon={<Warning />} label="異常検知" onClick={() => setMedicalSubTab(2)} color={medicalSubTab === 2 ? 'primary' : 'default'} />
              <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setMedicalSubTab(3); setMedicalLearnType(0); setMedicalLearnStep(p['medical_0'] ?? 0); setMedicalLearnSelected(null); setMedicalLearnFeedback(null); }} color={medicalSubTab === 3 ? 'primary' : 'default'} />
            </Stack>
            {medicalSubTab === 0 && (
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
            {medicalSubTab === 1 && (
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
            {medicalSubTab === 2 && (
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
            {medicalSubTab === 3 && (
              <Box>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip label="AI診断" onClick={() => { const p = loadLearnProgress(); setMedicalLearnType(0); setMedicalLearnStep(p['medical_0'] ?? 0); setMedicalLearnSelected(null); setMedicalLearnFeedback(null); }} color={medicalLearnType === 0 ? 'primary' : 'default'} variant={medicalLearnType === 0 ? 'filled' : 'outlined'} />
                  <Chip label="音声応答" onClick={() => { const p = loadLearnProgress(); setMedicalLearnType(1); setMedicalLearnStep(p['medical_1'] ?? 0); setMedicalLearnSelected(null); setMedicalLearnFeedback(null); }} color={medicalLearnType === 1 ? 'primary' : 'default'} variant={medicalLearnType === 1 ? 'filled' : 'outlined'} />
                  <Chip label="異常検知" onClick={() => { const p = loadLearnProgress(); setMedicalLearnType(2); setMedicalLearnStep(p['medical_2'] ?? 0); setMedicalLearnSelected(null); setMedicalLearnFeedback(null); }} color={medicalLearnType === 2 ? 'primary' : 'default'} variant={medicalLearnType === 2 ? 'filled' : 'outlined'} />
                </Stack>
                <LearnPanel steps={medicalLearnType === 0 ? MEDICAL_LEARN_AI : medicalLearnType === 1 ? MEDICAL_LEARN_VOICE : MEDICAL_LEARN_ANOMALY} stepIndex={medicalLearnStep} setStepIndex={setMedicalLearnStep} selected={medicalLearnSelected} setSelected={setMedicalLearnSelected} feedback={medicalLearnFeedback} setFeedback={setMedicalLearnFeedback} onReset={() => { setMedicalLearnStep(0); setMedicalLearnSelected(null); setMedicalLearnFeedback(null); }} />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={domainTab} index={2}>
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
              <Chip icon={<Payment />} label="決済" onClick={() => setFintechSubTab(0)} color={fintechSubTab === 0 ? 'primary' : 'default'} />
              <Chip icon={<Security />} label="リスクスコア" onClick={() => setFintechSubTab(1)} color={fintechSubTab === 1 ? 'primary' : 'default'} />
              <Chip icon={<Visibility />} label="取引監視" onClick={() => setFintechSubTab(2)} color={fintechSubTab === 2 ? 'primary' : 'default'} />
              <Chip icon={<Science />} label="ストレステスト" onClick={() => setFintechSubTab(3)} color={fintechSubTab === 3 ? 'primary' : 'default'} />
              <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setFintechSubTab(4); setFintechLearnType(0); setFintechLearnStep(p['fintech_0'] ?? 0); setFintechLearnSelected(null); setFintechLearnFeedback(null); }} color={fintechSubTab === 4 ? 'primary' : 'default'} />
            </Stack>
            {fintechSubTab === 0 && (
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
            {fintechSubTab === 1 && (
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
            {fintechSubTab === 2 && (
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
            {fintechSubTab === 3 && (
              <Stack spacing={2}>
                <Stack direction="row" spacing={2} alignItems="center">
                  <TextField type="number" label="ポートフォリオ価値（円）" value={portfolioValue} onChange={(e) => setPortfolioValue(Number(e.target.value) || 1000000)} size="small" sx={{ width: 220 }} />
                  <Button variant="contained" onClick={handleStressTest} disabled={loading}>ストレステスト実行</Button>
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
            {fintechSubTab === 4 && (
              <Box>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip label="決済" onClick={() => { const p = loadLearnProgress(); setFintechLearnType(0); setFintechLearnStep(p['fintech_0'] ?? 0); setFintechLearnSelected(null); setFintechLearnFeedback(null); }} color={fintechLearnType === 0 ? 'primary' : 'default'} variant={fintechLearnType === 0 ? 'filled' : 'outlined'} />
                  <Chip label="リスクスコア" onClick={() => { const p = loadLearnProgress(); setFintechLearnType(1); setFintechLearnStep(p['fintech_1'] ?? 0); setFintechLearnSelected(null); setFintechLearnFeedback(null); }} color={fintechLearnType === 1 ? 'primary' : 'default'} variant={fintechLearnType === 1 ? 'filled' : 'outlined'} />
                  <Chip label="取引監視" onClick={() => { const p = loadLearnProgress(); setFintechLearnType(2); setFintechLearnStep(p['fintech_2'] ?? 0); setFintechLearnSelected(null); setFintechLearnFeedback(null); }} color={fintechLearnType === 2 ? 'primary' : 'default'} variant={fintechLearnType === 2 ? 'filled' : 'outlined'} />
                  <Chip label="ストレステスト" onClick={() => { const p = loadLearnProgress(); setFintechLearnType(3); setFintechLearnStep(p['fintech_3'] ?? 0); setFintechLearnSelected(null); setFintechLearnFeedback(null); }} color={fintechLearnType === 3 ? 'primary' : 'default'} variant={fintechLearnType === 3 ? 'filled' : 'outlined'} />
                </Stack>
                <LearnPanel steps={fintechLearnType === 0 ? FINTECH_LEARN_PAYMENT : fintechLearnType === 1 ? FINTECH_LEARN_RISK : fintechLearnType === 2 ? FINTECH_LEARN_MONITOR : FINTECH_LEARN_STRESS} stepIndex={fintechLearnStep} setStepIndex={setFintechLearnStep} selected={fintechLearnSelected} setSelected={setFintechLearnSelected} feedback={fintechLearnFeedback} setFeedback={setFintechLearnFeedback} onReset={() => { setFintechLearnStep(0); setFintechLearnSelected(null); setFintechLearnFeedback(null); }} />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={domainTab} index={3}>
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
              <Chip icon={<Shield />} label="イベント" onClick={() => setSecuritySubTab(0)} color={securitySubTab === 0 ? 'primary' : 'default'} />
              <Chip icon={<Warning />} label="インシデント" onClick={() => setSecuritySubTab(1)} color={securitySubTab === 1 ? 'primary' : 'default'} />
              <Chip icon={<Security />} label="リスク" onClick={() => setSecuritySubTab(2)} color={securitySubTab === 2 ? 'primary' : 'default'} />
              <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSecuritySubTab(3); setSecurityLearnType(0); setSecurityLearnStep(p['security_0'] ?? 0); setSecurityLearnSelected(null); setSecurityLearnFeedback(null); }} color={securitySubTab === 3 ? 'primary' : 'default'} />
            </Stack>
            {securitySubTab === 0 && (
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
            {securitySubTab === 1 && (
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
            {securitySubTab === 2 && (
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
            {securitySubTab === 3 && (
              <Box>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip label="イベント" onClick={() => { const p = loadLearnProgress(); setSecurityLearnType(0); setSecurityLearnStep(p['security_0'] ?? 0); setSecurityLearnSelected(null); setSecurityLearnFeedback(null); }} color={securityLearnType === 0 ? 'primary' : 'default'} variant={securityLearnType === 0 ? 'filled' : 'outlined'} />
                  <Chip label="インシデント" onClick={() => { const p = loadLearnProgress(); setSecurityLearnType(1); setSecurityLearnStep(p['security_1'] ?? 0); setSecurityLearnSelected(null); setSecurityLearnFeedback(null); }} color={securityLearnType === 1 ? 'primary' : 'default'} variant={securityLearnType === 1 ? 'filled' : 'outlined'} />
                  <Chip label="リスク" onClick={() => { const p = loadLearnProgress(); setSecurityLearnType(2); setSecurityLearnStep(p['security_2'] ?? 0); setSecurityLearnSelected(null); setSecurityLearnFeedback(null); }} color={securityLearnType === 2 ? 'primary' : 'default'} variant={securityLearnType === 2 ? 'filled' : 'outlined'} />
                </Stack>
                <LearnPanel steps={securityLearnType === 0 ? SECURITY_LEARN_EVENT : securityLearnType === 1 ? SECURITY_LEARN_INCIDENT : SECURITY_LEARN_RISK} stepIndex={securityLearnStep} setStepIndex={setSecurityLearnStep} selected={securityLearnSelected} setSelected={setSecurityLearnSelected} feedback={securityLearnFeedback} setFeedback={setSecurityLearnFeedback} onReset={() => { setSecurityLearnStep(0); setSecurityLearnSelected(null); setSecurityLearnFeedback(null); }} />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={domainTab} index={4}>
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
              <Chip icon={<Build />} label="IaC" onClick={() => setInfraOpsSubTab(0)} color={infraOpsSubTab === 0 ? 'primary' : 'default'} />
              <Chip icon={<Cloud />} label="オーケストレーション" onClick={() => setInfraOpsSubTab(1)} color={infraOpsSubTab === 1 ? 'primary' : 'default'} />
              <Chip icon={<Visibility />} label="監視アラート" onClick={() => setInfraOpsSubTab(2)} color={infraOpsSubTab === 2 ? 'primary' : 'default'} />
              <Chip icon={<Science />} label="最適化推奨" onClick={() => setInfraOpsSubTab(3)} color={infraOpsSubTab === 3 ? 'primary' : 'default'} />
              <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setInfraOpsSubTab(4); setInfraOpsLearnType(0); setInfraOpsLearnStep(p['infraOps_0'] ?? 0); setInfraOpsLearnSelected(null); setInfraOpsLearnFeedback(null); }} color={infraOpsSubTab === 4 ? 'primary' : 'default'} />
            </Stack>
            {infraOpsSubTab === 0 && (
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
            {infraOpsSubTab === 1 && (
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
            {infraOpsSubTab === 2 && (
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
            {infraOpsSubTab === 3 && (
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
            {infraOpsSubTab === 4 && (
              <Box>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip label="IaC" onClick={() => { const p = loadLearnProgress(); setInfraOpsLearnType(0); setInfraOpsLearnStep(p['infraOps_0'] ?? 0); setInfraOpsLearnSelected(null); setInfraOpsLearnFeedback(null); }} color={infraOpsLearnType === 0 ? 'primary' : 'default'} variant={infraOpsLearnType === 0 ? 'filled' : 'outlined'} />
                  <Chip label="オーケストレーション" onClick={() => { const p = loadLearnProgress(); setInfraOpsLearnType(1); setInfraOpsLearnStep(p['infraOps_1'] ?? 0); setInfraOpsLearnSelected(null); setInfraOpsLearnFeedback(null); }} color={infraOpsLearnType === 1 ? 'primary' : 'default'} variant={infraOpsLearnType === 1 ? 'filled' : 'outlined'} />
                  <Chip label="監視" onClick={() => { const p = loadLearnProgress(); setInfraOpsLearnType(2); setInfraOpsLearnStep(p['infraOps_2'] ?? 0); setInfraOpsLearnSelected(null); setInfraOpsLearnFeedback(null); }} color={infraOpsLearnType === 2 ? 'primary' : 'default'} variant={infraOpsLearnType === 2 ? 'filled' : 'outlined'} />
                  <Chip label="最適化" onClick={() => { const p = loadLearnProgress(); setInfraOpsLearnType(3); setInfraOpsLearnStep(p['infraOps_3'] ?? 0); setInfraOpsLearnSelected(null); setInfraOpsLearnFeedback(null); }} color={infraOpsLearnType === 3 ? 'primary' : 'default'} variant={infraOpsLearnType === 3 ? 'filled' : 'outlined'} />
                </Stack>
                <LearnPanel steps={infraOpsLearnType === 0 ? INFRA_OPS_LEARN_IAC : infraOpsLearnType === 1 ? INFRA_OPS_LEARN_ORCH : infraOpsLearnType === 2 ? INFRA_OPS_LEARN_MONITOR : INFRA_OPS_LEARN_OPT} stepIndex={infraOpsLearnStep} setStepIndex={setInfraOpsLearnStep} selected={infraOpsLearnSelected} setSelected={setInfraOpsLearnSelected} feedback={infraOpsLearnFeedback} setFeedback={setInfraOpsLearnFeedback} onReset={() => { setInfraOpsLearnStep(0); setInfraOpsLearnSelected(null); setInfraOpsLearnFeedback(null); }} />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={domainTab} index={5}>
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
              <Chip icon={<Storage />} label="データレイク" onClick={() => setDxDataSubTab(0)} color={dxDataSubTab === 0 ? 'primary' : 'default'} />
              <Chip icon={<Science />} label="MLモデル" onClick={() => setDxDataSubTab(1)} color={dxDataSubTab === 1 ? 'primary' : 'default'} />
              <Chip icon={<Psychology />} label="生成AI" onClick={() => setDxDataSubTab(2)} color={dxDataSubTab === 2 ? 'primary' : 'default'} />
              <Chip icon={<Timeline />} label="パイプライン" onClick={() => setDxDataSubTab(3)} color={dxDataSubTab === 3 ? 'primary' : 'default'} />
              <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setDxDataSubTab(4); setDxDataLearnType(0); setDxDataLearnStep(p['dxData_0'] ?? 0); setDxDataLearnSelected(null); setDxDataLearnFeedback(null); }} color={dxDataSubTab === 4 ? 'primary' : 'default'} />
            </Stack>
            {dxDataSubTab === 0 && (
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
            {dxDataSubTab === 1 && (
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
            {dxDataSubTab === 2 && (
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
            {dxDataSubTab === 3 && (
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
            {dxDataSubTab === 4 && (
              <Box>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip label="データレイク" onClick={() => { const p = loadLearnProgress(); setDxDataLearnType(0); setDxDataLearnStep(p['dxData_0'] ?? 0); setDxDataLearnSelected(null); setDxDataLearnFeedback(null); }} color={dxDataLearnType === 0 ? 'primary' : 'default'} variant={dxDataLearnType === 0 ? 'filled' : 'outlined'} />
                  <Chip label="MLモデル" onClick={() => { const p = loadLearnProgress(); setDxDataLearnType(1); setDxDataLearnStep(p['dxData_1'] ?? 0); setDxDataLearnSelected(null); setDxDataLearnFeedback(null); }} color={dxDataLearnType === 1 ? 'primary' : 'default'} variant={dxDataLearnType === 1 ? 'filled' : 'outlined'} />
                  <Chip label="生成AI" onClick={() => { const p = loadLearnProgress(); setDxDataLearnType(2); setDxDataLearnStep(p['dxData_2'] ?? 0); setDxDataLearnSelected(null); setDxDataLearnFeedback(null); }} color={dxDataLearnType === 2 ? 'primary' : 'default'} variant={dxDataLearnType === 2 ? 'filled' : 'outlined'} />
                  <Chip label="パイプライン" onClick={() => { const p = loadLearnProgress(); setDxDataLearnType(3); setDxDataLearnStep(p['dxData_3'] ?? 0); setDxDataLearnSelected(null); setDxDataLearnFeedback(null); }} color={dxDataLearnType === 3 ? 'primary' : 'default'} variant={dxDataLearnType === 3 ? 'filled' : 'outlined'} />
                </Stack>
                <LearnPanel steps={dxDataLearnType === 0 ? DX_DATA_LEARN_LAKE : dxDataLearnType === 1 ? DX_DATA_LEARN_ML : dxDataLearnType === 2 ? DX_DATA_LEARN_GENAI : DX_DATA_LEARN_PIPELINE} stepIndex={dxDataLearnStep} setStepIndex={setDxDataLearnStep} selected={dxDataLearnSelected} setSelected={setDxDataLearnSelected} feedback={dxDataLearnFeedback} setFeedback={setDxDataLearnFeedback} onReset={() => { setDxDataLearnStep(0); setDxDataLearnSelected(null); setDxDataLearnFeedback(null); }} />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={domainTab} index={6}>
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
              <Chip icon={<Gavel />} label="規制対応" onClick={() => setComplianceSubTab(0)} color={complianceSubTab === 0 ? 'primary' : 'default'} />
              <Chip icon={<Visibility />} label="監査ログ" onClick={() => setComplianceSubTab(1)} color={complianceSubTab === 1 ? 'primary' : 'default'} />
              <Chip icon={<Policy />} label="ポリシー" onClick={() => setComplianceSubTab(2)} color={complianceSubTab === 2 ? 'primary' : 'default'} />
              <Chip icon={<Warning />} label="監査指摘" onClick={() => setComplianceSubTab(3)} color={complianceSubTab === 3 ? 'primary' : 'default'} />
              <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setComplianceSubTab(4); setComplianceLearnType(0); setComplianceLearnStep(p['compliance_0'] ?? 0); setComplianceLearnSelected(null); setComplianceLearnFeedback(null); }} color={complianceSubTab === 4 ? 'primary' : 'default'} />
            </Stack>
            {complianceSubTab === 0 && (
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
            {complianceSubTab === 1 && (
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
            {complianceSubTab === 2 && (
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
            {complianceSubTab === 3 && (
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
            {complianceSubTab === 4 && (
              <Box>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip label="規制対応" onClick={() => { const p = loadLearnProgress(); setComplianceLearnType(0); setComplianceLearnStep(p['compliance_0'] ?? 0); setComplianceLearnSelected(null); setComplianceLearnFeedback(null); }} color={complianceLearnType === 0 ? 'primary' : 'default'} variant={complianceLearnType === 0 ? 'filled' : 'outlined'} />
                  <Chip label="監査ログ" onClick={() => { const p = loadLearnProgress(); setComplianceLearnType(1); setComplianceLearnStep(p['compliance_1'] ?? 0); setComplianceLearnSelected(null); setComplianceLearnFeedback(null); }} color={complianceLearnType === 1 ? 'primary' : 'default'} variant={complianceLearnType === 1 ? 'filled' : 'outlined'} />
                  <Chip label="ポリシー" onClick={() => { const p = loadLearnProgress(); setComplianceLearnType(2); setComplianceLearnStep(p['compliance_2'] ?? 0); setComplianceLearnSelected(null); setComplianceLearnFeedback(null); }} color={complianceLearnType === 2 ? 'primary' : 'default'} variant={complianceLearnType === 2 ? 'filled' : 'outlined'} />
                  <Chip label="監査指摘" onClick={() => { const p = loadLearnProgress(); setComplianceLearnType(3); setComplianceLearnStep(p['compliance_3'] ?? 0); setComplianceLearnSelected(null); setComplianceLearnFeedback(null); }} color={complianceLearnType === 3 ? 'primary' : 'default'} variant={complianceLearnType === 3 ? 'filled' : 'outlined'} />
                </Stack>
                <LearnPanel steps={complianceLearnType === 0 ? COMPLIANCE_LEARN_REG : complianceLearnType === 1 ? COMPLIANCE_LEARN_AUDITLOG : complianceLearnType === 2 ? COMPLIANCE_LEARN_POLICY : COMPLIANCE_LEARN_FINDING} stepIndex={complianceLearnStep} setStepIndex={setComplianceLearnStep} selected={complianceLearnSelected} setSelected={setComplianceLearnSelected} feedback={complianceLearnFeedback} setFeedback={setComplianceLearnFeedback} onReset={() => { setComplianceLearnStep(0); setComplianceLearnSelected(null); setComplianceLearnFeedback(null); }} />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={domainTab} index={7}>
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
              <Chip icon={<LocalShipping />} label="物流" onClick={() => setSupplyChainSubTab(0)} color={supplyChainSubTab === 0 ? 'primary' : 'default'} />
              <Chip icon={<Inventory />} label="在庫" onClick={() => setSupplyChainSubTab(1)} color={supplyChainSubTab === 1 ? 'primary' : 'default'} />
              <Chip icon={<Payment />} label="調達" onClick={() => setSupplyChainSubTab(2)} color={supplyChainSubTab === 2 ? 'primary' : 'default'} />
              <Chip icon={<Timeline />} label="需要予測" onClick={() => setSupplyChainSubTab(3)} color={supplyChainSubTab === 3 ? 'primary' : 'default'} />
              <Chip icon={<School />} label="実務学習" onClick={() => { const p = loadLearnProgress(); setSupplyChainSubTab(4); setSupplyChainLearnType(0); setSupplyChainLearnStep(p['supplyChain_0'] ?? 0); setSupplyChainLearnSelected(null); setSupplyChainLearnFeedback(null); }} color={supplyChainSubTab === 4 ? 'primary' : 'default'} />
            </Stack>
            {supplyChainSubTab === 0 && (
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
            {supplyChainSubTab === 1 && (
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
            {supplyChainSubTab === 2 && (
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
            {supplyChainSubTab === 3 && (
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
            {supplyChainSubTab === 4 && (
              <Box>
                <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                  <Chip label="物流" onClick={() => { const p = loadLearnProgress(); setSupplyChainLearnType(0); setSupplyChainLearnStep(p['supplyChain_0'] ?? 0); setSupplyChainLearnSelected(null); setSupplyChainLearnFeedback(null); }} color={supplyChainLearnType === 0 ? 'primary' : 'default'} variant={supplyChainLearnType === 0 ? 'filled' : 'outlined'} />
                  <Chip label="在庫" onClick={() => { const p = loadLearnProgress(); setSupplyChainLearnType(1); setSupplyChainLearnStep(p['supplyChain_1'] ?? 0); setSupplyChainLearnSelected(null); setSupplyChainLearnFeedback(null); }} color={supplyChainLearnType === 1 ? 'primary' : 'default'} variant={supplyChainLearnType === 1 ? 'filled' : 'outlined'} />
                  <Chip label="調達" onClick={() => { const p = loadLearnProgress(); setSupplyChainLearnType(2); setSupplyChainLearnStep(p['supplyChain_2'] ?? 0); setSupplyChainLearnSelected(null); setSupplyChainLearnFeedback(null); }} color={supplyChainLearnType === 2 ? 'primary' : 'default'} variant={supplyChainLearnType === 2 ? 'filled' : 'outlined'} />
                  <Chip label="需要予測" onClick={() => { const p = loadLearnProgress(); setSupplyChainLearnType(3); setSupplyChainLearnStep(p['supplyChain_3'] ?? 0); setSupplyChainLearnSelected(null); setSupplyChainLearnFeedback(null); }} color={supplyChainLearnType === 3 ? 'primary' : 'default'} variant={supplyChainLearnType === 3 ? 'filled' : 'outlined'} />
                </Stack>
                <LearnPanel steps={supplyChainLearnType === 0 ? SUPPLY_CHAIN_LEARN_LOGISTICS : supplyChainLearnType === 1 ? SUPPLY_CHAIN_LEARN_INV : supplyChainLearnType === 2 ? SUPPLY_CHAIN_LEARN_PROC : SUPPLY_CHAIN_LEARN_DEMAND} stepIndex={supplyChainLearnStep} setStepIndex={setSupplyChainLearnStep} selected={supplyChainLearnSelected} setSelected={setSupplyChainLearnSelected} feedback={supplyChainLearnFeedback} setFeedback={setSupplyChainLearnFeedback} onReset={() => { setSupplyChainLearnStep(0); setSupplyChainLearnSelected(null); setSupplyChainLearnFeedback(null); }} />
              </Box>
            )}
          </TabPanel>
        </>
      )}
    </Box>
  );
};
