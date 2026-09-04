import React, { useState } from 'react';
import { Alert, TextField, Button, Typography, Card, CardContent, Grid, Box, Stack, Chip, Divider, CircularProgress } from '@mui/material';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function RootCausePage() {
  const [testName, setTestName] = useState('Checkout API');
  const [result, setResult] = useState(null);
  const [state, setState] = useState({ loading: false, error: '' });

  const handleAnalyze = async () => {
    if (!testName.trim()) return;
    setState({ loading: true, error: '' });
    try {
      const response = await fetch(`${API_URL}/root-cause/${encodeURIComponent(testName.trim())}`);
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.detail || 'Root-cause analysis failed.');
      setResult(payload);
    } catch (error) {
      setState({ loading: false, error: error.message });
      return;
    }
    setState({ loading: false, error: '' });
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
              <Button variant="contained" onClick={handleAnalyze} disabled={state.loading} startIcon={state.loading ? <CircularProgress size={18} color="inherit" /> : null}>Analyze</Button>
              {state.error && <Alert severity="error" sx={{ mt: 2 }}>{state.error}</Alert>}
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
                {result && <Chip label={`Confidence ${result.confidence || 0}%`} color="success" size="small" />}
              </Stack>
              {result ? <>
                <Typography variant="body1" mb={1}>{result.root_cause}</Typography>
                <Typography variant="subtitle2">Evidence</Typography>
                <Typography variant="body2" mb={1}>{result.evidence}</Typography>
                <Typography variant="subtitle2">Recommendation</Typography>
                <Typography variant="body2">{result.recommendation}</Typography>
              </> : <Typography variant="body2" color="text.secondary">Enter a test name and run an analysis.</Typography>}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default RootCausePage;
