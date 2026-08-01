import React from 'react';
import { Grid, Stack, Typography, Box, Chip } from '@mui/material';
import { motion } from 'framer-motion';
import TrendingUpRoundedIcon from '@mui/icons-material/TrendingUpRounded';
import CheckCircleRoundedIcon from '@mui/icons-material/CheckCircleRounded';
import ErrorOutlineRoundedIcon from '@mui/icons-material/ErrorOutlineRounded';
import BugReportRoundedIcon from '@mui/icons-material/BugReportRounded';
import FlashOnRoundedIcon from '@mui/icons-material/FlashOnRounded';
import SpeedRoundedIcon from '@mui/icons-material/SpeedRounded';
import KpiCard from '../components/KpiCard';
import AnalyticsCharts from '../components/AnalyticsCharts';
import HeatmapPanel from '../components/HeatmapPanel';
import AiInsightsCard from '../components/AiInsightsCard';
import FlakyTestsTable from '../components/FlakyTestsTable';
import AssistantPanel from '../components/AssistantPanel';

function DashboardPage() {
  const kpis = [
    { title: 'Total Tests Executed', value: '184', change: '+12.8% vs last week', icon: <TrendingUpRoundedIcon />, accent: '#0078D4' },
    { title: 'Test Pass Rate', value: '92%', change: '+3.2% stable', icon: <CheckCircleRoundedIcon />, accent: '#107C10' },
    { title: 'Total Failures', value: '14', change: '-1.4% improved', icon: <ErrorOutlineRoundedIcon />, accent: '#D13438' },
    { title: 'Flaky Tests Count', value: '10', change: '3 critical', icon: <BugReportRoundedIcon />, accent: '#FFB900' },
    { title: 'Critical Issues', value: '6', change: '2 new this week', icon: <FlashOnRoundedIcon />, accent: '#0078D4' },
    { title: 'Quality Score', value: '88/100', change: 'Excellent', icon: <SpeedRoundedIcon />, accent: '#107C10' },
  ];

  return (
    <Box>
      <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" alignItems={{ xs: 'flex-start', md: 'center' }} spacing={2} mb={3}>
        <Box>
          <Typography variant="h4" fontWeight={700}>Intelligent Test Report Analyzer</Typography>
          <Typography variant="body1" color="text.secondary">Executive-grade visibility into release readiness, flaky behavior, and AI-guided remediation.</Typography>
        </Box>
        <Chip label="Updated 2 min ago" color="success" />
      </Stack>

      <Grid container spacing={2} mb={3}>
        {kpis.map((kpi) => (
          <Grid item xs={12} sm={6} md={4} lg={2} key={kpi.title}>
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
              <KpiCard {...kpi} />
            </motion.div>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={2.5} mb={2.5}>
        <Grid item xs={12} lg={8}>
          <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}>
            <AnalyticsCharts />
          </motion.div>
        </Grid>
        <Grid item xs={12} lg={4}>
          <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35, delay: 0.05 }}>
            <AiInsightsCard />
          </motion.div>
        </Grid>
      </Grid>

      <Grid container spacing={2.5} mb={2.5}>
        <Grid item xs={12} lg={8}>
          <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35, delay: 0.08 }}>
            <FlakyTestsTable />
          </motion.div>
        </Grid>
        <Grid item xs={12} lg={4}>
          <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35, delay: 0.1 }}>
            <AssistantPanel />
          </motion.div>
        </Grid>
      </Grid>

      <Grid container spacing={2.5}>
        <Grid item xs={12} xl={8}>
          <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35, delay: 0.12 }}>
            <HeatmapPanel />
          </motion.div>
        </Grid>
        <Grid item xs={12} xl={4}>
          <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35, delay: 0.14 }}>
            <Box sx={{ height: '100%', borderRadius: 4, p: 3, bgcolor: 'background.paper', border: '1px solid', borderColor: 'divider' }}>
              <Typography variant="h6" gutterBottom>Weekly Quality Digest</Typography>
              <Typography variant="body2" color="text.secondary" mb={2}>A concise summary for leadership and delivery teams.</Typography>
              <Stack spacing={1.5}>
                <Box>
                  <Typography variant="subtitle2" fontWeight={700}>Key achievements</Typography>
                  <Typography variant="body2" color="text.secondary">Pass rate improved by 3.2% and critical wait time regressions dropped by 18%.</Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" fontWeight={700}>Key risks</Typography>
                  <Typography variant="body2" color="text.secondary">Payments and authentication remain the highest-density hotspots for recurring failures.</Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" fontWeight={700}>Recommended actions</Typography>
                  <Typography variant="body2" color="text.secondary">Prioritize retry backoff tuning and isolate unstable auth flows before the next release.</Typography>
                </Box>
                <Box sx={{ p: 2, borderRadius: 3, bgcolor: 'rgba(0,120,212,0.08)' }}>
                  <Typography variant="subtitle2" fontWeight={700}>Quality score summary</Typography>
                  <Typography variant="h4" color="primary.main" fontWeight={700}>88/100</Typography>
                </Box>
              </Stack>
            </Box>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
}

export default DashboardPage;
