/**
 * MLOpsページ
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
} from '@mui/material';
import {
  Science,
  ModelTraining,
  Timeline,
} from '@mui/icons-material';
import { mlopsApi, MLPipeline, MLModel, Experiment } from '../../api/mlops';

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

export const MLOpsPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [pipelines, setPipelines] = useState<MLPipeline[]>([]);
  const [models, setModels] = useState<MLModel[]>([]);
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) {
        const data = await mlopsApi.getPipelines();
        setPipelines(data);
      } else if (tabValue === 1) {
        const data = await mlopsApi.getModels();
        setModels(data);
      } else if (tabValue === 2) {
        const data = await mlopsApi.getExperiments();
        setExperiments(data);
      }
    } catch (err: any) {
      console.error('MLOps API Error:', err);
      if (err.code === 'ECONNREFUSED' || err.message?.includes('Network Error')) {
        setError('バックエンドサーバーに接続できません。バックエンドが起動しているか確認してください。');
      } else if (err.response?.status === 404) {
        setError('APIエンドポイントが見つかりません。');
      } else if (err.response?.status === 403) {
        setError('アクセス権限がありません。');
      } else if (err.response?.status === 422) {
        // バリデーションエラーの詳細を表示
        const errorData = err.response?.data;
        if (errorData?.error?.errors && Array.isArray(errorData.error.errors)) {
          const validationErrors = errorData.error.errors
            .map((e: any) => `${e.field}: ${e.message}`)
            .join(', ');
          setError(`バリデーションエラー: ${validationErrors}`);
        } else {
          setError(errorData?.error?.message || errorData?.detail || 'バリデーションエラーが発生しました');
        }
      } else if (err.response?.status === 500) {
        setError('サーバーエラーが発生しました。');
      } else {
        setError(err.response?.data?.error?.message || err.response?.data?.detail || err.message || 'データの取得に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'running':
      case 'active':
        return 'success';
      case 'pending':
        return 'warning';
      case 'failed':
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        MLOps
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        MLパイプラインの設計と実装、モデル管理、実験追跡
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab icon={<Timeline />} label="パイプライン" />
          <Tab icon={<ModelTraining />} label="モデル" />
          <Tab icon={<Science />} label="実験" />
        </Tabs>
      </Box>

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
          <TabPanel value={tabValue} index={0}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>名前</TableCell>
                    <TableCell>説明</TableCell>
                    <TableCell>ステージ数</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>作成日時</TableCell>
                    <TableCell>作成者</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {pipelines.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        パイプラインがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    pipelines.map((pipeline) => (
                      <TableRow key={pipeline.id}>
                        <TableCell>{pipeline.name}</TableCell>
                        <TableCell>{pipeline.description || '-'}</TableCell>
                        <TableCell>{pipeline.stages.length}</TableCell>
                        <TableCell>
                          <Chip
                            label={pipeline.status}
                            color={getStatusColor(pipeline.status) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(pipeline.created_at).toLocaleString('ja-JP')}
                        </TableCell>
                        <TableCell>{pipeline.created_by}</TableCell>
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
                    <TableCell>バージョン</TableCell>
                    <TableCell>フレームワーク</TableCell>
                    <TableCell>精度</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>作成日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {models.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        モデルがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    models.map((model) => (
                      <TableRow key={model.id}>
                        <TableCell>{model.name}</TableCell>
                        <TableCell>{model.version}</TableCell>
                        <TableCell>{model.framework}</TableCell>
                        <TableCell>
                          {model.accuracy !== undefined
                            ? `${(model.accuracy * 100).toFixed(2)}%`
                            : '-'}
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={model.status}
                            color={getStatusColor(model.status) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(model.created_at).toLocaleString('ja-JP')}
                        </TableCell>
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
                    <TableCell>名前</TableCell>
                    <TableCell>説明</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>メトリクス</TableCell>
                    <TableCell>作成日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {experiments.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        実験がありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    experiments.map((experiment) => (
                      <TableRow key={experiment.id}>
                        <TableCell>{experiment.name}</TableCell>
                        <TableCell>{experiment.description || '-'}</TableCell>
                        <TableCell>
                          <Chip
                            label={experiment.status}
                            color={getStatusColor(experiment.status) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {experiment.metrics
                            ? Object.entries(experiment.metrics)
                                .map(([k, v]) => `${k}: ${v}`)
                                .join(', ')
                            : '-'}
                        </TableCell>
                        <TableCell>
                          {new Date(experiment.created_at).toLocaleString('ja-JP')}
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
