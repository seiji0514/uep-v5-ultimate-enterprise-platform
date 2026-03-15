/**
 * 産業統合プラットフォーム 共通ユーティリティ
 */

const LEARN_PROGRESS_KEY = 'industry_unified_learn_progress';

export function loadLearnProgress(): Record<string, number> {
  try {
    const raw = localStorage.getItem(LEARN_PROGRESS_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

export function saveLearnProgress(progress: Record<string, number>) {
  try {
    localStorage.setItem(LEARN_PROGRESS_KEY, JSON.stringify(progress));
  } catch {
    /* ignore */
  }
}

export const getSeverityColor = (s: string) => {
  const v = (s || '').toLowerCase();
  return ['高', 'critical', 'high'].includes(v) ? 'error' : ['中', 'medium'].includes(v) ? 'warning' : 'info';
};

export const getStatusColor = (s: string) =>
  s === '要確認' || s === '監視中' ? 'warning' : s === '完了' ? 'success' : 'default';

export const getRiskColor = (level: string) =>
  ['高', 'high'].includes(level || '') ? 'error' : level === '中' ? 'warning' : 'success';
