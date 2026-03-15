/**
 * 最近使ったページのトラッキング
 * ルート変更時に自動で recentPages に追加
 */
import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { useUserSettings } from '../../contexts/UserSettingsContext';
import { searchItems } from '../../data/searchItems';

export const RecentPageTracker: React.FC = () => {
  const location = useLocation();
  const { addRecentPage } = useUserSettings();
  const isFirst = useRef(true);

  useEffect(() => {
    if (isFirst.current) {
      isFirst.current = false;
      return;
    }
    const path = location.pathname;
    if (path === '/login') return;
    const item = searchItems.find((i) => i.path === path && !i.external);
    if (item) {
      addRecentPage(item.path, item.label);
    }
  }, [location.pathname, addRecentPage]);

  return null;
};
