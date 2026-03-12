/**
 * 空港間便数マトリクス
 */
import React, { useMemo } from 'react';
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

interface AviationAirportMatrixProps {
  flights: { route: string }[];
}

export const AirportMatrix: React.FC<AviationAirportMatrixProps> = ({ flights }) => {
  const { matrix, airports } = useMemo(() => {
    const m: Record<string, Record<string, number>> = {};
    const set = new Set<string>();
    flights.forEach((f) => {
      const [dep, arr] = f.route.split('-').map((s) => s.trim());
      if (dep && arr) {
        set.add(dep);
        set.add(arr);
        if (!m[dep]) m[dep] = {};
        m[dep][arr] = (m[dep][arr] || 0) + 1;
      }
    });
    const list = Array.from(set).sort();
    return { matrix: m, airports: list };
  }, [flights]);

  if (airports.length === 0) return <Typography variant="body2" color="text.secondary">データがありません</Typography>;

  return (
    <TableContainer sx={{ maxWidth: 400 }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: 600 }}></TableCell>
            {airports.map((a) => (
              <TableCell key={a} align="center" sx={{ fontWeight: 600, fontSize: 11 }}>{a}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {airports.map((dep) => (
            <TableRow key={dep}>
              <TableCell sx={{ fontWeight: 600, fontSize: 11 }}>{dep}</TableCell>
              {airports.map((arr) => (
                <TableCell key={arr} align="center">
                  {dep === arr ? '-' : (matrix[dep]?.[arr] ?? 0)}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
