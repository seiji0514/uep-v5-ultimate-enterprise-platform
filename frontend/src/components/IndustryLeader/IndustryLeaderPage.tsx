/**
 * Level 4 インダストリーリーダーページ
 * グローバルスケール、最先端技術、業界標準
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Language,
  Cloud,
  Science,
  Description,
  Psychology,
  Hub,
  Policy,
  PhoneAndroid,
  Business,
} from '@mui/icons-material';
import { industryLeaderApi, Level4Overview } from '../../api/industryLeader';

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

export const IndustryLeaderPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [overview, setOverview] = useState<Level4Overview | null>(null);
  const [cdnConfig, setCdnConfig] = useState<any>(null);
  const [i18nConfig, setI18nConfig] = useState<any>(null);
  const [aiConfig, setAiConfig] = useState<any>(null);
  const [standardConfig, setStandardConfig] = useState<any>(null);
  const [reasoningAiConfig, setReasoningAiConfig] = useState<any>(null);
  const [mcpA2aConfig, setMcpA2aConfig] = useState<any>(null);
  const [governanceConfig, setGovernanceConfig] = useState<any>(null);
  const [onDeviceAiConfig, setOnDeviceAiConfig] = useState<any>(null);
  const [businessDomainConfig, setBusinessDomainConfig] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      const [overviewRes, cdnRes, i18nRes, aiRes, standardRes, reasoningRes, mcpRes, govRes, onDeviceRes, businessRes] = await Promise.all([
        industryLeaderApi.getOverview(),
        industryLeaderApi.getGlobalCdnConfig(),
        industryLeaderApi.getMultilingualConfig(),
        industryLeaderApi.getCuttingEdgeAiConfig(),
        industryLeaderApi.getIndustryStandard(),
        industryLeaderApi.getReasoningAiConfig(),
        industryLeaderApi.getMcpA2aConfig(),
        industryLeaderApi.getGovernanceWorkflowConfig(),
        industryLeaderApi.getOnDeviceAiConfig(),
        industryLeaderApi.getBusinessDomainConfig(),
      ]);
      setOverview(overviewRes);
      setCdnConfig(cdnRes);
      setI18nConfig(i18nRes);
      setAiConfig(aiRes);
      setStandardConfig(standardRes);
      setReasoningAiConfig(reasoningRes);
      setMcpA2aConfig(mcpRes);
      setGovernanceConfig(govRes);
      setOnDeviceAiConfig(onDeviceRes);
      setBusinessDomainConfig(businessRes);
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } }; message?: string };
      setError(e.response?.data?.detail || e.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Level 4 インダストリーリーダー
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 1 }}>
        グローバルスケール、最先端技術、業界標準の確立
      </Typography>
      <Chip label="設計・アーキテクチャ（組織・運用は除外）" size="small" color="info" sx={{ mb: 2 }} />

      {overview && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>グローバルCDN</Typography>
                <Typography variant="h6">{overview.features.global_scale.cdn ? '有効' : '-'}</Typography>
                <Typography variant="caption">多言語: {overview.features.global_scale.multilingual}言語</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>最先端AI技術</Typography>
                <Typography variant="h4">{overview.features.cutting_edge_ai.technologies_count}</Typography>
                <Typography variant="caption">技術統合</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>業界標準仕様</Typography>
                <Typography variant="h4">{overview.features.industry_standard.specs_count}</Typography>
                <Typography variant="caption">標準策定</Typography>
              </CardContent>
            </Card>
          </Grid>
          {overview.features.business_domains && (
            <Grid item xs={12} sm={6} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>ビジネス領域</Typography>
                  <Typography variant="h4">{overview.features.business_domains.domains_count}</Typography>
                  <Typography variant="caption">DX・EX・CX・UX等</Typography>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}

      <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)} variant="scrollable" scrollButtons="auto">
        <Tab icon={<Cloud />} iconPosition="start" label="グローバルCDN" />
        <Tab icon={<Language />} iconPosition="start" label="多言語対応" />
        <Tab icon={<Science />} iconPosition="start" label="最先端AI" />
        <Tab icon={<Psychology />} iconPosition="start" label="推論AI/MCP/ガバナンス/端末内" />
        <Tab icon={<Business />} iconPosition="start" label="ビジネス領域" />
        <Tab icon={<Description />} iconPosition="start" label="業界標準" />
      </Tabs>

      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {loading && <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>}

      {!loading && (
        <>
          <TabPanel value={tabValue} index={0}>
            {cdnConfig && (
              <Card>
                <CardContent>
                  <Typography variant="h6">プロバイダ: {cdnConfig.provider}</Typography>
                  <Typography variant="body2">エッジロケーション: {cdnConfig.edge_locations}箇所</Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>カバー: {cdnConfig.regions_covered?.join(', ')}</Typography>
                  <TableContainer sx={{ mt: 2 }}>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>機能</TableCell>
                          <TableCell>ステータス</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {cdnConfig.features?.map((f: any) => (
                          <TableRow key={f.name}>
                            <TableCell>{f.name}</TableCell>
                            <TableCell><Chip label={f.status} size="small" /></TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            {i18nConfig && (
              <Card>
                <CardContent>
                  <Typography variant="h6">対応言語: {i18nConfig.supported_languages?.length}言語</Typography>
                  <Typography variant="body2">デフォルト: {i18nConfig.default_locale}</Typography>
                  <Typography variant="body2">APIヘッダー: {i18nConfig.api_header}</Typography>
                  <TableContainer sx={{ mt: 2 }}>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>コード</TableCell>
                          <TableCell>言語</TableCell>
                          <TableCell>ロケール</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {i18nConfig.supported_languages?.map((l: any) => (
                          <TableRow key={l.code}>
                            <TableCell>{l.code}</TableCell>
                            <TableCell>{l.name}</TableCell>
                            <TableCell>{l.locale}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            {aiConfig && (
              <Box>
                <Typography variant="h6" gutterBottom>最先端AI/ML技術</Typography>
                <Grid container spacing={2}>
                  {aiConfig.technologies?.map((t: any) => (
                    <Grid item xs={12} sm={6} md={4} key={t.name}>
                      <Card>
                        <CardContent>
                          <Typography variant="subtitle2">{t.name}</Typography>
                          <Chip label={t.status} size="small" color={t.status === 'integrated' ? 'success' : 'default'} sx={{ mt: 0.5 }} />
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
                <Typography variant="h6" sx={{ mt: 2 }}>イノベーション領域</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                  {aiConfig.innovation_areas?.map((a: string) => (
                    <Chip key={a} label={a} size="small" variant="outlined" />
                  ))}
                </Box>
              </Box>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Box>
              <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>2025-2026 最新技術（4技術統合）</Typography>
              <Grid container spacing={2}>
                {reasoningAiConfig && (
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <Psychology color="primary" />
                          <Typography variant="h6">推論AI（o1系）</Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>{reasoningAiConfig.description}</Typography>
                        <Typography variant="caption" display="block" sx={{ mb: 1 }}>戦略: {reasoningAiConfig.routing_strategy}</Typography>
                        <TableContainer>
                          <Table size="small">
                            <TableBody>
                              {reasoningAiConfig.features?.map((f: any) => (
                                <TableRow key={f.name}>
                                  <TableCell>{f.name}</TableCell>
                                  <TableCell><Chip label={f.status} size="small" color={f.status === 'integrated' ? 'success' : 'default'} /></TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                )}
                {mcpA2aConfig && (
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <Hub color="primary" />
                          <Typography variant="h6">MCP / A2A</Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>{mcpA2aConfig.description}</Typography>
                        <TableContainer>
                          <Table size="small">
                            <TableBody>
                              {mcpA2aConfig.protocols?.map((p: any) => (
                                <TableRow key={p.name}>
                                  <TableCell>{p.name}</TableCell>
                                  <TableCell><Chip label={p.status} size="small" color="success" /></TableCell>
                                </TableRow>
                              ))}
                              {mcpA2aConfig.features?.map((f: any) => (
                                <TableRow key={f.name}>
                                  <TableCell>{f.name}</TableCell>
                                  <TableCell><Chip label={f.status} size="small" /></TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                )}
                {governanceConfig && (
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <Policy color="primary" />
                          <Typography variant="h6">ガバナンス・ワークフロー</Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>{governanceConfig.description}</Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 1 }}>
                          {governanceConfig.compliance?.map((c: string) => (
                            <Chip key={c} label={c} size="small" variant="outlined" />
                          ))}
                        </Box>
                        <TableContainer>
                          <Table size="small">
                            <TableBody>
                              {governanceConfig.features?.map((f: any) => (
                                <TableRow key={f.name}>
                                  <TableCell>{f.name}</TableCell>
                                  <TableCell><Chip label={f.status} size="small" color="success" /></TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                )}
                {onDeviceAiConfig && (
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <PhoneAndroid color="primary" />
                          <Typography variant="h6">端末内AI（オンデバイス）</Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>{onDeviceAiConfig.description}</Typography>
                        <TableContainer>
                          <Table size="small">
                            <TableBody>
                              {onDeviceAiConfig.architecture?.map((a: any) => (
                                <TableRow key={a.layer}>
                                  <TableCell>{a.layer}</TableCell>
                                  <TableCell>{a.purpose}</TableCell>
                                  <TableCell><Chip label={a.status} size="small" color="success" /></TableCell>
                                </TableRow>
                              ))}
                              {onDeviceAiConfig.features?.map((f: any) => (
                                <TableRow key={f.name}>
                                  <TableCell>{f.name}</TableCell>
                                  <TableCell><Chip label={f.status} size="small" color="success" /></TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                )}
              </Grid>
            </Box>
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            {businessDomainConfig && (
              <Box>
                <Typography variant="h6" gutterBottom>{businessDomainConfig.description}</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>{businessDomainConfig.integration_approach}</Typography>
                <Grid container spacing={2}>
                  {businessDomainConfig.domains?.map((d: any) => (
                    <Grid item xs={12} sm={6} md={4} key={d.id}>
                      <Card>
                        <CardContent>
                          <Typography variant="subtitle1" fontWeight="bold">{d.name}</Typography>
                          <Typography variant="caption" color="text.secondary" display="block">{d.full_name}</Typography>
                          <Typography variant="body2" sx={{ mt: 0.5 }}>{d.description}</Typography>
                          <Chip label={d.status} size="small" color="success" sx={{ mt: 1 }} />
                          <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {d.features?.map((f: string) => (
                              <Chip key={f} label={f} size="small" variant="outlined" />
                            ))}
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={5}>
            {standardConfig && (
              <Card>
                <CardContent>
                  <Typography variant="h6">{standardConfig.name} v{standardConfig.version}</Typography>
                  <TableContainer sx={{ mt: 2 }}>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>ID</TableCell>
                          <TableCell>タイトル</TableCell>
                          <TableCell>説明</TableCell>
                          <TableCell>ステータス</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {standardConfig.specifications?.map((s: any) => (
                          <TableRow key={s.id}>
                            <TableCell>{s.id}</TableCell>
                            <TableCell>{s.title}</TableCell>
                            <TableCell>{s.description}</TableCell>
                            <TableCell><Chip label={s.status} size="small" /></TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            )}
          </TabPanel>
        </>
      )}
    </Box>
  );
};
