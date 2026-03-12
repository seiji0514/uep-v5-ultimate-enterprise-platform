/**
 * ダッシュボードカスタマイズ - ウィジェット表示・並び順
 */
import { createContext, useContext, useState, useCallback, ReactNode } from 'react';

const STORAGE_KEY = 'uep_dashboard_layout';

export type WidgetId = 'kpi' | 'chart' | 'alerts' | 'weather' | 'calendar' | 'todo';

const DEFAULT_ORDER: WidgetId[] = ['kpi', 'chart', 'alerts', 'weather', 'calendar', 'todo'];
const DEFAULT_VISIBLE: Record<WidgetId, boolean> = { kpi: true, chart: true, alerts: true, weather: true, calendar: true, todo: true };

interface DashboardLayout {
  order: WidgetId[];
  visible: Record<WidgetId, boolean>;
}

const loadLayout = (): DashboardLayout => {
  try {
    const s = localStorage.getItem(STORAGE_KEY);
    if (s) {
      const parsed = JSON.parse(s);
      if (parsed.order?.length && parsed.visible) {
        const visible = { ...DEFAULT_VISIBLE, ...parsed.visible };
        const order = [...new Set([...DEFAULT_ORDER.filter(id => !parsed.order.includes(id)), ...parsed.order])];
        const allHidden = !visible.kpi && !visible.chart && !visible.alerts && !visible.weather && !visible.calendar && !visible.todo;
        if (allHidden) {
          const fixed = { order: DEFAULT_ORDER, visible: { ...DEFAULT_VISIBLE } };
          localStorage.setItem(STORAGE_KEY, JSON.stringify(fixed));
          return fixed;
        }
        return { order, visible };
      }
    }
  } catch {}
  return { order: DEFAULT_ORDER, visible: { ...DEFAULT_VISIBLE } };
};

interface DashboardContextType {
  layout: DashboardLayout;
  setWidgetVisible: (id: WidgetId, visible: boolean) => void;
  setWidgetOrder: (order: WidgetId[]) => void;
  moveWidget: (from: number, to: number) => void;
  resetLayout: () => void;
}

const DashboardContext = createContext<DashboardContextType | null>(null);

export function DashboardProvider({ children }: { children: ReactNode }) {
  const [layout, setLayout] = useState<DashboardLayout>(loadLayout);

  const setWidgetVisible = useCallback((id: WidgetId, visible: boolean) => {
    setLayout((prev) => {
      const next = { ...prev, visible: { ...prev.visible, [id]: visible } };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const setWidgetOrder = useCallback((order: WidgetId[]) => {
    setLayout((prev) => {
      const next = { ...prev, order };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const moveWidget = useCallback((from: number, to: number) => {
    setLayout((prev) => {
      const arr = [...prev.order];
      const [removed] = arr.splice(from, 1);
      arr.splice(to, 0, removed);
      const next = { ...prev, order: arr };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const resetLayout = useCallback(() => {
    const next = { order: DEFAULT_ORDER, visible: { ...DEFAULT_VISIBLE } };
    setLayout(next);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  }, []);

  return (
    <DashboardContext.Provider value={{ layout, setWidgetVisible, setWidgetOrder, moveWidget, resetLayout }}>
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  const ctx = useContext(DashboardContext);
  return ctx ?? {
    layout: loadLayout(),
    setWidgetVisible: () => {},
    setWidgetOrder: () => {},
    moveWidget: () => {},
    resetLayout: () => {},
  };
}
