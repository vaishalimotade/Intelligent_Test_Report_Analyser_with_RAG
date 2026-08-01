import { createTheme } from '@mui/material/styles';

const createAppTheme = (mode = 'light') => createTheme({
  palette: {
    mode,
    primary: { main: '#0078D4' },
    secondary: { main: '#0F6CBD' },
    success: { main: '#107C10' },
    warning: { main: '#FFB900' },
    error: { main: '#D13438' },
    background: {
      default: mode === 'dark' ? '#1E1E1E' : '#F8F9FB',
      paper: mode === 'dark' ? '#252525' : '#FFFFFF',
    },
    text: {
      primary: mode === 'dark' ? '#F5F7FA' : '#111827',
      secondary: mode === 'dark' ? '#B9C2D1' : '#64748B',
    },
    divider: mode === 'dark' ? '#3A3A3A' : '#E5E7EB',
  },
  typography: {
    fontFamily: 'Inter, Roboto, Arial, sans-serif',
    h1: { fontWeight: 700 },
    h2: { fontWeight: 700 },
    h3: { fontWeight: 700 },
    h4: { fontWeight: 700 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
  },
  shape: { borderRadius: 16 },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: mode === 'dark' ? '#252525' : '#FFFFFF',
          border: `1px solid ${mode === 'dark' ? '#3A3A3A' : '#E5E7EB'}`,
          boxShadow: mode === 'dark' ? '0 12px 24px rgba(0, 0, 0, 0.28)' : '0 12px 30px rgba(15, 23, 42, 0.06)',
          transition: 'transform 180ms ease, box-shadow 180ms ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: mode === 'dark' ? '0 16px 30px rgba(0, 0, 0, 0.32)' : '0 16px 32px rgba(15, 23, 42, 0.10)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 999,
          textTransform: 'none',
          boxShadow: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: mode === 'dark' ? '#252525' : '#FFFFFF',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: mode === 'dark' ? 'rgba(37, 37, 37, 0.9)' : 'rgba(255,255,255,0.9)',
          color: mode === 'dark' ? '#F5F7FA' : '#111827',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
        },
      },
    },
  },
});

export default createAppTheme;
