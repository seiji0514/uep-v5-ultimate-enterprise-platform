/**
 * TanStack React Query クライアント
 * API キャッシュ・再検証・オフライン対応の拡張
 */
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 2 * 60 * 1000, // 2分（キャッシュ有効期間）
      gcTime: 10 * 60 * 1000, // 10分（旧 cacheTime、未使用時の保持）
      retry: 2,
      refetchOnWindowFocus: true, // ウィンドウフォーカス時に再検証
      refetchOnReconnect: true, // オフライン復帰時に再検証
    },
    mutations: {
      retry: 0,
    },
  },
});
