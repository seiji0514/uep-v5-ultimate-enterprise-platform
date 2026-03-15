/**
 * 空データ表示用コンポーネント
 * 統一されたメッセージ表示
 */
import React from 'react';
import { Box, Typography } from '@mui/material';
import { Inbox } from '@mui/icons-material';

interface EmptyStateProps {
  message?: string;
  subMessage?: string;
  icon?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  message = 'データがありません',
  subMessage,
  icon = <Inbox sx={{ fontSize: 48, color: 'text.secondary', opacity: 0.5 }} />,
}) => (
  <Box
    sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      py: 6,
      px: 2,
      textAlign: 'center',
    }}
    role="status"
    aria-label={message}
  >
    {icon}
    <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
      {message}
    </Typography>
    {subMessage && (
      <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
        {subMessage}
      </Typography>
    )}
  </Box>
);
