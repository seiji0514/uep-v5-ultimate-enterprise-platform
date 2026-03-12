import React, { useState } from 'react';
import { Container, Paper, TextField, Button, Typography, Box, Alert } from '@mui/material';
import { Dashboard } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

export const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username.trim(), password.trim());
    } catch (err: any) {
      setError(err?.message || 'ログインに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ padding: 4, width: '100%' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1, mb: 2 }}>
            <Dashboard />
            <Typography component="h1" variant="h5">企業横断オペレーション基盤</Typography>
          </Box>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2, textAlign: 'center' }}>
            Enterprise Operations Hub
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
            <TextField margin="normal" required fullWidth label="ユーザー名" value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" autoFocus />
            <TextField margin="normal" required fullWidth label="パスワード" type="password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" />
            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} disabled={loading}>
              {loading ? 'ログイン中...' : 'ログイン'}
            </Button>
          </Box>
          <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 2 }}>
            デモ: kaho0525 / 0525 | admin / admin123 | operator / op123 | viewer / view123
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};
