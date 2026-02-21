/**
 * メインレイアウトコンポーネント
 */
import React, { useState } from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Avatar,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  Security,
  Cloud,
  Science,
  Psychology,
  Build,
  Settings,
  Logout,
  AccountCircle,
  Groups,
  Public,
  Star,
  Layers,
  Business,
  BugReport,
  Accessibility,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const DRAWER_WIDTH = 240;

interface NavItem {
  text: string;
  icon: React.ReactNode;
  path: string;
}

const menuItems: NavItem[] = [
  { text: 'ダッシュボード', icon: <Dashboard />, path: '/' },
  { text: 'MLOps', icon: <Science />, path: '/mlops' },
  { text: '生成AI', icon: <Psychology />, path: '/generative-ai' },
  { text: 'セキュリティコマンドセンター', icon: <Security />, path: '/security-center' },
  { text: 'クラウドインフラ', icon: <Cloud />, path: '/cloud-infra' },
  { text: 'IDOP', icon: <Build />, path: '/idop' },
  { text: 'AI支援開発', icon: <Build />, path: '/ai-dev' },
  { text: 'Chaos Engineering', icon: <BugReport />, path: '/chaos' },
  { text: 'インクルーシブ雇用AI', icon: <Accessibility />, path: '/inclusive-work' },
  { text: 'GraphQL', icon: <Build />, path: '/graphql' },
  { text: 'WebAssembly', icon: <Build />, path: '/wasm' },
  { text: '統合ビジネスプラットフォーム', icon: <Business />, path: '/unified-business' },
  { text: 'プラットフォーム (Level 2)', icon: <Layers />, path: '/platform' },
  { text: 'エコシステム (Level 3)', icon: <Groups />, path: '/ecosystem' },
  { text: 'インダストリー (Level 4)', icon: <Star />, path: '/industry-leader' },
  { text: 'グローバル (Level 5)', icon: <Public />, path: '/global-enterprise' },
  { text: '設定', icon: <Settings />, path: '/settings' },
];

export const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleMenuClose();
  };

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          UEP v5.0
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => {
                navigate(item.path);
                setMobileOpen(false);
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${DRAWER_WIDTH}px)` },
          ml: { sm: `${DRAWER_WIDTH}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            次世代エンタープライズ統合プラットフォーム v5.0 (UEP v5.0) - レベル5グローバルエンタープライズ対応システム
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2">{user?.full_name || user?.username}</Typography>
            <IconButton onClick={handleMenuOpen} size="small">
              <Avatar sx={{ width: 32, height: 32 }}>
                {user?.username?.charAt(0).toUpperCase()}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
            >
              <MenuItem onClick={() => { navigate('/profile'); handleMenuClose(); }}>
                <AccountCircle sx={{ mr: 1 }} />
                プロフィール
              </MenuItem>
              <MenuItem onClick={handleLogout}>
                <Logout sx={{ mr: 1 }} />
                ログアウト
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: DRAWER_WIDTH }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DRAWER_WIDTH },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DRAWER_WIDTH },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${DRAWER_WIDTH}px)` },
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};
