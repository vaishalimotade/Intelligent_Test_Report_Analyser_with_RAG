import React from 'react';
import { Card, CardContent, Typography, Box, Stack, TextField, Button, Chip, List, ListItem, ListItemText, Divider } from '@mui/material';
import AutoAwesomeRoundedIcon from '@mui/icons-material/AutoAwesomeRounded';
import SendRoundedIcon from '@mui/icons-material/SendRounded';

const sampleQuestions = [
  'Why did PaymentTest fail?',
  'Show top flaky tests',
  'Which module is highest risk?',
  'Compare release quality',
];

function AssistantPanel() {
  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent>
        <Stack direction="row" alignItems="center" spacing={1} mb={2}>
          <Box sx={{ color: '#0078D4', display: 'flex', alignItems: 'center' }}>
            <AutoAwesomeRoundedIcon />
          </Box>
          <Box>
            <Typography variant="h6">GenAI Assistant</Typography>
            <Typography variant="body2" color="text.secondary">Ask about failures, trends, and recommendations.</Typography>
          </Box>
        </Stack>

        <Box sx={{ border: '1px solid #E5E7EB', borderRadius: 2, p: 2, mb: 2, bgcolor: 'rgba(0,120,212,0.05)' }}>
          <Typography variant="subtitle2" fontWeight={700} gutterBottom>
            Suggested prompts
          </Typography>
          <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
            {sampleQuestions.map((question) => (
              <Chip key={question} label={question} variant="outlined" size="small" sx={{ borderColor: '#D0E7FF', color: '#0078D4' }} />
            ))}
          </Stack>
        </Box>

        <List disablePadding sx={{ mb: 2 }}>
          <ListItem alignItems="flex-start" sx={{ px: 0 }}>
            <ListItemText
              primary="Payment module failures increased by 24% in the last 7 days."
              secondary="Historical analysis suggests API timeout patterns as the primary cause."
            />
          </ListItem>
          <Divider component="li" />
          <ListItem alignItems="flex-start" sx={{ px: 0 }}>
            <ListItemText
              primary="Top risk module: Payments"
              secondary="High-density failure clusters appear around checkout and billing retries."
            />
          </ListItem>
        </List>

        <Stack spacing={1.5}>
          <TextField fullWidth size="small" placeholder="Ask the assistant" />
          <Button variant="contained" endIcon={<SendRoundedIcon />} sx={{ alignSelf: 'flex-start' }}>
            Send
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}

export default AssistantPanel;
