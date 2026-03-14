/**
 * 統合基盤モジュール（5モジュール）概要ページ
 * 5つのモジュールの説明を1画面で表示
 * 自動切替: 概要 → 製造・IoT → 医療 → 金融・FinTech → インクルーシブ雇用AI → 契約ワークフロー
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Chip,
  IconButton,
  FormControlLabel,
  Switch,
} from '@mui/material';
import {
  PrecisionManufacturing,
  LocalHospital,
  AccountBalance,
  Work,
  Assignment,
  ArrowForward,
  PlayArrow,
  VolumeUp,
  VolumeOff,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAutoPlay } from '../../contexts/AutoPlayContext';
import { AUTO_PLAY_STEPS } from '../../contexts/AutoPlayContext';
import { speak } from '../../lib/speech';

interface ModuleInfo {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  dataSource: string;
  path: string;
  icon: React.ReactNode;
  features: string[];
}

const modules: ModuleInfo[] = [
  { id: 'manufacturing', title: '製造・MLOps', subtitle: '予知保全・センサーデータ・異常検知', description: '製造業DXの需要が高い予知保全、センサーデータ収集、異常検知を提供。インフラ・監視・MLOpsとの相性が良く、設備の残余寿命（RUL）予測やIoT連携に対応。', dataSource: 'NASA C-MAPSS（シーマップス）など公開データで実機モードに対応済み。', path: '/manufacturing', icon: <PrecisionManufacturing fontSize="large" />, features: ['予知保全API', 'センサーデータ', '異常検知', 'MLOps', 'Prometheus', 'Grafana'] },
  { id: 'medical', title: '医療', subtitle: 'AI診断・音声応答・異常検知', description: '医療プラットフォーム向けのAI診断支援、音声応答、異常検知機能。MLOps基盤との連携により、医療データの分析・可視化をサポート。', dataSource: '患者情報の規制により、デモではサンプルデータを使用。顧客PoCでは実データ連携に置き換えて検証可能。', path: '/medical', icon: <LocalHospital fontSize="large" />, features: ['AI診断', '音声応答', '異常検知', '医療プラットフォーム'] },
  { id: 'fintech', title: '金融', subtitle: '決済・リスク・取引監視', description: '決済API、リスクスコア、取引監視を提供。高可用性・低レイテンシ・監視の経験を活かした金融システム基盤。', dataSource: '決済・取引データの機密性により、デモではサンプルデータを使用。顧客PoCでは実データ連携に置き換えて検証可能。', path: '/fintech', icon: <AccountBalance fontSize="large" />, features: ['決済API', 'リスクスコア', '取引監視', '高可用性'] },
  { id: 'inclusive-work', title: '障害者雇用', subtitle: 'マッチング・アクセシビリティAI・UX評価', description: '障害者雇用マッチング、アクセシビリティ特化AI、UX評価を統合。適性に応じた職種提案や、シンプルUI評価によりインクルーシブな雇用を支援。', dataSource: '求人データの提供元との契約が必要。個人開発のデモでは実データの取得が難しいためサンプルを使用。顧客PoCでは実データ連携に置き換えて検証可能。', path: '/inclusive-work', icon: <Work fontSize="large" />, features: ['マッチング', 'チャットAI', 'UX評価', 'エージェント'] },
  { id: 'contract-workflow', title: '契約ワークフロー', subtitle: '見積・契約・納品・請求の一気通貫', description: '見積・契約・納品・請求を一気通貫で管理。DB化・PDF出力・実データ運用に対応し、契約業務の効率化を実現。', dataSource: 'もともと実データのみで運用。', path: '/contract-workflow', icon: <Assignment fontSize="large" />, features: ['見積', '契約', '納品', '請求', 'PDF出力'] },
];

export const IntegratedModulesOverviewPage: React.FC = () => {
  const navigate = useNavigate();
  const autoPlay = useAutoPlay();
  const isAutoPlaying = autoPlay?.isAutoPlaying ?? false;
  const startAutoPlay = autoPlay?.startAutoPlay ?? (() => {});
  const narrationEnabled = autoPlay?.narrationEnabled ?? true;
  const setNarrationEnabled = autoPlay?.setNarrationEnabled ?? (() => {});
  const navigateToNextStep = autoPlay?.navigateToNextStep ?? (() => {});
  const [voicesReady, setVoicesReady] = useState(false);
  const hasSpeech = typeof window !== 'undefined' && 'speechSynthesis' in window;

  useEffect(() => {
    if (!hasSpeech) return;
    const loadVoices = () => {
      const v = window.speechSynthesis.getVoices();
      if (v.length > 0) setVoicesReady(true);
    };
    loadVoices();
    window.speechSynthesis.addEventListener('voiceschanged', loadVoices);
    return () => window.speechSynthesis.removeEventListener('voiceschanged', loadVoices);
  }, [hasSpeech]);

  const handlePlay = () => {
    startAutoPlay();
    const step = AUTO_PLAY_STEPS[0];
    if (narrationEnabled && hasSpeech && step) {
      speak(step.narration, 'ja-JP', () => {
        setTimeout(navigateToNextStep, 1500);
      });
    } else {
      setTimeout(navigateToNextStep, 500);
    }
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          統合基盤モジュール（5モジュール）概要
        </Typography>
        <Typography variant="body2" color="text.secondary">
          UEP v5.0 の統合基盤を構成する5つのモジュールの説明です。再生ボタンで、各モジュール画面を順に自動切替・ナレーション付きでご覧いただけます。
          {hasSpeech && !voicesReady && ' （音声読み込み中… 試聴ボタンで確認）'}
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 2, mb: 2, p: 2, borderRadius: 1, bgcolor: 'action.hover' }}>
        <IconButton onClick={handlePlay} color="primary" disabled={isAutoPlaying} aria-label="自動切替開始">
          <PlayArrow />
        </IconButton>
        <Typography variant="body2" color="text.secondary">
          5モジュール概要 → 製造・IoT → 医療 → 金融・FinTech → インクルーシブ雇用AI → 契約ワークフロー
        </Typography>
        {hasSpeech && (
          <>
            <FormControlLabel
              control={<Switch checked={narrationEnabled} onChange={(_, v) => setNarrationEnabled(v)} size="small" />}
              label={<Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>{narrationEnabled ? <VolumeUp fontSize="small" /> : <VolumeOff fontSize="small" />}<span>ナレーション</span></Box>}
            />
            <IconButton size="small" onClick={() => speak('5モジュール概要のナレーションです。音声が聞こえていますか？', 'ja-JP')} aria-label="ナレーション試聴" title="ナレーション試聴">
              <VolumeUp />
            </IconButton>
          </>
        )}
      </Box>

      <Grid container spacing={2}>
        {modules.map((mod) => (
          <Grid item xs={12} md={6} key={mod.id}>
            <Card variant="outlined" sx={{ height: '100%', transition: 'border-color 0.2s, box-shadow 0.2s', '&:hover': { borderColor: 'primary.main', boxShadow: 1 } }}>
              <CardActionArea onClick={() => navigate(mod.path)} sx={{ height: '100%', display: 'block', textAlign: 'left' }} aria-label={`${mod.title}の詳細へ`}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, mb: 1.5 }}>
                    <Box sx={{ color: 'primary.main', display: 'flex', alignItems: 'center', justifyContent: 'center', width: 48, height: 48, borderRadius: 1, bgcolor: 'action.hover' }}>{mod.icon}</Box>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="h6" fontWeight={600}>{mod.title}</Typography>
                      <Typography variant="caption" color="text.secondary">{mod.subtitle}</Typography>
                    </Box>
                    <ArrowForward sx={{ color: 'text.secondary', fontSize: 20 }} />
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>{mod.description}</Typography>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1, fontStyle: 'italic' }}><strong>データの出処:</strong> {mod.dataSource}</Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {mod.features.map((f) => <Chip key={f} label={f} size="small" variant="outlined" sx={{ fontSize: '0.7rem' }} />)}
                  </Box>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 3, p: 2, borderRadius: 1, bgcolor: 'action.hover', borderLeft: '4px solid', borderColor: 'primary.main' }}>
        <Typography variant="subtitle2" fontWeight={600} gutterBottom>データの出処について</Typography>
        <Typography variant="body2" color="text.secondary" component="div">
          <ul style={{ margin: '0.5rem 0', paddingLeft: '1.2rem' }}>
            <li><strong>製造:</strong> NASA C-MAPSS（シーマップス）など公開データで実機モードに対応済み。</li>
            <li><strong>医療:</strong> 患者情報の規制により、デモではサンプルデータを使用。顧客PoCでは実データ連携に置き換えて検証可能。</li>
            <li><strong>金融:</strong> 決済・取引データの機密性により、デモではサンプルデータを使用。顧客PoCでは実データ連携に置き換えて検証可能。</li>
            <li><strong>インクルーシブ雇用:</strong> 求人データの提供元との契約が必要。個人開発のデモでは実データの取得が難しいためサンプルを使用。顧客PoCでは実データ連携に置き換えて検証可能。</li>
            <li><strong>契約・納品・請求:</strong> もともと実データのみで運用。</li>
          </ul>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
            顧客PoC（ピーオーシー）では、各領域の実データ連携に置き換えて検証可能です。
          </Typography>
        </Typography>
      </Box>
    </Box>
  );
};
