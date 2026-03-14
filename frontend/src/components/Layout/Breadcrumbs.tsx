/**
 * パンくずリストコンポーネント
 * 現在位置を表示（アクセシビリティ対応）
 */
import React from 'react';
import { Breadcrumbs as MuiBreadcrumbs, Link, Typography } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';

const pathLabels: Record<string, string> = {
  '/': 'ダッシュボード',
  '/projects': 'プロジェクト一覧',
  '/mlops': 'MLOps',
  '/generative-ai': '生成AI',
  '/optimization': '最適化・精度向上',
  '/personal-accounting': '個人会計',
  '/cloud-infra': 'クラウドインフラ',
  '/infra-builder': 'インフラ構築',
  '/idop': 'IDOP',
  '/ai-dev': 'AI支援開発',
  '/platform': 'プラットフォーム',
  '/ecosystem': 'エコシステム',
  '/industry-leader': 'インダストリー',
  '/global-enterprise': 'グローバル',
  '/unified-business': '統合ビジネス',
  '/erp': 'ERP（統合基幹）',
  '/chaos': 'Chaos Engineering',
  '/inclusive-work': 'インクルーシブ雇用AI',
  '/graphql': 'GraphQL',
  '/wasm': 'WebAssembly',
  '/settings': '設定',
  '/tests': 'テスト',
  '/manufacturing': '製造・MLOps',
  '/fintech': '金融・FinTech',
  '/contract-workflow': '契約ワークフロー',
  '/integrated-modules': '5モジュール概要',
  '/integrated-modules/detail': '詳細説明',
  '/energy': 'エネルギー',
  '/medical': '医療',
  '/space': '宇宙・航空',
  '/traffic': '交通',
};

export const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const pathnames = location.pathname.split('/').filter((x) => x);

  const breadcrumbs = [
    { path: '/', label: pathLabels['/'] || 'ダッシュボード' },
    ...pathnames.map((_, i) => {
      const path = '/' + pathnames.slice(0, i + 1).join('/');
      return { path, label: pathLabels[path] || pathnames[i] };
    }),
  ];

  return (
    <MuiBreadcrumbs
      aria-label="パンくずリスト"
      sx={{ mb: 1, '& .MuiBreadcrumbs-separator': { mx: 0.5 } }}
    >
      {breadcrumbs.map((crumb, i) =>
        i === breadcrumbs.length - 1 ? (
          <Typography key={crumb.path} variant="body2" color="text.primary" fontWeight={500}>
            {crumb.label}
          </Typography>
        ) : (
          <Link
            key={crumb.path}
            component="button"
            variant="body2"
            color="text.secondary"
            underline="hover"
            onClick={() => navigate(crumb.path)}
            sx={{ cursor: 'pointer', bg: 'transparent', border: 'none', p: 0, font: 'inherit' }}
          >
            {crumb.label}
          </Link>
        )
      )}
    </MuiBreadcrumbs>
  );
};
