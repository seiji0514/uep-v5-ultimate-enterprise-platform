"""
衛星軌道追跡システム - ロギング設定
企業レベルのログ管理

作成日: 2025年11月2日
作成者: 小川清志
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config import settings

def setup_logger(name: str = "satellite_tracker") -> logging.Logger:
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
    """
    API リクエストをログ記録
    
    Parameters:
    -----------
    endpoint : str
        エンドポイント
    method : str
        HTTPメソッド
    status_code : int
        ステータスコード
    duration_ms : float
        処理時間（ミリ秒）
    """
    logger.info(
        f"API Request: {method} {endpoint} | Status: {status_code} | Duration: {duration_ms:.2f}ms"
    )


def log_orbit_calculation(satellite: str, duration_hours: float, data_points: int, calc_time_ms: float):
    """
    軌道計算をログ記録
    
    Parameters:
    -----------
    satellite : str
        衛星名
    duration_hours : float
        予測期間
    data_points : int
        データポイント数
    calc_time_ms : float
        計算時間（ミリ秒）
    """
    logger.info(
        f"Orbit Calculation: {satellite} | Duration: {duration_hours}h | "
        f"Points: {data_points} | Calc Time: {calc_time_ms:.2f}ms"
    )


def log_error(error_type: str, error_message: str, traceback_info: str = None):
    """
    エラーをログ記録
    
    Parameters:
    -----------
    error_type : str
        エラータイプ
    error_message : str
        エラーメッセージ
    traceback_info : str, optional
        トレースバック情報
    """
    logger.error(f"Error [{error_type}]: {error_message}")
    if traceback_info:
        logger.error(f"Traceback: {traceback_info}")
