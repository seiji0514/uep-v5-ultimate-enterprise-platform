/**
 * 自動切替中に表示するバー（停止ボタン）
 */
import React from 'react';
import { Box, IconButton, Typography, Tooltip } from '@mui/material';
import { Stop, VisibilityOff, Pause, PlayArrow } from '@mui/icons-material';
import { useAutoPlay } from '../../contexts/AutoPlayContext';
import { AUTO_PLAY_STEPS } from '../../contexts/AutoPlayContext';

export const AutoPlayBar: React.FC = () => {
  const ctx = useAutoPlay();
  if (!ctx || !ctx.isAutoPlaying || ctx.hidePlayBar) return null;
  const { currentStep, stopAutoPlay, setHidePlayBar, isPaused, togglePause } = ctx;

  const step = AUTO_PLAY_STEPS[currentStep];
  return (
    <Box
      sx={{
        position: 'fixed',
        bottom: 16,
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        alignItems: 'center',
        gap: 1,
        px: 2,
        py: 1,
        borderRadius: 2,
        bgcolor: 'primary.main',
        color: 'primary.contrastText',
        zIndex: 1300,
        boxShadow: 3,
      }}
    >
      <Typography variant="body2">自動再生中: {step?.title ?? ''}</Typography>
      <Tooltip title={isPaused ? '再開' : '一時停止'}>
        <IconButton size="small" onClick={togglePause} color="inherit" aria-label={isPaused ? '再開' : '一時停止'}>
          {isPaused ? <PlayArrow /> : <Pause />}
        </IconButton>
      </Tooltip>
      <Tooltip title="バーを非表示（画面共有用）">
        <IconButton size="small" onClick={() => setHidePlayBar(true)} color="inherit" aria-label="バーを非表示">
          <VisibilityOff />
        </IconButton>
      </Tooltip>
      <IconButton size="small" onClick={stopAutoPlay} color="inherit" aria-label="停止">
        <Stop />
      </IconButton>
    </Box>
  );
};
