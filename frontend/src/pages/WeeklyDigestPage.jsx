import React, { useState } from 'react';
import { Alert, Button, Card, CardContent, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle, Grid, Box, Stack, Chip, TextField, Typography } from '@mui/material';
import EmailRoundedIcon from '@mui/icons-material/EmailRounded';
import PictureAsPdfRoundedIcon from '@mui/icons-material/PictureAsPdfRounded';
import SendRoundedIcon from '@mui/icons-material/SendRounded';
import SlackIcon from '@mui/icons-material/TagRounded';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function WeeklyDigestPage() {
  const [notificationType, setNotificationType] = useState(null);
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('Weekly quality digest: quality score 88/100, pass rate 92%, and 14 total failures.');
  const [notificationState, setNotificationState] = useState({ status: 'idle', text: '' });

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

  const closeNotificationDialog = () => {
    if (notificationState.status !== 'loading') {
      setNotificationType(null);
      setNotificationState({ status: 'idle', text: '' });
    }
  };

  const openNotificationDialog = (type) => {
    setNotificationType(type);
    setNotificationState({ status: 'idle', text: '' });
  };

  const sendNotification = async () => {
    setNotificationState({ status: 'loading', text: '' });
    const params = new URLSearchParams();
    let endpoint;

    if (notificationType === 'email') {
      if (!email.trim()) {
        setNotificationState({ status: 'error', text: 'Enter an email address before sending.' });
        return;
      }
      endpoint = `${API_URL}/notify/email`;
      params.set('subject', 'Weekly Quality Digest');
      params.set('html_body', `<h1>Weekly Quality Digest</h1><p>Quality score: ${digest.quality_score}/100</p><p>Pass rate: ${digest.pass_rate}%</p><p>Failure rate: ${digest.fail_rate}%</p>`);
      params.set('to_address', email.trim());
    } else {
      if (!message.trim()) {
        setNotificationState({ status: 'error', text: 'Enter a message before sending.' });
        return;
      }
      endpoint = `${API_URL}/notify/slack`;
      params.set('message', message.trim());
    }

    try {
      const response = await fetch(`${endpoint}?${params.toString()}`, { method: 'POST' });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(result.detail || 'The notification could not be sent.');
      }
      setNotificationState({ status: 'success', text: `${notificationType === 'email' ? 'Email' : 'Slack message'} sent successfully.` });
    } catch (error) {
      setNotificationState({ status: 'error', text: error.message || 'The backend is unavailable.' });
    }
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
                <Button variant="contained" startIcon={<PictureAsPdfRoundedIcon />}>Export PDF</Button>
                <Button variant="outlined" startIcon={<EmailRoundedIcon />} onClick={() => openNotificationDialog('email')}>Email</Button>
                <Button variant="outlined" startIcon={<SlackIcon />} onClick={() => openNotificationDialog('slack')}>Slack</Button>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Dialog open={Boolean(notificationType)} onClose={closeNotificationDialog} fullWidth maxWidth="sm">
        <DialogTitle>{notificationType === 'email' ? 'Email weekly digest' : 'Send digest to Slack'}</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ pt: 1 }}>
            {notificationType === 'email' ? (
              <TextField
                autoFocus
                label="Recipient email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="recipient@example.com"
                fullWidth
              />
            ) : (
              <TextField
                autoFocus
                label="Message"
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                multiline
                minRows={3}
                fullWidth
              />
            )}
            {notificationState.status === 'error' && <Alert severity="error">{notificationState.text}</Alert>}
            {notificationState.status === 'success' && <Alert severity="success">{notificationState.text}</Alert>}
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={closeNotificationDialog} disabled={notificationState.status === 'loading'}>Cancel</Button>
          <Button variant="contained" onClick={sendNotification} disabled={notificationState.status === 'loading'} startIcon={notificationState.status === 'loading' ? <CircularProgress size={18} color="inherit" /> : <SendRoundedIcon />}>
            Send
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default WeeklyDigestPage;
