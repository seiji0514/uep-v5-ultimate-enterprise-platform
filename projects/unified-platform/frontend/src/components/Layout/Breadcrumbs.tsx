import { Breadcrumbs as MuiBreadcrumbs, Link, Typography } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';

const pathLabels: Record<string, string> = {
  '': 'ダッシュボード',
  medical: '医療',
  aviation: '航空',
  space: '宇宙',
  erp: 'ERP（統合基幹）',
  'legacy-migration': 'レガシー刷新',
  'data-integration': 'データ連携基盤',
  dx: 'DX推進基盤',
  settings: '設定',
};

export function Breadcrumbs() {
  const location = useLocation();
  const navigate = useNavigate();
  const segments = location.pathname.split('/').filter(Boolean);

  return (
    <MuiBreadcrumbs sx={{ mb: 1 }} aria-label="パンくず">
      <Link component="button" underline="hover" color="inherit" onClick={() => navigate('/')} sx={{ cursor: 'pointer' }}>
        ホーム
      </Link>
      {segments.map((seg, i) => {
        const path = '/' + segments.slice(0, i + 1).join('/');
        const label = pathLabels[seg] || seg;
        const isLast = i === segments.length - 1;
        return isLast ? (
          <Typography key={path} color="text.primary">{label}</Typography>
        ) : (
          <Link key={path} component="button" underline="hover" color="inherit" onClick={() => navigate(path)} sx={{ cursor: 'pointer' }}>
            {label}
          </Link>
        );
      })}
      {segments.length === 0 && <Typography color="text.primary">ダッシュボード</Typography>}
    </MuiBreadcrumbs>
  );
}
