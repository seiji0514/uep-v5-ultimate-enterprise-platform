import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

const proxyTarget = process.env.VITE_PROXY_TARGET || 'http://127.0.0.1:8000';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: '統合基盤プラットフォーム',
        short_name: '統合基盤',
        description: '統合基盤プラットフォーム',
        theme_color: '#1976d2',
        icons: [{ src: '/favicon.ico', sizes: '48x48', type: 'image/x-icon', purpose: 'any' }],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
        maximumFileSizeToCacheInBytes: 3 * 1024 * 1024, // 3MB（メインバンドル 2.3MB 対応）
      },
    }),
  ],
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': { target: proxyTarget, changeOrigin: true },
      '/health': { target: proxyTarget, changeOrigin: true },
      '/ready': { target: proxyTarget, changeOrigin: true },
      '/ws': { target: proxyTarget.replace('http', 'ws'), ws: true },
    },
  },
});
