/**
 * MSW ハンドラー
 * 開発時のAPIモック（REACT_APP_ENABLE_MSW=true で有効化）
 */
import { http, HttpResponse } from 'msw';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8080';

export const handlers = [
  http.get(`${API_BASE}/api/v1/health`, () => {
    return HttpResponse.json({ status: 'healthy', version: '5.0.0', timestamp: Date.now() / 1000 });
  }),
  http.get(`${API_BASE}/api/v1/mlops/pipelines`, () => {
    return HttpResponse.json([
      {
        id: 'mock-1',
        name: 'サンプルパイプライン',
        description: 'MSWモック',
        stages: [{ name: 'train' }, { name: 'deploy' }],
        status: 'active',
        created_at: new Date().toISOString(),
        created_by: 'developer',
      },
    ]);
  }),
];
