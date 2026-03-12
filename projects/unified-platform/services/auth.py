"""Phase 2: JWT Auth - RBAC"""
from datetime import datetime, timedelta
from typing import Optional
import bcrypt  # bcrypt 4.1+ 互換: passlib が __about__ を参照するため
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("_", (), {"__version__": getattr(bcrypt, "__version__", "4.0")})()
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader

from config import get_config

cfg = get_config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_password(plain: str, hashed: str) -> bool:
    """bcrypt を直接使用（passlib の互換問題を回避）"""
    if not hashed or not plain:
        return False
    try:
        if hashed.startswith("$2"):
            return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
        return pwd_context.verify(plain, hashed)
    except Exception:
        try:
            return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
        except Exception:
            return False


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=cfg["jwt_expire_minutes"]))
    payload = {"sub": subject, "exp": expire, "iat": datetime.utcnow()}
    return jwt.encode(payload, cfg["jwt_secret"], algorithm=cfg["jwt_algorithm"])


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, cfg["jwt_secret"], algorithms=[cfg["jwt_algorithm"]])
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    api_key: str = Depends(api_key_header),
) -> Optional[str]:
    """Phase 2: Auth - JWT or API Key"""
    if credentials:
        token = credentials.credentials
        payload = decode_token(token)
        if payload:
            return payload.get("sub")
    if api_key and api_key == "unified-demo-key":
        return "api-key-user"
    return None


async def require_auth(user: Optional[str] = Depends(get_current_user)) -> str:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
