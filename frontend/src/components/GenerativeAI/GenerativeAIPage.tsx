/**
 * 生成AIページ
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
} from '@mui/material';
import {
  Psychology,
  QuestionAnswer,
  Lightbulb,
} from '@mui/icons-material';
import { generativeAiApi } from '../../api/generativeAi';

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

export const GenerativeAIPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [prompt, setPrompt] = useState('');
  const [query, setQuery] = useState('');
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    try {
      setLoading(true);
      setError('');
      const response = await generativeAiApi.generate({ prompt });
      setResult(response.text || JSON.stringify(response, null, 2));
    } catch (err: any) {
      console.error('Generative AI API Error:', err);
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
        setError(err.response?.data?.error?.message || err.response?.data?.detail || '生成に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRAG = async () => {
    if (!query.trim()) return;
    try {
      setLoading(true);
      setError('');
      const response = await generativeAiApi.rag({ query });
      let display = response.answer || '';
      if (response.metrics) {
        display += `\n\n【評価指標】\n検索: ${response.metrics.retrieved_count}件, ` +
          `類似度: ${response.metrics.avg_relevance_score?.toFixed(2) || '-'}, ` +
          `レイテンシ: ${response.metrics.total_latency_ms}ms`;
      }
      if (response.sources?.length) {
        display += `\n\n【参照ソース】\n${response.sources.map((s: any) => `・${s.text?.slice(0, 80)}...`).join('\n')}`;
      }
      setResult(display || JSON.stringify(response, null, 2));
    } catch (err: any) {
      console.error('RAG API Error:', err);
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
        setError(err.response?.data?.error?.message || err.response?.data?.detail || 'RAGクエリに失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReasoning = async () => {
    if (!question.trim()) return;
    try {
      setLoading(true);
      setError('');
      const response = await generativeAiApi.reasoning({ question });
      setResult(response.answer || JSON.stringify(response, null, 2));
    } catch (err: any) {
      console.error('Reasoning API Error:', err);
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
        setError(err.response?.data?.error?.message || err.response?.data?.detail || '推論に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        生成AI
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        LLM統合、RAG、CoT推論、生成AIアプリケーション開発
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab icon={<Psychology />} label="テキスト生成" />
          <Tab icon={<QuestionAnswer />} label="RAG" />
          <Tab icon={<Lightbulb />} label="CoT推論" />
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
                  プロンプト入力
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="生成したいテキストのプロンプトを入力してください"
                  sx={{ mb: 2 }}
                />
                <Button
                  variant="contained"
                  onClick={handleGenerate}
                  disabled={loading || !prompt.trim()}
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
                  生成結果
                </Typography>
                <Paper
                  sx={{
                    p: 2,
                    minHeight: 200,
                    bgcolor: 'grey.100',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {result || '結果がここに表示されます'}
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
                  RAGクエリ
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="質問を入力してください"
                  sx={{ mb: 2 }}
                />
                <Button
                  variant="contained"
                  onClick={handleRAG}
                  disabled={loading || !query.trim()}
                  fullWidth
                >
                  {loading ? <CircularProgress size={24} /> : '検索'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  回答
                </Typography>
                <Paper
                  sx={{
                    p: 2,
                    minHeight: 200,
                    bgcolor: 'grey.100',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {result || '回答がここに表示されます'}
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
                  質問入力
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="推論が必要な質問を入力してください"
                  sx={{ mb: 2 }}
                />
                <Button
                  variant="contained"
                  onClick={handleReasoning}
                  disabled={loading || !question.trim()}
                  fullWidth
                >
                  {loading ? <CircularProgress size={24} /> : '推論'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  推論結果
                </Typography>
                <Paper
                  sx={{
                    p: 2,
                    minHeight: 200,
                    bgcolor: 'grey.100',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {result || '推論結果がここに表示されます'}
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};
