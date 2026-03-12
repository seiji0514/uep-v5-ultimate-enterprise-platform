/**
 * 航空管制レーダー風表示
 * 本物のATCレーダーに近いレイアウト
 */
import React from 'react';
import { Box, Typography } from '@mui/material';

const RADAR_COLOR = '#00ff41'; // レーダーグリーン（CRT風）
const RADAR_BG = '#0a0e14';

interface Flight {
  flight_id: string;
  route: string;
  departure: string;
  arrival: string;
  status: string;
}

interface AviationRadarPanelProps {
  flights: Flight[];
  airports: { airport: string; departures_today: number; arrivals_today: number; congestion: string }[];
}

// ルートから極座標を簡易算出（デモ用）
function routeToPosition(route: string, index: number): { r: number; theta: number } {
  const parts = route.split('-');
  const hash = (parts[0]?.charCodeAt(0) || 0) + (parts[1]?.charCodeAt(0) || 0) + index;
  const r = 25 + (hash % 45);
  const theta = (hash * 137.5) % 360;
  return { r, theta };
}

export const AviationRadarPanel: React.FC<AviationRadarPanelProps> = ({ flights, airports }) => {
  const size = 320;
  const center = size / 2;

  return (
    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
      {/* メインレーダースクリーン */}
      <Box
        sx={{
          width: size,
          height: size,
          borderRadius: '50%',
          bgcolor: RADAR_BG,
          border: `2px solid ${RADAR_COLOR}`,
          position: 'relative',
          overflow: 'hidden',
          boxShadow: `0 0 20px ${RADAR_COLOR}40, inset 0 0 60px ${RADAR_COLOR}08`,
        }}
      >
        {/* 同心円グリッド */}
        <svg width={size} height={size} style={{ position: 'absolute', left: 0, top: 0 }}>
          <defs>
            <filter id="radar-glow">
              <feGaussianBlur stdDeviation="1" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          {/* 距離リング 25%, 50%, 75%, 100% */}
          {[0.25, 0.5, 0.75, 1].map((scale) => (
            <circle
              key={scale}
              cx={center}
              cy={center}
              r={center * scale}
              fill="none"
              stroke={RADAR_COLOR}
              strokeWidth={0.5}
              opacity={0.4}
              filter="url(#radar-glow)"
            />
          ))}
          {/* 方位線 (N, NE, E, SE, S, SW, W, NW) */}
          {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => {
            const rad = (deg * Math.PI) / 180;
            const x2 = center + center * Math.sin(rad);
            const y2 = center - center * Math.cos(rad);
            return (
              <line
                key={deg}
                x1={center}
                y1={center}
                x2={x2}
                y2={y2}
                stroke={RADAR_COLOR}
                strokeWidth={0.5}
                opacity={0.3}
              />
            );
          })}
          {/* スイープ線（回転アニメーション） */}
          <g style={{ transformOrigin: '50% 50%', animation: 'radar-sweep 4s linear infinite' }}>
            <line
              x1={center}
              y1={center}
              x2={center}
              y2={8}
              stroke={RADAR_COLOR}
              strokeWidth={1}
              opacity={0.9}
            />
          </g>
          {/* 飛行機ブリップ */}
          {flights.map((f, i) => {
            const { r, theta } = routeToPosition(f.route, i);
            const rad = (theta * Math.PI) / 180;
            const x = center + (center * r) / 100 * Math.sin(rad);
            const y = center - (center * r) / 100 * Math.cos(rad);
            return (
              <g key={f.flight_id}>
                <rect
                  x={x - 4}
                  y={y - 2}
                  width={8}
                  height={4}
                  fill={RADAR_COLOR}
                  opacity={0.9}
                  transform={`rotate(${theta} ${x} ${y})`}
                />
                <text
                  x={x + 6}
                  y={y + 4}
                  fill={RADAR_COLOR}
                  fontSize={10}
                  fontFamily="monospace"
                  opacity={0.9}
                >
                  {f.flight_id}
                </text>
              </g>
            );
          })}
        </svg>
        {/* 方位ラベル */}
        <Box sx={{ position: 'absolute', top: 4, left: '50%', transform: 'translateX(-50%)' }}>
          <Typography component="span" sx={{ fontFamily: 'monospace', fontSize: 10, color: RADAR_COLOR, opacity: 0.8 }}>N</Typography>
        </Box>
        {/* スケール表示 */}
        <Box sx={{ position: 'absolute', bottom: 8, right: 12 }}>
          <Typography component="span" sx={{ fontFamily: 'monospace', fontSize: 9, color: RADAR_COLOR, opacity: 0.6 }}>RNG 100nm</Typography>
        </Box>
        <style>{`
          @keyframes radar-sweep {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}</style>
      </Box>

      {/* テレメトリパネル（レーダー風） */}
      <Box
        sx={{
          flex: 1,
          minWidth: 280,
          bgcolor: RADAR_BG,
          border: `1px solid ${RADAR_COLOR}`,
          borderRadius: 1,
          p: 1.5,
          fontFamily: 'monospace',
          boxShadow: `0 0 10px ${RADAR_COLOR}20`,
        }}
      >
        <Typography sx={{ fontFamily: 'monospace', fontSize: 11, color: RADAR_COLOR, mb: 1, opacity: 0.9 }}>
          === FLIGHT DATA ===
        </Typography>
        {flights.slice(0, 6).map((f) => (
          <Box key={f.flight_id} sx={{ fontSize: 10, color: RADAR_COLOR, opacity: 0.85, mb: 0.5 }}>
            {f.flight_id} | {f.route} | DEP {f.departure} ARR {f.arrival} | {f.status}
          </Box>
        ))}
        <Typography sx={{ fontFamily: 'monospace', fontSize: 11, color: RADAR_COLOR, mt: 1.5, mb: 0.5, opacity: 0.9 }}>
          === AIRPORT STATUS ===
        </Typography>
        {airports.slice(0, 4).map((a) => (
          <Box key={a.airport} sx={{ fontSize: 10, color: RADAR_COLOR, opacity: 0.85, mb: 0.5 }}>
            {a.airport} | DEP:{a.departures_today} ARR:{a.arrivals_today} | {a.congestion}
          </Box>
        ))}
      </Box>
    </Box>
  );
};
