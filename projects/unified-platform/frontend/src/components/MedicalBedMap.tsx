/**
 * 医療用ベッドマップ・病棟表示風（レーダー風）
 */
import React from 'react';
import { Box, Typography } from '@mui/material';

const MAP_COLOR = '#00e676';
const MAP_BG = '#0a0e14';

interface Patient {
  patient_id: string;
  heart_rate?: number;
  blood_pressure?: string;
  spo2?: number;
}

interface MedicalBedMapProps {
  patients: Patient[];
  aiStatus?: Record<string, string>;
}

export const MedicalBedMap: React.FC<MedicalBedMapProps> = ({ patients, aiStatus = {} }) => {
  const grid = Array.from({ length: 12 }, (_, i) => {
    const p = patients[i];
    const status = p ? (aiStatus[p.patient_id] || 'Monitor') : null;
    return { id: `B${i + 1}`, patient: p, status };
  });

  return (
    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
      <Box
        sx={{
          flex: '1 1 400px',
          minWidth: 320,
          bgcolor: MAP_BG,
          border: `2px solid ${MAP_COLOR}`,
          borderRadius: 1,
          p: 2,
          boxShadow: `0 0 20px ${MAP_COLOR}30`,
        }}
      >
        <Typography sx={{ fontFamily: 'monospace', fontSize: 12, color: MAP_COLOR, mb: 1.5 }}>
          WARD STATUS | BED MAP
        </Typography>
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 1 }}>
          {grid.map(({ id, patient, status }) => (
            <Box
              key={id}
              sx={{
                p: 1,
                border: `1px solid ${MAP_COLOR}`,
                borderRadius: 0.5,
                opacity: patient ? 1 : 0.4,
              }}
            >
              <Typography sx={{ fontSize: 10, color: MAP_COLOR }}>{id}</Typography>
              {patient ? (
                <>
                  <Typography sx={{ fontSize: 11, color: MAP_COLOR, fontFamily: 'monospace' }}>{patient.patient_id}</Typography>
                  <Typography sx={{ fontSize: 9, color: `${MAP_COLOR}99` }}>HR:{patient.heart_rate ?? '-'} SpO2:{patient.spo2 ?? '-'}</Typography>
                  <Typography sx={{ fontSize: 9, color: status === 'Review' ? '#ff9800' : MAP_COLOR }}>{status}</Typography>
                </>
              ) : (
                <Typography sx={{ fontSize: 9, color: `${MAP_COLOR}66` }}>--</Typography>
              )}
            </Box>
          ))}
        </Box>
      </Box>
    </Box>
  );
};
