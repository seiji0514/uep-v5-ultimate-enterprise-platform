"""
環境データサービス
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from app.core.influxdb_client import write_time_series_data, query_time_series_data
from app.schemas.environment import EnvironmentDataCreate, EnvironmentDataResponse
from loguru import logger


class EnvironmentService:
    """環境データサービス"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_environment_data(
        self,
        sensor_id: Optional[str] = None,
        data_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EnvironmentDataResponse]:
        """環境データの取得"""
        try:
            # InfluxDBから時系列データを取得
            if not start_time:
                start_time = datetime.now() - pd.Timedelta(days=1)
            if not end_time:
                end_time = datetime.now()
            
            filters = {}
            if sensor_id:
                filters["sensor_id"] = sensor_id
            if data_type:
                filters["data_type"] = data_type
            
            data = await query_time_series_data(
                measurement="environment_data",
                start=start_time.isoformat(),
                stop=end_time.isoformat(),
                filters=filters
            )
            
            # スキップとリミットを適用
            return data[skip:skip+limit]
            
        except Exception as e:
            logger.error(f"環境データ取得エラー: {e}")
            return []
    
    async def create_environment_data(
        self,
        sensor_id: str,
        data_type: str,
        value: float,
        unit: str
    ) -> dict:
        """環境データの作成"""
        try:
            # InfluxDBに時系列データを書き込み
            await write_time_series_data(
                measurement="environment_data",
                tags={
                    "sensor_id": sensor_id,
                    "data_type": data_type,
                    "unit": unit
                },
                fields={
                    "value": value
                }
            )
            
            logger.info(f"環境データ作成成功: sensor_id={sensor_id}, data_type={data_type}, value={value}")
            return {"message": "環境データを作成しました", "sensor_id": sensor_id, "data_type": data_type, "value": value}
            
        except Exception as e:
            logger.error(f"環境データ作成エラー: {e}")
            raise
    
    def analyze_environment_data(
        self,
        sensor_id: str,
        data_type: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """環境データの分析"""
        try:
            # データ取得
            data = self.get_environment_data(
                sensor_id=sensor_id,
                data_type=data_type,
                start_time=start_time,
                end_time=end_time,
                limit=10000
            )
            
            if not data:
                return {"error": "データが見つかりません"}
            
            # データをDataFrameに変換
            values = [d["value"] for d in data]
            df = pd.DataFrame({"value": values})
            
            # 統計分析
            analysis = {
                "mean": float(df["value"].mean()),
                "std": float(df["value"].std()),
                "min": float(df["value"].min()),
                "max": float(df["value"].max()),
                "median": float(df["value"].median()),
                "cv": float(df["value"].std() / df["value"].mean() * 100) if df["value"].mean() != 0 else 0,
                "recent_change_rate": float((df["value"].iloc[-1] - df["value"].iloc[0]) / df["value"].iloc[0] * 100) if len(df) > 1 and df["value"].iloc[0] != 0 else 0
            }
            
            logger.info(f"環境データ分析成功: sensor_id={sensor_id}, data_type={data_type}")
            return analysis
            
        except Exception as e:
            logger.error(f"環境データ分析エラー: {e}")
            raise
    
    def predict_environment_data(
        self,
        sensor_id: str,
        data_type: str,
        hours: int = 24
    ) -> dict:
        """環境データの予測（線形回帰）"""
        try:
            # 過去のデータを取得
            end_time = datetime.now()
            start_time = datetime.now() - pd.Timedelta(hours=hours*2)
            
            data = self.get_environment_data(
                sensor_id=sensor_id,
                data_type=data_type,
                start_time=start_time,
                end_time=end_time,
                limit=10000
            )
            
            if len(data) < 2:
                return {"error": "予測に十分なデータがありません"}
            
            # データをDataFrameに変換
            values = [d["value"] for d in data]
            timestamps = [pd.to_datetime(d["time"]) for d in data]
            
            df = pd.DataFrame({
                "timestamp": timestamps,
                "value": values
            })
            df = df.sort_values("timestamp")
            df["hours"] = (df["timestamp"] - df["timestamp"].min()).dt.total_seconds() / 3600
            
            # 線形回帰モデルの学習
            X = df[["hours"]].values
            y = df["value"].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # 次のhours時間の予測
            future_hours = np.arange(df["hours"].max() + 1, df["hours"].max() + hours + 1).reshape(-1, 1)
            predictions = model.predict(future_hours)
            
            result = {
                "predictions": [
                    {
                        "hours_ahead": i + 1,
                        "predicted_value": float(predictions[i])
                    }
                    for i in range(len(predictions))
                ],
                "model_coefficient": float(model.coef_[0]),
                "model_intercept": float(model.intercept_)
            }
            
            logger.info(f"環境データ予測成功: sensor_id={sensor_id}, data_type={data_type}, hours={hours}")
            return result
            
        except Exception as e:
            logger.error(f"環境データ予測エラー: {e}")
            raise

