/**
 * 全ドメイン横断検索
 */
import React, { useState, useEffect, useRef } from 'react';
import { TextField, Popper, Paper, List, ListItemButton, ListItemText, Box } from '@mui/material';
import { Search } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { unifiedApi } from '../api/unified';

export const GlobalSearch: React.FC = () => {
  const [q, setQ] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [anchor, setAnchor] = useState<HTMLElement | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const t = setTimeout(() => {
      if (q.trim().length >= 1) {
        unifiedApi.search(q.trim(), 10).then(r => {
          setResults(r.data.items || []);
          setOpen(true);
        }).catch(() => setResults([]));
      } else {
        setResults([]);
        setOpen(false);
      }
    }, 200);
    return () => clearTimeout(t);
  }, [q]);

  const handleSelect = (item: any) => {
    if (item.domain === 'medical') navigate(`/medical`);
    else if (item.domain === 'aviation') navigate(`/aviation`);
    else if (item.domain === 'space') navigate(`/space`);
    setOpen(false);
    setQ('');
  };

  return (
    <Box ref={containerRef} sx={{ display: 'flex', alignItems: 'center', mr: 1 }}>
      <TextField
        size="small"
        placeholder="検索..."
        value={q}
        onChange={(e) => setQ(e.target.value)}
        onFocus={() => setAnchor(containerRef.current)}
        onBlur={() => setTimeout(() => setOpen(false), 150)}
        InputProps={{
          startAdornment: <Search sx={{ mr: 1, color: 'text.secondary', fontSize: 20 }} />,
          sx: { bgcolor: 'rgba(255,255,255,0.08)', borderRadius: 1, '& fieldset': { border: 'none' } },
        }}
        sx={{ width: 180 }}
        aria-label="全ドメイン横断検索"
      />
      <Popper open={open && results.length > 0} anchorEl={anchor} placement="bottom-start" sx={{ zIndex: 1400 }}>
        <Paper elevation={8} sx={{ mt: 1, minWidth: 280, maxHeight: 300, overflow: 'auto' }}>
          <List dense>
            {results.map((item, i) => (
              <ListItemButton key={`${item.domain}-${item.id}-${i}`} onClick={() => handleSelect(item)}>
                <ListItemText primary={item.label} secondary={`${item.domain} / ${item.type}`} />
              </ListItemButton>
            ))}
          </List>
        </Paper>
      </Popper>
    </Box>
  );
};
