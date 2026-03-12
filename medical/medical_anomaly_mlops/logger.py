"""
医療データ異常検知MLOps - ロギング設定
企業レベルのログ管理

作成日: 2025年11月2日
作成者: 小川清志
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config import settings

def setup_logger(name: str = "medical_mlops") -> logging.Logger:
    """
    ロガーをセットアップ
    
    Parameters:
    -----------
    name : str
        ロガー名
        
    Returns:
    --------
    logger : logging.Logger
        設定済みロガー
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # 既存のハンドラをクリア
    logger.handlers.clear()
    
    # フォーマッター
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # コンソールハンドラ
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ファイルハンドラ（ログローテーション付き）
    if settings.LOG_FILE:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            settings.LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# グローバルロガーインスタンス
logger = setup_logger()


def log_api_request(endpoint: str, method: str, status_code: int, duration_ms: float):
    """API リクエストをログ記録"""
    logger.info(
        f"API Request: {method} {endpoint} | Status: {status_code} | Duration: {duration_ms:.2f}ms"
    )


def log_prediction(num_samples: int, num_anomalies: int, calc_time_ms: float, accuracy: float):
    """異常検知予測をログ記録"""
    logger.info(
        f"Prediction: Samples={num_samples} | Anomalies={num_anomalies} | "
        f"Accuracy={accuracy:.2%} | Time={calc_time_ms:.2f}ms"
    )


def log_model_training(samples: int, accuracy: float, training_time_sec: float):
    """モデル訓練をログ記録"""
    logger.info(
        f"Model Training: Samples={samples} | Accuracy={accuracy:.2%} | "
        f"Time={training_time_sec:.2f}s"
    )


def log_error(error_type: str, error_message: str, traceback_info: str = None):
    """エラーをログ記録"""
    logger.error(f"Error [{error_type}]: {error_message}")
    if traceback_info:
        logger.error(f"Traceback: {traceback_info}")

