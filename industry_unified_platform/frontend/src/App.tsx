import React, { useState, useEffect } from 'react';
import { Box, AppBar, Toolbar, Typography, Container, Button, Chip } from '@mui/material';
import { Business, Logout, Link } from '@mui/icons-material';
import { IndustryUnifiedPlatformPage } from './components/IndustryUnifiedPlatformPage';
import { LoginPage } from './components/LoginPage';
import { useAuth } from './contexts/AuthContext';

function App() {
  const { isAuthenticated, isLoading, logout } = useAuth();
  const [ssoOrigin, setSsoOrigin] = useState<string | null>(null);
  useEffect(() => {
    setSsoOrigin(sessionStorage.getItem('industry_sso_origin'));
  }, []);

  if (isLoading) return null;
  if (!isAuthenticated) return <LoginPage />;

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static">
        <Toolbar sx={{ minHeight: { xs: 48, sm: 64 }, px: { xs: 1, sm: 2 } }}>
          <Business sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            産業統合プラットフォーム
          </Typography>
          {ssoOrigin && (
            <Chip icon={<Link />} label="UEP連携" size="small" sx={{ mr: 1, color: 'inherit', borderColor: 'inherit' }} variant="outlined" />
          )}
          <Button color="inherit" startIcon={<Logout />} onClick={logout}>ログアウト</Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: { xs: 2, sm: 3 }, px: { xs: 1, sm: 2 } }}>
        <IndustryUnifiedPlatformPage />
      </Container>
    </Box>
  );
}

export default App;
