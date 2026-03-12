"""
インフラ構築専用システム - データモデル
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BuildStage(str, Enum):
    """構築ステージ"""

    DESIGN = "design"  # 設計
    BUILD = "build"  # 構築
    DEPLOY = "deploy"  # デプロイ
    VERIFY = "verify"  # 検証
    COMPLETED = "completed"  # 完了


class BuildProjectStatus(str, Enum):
    """プロジェクトステータス"""

    DRAFT = "draft"  # 下書き
    IN_PROGRESS = "in_progress"  # 進行中
    COMPLETED = "completed"  # 完了
    FAILED = "failed"  # 失敗
    CANCELLED = "cancelled"  # キャンセル


class PipelineStatus(str, Enum):
    """パイプラインステータス"""

    PENDING = "pending"  # 待機中
    RUNNING = "running"  # 実行中
    SUCCESS = "success"  # 成功
    FAILED = "failed"  # 失敗
    CANCELLED = "cancelled"  # キャンセル


# --- リクエストモデル ---


class BuildProjectCreate(BaseModel):
    """構築プロジェクト作成"""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    target_provider: str = "docker"  # docker, kubernetes, terraform
    blueprint: Optional[Dict[str, Any]] = None


class BuildProjectUpdate(BaseModel):
    """構築プロジェクト更新"""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[BuildProjectStatus] = None


class PipelineCreate(BaseModel):
    """パイプライン作成"""

    project_id: str
    stages: List[str] = ["design", "build", "deploy", "verify"]


class BlueprintCreate(BaseModel):
    """ブループリント作成"""

    name: str = Field(..., min_length=1, max_length=200)
    provider: str = "terraform"  # terraform, docker-compose, kubernetes
    content: str = Field(..., min_length=1)
    variables: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
