/**
 * ローディングスケルトン
 */
import { Box, Skeleton } from '@mui/material';

export function LoadingSkeleton() {
  return (
    <Box sx={{ p: 2 }}>
      <Skeleton variant="text" width="40%" height={40} sx={{ mb: 2 }} />
      <Skeleton variant="rectangular" height={120} sx={{ mb: 2, borderRadius: 1 }} />
      <Skeleton variant="rectangular" height={200} sx={{ borderRadius: 1 }} />
    </Box>
  );
}
