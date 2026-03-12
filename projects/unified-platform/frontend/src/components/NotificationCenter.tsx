/**
 * 通知センター - アラート一覧・既読管理
 */
import React, { useState, useEffect } from 'react';
import { IconButton, Popover, List, ListItem, ListItemText, Typography, Box, Chip } from '@mui/material';
import { Notifications } from '@mui/icons-material';
import { unifiedApi } from '../api/unified';

export const NotificationCenter: React.FC = () => {
  const [anchor, setAnchor] = useState<HTMLElement | null>(null);
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    if (anchor) {
      unifiedApi.notifications.list().then(r => setItems(r.data.items || [])).catch(() => {});
    }
  }, [anchor]);

  const handleMarkRead = (id: number) => {
    unifiedApi.notifications.markRead(id).then(() => {
      setItems(prev => prev.map(it => it.id === id ? { ...it, read: true } : it));
    }).catch(() => {});
  };

  const unreadCount = items.filter(i => !i.read).length;

  return (
    <>
      <IconButton color="inherit" onClick={(e) => setAnchor(e.currentTarget)} aria-label={`通知${unreadCount ? `（${unreadCount}件未読）` : ''}`}>
        <Notifications />
        {unreadCount > 0 && (
          <Box component="span" sx={{ position: 'absolute', top: 4, right: 4, width: 8, height: 8, borderRadius: '50%', bgcolor: 'error.main' }} />
        )}
      </IconButton>
      <Popover
        open={!!anchor}
        anchorEl={anchor}
        onClose={() => setAnchor(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <Box sx={{ p: 2, minWidth: 320, maxHeight: 400, overflow: 'auto' }}>
          <Typography variant="subtitle1" fontWeight={600} gutterBottom>通知</Typography>
          {items.length === 0 ? (
            <Typography variant="body2" color="text.secondary">通知はありません</Typography>
          ) : (
            <List dense>
              {items.map((it) => (
                <ListItem
                  key={it.id}
                  sx={{ opacity: it.read ? 0.7 : 1, borderBottom: '1px solid', borderColor: 'divider' }}
                  secondaryAction={!it.read && <Chip label="既読" size="small" onClick={() => handleMarkRead(it.id)} />}
                >
                  <ListItemText primary={it.title} secondary={it.body || it.created_at} />
                </ListItem>
              ))}
            </List>
          )}
        </Box>
      </Popover>
    </>
  );
};
