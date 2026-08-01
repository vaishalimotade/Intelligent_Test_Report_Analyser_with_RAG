import React from 'react';
import { Card, CardContent, Typography, Grid, Stack, Chip, Box } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Line, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Tooltip as ChartTooltip, Legend, Filler } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, ChartTooltip, Legend, Filler);

function AnalyticsCharts() {
  const theme = useTheme();
  const lineData = {
    labels: ['May 1', 'May 8', 'May 15', 'May 22', 'May 29', 'Jun 5'],
    datasets: [
      { label: 'Success Trend', data: [84, 86, 88, 90, 91, 92], borderColor: theme.palette.primary.main, backgroundColor: 'rgba(0,120,212,0.12)', tension: 0.35, fill: true, pointRadius: 4 },
      { label: 'Failure Trend', data: [16, 14, 12, 10, 9, 8], borderColor: theme.palette.error.main, backgroundColor: 'rgba(209,52,56,0.12)', tension: 0.35, fill: true, pointRadius: 4 },
      { label: 'Release Quality', data: [76, 80, 82, 84, 86, 88], borderColor: theme.palette.success.main, backgroundColor: 'rgba(16,124,16,0.12)', tension: 0.35, fill: true, pointRadius: 4 },
    ],
  };

  const doughnutData = {
    labels: ['Timeout Errors', 'Database Errors', 'Authentication Failures', 'Assertion Failures', 'Other'],
    datasets: [{
      data: [34, 18, 14, 12, 22],
      backgroundColor: ['#0078D4', '#FFB900', '#D13438', '#107C10', '#64748B'],
      borderWidth: 0,
    }],
  };

  return (
    <Grid container spacing={2.5}>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
              <Box>
                <Typography variant="h6">Quality Overview</Typography>
                <Typography variant="body2" color="text.secondary">A 30-day view of reliability, failures, and release quality.</Typography>
              </Box>
              <Chip label="30-day trend" color="primary" size="small" />
            </Stack>
            <Box sx={{ height: 320 }}>
              <Line data={lineData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: theme.palette.text.secondary } } }, scales: { x: { ticks: { color: theme.palette.text.secondary }, grid: { display: false } }, y: { ticks: { color: theme.palette.text.secondary }, grid: { color: theme.palette.divider } } } }} />
            </Box>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={7}>
        <Card>
          <CardContent>
            <Typography variant="h6" mb={2}>Failure Distribution</Typography>
            <Box sx={{ height: 260 }}>
              <Doughnut data={doughnutData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: theme.palette.text.secondary, boxWidth: 12, padding: 16 } } } }} />
            </Box>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={5}>
        <Card>
          <CardContent>
            <Typography variant="h6" mb={2}>AI Summary</Typography>
            <Typography variant="body2" color="text.secondary" mb={2}>Payment and checkout failures are driving most of the volatility. Timeout handling and auth retry storms are the dominant patterns.</Typography>
            <Box sx={{ p: 2, borderRadius: 3, bgcolor: 'rgba(0,120,212,0.08)' }}>
              <Typography variant="subtitle2" fontWeight={700}>Observed issue</Typography>
              <Typography variant="body2" color="text.secondary" mb={1}>Failure clusters rose by 24% over the last 7 days.</Typography>
              <Typography variant="subtitle2" fontWeight={700}>Recommended action</Typography>
              <Typography variant="body2" color="text.secondary">Route around flaky auth retries and adjust payment timeout thresholds.</Typography>
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}

export default AnalyticsCharts;
