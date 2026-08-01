import React from 'react';
import { Card, CardContent, Typography, Box, Stack, LinearProgress, Chip } from '@mui/material';
import AutoAwesomeRoundedIcon from '@mui/icons-material/AutoAwesomeRounded';

function AiInsightsCard() {
  return (
    <Card sx={{ height: '100%', borderLeft: '4px solid', borderColor: 'primary.main' }}>
      <CardContent>
        <Stack direction="row" spacing={1} alignItems="center" mb={2}>
          <Box sx={{ color: 'primary.main', display: 'flex', alignItems: 'center' }}>
            <AutoAwesomeRoundedIcon />
          </Box>
          <Box>
            <Typography variant="h6">AI Root Cause Analysis</Typography>
            <Typography variant="body2" color="text.secondary">Conversational intelligence for the next best action.</Typography>
          </Box>
        </Stack>
        <Typography variant="body2" color="text.secondary" mb={2}>
          “Payment module failures increased by 24% in the last 7 days. Historical analysis suggests API timeout as the primary cause.”
        </Typography>
        <Stack spacing={1.8}>
          <Box>
            <Typography variant="subtitle2" fontWeight={700}>Observed issue</Typography>
            <Typography variant="body2" color="text.secondary">Intermittent checkout failures correlate with elevated retry traffic.</Typography>
          </Box>
          <Box>
            <Typography variant="subtitle2" fontWeight={700}>Historical trend</Typography>
            <Typography variant="body2" color="text.secondary">The trend has worsened since the last release window and shows a strong weekend spike.</Typography>
          </Box>
          <Box>
            <Typography variant="subtitle2" fontWeight={700}>Probable root cause</Typography>
            <Typography variant="body2" color="text.secondary">Timeout jitter and auth token refresh collisions are increasing false negative failures.</Typography>
          </Box>
          <Box>
            <Typography variant="subtitle2" fontWeight={700}>Recommended action</Typography>
            <Typography variant="body2" color="text.secondary">Introduce exponential backoff, circuit breaker logic, and targeted payment-service diagnostics.</Typography>
          </Box>
          <Box>
            <Stack direction="row" justifyContent="space-between" alignItems="center" mb={0.8}>
              <Typography variant="subtitle2" fontWeight={700}>Release readiness</Typography>
              <Chip label="82/100" color="success" size="small" />
            </Stack>
            <LinearProgress variant="determinate" value={82} sx={{ height: 8, borderRadius: 999, bgcolor: 'divider', '& .MuiLinearProgress-bar': { bgcolor: 'success.main' } }} />
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
}

export default AiInsightsCard;
