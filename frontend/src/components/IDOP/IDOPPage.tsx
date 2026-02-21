/**
 * IDOPページ
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
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
  Build,
  Apps,
} from '@mui/icons-material';
import { idopApi, CICDPipeline, Application } from '../../api/idop';

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

export const IDOPPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [pipelines, setPipelines] = useState<CICDPipeline[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) {
        const data = await idopApi.getPipelines();
        setPipelines(data);
      } else if (tabValue === 1) {
        const data = await idopApi.getApplications();
        setApplications(data);
      }
    } catch (err: any) {
      console.error('IDOP API Error:', err);
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
      case 'deployed':
        return 'success';
      case 'pending':
      case 'building':
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
        IDOP
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        開発から運用まで、ソフトウェア開発ライフサイクル全体をカバー
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab icon={<Build />} label="CI/CDパイプライン" />
          <Tab icon={<Apps />} label="アプリケーション" />
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
                        CI/CDパイプラインがありません
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
                    <TableCell>説明</TableCell>
                    <TableCell>環境</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>作成日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {applications.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        アプリケーションがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    applications.map((app) => (
                      <TableRow key={app.id}>
                        <TableCell>{app.name}</TableCell>
                        <TableCell>{app.description || '-'}</TableCell>
                        <TableCell>{app.environment}</TableCell>
                        <TableCell>
                          <Chip
                            label={app.status}
                            color={getStatusColor(app.status) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(app.created_at).toLocaleString('ja-JP')}
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
