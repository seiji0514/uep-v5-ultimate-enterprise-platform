"""
DX・データ系 API
データレイク、AI/ML、生成AI
認証不要でデモ用サンプルデータを返す
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/dx-data", tags=["DX・データ系"])


def _data_lake_catalogs() -> List[Dict[str, Any]]:
    return [
        {"id": "cat-001", "name": "顧客データレイク", "size_gb": 1250, "records": 15000000, "last_ingest": (datetime.utcnow() - timedelta(hours=1)).isoformat(), "format": "Parquet"},
        {"id": "cat-002", "name": "ログアーカイブ", "size_gb": 3200, "records": 500000000, "last_ingest": (datetime.utcnow() - timedelta(minutes=30)).isoformat(), "format": "JSON"},
        {"id": "cat-003", "name": "機械学習データセット", "size_gb": 450, "records": 5000000, "last_ingest": (datetime.utcnow() - timedelta(days=1)).isoformat(), "format": "Parquet"},
        {"id": "cat-004", "name": "トランザクション履歴", "size_gb": 890, "records": 85000000, "last_ingest": (datetime.utcnow() - timedelta(minutes=15)).isoformat(), "format": "Parquet"},
        {"id": "cat-005", "name": "センサーデータアーカイブ", "size_gb": 2100, "records": 1200000000, "last_ingest": (datetime.utcnow() - timedelta(hours=2)).isoformat(), "format": "Parquet"},
        {"id": "cat-006", "name": "Webアクセスログ", "size_gb": 680, "records": 200000000, "last_ingest": (datetime.utcnow() - timedelta(minutes=5)).isoformat(), "format": "JSON"},
        {"id": "cat-007", "name": "在庫・在庫履歴", "size_gb": 320, "records": 45000000, "last_ingest": (datetime.utcnow() - timedelta(hours=4)).isoformat(), "format": "Parquet"},
        {"id": "cat-008", "name": "マーケティングデータ", "size_gb": 520, "records": 28000000, "last_ingest": (datetime.utcnow() - timedelta(days=2)).isoformat(), "format": "CSV"},
    ]


def _ml_models() -> List[Dict[str, Any]]:
    return [
        {"id": "model-001", "name": "推論モデルv1.2", "accuracy": 0.95, "status": "本番", "inference_count_today": 12500, "framework": "PyTorch"},
        {"id": "model-002", "name": "異常検知モデル", "accuracy": 0.92, "status": "検証中", "inference_count_today": 3200, "framework": "scikit-learn"},
        {"id": "model-003", "name": "レコメンドエンジン", "accuracy": 0.88, "status": "本番", "inference_count_today": 45000, "framework": "PyTorch"},
        {"id": "model-004", "name": "チャーン予測", "accuracy": 0.91, "status": "本番", "inference_count_today": 8200, "framework": "XGBoost"},
        {"id": "model-005", "name": "需要予測v2", "accuracy": 0.89, "status": "本番", "inference_count_today": 15600, "framework": "Prophet"},
        {"id": "model-006", "name": "画像分類v1", "accuracy": 0.94, "status": "本番", "inference_count_today": 28000, "framework": "TensorFlow"},
        {"id": "model-007", "name": "NLP感情分析", "accuracy": 0.87, "status": "検証中", "inference_count_today": 5600, "framework": "HuggingFace"},
        {"id": "model-008", "name": "在庫最適化", "accuracy": 0.93, "status": "本番", "inference_count_today": 4200, "framework": "scikit-learn"},
    ]


def _generative_ai_usage() -> List[Dict[str, Any]]:
    return [
        {"id": "gen-001", "operation": "RAG検索", "model": "gpt-4", "tokens_today": 125000, "status": "稼働中", "cost_estimate": 2.5},
        {"id": "gen-002", "operation": "要約生成", "model": "claude-3", "tokens_today": 85000, "status": "稼働中", "cost_estimate": 1.8},
        {"id": "gen-003", "operation": "コード補助", "model": "codellama", "tokens_today": 42000, "status": "稼働中", "cost_estimate": 0.5},
        {"id": "gen-004", "operation": "ドキュメント生成", "model": "gpt-4", "tokens_today": 68000, "status": "稼働中", "cost_estimate": 1.4},
        {"id": "gen-005", "operation": "チャットボット", "model": "claude-3", "tokens_today": 210000, "status": "稼働中", "cost_estimate": 4.2},
        {"id": "gen-006", "operation": "画像生成", "model": "DALL-E 3", "tokens_today": 8500, "status": "稼働中", "cost_estimate": 1.7},
        {"id": "gen-007", "operation": "翻訳API", "model": "gpt-4", "tokens_today": 95000, "status": "稼働中", "cost_estimate": 1.9},
        {"id": "gen-008", "operation": "FAQ自動応答", "model": "claude-3", "tokens_today": 125000, "status": "稼働中", "cost_estimate": 2.5},
    ]


def _data_pipelines() -> List[Dict[str, Any]]:
    return [
        {"id": "pipe-001", "name": "日次ログ集計", "schedule": "0 2 * * *", "status": "成功", "last_run": (datetime.utcnow() - timedelta(hours=8)).isoformat(), "duration_min": 12},
        {"id": "pipe-002", "name": "リアルタイム取り込み", "schedule": "継続", "status": "実行中", "last_run": (datetime.utcnow() - timedelta(minutes=1)).isoformat(), "duration_min": 0},
        {"id": "pipe-003", "name": "週次レポート", "schedule": "0 9 * * 1", "status": "待機", "last_run": (datetime.utcnow() - timedelta(days=2)).isoformat(), "duration_min": 45},
        {"id": "pipe-004", "name": "ML学習パイプライン", "schedule": "0 3 * * *", "status": "成功", "last_run": (datetime.utcnow() - timedelta(hours=5)).isoformat(), "duration_min": 90},
        {"id": "pipe-005", "name": "データ品質チェック", "schedule": "*/30 * * * *", "status": "実行中", "last_run": (datetime.utcnow() - timedelta(minutes=5)).isoformat(), "duration_min": 3},
        {"id": "pipe-006", "name": "顧客データ同期", "schedule": "0 1 * * *", "status": "成功", "last_run": (datetime.utcnow() - timedelta(hours=9)).isoformat(), "duration_min": 25},
        {"id": "pipe-007", "name": "在庫集計", "schedule": "0 */6 * * *", "status": "成功", "last_run": (datetime.utcnow() - timedelta(hours=2)).isoformat(), "duration_min": 8},
        {"id": "pipe-008", "name": "SLAレポート", "schedule": "0 8 1 * *", "status": "待機", "last_run": (datetime.utcnow() - timedelta(days=10)).isoformat(), "duration_min": 15},
    ]


@router.get("/data-lake-catalogs")
async def get_data_lake():
    return {"items": _data_lake_catalogs(), "total": len(_data_lake_catalogs())}


@router.get("/ml-models")
async def get_ml_models():
    return {"items": _ml_models(), "total": len(_ml_models())}


@router.get("/generative-ai-usage")
async def get_genai_usage():
    return {"items": _generative_ai_usage(), "total": len(_generative_ai_usage())}


@router.get("/data-pipelines")
async def get_pipelines():
    return {"items": _data_pipelines(), "total": len(_data_pipelines())}


@router.get("/dashboard")
async def get_dashboard():
    return {
        "data_lake_total_gb": sum(c["size_gb"] for c in _data_lake_catalogs()),
        "ml_models_count": len(_ml_models()),
        "genai_tokens_today": sum(g["tokens_today"] for g in _generative_ai_usage()),
        "pipelines_running": len([p for p in _data_pipelines() if p["status"] == "実行中"]),
    }
