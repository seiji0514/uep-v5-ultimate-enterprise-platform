"""
UEP v5.0 - Backend API
次世代エンタープライズ統合プラットフォーム v5.0
エンタープライズレベルの実装
"""
import logging
import warnings

# 警告フィルターの設定
warnings.filterwarnings(
    "ignore", message='Field name "schema" shadows an attribute in parent "BaseModel"'
)
warnings.filterwarnings(
    "ignore", category=UserWarning, module="pydantic._internal_fields"
)
warnings.filterwarnings(
    "ignore", message="pkg_resources is deprecated", category=UserWarning
)

# ロギング設定
logging.getLogger("kafka").setLevel(logging.ERROR)  # Kafkaの警告を抑制
logging.getLogger("opentelemetry").setLevel(logging.ERROR)  # OpenTelemetryの警告を抑制

import os
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# コアモジュールのインポート
from core.config import settings
from core.database import get_db, init_db
from core.error_handler import (
    general_exception_handler,
    http_exception_handler,
    uep_exception_handler,
    validation_exception_handler,
)
from core.exceptions import UEPException
from core.rate_limit import limiter
from core.security import SecurityHeadersMiddleware, csrf_protection

try:
    from slowapi.errors import RateLimitExceeded
except ImportError:
    from slowapi import RateLimitExceeded

# 環境変数の読み込み（.envファイルがある場合）
env_file = Path(".env")
if env_file.exists():
    from dotenv import load_dotenv

    load_dotenv()

from auth.jwt_auth import get_current_active_user, get_current_user
from auth.rbac import require_permission, require_role

# 認証・認可モジュールのインポート
from auth.routes import router as auth_router

# データレイクモジュールのインポート
from data_lake.routes import router as data_lake_router

# イベントストリーミングモジュールのインポート（オプショナル）
try:
    from event_streaming.routes import router as event_streaming_router

    EVENT_STREAMING_AVAILABLE = True
except ImportError as e:
    import logging

    logger = logging.getLogger(__name__)
    logger.warning(f"Event streaming module not available: {e}")
    EVENT_STREAMING_AVAILABLE = False
    event_streaming_router = None

from ai_dev.routes import router as ai_dev_router
from cloud_infra.routes import router as cloud_infra_router
from generative_ai.routes import router as generative_ai_router
from idop.routes import router as idop_router

# Phase 2: コアシステム層のインポート
from mlops.routes import router as mlops_router
from monitoring.logging import logging_handler
from monitoring.metrics import metrics_collector

# 監視・オブザーバビリティモジュールのインポート
from monitoring.routes import router as monitoring_router
from monitoring.tracing import tracing_handler

# セキュリティモジュールのインポート
from security.routes import router as security_router
from security.zero_trust import zero_trust_policy
from security_center.routes import router as security_center_router

# インクルーシブ雇用AIプラットフォーム（障害者雇用マッチング + アクセシビリティ + UX評価）
try:
    from inclusive_work.routes import router as inclusive_work_router

    INCLUSIVE_WORK_AVAILABLE = True
except ImportError as e:
    import logging

    logging.getLogger(__name__).warning(f"Inclusive work module not available: {e}")
    INCLUSIVE_WORK_AVAILABLE = False
    inclusive_work_router = None

# Chaos Engineering（障害シミュレーション・レジリエンス検証）
from chaos.routes import router as chaos_router

# Level 3: エコシステムモジュール
from ecosystem.routes import router as ecosystem_router

# Level 5: グローバルエンタープライズモジュール
from global_enterprise.routes import router as global_enterprise_router

# Level 4: インダストリーリーダーモジュール
from industry_leader.routes import router as industry_leader_router

# Level 2: プラットフォームモジュール
from platform_level.routes import router as platform_router

# 統合ビジネスプラットフォーム（業務効率化・人材・顧客対応の3システム統合）
from unified_business_platform.routes import router as unified_business_router

# GraphQL（strawberry-graphql が必要。graphql_api は graphql パッケージとの名前衝突回避）
try:
    from graphql_api.routes import graphql_router

    GRAPHQL_AVAILABLE = True
except ImportError as e:
    import logging

    logger = logging.getLogger(__name__)
    logger.warning(
        f"GraphQL module not available (pip install strawberry-graphql[fastapi]): {e}"
    )
    GRAPHQL_AVAILABLE = False
    graphql_router = None

# Phase 4: 最適化モジュールのインポート（オプショナル）
# グローバル変数を事前に初期化（確実に定義されるように）
performance_optimizer = None
optimization_router = None
OPTIMIZATION_AVAILABLE = False

try:
    from optimization.performance import performance_optimizer
    from optimization.routes import router as optimization_router

    OPTIMIZATION_AVAILABLE = True
except ImportError as e:
    import logging

    logger = logging.getLogger(__name__)
    logger.warning(f"Optimization module not available: {e}")
    # performance_optimizer と optimization_router は既に None に設定済み
except Exception as e:
    import logging

    logger = logging.getLogger(__name__)
    logger.warning(f"Failed to import optimization module: {e}")
    # performance_optimizer と optimization_router は既に None に設定済み


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時の処理
    # データベーステーブルの作成（開発環境のみ）
    if settings.DEBUG:
        try:
            init_db()
        except Exception as e:
            print(f"Warning: Database initialization failed: {e}")

    # 登録ルートの確認（Chaos/GraphQL のデバッグ用）
    def _get_paths(routes, prefix=""):
        paths = []
        for r in routes:
            if hasattr(r, "path") and r.path:
                paths.append(prefix + r.path)
            if hasattr(r, "routes"):
                paths.extend(_get_paths(r.routes, prefix))
        return paths

    all_paths = _get_paths(app.routes)
    chaos_paths = [p for p in all_paths if "chaos" in p]
    chaos_ok = "/chaos-ok" in all_paths
    print(
        f"""
    ==========================================
    {settings.APP_NAME} v{settings.APP_VERSION}
    ==========================================
    Environment: {settings.ENVIRONMENT}
    Debug Mode: {settings.DEBUG}
    Server: http://{settings.HOST}:{settings.PORT}
    API Docs: http://{settings.HOST}:{settings.PORT}/docs
    ------------------------------------------
    [DEBUG] /chaos-ok: {'OK' if chaos_ok else 'NOT FOUND'}
    [DEBUG] Chaos paths: {chaos_paths[:5] if chaos_paths else '(none)'}
    [DEBUG] Instance ID: {_chaos_instance_id}  ← /chaos-ok のレスポンスと一致すれば同一プロセス
    ==========================================
    """
    )

    yield

    # 終了時の処理
    print("Shutting down UEP v5.0...")


app = FastAPI(
    title=settings.APP_NAME,
    description="次世代エンタープライズ統合プラットフォーム v5.0 - エンタープライズレベル実装",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",  # 開発環境では常に有効
    lifespan=lifespan,
)

# Chaos 診断ルートを最優先で登録（add_api_route で同期的に登録）
import random as _rand

_chaos_instance_id = f"{time.time():.0f}-{_rand.randint(1000,9999)}"


async def _chaos_ok_handler():
    return {
        "status": "ok",
        "instance_id": _chaos_instance_id,
        "message": "Chaos/GraphQL",
    }


async def _chaos_status_handler():
    return {
        "enabled": True,
        "endpoints": {
            "delay": "/api/v1/chaos/delay",
            "error": "/api/v1/chaos/error",
            "mixed": "/api/v1/chaos/mixed",
        },
        "description": "障害シミュレーション用エンドポイント（開発・検証環境向け）",
    }


app.add_api_route(
    "/chaos-ok", _chaos_ok_handler, methods=["GET"], include_in_schema=False
)
app.add_api_route(
    "/api/v1/chaos/status",
    _chaos_status_handler,
    methods=["GET"],
    tags=["Chaos Engineering"],
)

# レート制限の設定
app.state.limiter = limiter
try:
    from slowapi import _rate_limit_exceeded_handler

    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
except ImportError:
    # slowapiのバージョンによっては異なるパスからインポート
    try:
        from slowapi.errors import _rate_limit_exceeded_handler

        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    except ImportError:
        # レート制限エラーハンドラーが利用できない場合はスキップ
        pass

# エラーハンドラーの登録
app.add_exception_handler(UEPException, uep_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 認証ルーターを追加
app.include_router(auth_router)

# データレイクルーターを追加
app.include_router(data_lake_router)

# イベントストリーミングルーターを追加（利用可能な場合）
if EVENT_STREAMING_AVAILABLE and event_streaming_router:
    app.include_router(event_streaming_router)

# 監視・オブザーバビリティルーターを追加
app.include_router(monitoring_router)

# セキュリティルーターを追加
app.include_router(security_router)

# Phase 2: コアシステム層のルーターを追加
app.include_router(mlops_router)
app.include_router(generative_ai_router)
app.include_router(security_center_router)
app.include_router(cloud_infra_router)
app.include_router(idop_router)
app.include_router(ai_dev_router)
if INCLUSIVE_WORK_AVAILABLE and inclusive_work_router:
    app.include_router(inclusive_work_router)
app.include_router(platform_router)
app.include_router(ecosystem_router)
app.include_router(industry_leader_router)
app.include_router(global_enterprise_router)
app.include_router(unified_business_router)
# chaos_router は include するが、確実に動作するよう /api/v1/chaos/status は上記で直接定義
try:
    app.include_router(chaos_router)
except Exception as e:
    import logging

    logging.getLogger(__name__).warning(f"Chaos router not included: {e}")
if GRAPHQL_AVAILABLE and graphql_router:
    app.include_router(graphql_router, prefix="/graphql")
else:
    # GraphQL が利用できない場合のフォールバック
    @app.get("/graphql", tags=["GraphQL"])
    async def graphql_fallback():
        return {
            "message": "GraphQL not available. Install: pip install strawberry-graphql[fastapi]"
        }


# Phase 4: 最適化ルーターを追加（利用可能な場合）
if OPTIMIZATION_AVAILABLE and optimization_router:
    app.include_router(optimization_router)

# OpenTelemetryでFastAPIを計装
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    FastAPIInstrumentor.instrument_app(app)
except Exception:
    pass  # OpenTelemetryが利用できない場合は無視

# セキュリティヘッダーミドルウェア（最初に追加）
app.add_middleware(SecurityHeadersMiddleware)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=[
        "X-Request-ID",
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
    ],
)


# リクエストIDミドルウェア
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    import time

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # メトリクス収集用の開始時間
    start_time = time.time()

    try:
        # 公開エンドポイントはゼロトラストポリシーの評価をスキップ
        public_paths = [
            "/",
            "/health",
            "/metrics",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/health",
            "/graphql",
            "/chaos-ok",
        ]
        is_public_path = (
            request.url.path in public_paths
            or request.url.path.startswith("/docs")
            or request.url.path.startswith("/static")
            or request.url.path.startswith("/graphql")
            or request.url.path.startswith("/api/v1/chaos")
        )

        # ゼロトラストポリシーでアクセスを評価（公開エンドポイントとセキュリティエンドポイント以外）
        if not is_public_path and not request.url.path.startswith("/api/v1/security"):
            # ユーザー情報を取得（認証済みの場合）
            user_attributes = {}
            try:
                from auth.jwt_auth import get_current_user

                # 認証トークンがある場合のみ評価
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    # 簡易的な実装（実際にはトークンを検証）
                    user_attributes = {
                        "roles": ["user"],  # 実際の実装ではトークンから取得
                        "permissions": ["read"],
                    }
            except:
                pass

            request_attributes = {
                "ip": request.client.host if request.client else "unknown",
                "timestamp": datetime.utcnow().isoformat(),
            }

            allowed, reason = zero_trust_policy.evaluate_access(
                resource_path=request.url.path,
                user_attributes=user_attributes,
                request_attributes=request_attributes,
            )

            if not allowed and user_attributes:  # 認証済みの場合のみチェック
                from fastapi.responses import JSONResponse

                return JSONResponse(
                    status_code=403,
                    content={"detail": reason or "Access denied by zero trust policy"},
                )

        response = await call_next(request)

        # メトリクスを記録
        duration = time.time() - start_time
        metrics_collector.record_request(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
            duration=duration,
        )

        # パフォーマンスメトリクスを記録（利用可能な場合）
        if performance_optimizer:
            try:
                performance_optimizer.record_request(
                    endpoint=request.url.path,
                    response_time=duration,
                    is_error=(response.status_code >= 400),
                )
            except Exception as e:
                # パフォーマンス記録のエラーはログに記録するが、リクエスト処理は続行
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to record performance metrics: {e}")

        # ログを記録
        logging_handler.log_info(
            f"{request.method} {request.url.path} - {response.status_code}",
            request_id=request_id,
        )

        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as e:
        # エラーメトリクスを記録
        metrics_collector.record_error(error_type=type(e).__name__, service="backend")

        # エラーログを記録
        logging_handler.log_error(
            f"{request.method} {request.url.path} - Error",
            error=e,
            request_id=request_id,
        )
        raise


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "UEP v5.0 - Ultimate Enterprise Platform",
        "version": settings.APP_VERSION,
        "status": "running",
        "practical_maximum_difficulty": True,
        "levels": [
            "Level 1: Enterprise",
            "Level 2: Platform",
            "Level 3: Ecosystem",
            "Level 4: Industry Leader",
            "Level 5: Global (design)",
        ],
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1",
        "graphql": "/graphql",
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "service": "UEP v5.0 Backend API",
    }


@app.get("/metrics")
async def metrics():
    """Prometheusメトリクスエンドポイント"""
    return metrics_collector.get_metrics()


@app.get("/api/v1/health")
async def api_health():
    """APIヘルスチェック"""
    return {"status": "healthy", "version": "5.0.0", "timestamp": time.time()}


@app.get("/api/v1/grpc/status", tags=["gRPC"])
async def grpc_status():
    """gRPC サービス状態（proto 生成コードの有無）"""
    try:
        from grpc_service import uep_internal_pb2  # noqa: F401

        return {
            "available": True,
            "port": int(os.getenv("GRPC_PORT", "50051")),
            "message": "gRPC service ready. Start with: python -m grpc_service.server",
        }
    except ImportError:
        return {
            "available": False,
            "message": "Run: pip install grpcio-tools && python -m grpc_tools.protoc -I. --python_out=grpc_service --grpc_python_out=grpc_service grpc_service/proto/uep_internal.proto",
        }


@app.get("/api/v1/services")
async def list_services(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """登録されているサービス一覧（認証必須）"""
    return {
        "services": [
            {"name": "backend-api", "url": "http://backend:8000", "status": "active"},
            {
                "name": "mlops-service",
                "url": "http://mlops-service:8003",
                "status": "pending",
            },
            {
                "name": "generative-ai-service",
                "url": "http://generative-ai-service:8004",
                "status": "pending",
            },
            {
                "name": "security-service",
                "url": "http://security-service:8005",
                "status": "pending",
            },
        ],
        "user": current_user["username"],
    }


@app.get("/api/v1/gateway/routes")
@require_permission("read")
async def list_routes(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """登録されているルート一覧（read権限必須）"""
    return {
        "routes": [
            {
                "path": "/api/v1",
                "service": "backend-api",
                "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            },
            {
                "path": "/api/v1/mlops",
                "service": "mlops-service",
                "methods": ["GET", "POST"],
            },
            {
                "path": "/api/v1/generative-ai",
                "service": "generative-ai-service",
                "methods": ["GET", "POST"],
            },
            {
                "path": "/api/v1/security",
                "service": "security-service",
                "methods": ["GET", "POST"],
            },
        ],
        "user": current_user["username"],
        "permissions": current_user.get("permissions", []),
    }


@app.get("/api/v1/admin/users")
@require_role("admin")
async def list_users(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """ユーザー一覧（adminロール必須）"""
    from auth.routes import get_demo_users

    demo_users = get_demo_users()
    users = []
    for username, user_data in demo_users.items():
        users.append(
            {
                "username": user_data["username"],
                "email": user_data["email"],
                "full_name": user_data.get("full_name"),
                "department": user_data.get("department"),
                "roles": user_data.get("roles", []),
                "is_active": user_data.get("is_active", True),
            }
        )

    return {
        "users": users,
        "total": len(users),
        "requested_by": current_user["username"],
    }


if __name__ == "__main__":
    # reload=True だと子プロセスでルートが正しく読み込まれない場合があるため、app オブジェクトを直接渡す
    # reload が必要な場合は reload=True に戻し、起動後にファイル変更で自動再起動される
    if settings.DEBUG:
        uvicorn.run(
            app,  # オブジェクトを直接渡す（reload 時は "main:app" が必要だが、ルート未登録の不具合回避のため app を使用）
            host=settings.HOST,
            port=settings.PORT,
            log_level=settings.LOG_LEVEL.lower(),
            reload=False,  # True にすると /chaos-ok 等が 404 になる不具合あり
            access_log=True,
        )
    else:
        uvicorn.run(
            app,
            host=settings.HOST,
            port=settings.PORT,
            log_level=settings.LOG_LEVEL.lower(),
            reload=False,
            access_log=True,
        )
