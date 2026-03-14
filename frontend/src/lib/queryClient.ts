/**
 * TanStack React Query クライアント
 * 補強スキル: API キャッシュ、再検証、オフライン
 */
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1分
      retry: 2,
    },
  },
});
