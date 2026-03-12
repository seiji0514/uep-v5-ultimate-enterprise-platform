/**
 * アプリシェル - サイドバー・AppBar・パンくず・ログアウト
 */
import React, { useState } from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Button,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { Menu as MenuIcon, Dashboard, LocalHospital, Flight, Satellite, Inventory, Storage, Sync, TrendingUp, Logout, Settings } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../contexts/AuthContext';
import { Breadcrumbs } from './Breadcrumbs';
import { GlobalSearch } from '../GlobalSearch';
import { NotificationCenter } from '../NotificationCenter';

const DRAWER_WIDTH = 260;

interface AppShellProps {
  children: React.ReactNode;
}

const navPaths = [
  { key: 'dashboard', icon: <Dashboard />, path: '/' },
  { key: 'medical', icon: <LocalHospital />, path: '/medical' },
  { key: 'aviation', icon: <Flight />, path: '/aviation' },
  { key: 'space', icon: <Satellite />, path: '/space' },
  { key: 'erp', icon: <Inventory />, path: '/erp' },
  { key: 'legacyMigration', icon: <Storage />, path: '/legacy-migration' },
  { key: 'dataIntegration', icon: <Sync />, path: '/data-integration' },
  { key: 'dx', icon: <TrendingUp />, path: '/dx' },
  { key: 'settings', icon: <Settings />, path: '/settings' },
];

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [open, setOpen] = useState(!isMobile);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const { t } = useTranslation();

  const drawerVariant = isMobile ? 'temporary' : 'persistent';
  const contentMarginLeft = isMobile ? 0 : (open ? DRAWER_WIDTH : 0);

  const handleNav = (path: string) => {
    navigate(path);
    if (isMobile) setOpen(false);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }} role="main">
      <Box component="a" href="#main-content" sx={{ position: 'absolute', left: -9999, zIndex: 9999, p: 1, bgcolor: 'primary.main', color: 'white', '&:focus': { left: 8, top: 72 } }} tabIndex={0} aria-label="メインコンテンツへスキップ">メインコンテンツへスキップ</Box>
      <AppBar position="fixed" elevation={0} sx={{ zIndex: (t) => t.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton color="inherit" onClick={() => setOpen(!open)} edge="start" sx={{ mr: 1 }}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            {import.meta.env.VITE_APP_TITLE || '統合基盤プラットフォーム'}
          </Typography>
          <GlobalSearch />
          <NotificationCenter />
          <Typography variant="body2" color="text.secondary" sx={{ display: { xs: 'none', sm: 'block' }, mr: 1 }}>
            {user}
          </Typography>
          <Button color="inherit" startIcon={<Logout />} onClick={() => { logout(); navigate('/login'); }} size="small" aria-label="ログアウト">
            ログアウト
          </Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant={drawerVariant}
        open={open}
        onClose={() => setOpen(false)}
        sx={{
          width: open ? DRAWER_WIDTH : 0,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            boxSizing: 'border-box',
            top: 64,
            backgroundColor: '#0b0c0e',
            borderRight: '1px solid #2d2d2d',
          },
        }}
      >
        <List sx={{ pt: 2 }} role="navigation" aria-label="メインナビゲーション">
          {navPaths.map((item) => (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => handleNav(item.path)}
                aria-current={location.pathname === item.path ? 'page' : undefined}
                sx={{
                  '&.Mui-selected': { backgroundColor: 'rgba(244, 104, 0, 0.15)' },
                }}
              >
                <ListItemIcon sx={{ color: 'primary.main', minWidth: 40 }}>{item.icon}</ListItemIcon>
                <ListItemText primary={t(`nav.${item.key}`)} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>
      <Box
        id="main-content"
        component="main"
        tabIndex={-1}
        sx={{
          flex: '1 1 0',
          display: 'block',
          width: '100%',
          minWidth: 280,
          minHeight: 'calc(100vh - 64px)',
          p: { xs: 2, sm: 3, md: 4 },
          mt: 8,
          ml: contentMarginLeft,
          transition: 'margin 0.2s',
          overflow: 'auto',
          boxSizing: 'border-box',
          bgcolor: '#0f1114',
          backgroundImage: 'linear-gradient(180deg, rgba(244,104,0,0.03) 0%, transparent 120px)',
        }}
        aria-label="メインコンテンツ"
      >
        <Breadcrumbs />
        {children}
      </Box>
    </Box>
  );
};
