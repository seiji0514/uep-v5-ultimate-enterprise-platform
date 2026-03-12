/**
 * 最適化・精度向上ページ
 * 異常検知（閾値・アンサンブル）、ヘルスチェック、キャッシュ状態の可視化
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
  TableRow,
  TextField,
  Button,
  Alert,
  Chip,
  CircularProgress,
  Paper,
} from '@mui/material';
import {
  Warning,
  CheckCircle,
  Cached,
  HealthAndSafety,
} from '@mui/icons-material';
import { optimizationApi, ThresholdConfig } from '../../api/optimization';
import apiClient from '../../api/client';

export const OptimizationPage: React.FC = () => {
  const [thresholds, setThresholds] = useState<Record<string, ThresholdConfig>>({});
  const [healthDetail, setHealthDetail] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [detectMetric, setDetectMetric] = useState('heart_rate');
  const [detectValue, setDetectValue] = useState('125');
  const [detectResult, setDetectResult] = useState<Record<string, unknown> | null>(null);
  const [detecting, setDetecting] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [threshRes, healthRes] = await Promise.all([
        optimizationApi.getThresholds(),
        apiClient.get('/api/v1/monitoring/health/detailed').catch(() => ({ data: null })),
      ]);
      setThresholds(threshRes.thresholds || {});
      setHealthDetail(healthRes.data as Record<string, unknown> | null);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '読み込みに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDetect = async () => {
    const val = parseFloat(detectValue);
    if (isNaN(val)) return;
    try {
      setDetecting(true);
      setDetectResult(null);
      const result = await optimizationApi.detectAnomaly(detectMetric, val);
      setDetectResult(result as unknown as Record<string, unknown>);
    } catch (err: any) {
      setDetectResult({ error: err.response?.data?.detail || err.message });
    } finally {
      setDetecting(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress aria-label="読み込み中" />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }} component="h1">
        最適化・精度向上
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        RAG検索精度、推論品質、異常検知、稼働率、推論レイテンシの改善機能を可視化します。
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* 異常検知 - 閾値一覧 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Warning color="warning" /> 異常検知 閾値設定
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                閾値調整・特徴量・モデルアンサンブルで検知精度を向上
              </Typography>
              <Table size="small">
                <TableBody>
                  {Object.entries(thresholds).map(([key, cfg]) => (
                    <TableRow key={key}>
                      <TableCell>{cfg.metric}</TableCell>
                      <TableCell>上限: {cfg.upper}</TableCell>
                      <TableCell>下限: {cfg.lower}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>

        {/* 異常検知 - 検知実行 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                異常検知テスト（アンサンブル）
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center', mb: 2 }}>
                <TextField
                  select
                  size="small"
                  label="メトリック"
                  value={detectMetric}
                  onChange={(e) => setDetectMetric(e.target.value)}
                  SelectProps={{ native: true }}
                  sx={{ minWidth: 140 }}
                >
                  {Object.keys(thresholds).length > 0 ? (
                    Object.keys(thresholds).map((k) => (
                      <option key={k} value={k}>{thresholds[k]?.metric || k}</option>
                    ))
                  ) : (
                    <>
                      <option value="heart_rate">心拍数</option>
                      <option value="vibration">振動</option>
                      <option value="temperature_equipment">設備温度</option>
                    </>
                  )}
                </TextField>
                <TextField
                  size="small"
                  label="値"
                  type="number"
                  value={detectValue}
                  onChange={(e) => setDetectValue(e.target.value)}
                  sx={{ width: 100 }}
                />
                <Button
                  variant="contained"
                  onClick={handleDetect}
                  disabled={detecting}
                  startIcon={detecting ? <CircularProgress size={16} /> : <Warning />}
                >
                  検知
                </Button>
              </Box>
              {detectResult && (
                <Paper variant="outlined" sx={{ p: 2, bgcolor: 'action.hover' }}>
                  <Typography variant="body2" component="pre" sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
                    {JSON.stringify(detectResult, null, 2)}
                  </Typography>
                  {detectResult.is_anomaly === true && (
                    <Chip
                      label={`異常: ${detectResult.severity}`}
                      color="error"
                      size="small"
                      sx={{ mt: 1 }}
                    />
                  )}
                </Paper>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* 稼働率 - ヘルスチェック */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <HealthAndSafety color="success" /> 稼働率・監視
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                リトライ・フェイルオーバー・監視強化
              </Typography>
              {healthDetail ? (
                <Box>
                  <Chip
                    label={String(healthDetail.status || 'unknown')}
                    color={healthDetail.status === 'healthy' ? 'success' : 'default'}
                    size="small"
                    sx={{ mr: 1 }}
                  />
                  {typeof healthDetail.healthy_count === 'number' && (
                    <Typography variant="body2" component="span">
                      健全サービス: {healthDetail.healthy_count}
                    </Typography>
                  )}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  ヘルス詳細は利用できません
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* 推論レイテンシ - キャッシュ */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Cached color="primary" /> 推論レイテンシ・キャッシュ
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                同一クエリの2回目以降はキャッシュヒットで高速応答
              </Typography>
              <Alert severity="info" sx={{ mt: 1 }}>
                生成AIページで同じプロンプトを2回実行すると、2回目は「キャッシュヒット」と表示されます。
              </Alert>
            </CardContent>
          </Card>
        </Grid>

        {/* 実装済み機能サマリ */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <CheckCircle color="success" /> 実装済みの5項目
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">RAG検索精度</Typography>
                    <Typography variant="body2" color="text.secondary">
                      ハイブリッド検索、RRF再ランキング、チャンク分割
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">推論品質</Typography>
                    <Typography variant="body2" color="text.secondary">
                      CoTプロンプト強化、難度別モデル選択
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">異常検知</Typography>
                    <Typography variant="body2" color="text.secondary">
                      閾値調整、Z-score/ローリング、アンサンブル
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">稼働率</Typography>
                    <Typography variant="body2" color="text.secondary">
                      ヘルスチェックリトライ、フェイルオーバー
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">推論レイテンシ</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Redis/メモリキャッシュ、LLMフェイルオーバー
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
