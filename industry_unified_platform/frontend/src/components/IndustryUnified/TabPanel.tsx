/**
 * TabPanel - タブパネル共通コンポーネント
 */
import React from 'react';
import { Box } from '@mui/material';
import type { TabPanelProps } from './types';

export function TabPanel({ children, value, index }: TabPanelProps) {
  return (
    <div
      role="tabpanel"
      id={`domain-panel-${index}`}
      aria-labelledby={`domain-tab-${index}`}
      hidden={value !== index}
      tabIndex={0}
    >
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  );
}
