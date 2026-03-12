/**
 * デザインシステム - spacing, typography の定数化
 */
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
} as const;

export const typography = {
  h4: { fontSize: '1.5rem', fontWeight: 600 },
  h5: { fontSize: '1.25rem', fontWeight: 600 },
  h6: { fontSize: '1rem', fontWeight: 600 },
  body1: { fontSize: '1rem' },
  body2: { fontSize: '0.875rem' },
  caption: { fontSize: '0.75rem' },
} as const;

export const layout = {
  drawerWidth: 260,
  appBarHeight: 64,
  contentPadding: { xs: 2, sm: 3 },
} as const;
