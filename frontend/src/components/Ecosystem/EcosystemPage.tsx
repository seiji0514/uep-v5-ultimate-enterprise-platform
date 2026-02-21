/**
 * Level 3 エコシステムページ
 * パートナー統合、コミュニティ機能、業界標準
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Tabs,
  Tab,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Groups,
  Store,
  Storage,
  Forum,
  Description,
  Download,
} from '@mui/icons-material';
import { ecosystemApi, EcosystemOverview, Partner, MarketplaceItem, SharedModel, ForumPost } from '../../api/ecosystem';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  );
}

export const EcosystemPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [overview, setOverview] = useState<EcosystemOverview | null>(null);
  const [partners, setPartners] = useState<Partner[]>([]);
  const [marketplaceItems, setMarketplaceItems] = useState<MarketplaceItem[]>([]);
  const [sharedModels, setSharedModels] = useState<SharedModel[]>([]);
  const [forumPosts, setForumPosts] = useState<ForumPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [overviewRes, partnersRes, marketplaceRes, modelsRes, postsRes] = await Promise.all([
        ecosystemApi.getOverview(),
        ecosystemApi.getPartners(),
        ecosystemApi.getMarketplaceItems(),
        ecosystemApi.getSharedModels(),
        ecosystemApi.getForumPosts(),
      ]);
      setOverview(overviewRes);
      setPartners(partnersRes);
      setMarketplaceItems(marketplaceRes);
      setSharedModels(modelsRes);
      setForumPosts(postsRes);
    } catch (err: unknown) {
      const e = err as { response?: { status?: number; data?: { detail?: string } }; message?: string };
      setError(e.response?.data?.detail || e.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return 'success';
      case 'pending': return 'warning';
      case 'rejected': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Level 3 エコシステム
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
        パートナー統合、コミュニティ機能、業界標準の確立
      </Typography>

      {overview && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>パートナー</Typography>
                <Typography variant="h4">{overview.features.partner_integration.partners_count}</Typography>
                <Typography variant="caption">マーケットプレイス: {overview.features.partner_integration.marketplace_count}件</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>共有モデル</Typography>
                <Typography variant="h4">{overview.features.community.shared_models_count}</Typography>
                <Typography variant="caption">フォーラム: {overview.features.community.forum_posts_count}件</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>業界標準</Typography>
                <Typography variant="h6">標準API仕様</Typography>
                <Typography variant="caption">OpenAPI 3.0 準拠</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
        <Tab icon={<Groups />} iconPosition="start" label="パートナー" />
        <Tab icon={<Store />} iconPosition="start" label="マーケットプレイス" />
        <Tab icon={<Storage />} iconPosition="start" label="共有モデル" />
        <Tab icon={<Forum />} iconPosition="start" label="コミュニティフォーラム" />
        <Tab icon={<Description />} iconPosition="start" label="標準API仕様" />
      </Tabs>

      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {loading && <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>}

      {!loading && (
        <>
          <TabPanel value={tabValue} index={0}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>組織名</TableCell>
                    <TableCell>連絡先</TableCell>
                    <TableCell>ステータス</TableCell>
                    <TableCell>登録日</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {partners.map((p) => (
                    <TableRow key={p.id}>
                      <TableCell>{p.organization}</TableCell>
                      <TableCell>{p.contact_email}</TableCell>
                      <TableCell><Chip label={p.status} color={getStatusColor(p.status) as any} size="small" /></TableCell>
                      <TableCell>{new Date(p.created_at).toLocaleDateString('ja-JP')}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={2}>
              {marketplaceItems.map((item) => (
                <Grid item xs={12} sm={6} md={4} key={item.id}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">{item.name}</Typography>
                      <Typography variant="body2" color="text.secondary">{item.description}</Typography>
                      <Box sx={{ mt: 1 }}>
                        <Chip label={item.category} size="small" sx={{ mr: 0.5 }} />
                        <Chip label={item.price_type} size="small" color="success" />
                      </Box>
                      <Typography variant="caption">提供: {item.partner_name} / DL: {item.download_count}</Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" startIcon={<Download />}>ダウンロード</Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <Grid container spacing={2}>
              {sharedModels.map((m) => (
                <Grid item xs={12} sm={6} md={4} key={m.id}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">{m.name}</Typography>
                      <Typography variant="body2" color="text.secondary">{m.description}</Typography>
                      <Box sx={{ mt: 1 }}>
                        <Chip label={m.model_type} size="small" sx={{ mr: 0.5 }} />
                        <Chip label={m.source} size="small" />
                      </Box>
                      <Typography variant="caption">作成: {m.created_by} / DL: {m.download_count}</Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" startIcon={<Download />}>ダウンロード</Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Grid container spacing={2}>
              {forumPosts.map((post) => (
                <Grid item xs={12} key={post.id}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">{post.title}</Typography>
                      <Typography variant="body2" color="text.secondary">{post.content}</Typography>
                      <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                        <Chip label={post.category} size="small" />
                        <Typography variant="caption">by {post.author}</Typography>
                        <Typography variant="caption">コメント: {post.comment_count} / いいね: {post.likes}</Typography>
                      </Box>
                    </CardContent>
                    <CardActions>
                      <Button size="small">コメントを見る</Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            <Card>
              <CardContent>
                <Typography variant="h6">UEP Ecosystem Standard API</Typography>
                <Typography variant="body2" paragraph>
                  UEP v5.0 Level 3 エコシステムの標準API仕様。OpenAPI 3.0 準拠。
                </Typography>
                <Typography variant="body2" paragraph>
                  エンドポイント: <code>/api/v1/ecosystem/standard-api-spec</code>
                </Typography>
                <Button
                  variant="contained"
                  href="http://localhost:8000/api/v1/ecosystem/standard-api-spec"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  仕様を表示
                </Button>
              </CardContent>
            </Card>
          </TabPanel>
        </>
      )}
    </Box>
  );
};
