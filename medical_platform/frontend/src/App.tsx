import React from 'react';
import { Box, AppBar, Toolbar, Typography, Container, Button } from '@mui/material';
import { LocalHospital, Logout } from '@mui/icons-material';
import { MedicalPlatformPage } from './components/MedicalPlatformPage';
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
          <LocalHospital sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            医療・ヘルスケアプラットフォーム
          </Typography>
          <Button color="inherit" startIcon={<Logout />} onClick={logout}>
            ログアウト
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: 3 }}>
        <MedicalPlatformPage />
      </Container>
    </Box>
  );
}

export default App;
