/**
 * ダッシュボードページ
 */
import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
} from '@mui/material';
import {
  Science,
  Psychology,
  Security,
  Cloud,
  Build,
  Layers,
  Groups,
  Star,
  Public,
  Dashboard as DashboardIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

interface DashboardCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  path: string;
  color: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({ title, description, icon, path, color }) => {
  const navigate = useNavigate();

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ color, mr: 2 }}>{icon}</Box>
          <Typography variant="h5" component="h2">
            {title}
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" onClick={() => navigate(path)}>
          詳細を見る
        </Button>
      </CardActions>
    </Card>
  );
};

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();

  const dashboardCards = [
    {
      title: 'MLOps',
      description: 'MLパイプラインの設計と実装、モデル管理、実験追跡',
      icon: <Science fontSize="large" />,
      path: '/mlops',
      color: '#1976d2',
    },
    {
      title: '生成AI',
      description: 'LLM統合、RAG、CoT推論、生成AIアプリケーション開発',
      icon: <Psychology fontSize="large" />,
      path: '/generative-ai',
      color: '#9c27b0',
    },
    {
      title: 'セキュリティコマンドセンター',
      description: 'セキュリティ監視、インシデント対応、リスク分析',
      icon: <Security fontSize="large" />,
      path: '/security-center',
      color: '#d32f2f',
    },
    {
      title: 'クラウドインフラ',
      description: 'クラウド設計・運用、IaC運用、コンテナ化・オーケストレーション',
      icon: <Cloud fontSize="large" />,
      path: '/cloud-infra',
      color: '#0288d1',
    },
    {
      title: 'IDOP',
      description: '開発から運用まで、ソフトウェア開発ライフサイクル全体をカバー',
      icon: <Build fontSize="large" />,
      path: '/idop',
      color: '#f57c00',
    },
    {
      title: 'AI支援開発',
      description: 'コード生成支援、テスト自動化、コードレビュー支援',
      icon: <Build fontSize="large" />,
      path: '/ai-dev',
      color: '#388e3c',
    },
    {
      title: 'プラットフォーム (Level 2)',
      description: 'マルチテナント、SaaS化、APIマーケットプレイス',
      icon: <Layers fontSize="large" />,
      path: '/platform',
      color: '#00838f',
    },
    {
      title: 'エコシステム (Level 3)',
      description: 'パートナー統合、モデル共有、コミュニティフォーラム、業界標準',
      icon: <Groups fontSize="large" />,
      path: '/ecosystem',
      color: '#7b1fa2',
    },
    {
      title: 'インダストリー (Level 4)',
      description: 'グローバルCDN、多言語対応、最先端AI、業界標準の確立',
      icon: <Star fontSize="large" />,
      path: '/industry-leader',
      color: '#e65100',
    },
    {
      title: 'グローバル (Level 5)',
      description: 'マルチリージョン、高可用性99.99%、ゼロダウンタイム、コンプライアンス、DR',
      icon: <Public fontSize="large" />,
      path: '/global-enterprise',
      color: '#1565c0',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        ダッシュボード
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        ようこそ、{user?.full_name || user?.username}さん
      </Typography>
      <Typography variant="body2" color="primary.main" sx={{ mb: 2 }}>
        ⭐ 実用的最高難易度 - 本番環境対応・Level 1〜5 統合
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {dashboardCards.map((card) => (
          <Grid item xs={12} sm={6} md={4} key={card.title}>
            <DashboardCard {...card} />
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ p: 3, mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          システム情報
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>バージョン:</strong> 5.0.0
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>環境:</strong> 開発環境
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>ユーザー:</strong> {user?.username} ({user?.roles.join(', ')})
        </Typography>
      </Paper>
    </Box>
  );
};
