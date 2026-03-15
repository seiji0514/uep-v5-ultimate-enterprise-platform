/**
 * グローバル検索コンポーネント
 * ダッシュボード・サイドバー用のページ検索
 */
import React, { useState, useMemo, useCallback, useRef } from 'react';
import {
  Box,
  TextField,
  InputAdornment,
  Popper,
  Paper,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  IconButton,
} from '@mui/material';
import { Search as SearchIcon, Star, StarBorder, History } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { searchItems, SearchItem } from '../../data/searchItems';
import { useUserSettings } from '../../contexts/UserSettingsContext';

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

function resolvePath(item: SearchItem): string {
  if (item.path === 'industry-unified') return getIndustryUnifiedUrl();
  if (item.path === 'eoh') return getEOHUrl();
  return item.path;
}

function isExternal(item: SearchItem): boolean {
  return Boolean(item.external);
}

interface GlobalSearchProps {
  compact?: boolean;
  onSelect?: () => void;
}

export const GlobalSearch: React.FC<GlobalSearchProps> = ({ compact, onSelect }) => {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const { favorites, recentPages, addFavorite, removeFavorite, isFavorite, addRecentPage } = useUserSettings();

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return searchItems.slice(0, 12);
    return searchItems.filter(
      (item) =>
        item.label.toLowerCase().includes(q) ||
        (item.group && item.group.toLowerCase().includes(q))
    );
  }, [query]);

  const handleSelect = useCallback(
    (item: SearchItem) => {
      const path = resolvePath(item);
      const ext = isExternal(item);
      if (ext) {
        window.location.href = path;
      } else {
        addRecentPage(item.path, item.label);
        navigate(item.path);
      }
      setQuery('');
      setOpen(false);
      onSelect?.();
    },
    [navigate, addRecentPage, onSelect]
  );

  const handleFocus = useCallback((e: React.FocusEvent) => {
    setAnchorEl(e.currentTarget as HTMLElement);
    setOpen(true);
  }, []);

  const handleBlur = useCallback(() => {
    setTimeout(() => setOpen(false), 150);
  }, []);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOpen(false);
        inputRef.current?.blur();
      }
    },
    []
  );

  const toggleFavorite = useCallback(
    (e: React.MouseEvent, path: string) => {
      e.stopPropagation();
      if (isFavorite(path)) removeFavorite(path);
      else addFavorite(path);
    },
    [isFavorite, addFavorite, removeFavorite]
  );

  const showFavorites = !query && favorites.length > 0;
  const showRecent = !query && recentPages.length > 0 && favorites.length < 5;

  return (
    <Box sx={{ flex: compact ? undefined : 1, maxWidth: compact ? 200 : 400 }}>
      <TextField
        inputRef={inputRef}
        size="small"
        placeholder="ページを検索..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={handleFocus}
        onBlur={handleBlur}
        onKeyDown={handleKeyDown}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon fontSize="small" color="action" aria-hidden />
            </InputAdornment>
          ),
        }}
        inputProps={{
          'aria-label': 'ページを検索',
          'aria-autocomplete': 'list',
          'aria-expanded': open,
          role: 'combobox',
        }}
        sx={{
          '& .MuiOutlinedInput-root': {
            backgroundColor: 'action.hover',
            '&:focus-within': { backgroundColor: 'background.paper' },
          },
        }}
      />
      <Popper
        open={open && (results.length > 0 || showFavorites || showRecent)}
        anchorEl={anchorEl}
        placement="bottom-start"
        style={{ zIndex: 1300, width: anchorEl ? Math.max(anchorEl.offsetWidth, 320) : 320 }}
      >
        <Paper
          elevation={8}
          sx={{ mt: 1, maxHeight: 400, overflow: 'auto' }}
          role="listbox"
          aria-label="検索結果"
        >
          {showFavorites && !query && (
            <>
              <Typography variant="caption" color="text.secondary" sx={{ px: 2, pt: 1.5, display: 'block' }}>
                お気に入り
              </Typography>
              {favorites.slice(0, 5).map((path) => {
                const item = searchItems.find((i) => i.path === path);
                if (!item) return null;
                return (
                  <ListItemButton
                    key={path}
                    onClick={() => handleSelect(item)}
                    sx={{ py: 0.5 }}
                    aria-label={`${item.label}へ移動`}
                  >
                    <ListItemIcon sx={{ minWidth: 36 }}>
                      <IconButton
                        size="small"
                        onClick={(e) => toggleFavorite(e, path)}
                        aria-label={`${item.label}のお気に入りを解除`}
                      >
                        <Star fontSize="small" color="primary" />
                      </IconButton>
                    </ListItemIcon>
                    <ListItemText primary={item.label} secondary={item.group} primaryTypographyProps={{ variant: 'body2' }} />
                  </ListItemButton>
                );
              })}
            </>
          )}
          {showRecent && !query && (
            <>
              <Typography variant="caption" color="text.secondary" sx={{ px: 2, pt: 1.5, display: 'block' }}>
                最近使った
              </Typography>
              {recentPages.slice(0, 5).map((p) => (
                <ListItemButton
                  key={p.path}
                  onClick={() => {
                    const item = searchItems.find((i) => i.path === p.path);
                    if (item) handleSelect(item);
                  }}
                  sx={{ py: 0.5 }}
                  aria-label={`${p.label}へ移動`}
                >
                  <ListItemIcon sx={{ minWidth: 36 }}>
                    <History fontSize="small" color="action" />
                  </ListItemIcon>
                  <ListItemText primary={p.label} primaryTypographyProps={{ variant: 'body2' }} />
                </ListItemButton>
              ))}
            </>
          )}
          {results.length > 0 && (
            <>
              <Typography variant="caption" color="text.secondary" sx={{ px: 2, pt: 1.5, display: 'block' }}>
                {query ? '検索結果' : 'すべてのページ'}
              </Typography>
              <List dense disablePadding>
                {results.slice(0, 10).map((item) => (
                  <ListItemButton
                    key={item.path}
                    onClick={() => handleSelect(item)}
                    sx={{ py: 0.5 }}
                    aria-label={`${item.label}へ移動`}
                  >
                    <ListItemIcon sx={{ minWidth: 36 }}>
                      {!isExternal(item) ? (
                        <IconButton
                          size="small"
                          onClick={(e) => toggleFavorite(e, item.path)}
                          aria-label={isFavorite(item.path) ? `${item.label}のお気に入りを解除` : `${item.label}をお気に入りに追加`}
                        >
                          {isFavorite(item.path) ? (
                            <Star fontSize="small" color="primary" />
                          ) : (
                            <StarBorder fontSize="small" color="action" />
                          )}
                        </IconButton>
                      ) : (
                        <Box sx={{ width: 24 }} />
                      )}
                    </ListItemIcon>
                    <ListItemText
                      primary={item.label}
                      secondary={item.group}
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItemButton>
                ))}
              </List>
            </>
          )}
        </Paper>
      </Popper>
    </Box>
  );
};
