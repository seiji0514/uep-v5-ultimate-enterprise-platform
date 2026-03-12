/**
 * 教育 ページ
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Chip,
  LinearProgress,
} from '@mui/material';
import { School, Timeline, Grade } from '@mui/icons-material';
import { educationApi, Course, LearningProgress, Grade as GradeType } from '../../api/education';

function TabPanel({ children, value, index }: { children?: React.ReactNode; index: number; value: number }) {
  return <div role="tabpanel" hidden={value !== index}>{value === index && <Box sx={{ p: 2 }}>{children}</Box>}</div>;
}

export const EducationPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [courses, setCourses] = useState<Course[]>([]);
  const [progress, setProgress] = useState<LearningProgress[]>([]);
  const [grades, setGrades] = useState<GradeType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [tabValue]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      if (tabValue === 0) setCourses(await educationApi.getCourses());
      else if (tabValue === 1) setProgress(await educationApi.getLearningProgress());
      else setGrades(await educationApi.getGrades());
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'データの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 0 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h5" fontWeight={600} gutterBottom>教育</Typography>
        <Typography variant="body2" color="text.secondary">LMS、学習進捗、成績、教材管理</Typography>
      </Box>
      <Paper elevation={0}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab icon={<School />} iconPosition="start" label="コース" />
          <Tab icon={<Timeline />} iconPosition="start" label="学習進捗" />
          <Tab icon={<Grade />} iconPosition="start" label="成績" />
        </Tabs>
        {error && <Alert severity="error" sx={{ m: 2 }} onClose={() => setError('')}>{error}</Alert>}
        {loading ? <Box sx={{ p: 4, textAlign: 'center' }}><CircularProgress /></Box> : (
          <>
            <TabPanel value={tabValue} index={0}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>コース</TableCell><TableCell>ステータス</TableCell><TableCell>受講者</TableCell><TableCell>完了率</TableCell></TableRow></TableHead>
                  <TableBody>
                    {courses.map((c) => (
                      <TableRow key={c.id}><TableCell>{c.title}</TableCell><TableCell><Chip label={c.status} size="small" /></TableCell><TableCell>{c.enrolled}</TableCell><TableCell><LinearProgress variant="determinate" value={c.completion_rate * 100} sx={{ width: 80 }} /> {(c.completion_rate * 100).toFixed(0)}%</TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>受講者</TableCell><TableCell>コース</TableCell><TableCell>進捗</TableCell><TableCell>最終アクセス</TableCell></TableRow></TableHead>
                  <TableBody>
                    {progress.map((p, i) => (
                      <TableRow key={i}><TableCell>{p.student_id}</TableCell><TableCell>{p.course}</TableCell><TableCell><LinearProgress variant="determinate" value={p.progress} sx={{ width: 80 }} /> {p.progress}%</TableCell><TableCell>{new Date(p.last_accessed).toLocaleString('ja-JP')}</TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              <TableContainer>
                <Table size="small">
                  <TableHead><TableRow><TableCell>受講者</TableCell><TableCell>コース</TableCell><TableCell>スコア</TableCell><TableCell>評価</TableCell></TableRow></TableHead>
                  <TableBody>
                    {grades.map((g, i) => (
                      <TableRow key={i}><TableCell>{g.student_id}</TableCell><TableCell>{g.course}</TableCell><TableCell>{g.score}</TableCell><TableCell><Chip label={g.grade} size="small" color={g.grade === 'A' ? 'success' : 'default'} /></TableCell></TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
          </>
        )}
      </Paper>
    </Box>
  );
};
