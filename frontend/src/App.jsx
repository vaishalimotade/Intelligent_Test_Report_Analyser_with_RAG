import React, { useMemo, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import DashboardShell from './components/DashboardShell';
import DashboardPage from './pages/DashboardPage';
import FlakyTestsPage from './pages/FlakyTestsPage';
import FailureTrendsPage from './pages/FailureTrendsPage';
import RootCausePage from './pages/RootCausePage';
import WeeklyDigestPage from './pages/WeeklyDigestPage';
import createAppTheme from './theme';

function App() {
  const [mode, setMode] = useState('light');
  const theme = useMemo(() => createAppTheme(mode), [mode]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <DashboardShell mode={mode} onToggleTheme={() => setMode((current) => (current === 'light' ? 'dark' : 'light'))}>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/quality-analytics" element={<DashboardPage />} />
            <Route path="/flaky-tests" element={<FlakyTestsPage />} />
            <Route path="/hotspots" element={<FailureTrendsPage />} />
            <Route path="/failure-trends" element={<FailureTrendsPage />} />
            <Route path="/root-cause" element={<RootCausePage />} />
            <Route path="/weekly-digest" element={<WeeklyDigestPage />} />
            <Route path="/settings" element={<WeeklyDigestPage />} />
          </Routes>
        </DashboardShell>
      </Router>
    </ThemeProvider>
  );
}

export default App;
