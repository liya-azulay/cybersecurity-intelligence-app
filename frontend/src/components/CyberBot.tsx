import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';

interface BotMessage {
  id: string;
  type: 'user' | 'bot';
  message: string;
  timestamp: Date;
  success?: boolean;
  commandType?: string;
}

interface BotResponse {
  success: boolean;
  message: string;
  data?: any;
  command_type: string;
  timestamp: string;
}

const CyberBot: React.FC = () => {
  const [messages, setMessages] = useState<BotMessage[]>([
    {
      id: '1',
      type: 'bot',
      message: '🤖 **Welcome to Cyber Bot!**\n\nI can help you with:\n• 🔍 Search attack patterns\n• 🛡️ Check file hashes with VirusTotal\n• 📊 Get statistics\n• ❓ Provide help\n\nType `help` to see all commands!',
      timestamp: new Date(),
      success: true,
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: BotMessage = {
      id: Date.now().toString(),
      type: 'user',
      message: inputMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/bot/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          user_id: 'user_1',
          session_id: 'session_1',
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const botResponse: BotResponse = await response.json();

      const botMessage: BotMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        message: botResponse.message,
        timestamp: new Date(botResponse.timestamp),
        success: botResponse.success,
        commandType: botResponse.command_type,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      const errorMessage: BotMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        message: '❌ **Error:** Unable to connect to the bot. Please make sure the backend server is running.',
        timestamp: new Date(),
        success: false,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: '1',
        type: 'bot',
        message: '🤖 **Welcome to Cyber Bot!**\n\nI can help you with:\n• 🔍 Search attack patterns\n• 🛡️ Check file hashes with VirusTotal\n• 📊 Get statistics\n• ❓ Provide help\n\nType `help` to see all commands!',
        timestamp: new Date(),
        success: true,
      },
    ]);
    setError(null);
  };

  const formatMessage = (message: string) => {
    // Simple markdown-like formatting
    return message
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code style="background: #f5f5f5; padding: 2px 4px; border-radius: 3px; font-family: monospace;">$1</code>')
      .replace(/\n/g, '<br>');
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Paper sx={{ p: 2, mb: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
        <BotIcon color="primary" sx={{ fontSize: 32 }} />
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h6" component="h2">
            Cyber Bot
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Your AI cybersecurity assistant
          </Typography>
        </Box>
        <Button
          startIcon={<RefreshIcon />}
          onClick={clearChat}
          variant="outlined"
          size="small"
        >
          Clear Chat
        </Button>
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Messages */}
      <Paper sx={{ flexGrow: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
          <List>
            {messages.map((message, index) => (
              <React.Fragment key={message.id}>
                <ListItem
                  sx={{
                    flexDirection: 'column',
                    alignItems: message.type === 'user' ? 'flex-end' : 'flex-start',
                    px: 0,
                  }}
                >
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1,
                      mb: 1,
                      flexDirection: message.type === 'user' ? 'row-reverse' : 'row',
                    }}
                  >
                    {message.type === 'bot' ? (
                      <BotIcon color="primary" sx={{ fontSize: 20 }} />
                    ) : (
                      <PersonIcon color="action" sx={{ fontSize: 20 }} />
                    )}
                    <Typography variant="caption" color="text.secondary">
                      {message.type === 'bot' ? 'Cyber Bot' : 'You'} •{' '}
                      {message.timestamp.toLocaleTimeString()}
                    </Typography>
                    {message.commandType && (
                      <Chip
                        label={message.commandType}
                        size="small"
                        variant="outlined"
                        color={message.success ? 'success' : 'error'}
                      />
                    )}
                  </Box>
                  <Paper
                    sx={{
                      p: 2,
                      maxWidth: '80%',
                      backgroundColor: message.type === 'user' ? 'primary.main' : 'grey.100',
                      color: message.type === 'user' ? 'primary.contrastText' : 'text.primary',
                    }}
                  >
                    <Typography
                      variant="body1"
                      sx={{
                        whiteSpace: 'pre-wrap',
                        '& strong': { fontWeight: 'bold' },
                        '& em': { fontStyle: 'italic' },
                        '& code': {
                          backgroundColor: message.type === 'user' ? 'rgba(255,255,255,0.2)' : '#f5f5f5',
                          padding: '2px 4px',
                          borderRadius: '3px',
                          fontFamily: 'monospace',
                        },
                      }}
                      dangerouslySetInnerHTML={{
                        __html: formatMessage(message.message),
                      }}
                    />
                  </Paper>
                </ListItem>
                {index < messages.length - 1 && <Divider sx={{ my: 1 }} />}
              </React.Fragment>
            ))}
            {isLoading && (
              <ListItem sx={{ justifyContent: 'center' }}>
                <CircularProgress size={24} />
                <Typography variant="body2" sx={{ ml: 2 }}>
                  Cyber Bot is thinking...
                </Typography>
              </ListItem>
            )}
          </List>
          <div ref={messagesEndRef} />
        </Box>

        {/* Input */}
        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              multiline
              maxRows={4}
              placeholder="Ask me anything about cybersecurity... (e.g., 'search process injection' or 'check md5 5d41402abc4b2a76b9719d911017c592')"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              variant="outlined"
              size="small"
            />
            <IconButton
              color="primary"
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              sx={{ alignSelf: 'flex-end' }}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default CyberBot;
