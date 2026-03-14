/**
 * Web Vitals レポート
 * 補強スキル: パフォーマンス計測
 */
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

type MetricHandler = (metric: { name: string; value: number }) => void;

function reportToConsole(metric: { name: string; value: number }): void {
  console.log(`[Web Vitals] ${metric.name}:`, metric.value);
}

export function reportWebVitals(handler?: MetricHandler): void {
  const onReport = handler || reportToConsole;
  getCLS(onReport);
  getFID(onReport);
  getFCP(onReport);
  getLCP(onReport);
  getTTFB(onReport);
}
