/**
 * 患者タイムライン - AI診断・バイタル記録の時系列表示
 */
import React, { useMemo } from 'react';
import { Box, Typography, Paper, Chip } from '@mui/material';
import { Psychology, MonitorHeart } from '@mui/icons-material';

interface TimelineItem {
  id: string;
  type: 'ai' | 'vital';
  patient_id: string;
  timestamp: string;
  label: string;
  detail?: string;
}

interface MedicalPatientTimelineProps {
  ai: any[];
  vital: any[];
  patientMap: Record<string, any>;
}

export const MedicalPatientTimeline: React.FC<MedicalPatientTimelineProps> = ({ ai, vital, patientMap }) => {
  const items: TimelineItem[] = useMemo(() => {
    const list: TimelineItem[] = [];
    (ai || []).forEach((r: any) => {
      list.push({
        id: r.id,
        type: 'ai',
        patient_id: r.patient_id,
        timestamp: r.created_at || new Date().toISOString(),
        label: r.finding,
        detail: `信頼度 ${((r.confidence || 0) * 100).toFixed(0)}% / ${r.status}`,
      });
    });
    (vital || []).forEach((v: any, i: number) => {
      list.push({
        id: `v-${v.patient_id}-${i}`,
        type: 'vital',
        patient_id: v.patient_id,
        timestamp: v.timestamp || new Date().toISOString(),
        label: `HR ${v.heart_rate} / BP ${v.blood_pressure} / SpO2 ${v.spo2}%`,
        detail: 'バイタル記録',
      });
    });
    list.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
    return list.slice(0, 20);
  }, [ai, vital]);

  return (
    <Box sx={{ maxHeight: 400, overflow: 'auto' }}>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        患者ごとのAI診断・バイタル記録を時系列で表示（直近20件）
      </Typography>
      {items.map((item) => {
        const name = patientMap[item.patient_id] ? `${patientMap[item.patient_id].family_name} ${patientMap[item.patient_id].given_name}` : item.patient_id;
        const date = new Date(item.timestamp);
        const timeStr = date.toLocaleString('ja-JP', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        return (
          <Paper key={item.id} elevation={0} sx={{ p: 1.5, mb: 1, borderLeft: 3, borderColor: item.type === 'ai' ? 'primary.main' : 'success.main' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
              {item.type === 'ai' ? <Psychology fontSize="small" color="primary" /> : <MonitorHeart fontSize="small" color="success" />}
              <Chip size="small" label={item.type === 'ai' ? 'AI診断' : 'バイタル'} variant="outlined" color={item.type === 'ai' ? 'primary' : 'success'} />
              <Typography variant="caption" color="text.secondary">{name} ({item.patient_id})</Typography>
              <Typography variant="caption" color="text.secondary">{timeStr}</Typography>
            </Box>
            <Typography variant="body2" sx={{ mt: 0.5 }}>{item.label}</Typography>
            {item.detail && <Typography variant="caption" color="text.secondary">{item.detail}</Typography>}
          </Paper>
        );
      })}
      {items.length === 0 && <Typography variant="body2" color="text.secondary">データがありません</Typography>}
    </Box>
  );
};
