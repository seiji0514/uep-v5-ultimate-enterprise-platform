/**
 * WebSocket 接続 - リアルタイム更新トリガー
 */
import { useEffect, useRef } from 'react';

const getWsUrl = () => {
  const base = import.meta.env.VITE_API_URL || '';
  const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = base ? new URL(base).host : window.location.host;
  return `${proto}//${host}/ws`;
};

export function useWebSocket(onRefresh: () => void, enabled: boolean = true) {
  const onRefreshRef = useRef(onRefresh);
  onRefreshRef.current = onRefresh;

  useEffect(() => {
    if (!enabled) return;
    const url = getWsUrl();
    let ws: WebSocket | null = null;
    let reconnectTimer: ReturnType<typeof setTimeout>;

    const connect = () => {
      try {
        ws = new WebSocket(url);
        ws.onmessage = (e) => {
          try {
            const data = JSON.parse(e.data);
            if (data?.type === 'refresh') {
              onRefreshRef.current();
            }
          } catch {
            // ignore
          }
        };
        ws.onclose = () => {
          reconnectTimer = setTimeout(connect, 5000);
        };
        ws.onerror = () => {
          ws?.close();
        };
      } catch {
        reconnectTimer = setTimeout(connect, 5000);
      }
    };
    connect();
    return () => {
      clearTimeout(reconnectTimer);
      ws?.close();
    };
  }, [enabled]);
}
