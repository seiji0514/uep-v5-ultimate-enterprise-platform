/**
 * インフラ構築専用システムページ
 *
 * インフラ構築に特化したワークフロー管理。
 * 設計 → 構築 → デプロイ → 検証の一連の流れを管理。
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Grid,
  Button,
} from '@mui/material';
import {
  Folder,
  Description,
  PlayArrow,
  CheckCircle,
} from '@mui/icons-material';
import {
  infraBuilderApi,
  BuildProject,
  Blueprint,
  PipelineRun,
  InfraBuilderDashboard,
} from '../../api/infraBuilder';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export const InfraBuilderPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [dashboard, setDashboard] = useState<InfraBuilderDashboard | null>(null);
  const [projects, setProjects] = useState<BuildProject[]>([]);
  const [blueprints, setBlueprints] = useState<Blueprint[]>([]);
  const [pipelines, setPipelines] = useState<PipelineRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [runningPipeline, setRunningPipeline] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [dashboardData, projectsData, blueprintsData, pipelinesData] = await Promise.all([
        infraBuilderApi.getDashboard(),
        infraBuilderApi.getProjects(),
        infraBuilderApi.getBlueprints(),
        infraBuilderApi.getPipelines(),
      ]);
      setDashboard(dashboardData);
      setProjects(projectsData);
      setBlueprints(blueprintsData);
      setPipelines(pipelinesData);
    } catch (err: unknown) {
      console.error('Infra Builder API Error:', err);
      const e = err as { code?: string; message?: string; response?: { status?: number; data?: { detail?: string } } };
      if (e.code === 'ECONNREFUSED' || e.message?.includes('Network Error')) {
        setError('バックエンドサーバーに接続できません。バックエンドが起動しているか確認してください。');
      } else if (e.response?.status === 404) {
        setError('APIエンドポイントが見つかりません。');
      } else if (e.response?.status === 403) {
        setError('アクセス権限がありません。');
      } else {
        setError(e.response?.data?.detail || e.message || 'データの取得に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRunPipeline = async (projectId: string) => {
    try {
      setRunningPipeline(projectId);
      await infraBuilderApi.runPipeline(projectId);
      await loadData();
    } catch (err) {
      console.error('Pipeline run error:', err);
      setError('パイプラインの実行に失敗しました');
    } finally {
      setRunningPipeline(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'in_progress':
      case 'running':
      case 'success':
      case 'completed':
        return 'success';
      case 'pending':
      case 'draft':
        return 'warning';
      case 'failed':
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStageLabel = (stage: string) => {
    const labels: Record<string, string> = {
      design: '設計',
      build: '構築',
      deploy: 'デプロイ',
      verify: '検証',
      completed: '完了',
    };
    return labels[stage] || stage;
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        インフラ構築専用システム
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        設計 → 構築 → デプロイ → 検証のワークフローでインフラ構築を管理。Docker、Kubernetes、Terraform に対応。
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          {/* ダッシュボードサマリー */}
          {dashboard && (
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      プロジェクト総数
                    </Typography>
                    <Typography variant="h4">{dashboard.total_projects}</Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      進行中
                    </Typography>
                    <Typography variant="h4" color="primary">
                      {dashboard.in_progress}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      ブループリント
                    </Typography>
                    <Typography variant="h4">{dashboard.total_blueprints}</Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      パイプライン実行
                    </Typography>
                    <Typography variant="h4">{dashboard.total_pipeline_runs}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          )}

          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
            <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
              <Tab icon={<Folder />} label="構築プロジェクト" />
              <Tab icon={<Description />} label="ブループリント" />
              <Tab icon={<PlayArrow />} label="パイプライン実行" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>名前</TableCell>
                    <TableCell>プロバイダー</TableCell>
                    <TableCell>ステージ</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>作成日時</TableCell>
                    <TableCell>操作</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {projects.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        プロジェクトがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    projects.map((project) => (
                      <TableRow key={project.id}>
                        <TableCell>
                          <Typography fontWeight="medium">{project.name}</Typography>
                          {project.description && (
                            <Typography variant="caption" color="text.secondary" display="block">
                              {project.description}
                            </Typography>
                          )}
                        </TableCell>
                        <TableCell>{project.target_provider}</TableCell>
                        <TableCell>{getStageLabel(project.current_stage)}</TableCell>
                        <TableCell>
                          <Chip
                            label={project.status}
                            color={getStatusColor(project.status) as 'success' | 'warning' | 'error' | 'default'}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(project.created_at).toLocaleString('ja-JP')}
                        </TableCell>
                        <TableCell>
                          <Button
                            size="small"
                            variant="outlined"
                            startIcon={<PlayArrow />}
                            onClick={() => handleRunPipeline(project.id)}
                            disabled={runningPipeline === project.id}
                          >
                            実行
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>名前</TableCell>
                    <TableCell>プロバイダー</TableCell>
                    <TableCell>説明</TableCell>
                    <TableCell>作成日時</TableCell>
                    <TableCell>作成者</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {blueprints.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        ブループリントがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    blueprints.map((bp) => (
                      <TableRow key={bp.id}>
                        <TableCell>{bp.name}</TableCell>
                        <TableCell>{bp.provider}</TableCell>
                        <TableCell>{bp.description || '-'}</TableCell>
                        <TableCell>
                          {new Date(bp.created_at).toLocaleString('ja-JP')}
                        </TableCell>
                        <TableCell>{bp.created_by}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>ID</TableCell>
                    <TableCell>プロジェクトID</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>ステージ</TableCell>
                    <TableCell>開始日時</TableCell>
                    <TableCell>ログ</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {pipelines.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        パイプライン実行履歴がありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    pipelines.map((pipe) => (
                      <TableRow key={pipe.id}>
                        <TableCell>{pipe.id}</TableCell>
                        <TableCell>{pipe.project_id}</TableCell>
                        <TableCell>
                          <Chip
                            label={pipe.status}
                            color={getStatusColor(pipe.status) as 'success' | 'warning' | 'error' | 'default'}
                            size="small"
                            icon={pipe.status === 'success' ? <CheckCircle /> : undefined}
                          />
                        </TableCell>
                        <TableCell>{pipe.current_stage || '-'}</TableCell>
                        <TableCell>
                          {new Date(pipe.started_at).toLocaleString('ja-JP')}
                        </TableCell>
                        <TableCell>
                          {pipe.logs && pipe.logs.length > 0 ? (
                            <Box component="pre" sx={{ fontSize: '0.75rem', maxHeight: 80, overflow: 'auto' }}>
                              {pipe.logs.join('\n')}
                            </Box>
                          ) : (
                            '-'
                          )}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>
        </>
      )}
    </Box>
  );
};
