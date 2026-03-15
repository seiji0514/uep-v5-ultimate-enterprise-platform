/**
 * ローディングスケルトン
 * 全API呼び出しでスケルトン/スピナーを統一
 */
import React from 'react';
import { Box, Skeleton } from '@mui/material';

interface LoadingSkeletonProps {
  variant?: 'table' | 'card' | 'list' | 'form';
  rows?: number;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  variant = 'list',
  rows = 5,
}) => {
  if (variant === 'table') {
    return (
      <Box sx={{ p: 2 }} aria-busy="true" aria-label="読み込み中">
        <Skeleton variant="rectangular" height={40} sx={{ mb: 1 }} />
        {Array.from({ length: rows }).map((_, i) => (
          <Skeleton key={i} variant="rectangular" height={36} sx={{ mb: 0.5 }} />
        ))}
      </Box>
    );
  }

  if (variant === 'card') {
    return (
      <Box sx={{ p: 2 }} aria-busy="true" aria-label="読み込み中">
        <Skeleton variant="rectangular" height={120} sx={{ borderRadius: 1, mb: 2 }} />
        <Skeleton variant="rectangular" height={120} sx={{ borderRadius: 1, mb: 2 }} />
        <Skeleton variant="rectangular" height={120} sx={{ borderRadius: 1 }} />
      </Box>
    );
  }

  if (variant === 'form') {
    return (
      <Box sx={{ p: 2 }} aria-busy="true" aria-label="読み込み中">
        <Skeleton variant="rectangular" height={56} sx={{ mb: 2 }} />
        <Skeleton variant="rectangular" height={56} sx={{ mb: 2 }} />
        <Skeleton variant="rectangular" height={56} sx={{ mb: 2 }} />
        <Skeleton variant="rectangular" height={40} sx={{ width: 120 }} />
      </Box>
    );
  }

  if (variant === 'list') {
    return (
      <Box sx={{ p: 2 }} aria-busy="true" aria-label="読み込み中">
        {Array.from({ length: rows }).map((_, i) => (
          <Box key={i} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Skeleton variant="circular" width={40} height={40} sx={{ mr: 2 }} />
            <Box sx={{ flex: 1 }}>
              <Skeleton variant="text" width="80%" />
              <Skeleton variant="text" width="50%" />
            </Box>
          </Box>
        ))}
      </Box>
    );
  }

  return null;
};
