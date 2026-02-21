"""
エラーハンドラーモジュール
統一されたエラーレスポンス
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.exceptions import UEPException
from core.config import settings
import traceback
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def uep_exception_handler(request: Request, exc: UEPException):
    """UEP例外ハンドラー"""
    logger.error(
        f"UEP Exception: {exc.message}",
        extra={
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "path": request.url.path,
                "timestamp": str(datetime.utcnow())
            }
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """HTTP例外ハンドラー"""
    # 404 時に登録ルートをログ（Chaos/GraphQL デバッグ用）
    if exc.status_code == 404 and request.url.path in ("/chaos-ok", "/api/v1/chaos/status", "/graphql"):
        app = request.app
        routes_info = []
        for r in getattr(app, "routes", []):
            if hasattr(r, "path") and r.path:
                routes_info.append(r.path)
            elif hasattr(r, "path") and hasattr(r, "routes"):
                for sr in getattr(r, "routes", []):
                    if hasattr(sr, "path") and sr.path:
                        routes_info.append(f"{r.path}->{sr.path}")
        logger.warning(f"404 for {request.url.path} - registered paths sample: {routes_info[:15]}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "status_code": exc.status_code,
                "path": request.url.path,
                "timestamp": str(datetime.utcnow())
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """バリデーション例外ハンドラー"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "errors": errors,
                "path": request.url.path,
                "timestamp": str(datetime.utcnow())
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """一般的な例外ハンドラー"""
    # デバッグモードまたは開発環境では詳細なエラー情報を表示
    is_debug = settings.DEBUG or settings.ENVIRONMENT == "development"
    
    if is_debug:
        error_detail = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc().split('\n')[-10:]  # 最後の10行のみ
        }
    else:
        error_detail = {
            "message": "An internal server error occurred"
        }

    logger.exception(
        f"Unhandled exception: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc()
        }
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc) if is_debug else "An internal server error occurred",
                "details": error_detail,
                "path": request.url.path,
                "timestamp": str(datetime.utcnow())
            }
        }
    )
