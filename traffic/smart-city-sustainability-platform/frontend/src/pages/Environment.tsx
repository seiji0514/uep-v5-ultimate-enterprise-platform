import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { environmentService } from '../services/api';
import './Environment.css';

const Environment: React.FC = () => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await environmentService.getData();
        setData(response.data);
      } catch (error) {
        console.error('環境データ取得エラー:', error);
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

  const chartData = {
    labels: data.map((d) => new Date(d.timestamp).toLocaleTimeString('ja-JP')),
    datasets: [
      {
        label: '環境データ',
        data: data.map((d) => d.value),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return (
    <div className="environment">
      <h2>環境データ</h2>
      <div className="environment-chart">
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default Environment;

