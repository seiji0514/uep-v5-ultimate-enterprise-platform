/**
 * 5モジュール詳細説明ページ
 * 想定ユースケース・システム構成・データの出処・公開データ活用を1画面でナレーション付き説明
 * 読み上げ箇所とスクロールを連動（データの出処・公開データ活用は該当セクションへ自動スクロール）
 */
import React, { useEffect, useRef } from 'react';
import { Box, Typography, Button } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAutoPlay } from '../../contexts/AutoPlayContext';
import { speakSequence } from '../../lib/speech';

const NARRATION_STEP_INDEX = 1 as const;

const NARRATION_PARTS = [
  { text: '想定ユースケース。製造と契約の連携で、予知保全アラートから発注フローを自動起動。医療と障害者雇用で、病院の採用マッチングを支援。金融と製造で、設備投資の融資判断を支援。' },
  { text: 'システム構成は、React、FastAPI、各モジュールAPIがRESTで連携。Prometheusでメトリクス収集、Grafanaで可視化。' },
  { text: 'データの出処は、製造はNASA C-MAPSSなど公開データ、契約は実データ運用中、医療・金融・障害者雇用はPoCで実データ連携可能です。顧客PoCでは各領域の実データに置き換えて検証できます。' },
  { text: '公開データの拡張として、MIMIC-III、PhysioNet、Kaggle、厚労省オープンデータなどが利用可能です。各モジュールのダッシュボードを充実できます。' },
];

export const OverviewDetailPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const autoPlay = useAutoPlay();
  const isAutoPlaying = autoPlay?.isAutoPlaying ?? false;
  const currentStep = autoPlay?.currentStep ?? 0;
  const narrationEnabled = autoPlay?.narrationEnabled ?? true;
  const navigateToNextStep = autoPlay?.navigateToNextStep ?? (() => {});
  const stateStep = (location.state as { autoPlayStep?: number })?.autoPlayStep;
  const shouldSpeak = isAutoPlaying && narrationEnabled && (currentStep === NARRATION_STEP_INDEX || stateStep === NARRATION_STEP_INDEX);

  const refUseCase = useRef<HTMLDivElement>(null);
  const refArch = useRef<HTMLDivElement>(null);
  const refDataSource = useRef<HTMLDivElement>(null);
  const refPublicData = useRef<HTMLDivElement>(null);
  const hasPlayedRef = useRef(false);

  useEffect(() => {
    if (!shouldSpeak) return;
    if (hasPlayedRef.current) return;
    hasPlayedRef.current = true;
    const items = NARRATION_PARTS.map((p, i) => ({
      text: p.text,
      onBefore: () => {
        const refs = [refUseCase, refArch, refDataSource, refPublicData];
        refs[i]?.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      },
    }));
    speakSequence(items, 'ja-JP', () => {
      setTimeout(navigateToNextStep, 1500);
    });
    return () => { hasPlayedRef.current = false; };
  }, [shouldSpeak, navigateToNextStep]);

  return (
    <Box sx={{ p: 0 }}>
      <Button
        startIcon={<ArrowBack />}
        onClick={() => navigate('/integrated-modules')}
        sx={{ mb: 2 }}
        size="small"
      >
        5モジュール概要へ戻る
      </Button>

      <Typography variant="h5" fontWeight={600} gutterBottom sx={{ mb: 3 }}>
        統合基盤の詳細
      </Typography>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        <Box ref={refUseCase} sx={{ p: 2, borderRadius: 1, bgcolor: 'action.hover', borderLeft: '4px solid', borderColor: 'info.main' }}>
          <Typography variant="subtitle2" fontWeight={600} gutterBottom color="info.main">想定ユースケース（モジュール間連携）</Typography>
          <Typography variant="body2" color="text.secondary" component="div">
            <ul style={{ margin: '0.5rem 0', paddingLeft: '1.2rem' }}>
              <li><strong>製造×契約:</strong> 設備メンテナンス部品の発注・見積・契約・納品・請求を一気通貫で連携。予知保全のアラートから自動で発注フローを起動。</li>
              <li><strong>医療×障害者雇用:</strong> 医療機関の採用と障害者雇用マッチングを連携。病院の職種ニーズとアクセシビリティ評価を統合し、適性マッチングを支援。</li>
              <li><strong>金融×製造:</strong> 設備投資・サプライチェーン金融と製造データを連携。稼働率・異常検知結果をリスクスコアに反映し、融資判断を支援。</li>
              <li><strong>契約×医療・金融:</strong> 医療機器・金融サービスの契約・NDA・SLA管理を契約ワークフローで一元管理。</li>
            </ul>
          </Typography>
        </Box>

        <Box ref={refArch} sx={{ p: 2, borderRadius: 1, bgcolor: 'action.hover', borderLeft: '4px solid', borderColor: 'secondary.main' }}>
          <Typography variant="subtitle2" fontWeight={600} gutterBottom color="secondary.main">システム構成・監視・運用</Typography>
          <Typography variant="body2" color="text.secondary" component="div" sx={{ mb: 2 }}>
            フロントエンド（React）、バックエンド（FastAPI）、各モジュールAPIがRESTで連携。製造モジュールではPrometheusでメトリクス収集、Grafanaで可視化・アラートを実装済み。
          </Typography>
          <Box sx={{ fontFamily: 'monospace', fontSize: '0.75rem', p: 1.5, borderRadius: 1, bgcolor: 'background.default', overflow: 'auto' }}>
            <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>{`[クライアント] → [React SPA] → [FastAPI Gateway]
                              ↓
    ┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
    │ 製造・IoT   │ 医療        │ 金融        │ 障害者雇用  │ 契約WF      │
    │ (予知保全)  │ (AI診断)    │ (決済)      │ (マッチング)│ (見積〜請求)│
    └──────┬──────┴─────────────┴─────────────┴─────────────┴─────────────┘
           │
    [Prometheus] ← メトリクス収集
           ↓
    [Grafana] ← 可視化・アラート・ダッシュボード`}</pre>
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
            Prometheus: 時系列メトリクス収集。Grafana: ダッシュボード・アラート・異常検知の可視化。製造モジュールで実装済み、他モジュールへ拡張可能。
          </Typography>
        </Box>

        <Box ref={refDataSource} sx={{ p: 2, borderRadius: 1, bgcolor: 'action.hover', borderLeft: '4px solid', borderColor: 'primary.main' }}>
          <Typography variant="subtitle2" fontWeight={600} gutterBottom color="primary.main">データの出処について</Typography>
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

        <Box ref={refPublicData} sx={{ p: 2, borderRadius: 1, bgcolor: 'action.hover', borderLeft: '4px solid', borderColor: 'success.main' }}>
          <Typography variant="subtitle2" fontWeight={600} gutterBottom color="success.main">公開データ活用の拡張可能性</Typography>
          <Typography variant="body2" color="text.secondary" component="div">
            <ul style={{ margin: '0.5rem 0', paddingLeft: '1.2rem' }}>
              <li><strong>製造:</strong> NASA C-MAPSS で実装済み。他にも MIMIC-III（医療）、UCI Machine Learning など公開データセットとの連携が可能。</li>
              <li><strong>医療:</strong> MIMIC-III、PhysioNet など匿名化された医療データでPoC検証が可能。デモではサンプル、顧客環境では実データに置換。</li>
              <li><strong>金融:</strong> Kaggle のクレジットカード不正検知、取引シミュレーションデータなどでリスクモデル・異常検知の検証が可能。</li>
              <li><strong>障害者雇用:</strong> 公的求人オープンデータ（厚労省など）との連携でマッチング精度の検証が可能。</li>
            </ul>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
              各モジュールのダッシュボードは、上記公開データを組み込むことで指標・グラフを充実できます。
            </Typography>
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};
