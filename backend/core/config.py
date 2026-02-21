"""
設定管理モジュール
Pydantic Settingsを使用した設定管理
"""
import os
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""

    # アプリケーション基本設定
    APP_NAME: str = "UEP v5.0 - Ultimate Enterprise Platform"
    APP_VERSION: str = "5.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")

    # サーバー設定
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    # データベース設定（ローカル開発はSQLite、本番はPostgreSQL推奨）
    DATABASE_URL: str = Field(default="sqlite:///./uep_db.sqlite", env="DATABASE_URL")
    DB_POOL_SIZE: int = Field(default=20, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=40, env="DB_MAX_OVERFLOW")

    # Redis設定
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_PASSWORD: Optional[str] = Field(default=None, env="REDIS_PASSWORD")

    # セキュリティ設定
    SECRET_KEY: str = Field(
        default="change-this-secret-key-in-production", env="SECRET_KEY"
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # CORS設定
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"], env="CORS_ORIGINS"
    )

    # APIレート制限設定
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")

    # ロギング設定
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    LOGSTASH_URL: Optional[str] = Field(default=None, env="LOGSTASH_URL")

    # 監視設定
    PROMETHEUS_ENABLED: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    OPENTELEMETRY_ENABLED: bool = Field(default=True, env="OPENTELEMETRY_ENABLED")

    # セキュリティ設定
    CSRF_ENABLED: bool = Field(default=True, env="CSRF_ENABLED")
    CSRF_SECRET: Optional[str] = Field(default=None, env="CSRF_SECRET")
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"], env="ALLOWED_HOSTS"
    )

    # ファイルアップロード設定
    MAX_UPLOAD_SIZE: int = Field(
        default=100 * 1024 * 1024, env="MAX_UPLOAD_SIZE"
    )  # 100MB
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=["jpg", "jpeg", "png", "pdf", "doc", "docx"], env="ALLOWED_EXTENSIONS"
    )

    # Celery設定（非同期処理）
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1", env="CELERY_BROKER_URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND"
    )

    # Kafka設定
    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        default="localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS"
    )

    # MinIO設定
    MINIO_ENDPOINT: str = Field(default="localhost:9000", env="MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: str = Field(default="minioadmin", env="MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = Field(default="minioadmin", env="MINIO_SECRET_KEY")
    MINIO_SECURE: bool = Field(default=False, env="MINIO_SECURE")

    # Vault設定
    VAULT_URL: str = Field(default="http://localhost:8200", env="VAULT_URL")
    VAULT_TOKEN: Optional[str] = Field(default=None, env="VAULT_TOKEN")

    @field_validator("PORT", mode="before")
    @classmethod
    def strip_port(cls, v):
        """PORT の前後の空白を除去（Windows set コマンド対策）"""
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """CORS_ORIGINSをリストに変換"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v):
        """ALLOWED_HOSTSをリストに変換"""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v):
        """ALLOWED_EXTENSIONSをリストに変換"""
        if isinstance(v, str):
            return [ext.strip().lower() for ext in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# グローバル設定インスタンス
settings = Settings()
