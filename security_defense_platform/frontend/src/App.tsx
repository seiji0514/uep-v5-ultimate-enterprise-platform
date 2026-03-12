import React from 'react';
import { Box, AppBar, Toolbar, Typography, Container, Button } from '@mui/material';
import { Shield, Logout } from '@mui/icons-material';
import { SecurityDefensePlatformPage } from './components/SecurityDefensePlatformPage';
import { LoginPage } from './components/LoginPage';
import { useAuth } from './contexts/AuthContext';

function App() {
  const { isAuthenticated, isLoading, logout } = useAuth();

  if (isLoading) {
    return null;
  }

  if (!isAuthenticated) {
    return <LoginPage />;
  }

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static">
        <Toolbar>
          <Shield sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            統合セキュリティ・防衛プラットフォーム
          </Typography>
          <Button color="inherit" startIcon={<Logout />} onClick={logout}>
            ログアウト
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: 3 }}>
        <SecurityDefensePlatformPage />
      </Container>
    </Box>
  );
}

export default App;
