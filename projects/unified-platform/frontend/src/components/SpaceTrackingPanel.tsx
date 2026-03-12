/**
 * 宇宙管制・衛星追跡風表示
 * NASAミッション管制・テレメトリ表示に近いレイアウト
 */
import React from 'react';
import { Box, Typography } from '@mui/material';

const TELEMETRY_COLOR = '#00d4ff'; // 宇宙管制風シアン
const TELEMETRY_BG = '#0a0e14';
const ACCENT_AMBER = '#ffb000';

interface Satellite {
  id: string;
  name: string;
  orbit_km: number;
  inclination: number;
  period_min: number;
  status: string;
}

interface Launch {
  id: string;
  mission: string;
  date: string;
  vehicle: string;
  status: string;
}

interface SpaceTrackingPanelProps {
  satellites: Satellite[];
  launches: Launch[];
}

export const SpaceTrackingPanel: React.FC<SpaceTrackingPanelProps> = ({ satellites, launches }) => {
  return (
    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
      {/* オービット表示（衛星軌道） */}
      <Box
        sx={{
          width: 320,
          height: 320,
          borderRadius: '50%',
          bgcolor: TELEMETRY_BG,
          border: `2px solid ${TELEMETRY_COLOR}`,
          position: 'relative',
          overflow: 'hidden',
          boxShadow: `0 0 20px ${TELEMETRY_COLOR}30, inset 0 0 80px ${TELEMETRY_COLOR}06`,
        }}
      >
        <svg width="100%" height="100%" viewBox="0 0 320 320" style={{ position: 'absolute' }}>
          {/* 地球 */}
          <circle cx="160" cy="160" r="45" fill="#0d2137" stroke={TELEMETRY_COLOR} strokeWidth="0.5" opacity="0.9" />
          <circle cx="160" cy="160" r="40" fill="#1a4d6e" stroke={TELEMETRY_COLOR} strokeWidth="0.5" opacity="0.8" />
          {/* 軌道リング（衛星ごとに異なる高度） */}
          {satellites.slice(0, 4).map((s, i) => {
            const orbitColor = (s.orbit_km || 0) < 2000 ? '#00ff41' : (s.orbit_km || 0) < 36000 ? TELEMETRY_COLOR : ACCENT_AMBER;
            const baseRadius = 60 + Math.min((s.orbit_km / 600) * 35, 80) + i * 12;
            const r = Math.min(baseRadius, 140);
            const angle = (i * 85 + (s.orbit_km % 360)) * (Math.PI / 180);
            const sx = 160 + r * Math.cos(angle);
            const sy = 160 - r * Math.sin(angle);
            return (
              <g key={s.id}>
                <circle
                  cx="160"
                  cy="160"
                  r={r}
                  fill="none"
                  stroke={orbitColor}
                  strokeWidth="0.5"
                  opacity={0.5}
                />
                {/* 衛星位置（LEO=緑/MEO=シアン/GEO=琥珀） */}
                <circle cx={sx} cy={sy} r="4" fill={orbitColor} opacity={0.95} />
                <text x={sx + 6} y={sy + 4} fill={orbitColor} fontSize={9} fontFamily="monospace" opacity={0.9}>
                  {s.id}
                </text>
              </g>
            );
          })}
          {/* グリッド線 */}
          {[0.25, 0.5, 0.75].map((s) => (
            <ellipse
              key={s}
              cx="160"
              cy="160"
              rx={150 * s}
              ry={150 * s}
              fill="none"
              stroke={TELEMETRY_COLOR}
              strokeWidth="0.3"
              opacity={0.2}
            />
          ))}
        </svg>
        <Box sx={{ position: 'absolute', bottom: 8, left: 12 }}>
          <Typography sx={{ fontFamily: 'monospace', fontSize: 9, color: TELEMETRY_COLOR, opacity: 0.7 }}>
            ORBIT TRACKING | {satellites.length} OBJECTS
          </Typography>
        </Box>
      </Box>

      {/* テレメトリパネル（NASA管制風） */}
      <Box sx={{ flex: 1, minWidth: 280, display: 'flex', flexDirection: 'column', gap: 1.5 }}>
        <Box
          sx={{
            bgcolor: TELEMETRY_BG,
            border: `1px solid ${TELEMETRY_COLOR}`,
            borderRadius: 1,
            p: 1.5,
            fontFamily: 'monospace',
            boxShadow: `0 0 10px ${TELEMETRY_COLOR}20`,
          }}
        >
          <Typography sx={{ fontFamily: 'monospace', fontSize: 11, color: TELEMETRY_COLOR, mb: 1, opacity: 0.9 }}>
            === SATELLITE TELEMETRY ===
          </Typography>
          {satellites.slice(0, 5).map((s) => (
            <Box key={s.id} sx={{ fontSize: 10, color: TELEMETRY_COLOR, opacity: 0.85, mb: 0.5 }}>
              {s.id} | ORB:{s.orbit_km}km INC:{s.inclination}° PER:{s.period_min}min | {s.status}
            </Box>
          ))}
        </Box>
        <Box
          sx={{
            bgcolor: TELEMETRY_BG,
            border: `1px solid ${ACCENT_AMBER}`,
            borderRadius: 1,
            p: 1.5,
            fontFamily: 'monospace',
            boxShadow: `0 0 10px ${ACCENT_AMBER}20`,
          }}
        >
          <Typography sx={{ fontFamily: 'monospace', fontSize: 11, color: ACCENT_AMBER, mb: 1, opacity: 0.9 }}>
            === LAUNCH MANIFEST ===
          </Typography>
          {launches.slice(0, 4).map((l) => (
            <Box key={l.id} sx={{ fontSize: 10, color: ACCENT_AMBER, opacity: 0.85, mb: 0.5 }}>
              {l.id} | {l.mission} | {l.date} | {l.vehicle} | {l.status}
            </Box>
          ))}
        </Box>
      </Box>
    </Box>
  );
};
