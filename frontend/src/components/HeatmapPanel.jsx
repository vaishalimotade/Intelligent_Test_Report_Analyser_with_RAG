import React from 'react';
import { Card, CardContent, Typography, Box, Stack, Chip } from '@mui/material';

const heatmapRows = [
  { day: 'Mon', values: ['#107C10', '#FFB900', '#D13438', '#107C10', '#FFB900'] },
  { day: 'Tue', values: ['#FFB900', '#107C10', '#FFB900', '#D13438', '#107C10'] },
  { day: 'Wed', values: ['#107C10', '#107C10', '#FFB900', '#107C10', '#D13438'] },
  { day: 'Thu', values: ['#D13438', '#FFB900', '#107C10', '#FFB900', '#107C10'] },
  { day: 'Fri', values: ['#107C10', '#D13438', '#107C10', '#107C10', '#FFB900'] },
];
const modules = ['Payments', 'Checkout', 'Orders', 'Authentication', 'Search', 'Inventory'];

function HeatmapPanel() {
  return (
    <Card>
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Box>
            <Typography variant="h6">Hotspot Heatmap</Typography>
            <Typography variant="body2" color="text.secondary">Modules with the highest failure density across the last 30 days.</Typography>
          </Box>
          <Chip label="Last 30 days" color="primary" size="small" />
        </Stack>
        <Box sx={{ overflowX: 'auto' }}>
          <Box component="table" sx={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left', padding: '8px 10px', color: '#64748B' }}>Day</th>
                {modules.map((module) => (
                  <th key={module} style={{ textAlign: 'left', padding: '8px 10px', color: '#64748B' }}>{module}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {heatmapRows.map((row) => (
                <tr key={row.day}>
                  <td style={{ padding: '8px 10px', color: 'text.secondary' }}>{row.day}</td>
                  {row.values.map((color, index) => (
                    <td key={`${row.day}-${index}`} style={{ padding: '8px 10px' }}>
                      <Box sx={{ width: 40, height: 40, borderRadius: 1.8, bgcolor: color, boxShadow: 'inset 0 0 0 1px rgba(255,255,255,0.24)' }} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}

export default HeatmapPanel;
