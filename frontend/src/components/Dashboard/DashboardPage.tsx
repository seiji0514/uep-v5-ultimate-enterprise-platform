/**
 * ダッシュボードページ
 * 統合ダッシュボード・画面構成（24カラムグリッド、パネル、左寄せタイトル）
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  IconButton,
  Chip,
  CircularProgress,
} from '@mui/material';
import {
  Science,
  Cloud,
  Build,
  Public,
  FolderSpecial,
  ArrowForward,
  BugReport,
  Work,
  PrecisionManufacturing,
  AccountBalance,
  Bolt,
  LocalHospital,
  Satellite,
  Traffic,
  Hub,
  OpenInNew,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { apiClient } from '../../api/client';

const getIndustryUnifiedUrl = () => {
  const base = process.env.REACT_APP_INDUSTRY_UNIFIED_URL || 'http://localhost:3010';
  const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;
  return token ? `${base}?token=${encodeURIComponent(token)}` : base;
};

const getEOHUrl = () => {
  const base = process.env.REACT_APP_EOH_URL || 'http://localhost:3020';
  const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;
  return token ? `${base}?token=${encodeURIComponent(token)}` : base;
};

interface PanelProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  path: string;
  color: string;
  span?: number; // 1-24（24カラムグリッド）
  external?: boolean; // 外部リンク（別アプリ）の場合 true
}

const DashboardPanel: React.FC<PanelProps> = ({ title, description, icon, path, color, span = 8, external }) => {
  const navigate = useNavigate();
  const handleClick = () => {
    if (external) {
      window.open(path, '_blank', 'noopener,noreferrer');
    } else {
      navigate(path);
    }
  };
  return (
    <Grid item xs={12} sm={12} md={span} lg={span}>
      <Paper
        component="article"
        role="button"
        tabIndex={0}
        aria-label={`${title}へ移動`}
        sx={{
          p: 2,
          height: '100%',
          minHeight: 140,
          cursor: 'pointer',
          transition: 'border-color 0.2s',
          '&:hover': {
            borderColor: color,
            '& .panel-action': { opacity: 1 },
          },
          '&:focus-visible': {
            outline: '2px solid',
            outlineColor: 'primary.main',
          },
        }}
        onClick={handleClick}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleClick(); } }}
        elevation={0}
      >
        {/* 左寄せパネルヘッダー */}
        <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 1.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Box sx={{ color, display: 'flex', alignItems: 'center' }}>{icon}</Box>
            <Typography variant="subtitle1" fontWeight={600} sx={{ color: 'text.primary' }}>
              {title}
            </Typography>
          </Box>
          <IconButton size="small" className="panel-action" sx={{ opacity: 0.6 }} aria-hidden>
            {external ? <OpenInNew fontSize="small" /> : <ArrowForward fontSize="small" />}
          </IconButton>
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.5 }}>
          {description}
        </Typography>
      </Paper>
    </Grid>
  );
};

interface ActionItems {
  manufacturing?: number;
  medical?: number;
  fintech?: number;
  inclusive_work?: number;
  contract?: number;
  total?: number;
}

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [actionItems, setActionItems] = useState<ActionItems | null>(null);
  const [actionItemsLoading, setActionItemsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    apiClient.get<ActionItems>('/api/v1/cross-module/action-items')
      .then((r) => { if (!cancelled) setActionItems(r.data); })
      .catch(() => { if (!cancelled) setActionItems(null); })
      .finally(() => { if (!cancelled) setActionItemsLoading(false); });
    return () => { cancelled = true; };
  }, []);

  const panels: PanelProps[] = [
    {
      title: 'プロジェクト一覧',
      description: 'プロジェクト単位で横断管理。チーム開発・役割分担を想定',
      icon: <FolderSpecial />,
      path: '/projects',
      color: '#F46800',
      span: 12,
    },
    {
      title: '産業統合プラットフォーム',
      description: '製造・医療・金融・セキュリティ等を1画面でシミュレーション。実務学習付き',
      icon: <Hub />,
      path: getIndustryUnifiedUrl(),
      color: '#5794F2',
      span: 12,
      external: true,
    },
    {
      title: '企業横断オペレーション基盤',
      description: '観測・タスク・リスクの一元管理。要対応の横断把握・エクスポート',
      icon: <Hub />,
      path: getEOHUrl(),
      color: '#73BF69',
      span: 12,
      external: true,
    },
    {
      title: 'インフラ基盤',
      description: 'クラウドインフラ、インフラ構築専用。設計→構築→デプロイ→検証',
      icon: <Cloud />,
      path: '/cloud-infra',
      color: '#5794F2',
      span: 8,
    },
    {
      title: 'AI・ML',
      description: 'MLOps、生成AI、AI支援開発。MLパイプライン、RAG、CoT推論',
      icon: <Science />,
      path: '/mlops',
      color: '#B4B4B4',
      span: 8,
    },
    {
      title: 'インクルーシブ雇用AI',
      description: '障害者雇用マッチング、アクセシビリティ特化AI、当事者視点UX評価',
      icon: <Work />,
      path: '/inclusive-work',
      color: '#73BF69',
      span: 8,
    },
    {
      title: '開発・運用',
      description: 'IDOP。開発から運用までソフトウェア開発ライフサイクル全体',
      icon: <Build />,
      path: '/idop',
      color: '#73BF69',
      span: 8,
    },
    {
      title: 'プラットフォーム拡張',
      description: 'Level 2〜5。マルチテナント、エコシステム、グローバル展開',
      icon: <Public />,
      path: '/global-enterprise',
      color: '#F46800',
      span: 8,
    },
    {
      title: 'テスト',
      description: 'API・セキュリティ・契約・統合・E2E のテスト種別・内容・結果',
      icon: <BugReport />,
      path: '/tests',
      color: '#73BF69',
      span: 8,
    },
    {
      title: '製造・IoT',
      description: '予知保全・品質管理。インフラ・監視・MLOpsとの相性が良く、製造業DXの需要が高い',
      icon: <PrecisionManufacturing />,
      path: '/manufacturing',
      color: '#5794F2',
      span: 8,
    },
    {
      title: '金融・FinTech',
      description: '決済・リスク管理。高可用性・低レイテンシ・監視の経験をそのまま活かせる',
      icon: <AccountBalance />,
      path: '/fintech',
      color: '#F46800',
      span: 8,
    },
    {
      title: 'エネルギー',
      description: 'スマートグリッド・需給予測。時系列予測・リアルタイム制御・監視基盤の経験を活かせる',
      icon: <Bolt />,
      path: '/energy',
      color: '#73BF69',
      span: 8,
    },
    {
      title: '医療',
      description: 'AI診断、音声応答、異常検知、医療プラットフォーム。MLOpsとの相性が良い',
      icon: <LocalHospital />,
      path: '/medical',
      color: '#E02F44',
      span: 8,
    },
    {
      title: '宇宙・航空',
      description: '衛星軌道追跡、航空宇宙システム、時空操作',
      icon: <Satellite />,
      path: '/space',
      color: '#5794F2',
      span: 8,
    },
    {
      title: '交通',
      description: '交通管理、航空管制、スマートシティ持続可能性プラットフォーム',
      icon: <Traffic />,
      path: '/traffic',
      color: '#73BF69',
      span: 8,
    },
  ];

  return (
    <Box sx={{ p: 0 }}>
      {/* コンパクトなヘッダー */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          Dashboards
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {user?.full_name || user?.username} · 4分割統合プラットフォーム
        </Typography>
      </Box>

      {/* 要対応横断（5モジュール） */}
      <Box component="section" sx={{ mb: 3 }}>
        <Typography variant="overline" color="text.secondary" sx={{ display: 'block', mb: 1.5 }}>
          要対応横断（5モジュール）
        </Typography>
        <Paper sx={{ p: 2 }} elevation={0}>
          {actionItemsLoading ? (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <CircularProgress size={24} />
              <Typography variant="body2" color="text.secondary">読み込み中...</Typography>
            </Box>
          ) : actionItems && (actionItems.total ?? 0) > 0 ? (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
              <Typography variant="body2" color="text.secondary" sx={{ mr: 1 }}>合計:</Typography>
              <Chip label={`${actionItems.total} 件`} color="error" size="small" sx={{ fontWeight: 600 }} />
              {(actionItems.manufacturing ?? 0) > 0 && <Chip label={`製造 ${actionItems.manufacturing}`} size="small" color="warning" onClick={() => navigate('/manufacturing')} sx={{ cursor: 'pointer' }} />}
              {(actionItems.medical ?? 0) > 0 && <Chip label={`医療 ${actionItems.medical}`} size="small" color="warning" onClick={() => navigate('/medical')} sx={{ cursor: 'pointer' }} />}
              {(actionItems.fintech ?? 0) > 0 && <Chip label={`金融 ${actionItems.fintech}`} size="small" color="warning" onClick={() => navigate('/fintech')} sx={{ cursor: 'pointer' }} />}
              {(actionItems.contract ?? 0) > 0 && <Chip label={`契約 ${actionItems.contract}`} size="small" color="warning" onClick={() => navigate('/contract-workflow')} sx={{ cursor: 'pointer' }} />}
            </Box>
          ) : (
            <Typography variant="body2" color="text.secondary">要対応はありません</Typography>
          )}
        </Paper>
      </Box>

      {/* 大きなKPI（Statsパネル） */}
      <Box component="section" sx={{ mb: 3 }}>
        <Typography variant="overline" color="text.secondary" sx={{ display: 'block', mb: 1.5 }}>
          Stats Overview
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={6} sm={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }} elevation={0}>
              <Typography variant="h3" fontWeight={700} sx={{ color: '#73BF69' }}>
                99.995%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                稼働率
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }} elevation={0}>
              <Typography variant="h3" fontWeight={700} sx={{ color: '#5794F2' }}>
                5
              </Typography>
              <Typography variant="body2" color="text.secondary">
                プロジェクト
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }} elevation={0}>
              <Typography variant="h3" fontWeight={700} sx={{ color: '#F46800' }}>
                50+
              </Typography>
              <Typography variant="body2" color="text.secondary">
                API
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }} elevation={0}>
              <Typography variant="h3" fontWeight={700} sx={{ color: '#73BF69' }}>
                &lt;10ms
              </Typography>
              <Typography variant="body2" color="text.secondary">
                推論レイテンシ
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* 24カラムグリッド（Row 1） */}
      <Box component="section" sx={{ mb: 3 }}>
        <Typography variant="overline" color="text.secondary" sx={{ display: 'block', mb: 1.5 }}>
          Overview
        </Typography>
        <Grid container spacing={2}>
          {panels.map((panel) => (
            <DashboardPanel key={panel.title} {...panel} />
          ))}
        </Grid>
      </Box>

      {/* システム情報パネル */}
      <Paper sx={{ p: 2 }} elevation={0}>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          システム情報
        </Typography>
        <Typography variant="body2" color="text.secondary">
          バージョン 5.0.0 · 4分割構成 · {user?.username}
        </Typography>
      </Paper>
    </Box>
  );
};
