/**
 * MSW ブラウザワーカー
 * 開発時にのみ有効化（index.tsx で条件付き初期化）
 */
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);
