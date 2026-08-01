import React from 'react';
import { Card, CardContent, Box, Typography, Stack, Chip } from '@mui/material';

function KpiCard({ title, value, change, icon, accent }) {
  return (
    <Card sx={{ height: 140, borderRadius: 2.5, display: 'flex', alignItems: 'center' }}>
      <CardContent sx={{ width: '100%' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start" spacing={1}>
          <Box sx={{ minWidth: 0 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 0.8 }}>{title}</Typography>
            <Typography variant="h5" fontWeight={700}>{value}</Typography>
          </Box>
          <Box sx={{ width: 42, height: 42, borderRadius: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: `${accent}14`, color: accent }}>
            {icon}
          </Box>
        </Stack>
        <Box sx={{ mt: 1.5 }}>
          <Chip label={change} size="small" sx={{ bgcolor: `${accent}14`, color: accent, borderRadius: 999 }} />
        </Box>
      </CardContent>
    </Card>
  );
}

export default KpiCard;
