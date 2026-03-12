/**
 * 医療用バイタルモニター・波形表示風パネル（異常時アラート付き）
 */
import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import { Warning } from '@mui/icons-material';

const MONITOR_COLOR = '#00e676';
const MONITOR_BG = '#0a0e14';
const ALERT_COLOR = '#ff5252';

interface VitalSign {
  patient_id: string;
  heart_rate: number;
  blood_pressure: string;
  spo2: number;
}

interface MedicalVitalMonitorProps {
  vitals: VitalSign[];
}

function parseBP(bp: string): { sys: number; dia: number } {
  const m = bp?.match(/(\d+)\s*\/\s*(\d+)/);
  return m ? { sys: +m[1], dia: +m[2] } : { sys: 0, dia: 0 };
}

function isVitalAbnormal(v: VitalSign): { alert: boolean; reasons: string[] } {
  const reasons: string[] = [];
  if (v.heart_rate > 100 || v.heart_rate < 50) reasons.push('HR');
  if (v.spo2 < 95) reasons.push('SpO2');
  const { sys, dia } = parseBP(v.blood_pressure);
  if (sys > 160 || dia > 100 || (sys > 0 && sys < 90)) reasons.push('BP');
  return { alert: reasons.length > 0, reasons };
}

// 簡易波形データ（ECG風）
function generateWavePoints(count: number, base: number, amp: number): string {
  const pts: string[] = [];
  for (let i = 0; i < count; i++) {
    const x = (i / count) * 400;
    const y = base + amp * Math.sin((i / 20) * Math.PI) * (i % 25 < 5 ? 0.3 : 1);
    pts.push(`${x},${y}`);
  }
  return pts.join(' ');
}

export const MedicalVitalMonitor: React.FC<MedicalVitalMonitorProps> = ({ vitals }) => {
  return (
    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
      {vitals.slice(0, 4).map((v, i) => {
        const { alert, reasons } = isVitalAbnormal(v);
        const borderColor = alert ? ALERT_COLOR : MONITOR_COLOR;
        const boxShadow = alert ? `0 0 20px ${ALERT_COLOR}60` : `0 0 15px ${MONITOR_COLOR}30`;
        return (
        <Box
          key={`${v.patient_id}-${i}`}
          sx={{
            flex: '1 1 280px',
            minWidth: 260,
            bgcolor: MONITOR_BG,
            border: `2px solid ${borderColor}`,
            borderRadius: 1,
            p: 1.5,
            boxShadow,
            animation: alert ? 'pulse 2s ease-in-out infinite' : 'none',
            '@keyframes pulse': { '0%,100%': { boxShadow }, '50%': { boxShadow: `0 0 30px ${ALERT_COLOR}90` } },
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
            <Typography sx={{ fontFamily: 'monospace', fontSize: 11, color: borderColor }}>
              PATIENT: {v.patient_id}
            </Typography>
            {alert && <Chip size="small" icon={<Warning />} label={`要観察: ${reasons.join(',')}`} color="error" sx={{ fontSize: 10 }} />}
          </Box>
          <Box sx={{ display: 'flex', gap: 2, mb: 1 }}>
            <Box>
              <Typography sx={{ fontSize: 9, color: `${borderColor}99` }}>HR</Typography>
              <Typography sx={{ fontFamily: 'monospace', fontSize: 18, color: reasons.includes('HR') ? ALERT_COLOR : borderColor, fontWeight: 600 }}>
                {v.heart_rate}
              </Typography>
              <Typography sx={{ fontSize: 9, color: `${MONITOR_COLOR}99` }}>bpm</Typography>
            </Box>
            <Box>
              <Typography sx={{ fontSize: 9, color: `${borderColor}99` }}>BP</Typography>
              <Typography sx={{ fontFamily: 'monospace', fontSize: 18, color: reasons.includes('BP') ? ALERT_COLOR : borderColor, fontWeight: 600 }}>
                {v.blood_pressure}
              </Typography>
              <Typography sx={{ fontSize: 9, color: `${MONITOR_COLOR}99` }}>mmHg</Typography>
            </Box>
            <Box>
              <Typography sx={{ fontSize: 9, color: `${borderColor}99` }}>SpO2</Typography>
              <Typography sx={{ fontFamily: 'monospace', fontSize: 18, color: reasons.includes('SpO2') ? ALERT_COLOR : borderColor, fontWeight: 600 }}>
                {v.spo2}
              </Typography>
              <Typography sx={{ fontSize: 9, color: `${MONITOR_COLOR}99` }}>%</Typography>
            </Box>
          </Box>
          {/* 波形表示（ECG風） */}
          <Box sx={{ height: 50, position: 'relative', overflow: 'hidden' }}>
            <svg width="100%" height="50" viewBox="0 0 400 50" preserveAspectRatio="none">
              <polyline
                fill="none"
                stroke={alert ? ALERT_COLOR : MONITOR_COLOR}
                strokeWidth="0.5"
                points={generateWavePoints(100, 25, 12)}
              />
            </svg>
          </Box>
        </Box>
        );
      })}
    </Box>
  );
};
