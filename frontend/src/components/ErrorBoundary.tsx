/**
 * グローバルエラーバウンダリ
 * 予期しないエラーをキャッチし、ユーザーフレンドリーなUIを表示
 */
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Box, Button, Paper, Typography } from '@mui/material';
import { Refresh, BugReport } from '@mui/icons-material';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '60vh',
            p: 3,
          }}
        >
          <Paper
            sx={{
              p: 4,
              maxWidth: 480,
              textAlign: 'center',
            }}
            elevation={0}
          >
            <BugReport sx={{ fontSize: 48, color: 'error.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              エラーが発生しました
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              予期しないエラーが発生しました。ページを再読み込みするか、しばらくしてから再度お試しください。
            </Typography>
            <Button
              variant="contained"
              startIcon={<Refresh />}
              onClick={this.handleRetry}
              aria-label="再試行"
            >
              再試行
            </Button>
          </Paper>
        </Box>
      );
    }
    return this.props.children;
  }
}
