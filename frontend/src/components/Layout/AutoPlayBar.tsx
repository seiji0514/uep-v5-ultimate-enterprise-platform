/**
 * 自動切替中に表示するバー（停止ボタン）
 */
import React from 'react';
import { Box, IconButton, Typography } from '@mui/material';
import { Stop } from '@mui/icons-material';
import { useAutoPlay } from '../../contexts/AutoPlayContext';
import { AUTO_PLAY_STEPS } from '../../contexts/AutoPlayContext';

export const AutoPlayBar: React.FC = () => {
  const ctx = useAutoPlay();
  if (!ctx || !ctx.isAutoPlaying) return null;
  const { currentStep, stopAutoPlay } = ctx;

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
      <IconButton size="small" onClick={stopAutoPlay} color="inherit" aria-label="停止">
        <Stop />
      </IconButton>
    </Box>
  );
};
