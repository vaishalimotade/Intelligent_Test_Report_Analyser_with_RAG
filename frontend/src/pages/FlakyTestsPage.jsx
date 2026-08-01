import React, { useMemo, useState } from 'react';
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Stack, Chip, MenuItem, Pagination, Box, Card } from '@mui/material';
import { TableSortLabel } from '@mui/material';

const initialTests = [
  { test_name: 'Login Flow', module_name: 'Auth', failure_rate: 18, flaky_score: 83, risk_level: 'Critical', recommendation: 'Stabilize auth dependency timing.' },
  { test_name: 'Checkout API', module_name: 'Payments', failure_rate: 14, flaky_score: 76, risk_level: 'High', recommendation: 'Add retry jitter and timeouts.' },
  { test_name: 'Search Filter', module_name: 'Search', failure_rate: 9, flaky_score: 61, risk_level: 'Medium', recommendation: 'Investigate async rendering.' },
  { test_name: 'Billing Sync', module_name: 'Billing', failure_rate: 4, flaky_score: 41, risk_level: 'Low', recommendation: 'Add resilience logging.' },
  { test_name: 'Payment Retry', module_name: 'Payments', failure_rate: 12, flaky_score: 72, risk_level: 'High', recommendation: 'Rework retry policy.' },
];

function FlakyTestsPage() {
  const [query, setQuery] = useState('');
  const [riskFilter, setRiskFilter] = useState('All');
  const [moduleFilter, setModuleFilter] = useState('All');
  const [orderBy, setOrderBy] = useState('flaky_score');
  const [orderDirection, setOrderDirection] = useState('desc');
  const [page, setPage] = useState(1);
  const pageSize = 5;

  const filteredTests = useMemo(() => {
    const next = initialTests.filter((row) => {
      const matchesQuery = `${row.test_name} ${row.module_name}`.toLowerCase().includes(query.toLowerCase());
      const matchesRisk = riskFilter === 'All' || row.risk_level === riskFilter;
      const matchesModule = moduleFilter === 'All' || row.module_name === moduleFilter;
      return matchesQuery && matchesRisk && matchesModule;
    });

    next.sort((a, b) => {
      const valueA = a[orderBy];
      const valueB = b[orderBy];
      const direction = orderDirection === 'asc' ? 1 : -1;
      return (valueA > valueB ? 1 : -1) * direction;
    });

    return next;
  }, [query, riskFilter, moduleFilter, orderBy, orderDirection]);

  const pagedTests = filteredTests.slice((page - 1) * pageSize, page * pageSize);

  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && orderDirection === 'asc';
    setOrderDirection(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>Flaky Tests Observatory</Typography>
      <Typography variant="body1" color="text.secondary" mb={2}>Compact analysis of unstable tests and recommended interventions.</Typography>
      <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} mb={2}>
        <TextField size="small" label="Search tests" value={query} onChange={(e) => { setQuery(e.target.value); setPage(1); }} fullWidth />
        <TextField select size="small" label="Risk Level" value={riskFilter} onChange={(e) => { setRiskFilter(e.target.value); setPage(1); }} sx={{ minWidth: 180 }}>
          <MenuItem value="All">All</MenuItem>
          <MenuItem value="Critical">Critical</MenuItem>
          <MenuItem value="High">High</MenuItem>
          <MenuItem value="Medium">Medium</MenuItem>
          <MenuItem value="Low">Low</MenuItem>
        </TextField>
        <TextField select size="small" label="Module" value={moduleFilter} onChange={(e) => { setModuleFilter(e.target.value); setPage(1); }} sx={{ minWidth: 180 }}>
          <MenuItem value="All">All</MenuItem>
          <MenuItem value="Auth">Auth</MenuItem>
          <MenuItem value="Payments">Payments</MenuItem>
          <MenuItem value="Search">Search</MenuItem>
          <MenuItem value="Billing">Billing</MenuItem>
        </TextField>
      </Stack>
      <Card>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>
                  <TableSortLabel active={orderBy === 'test_name'} direction={orderBy === 'test_name' ? orderDirection : 'asc'} onClick={() => handleRequestSort('test_name')}>
                    Test Name
                  </TableSortLabel>
                </TableCell>
                <TableCell>Module</TableCell>
                <TableCell>
                  <TableSortLabel active={orderBy === 'failure_rate'} direction={orderBy === 'failure_rate' ? orderDirection : 'asc'} onClick={() => handleRequestSort('failure_rate')}>
                    Failure Rate
                  </TableSortLabel>
                </TableCell>
                <TableCell>
                  <TableSortLabel active={orderBy === 'flaky_score'} direction={orderBy === 'flaky_score' ? orderDirection : 'asc'} onClick={() => handleRequestSort('flaky_score')}>
                    Flaky Score
                  </TableSortLabel>
                </TableCell>
                <TableCell>Risk Level</TableCell>
                <TableCell>Recommendation</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {pagedTests.map((row) => (
                <TableRow key={`${row.test_name}-${row.module_name}`} hover>
                  <TableCell>{row.test_name}</TableCell>
                  <TableCell>{row.module_name}</TableCell>
                  <TableCell>{row.failure_rate}%</TableCell>
                  <TableCell>{row.flaky_score}%</TableCell>
                  <TableCell><Chip label={row.risk_level} color={row.risk_level === 'Critical' ? 'error' : row.risk_level === 'High' ? 'warning' : row.risk_level === 'Medium' ? 'info' : 'success'} size="small" /></TableCell>
                  <TableCell>{row.recommendation}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Card>
      <Box mt={2} display="flex" justifyContent="flex-end">
        <Pagination count={Math.max(1, Math.ceil(filteredTests.length / pageSize))} page={page - 1} onChange={(_, value) => setPage(value)} color="primary" />
      </Box>
    </Box>
  );
}

export default FlakyTestsPage;
