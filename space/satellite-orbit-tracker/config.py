"""
衛星軌道追跡システム - 設定管理
環境変数とアプリケーション設定

作成日: 2025年11月2日
作成者: 小川清志
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # API設定
    API_TITLE: str = "Satellite Orbit Tracker API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "衛星軌道計算・追跡システム - 企業レベル実装"
    
    # サーバー設定
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    
    # CORS設定
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # ログ設定
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = "logs/satellite_tracker.log"
    
    # データベース設定（将来の拡張用）
    DATABASE_URL: Optional[str] = None
    
    # Redis設定（キャッシング用）
    REDIS_URL: Optional[str] = None
    REDIS_ENABLED: bool = False
    
    # AWS設定（Ground Station統合用）
    AWS_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # セキュリティ設定
    API_KEY_ENABLED: bool = False
    API_KEY: Optional[str] = None
    
    # 軌道計算設定
    DEFAULT_PREDICTION_HOURS: float = 24.0
    DEFAULT_STEP_MINUTES: float = 5.0
    MAX_PREDICTION_HOURS: float = 168.0  # 7日間
    
    # パフォーマンス設定
    ENABLE_CACHE: bool = True
    CACHE_TTL_SECONDS: int = 300  # 5分
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# グローバル設定インスタンス
settings = Settings()
