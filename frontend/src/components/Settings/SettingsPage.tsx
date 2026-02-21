/**
 * 設定ページ
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
  Divider,
  Alert,
  Paper,
  List,
  ListItem,
  ListItemText,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  AccountCircle,
  Security,
  Notifications,
  Language,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';

export const SettingsPage: React.FC = () => {
  const { user } = useAuth();
  const [email, setEmail] = useState(user?.email || '');
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [notifications, setNotifications] = useState(true);
  const [language, setLanguage] = useState('ja');
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSave = () => {
    // 設定を保存（実際の実装ではAPIを呼び出す）
    setMessage({ type: 'success', text: '設定を保存しました' });
    setTimeout(() => setMessage(null), 3000);
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        設定
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        ユーザー設定とシステム設定を管理
      </Typography>

      {message && (
        <Alert severity={message.type} sx={{ mb: 2 }}>
          {message.text}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AccountCircle sx={{ mr: 1 }} />
                <Typography variant="h6">プロフィール設定</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <TextField
                fullWidth
                label="ユーザー名"
                value={user?.username || ''}
                disabled
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="メールアドレス"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="表示名"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="部署"
                value={user?.department || ''}
                disabled
                sx={{ mb: 2 }}
              />
              <Button variant="contained" onClick={handleSave} fullWidth>
                保存
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Security sx={{ mr: 1 }} />
                <Typography variant="h6">セキュリティ設定</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <List>
                <ListItem>
                  <ListItemText
                    primary="ロール"
                    secondary={user?.roles.join(', ') || '-'}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="権限"
                    secondary={user?.roles.includes('admin') ? '全権限' : '制限あり'}
                  />
                </ListItem>
              </List>
              <Button variant="outlined" fullWidth sx={{ mt: 2 }}>
                パスワード変更
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Notifications sx={{ mr: 1 }} />
                <Typography variant="h6">通知設定</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <FormControlLabel
                control={
                  <Switch
                    checked={notifications}
                    onChange={(e) => setNotifications(e.target.checked)}
                  />
                }
                label="通知を有効にする"
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Language sx={{ mr: 1 }} />
                <Typography variant="h6">言語設定</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <TextField
                fullWidth
                select
                label="言語"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                SelectProps={{
                  native: true,
                }}
              >
                <option value="ja">日本語</option>
                <option value="en">English</option>
              </TextField>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                システム情報
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
                <Typography variant="body2">
                  <strong>バージョン:</strong> 5.0.0
                </Typography>
                <Typography variant="body2">
                  <strong>環境:</strong> 開発環境
                </Typography>
                <Typography variant="body2">
                  <strong>ユーザー:</strong> {user?.username} ({user?.roles.join(', ')})
                </Typography>
              </Paper>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
