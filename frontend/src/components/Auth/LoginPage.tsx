/**
 * ログインページ
 */
import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
} from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Navigate } from 'react-router-dom';

export const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [touched, setTouched] = useState({ username: false, password: false });
  const { login, isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();

  // 既にログイン済みならダッシュボードへ
  if (!isLoading && isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    const u = username.trim();
    const p = password.trim();
    if (!u || !p) {
      setError('ユーザー名とパスワードを入力してください。');
      return;
    }
    if (u.length < 2) {
      setError('ユーザー名は2文字以上で入力してください。');
      return;
    }
    if (p.length < 4) {
      setError('パスワードは4文字以上で入力してください。');
      return;
    }
    setLoading(true);

    try {
      await login({ username: u, password: p });
      setLoading(false); // CircularProgress を先にアンマウント（removeChild エラー回避）
      // 次のフレームでナビゲート（DOM 更新を待つ）
      requestAnimationFrame(() => {
        requestAnimationFrame(() => navigate('/', { replace: true }));
      });
    } catch (err: any) {
      let message = 'ログインに失敗しました';
      if (!err.response) {
        message = 'サーバーに接続できません。バックエンドが起動しているか確認し、数秒後に再試行してください。';
      } else if (err.response.status === 401) {
        message = 'ユーザー名またはパスワードが正しくありません。';
      } else if (err.response?.data?.detail) {
        message = typeof err.response.data.detail === 'string'
          ? err.response.data.detail
          : JSON.stringify(err.response.data.detail);
      }
      setError(message);
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ padding: 4, width: '100%' }}>
          <Typography component="h1" variant="h4" align="center" gutterBottom>
            UEP v5.0
          </Typography>
          <Typography component="h2" variant="h6" align="center" color="text.secondary" gutterBottom>
            Ultimate Enterprise Platform
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="ユーザー名"
              error={touched.username && username.trim().length > 0 && username.trim().length < 2}
              helperText={touched.username && username.trim().length > 0 && username.trim().length < 2 ? '2文字以上で入力してください' : ''}
              onBlur={() => setTouched((t) => ({ ...t, username: true }))}
              name="username"
              autoComplete="username"
              autoFocus
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="パスワード"
              type="password"
              id="password"
              autoComplete="current-password"
              error={touched.password && password.length > 0 && password.length < 4}
              helperText={touched.password && password.length > 0 && password.length < 4 ? '4文字以上で入力してください' : ''}
              onBlur={() => setTouched((t) => ({ ...t, password: true }))}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
              aria-label="ログイン"
            >
              {loading ? 'ログイン中...' : 'ログイン'}
            </Button>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary" align="center">
                デモ: kaho0525 / 0525 または developer / dev123
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};
