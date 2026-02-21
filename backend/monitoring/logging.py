"""
ログ管理モジュール
構造化ログの収集と送信（JSON形式、機密情報マスキング）
"""
import json
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

# 機密情報マスキング用パターン
_SENSITIVE_PATTERNS = [
    (
        re.compile(
            r'(password|passwd|secret|token|api_key)\s*[:=]\s*["\']?[^"\'\s]+', re.I
        ),
        r"\1=***MASKED***",
    ),
    (re.compile(r"Bearer\s+[A-Za-z0-9\-_.]+"), "Bearer ***MASKED***"),
]


def _mask_sensitive(msg: str) -> str:
    """機密情報をマスキング"""
    for pattern, repl in _SENSITIVE_PATTERNS:
        msg = pattern.sub(repl, msg)
    return msg


class JsonFormatter(logging.Formatter):
    """JSON形式の構造化ログフォーマッター"""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": _mask_sensitive(record.getMessage()),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if hasattr(record, "user_id"):
            log_obj["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id
        if hasattr(record, "service"):
            log_obj["service"] = record.service
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj, ensure_ascii=False)


class LogstashHandler(logging.Handler):
    """Logstashハンドラー"""

    def __init__(self, logstash_url: Optional[str] = None):
        """
        Logstashハンドラーを初期化

        Args:
            logstash_url: LogstashのURL（デフォルト: 環境変数から取得）
        """
        super().__init__()
        self.logstash_url = logstash_url or os.getenv(
            "LOGSTASH_URL", "http://logstash:8080"
        )
        self.client = httpx.AsyncClient(timeout=5.0)

    def emit(self, record: logging.LogRecord):
        """ログレコードをLogstashに送信"""
        try:
            log_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }

            # 追加のフィールド
            if hasattr(record, "user_id"):
                log_data["user_id"] = record.user_id

            if hasattr(record, "request_id"):
                log_data["request_id"] = record.request_id

            if hasattr(record, "service"):
                log_data["service"] = record.service

            # 例外情報
            if record.exc_info:
                log_data["exception"] = self.format(record)

            # 非同期で送信（実際の実装では適切に処理）
            # ここでは簡易実装のため同期送信
            try:
                import asyncio

                asyncio.create_task(self._send_log(log_data))
            except:
                pass  # エラー時は無視
        except Exception:
            self.handleError(record)

    async def _send_log(self, log_data: Dict[str, Any]):
        """ログをLogstashに送信"""
        try:
            await self.client.post(self.logstash_url, json=log_data)
        except Exception:
            pass  # エラー時は無視


class LoggingHandler:
    """ログ管理ハンドラークラス"""

    def __init__(self, service_name: str = "uep-backend"):
        """
        ログ管理ハンドラーを初期化

        Args:
            service_name: サービス名
        """
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)

        # コンソールハンドラー（構造化ログ JSON 形式）
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JsonFormatter())
        self.logger.addHandler(console_handler)

        # Logstashハンドラー（オプション）
        try:
            logstash_handler = LogstashHandler()
            self.logger.addHandler(logstash_handler)
        except Exception:
            pass  # Logstashが利用できない場合は無視

    def log_info(
        self,
        message: str,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        **kwargs
    ):
        """情報ログを記録"""
        extra = {"service": self.service_name, **kwargs}
        if user_id:
            extra["user_id"] = user_id
        if request_id:
            extra["request_id"] = request_id

        self.logger.info(message, extra=extra)

    def log_error(
        self,
        message: str,
        error: Optional[Exception] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        **kwargs
    ):
        """エラーログを記録"""
        extra = {"service": self.service_name, **kwargs}
        if user_id:
            extra["user_id"] = user_id
        if request_id:
            extra["request_id"] = request_id

        if error:
            self.logger.error(message, exc_info=error, extra=extra)
        else:
            self.logger.error(message, extra=extra)

    def log_warning(
        self,
        message: str,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        **kwargs
    ):
        """警告ログを記録"""
        extra = {"service": self.service_name, **kwargs}
        if user_id:
            extra["user_id"] = user_id
        if request_id:
            extra["request_id"] = request_id

        self.logger.warning(message, extra=extra)


# グローバルインスタンス
logging_handler = LoggingHandler()
