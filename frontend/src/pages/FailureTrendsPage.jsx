import React from 'react';
import { Grid, Typography, Paper, Box, Stack, Chip, List, ListItem, ListItemText } from '@mui/material';

function FailureTrendsPage() {
  const patterns = [
    { reason: 'Timeout during checkout', module_name: 'Checkout API', count: 12, severity: 'Critical' },
    { reason: 'Intermittent 500 on login', module_name: 'Auth Service', count: 9, severity: 'High' },
    { reason: 'Search results race condition', module_name: 'Search Module', count: 7, severity: 'Medium' },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Failure Trends Intelligence</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" mb={2}>Chronology of Failures</Typography>
            <List>
              {patterns.map((item, idx) => (
                <ListItem key={idx} sx={{ borderBottom: idx < patterns.length - 1 ? '1px solid rgba(255,255,255,0.08)' : 'none' }}>
                  <ListItemText primary={item.reason} secondary={`${item.module_name} — ${item.count} occurrences`} />
                  <Chip label={item.severity} color={item.severity === 'Critical' ? 'error' : item.severity === 'High' ? 'warning' : 'info'} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" mb={2}>Signal Summary</Typography>
            <Stack spacing={2}>
              <Box>
                <Typography variant="body2" color="text.secondary">Peak Window</Typography>
                <Typography variant="h5">08:00 – 10:00 UTC</Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary">Affected Modules</Typography>
                <Typography variant="h5">Auth, Payments, Search</Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary">Risk Signal</Typography>
                <Typography variant="h5">Escalating</Typography>
              </Box>
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default FailureTrendsPage;
