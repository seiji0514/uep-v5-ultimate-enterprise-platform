import React from 'react';
import { Box, AppBar, Toolbar, Typography, Container, Button } from '@mui/material';
import { PrecisionManufacturing, Logout } from '@mui/icons-material';
import { ManufacturingPlatformPage } from './components/ManufacturingPlatformPage';
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
          <PrecisionManufacturing sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            製造・IoTプラットフォーム
          </Typography>
          <Button color="inherit" startIcon={<Logout />} onClick={logout}>
            ログアウト
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: 3 }}>
        <ManufacturingPlatformPage />
      </Container>
    </Box>
  );
}

export default App;
