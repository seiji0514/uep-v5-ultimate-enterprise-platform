"""
セキュリティAPIエンドポイント
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Optional, Dict, Any
from datetime import datetime
from .vault_client import vault_client
from .zero_trust import zero_trust_policy
from .policies import SecurityPolicy, security_policy_manager
from .models import (
    PolicyCreate, PolicyUpdate
)
from auth.jwt_auth import get_current_active_user
from auth.rbac import require_role

router = APIRouter(prefix="/api/v1/security", tags=["セキュリティ"])


@router.get("/vault/status")
@require_role("admin")
async def get_vault_status(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Vaultの状態を取得"""
    is_authenticated = vault_client.is_authenticated()
    return {
        "status": "authenticated" if is_authenticated else "unauthenticated",
        "vault_url": vault_client.vault_url
    }


@router.get("/secrets")
@require_role("admin")
async def list_secrets(
    path: str = "secret",
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """シークレット一覧を取得"""
    try:
        secrets = vault_client.list_secrets(path=path)
        return {
            "secrets": [
                {
                    "path": f"{path}/{secret}",
                    "name": secret
                }
                for secret in secrets
            ],
            "count": len(secrets)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/secrets/{secret_path:path}")
async def get_secret(
    secret_path: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """シークレットを取得"""
    # ゼロトラストポリシーでアクセスを評価
    user_attributes = {
        "roles": current_user.get("roles", []),
        "permissions": current_user.get("permissions", []),
    }
    request_attributes = {
        "ip": "127.0.0.1",  # 実際の実装ではリクエストから取得
    }

    allowed, reason = zero_trust_policy.evaluate_access(
        resource_path=f"/api/v1/security/secrets/{secret_path}",
        user_attributes=user_attributes,
        request_attributes=request_attributes
    )

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=reason or "Access denied"
        )

    try:
        # Vaultからシークレットを取得
        full_path = f"secret/data/{secret_path}" if not secret_path.startswith("secret/") else secret_path
        secret_data = vault_client.read_secret(full_path)

        if not secret_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Secret not found"
            )

        return {
            "path": secret_path,
            "data": secret_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/secrets/{secret_path:path}")
@require_role("admin")
async def create_secret(
    secret_path: str,
    secret_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """シークレットを作成"""
    try:
        full_path = f"secret/data/{secret_path}" if not secret_path.startswith("secret/") else secret_path
        success = vault_client.write_secret(full_path, secret_data)

        if success:
            return {
                "message": "Secret created successfully",
                "path": secret_path
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create secret"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/policies", response_model=List[SecurityPolicy])
async def list_policies(
    policy_type: Optional[str] = None,
    enabled_only: bool = False,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """セキュリティポリシー一覧を取得"""
    policies = security_policy_manager.list_policies(
        policy_type=policy_type,
        enabled_only=enabled_only
    )
    return policies


@router.post("/policies", response_model=SecurityPolicy, status_code=status.HTTP_201_CREATED)
@require_role("admin")
async def create_policy(
    policy_data: PolicyCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """セキュリティポリシーを作成"""
    policy = SecurityPolicy(
        id=policy_data.id,
        name=policy_data.name,
        description=policy_data.description,
        policy_type=policy_data.policy_type,
        rules=policy_data.rules,
        enabled=policy_data.enabled if hasattr(policy_data, "enabled") else True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    return security_policy_manager.create_policy(policy)


@router.get("/policies/{policy_id}", response_model=SecurityPolicy)
async def get_policy(
    policy_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """セキュリティポリシーを取得"""
    policy = security_policy_manager.get_policy(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    return policy


@router.put("/policies/{policy_id}", response_model=SecurityPolicy)
@require_role("admin")
async def update_policy(
    policy_id: str,
    policy_data: PolicyUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """セキュリティポリシーを更新"""
    policy = security_policy_manager.update_policy(
        policy_id,
        **policy_data.dict(exclude_unset=True)
    )

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )

    return policy


@router.get("/zero-trust/evaluate")
async def evaluate_zero_trust(
    resource_path: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """ゼロトラストポリシーを評価"""
    user_attributes = {
        "roles": current_user.get("roles", []),
        "permissions": current_user.get("permissions", []),
        "mfa_verified": current_user.get("mfa_verified", False),
    }

    request_attributes = {
        "ip": "127.0.0.1",  # 実際の実装ではリクエストから取得
        "timestamp": datetime.utcnow().isoformat(),
    }

    allowed, reason = zero_trust_policy.evaluate_access(
        resource_path=resource_path,
        user_attributes=user_attributes,
        request_attributes=request_attributes
    )

    return {
        "allowed": allowed,
        "reason": reason,
        "resource_path": resource_path,
        "user_attributes": user_attributes
    }
