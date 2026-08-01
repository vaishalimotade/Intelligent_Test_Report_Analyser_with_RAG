import React from 'react';
import { Card, CardContent, Typography, Stack, Chip, Table, TableBody, TableCell, TableHead, TableRow, Box } from '@mui/material';

const flakyTests = [
  { name: 'PaymentCheckoutFlow', module: 'Payments', executions: 184, failures: 21, score: 92, risk: 'High' },
  { name: 'InventorySyncJob', module: 'Inventory', executions: 162, failures: 14, score: 86, risk: 'Medium' },
  { name: 'AuthSessionRefresh', module: 'Authentication', executions: 176, failures: 12, score: 82, risk: 'Medium' },
  { name: 'SearchIndexing', module: 'Search', executions: 152, failures: 10, score: 78, risk: 'Low' },
  { name: 'CheckoutRetryHandler', module: 'Checkout', executions: 198, failures: 17, score: 89, risk: 'High' },
  { name: 'OrderStatusSync', module: 'Orders', executions: 140, failures: 9, score: 74, risk: 'Low' },
  { name: 'SessionTokenRotation', module: 'Authentication', executions: 158, failures: 11, score: 81, risk: 'Medium' },
  { name: 'PaymentWebhookReplay', module: 'Payments', executions: 137, failures: 8, score: 72, risk: 'Low' },
  { name: 'SearchFacetFilter', module: 'Search', executions: 166, failures: 13, score: 84, risk: 'Medium' },
  { name: 'InventoryAvailCheck', module: 'Inventory', executions: 173, failures: 7, score: 69, risk: 'Low' },
];

function FlakyTestsTable() {
  const getRiskColor = (risk) => {
    if (risk === 'High') return { color: '#D13438', bg: '#FCE7E9' };
    if (risk === 'Medium') return { color: '#FFB900', bg: '#FFF4D6' };
    return { color: '#107C10', bg: '#E6F4EA' };
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
          <Box>
            <Typography variant="h6">Top 10 Flaky Tests</Typography>
            <Typography variant="body2" color="text.secondary">Signals that need follow-up before the next release.</Typography>
          </Box>
          <Chip label="Top risk" color="warning" size="small" />
        </Stack>
        <Box sx={{ overflowX: 'auto' }}>
          <Table size="small" aria-label="flaky tests table">
            <TableHead>
              <TableRow>
                <TableCell>Test Name</TableCell>
                <TableCell>Module</TableCell>
                <TableCell>Exec Count</TableCell>
                <TableCell>Failure Count</TableCell>
                <TableCell>Flaky Score</TableCell>
                <TableCell>Risk Level</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {flakyTests.map((test) => {
                const riskColor = getRiskColor(test.risk);
                return (
                  <TableRow key={test.name} hover>
                    <TableCell>{test.name}</TableCell>
                    <TableCell>{test.module}</TableCell>
                    <TableCell>{test.executions}</TableCell>
                    <TableCell>{test.failures}</TableCell>
                    <TableCell>{test.score}</TableCell>
                    <TableCell>
                      <Chip label={test.risk} size="small" sx={{ bgcolor: riskColor.bg, color: riskColor.color, fontWeight: 700 }} />
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </Box>
      </CardContent>
    </Card>
  );
}

export default FlakyTestsTable;
