/**
 * インクルーシブ雇用AIプラットフォーム
 * 障害者雇用マッチング + アクセシビリティ特化AI + UX評価
 */
import React, { useState } from 'react';
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Card,
  CardContent,
  TextField,
  Button,
  Paper,
  Grid,
  Chip,
  Alert,
  CircularProgress,
  FormControlLabel,
  Switch,
} from '@mui/material';
import {
  Work,
  Chat,
  Assessment,
  Psychology,
} from '@mui/icons-material';
import apiClient from '../../api/client';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  );
}

export const InclusiveWorkPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [skills, setSkills] = useState('');
  const [chatMessage, setChatMessage] = useState('');
  const [evalUrl, setEvalUrl] = useState('');
  const [agentQuery, setAgentQuery] = useState('');
  const [simpleUi, setSimpleUi] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleMatching = async () => {
    try {
      setLoading(true);
      setError('');
      const res = await apiClient.post('/api/v1/inclusive-work/matching', {
        skills: skills ? skills.split(',').map((s) => s.trim()) : [],
      });
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'マッチングに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleChat = async () => {
    try {
      setLoading(true);
      setError('');
      const res = await apiClient.post('/api/v1/inclusive-work/chat', {
        message: chatMessage,
        simple_ui: simpleUi,
      });
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'チャットに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleEval = async () => {
    try {
      setLoading(true);
      setError('');
      const res = await apiClient.post('/api/v1/inclusive-work/ux-evaluation', {
        url: evalUrl,
      });
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || '評価に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleAgent = async () => {
    try {
      setLoading(true);
      setError('');
      const res = await apiClient.post('/api/v1/inclusive-work/agent', {
        task_type: 'matching',
        query: agentQuery,
        context: { skills: agentQuery.split(',').map((s) => s.trim()) },
      });
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'エージェント実行に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        インクルーシブ雇用AI
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        障害者雇用マッチング + アクセシビリティ特化AI + 当事者視点UX評価
      </Typography>

      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tab icon={<Work />} label="マッチング" />
        <Tab icon={<Chat />} label="アクセシビリティAI" />
        <Tab icon={<Assessment />} label="UX評価" />
        <Tab icon={<Psychology />} label="AIエージェント" />
      </Tabs>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>求人マッチング</Typography>
                <TextField
                  fullWidth
                  label="スキル（カンマ区切り）"
                  placeholder="Python, React, リモート"
                  value={skills}
                  onChange={(e) => setSkills(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <Button variant="contained" onClick={handleMatching} disabled={loading} fullWidth>
                  {loading ? <CircularProgress size={24} /> : '検索'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>マッチ結果</Typography>
                {result?.matches?.length ? (
                  result.matches.map((job: any) => (
                    <Paper key={job.id} sx={{ p: 2, mb: 1 }}>
                      <Typography variant="subtitle1">{job.title} - {job.company}</Typography>
                      <Box sx={{ mt: 1 }}>
                        <Chip size="small" label={`適合度 ${(job.match_score * 100).toFixed(0)}%`} color="primary" sx={{ mr: 1 }} />
                        {job.disability_support?.map((s: string) => (
                          <Chip key={s} size="small" label={s} variant="outlined" sx={{ mr: 0.5, mb: 0.5 }} />
                        ))}
                      </Box>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>{job.description}</Typography>
                    </Paper>
                  ))
                ) : (
                  <Typography color="text.secondary">スキルを入力して検索してください</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>アクセシビリティAI</Typography>
                <FormControlLabel
                  control={<Switch checked={simpleUi} onChange={(e) => setSimpleUi(e.target.checked)} />}
                  label="簡易UIモード（短い応答）"
                />
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="メッセージ"
                  placeholder="求人、リモート、障害者雇用..."
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <Button variant="contained" onClick={handleChat} disabled={loading || !chatMessage.trim()} fullWidth>
                  {loading ? <CircularProgress size={24} /> : '送信'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>回答</Typography>
                <Paper sx={{ p: 2, minHeight: 120, bgcolor: 'grey.100' }}>
                  {result?.answer || 'メッセージを入力して送信してください'}
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>当事者視点UX評価</Typography>
                <TextField
                  fullWidth
                  label="評価するURL"
                  placeholder="https://example.com"
                  value={evalUrl}
                  onChange={(e) => setEvalUrl(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <Button variant="contained" onClick={handleEval} disabled={loading || !evalUrl.trim()} fullWidth>
                  {loading ? <CircularProgress size={24} /> : '評価'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>評価結果</Typography>
                {result?.overall_score != null ? (
                  <Box>
                    <Chip label={`総合: ${result.overall_score} (${result.grade})`} color="primary" sx={{ mb: 2 }} />
                    <Typography variant="body2" sx={{ mb: 2 }}>{result.summary}</Typography>
                    {result.items?.map((item: any) => (
                      <Paper key={item.id} sx={{ p: 1, mb: 1 }}>
                        {item.name}: {item.score} ({item.status}) - {item.recommendation}
                      </Paper>
                    ))}
                  </Box>
                ) : (
                  <Typography color="text.secondary">URLを入力して評価してください</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>AIエージェント</Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="クエリ（スキル等）"
                  placeholder="Python, React, リモート"
                  value={agentQuery}
                  onChange={(e) => setAgentQuery(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <Button variant="contained" onClick={handleAgent} disabled={loading || !agentQuery.trim()} fullWidth>
                  {loading ? <CircularProgress size={24} /> : '実行'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>エージェント結果</Typography>
                <Paper sx={{ p: 2, minHeight: 120, bgcolor: 'grey.100', whiteSpace: 'pre-wrap' }}>
                  {result ? JSON.stringify(result, null, 2) : 'クエリを入力して実行してください'}
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
};
