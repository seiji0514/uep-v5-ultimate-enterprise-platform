/**
 * エラーバウンダリ
 * 子コンポーネントのエラーを捕捉し、白画面を防ぐ
 */
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({ errorInfo });
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      return (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh',
            p: 2,
            bgcolor: '#f5f5f5',
          }}
        >
          <Paper sx={{ p: 4, maxWidth: 600 }}>
            <Typography variant="h5" color="error" gutterBottom>
              エラーが発生しました
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              {this.state.error.message}
            </Typography>
            {this.state.errorInfo && (
              <Typography
                variant="body2"
                component="pre"
                sx={{
                  p: 2,
                  bgcolor: '#fafafa',
                  overflow: 'auto',
                  fontSize: 12,
                  mb: 2,
                }}
              >
                {this.state.errorInfo.componentStack}
              </Typography>
            )}
            <Button variant="contained" onClick={this.handleRetry}>
              再試行
            </Button>
          </Paper>
        </Box>
      );
    }

    return this.props.children;
  }
}
