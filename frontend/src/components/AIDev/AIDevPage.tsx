/**
 * AI支援開発ページ
 */
import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Paper,
  Tabs,
  Tab,
  Alert,
  CircularProgress,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import {
  Code,
  BugReport,
  Description,
} from '@mui/icons-material';
import { aiDevApi, CodeGenerateRequest, CodeReviewRequest, DocumentationRequest } from '../../api/aiDev';

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

export const AIDevPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [description, setDescription] = useState('');
  const [code, setCode] = useState('');
  const [docContent, setDocContent] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [checkStyle, setCheckStyle] = useState(true);
  const [checkSecurity, setCheckSecurity] = useState(true);
  const [checkPerformance, setCheckPerformance] = useState(false);

  const handleGenerateCode = async () => {
    if (!description.trim()) return;
    try {
      setLoading(true);
      setError('');
      const request: CodeGenerateRequest = {
        description,
        language: 'python',
      };
      const response = await aiDevApi.generateCode(request);
      setResult(response.code || JSON.stringify(response, null, 2));
    } catch (err: any) {
      console.error('Code Generation API Error:', err);
      if (err.response?.status === 422) {
        const errorData = err.response?.data;
        if (errorData?.error?.errors && Array.isArray(errorData.error.errors)) {
          const validationErrors = errorData.error.errors
            .map((e: any) => `${e.field}: ${e.message}`)
            .join(', ');
          setError(`バリデーションエラー: ${validationErrors}`);
        } else {
          setError(errorData?.error?.message || errorData?.detail || 'バリデーションエラーが発生しました');
        }
      } else {
        setError(err.response?.data?.error?.message || err.response?.data?.detail || 'コード生成に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReviewCode = async () => {
    if (!code.trim()) return;
    try {
      setLoading(true);
      setError('');
      const request: CodeReviewRequest = {
        code,
        language: 'python',
        check_style: checkStyle,
        check_security: checkSecurity,
        check_performance: checkPerformance,
      };
      const response = await aiDevApi.reviewCode(request);
      setResult(JSON.stringify(response, null, 2));
    } catch (err: any) {
      console.error('Code Review API Error:', err);
      if (err.response?.status === 422) {
        const errorData = err.response?.data;
        if (errorData?.error?.errors && Array.isArray(errorData.error.errors)) {
          const validationErrors = errorData.error.errors
            .map((e: any) => `${e.field}: ${e.message}`)
            .join(', ');
          setError(`バリデーションエラー: ${validationErrors}`);
        } else {
          setError(errorData?.error?.message || errorData?.detail || 'バリデーションエラーが発生しました');
        }
      } else {
        setError(err.response?.data?.error?.message || err.response?.data?.detail || 'コードレビューに失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateDoc = async () => {
    if (!docContent.trim()) return;
    try {
      setLoading(true);
      setError('');
      const request: DocumentationRequest = {
        doc_type: 'readme',
        content: docContent,
        language: 'python',
      };
      const response = await aiDevApi.generateDocumentation(request);
      setResult(response.documentation || JSON.stringify(response, null, 2));
    } catch (err: any) {
      console.error('Documentation Generation API Error:', err);
      if (err.response?.status === 422) {
        const errorData = err.response?.data;
        if (errorData?.error?.errors && Array.isArray(errorData.error.errors)) {
          const validationErrors = errorData.error.errors
            .map((e: any) => `${e.field}: ${e.message}`)
            .join(', ');
          setError(`バリデーションエラー: ${validationErrors}`);
        } else {
          setError(errorData?.error?.message || errorData?.detail || 'バリデーションエラーが発生しました');
        }
      } else {
        setError(err.response?.data?.error?.message || err.response?.data?.detail || 'ドキュメント生成に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        AI支援開発
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        コード生成支援、テスト自動化、コードレビュー支援
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab icon={<Code />} label="コード生成" />
          <Tab icon={<BugReport />} label="コードレビュー" />
          <Tab icon={<Description />} label="ドキュメント生成" />
        </Tabs>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  コード生成
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="生成したいコードの説明を入力してください"
                  sx={{ mb: 2 }}
                />
                <Button
                  variant="contained"
                  onClick={handleGenerateCode}
                  disabled={loading || !description.trim()}
                  fullWidth
                >
                  {loading ? <CircularProgress size={24} /> : '生成'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  生成されたコード
                </Typography>
                <Paper
                  sx={{
                    p: 2,
                    minHeight: 200,
                    bgcolor: 'grey.100',
                    fontFamily: 'monospace',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {result || '生成されたコードがここに表示されます'}
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  コードレビュー
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={8}
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="レビューしたいコードを入力してください"
                  sx={{ mb: 2 }}
                />
                <Box sx={{ mb: 2 }}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={checkStyle}
                        onChange={(e) => setCheckStyle(e.target.checked)}
                      />
                    }
                    label="スタイルチェック"
                  />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={checkSecurity}
                        onChange={(e) => setCheckSecurity(e.target.checked)}
                      />
                    }
                    label="セキュリティチェック"
                  />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={checkPerformance}
                        onChange={(e) => setCheckPerformance(e.target.checked)}
                      />
                    }
                    label="パフォーマンスチェック"
                  />
                </Box>
                <Button
                  variant="contained"
                  onClick={handleReviewCode}
                  disabled={loading || !code.trim()}
                  fullWidth
                >
                  {loading ? <CircularProgress size={24} /> : 'レビュー'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  レビュー結果
                </Typography>
                <Paper
                  sx={{
                    p: 2,
                    minHeight: 200,
                    bgcolor: 'grey.100',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {result || 'レビュー結果がここに表示されます'}
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  ドキュメント生成
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  value={docContent}
                  onChange={(e) => setDocContent(e.target.value)}
                  placeholder="ドキュメントの内容を入力してください"
                  sx={{ mb: 2 }}
                />
                <Button
                  variant="contained"
                  onClick={handleGenerateDoc}
                  disabled={loading || !docContent.trim()}
                  fullWidth
                >
                  {loading ? <CircularProgress size={24} /> : '生成'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  生成されたドキュメント
                </Typography>
                <Paper
                  sx={{
                    p: 2,
                    minHeight: 200,
                    bgcolor: 'grey.100',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {result || '生成されたドキュメントがここに表示されます'}
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};
