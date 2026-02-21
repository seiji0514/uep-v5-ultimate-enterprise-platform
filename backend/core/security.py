"""
セキュリティミドルウェア
CSRF保護、セキュリティヘッダーなど
"""
import hashlib
import hmac
import secrets
import time
from typing import Callable, Dict, List

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """セキュリティヘッダーを追加するミドルウェア"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # セキュリティヘッダーの追加
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"

        # `/docs`と`/redoc`のパスではCSPを緩和（Swagger UI用）
        if request.url.path.startswith("/docs") or request.url.path.startswith(
            "/redoc"
        ):
            # Swagger UI用のCSP（cdn.jsdelivr.netを許可、ソースマップも許可）
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https:; "
                "font-src 'self' data: https://cdn.jsdelivr.net; "
                "connect-src 'self' https://cdn.jsdelivr.net"
            )
        else:
            # 通常のCSP
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'"
            )

        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers[
            "Permissions-Policy"
        ] = "geolocation=(), microphone=(), camera=()"

        return response


class CSRFProtection:
    """CSRF保護クラス"""

    def __init__(self):
        self.secret = settings.CSRF_SECRET or settings.SECRET_KEY

    def generate_token(self) -> str:
        """CSRFトークンを生成"""
        return secrets.token_urlsafe(32)

    def validate_token(self, token: str, session_token: str) -> bool:
        """CSRFトークンを検証"""
        if not token or not session_token:
            return False

        # タイミング攻撃を防ぐため、hmac.compare_digestを使用
        return hmac.compare_digest(token.encode(), session_token.encode())

    def get_token_from_header(self, request: Request) -> str:
        """リクエストヘッダーからCSRFトークンを取得"""
        return request.headers.get("X-CSRF-Token", "")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """レート制限ミドルウェア"""

    def __init__(self, app, calls: int = 60, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: Dict[str, List[float]] = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        # クライアント識別子を取得（IPアドレスまたはユーザーID）
        client_id = request.client.host if request.client else "unknown"

        # 認証済みユーザーの場合はユーザーIDを使用
        if hasattr(request.state, "user") and request.state.user:
            client_id = request.state.user.get("username", client_id)

        current_time = time.time()

        # クライアントのリクエスト履歴を取得
        if client_id not in self.clients:
            self.clients[client_id] = []

        # 古いリクエストを削除
        self.clients[client_id] = [
            req_time
            for req_time in self.clients[client_id]
            if current_time - req_time < self.period
        ]

        # レート制限チェック
        if len(self.clients[client_id]) >= self.calls:
            from core.exceptions import RateLimitError

            raise RateLimitError(
                message=f"Rate limit exceeded. Maximum {self.calls} requests per {self.period} seconds.",
                retry_after=int(
                    self.period - (current_time - self.clients[client_id][0])
                ),
            )

        # リクエストを記録
        self.clients[client_id].append(current_time)

        response = await call_next(request)

        # レート制限ヘッダーを追加
        remaining = self.calls - len(self.clients[client_id])
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.period))

        return response


# グローバルインスタンス
csrf_protection = CSRFProtection()
