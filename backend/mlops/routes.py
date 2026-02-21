"""
MLOps APIエンドポイント
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .experiment_tracking import Experiment, experiment_tracker
from .model_registry import MLModel, ModelStatus, model_registry
from .models import (
    ExperimentCreate,
    ExperimentUpdate,
    ModelCreate,
    ModelVersionCreate,
    PipelineCreate,
    PipelineExecute,
)
from .pipeline import MLPipeline, PipelineStatus, pipeline_executor

router = APIRouter(prefix="/api/v1/mlops", tags=["MLOps"])


@router.get("/pipelines", response_model=List[MLPipeline])
@require_permission("read")
async def list_pipelines(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """パイプライン一覧を取得"""
    pipelines = pipeline_executor.list_pipelines()
    return pipelines


@router.post(
    "/pipelines", response_model=MLPipeline, status_code=status.HTTP_201_CREATED
)
@require_permission("manage_mlops")
async def create_pipeline(
    pipeline_data: PipelineCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """パイプラインを作成"""
    pipeline = pipeline_executor.create_pipeline(
        name=pipeline_data.name,
        stages=pipeline_data.stages,
        created_by=current_user["username"],
        description=pipeline_data.description,
    )
    return pipeline


@router.get("/pipelines/{pipeline_id}", response_model=MLPipeline)
@require_permission("read")
async def get_pipeline(
    pipeline_id: str, current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """パイプラインを取得"""
    pipeline = pipeline_executor.get_pipeline(pipeline_id)
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found"
        )
    return pipeline


@router.post("/pipelines/{pipeline_id}/execute")
@require_permission("manage_mlops")
async def execute_pipeline(
    pipeline_id: str, current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """パイプラインを実行"""
    try:
        execution = pipeline_executor.execute_pipeline(pipeline_id)
        return execution
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/models", response_model=List[MLModel])
@require_permission("read")
async def list_models(
    model_type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """モデル一覧を取得"""
    model_status = ModelStatus(status) if status else None
    models = model_registry.list_models(model_type=model_type, status=model_status)
    return models


@router.post("/models", response_model=MLModel, status_code=status.HTTP_201_CREATED)
@require_permission("manage_mlops")
async def register_model(
    model_data: ModelCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """モデルを登録"""
    model = model_registry.register_model(
        name=model_data.name,
        model_type=model_data.model_type,
        framework=model_data.framework,
        created_by=current_user["username"],
        description=model_data.description,
    )
    return model


@router.post("/models/{model_id}/versions")
@require_permission("manage_mlops")
async def register_version(
    model_id: str,
    version_data: ModelVersionCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """モデルバージョンを登録"""
    try:
        version = model_registry.register_version(
            model_id=model_id,
            version=version_data.version,
            model_path=version_data.model_path,
            metrics=version_data.metrics,
            created_by=current_user["username"],
            metadata=version_data.metadata,
        )
        return version
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/models/{model_id}/versions/{version}/promote")
@require_permission("manage_mlops")
async def promote_version(
    model_id: str,
    version: str,
    target_status: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """モデルバージョンをプロモート"""
    try:
        model_status = ModelStatus(target_status)
        success = model_registry.promote_version(model_id, version, model_status)
        if success:
            return {"message": f"Version {version} promoted to {target_status}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to promote version",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status"
        )


@router.post("/models/{model_id}/deploy")
@require_permission("manage_mlops")
async def deploy_model(
    model_id: str,
    version: str,
    deployment_config: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """モデルをデプロイ"""
    try:
        deployment = model_registry.deploy_model(
            model_id=model_id, version=version, deployment_config=deployment_config
        )
        return deployment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/experiments", response_model=List[Experiment])
@require_permission("read")
async def list_experiments(
    tags: Optional[str] = None,
    status: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """実験一覧を取得"""
    tag_list = tags.split(",") if tags else None
    experiments = experiment_tracker.list_experiments(tags=tag_list, status=status)
    return experiments


@router.post(
    "/experiments", response_model=Experiment, status_code=status.HTTP_201_CREATED
)
@require_permission("manage_mlops")
async def create_experiment(
    experiment_data: ExperimentCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """実験を作成"""
    experiment = experiment_tracker.create_experiment(
        name=experiment_data.name,
        created_by=current_user["username"],
        description=experiment_data.description,
        parameters=experiment_data.parameters,
        tags=experiment_data.tags,
    )
    return experiment


@router.put("/experiments/{experiment_id}")
@require_permission("manage_mlops")
async def update_experiment(
    experiment_id: str,
    experiment_data: ExperimentUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """実験を更新"""
    experiment = experiment_tracker.get_experiment(experiment_id)
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found"
        )

    if experiment_data.parameters:
        experiment_tracker.log_parameters(experiment_id, experiment_data.parameters)

    if experiment_data.metrics:
        experiment_tracker.log_metrics(experiment_id, experiment_data.metrics)

    if experiment_data.status == "completed":
        experiment_tracker.complete_experiment(experiment_id)

    return experiment_tracker.get_experiment(experiment_id)


@router.post("/experiments/compare")
@require_permission("read")
async def compare_experiments(
    experiment_ids: List[str],
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """実験を比較"""
    comparison = experiment_tracker.compare_experiments(experiment_ids)
    return comparison
