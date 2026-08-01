import React, { useState } from 'react';
import { TextField, Button, Typography, Card, CardContent, Grid, Box, Stack, Chip, Divider } from '@mui/material';

function RootCausePage() {
  const [testName, setTestName] = useState('Checkout API');
  const [result, setResult] = useState({
    root_cause: 'A race condition appears when the payment gateway times out and retries the request.',
    evidence: 'The same test failed 3 times within 10 minutes and the gateway logs show timeout spikes.',
    recommendation: 'Add retry jitter and inspect the timeout configuration for the payment gateway.',
  });

  const handleAnalyze = () => {
    setResult({
      root_cause: `Analysis for ${testName}: unstable dependency timing and timeout mismatch.`,
      evidence: 'The test is flaky under burst load and correlates with increased latency.',
      recommendation: 'Stabilize the dependency boundary and add more robust waiting logic.',
    });
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>AI Root Cause Analysis</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={5}>
          <Card>
            <CardContent>
              <Typography variant="h6" mb={2}>Investigate a Failure</Typography>
              <TextField label="Test Name" value={testName} onChange={(e) => setTestName(e.target.value)} fullWidth margin="normal" />
              <Button variant="contained" onClick={handleAnalyze}>Analyze</Button>
              <Divider sx={{ my: 2 }} />
              <Stack spacing={1.5}>
                <Box>
                  <Typography variant="subtitle2">Failure Timeline</Typography>
                  <Typography variant="body2">09:12 UTC – timeout spike</Typography>
                  <Typography variant="body2">09:18 UTC – retry storm</Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2">Similar Historical Failures</Typography>
                  <Typography variant="body2">Checkout gateway flake • 2 similar incidents</Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={7}>
          <Card>
            <CardContent>
              <Stack direction="row" spacing={1} alignItems="center" mb={2}>
                <Typography variant="h6">AI Recommendation</Typography>
                <Chip label="Confidence 92%" color="success" size="small" />
              </Stack>
              <Typography variant="body1" mb={1}>{result.root_cause}</Typography>
              <Typography variant="subtitle2">Evidence</Typography>
              <Typography variant="body2" mb={1}>{result.evidence}</Typography>
              <Typography variant="subtitle2">Recommendation</Typography>
              <Typography variant="body2">{result.recommendation}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default RootCausePage;
