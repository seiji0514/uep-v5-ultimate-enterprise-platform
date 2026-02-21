/**
 * WebAssembly デモページ
 * WASM による計算処理のデモ
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import { loadWasm, wasmAdd, wasmMultiply, wasmSum, isWasmLoaded } from '../../wasm/compute';

export const WasmPage: React.FC = () => {
  const [loaded, setLoaded] = useState(false);
  const [a, setA] = useState(10);
  const [b, setB] = useState(20);
  const [n, setN] = useState(100);
  const [addResult, setAddResult] = useState<number | null>(null);
  const [mulResult, setMulResult] = useState<number | null>(null);
  const [sumResult, setSumResult] = useState<number | null>(null);

  useEffect(() => {
    loadWasm().then(setLoaded);
  }, []);

  const runAdd = () => setAddResult(wasmAdd(a, b));
  const runMul = () => setMulResult(wasmMultiply(a, b));
  const runSum = () => setSumResult(wasmSum(n));

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        WebAssembly 計算デモ
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        フロントエンドの計算処理を WASM で実行（.wasm が無い場合は JS フォールバック）
      </Typography>

      {!loaded && (
        <Alert severity="info" sx={{ mb: 2 }}>
          モジュールをロード中...
        </Alert>
      )}
      {loaded && (
        <Alert severity={isWasmLoaded() ? 'success' : 'info'} sx={{ mb: 2 }}>
          {isWasmLoaded()
            ? 'WASM モジュールで実行中'
            : 'JS フォールバックで実行中（compute.wasm をビルドするには wat2wasm を使用）'}
        </Alert>
      )}

      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                加算: add(a, b)
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexWrap: 'wrap' }}>
                <TextField
                  type="number"
                  size="small"
                  value={a}
                  onChange={(e) => setA(Number(e.target.value))}
                  sx={{ width: 80 }}
                />
                <Typography>+</Typography>
                <TextField
                  type="number"
                  size="small"
                  value={b}
                  onChange={(e) => setB(Number(e.target.value))}
                  sx={{ width: 80 }}
                />
                <Button variant="contained" onClick={runAdd}>
                  実行
                </Button>
              </Box>
              {addResult !== null && (
                <Typography sx={{ mt: 1 }}>結果: {addResult}</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                乗算: multiply(a, b)
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexWrap: 'wrap' }}>
                <TextField
                  type="number"
                  size="small"
                  value={a}
                  onChange={(e) => setA(Number(e.target.value))}
                  sx={{ width: 80 }}
                />
                <Typography>×</Typography>
                <TextField
                  type="number"
                  size="small"
                  value={b}
                  onChange={(e) => setB(Number(e.target.value))}
                  sx={{ width: 80 }}
                />
                <Button variant="contained" onClick={runMul}>
                  実行
                </Button>
              </Box>
              {mulResult !== null && (
                <Typography sx={{ mt: 1 }}>結果: {mulResult}</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                合計: sum(n) = 0+1+...+(n-1)
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexWrap: 'wrap' }}>
                <TextField
                  type="number"
                  size="small"
                  value={n}
                  onChange={(e) => setN(Number(e.target.value))}
                  sx={{ width: 80 }}
                />
                <Button variant="contained" onClick={runSum}>
                  実行
                </Button>
              </Box>
              {sumResult !== null && (
                <Typography sx={{ mt: 1 }}>結果: {sumResult}</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ p: 2, mt: 2 }}>
        <Typography variant="subtitle2" gutterBottom>
          compute.wasm のビルド
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <code>wat2wasm frontend/public/wasm/compute.wat -o frontend/public/wasm/compute.wasm</code>
          <br />
          (wabt をインストール: choco install wabt / brew install wabt)
        </Typography>
      </Paper>
    </Box>
  );
};
