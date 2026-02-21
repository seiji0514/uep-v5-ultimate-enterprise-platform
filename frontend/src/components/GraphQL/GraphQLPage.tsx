/**
 * GraphQL クライアントページ
 * クエリを実行して結果を表示
 */
import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import { Send, Code } from '@mui/icons-material';
import { graphqlQuery, QUERIES, GraphQLResponse } from '../../api/graphql';

export const GraphQLPage: React.FC = () => {
  const [query, setQuery] = useState(QUERIES.hello);
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExecute = async () => {
    setLoading(true);
    setError(null);
    setResult('');
    try {
      const res: GraphQLResponse<unknown> = await graphqlQuery(query);
      if (res.errors && res.errors.length > 0) {
        setError(res.errors.map((e) => e.message).join(', '));
      } else {
        setResult(JSON.stringify(res.data, null, 2));
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const insertExample = (q: string) => setQuery(q);

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        GraphQL クライアント
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        /graphql エンドポイントにクエリを送信して結果を確認できます。
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              クエリ例
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
              <Button
                size="small"
                variant="outlined"
                startIcon={<Code />}
                onClick={() => insertExample(QUERIES.hello)}
              >
                hello
              </Button>
              <Button
                size="small"
                variant="outlined"
                onClick={() => insertExample(QUERIES.health)}
              >
                health
              </Button>
              <Button
                size="small"
                variant="outlined"
                onClick={() => insertExample(QUERIES.services)}
              >
                services
              </Button>
            </Box>
            <TextField
              fullWidth
              multiline
              rows={8}
              label="GraphQL クエリ"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="query { hello }"
              sx={{ fontFamily: 'monospace' }}
            />
            <Button
              variant="contained"
              startIcon={loading ? <CircularProgress size={20} /> : <Send />}
              onClick={handleExecute}
              disabled={loading}
              sx={{ mt: 2 }}
            >
              実行
            </Button>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                結果
              </Typography>
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}
              {result ? (
                <Box
                  component="pre"
                  sx={{
                    p: 2,
                    bgcolor: 'grey.100',
                    borderRadius: 1,
                    overflow: 'auto',
                    fontFamily: 'monospace',
                    fontSize: '0.85rem',
                  }}
                >
                  {result}
                </Box>
              ) : (
                <Typography color="text.secondary">
                  クエリを実行すると結果がここに表示されます。
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
