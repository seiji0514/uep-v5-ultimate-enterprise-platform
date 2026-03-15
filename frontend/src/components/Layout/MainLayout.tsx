/**
 * メインレイアウトコンポーネント
 * 統合ダッシュボードUI・4〜5分割（企業向けデモ）
 * サイドバー折りたたみ・パンくず・アクセシビリティ対応
 */
import React, { useState, useEffect } from 'react';
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
  Collapse,
  Tooltip,
  Dialog,
  DialogContent,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Search as SearchIcon,
  ChevronLeft,
  ChevronRight,
  Dashboard,
  Cloud,
  Construction,
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
  ExpandLess,
  ExpandMore,
  FolderSpecial,
  BugReport,
  Work,
  PrecisionManufacturing,
  AccountBalance,
  Bolt,
  Inventory,
  Hub,
  ArrowForward,
  Domain,
  Store,
  School,
  Gavel,
  LocalShipping,
  LocalHospital,
  SmartToy,
  Traffic,
  Assignment,
  DarkMode,
  LightMode,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useAutoPlay } from '../../contexts/AutoPlayContext';
import { useUserSettings } from '../../contexts/UserSettingsContext';
import { Breadcrumbs } from './Breadcrumbs';
import { AutoPlayBar } from './AutoPlayBar';
import { GlobalSearch } from './GlobalSearch';
import { NotificationCenter } from './NotificationCenter';
import { RecentPageTracker } from './RecentPageTracker';

const DRAWER_WIDTH = 320;
const DRAWER_WIDTH_COLLAPSED = 72;
const getIndustryUnifiedUrl = () => {
  const base = process.env.REACT_APP_INDUSTRY_UNIFIED_URL || 'http://localhost:3010';
  const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;
  return token ? `${base}?token=${encodeURIComponent(token)}` : base;
};

const getEOHUrl = () => {
  const base = process.env.REACT_APP_EOH_URL || 'http://localhost:3020';
  const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;
  return token ? `${base}?token=${encodeURIComponent(token)}` : base;
};

interface NavItem {
  text: string;
  icon: React.ReactNode;
  path: string;
  external?: boolean;
}

interface NavGroup {
  title: string;
  icon: React.ReactNode;
  items: NavItem[];
}

// 4〜5分割（企業向けデモ）
const navGroups: NavGroup[] = [
  {
    title: '統合基盤モジュール（6モジュール）',
    icon: <Hub />,
    items: [
      { text: '6モジュール概要', icon: <Layers />, path: '/integrated-modules' },
      { text: '製造・MLOps', icon: <PrecisionManufacturing />, path: '/manufacturing' },
      { text: '障害者雇用', icon: <Work />, path: '/inclusive-work' },
      { text: '医療', icon: <LocalHospital />, path: '/medical' },
      { text: '金融', icon: <AccountBalance />, path: '/fintech' },
      { text: '契約ワークフロー', icon: <Assignment />, path: '/contract-workflow' },
      { text: '物流・サプライチェーン', icon: <LocalShipping />, path: '/supply-chain' },
      { text: '現場AIエージェント', icon: <SmartToy />, path: '/field-agent' },
    ],
  },
  {
    title: 'インフラ基盤',
    icon: <Cloud />,
    items: [
      { text: 'クラウドインフラ', icon: <Cloud />, path: '/cloud-infra' },
      { text: 'インフラ構築専用', icon: <Construction />, path: '/infra-builder' },
    ],
  },
  {
    title: 'AI・ML',
    icon: <Science />,
    items: [
      { text: 'MLOps', icon: <Science />, path: '/mlops' },
      { text: '生成AI', icon: <Psychology />, path: '/generative-ai' },
      { text: '最適化・精度向上', icon: <Star />, path: '/optimization' },
      { text: 'AI支援開発', icon: <Build />, path: '/ai-dev' },
    ],
  },
  {
    title: '開発・運用',
    icon: <Build />,
    items: [
      { text: 'IDOP', icon: <Build />, path: '/idop' },
    ],
  },
  {
    title: 'プラットフォーム拡張',
    icon: <Public />,
    items: [
      { text: 'プラットフォーム (Level 2)', icon: <Layers />, path: '/platform' },
      { text: 'エコシステム (Level 3)', icon: <Groups />, path: '/ecosystem' },
      { text: 'インダストリー (Level 4)', icon: <Star />, path: '/industry-leader' },
      { text: 'グローバル (Level 5)', icon: <Public />, path: '/global-enterprise' },
    ],
  },
  {
    title: 'ビジネス領域',
    icon: <Build />,
    items: [
      { text: 'ERP（統合基幹）', icon: <Inventory />, path: '/erp' },
      { text: '製造・IoT', icon: <PrecisionManufacturing />, path: '/manufacturing' },
      { text: '金融・FinTech', icon: <AccountBalance />, path: '/fintech' },
      { text: 'エネルギー', icon: <Bolt />, path: '/energy' },
      { text: '医療', icon: <LocalHospital />, path: '/medical' },
      { text: '交通', icon: <Traffic />, path: '/traffic' },
      { text: '公共・官公庁', icon: <Domain />, path: '/public-sector' },
      { text: '小売・EC', icon: <Store />, path: '/retail' },
      { text: '教育', icon: <School />, path: '/education' },
      { text: '法務', icon: <Gavel />, path: '/legal' },
      { text: 'サプライチェーン', icon: <LocalShipping />, path: '/supply-chain' },
      { text: '産業統合プラットフォーム', icon: <Hub />, path: 'industry-unified', external: true },
      { text: '企業横断オペレーション基盤', icon: <Hub />, path: 'eoh', external: true },
    ],
  },
];

const topItems: NavItem[] = [
  { text: 'プロジェクト一覧', icon: <FolderSpecial />, path: '/projects' },
  { text: 'ダッシュボード', icon: <Dashboard />, path: '/' },
];

const bottomItems: NavItem[] = [
  { text: '個人会計', icon: <AccountBalance />, path: '/personal-accounting' },
  { text: 'テスト', icon: <BugReport />, path: '/tests' },
  { text: 'Chaos Engineering', icon: <Build />, path: '/chaos' },
  { text: 'GraphQL', icon: <Build />, path: '/graphql' },
  { text: '設定', icon: <Settings />, path: '/settings' },
];

const INTEGRATED_GROUP_TITLE = '統合基盤モジュール（6モジュール）';

export const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [drawerCollapsed, setDrawerCollapsed] = useState(false);
  const [integratedOnly, setIntegratedOnly] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>({
    '統合基盤モジュール（6モジュール）': true,
    'インフラ基盤': true,
    'AI・ML': true,
    '監視・セキュリティ': true,
    '開発・運用': true,
    'プラットフォーム拡張': true,
    'ビジネス領域': true,
  });
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const autoPlay = useAutoPlay();
  const { themeMode, toggleTheme } = useUserSettings();

  useEffect(() => {
    if (!autoPlay?.isAutoPlaying || !autoPlay?.togglePause) return;
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' && !['INPUT', 'TEXTAREA', 'BUTTON'].includes((e.target as HTMLElement)?.tagName)) {
        e.preventDefault();
        autoPlay.togglePause();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [autoPlay?.isAutoPlaying, autoPlay?.togglePause]);

  const handleDrawerToggle = () => setMobileOpen(!mobileOpen);
  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => setAnchorEl(event.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);

  const handleGroupToggle = (title: string) => {
    setOpenGroups((prev) => ({ ...prev, [title]: !prev[title] }));
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleMenuClose();
  };

  const nav = (path: string) => {
    navigate(path);
    setMobileOpen(false);
  };

  const drawerWidth = drawerCollapsed ? DRAWER_WIDTH_COLLAPSED : DRAWER_WIDTH;

  const drawer = (
    <div role="navigation" aria-label="メインメニュー">
      <Toolbar sx={{ justifyContent: drawerCollapsed ? 'center' : 'space-between', minHeight: 64 }}>
        {!drawerCollapsed && (
          <Typography variant="h6" noWrap component="div">
            UEP v5.0
          </Typography>
        )}
        <IconButton
          onClick={() => setDrawerCollapsed(!drawerCollapsed)}
          aria-label={drawerCollapsed ? 'サイドバーを展開' : 'サイドバーを折りたたむ'}
          sx={{ display: { xs: 'none', sm: 'flex' }, '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main' } }}
        >
          {drawerCollapsed ? <ChevronRight /> : <ChevronLeft />}
        </IconButton>
      </Toolbar>
      <Divider />
      <List dense>
        {topItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => nav(item.path)}
              aria-label={item.text}
              sx={{ '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main' } }}
            >
              <ListItemIcon sx={{ minWidth: 36 }} aria-hidden>{item.icon}</ListItemIcon>
              {!drawerCollapsed && (
                <ListItemText primary={item.text} primaryTypographyProps={{ variant: 'body2' }} />
              )}
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider sx={{ my: 1 }} />
      <List dense sx={{ display: drawerCollapsed ? 'none' : 'block' }}>
        {(integratedOnly ? navGroups.filter((g) => g.title === INTEGRATED_GROUP_TITLE) : navGroups).map((group) => (
          <React.Fragment key={group.title}>
            <ListItemButton
              onClick={() => handleGroupToggle(group.title)}
              aria-expanded={openGroups[group.title]}
              aria-label={`${group.title}メニュー`}
              sx={{ '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main' } }}
            >
              <ListItemIcon sx={{ minWidth: 36 }} aria-hidden>{group.icon}</ListItemIcon>
              <ListItemText primary={group.title} primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }} />
              {openGroups[group.title] ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
            <Collapse in={openGroups[group.title]} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {group.items.map((item) => (
                  <ListItem key={item.path} disablePadding sx={{ pl: 3 }}>
                    <ListItemButton
                      selected={!item.external && location.pathname === item.path}
                      onClick={() => {
                        if (item.external) {
                          const url = item.path === 'industry-unified' ? getIndustryUnifiedUrl() : item.path === 'eoh' ? getEOHUrl() : item.path;
                          window.location.href = url;
                          setMobileOpen(false);
                        } else {
                          nav(item.path);
                        }
                      }}
                      aria-label={item.text}
                      sx={{ '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main' } }}
                    >
                      <ListItemIcon sx={{ minWidth: 32 }} aria-hidden>{item.icon}</ListItemIcon>
                      <ListItemText primary={item.text} primaryTypographyProps={{ variant: 'body2' }} />
                      {item.external && <ArrowForward sx={{ fontSize: 14, ml: 0.5, opacity: 0.6 }} />}
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Collapse>
          </React.Fragment>
        ))}
      </List>
      <Divider sx={{ my: 1 }} />
      <List dense>
        {(integratedOnly ? bottomItems.filter((i) => i.text === '設定') : bottomItems).map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => nav(item.path)}
              aria-label={item.text}
              sx={{ '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main' } }}
            >
              <ListItemIcon sx={{ minWidth: 36 }} aria-hidden>{item.icon}</ListItemIcon>
              {!drawerCollapsed && (
                <ListItemText primary={item.text} primaryTypographyProps={{ variant: 'body2' }} />
              )}
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
        sx={{ width: { sm: `calc(100% - ${drawerWidth}px)` }, ml: { sm: `${drawerWidth}px` } }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
            aria-label="メニューを開く"
          >
            <MenuIcon />
          </IconButton>
          <Box sx={{ flex: 1, display: { xs: 'none', md: 'flex' }, mr: 2, maxWidth: 400 }}>
            <GlobalSearch />
          </Box>
          <Tooltip title="検索">
            <IconButton
              color="inherit"
              onClick={() => setSearchOpen(true)}
              sx={{ display: { xs: 'flex', md: 'none' }, mr: 0.5 }}
              aria-label="検索を開く"
            >
              <SearchIcon />
            </IconButton>
          </Tooltip>
          <Dialog open={searchOpen} onClose={() => setSearchOpen(false)} maxWidth="sm" fullWidth PaperProps={{ sx: { mt: 6 } }}>
            <DialogContent>
              <GlobalSearch compact onSelect={() => setSearchOpen(false)} />
            </DialogContent>
          </Dialog>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: { md: 0 }, fontSize: { xs: '0.9rem', sm: '1rem' }, display: { xs: 'block', md: 'none' } }}>
            UEP v5.0
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Tooltip title={themeMode === 'dark' ? 'ライトモードに切替' : 'ダークモードに切替'}>
              <IconButton
                color="inherit"
                onClick={toggleTheme}
                aria-label={themeMode === 'dark' ? 'ライトモードに切替' : 'ダークモードに切替'}
                sx={{ '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main' } }}
              >
                {themeMode === 'dark' ? <LightMode /> : <DarkMode />}
              </IconButton>
            </Tooltip>
            <NotificationCenter />
            <Tooltip title={integratedOnly ? 'すべて表示に切替' : '統合基盤のみ表示に切替'}>
              <IconButton
                onClick={() => setIntegratedOnly(!integratedOnly)}
                size="small"
                color={integratedOnly ? 'primary' : 'default'}
                aria-label={integratedOnly ? 'すべて表示' : '統合基盤のみ表示'}
                sx={{ '&:focus-visible': { outline: '2px solid', outlineColor: 'primary.main' } }}
              >
                <Layers />
              </IconButton>
            </Tooltip>
            <Typography variant="body2">{user?.full_name || user?.username}</Typography>
            <IconButton
              onClick={handleMenuOpen}
              size="small"
              aria-label="アカウントメニュー"
              aria-haspopup="true"
              aria-expanded={Boolean(anchorEl)}
            >
              <Avatar sx={{ width: 32, height: 32 }}>{user?.username?.charAt(0).toUpperCase()}</Avatar>
            </IconButton>
            <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
              <MenuItem onClick={() => { nav('/profile'); handleMenuClose(); }}>
                <AccountCircle sx={{ mr: 1 }} /> プロフィール
              </MenuItem>
              <MenuItem onClick={handleLogout}>
                <Logout sx={{ mr: 1 }} /> ログアウト
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{ display: { xs: 'block', sm: 'none' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DRAWER_WIDTH } }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{ display: { xs: 'none', sm: 'block' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, transition: 'width 0.2s' } }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}>
        <RecentPageTracker />
        <Toolbar />
        <Breadcrumbs />
        {children}
      </Box>
      <AutoPlayBar />
    </Box>
  );
};
