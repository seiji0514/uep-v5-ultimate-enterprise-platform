/**
 * プロジェクト一覧ページ
 * 統合ダッシュボード・パネル構成（左寄せタイトル、グリッド、統計表示）
 */
import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  IconButton,
  LinearProgress,
} from '@mui/material';
import {
  Cloud,
  Science,
  Public,
  ArrowForward,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface Project {
  id: string;
  name: string;
  description: string;
  category: string;
  categoryPath: string;
  status: string;
  progress: number;
  teamRole?: string;
  icon: React.ReactNode;
}

const projects: Project[] = [
  {
    id: 'uep-demo-unified',
    name: 'UEP推論最適化基盤',
    description: 'MLOps推論モデル→クラウドインフラ→Level 5東京リージョンまで一元化。レイテンシ50%削減、稼働率99.995%達成',
    category: 'インフラ基盤 × AI・ML',
    categoryPath: '/mlops',
    status: '進行中',
    progress: 85,
    teamRole: 'インフラ構築・監視基盤担当',
    icon: <Cloud />,
  },
  {
    id: 'web-app-base',
    name: 'Webアプリ基盤構築',
    description: 'Nginx + Redis のコンテナ基盤。Docker構築、設計→構築→デプロイ→検証のワークフロー',
    category: 'インフラ基盤',
    categoryPath: '/infra-builder',
    status: '構築中',
    progress: 70,
    teamRole: 'インフラエンジニア',
    icon: <Cloud />,
  },
  {
    id: 'k8s-cluster',
    name: 'Kubernetes クラスタ構築',
    description: 'K8sマニフェストによるデプロイ。Level 5 マルチリージョン展開を想定',
    category: 'インフラ基盤 × プラットフォーム拡張',
    categoryPath: '/infra-builder',
    status: '設計中',
    progress: 30,
    teamRole: '設計・構築担当',
    icon: <Public />,
  },
  {
    id: 'inference-optimization',
    name: '推論レイテンシ最適化',
    description: 'MLOps実験・モデルv1.2登録。A/Bテスト、レイテンシ8.5ms、スループット5倍向上',
    category: 'AI・ML',
    categoryPath: '/mlops',
    status: '完了',
    progress: 100,
    teamRole: 'MLOpsエンジニア',
    icon: <Science />,
  },
];

const statusColor = (status: string) => {
  if (status === '完了') return '#73BF69';
  if (status === '進行中' || status === '構築中') return '#5794F2';
  return '#B4B4B4';
};

export const ProjectsPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      {/* コンパクトヘッダー */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>
          Projects
        </Typography>
        <Typography variant="body2" color="text.secondary">
          4分割カテゴリを横断。チーム開発・役割分担を想定
        </Typography>
      </Box>

      {/* 大きなKPI（Stats） */}
      <Box component="section" sx={{ mb: 3 }}>
        <Typography variant="overline" color="text.secondary" sx={{ display: 'block', mb: 1.5 }}>
          Stats
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={4} sm={2}>
            <Paper sx={{ p: 1.5, textAlign: 'center' }} elevation={0}>
              <Typography variant="h4" fontWeight={700} sx={{ color: '#5794F2' }}>5</Typography>
              <Typography variant="caption" color="text.secondary">プロジェクト</Typography>
            </Paper>
          </Grid>
          <Grid item xs={4} sm={2}>
            <Paper sx={{ p: 1.5, textAlign: 'center' }} elevation={0}>
              <Typography variant="h4" fontWeight={700} sx={{ color: '#73BF69' }}>1</Typography>
              <Typography variant="caption" color="text.secondary">完了</Typography>
            </Paper>
          </Grid>
          <Grid item xs={4} sm={2}>
            <Paper sx={{ p: 1.5, textAlign: 'center' }} elevation={0}>
              <Typography variant="h4" fontWeight={700} sx={{ color: '#F46800' }}>3</Typography>
              <Typography variant="caption" color="text.secondary">進行中</Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* パネルグリッド */}
      <Box component="section" sx={{ mb: 3 }}>
        <Typography variant="overline" color="text.secondary" sx={{ display: 'block', mb: 1.5 }}>
          プロジェクト一覧
        </Typography>
        <Grid container spacing={2}>
          {projects.map((project) => (
            <Grid item xs={12} md={6} key={project.id}>
              <Paper
                sx={{
                  p: 2,
                  height: '100%',
                  cursor: 'pointer',
                  transition: 'border-color 0.2s',
                  '&:hover': {
                    borderColor: '#F46800',
                    '& .panel-action': { opacity: 1 },
                  },
                }}
                onClick={() => navigate(project.categoryPath)}
                elevation={0}
              >
                {/* 左寄せパネルヘッダー */}
                <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 1.5 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                    <Box sx={{ color: 'primary.main' }}>{project.icon}</Box>
                    <Typography variant="subtitle1" fontWeight={600}>
                      {project.name}
                    </Typography>
                    <Box
                      component="span"
                      sx={{
                        px: 1,
                        py: 0.25,
                        borderRadius: 1,
                        fontSize: '0.75rem',
                        bgcolor: `${statusColor(project.status)}20`,
                        color: statusColor(project.status),
                      }}
                    >
                      {project.status}
                    </Box>
                  </Box>
                  <IconButton size="small" className="panel-action" sx={{ opacity: 0.6 }} aria-label={`${project.name}を開く`}>
                    <ArrowForward fontSize="small" />
                  </IconButton>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5, lineHeight: 1.5 }}>
                  {project.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 1.5 }}>
                  <Box
                    component="span"
                    sx={{
                      px: 1,
                      py: 0.25,
                      borderRadius: 1,
                      fontSize: '0.7rem',
                      border: '1px solid',
                      borderColor: 'divider',
                    }}
                  >
                    {project.category}
                  </Box>
                  {project.teamRole && (
                    <Box
                      component="span"
                      sx={{
                        px: 1,
                        py: 0.25,
                        borderRadius: 1,
                        fontSize: '0.7rem',
                        border: '1px solid',
                        borderColor: 'primary.main',
                        color: 'primary.main',
                      }}
                    >
                      {project.teamRole}
                    </Box>
                  )}
                </Box>
                {/* 進捗バー */}
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    {project.progress}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={project.progress}
                    sx={{
                      mt: 0.5,
                      height: 4,
                      borderRadius: 1,
                      bgcolor: 'rgba(255,255,255,0.1)',
                      '& .MuiLinearProgress-bar': {
                        bgcolor: project.progress === 100 ? '#73BF69' : '#F46800',
                      },
                    }}
                  />
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* 表形式（データテーブル） */}
      <Paper sx={{ p: 2 }} elevation={0}>
        <Typography variant="overline" color="text.secondary" sx={{ display: 'block', mb: 1.5 }}>
          一覧
        </Typography>
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: '1fr 1.5fr 1fr 0.8fr 0.6fr',
            gap: 1,
            fontSize: '0.8rem',
          }}
        >
          <Box sx={{ fontWeight: 600, color: 'text.secondary' }}>プロジェクト</Box>
          <Box sx={{ fontWeight: 600, color: 'text.secondary' }}>カテゴリ</Box>
          <Box sx={{ fontWeight: 600, color: 'text.secondary' }}>役割</Box>
          <Box sx={{ fontWeight: 600, color: 'text.secondary' }}>ステータス</Box>
          <Box sx={{ fontWeight: 600, color: 'text.secondary' }}>進捗</Box>
          {projects.map((project) => (
            <React.Fragment key={project.id}>
              <Box>{project.name}</Box>
              <Box color="text.secondary">{project.category}</Box>
              <Box color="text.secondary">{project.teamRole || '-'}</Box>
              <Box sx={{ color: statusColor(project.status) }}>{project.status}</Box>
              <Box color="text.secondary">{project.progress}%</Box>
            </React.Fragment>
          ))}
        </Box>
      </Paper>
    </Box>
  );
};
