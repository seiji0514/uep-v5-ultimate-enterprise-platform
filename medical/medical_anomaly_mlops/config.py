"""
医療データ異常検知MLOps - 設定管理
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
    API_TITLE: str = "Medical Anomaly Detection MLOps API"
    API_VERSION: str = "2.0.0"
    API_DESCRIPTION: str = "医療データ異常検知MLOpsシステム - 企業レベル実装"
    
    # サーバー設定
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    RELOAD: bool = False
    
    # CORS設定
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # ログ設定
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = "logs/medical_mlops.log"
    
    # データベース設定（将来の拡張用）
    DATABASE_URL: Optional[str] = None
    
    # Redis設定（キャッシング用）
    REDIS_URL: Optional[str] = None
    REDIS_ENABLED: bool = False
    
    # AWS設定（SageMaker統合用）
    AWS_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    SAGEMAKER_ENDPOINT_NAME: Optional[str] = None
    
    # セキュリティ設定
    API_KEY_ENABLED: bool = False
    API_KEY: Optional[str] = None
    
    # MLOps設定
    MODEL_PATH: str = "advanced_model.pkl"
    SCALER_PATH: str = "scaler.pkl"
    METADATA_PATH: str = "advanced_metadata.json"
    
    # 異常検知設定
    ANOMALY_THRESHOLD: float = 0.5
    CONFIDENCE_THRESHOLD: float = 0.8
    
    # データ設定
    SAMPLE_DATA_PATH: str = "medical_data_sample.csv"
    MAX_BATCH_SIZE: int = 1000
    
    # パフォーマンス設定
    ENABLE_CACHE: bool = True
    CACHE_TTL_SECONDS: int = 300
    
    # GDPR/個人情報保護設定
    ENABLE_DATA_ANONYMIZATION: bool = True
    ENABLE_AUDIT_LOG: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# グローバル設定インスタンス
settings = Settings()

