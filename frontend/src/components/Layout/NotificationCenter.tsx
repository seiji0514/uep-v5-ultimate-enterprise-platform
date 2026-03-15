/**
 * 通知センターコンポーネント
 * インシデント・アラートの一覧表示
 */
import React, { useState } from 'react';
import {
  IconButton,
  Badge,
  Popover,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Typography,
  Button,
  Box,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  NotificationsNone,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  CheckCircle as CheckIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useNotifications } from '../../contexts/NotificationContext';
import type { Notification, NotificationSeverity } from '../../contexts/NotificationContext';

const severityConfig: Record<NotificationSeverity, { icon: React.ReactNode; color: 'error' | 'warning' | 'info' | 'success' }> = {
  error: { icon: <ErrorIcon fontSize="small" />, color: 'error' },
  warning: { icon: <WarningIcon fontSize="small" />, color: 'warning' },
  info: { icon: <InfoIcon fontSize="small" />, color: 'info' },
  success: { icon: <CheckIcon fontSize="small" />, color: 'success' },
};

function formatTime(d: Date): string {
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  if (diff < 60000) return 'たった今';
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分前`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}時間前`;
  return d.toLocaleDateString('ja-JP', { month: 'short', day: 'numeric' });
}

export const NotificationCenter: React.FC = () => {
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const { notifications, unreadCount, markAsRead, markAllAsRead, removeNotification, clearAll } = useNotifications();
  const navigate = useNavigate();

  const handleOpen = (e: React.MouseEvent<HTMLElement>) => setAnchorEl(e.currentTarget);
  const handleClose = () => setAnchorEl(null);

  const handleItemClick = (n: Notification) => {
    markAsRead(n.id);
    if (n.link) {
      navigate(n.link);
      handleClose();
    }
  };

  const open = Boolean(anchorEl);

  return (
    <>
      <IconButton
        color="inherit"
        onClick={handleOpen}
        aria-label={`通知${unreadCount > 0 ? `（未読${unreadCount}件）` : ''}`}
        aria-haspopup="true"
        aria-expanded={open}
        sx={{ '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main' } }}
      >
        <Badge badgeContent={unreadCount} color="error">
          {unreadCount > 0 ? <NotificationsIcon /> : <NotificationsNone />}
        </Badge>
      </IconButton>
      <Popover
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        slotProps={{ paper: { sx: { width: 360, maxHeight: 480 } } }}
        aria-label="通知一覧"
      >
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="subtitle1" fontWeight={600}>
            通知
          </Typography>
          {notifications.length > 0 && (
            <Box sx={{ display: 'flex', gap: 0.5 }}>
              {unreadCount > 0 && (
                <Button size="small" onClick={markAllAsRead}>
                  すべて既読
                </Button>
              )}
              <Button size="small" color="inherit" onClick={clearAll}>
                クリア
              </Button>
            </Box>
          )}
        </Box>
        <List dense disablePadding>
          {notifications.length === 0 ? (
            <ListItem disablePadding>
              <ListItemText
                primary="通知はありません"
                primaryTypographyProps={{ variant: 'body2', color: 'text.secondary' }}
                sx={{ py: 3, px: 2, textAlign: 'center' }}
              />
            </ListItem>
          ) : (
            notifications.slice(0, 20).map((n) => {
              const config = severityConfig[n.severity];
              return (
                <ListItem
                  key={n.id}
                  button
                  onClick={() => handleItemClick(n)}
                  sx={{
                    opacity: n.read ? 0.8 : 1,
                    borderLeft: n.read ? 'none' : '3px solid',
                    borderColor: `${config.color}.main`,
                  }}
                  alignItems="flex-start"
                >
                  <Box sx={{ mr: 1, mt: 0.5, color: `${config.color}.main` }}>{config.icon}</Box>
                  <ListItemText
                    primary={n.title}
                    secondary={
                      <>
                        {n.message && (
                          <Typography variant="body2" color="text.secondary" component="span" sx={{ display: 'block' }}>
                            {n.message}
                          </Typography>
                        )}
                        <Typography variant="caption" color="text.secondary" component="span">
                          {formatTime(n.timestamp)}
                        </Typography>
                      </>
                    }
                    primaryTypographyProps={{ variant: 'body2', fontWeight: n.read ? 400 : 600 }}
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      size="small"
                      onClick={(e) => {
                        e.stopPropagation();
                        removeNotification(n.id);
                      }}
                      aria-label="通知を削除"
                    >
                      ×
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              );
            })
          )}
        </List>
      </Popover>
    </>
  );
};
