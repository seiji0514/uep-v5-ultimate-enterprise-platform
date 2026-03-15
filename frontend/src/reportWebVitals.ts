import { ReportHandler } from 'web-vitals';

const reportWebVitals = (onPerfEntry?: ReportHandler) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

/** Web Vitals をコンソール・将来はダッシュボードに送信 */
export const sendToAnalytics: ReportHandler = (metric) => {
  if (process.env.NODE_ENV === 'development') {
    console.debug('[Web Vitals]', metric.name, metric.value, metric.id);
  }
  // 将来: ダッシュボードAPIへ送信
};

export default reportWebVitals;
