"""
MLモデルレジストリモジュール
MLモデルの管理・デプロイ・監視
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ModelStatus(str, Enum):
    """モデルステータス"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"


class ModelVersion(BaseModel):
    """モデルバージョン"""

    model_config = {"protected_namespaces": ()}

    version: str
    model_path: str
    metrics: Dict[str, float]
    status: ModelStatus = ModelStatus.DEVELOPMENT
    created_at: datetime
    created_by: str
    metadata: Optional[Dict[str, Any]] = None


class MLModel(BaseModel):
    """MLモデル"""

    model_config = {"protected_namespaces": ()}

    id: str
    name: str
    description: Optional[str] = None
    model_type: str  # classification, regression, etc.
    framework: str  # tensorflow, pytorch, sklearn, etc.
    versions: List[ModelVersion] = []
    current_version: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    created_by: str


class ModelRegistry:
    """モデルレジストリクラス"""

    def __init__(self):
        """モデルレジストリを初期化"""
        self._models: Dict[str, MLModel] = {}

    def register_model(
        self,
        name: str,
        model_type: str,
        framework: str,
        created_by: str,
        description: Optional[str] = None,
    ) -> MLModel:
        """モデルを登録"""
        model_id = str(uuid.uuid4())

        model = MLModel(
            id=model_id,
            name=name,
            description=description,
            model_type=model_type,
            framework=framework,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by=created_by,
        )

        self._models[model_id] = model
        return model

    def register_version(
        self,
        model_id: str,
        version: str,
        model_path: str,
        metrics: Dict[str, float],
        created_by: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ModelVersion:
        """モデルバージョンを登録"""
        model = self._models.get(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")

        model_version = ModelVersion(
            version=version,
            model_path=model_path,
            metrics=metrics,
            created_at=datetime.utcnow(),
            created_by=created_by,
            metadata=metadata,
        )

        model.versions.append(model_version)
        model.current_version = version
        model.updated_at = datetime.utcnow()

        return model_version

    def promote_version(
        self, model_id: str, version: str, target_status: ModelStatus
    ) -> bool:
        """モデルバージョンをプロモート"""
        model = self._models.get(model_id)
        if not model:
            return False

        version_obj = next((v for v in model.versions if v.version == version), None)
        if not version_obj:
            return False

        version_obj.status = target_status
        if target_status == ModelStatus.PRODUCTION:
            model.current_version = version

        model.updated_at = datetime.utcnow()
        return True

    def get_model(self, model_id: str) -> Optional[MLModel]:
        """モデルを取得"""
        return self._models.get(model_id)

    def list_models(
        self, model_type: Optional[str] = None, status: Optional[ModelStatus] = None
    ) -> List[MLModel]:
        """モデル一覧を取得"""
        models = list(self._models.values())

        if model_type:
            models = [m for m in models if m.model_type == model_type]

        if status:
            models = [
                m
                for m in models
                if m.current_version
                and any(
                    v.version == m.current_version and v.status == status
                    for v in m.versions
                )
            ]

        return models

    def deploy_model(
        self, model_id: str, version: str, deployment_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """モデルをデプロイ"""
        model = self._models.get(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")

        version_obj = next((v for v in model.versions if v.version == version), None)
        if not version_obj:
            raise ValueError(f"Version {version} not found")

        # デプロイ処理（簡易実装）
        deployment_id = str(uuid.uuid4())

        return {
            "deployment_id": deployment_id,
            "model_id": model_id,
            "version": version,
            "status": "deployed",
            "endpoint": f"/api/v1/mlops/models/{model_id}/predict",
            "created_at": datetime.utcnow().isoformat(),
        }


# グローバルインスタンス
model_registry = ModelRegistry()
