/**
 * 統合基盤モジュール（5モジュール）概要ページ
 * 5つのモジュールの説明を1画面で表示
 * 読み上げ箇所とスクロールを連動
 */
import React, { useState, useEffect, useRef } from 'react';
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
import { useNavigate, useLocation } from 'react-router-dom';
import { useAutoPlay } from '../../contexts/AutoPlayContext';
import { speak, speakSequence } from '../../lib/speech';

interface ModuleInfo {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  dataSource: string;
  verificationStatus: string;
  path: string;
  icon: React.ReactNode;
  features: string[];
}

const NARRATION_PARTS = [
  { text: '統合基盤モジュール、5つのモジュールの概要です。' },
  { text: 'なぜ5モジュールか。製造・医療・金融・障害者雇用・契約ワークフローを統合することで、業界横断のデータ連携と共通基盤の再利用を実現。顧客PoC・本番導入が可能な設計です。' },
  { text: '検証状況。製造は公開データ検証済み、契約は実データ運用中、医療・金融・障害者雇用はPoCで実データ連携可能です。' },
  { text: '製造・IoT、医療、金融、障害者雇用、契約ワークフローを順にご紹介します。顧客PoCでは、各領域の実データ連携に置き換えて検証可能です。' },
];

const modules: ModuleInfo[] = [
  { id: 'manufacturing', title: '製造・MLOps', subtitle: '予知保全・センサーデータ・異常検知', description: '製造業DXの需要が高い予知保全、センサーデータ収集、異常検知を提供。インフラ・監視・MLOpsとの相性が良く、設備の残余寿命（RUL）予測やIoT連携に対応。', dataSource: 'NASA C-MAPSS（シーマップス）など公開データで実機モードに対応済み。', verificationStatus: '公開データ検証済み', path: '/manufacturing', icon: <PrecisionManufacturing fontSize="large" />, features: ['予知保全API', 'センサーデータ', '異常検知', 'MLOps', 'Prometheus', 'Grafana'] },
  { id: 'medical', title: '医療', subtitle: 'AI診断・音声応答・異常検知', description: '医療プラットフォーム向けのAI診断支援、音声応答、異常検知機能。MLOps基盤との連携により、医療データの分析・可視化をサポート。', dataSource: '患者情報の規制により、デモではサンプルデータを使用。顧客PoCでは実データ連携に置き換えて検証可能。', verificationStatus: 'PoC実データ連携可', path: '/medical', icon: <LocalHospital fontSize="large" />, features: ['AI診断', '音声応答', '異常検知', '医療プラットフォーム'] },
  { id: 'fintech', title: '金融', subtitle: '決済・リスク・取引監視', description: '決済API、リスクスコア、取引監視を提供。高可用性・低レイテンシ・監視の経験を活かした金融システム基盤。', dataSource: '決済・取引データの機密性により、デモではサンプルデータを使用。顧客PoCでは実データ連携に置き換えて検証可能。', verificationStatus: 'PoC実データ連携可', path: '/fintech', icon: <AccountBalance fontSize="large" />, features: ['決済API', 'リスクスコア', '取引監視', '高可用性'] },
  { id: 'inclusive-work', title: '障害者雇用', subtitle: 'マッチング・アクセシビリティAI・UX評価', description: '障害者雇用マッチング、アクセシビリティ特化AI、UX評価を統合。適性に応じた職種提案や、シンプルUI評価によりインクルーシブな雇用を支援。', dataSource: '求人データの提供元との契約が必要。個人開発のデモでは実データの取得が難しいためサンプルを使用。顧客PoCでは実データ連携に置き換えて検証可能。', verificationStatus: 'PoC実データ連携可', path: '/inclusive-work', icon: <Work fontSize="large" />, features: ['マッチング', 'チャットAI', 'UX評価', 'エージェント'] },
  { id: 'contract-workflow', title: '契約ワークフロー', subtitle: '見積・契約・納品・請求の一気通貫', description: '見積・契約・納品・請求を一気通貫で管理。DB化・PDF出力・実データ運用に対応し、契約業務の効率化を実現。', dataSource: 'もともと実データのみで運用。', verificationStatus: '実データ運用中', path: '/contract-workflow', icon: <Assignment fontSize="large" />, features: ['見積', '契約', '納品', '請求', 'PDF出力'] },
];

export const IntegratedModulesOverviewPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const autoPlay = useAutoPlay();
  const isAutoPlaying = autoPlay?.isAutoPlaying ?? false;
  const startAutoPlay = autoPlay?.startAutoPlay ?? (() => {});
  const narrationEnabled = autoPlay?.narrationEnabled ?? true;
  const setNarrationEnabled = autoPlay?.setNarrationEnabled ?? (() => {});
  const setHidePlayBar = autoPlay?.setHidePlayBar ?? (() => {});
  const hidePlayBar = autoPlay?.hidePlayBar ?? false;
  const navigateToNextStep = autoPlay?.navigateToNextStep ?? (() => {});
  const currentStep = autoPlay?.currentStep ?? 0;
  const stateStep = (location.state as { autoPlayStep?: number })?.autoPlayStep;
  const shouldSpeak = isAutoPlaying && (currentStep === 0 || stateStep === 0);
  const [voicesReady, setVoicesReady] = useState(false);
  const hasSpeech = typeof window !== 'undefined' && 'speechSynthesis' in window;

  const refHeader = useRef<HTMLDivElement>(null);
  const refWhy5 = useRef<HTMLDivElement>(null);
  const refVerification = useRef<HTMLDivElement>(null);
  const refModules = useRef<HTMLDivElement>(null);
  const hasPlayedRef = useRef(false);

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

  useEffect(() => {
    if (!shouldSpeak || !narrationEnabled || !hasSpeech) return;
    if (hasPlayedRef.current) return;
    hasPlayedRef.current = true;
    const refs = [refHeader, refWhy5, refVerification, refModules];
    const items = NARRATION_PARTS.map((p, i) => ({
      text: p.text,
      onBefore: () => refs[i]?.current?.scrollIntoView({ behavior: 'smooth', block: 'center' }),
    }));
    speakSequence(items, 'ja-JP', () => {
      setTimeout(navigateToNextStep, 1500);
    });
    return () => { hasPlayedRef.current = false; };
  }, [shouldSpeak, narrationEnabled, hasSpeech, navigateToNextStep]);

  const handlePlay = () => {
    startAutoPlay();
    if (narrationEnabled && hasSpeech) {
      hasPlayedRef.current = false;
      // useEffect が shouldSpeak で発火するので、startAutoPlay 後に自動でナレーション開始
    } else {
      setTimeout(navigateToNextStep, 500);
    }
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box ref={refHeader} sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          統合基盤モジュール（5モジュール）概要
        </Typography>
        <Typography variant="body2" color="text.secondary">
          UEP v5.0 の統合基盤を構成する5つのモジュールの説明です。再生ボタンで、各モジュール画面を順に自動切替・ナレーション付きでご覧いただけます。
          {hasSpeech && !voicesReady && ' （音声読み込み中… 試聴ボタンで確認）'}
        </Typography>
      </Box>

      <Box ref={refWhy5} sx={{ mb: 2, p: 2, borderRadius: 1, bgcolor: 'action.hover', borderLeft: '4px solid', borderColor: 'success.main' }}>
        <Typography variant="subtitle2" fontWeight={600} gutterBottom color="success.main">なぜ5モジュールか</Typography>
        <Typography variant="body2" color="text.secondary" component="div">
          製造・医療・金融・障害者雇用・契約ワークフローを統合することで、<strong>業界横断のデータ連携</strong>と<strong>共通基盤の再利用</strong>を実現。各領域の実データ連携に置き換えることで、顧客PoC・本番導入が可能な設計です。
        </Typography>
      </Box>

      <Box ref={refVerification} sx={{ mb: 2, p: 1.5, borderRadius: 1, bgcolor: 'action.selected', display: 'flex', flexWrap: 'wrap', gap: 1, alignItems: 'center' }}>
        <Typography variant="caption" fontWeight={600} sx={{ mr: 1 }}>検証状況サマリ:</Typography>
        <Chip size="small" label="製造: 公開データ検証済み" color="success" sx={{ fontSize: '0.7rem' }} />
        <Chip size="small" label="契約: 実データ運用中" color="success" sx={{ fontSize: '0.7rem' }} />
        <Chip size="small" label="医療・金融・障害者雇用: PoC実データ連携可" color="info" sx={{ fontSize: '0.7rem' }} />
      </Box>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 2, mb: 2, p: 2, borderRadius: 1, bgcolor: 'action.hover' }}>
        <IconButton onClick={handlePlay} color="primary" disabled={isAutoPlaying} aria-label="自動切替開始">
          <PlayArrow />
        </IconButton>
        <Typography variant="body2" color="text.secondary">
          5モジュール概要 → 詳細説明 → 製造・IoT → 医療 → 金融・FinTech → インクルーシブ雇用AI → 契約ワークフロー
          {hasSpeech && ' （Spaceキーで一時停止/再開）'}
        </Typography>
        {hasSpeech && (
          <>
            <FormControlLabel
              control={<Switch checked={narrationEnabled} onChange={(_, v) => setNarrationEnabled(v)} size="small" />}
              label={<Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>{narrationEnabled ? <VolumeUp fontSize="small" /> : <VolumeOff fontSize="small" />}<span>ナレーション</span></Box>}
            />
            <FormControlLabel
              control={<Switch checked={hidePlayBar} onChange={(_, v) => setHidePlayBar(v)} size="small" />}
              label={<span>再生中バーを非表示（画面共有用）</span>}
            />
            <IconButton size="small" onClick={() => speak('5モジュール概要のナレーションです。音声が聞こえていますか？', 'ja-JP')} aria-label="ナレーション試聴" title="ナレーション試聴">
              <VolumeUp />
            </IconButton>
          </>
        )}
      </Box>

      <Box ref={refModules}>
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
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1, flexWrap: 'wrap' }}>
                    <Chip size="small" label={mod.verificationStatus} color={mod.verificationStatus.includes('検証済み') || mod.verificationStatus.includes('実運用') ? 'success' : 'info'} sx={{ fontSize: '0.65rem' }} />
                    <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic' }}><strong>データ:</strong> {mod.dataSource}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {mod.features.map((f) => <Chip key={f} label={f} size="small" variant="outlined" sx={{ fontSize: '0.7rem' }} />)}
                  </Box>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
      </Box>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
        <Typography
          component="button"
          variant="body2"
          onClick={() => navigate('/integrated-modules/detail')}
          sx={{
            color: 'primary.main',
            cursor: 'pointer',
            textDecoration: 'underline',
            background: 'none',
            border: 'none',
            font: 'inherit',
          }}
        >
          想定ユースケース・システム構成・データの出処・公開データ活用の詳細を見る →
        </Typography>
      </Box>
    </Box>
  );
};
