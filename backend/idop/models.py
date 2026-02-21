"""
IDOP関連のデータモデル
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class CICDPipelineCreate(BaseModel):
    """CI/CDパイプライン作成モデル"""
    name: str
    repository: str
    branch: str = "main"
    stages: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None


class CICDTrigger(BaseModel):
    """CI/CDトリガーモデル"""
    commit_hash: Optional[str] = None


class ApplicationCreate(BaseModel):
    """アプリケーション作成モデル"""
    name: str
    repository: str
    description: Optional[str] = None
    environments: Optional[List[str]] = None


class ApplicationDeploy(BaseModel):
    """アプリケーションデプロイモデル"""
    environment: str
    version: str
    config: Optional[Dict[str, Any]] = None
