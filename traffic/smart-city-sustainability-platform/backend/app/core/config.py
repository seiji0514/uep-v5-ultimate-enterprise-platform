"""
アプリケーション設定
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # アプリケーション設定
    APP_NAME: str = "スマートシティ×サステナビリティ統合プラットフォーム"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # データベース設定
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "smart_city_sustainability"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    
    @property
    def DATABASE_URL(self) -> str:
        """データベースURL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # InfluxDB設定
    INFLUXDB_URL: str = "http://influxdb:8086"
    INFLUXDB_TOKEN: str = "your_influxdb_token"
    INFLUXDB_ORG: str = "smart_city_org"
    INFLUXDB_BUCKET: str = "smart_city_data"
    
    # Kafka設定
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_TOPIC_IOT_DATA: str = "iot_sensor_data"
    KAFKA_TOPIC_ENVIRONMENT_DATA: str = "environment_data"
    KAFKA_TOPIC_TRAFFIC_DATA: str = "traffic_data"
    KAFKA_TOPIC_ENERGY_DATA: str = "energy_data"
    
    # セキュリティ設定
    SECRET_KEY: str = "your_secret_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS設定
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # 監視設定
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3001
    
    # 外部API設定
    WEATHER_API_KEY: str = ""
    GOOGLE_MAPS_API_KEY: str = ""
    
    # ログ設定
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

