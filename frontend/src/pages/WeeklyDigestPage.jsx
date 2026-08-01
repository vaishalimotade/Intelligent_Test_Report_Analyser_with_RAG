import React from 'react';
import { Typography, Card, CardContent, Grid, Box, Stack, Chip, Button } from '@mui/material';

function WeeklyDigestPage() {
  const digest = {
    total_executions: 184,
    pass_rate: 92,
    fail_rate: 8,
    quality_score: 88,
    recommendations: [
      'Investigate checkout timeouts during peak traffic.',
      'Stabilize login tests by reducing dependency flakiness.',
      'Add more coverage around search race conditions.',
    ],
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Executive Weekly Digest</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Quality Score</Typography>
              <Typography variant="h3" fontWeight={700}>{digest.quality_score}/100</Typography>
              <Chip label="Strong release posture" color="success" sx={{ mt: 2 }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6">AI Summary</Typography>
              <Typography variant="body1" mt={1}>The system observed a modest but meaningful improvement in reliability versus last week, while checkout issues remain the most prominent risk to watch.</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Top Risks</Typography>
              <ul>
                <li>Checkout timeout spikes</li>
                <li>Auth dependency flake</li>
                <li>Search race conditions</li>
              </ul>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Management Insights</Typography>
              <Typography variant="body1" mt={1}>Release readiness remains high, but one critical payment path should be monitored closely before deployment.</Typography>
              <Stack direction="row" spacing={1} mt={2}>
                <Button variant="contained">Export PDF</Button>
                <Button variant="outlined">Email</Button>
                <Button variant="outlined">Slack</Button>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default WeeklyDigestPage;
