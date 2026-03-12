/**
 * フライト経路の地図表示（SVG簡易版）
 */
import React, { useMemo } from 'react';
import { Box, Typography } from '@mui/material';

const COORDS: Record<string, [number, number]> = {
  NRT: [35.77, 140.39], HND: [35.55, 139.78], KIX: [34.43, 135.24], NGO: [34.86, 136.81],
  LAX: [33.94, -118.41], SFO: [37.62, -122.38], LHR: [51.47, -0.45], SIN: [1.36, 103.99],
  HKG: [22.31, 113.92], SEL: [37.46, 126.44], ICN: [37.46, 126.44],
};

function toSvg(lat: number, lon: number, w: number, h: number): [number, number] {
  const x = (lon + 180) / 360 * w;
  const y = h - (lat + 90) / 180 * h;
  return [x, y];
}

interface AviationFlightMapProps {
  flights: { flight_id: string; route: string }[];
}

export const AviationFlightMap: React.FC<AviationFlightMapProps> = ({ flights }) => {
  const routes = useMemo(() => {
    return flights
      .map((f) => {
        const [dep, arr] = f.route.split('-').map((s) => s.trim());
        const from = COORDS[dep] || COORDS[dep?.slice(0, 3)] || null;
        const to = COORDS[arr] || COORDS[arr?.slice(0, 3)] || null;
        if (!from || !to) return null;
        return { dep, arr, from, to, id: f.flight_id };
      })
      .filter(Boolean) as { dep: string; arr: string; from: [number, number]; to: [number, number]; id: string }[];
  }, [flights]);

  const w = 400;
  const h = 220;

  return (
    <Box sx={{ bgcolor: '#0a0e14', border: '1px solid #00ff41', borderRadius: 1, p: 1, overflow: 'hidden' }}>
      <Typography sx={{ fontFamily: 'monospace', fontSize: 11, color: '#00ff41', mb: 1 }}>FLIGHT ROUTES</Typography>
      <svg width="100%" height={h} viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="xMidYMid meet">
        {/* 簡易世界地図枠 */}
        <rect x={0} y={0} width={w} height={h} fill="#0d1520" stroke="#00ff4133" strokeWidth={0.5} />
        {/* 経路線 */}
        {routes.map((r) => {
          const [x1, y1] = toSvg(r.from[0], r.from[1], w, h);
          const [x2, y2] = toSvg(r.to[0], r.to[1], w, h);
          return (
            <g key={r.id}>
              <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#00ff41" strokeWidth={1} opacity={0.6} strokeDasharray="4 2" />
              <circle cx={x1} cy={y1} r={3} fill="#00ff41" opacity={0.9} />
              <circle cx={x2} cy={y2} r={3} fill="#00ff41" opacity={0.9} />
              <text x={x1} y={y1 - 6} fill="#00ff41" fontSize={8} fontFamily="monospace">{r.dep}</text>
              <text x={x2} y={y2 - 6} fill="#00ff41" fontSize={8} fontFamily="monospace">{r.arr}</text>
            </g>
          );
        })}
      </svg>
    </Box>
  );
};
