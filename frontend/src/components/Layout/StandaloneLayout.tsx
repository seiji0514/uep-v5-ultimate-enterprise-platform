/**
 * 単独システム用レイアウト
 * UEP v5.0・統合基盤に属さないシステム専用（サイドバー・UEPナビなし）
 */
import React, { useState } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
} from '@mui/material';
import { Logout } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

export const StandaloneLayout: React.FC<{ children: React.ReactNode; title: string }> = ({
  children,
  title,
}) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => setAnchorEl(event.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);
  const handleLogout = () => {
    handleMenuClose();
    logout();
    navigate('/login');
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static" elevation={0} sx={{ borderBottom: '1px solid', borderColor: 'divider' }}>
        <Toolbar>
          <Typography variant="h6" component="h1" sx={{ flexGrow: 1 }} aria-label={title}>
            {title}
          </Typography>
          <IconButton
            color="inherit"
            onClick={handleMenuOpen}
            aria-label="アカウントメニュー"
            aria-haspopup="true"
            aria-expanded={Boolean(anchorEl)}
          >
            <Avatar sx={{ width: 32, height: 32 }}>
              {(user?.username ?? user?.email ?? 'U').charAt(0).toUpperCase()}
            </Avatar>
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
          >
            <MenuItem disabled>
              <Typography variant="body2" color="text.secondary">
                {user?.username ?? user?.email ?? 'ユーザー'}
              </Typography>
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <Logout fontSize="small" sx={{ mr: 1 }} />
              ログアウト
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {children}
      </Box>
    </Box>
  );
};
