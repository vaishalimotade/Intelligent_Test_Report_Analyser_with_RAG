import React, { useState } from 'react';
import { Box, Drawer, AppBar, Toolbar, IconButton, Typography, InputBase, Avatar, Badge, List, ListItemButton, ListItemIcon, ListItemText, Divider, Tooltip, CssBaseline, Stack, Chip, FormControl, Select, MenuItem, Switch, useTheme } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import NotificationsNoneIcon from '@mui/icons-material/NotificationsNone';
import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded';
import BarChartRoundedIcon from '@mui/icons-material/BarChartRounded';
import BiotechRoundedIcon from '@mui/icons-material/BiotechRounded';
import LocalFireDepartmentRoundedIcon from '@mui/icons-material/LocalFireDepartmentRounded';
import PsychologyRoundedIcon from '@mui/icons-material/PsychologyRounded';
import InsightsRoundedIcon from '@mui/icons-material/InsightsRounded';
import DescriptionRoundedIcon from '@mui/icons-material/DescriptionRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded';
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';
import { useLocation, Link } from 'react-router-dom';

const drawerWidth = 250;
const menuItems = [
  { label: 'Dashboard', icon: <DashboardRoundedIcon />, path: '/' },
  { label: 'Quality Analytics', icon: <BarChartRoundedIcon />, path: '/quality-analytics' },
  { label: 'Flaky Tests', icon: <BiotechRoundedIcon />, path: '/flaky-tests' },
  { label: 'Hotspots', icon: <LocalFireDepartmentRoundedIcon />, path: '/hotspots' },
  { label: 'AI Root Cause', icon: <PsychologyRoundedIcon />, path: '/root-cause' },
  { label: 'Failure Trends', icon: <InsightsRoundedIcon />, path: '/failure-trends' },
  { label: 'Weekly Digest', icon: <DescriptionRoundedIcon />, path: '/weekly-digest' },
  { label: 'Settings', icon: <SettingsRoundedIcon />, path: '/settings' },
];

function DashboardShell({ children, mode, onToggleTheme }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [dateRange, setDateRange] = useState('Last 30 days');
  const [release, setRelease] = useState('Release 2026.08');
  const location = useLocation();
  const theme = useTheme();

  const handleDrawerToggle = () => setMobileOpen(!mobileOpen);

  const drawer = (
    <Box sx={{ height: '100%', bgcolor: 'background.paper', borderRight: `1px solid ${theme.palette.divider}` }}>
      <Box sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 1.5 }}>
        <Box sx={{ width: 44, height: 44, borderRadius: 2.5, bgcolor: 'primary.main', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 700 }}>IT</Box>
        <Box>
          <Typography variant="subtitle1" fontWeight={700}>Intelligent Test</Typography>
          <Typography variant="caption" color="text.secondary">Insights Engine</Typography>
        </Box>
      </Box>
      <Divider />
      <List sx={{ px: 1.2, py: 1.5 }}>
        {menuItems.map((item) => {
          const active = location.pathname === item.path;
          return (
            <ListItemButton
              key={item.label}
              component={Link}
              to={item.path}
              selected={active}
              sx={{
                borderRadius: 2,
                mb: 0.75,
                color: active ? 'primary.main' : 'text.secondary',
                bgcolor: active ? 'rgba(0,120,212,0.08)' : 'transparent',
                '&.Mui-selected': { bgcolor: 'rgba(0,120,212,0.08)', color: 'primary.main' },
                '&:hover': { bgcolor: 'action.hover' },
              }}
            >
              <ListItemIcon sx={{ color: active ? 'primary.main' : 'inherit', minWidth: 36 }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          );
        })}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <CssBaseline />
      <AppBar position="fixed" elevation={0} sx={{ width: { md: `calc(100% - ${drawerWidth}px)` }, ml: { md: `${drawerWidth}px` }, backdropFilter: 'blur(18px)', borderBottom: `1px solid ${theme.palette.divider}` }}>
        <Toolbar sx={{ gap: 1.2, py: 0.5 }}>
          <IconButton color="inherit" edge="start" sx={{ mr: 1, display: { md: 'none' } }} onClick={handleDrawerToggle} aria-label="Open sidebar">
            <MenuIcon />
          </IconButton>
          <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', gap: 1.5, bgcolor: 'background.default', border: `1px solid ${theme.palette.divider}`, borderRadius: 999, px: 2, py: 1 }}>
            <SearchIcon color="action" />
            <InputBase placeholder="Search insights, modules, tests" sx={{ width: '100%' }} inputProps={{ 'aria-label': 'Search insights' }} />
          </Box>
          <Stack direction={{ xs: 'column', lg: 'row' }} alignItems="center" spacing={1}>
            <FormControl size="small" sx={{ minWidth: 140 }}>
              <Select value={dateRange} onChange={(event) => setDateRange(event.target.value)} displayEmpty>
                <MenuItem value="Last 30 days">Last 30 days</MenuItem>
                <MenuItem value="Last 7 days">Last 7 days</MenuItem>
                <MenuItem value="Last 90 days">Last 90 days</MenuItem>
              </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 160 }}>
              <Select value={release} onChange={(event) => setRelease(event.target.value)} displayEmpty>
                <MenuItem value="Release 2026.08">Release 2026.08</MenuItem>
                <MenuItem value="Release 2026.07">Release 2026.07</MenuItem>
                <MenuItem value="Release 2026.06">Release 2026.06</MenuItem>
              </Select>
            </FormControl>
            <Stack direction="row" alignItems="center" spacing={0.5} sx={{ px: 1, py: 0.5, borderRadius: 999, bgcolor: 'background.paper', border: `1px solid ${theme.palette.divider}` }}>
              <LightModeRoundedIcon color={mode === 'light' ? 'primary' : 'inherit'} fontSize="small" />
              <Switch checked={mode === 'dark'} onChange={onToggleTheme} inputProps={{ 'aria-label': 'Theme toggle' }} />
              <DarkModeRoundedIcon color={mode === 'dark' ? 'primary' : 'inherit'} fontSize="small" />
            </Stack>
            <Tooltip title="Notifications"><IconButton color="inherit" aria-label="Notifications"><Badge badgeContent={4} color="error"><NotificationsNoneIcon /></Badge></IconButton></Tooltip>
            <Avatar sx={{ bgcolor: 'primary.main', width: 36, height: 36 }}>AD</Avatar>
            <Chip label="Enterprise" color="primary" size="small" />
          </Stack>
        </Toolbar>
      </AppBar>
      <Box component="nav" sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}>
        <Drawer variant="temporary" open={mobileOpen} onClose={handleDrawerToggle} ModalProps={{ keepMounted: true }} sx={{ display: { xs: 'block', md: 'none' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth } }}>
          {drawer}
        </Drawer>
        <Drawer variant="permanent" open sx={{ display: { xs: 'none', md: 'block' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth } }}>
          {drawer}
        </Drawer>
      </Box>
      <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, md: 3 }, pt: { xs: 10, md: 12 } }}>
        {children}
      </Box>
    </Box>
  );
}

export default DashboardShell;
