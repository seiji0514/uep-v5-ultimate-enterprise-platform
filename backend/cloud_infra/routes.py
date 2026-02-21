"""
クラウドインフラAPIエンドポイント
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .iac import IaCProvider, IaCTemplate, iac_manager
from .infrastructure import (InfrastructureResource, ResourceStatus,
                             ResourceType, infrastructure_manager)
from .models import (DeploymentCreate, DeploymentUpdate, IaCDeploy,
                     IaCTemplateCreate, ResourceCreate)
from .orchestration import (Deployment, DeploymentStatus,
                            OrchestrationPlatform, orchestration_manager)

router = APIRouter(prefix="/api/v1/cloud-infra", tags=["クラウドインフラ"])


@router.get("/resources", response_model=List[InfrastructureResource])
@require_permission("read")
async def list_resources(
    resource_type: Optional[str] = None,
    provider: Optional[str] = None,
    status: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """リソース一覧を取得"""
    resource_type_enum = ResourceType(resource_type) if resource_type else None
    status_enum = ResourceStatus(status) if status else None
    resources = infrastructure_manager.list_resources(
        resource_type=resource_type_enum, provider=provider, status=status_enum
    )
    return resources


@router.post(
    "/resources",
    response_model=InfrastructureResource,
    status_code=status.HTTP_201_CREATED,
)
@require_permission("manage_infrastructure")
async def create_resource(
    resource_data: ResourceCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """リソースを作成"""
    resource_type = ResourceType(resource_data.resource_type)
    resource = infrastructure_manager.create_resource(
        name=resource_data.name,
        resource_type=resource_type,
        provider=resource_data.provider,
        region=resource_data.region,
        config=resource_data.config,
        tags=resource_data.tags,
    )
    return resource


@router.get("/iac/templates", response_model=List[IaCTemplate])
@require_permission("read")
async def list_templates(
    provider: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """IaCテンプレート一覧を取得"""
    provider_enum = IaCProvider(provider) if provider else None
    templates = iac_manager.list_templates(provider=provider_enum)
    return templates


@router.post(
    "/iac/templates", response_model=IaCTemplate, status_code=status.HTTP_201_CREATED
)
@require_permission("manage_infrastructure")
async def create_template(
    template_data: IaCTemplateCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """IaCテンプレートを作成"""
    provider = IaCProvider(template_data.provider)
    template = iac_manager.create_template(
        name=template_data.name,
        provider=provider,
        template_content=template_data.template_content,
        created_by=current_user["username"],
        description=template_data.description,
        variables=template_data.variables,
    )
    return template


@router.post("/iac/templates/{template_id}/deploy")
@require_permission("manage_infrastructure")
async def deploy_template(
    template_id: str,
    deploy_data: IaCDeploy,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """IaCテンプレートをデプロイ"""
    try:
        deployment = iac_manager.deploy_template(
            template_id=template_id, variables=deploy_data.variables
        )
        return deployment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/deployments", response_model=List[Deployment])
@require_permission("read")
async def list_deployments(
    platform: Optional[str] = None,
    namespace: Optional[str] = None,
    status: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """デプロイメント一覧を取得"""
    platform_enum = OrchestrationPlatform(platform) if platform else None
    status_enum = DeploymentStatus(status) if status else None
    deployments = orchestration_manager.list_deployments(
        platform=platform_enum, namespace=namespace, status=status_enum
    )
    return deployments


@router.post(
    "/deployments", response_model=Deployment, status_code=status.HTTP_201_CREATED
)
@require_permission("manage_infrastructure")
async def create_deployment(
    deployment_data: DeploymentCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """デプロイメントを作成"""
    platform = OrchestrationPlatform(deployment_data.platform)
    deployment = orchestration_manager.create_deployment(
        name=deployment_data.name,
        platform=platform,
        image=deployment_data.image,
        replicas=deployment_data.replicas,
        config=deployment_data.config,
        namespace=deployment_data.namespace,
    )
    return deployment


@router.post("/deployments/{deployment_id}/scale")
@require_permission("manage_infrastructure")
async def scale_deployment(
    deployment_id: str,
    replicas: int,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """デプロイメントをスケール"""
    deployment = orchestration_manager.scale_deployment(deployment_id, replicas)
    if deployment:
        return deployment
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Deployment not found"
        )
