import React, { useEffect, useState } from 'react';
import { sensorService } from '../services/api';
import './Sensors.css';

const Sensors: React.FC = () => {
  const [sensors, setSensors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSensors = async () => {
      try {
        const response = await sensorService.getSensors();
        setSensors(response.data);
      } catch (error) {
        console.error('センサー取得エラー:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSensors();
  }, []);

  if (loading) {
    return <div className="loading">読み込み中...</div>;
  }

  return (
    <div className="sensors">
      <h2>IoTセンサー一覧</h2>
      <table className="sensors-table">
        <thead>
          <tr>
            <th>センサーID</th>
            <th>タイプ</th>
            <th>場所</th>
            <th>ステータス</th>
            <th>作成日時</th>
          </tr>
        </thead>
        <tbody>
          {sensors.map((sensor) => (
            <tr key={sensor.id}>
              <td>{sensor.sensor_id}</td>
              <td>{sensor.sensor_type}</td>
              <td>{sensor.location_name || '-'}</td>
              <td>
                <span className={`status-badge status-${sensor.status}`}>
                  {sensor.status}
                </span>
              </td>
              <td>{new Date(sensor.created_at).toLocaleString('ja-JP')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Sensors;

