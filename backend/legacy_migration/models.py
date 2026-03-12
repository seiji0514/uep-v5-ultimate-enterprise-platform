"""
レガシー移行 - Pydanticモデル
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class MigrationJobCreate(BaseModel):
    """移行ジョブ作成"""

    source_type: str  # csv, excel, db, api
    source_config: Dict[str, Any]  # 接続情報等
    target_system: str  # erp_sales, erp_purchasing, accounting
    mapping: Optional[Dict[str, str]] = None  # フィールドマッピング


class MigrationValidationRequest(BaseModel):
    """移行検証リクエスト"""

    job_id: str
    compare_field: str  # 比較対象フィールド
