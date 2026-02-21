"""
MLOps関連のデータモデル
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class PipelineCreate(BaseModel):
    """パイプライン作成モデル"""

    name: str
    description: Optional[str] = None
    stages: List[Dict[str, Any]]


class PipelineExecute(BaseModel):
    """パイプライン実行モデル"""

    config: Optional[Dict[str, Any]] = None


class ModelCreate(BaseModel):
    """モデル作成モデル"""

    model_config = {"protected_namespaces": ()}

    name: str
    model_type: str
    framework: str
    description: Optional[str] = None


class ModelVersionCreate(BaseModel):
    """モデルバージョン作成モデル"""

    model_config = {"protected_namespaces": ()}

    version: str
    model_path: str
    metrics: Dict[str, float]
    metadata: Optional[Dict[str, Any]] = None


class ExperimentCreate(BaseModel):
    """実験作成モデル"""

    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class ExperimentUpdate(BaseModel):
    """実験更新モデル"""

    parameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, float]] = None
    status: Optional[str] = None
    artifacts: Optional[List[str]] = None
