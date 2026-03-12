import React, { useEffect, useState } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { dashboardService } from '../services/api';
import './Dashboard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard: React.FC = () => {
  const [overview, setOverview] = useState<any>(null);
  const [kpi, setKpi] = useState<any>(null);
  const [alertsSummary, setAlertsSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewData, kpiData, alertsData] = await Promise.all([
          dashboardService.getOverview(),
          dashboardService.getKPI(),
          dashboardService.getAlertsSummary(),
        ]);
        setOverview(overviewData);
        setKpi(kpiData);
        setAlertsSummary(alertsData);
      } catch (error) {
        console.error('データ取得エラー:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 60000); // 1分ごとに更新
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="loading">読み込み中...</div>;
  }

  const energyChartData = {
    labels: ['消費量', '発電量'],
    datasets: [
      {
        label: 'エネルギー',
        data: [
          kpi?.energy?.total_consumption || 0,
          kpi?.energy?.total_generation || 0,
        ],
        backgroundColor: ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)'],
      },
    ],
  };

  return (
    <div className="dashboard">
      <h2>統括責任者向けダッシュボード</h2>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>概要</h3>
          <div className="overview-stats">
            <div className="stat-item">
              <span className="stat-label">環境データポイント:</span>
              <span className="stat-value">{overview?.environment?.data_points || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">交通データポイント:</span>
              <span className="stat-value">{overview?.traffic?.data_points || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">エネルギーデータポイント:</span>
              <span className="stat-value">{overview?.energy?.data_points || 0}</span>
            </div>
          </div>
        </div>

        <div className="dashboard-card">
          <h3>統合KPI</h3>
          <div className="kpi-stats">
            <div className="kpi-item">
              <span className="kpi-label">エネルギーの自給率:</span>
              <span className="kpi-value">
                {kpi?.energy?.self_sufficiency_rate?.toFixed(2) || 0}%
              </span>
            </div>
            <div className="kpi-item">
              <span className="kpi-label">渋滞率:</span>
              <span className="kpi-value">
                {kpi?.traffic?.congestion_rate?.toFixed(2) || 0}%
              </span>
            </div>
          </div>
        </div>

        <div className="dashboard-card">
          <h3>エネルギー</h3>
          <Bar data={energyChartData} />
        </div>

        <div className="dashboard-card">
          <h3>アラートサマリー</h3>
          <div className="alerts-summary">
            <div className="alert-stat">
              <span className="alert-label">総アラート数:</span>
              <span className="alert-value">{alertsSummary?.total || 0}</span>
            </div>
            <div className="alert-stat">
              <span className="alert-label">重大度別:</span>
              <div className="alert-severity">
                {Object.entries(alertsSummary?.by_severity || {}).map(([severity, count]) => (
                  <div key={severity}>
                    {severity}: {count as number}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

