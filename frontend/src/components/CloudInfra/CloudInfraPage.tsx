/**
 * クラウドインフラページ
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
  Cloud,
  Storage,
  SettingsApplications,
} from '@mui/icons-material';
import { cloudInfraApi, InfrastructureResource, IaCTemplate, Deployment } from '../../api/cloudInfra';

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

export const CloudInfraPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [resources, setResources] = useState<InfrastructureResource[]>([]);
  const [templates, setTemplates] = useState<IaCTemplate[]>([]);
  const [deployments, setDeployments] = useState<Deployment[]>([]);
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
        const data = await cloudInfraApi.getResources();
        setResources(data);
      } else if (tabValue === 1) {
        const data = await cloudInfraApi.getTemplates();
        setTemplates(data);
      } else if (tabValue === 2) {
        const data = await cloudInfraApi.getDeployments();
        setDeployments(data);
      }
    } catch (err: any) {
      console.error('Cloud Infra API Error:', err);
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
      case 'active':
      case 'running':
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
        クラウドインフラ
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        クラウド設計・運用、IaC運用、コンテナ化・オーケストレーション
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab icon={<Cloud />} label="リソース" />
          <Tab icon={<Storage />} label="IaCテンプレート" />
          <Tab icon={<SettingsApplications />} label="デプロイメント" />
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
                    <TableCell>リソースタイプ</TableCell>
                    <TableCell>プロバイダー</TableCell>
                    <TableCell>リージョン</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>作成日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {resources.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        リソースがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    resources.map((resource) => (
                      <TableRow key={resource.id}>
                        <TableCell>{resource.name}</TableCell>
                        <TableCell>{resource.resource_type}</TableCell>
                        <TableCell>{resource.provider}</TableCell>
                        <TableCell>{resource.region}</TableCell>
                        <TableCell>
                          <Chip
                            label={resource.status}
                            color={getStatusColor(resource.status) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(resource.created_at).toLocaleString('ja-JP')}
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
                    <TableCell>作成日時</TableCell>
                    <TableCell>作成者</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {templates.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4} align="center">
                        IaCテンプレートがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    templates.map((template) => (
                      <TableRow key={template.id}>
                        <TableCell>{template.name}</TableCell>
                        <TableCell>{template.provider}</TableCell>
                        <TableCell>
                          {new Date(template.created_at).toLocaleString('ja-JP')}
                        </TableCell>
                        <TableCell>{template.created_by}</TableCell>
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
                    <TableCell>プラットフォーム</TableCell>
                    <TableCell>レプリカ数</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>作成日時</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {deployments.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        デプロイメントがありません
                      </TableCell>
                    </TableRow>
                  ) : (
                    deployments.map((deployment) => (
                      <TableRow key={deployment.id}>
                        <TableCell>{deployment.name}</TableCell>
                        <TableCell>{deployment.platform}</TableCell>
                        <TableCell>{deployment.replicas}</TableCell>
                        <TableCell>
                          <Chip
                            label={deployment.status}
                            color={getStatusColor(deployment.status) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {new Date(deployment.created_at).toLocaleString('ja-JP')}
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
