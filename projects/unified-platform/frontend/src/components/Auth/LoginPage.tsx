import { useState } from 'react';
import { Box, Paper, TextField, Button, Typography, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    const result = await login(username, password);
    if (result.ok) navigate('/');
    else setError(result.error || 'ログインに失敗しました。ユーザー名・パスワードを確認してください。');
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'background.default', p: 2 }}>
      <Paper elevation={0} sx={{ p: 3, maxWidth: 400, width: '100%' }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>{import.meta.env.VITE_APP_TITLE || '統合基盤プラットフォーム'}</Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>ログイン</Typography>
        <form onSubmit={handleSubmit}>
          <TextField fullWidth label="ユーザー名" value={username} onChange={(e) => setUsername(e.target.value)} sx={{ mb: 2 }} />
          <TextField fullWidth type="password" label="パスワード" value={password} onChange={(e) => setPassword(e.target.value)} sx={{ mb: 2 }} />
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Button type="submit" variant="contained" fullWidth>ログイン</Button>
        </form>
      </Paper>
    </Box>
  );
}
