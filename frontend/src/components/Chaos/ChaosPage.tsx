/**
 * Chaos Engineering ページ
 * 障害シミュレーション（遅延・エラー注入）のUI
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Slider,
  Alert,
  CircularProgress,
  Chip,
  Divider,
} from '@mui/material';
import { BugReport, Speed, Error as ErrorIcon, Shuffle } from '@mui/icons-material';
import { chaosApi, ChaosStatus } from '../../api/chaos';

export const ChaosPage: React.FC = () => {
  const [status, setStatus] = useState<ChaosStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [result, setResult] = useState<string>('');
  const [delayMs, setDelayMs] = useState(500);
  const [errorRate, setErrorRate] = useState(0.5);
  const [mixedDelay, setMixedDelay] = useState(200);
  const [mixedErrorRate, setMixedErrorRate] = useState(0.3);
  const [executing, setExecuting] = useState(false);

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    try {
      setLoading(true);
      setError('');
      const res = await chaosApi.getStatus();
      setStatus(res.data);
    } catch (err: any) {
      setError(err.response?.status === 404 ? 'Chaos API が見つかりません。' : 'バックエンドに接続できません。');
      setStatus(null);
    } finally {
      setLoading(false);
    }
  };

  const handleDelay = async () => {
    setExecuting(true);
    setResult('');
    try {
      const start = Date.now();
      const res = await chaosApi.delay(delayMs);
      const elapsed = Date.now() - start;
      setResult(`遅延注入完了: ${res.data.actual_delay_ms}ms（経過: ${elapsed}ms）`);
    } catch (err: any) {
      setResult(`エラー: ${err.message || 'リクエスト失敗'}`);
    } finally {
      setExecuting(false);
    }
  };

  const handleError = async () => {
    setExecuting(true);
    setResult('');
    try {
      const res = await chaosApi.error(errorRate);
      setResult(res.data.message);
    } catch (err: any) {
      setResult(`エラー注入: HTTP ${err.response?.status || '不明'}`);
    } finally {
      setExecuting(false);
    }
  };

  const handleMixed = async () => {
    setExecuting(true);
    setResult('');
    try {
      const res = await chaosApi.mixed(mixedDelay, mixedErrorRate);
      setResult(`${res.data.message} (delay=${res.data.delay_ms}ms, error_rate=${res.data.error_rate})`);
    } catch (err: any) {
      setResult(`エラー注入: HTTP ${err.response?.status || '不明'}（混合シナリオ）`);
    } finally {
      setExecuting(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !status) {
    return (
      <Box p={3}>
        <Alert severity="error">{error || 'Chaos API の状態を取得できませんでした。'}</Alert>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Chaos Engineering
      </Typography>
      <Typography color="text.secondary" paragraph>
        障害シミュレーション（遅延・エラー注入）によるレジリエンス検証。開発・検証環境向け。
      </Typography>

      <Box mb={3}>
        <Chip label={status.enabled ? '有効' : '無効'} color={status.enabled ? 'success' : 'default'} size="small" />
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <Speed color="primary" />
                <Typography variant="h6">遅延注入</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                レスポンスを指定時間遅延させます（レイテンシ検証用）
              </Typography>
              <Box mt={2}>
                <Typography gutterBottom>遅延時間: {delayMs}ms</Typography>
                <Slider
                  value={delayMs}
                  onChange={(_, v) => setDelayMs(v as number)}
                  min={0}
                  max={5000}
                  step={100}
                  valueLabelDisplay="auto"
                />
              </Box>
            </CardContent>
            <CardActions>
              <Button variant="contained" onClick={handleDelay} disabled={executing}>
                {executing ? <CircularProgress size={24} /> : '実行'}
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <ErrorIcon color="error" />
                <Typography variant="h6">エラー注入</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                指定確率でHTTPエラーを返します（エラーハンドリング検証用）
              </Typography>
              <Box mt={2}>
                <Typography gutterBottom>エラー率: {(errorRate * 100).toFixed(0)}%</Typography>
                <Slider
                  value={errorRate}
                  onChange={(_, v) => setErrorRate(v as number)}
                  min={0}
                  max={1}
                  step={0.1}
                  valueLabelDisplay="auto"
                  valueLabelFormat={(v) => `${(v * 100).toFixed(0)}%`}
                />
              </Box>
            </CardContent>
            <CardActions>
              <Button variant="contained" color="error" onClick={handleError} disabled={executing}>
                {executing ? <CircularProgress size={24} /> : '実行'}
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <Shuffle color="secondary" />
                <Typography variant="h6">混合シナリオ</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                遅延＋エラー注入を組み合わせた検証
              </Typography>
              <Box mt={2}>
                <Typography gutterBottom>遅延: {mixedDelay}ms</Typography>
                <Slider
                  value={mixedDelay}
                  onChange={(_, v) => setMixedDelay(v as number)}
                  min={0}
                  max={2000}
                  step={100}
                  valueLabelDisplay="auto"
                />
                <Typography gutterBottom sx={{ mt: 2 }}>エラー率: {(mixedErrorRate * 100).toFixed(0)}%</Typography>
                <Slider
                  value={mixedErrorRate}
                  onChange={(_, v) => setMixedErrorRate(v as number)}
                  min={0}
                  max={1}
                  step={0.1}
                  valueLabelDisplay="auto"
                  valueLabelFormat={(v) => `${(v * 100).toFixed(0)}%`}
                />
              </Box>
            </CardContent>
            <CardActions>
              <Button variant="contained" color="secondary" onClick={handleMixed} disabled={executing}>
                {executing ? <CircularProgress size={24} /> : '実行'}
              </Button>
            </CardActions>
          </Card>
        </Grid>

        {result && (
          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">実行結果</Typography>
                <Typography variant="body1" sx={{ mt: 1 }}>{result}</Typography>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};
