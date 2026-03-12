/**
 * ソート・ページネーション対応テーブル
 */
import { useState, useMemo } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  TablePagination,
} from '@mui/material';

type Order = 'asc' | 'desc';

interface SortableTableProps<T> {
  data: T[];
  columns: { key: keyof T | string; label: string; sortable?: boolean }[];
  rowsPerPageOptions?: number[];
  defaultOrderBy?: keyof T | string;
  renderRow: (row: T) => React.ReactNode; // TableCell elements
  getRowKey: (row: T) => string;
}

export function SortableTable<T extends Record<string, unknown>>({
  data,
  columns,
  rowsPerPageOptions = [5, 10, 25],
  defaultOrderBy,
  renderRow,
  getRowKey,
}: SortableTableProps<T>) {
  const [order, setOrder] = useState<Order>('asc');
  const [orderBy, setOrderBy] = useState<keyof T | string>(defaultOrderBy ?? columns[0]?.key ?? '');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(rowsPerPageOptions[0] ?? 10);

  const sorted = useMemo(() => {
    const key = orderBy as string;
    return [...data].sort((a, b) => {
      const av = a[key];
      const bv = b[key];
      const cmp = typeof av === 'number' && typeof bv === 'number'
        ? av - bv
        : String(av ?? '').localeCompare(String(bv ?? ''));
      return order === 'asc' ? cmp : -cmp;
    });
  }, [data, orderBy, order]);

  const paginated = useMemo(
    () => sorted.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    [sorted, page, rowsPerPage]
  );

  const handleSort = (key: keyof T | string) => {
    const isAsc = orderBy === key && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(key);
  };

  return (
    <>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell key={String(col.key)}>
                  {col.sortable !== false ? (
                    <TableSortLabel
                      active={orderBy === col.key}
                      direction={orderBy === col.key ? order : 'asc'}
                      onClick={() => handleSort(col.key)}
                    >
                      {col.label}
                    </TableSortLabel>
                  ) : (
                    col.label
                  )}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {paginated.map((row) => (
              <TableRow key={getRowKey(row)}>{renderRow(row)}</TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={rowsPerPageOptions}
        component="div"
        count={data.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={(_, p) => setPage(p)}
        onRowsPerPageChange={(e) => {
          setRowsPerPage(parseInt(e.target.value, 10));
          setPage(0);
        }}
        labelRowsPerPage="表示件数"
      />
    </>
  );
}
