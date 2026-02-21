"""
データレイクAPIエンドポイント
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional, Dict, Any
from .minio_client import MinIOClient
from .catalog import catalog, DataCatalogEntry
from .governance import governance, DataGovernancePolicy
from .models import (
    BucketCreate, BucketResponse, ObjectInfo,
    CatalogCreate, CatalogUpdate, GovernancePolicyCreate
)
from auth.jwt_auth import get_current_active_user

router = APIRouter(prefix="/api/v1/data-lake", tags=["データレイク"])

# MinIOクライアントのインスタンス
minio_client = MinIOClient()


@router.get("/buckets", response_model=List[BucketResponse])
async def list_buckets(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """バケット一覧を取得"""
    try:
        buckets = minio_client.list_buckets()
        return [BucketResponse(**bucket) for bucket in buckets]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/buckets", response_model=BucketResponse, status_code=status.HTTP_201_CREATED)
async def create_bucket(
    bucket_data: BucketCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """バケットを作成"""
    try:
        created = minio_client.create_bucket(bucket_data.name, bucket_data.region)
        if not created:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bucket already exists"
            )

        # バケット作成後にカタログに登録（オプション）
        return BucketResponse(name=bucket_data.name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/buckets/{bucket_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bucket(
    bucket_name: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """バケットを削除"""
    try:
        deleted = minio_client.delete_bucket(bucket_name)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bucket not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/buckets/{bucket_name}/objects", response_model=List[ObjectInfo])
async def list_objects(
    bucket_name: str,
    prefix: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """オブジェクト一覧を取得"""
    # アクセス権限チェック
    user_roles = current_user.get("roles", [])
    if not governance.check_access(bucket_name, user_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    try:
        objects = minio_client.list_objects(bucket_name, prefix=prefix)
        return [ObjectInfo(**obj) for obj in objects]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/buckets/{bucket_name}/upload")
async def upload_file(
    bucket_name: str,
    file: UploadFile = File(...),
    object_name: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """ファイルをアップロード"""
    # アクセス権限チェック
    user_roles = current_user.get("roles", [])
    if not governance.check_access(bucket_name, user_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    try:
        object_name = object_name or file.filename
        file_data = await file.read()

        minio_client.upload_file(
            bucket_name,
            object_name,
            file_data,
            content_type=file.content_type
        )

        # カタログに登録
        catalog.register(
            name=file.filename or object_name,
            bucket_name=bucket_name,
            object_name=object_name,
            data_type="raw",  # デフォルト
            format=file.content_type or "application/octet-stream",
            owner=current_user["username"],
            size=len(file_data)
        )

        return {
            "message": "File uploaded successfully",
            "bucket": bucket_name,
            "object": object_name
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/buckets/{bucket_name}/objects/{object_name}")
async def download_file(
    bucket_name: str,
    object_name: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """ファイルをダウンロード"""
    # アクセス権限チェック
    user_roles = current_user.get("roles", [])
    if not governance.check_access(bucket_name, user_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    try:
        file_data = minio_client.download_file(bucket_name, object_name)
        object_info = minio_client.get_object_info(bucket_name, object_name)

        from fastapi.responses import Response
        return Response(
            content=file_data,
            media_type=object_info.get("content_type", "application/octet-stream"),
            headers={
                "Content-Disposition": f'attachment; filename="{object_name}"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/buckets/{bucket_name}/objects/{object_name}")
async def delete_object(
    bucket_name: str,
    object_name: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """オブジェクトを削除"""
    # アクセス権限チェック
    user_roles = current_user.get("roles", [])
    if not governance.check_access(bucket_name, user_roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    try:
        minio_client.delete_object(bucket_name, object_name)

        # カタログから削除
        catalog_id = f"{bucket_name}/{object_name}"
        catalog.delete(catalog_id)

        return {"message": "Object deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# データカタログエンドポイント
@router.get("/catalog", response_model=List[DataCatalogEntry])
async def list_catalog(
    data_type: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """カタログ一覧を取得"""
    tag_list = tags.split(",") if tags else None
    entries = catalog.list(data_type=data_type, owner=owner, tags=tag_list)
    return entries


@router.post("/catalog", response_model=DataCatalogEntry, status_code=status.HTTP_201_CREATED)
async def create_catalog_entry(
    catalog_data: CatalogCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """カタログエントリを作成"""
    entry = catalog.register(
        name=catalog_data.name,
        bucket_name=catalog_data.bucket_name,
        object_name=catalog_data.object_name,
        data_type=catalog_data.data_type,
        format=catalog_data.format,
        owner=current_user["username"],
        description=catalog_data.description,
        schema=catalog_data.schema,
        tags=catalog_data.tags,
        metadata=catalog_data.metadata
    )
    return entry


@router.get("/catalog/{catalog_id}", response_model=DataCatalogEntry)
async def get_catalog_entry(
    catalog_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """カタログエントリを取得"""
    entry = catalog.get(catalog_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog entry not found"
        )
    return entry


@router.put("/catalog/{catalog_id}", response_model=DataCatalogEntry)
async def update_catalog_entry(
    catalog_id: str,
    catalog_data: CatalogUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """カタログエントリを更新"""
    entry = catalog.update(
        catalog_id,
        **catalog_data.dict(exclude_unset=True)
    )
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog entry not found"
        )
    return entry


# データガバナンスエンドポイント
@router.get("/governance/policies", response_model=List[DataGovernancePolicy])
async def list_policies(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """ガバナンスポリシー一覧を取得"""
    return governance.list_policies()


@router.get("/governance/policies/{bucket_name}")
async def get_policy_for_bucket(
    bucket_name: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """バケットに適用されるポリシーを取得"""
    policy = governance.find_policy_for_bucket(bucket_name)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found for bucket"
        )
    return policy
