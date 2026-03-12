/**
 * 設定ページ - テーマ・ポーリング間隔・言語・パスワード変更・ヘルス・ログ
 */
import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, FormControlLabel, Switch, Slider, TextField, FormControl, InputLabel, Select, MenuItem, Button, Alert, Chip } from '@mui/material';
import { HealthAndSafety, Terminal, Refresh } from '@mui/icons-material';
import { useThemeMode } from '../contexts/ThemeContext';
import { useSettings } from '../contexts/SettingsContext';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';
import { authApi, unifiedApi } from '../api/unified';

export const SettingsPage: React.FC = () => {
  const { mode, toggleTheme } = useThemeMode();
  const { settings, setPollInterval, setItemsPerPage, setCompactMode } = useSettings();
  const { t, i18n } = useTranslation();
  const { user } = useAuth();
  const [currentPw, setCurrentPw] = useState('');
  const [newPw, setNewPw] = useState('');
  const [pwMsg, setPwMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [health, setHealth] = useState<{ health?: any; ready?: any } | null>(null);
  const [logs, setLogs] = useState<{ ts: string; level: string; msg: string }[]>([]);
  const [showLogs, setShowLogs] = useState(false);

  useEffect(() => {
    unifiedApi.health.detail().then((r) => setHealth(r.data)).catch(() => setHealth(null));
  }, []);

  const loadLogs = () => {
    unifiedApi.logs.list(100).then((r) => setLogs(r.data.items || [])).catch(() => setLogs([]));
    setShowLogs(true);
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPwMsg(null);
    if (!currentPw || !newPw) {
      setPwMsg({ type: 'error', text: '現在のパスワードと新しいパスワードを入力してください。' });
      return;
    }
    if (newPw.length < 8) {
      setPwMsg({ type: 'error', text: '新しいパスワードは8文字以上にしてください。' });
      return;
    }
    if (!/[a-zA-Z]/.test(newPw) || !/[0-9]/.test(newPw)) {
      setPwMsg({ type: 'error', text: '新しいパスワードは英字と数字の両方を含めてください。' });
      return;
    }
    try {
      await authApi.changePassword(currentPw, newPw);
      setPwMsg({ type: 'success', text: 'パスワードを変更しました。' });
      setCurrentPw('');
      setNewPw('');
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setPwMsg({ type: 'error', text: typeof detail === 'string' ? detail : 'パスワードの変更に失敗しました。' });
    }
  };

  return (
    <Box component="section" sx={{ minHeight: 400, width: '100%', display: 'block', pt: 1 }}>
      <Typography variant="h5" fontWeight={600} gutterBottom>{t('settings.title')}</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        {t('settings.subtitle')}
      </Typography>

      <Paper elevation={0} sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>{t('settings.theme')}</Typography>
        <FormControlLabel
          control={<Switch checked={mode === 'dark'} onChange={toggleTheme} />}
          label={mode === 'dark' ? t('settings.darkMode') : t('settings.lightMode')}
        />
      </Paper>

      <Paper elevation={0} sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>{t('settings.language')}</Typography>
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel>{t('settings.language')}</InputLabel>
          <Select value={i18n.language?.startsWith('en') ? 'en' : 'ja'} label={t('settings.language')} onChange={(e) => i18n.changeLanguage(e.target.value)}>
            <MenuItem value="ja">{t('settings.japanese')}</MenuItem>
            <MenuItem value="en">{t('settings.english')}</MenuItem>
          </Select>
        </FormControl>
      </Paper>

      <Paper elevation={0} sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>{t('settings.pollInterval')}</Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {settings.pollIntervalMs / 1000} 秒
        </Typography>
        <Slider
          value={settings.pollIntervalMs / 1000}
          min={5}
          max={300}
          step={5}
          valueLabelDisplay="auto"
          valueLabelFormat={(v) => `${v}秒`}
          onChange={(_, v) => setPollInterval((v as number) * 1000)}
        />
        <TextField
          type="number"
          size="small"
          label="秒数（直接入力）"
          value={settings.pollIntervalMs / 1000}
          onChange={(e) => setPollInterval(parseInt(e.target.value, 10) * 1000)}
          inputProps={{ min: 5, max: 300 }}
          sx={{ mt: 2, width: 120 }}
        />
      </Paper>

      <Paper elevation={0} sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>表示設定</Typography>
        <FormControl size="small" sx={{ minWidth: 160, mr: 2 }}>
          <InputLabel>一覧の表示件数</InputLabel>
          <Select value={settings.itemsPerPage} label="一覧の表示件数" onChange={(e) => setItemsPerPage(Number(e.target.value))}>
            <MenuItem value={5}>5件</MenuItem>
            <MenuItem value={10}>10件</MenuItem>
            <MenuItem value={25}>25件</MenuItem>
            <MenuItem value={50}>50件</MenuItem>
          </Select>
        </FormControl>
        <FormControlLabel control={<Switch checked={settings.compactMode} onChange={(_, v) => setCompactMode(v)} size="small" />} label="コンパクト表示" />
      </Paper>

      <Paper elevation={0} sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <HealthAndSafety fontSize="small" /> ヘルスダッシュボード
        </Typography>
        {health ? (
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 1 }}>
            <Chip label={`Health: ${health.health?.status ?? '-'}`} color={health.health?.status === 'ok' ? 'success' : 'default'} size="small" />
            <Chip label={`Ready: ${health.ready?.status ?? '-'}`} color={health.ready?.database ? 'success' : 'warning'} size="small" />
            <Chip label={`DB: ${health.ready?.database ? 'OK' : 'NG'}`} color={health.ready?.database ? 'success' : 'error'} size="small" />
          </Box>
        ) : (
          <Typography variant="body2" color="text.secondary">取得できません</Typography>
        )}
      </Paper>

      <Paper elevation={0} sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1" fontWeight={600} gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Terminal fontSize="small" /> ログビューア
        </Typography>
        <Button size="small" startIcon={<Refresh />} onClick={loadLogs}>ログを取得</Button>
        {showLogs && (
          <Box sx={{ mt: 2, maxHeight: 300, overflow: 'auto', bgcolor: 'action.hover', p: 1, borderRadius: 1, fontFamily: 'monospace', fontSize: 12 }}>
            {logs.length === 0 ? <Typography variant="body2" color="text.secondary">ログがありません</Typography> : logs.map((l, i) => (
              <Box key={i} sx={{ mb: 0.5 }}><Typography component="span" variant="caption" color="text.secondary">{l.ts}</Typography> [{l.level}] {l.msg}</Box>
            ))}
          </Box>
        )}
      </Paper>

      {user && user !== 'api-key-user' && (
        <Paper elevation={0} sx={{ p: 2, mt: 2 }}>
          <Typography variant="subtitle1" fontWeight={600} gutterBottom>パスワード変更</Typography>
          <form onSubmit={handleChangePassword}>
            <TextField
              fullWidth
              type="password"
              label="現在のパスワード"
              value={currentPw}
              onChange={(e) => setCurrentPw(e.target.value)}
              sx={{ mb: 2 }}
              autoComplete="current-password"
            />
            <TextField
              fullWidth
              type="password"
              label="新しいパスワード（8文字以上・英数字含む）"
              value={newPw}
              onChange={(e) => setNewPw(e.target.value)}
              sx={{ mb: 2 }}
              autoComplete="new-password"
            />
            {pwMsg && <Alert severity={pwMsg.type} sx={{ mb: 2 }}>{pwMsg.text}</Alert>}
            <Button type="submit" variant="outlined">パスワードを変更</Button>
          </form>
        </Paper>
      )}
    </Box>
  );
};
