"""
InfluxDBクライアント設定
"""

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from app.core.config import settings
from loguru import logger

# InfluxDBクライアントの作成
influxdb_client = InfluxDBClient(
    url=settings.INFLUXDB_URL,
    token=settings.INFLUXDB_TOKEN,
    org=settings.INFLUXDB_ORG
)

# 書き込みAPIの取得
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

# クエリAPIの取得
query_api = influxdb_client.query_api()


async def write_time_series_data(measurement: str, tags: dict, fields: dict, timestamp: str = None):
    """時系列データの書き込み"""
    try:
        from influxdb_client import Point
        
        point = Point(measurement)
        
        # タグの追加
        for key, value in tags.items():
            point.tag(key, value)
        
        # フィールドの追加
        for key, value in fields.items():
            point.field(key, value)
        
        # タイムスタンプの設定
        if timestamp:
            point.time(timestamp)
        
        write_api.write(bucket=settings.INFLUXDB_BUCKET, record=point)
        logger.info(f"時系列データ書き込み成功: {measurement}")
        
    except Exception as e:
        logger.error(f"時系列データ書き込みエラー: {e}")
        raise


async def query_time_series_data(measurement: str, start: str, stop: str, filters: dict = None):
    """時系列データのクエリ"""
    try:
        query = f'''
        from(bucket: "{settings.INFLUXDB_BUCKET}")
        |> range(start: {start}, stop: {stop})
        |> filter(fn: (r) => r._measurement == "{measurement}")
        '''
        
        if filters:
            for key, value in filters.items():
                query += f'|> filter(fn: (r) => r.{key} == "{value}")'
        
        result = query_api.query(query)
        
        data = []
        for table in result:
            for record in table.records:
                data.append({
                    "time": record.get_time(),
                    "measurement": record.get_measurement(),
                    "field": record.get_field(),
                    "value": record.get_value(),
                    "tags": record.values
                })
        
        logger.info(f"時系列データクエリ成功: {measurement}")
        return data
        
    except Exception as e:
        logger.error(f"時系列データクエリエラー: {e}")
        raise

