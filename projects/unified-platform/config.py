"""Unified Platform Config - Medical / Aviation / Space"""
import os
from functools import lru_cache


@lru_cache
def get_config():
    testing = os.getenv("TESTING", "false").lower() == "true"
    db_url = "sqlite+aiosqlite:///./test.db" if testing else os.getenv("DATABASE_URL", "postgresql+asyncpg://unified:unified@localhost:5432/unified")
    db_sync = "sqlite:///./test.db" if testing else os.getenv("DATABASE_URL_SYNC", "postgresql://unified:unified@localhost:5432/unified")
    return {
        "app_name": "Unified Platform (Medical/Aviation/Space)",
        "version": "1.0.0",
        "testing": testing,
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "database_url": db_url,
        "database_url_sync": db_sync,
        "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        "jwt_secret": os.getenv("JWT_SECRET", "change-me-in-production-secret-key"),
        "jwt_algorithm": "HS256",
        "jwt_expire_minutes": int(os.getenv("JWT_EXPIRE_MINUTES", "30")),
        "login_max_attempts": int(os.getenv("LOGIN_MAX_ATTEMPTS", "5")),
        "login_lockout_minutes": int(os.getenv("LOGIN_LOCKOUT_MINUTES", "15")),
        "audit_log_enabled": os.getenv("AUDIT_LOG_ENABLED", "true").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO").upper(),
        "otlp_endpoint": os.getenv("OTLP_ENDPOINT", "http://localhost:4317"),
        "slack_webhook_url": os.getenv("SLACK_WEBHOOK_URL", ""),
        "alert_email": os.getenv("ALERT_EMAIL", ""),
        "demo_login_enabled": os.getenv("DEMO_LOGIN_ENABLED", "false").lower() == "true",
    }
