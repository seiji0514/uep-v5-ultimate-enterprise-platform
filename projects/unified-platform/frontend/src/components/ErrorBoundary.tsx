/**
 * エラーバウンダリ
 */
import { Component, ErrorInfo, ReactNode } from 'react';
import { Box, Button, Paper, Typography } from '@mui/material';
import { Refresh, BugReport } from '@mui/icons-material';

interface Props { children: ReactNode; }
interface State { hasError: boolean; error: Error | null; }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', p: 3 }}>
          <Paper sx={{ p: 4, maxWidth: 480, textAlign: 'center' }} elevation={0}>
            <BugReport sx={{ fontSize: 48, color: 'error.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>エラーが発生しました</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              {this.state.error?.message}
            </Typography>
            <Button startIcon={<Refresh />} variant="contained" onClick={() => this.setState({ hasError: false, error: null })}>
              再試行
            </Button>
          </Paper>
        </Box>
      );
    }
    return this.props.children;
  }
}
