/**
 * テストページ
 * テスト種別・内容・結果をカテゴリー別に表示（企業向けデモ）
 */
import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
} from '@mui/material';
import {
  ExpandMore,
  CheckCircle,
  Error as ErrorIcon,
  Science,
  Security,
  Description,
  IntegrationInstructions,
  Storage,
  Speed,
  Cached,
  PlayArrow,
} from '@mui/icons-material';

interface TestItem {
  file: string;
  content: string;
  status?: 'passed' | 'failed' | 'skipped' | 'pending';
  lastRun?: string;
}

interface TestCategory {
  id: string;
  title: string;
  icon: React.ReactNode;
  color: string;
  items: TestItem[];
}

const testCategories: TestCategory[] = [
  {
    id: 'api',
    title: 'API',
    icon: <Science />,
    color: '#F46800',
    items: [
      { file: 'test_api_endpoints.py', content: 'ヘルスチェック、メトリクス、OpenAPI、404、エラー形式', status: 'passed', lastRun: '2026-02' },
    ],
  },
  {
    id: 'security',
    title: 'セキュリティ',
    icon: <Security />,
    color: '#5794F2',
    items: [
      { file: 'test_security.py', content: 'セキュリティヘッダー、CORS', status: 'passed', lastRun: '2026-02' },
    ],
  },
  {
    id: 'contract',
    title: '契約',
    icon: <Description />,
    color: '#73BF69',
    items: [
      { file: 'contract/test_contract_auth.py', content: 'ログインAPI、/me、認証エラー、ヘルスチェック', status: 'passed', lastRun: '2026-02' },
      { file: 'contract/test_contract_mlops.py', content: 'MLOps パイプラインAPI', status: 'passed', lastRun: '2026-02' },
      { file: 'contract/test_contract_chaos.py', content: 'Chaos エンドポイント', status: 'passed', lastRun: '2026-02' },
    ],
  },
  {
    id: 'integration',
    title: '統合',
    icon: <IntegrationInstructions />,
    color: '#B877D9',
    items: [
      { file: 'test_integration.py', content: 'MLOps、認証フロー', status: 'passed', lastRun: '2026-02' },
    ],
  },
  {
    id: 'db',
    title: 'DB',
    icon: <Storage />,
    color: '#FF9830',
    items: [
      { file: 'test_database.py', content: 'データベース接続', status: 'passed', lastRun: '2026-02' },
    ],
  },
  {
    id: 'rate-limit',
    title: 'レート制限',
    icon: <Speed />,
    color: '#F2CC0C',
    items: [
      { file: 'test_rate_limit.py', content: 'レート制限', status: 'passed', lastRun: '2026-02' },
    ],
  },
  {
    id: 'cache',
    title: 'キャッシュ',
    icon: <Cached />,
    color: '#73BF69',
    items: [
      { file: 'test_cache.py', content: 'キャッシュ', status: 'passed', lastRun: '2026-02' },
    ],
  },
];

const e2eTests = [
  { file: 'login.spec.ts', content: 'ログイン画面の E2E' },
  { file: 'chaos.spec.ts', content: 'Chaos Engineering ページの E2E' },
];

const StatusChip: React.FC<{ status?: TestItem['status'] }> = ({ status }) => {
  if (!status || status === 'pending') {
    return <Chip size="small" label="未実行" color="default" variant="outlined" />;
  }
  if (status === 'passed') {
    return <Chip size="small" icon={<CheckCircle />} label="PASSED" color="success" />;
  }
  if (status === 'failed') {
    return <Chip size="small" icon={<ErrorIcon />} label="FAILED" color="error" />;
  }
  return <Chip size="small" label="SKIPPED" color="warning" variant="outlined" />;
};

export const TestsPage: React.FC = () => {
  const [expanded, setExpanded] = useState<string | false>('api');

  const handleAccordionChange = (panel: string) => (_: React.SyntheticEvent, isExpanded: boolean) => {
    setExpanded(isExpanded ? panel : false);
  };

  return (
    <Box>
      <Typography variant="h5" fontWeight={600} sx={{ mb: 2, color: 'text.primary' }}>
        テスト概要
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        企業向け品質保証の観点で、バックエンド・E2E のテスト種別・内容・結果をカテゴリー別に表示します。
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>実行方法:</strong> <code>cd backend &amp;&amp; python -m pytest tests/ -v --no-cov</code>
        </Typography>
      </Alert>

      <Grid container spacing={2}>
        {testCategories.map((cat) => (
          <Grid item xs={12} key={cat.id}>
            <Accordion
              expanded={expanded === cat.id}
              onChange={handleAccordionChange(cat.id)}
              sx={{
                bgcolor: 'background.paper',
                border: '1px solid',
                borderColor: 'divider',
                '&:before': { display: 'none' },
              }}
            >
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                  <Box sx={{ color: cat.color }}>{cat.icon}</Box>
                  <Typography fontWeight={600}>{cat.title}</Typography>
                  <Chip
                    size="small"
                    label={`${cat.items.length} 件`}
                    variant="outlined"
                    sx={{ ml: 1 }}
                  />
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <TableContainer component={Paper} variant="outlined" sx={{ bgcolor: 'transparent' }}>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>ファイル</TableCell>
                        <TableCell>内容</TableCell>
                        <TableCell align="center">結果</TableCell>
                        <TableCell>最終実行</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {cat.items.map((item, idx) => (
                        <TableRow key={idx}>
                          <TableCell sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
                            {item.file}
                          </TableCell>
                          <TableCell sx={{ color: 'text.secondary', fontSize: '0.9rem' }}>
                            {item.content}
                          </TableCell>
                          <TableCell align="center">
                            <StatusChip status={item.status} />
                          </TableCell>
                          <TableCell sx={{ color: 'text.secondary', fontSize: '0.85rem' }}>
                            {item.lastRun || '-'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </AccordionDetails>
            </Accordion>
          </Grid>
        ))}
      </Grid>

      <Typography variant="h6" fontWeight={600} sx={{ mt: 4, mb: 2, color: 'text.primary' }}>
        E2E（Playwright）
      </Typography>
      <Paper sx={{ p: 2, border: '1px solid', borderColor: 'divider' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ファイル</TableCell>
              <TableCell>内容</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {e2eTests.map((item, idx) => (
              <TableRow key={idx}>
                <TableCell sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>{item.file}</TableCell>
                <TableCell sx={{ color: 'text.secondary' }}>{item.content}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
          実行: <code>cd e2e &amp;&amp; npx playwright test</code>
        </Typography>
      </Paper>

      <Box sx={{ mt: 3, display: 'flex', alignItems: 'center', gap: 1, color: 'text.secondary' }}>
        <PlayArrow fontSize="small" />
        <Typography variant="body2">
          面談での説明: 契約テストでAPI入出力形式を自動検証、セキュリティテストでヘッダー・CORSを検証、CI/CDでプッシュ時に自動実行
        </Typography>
      </Box>
    </Box>
  );
};
