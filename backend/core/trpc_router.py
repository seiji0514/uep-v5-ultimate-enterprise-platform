"""
tRPC 風ルーター（Python バックエンド）
型安全 API のスケルトン（フロントは TypeScript tRPC クライアントと連携）
補強スキル: tRPC、型安全 API
"""
from typing import Any, Callable, Dict, Generic, TypeVar

T = TypeVar("T")


class TRPCRouter(Generic[T]):
    """
    tRPC 風ルーター
    手続きを登録し、型付きで呼び出し可能にするスケルトン
    """

    def __init__(self, prefix: str = ""):
        self.prefix = prefix
        self._procedures: Dict[str, Callable[..., T]] = {}

    def query(self, name: str):
        """クエリ手続きを登録するデコレータ"""

        def decorator(fn: Callable[..., T]):
            key = f"{self.prefix}.{name}" if self.prefix else name
            self._procedures[key] = fn
            return fn

        return decorator

    def mutation(self, name: str):
        """ミューテーション手続きを登録するデコレータ（query と同じ）"""
        return self.query(name)

    def call(self, path: str, *args, **kwargs) -> T:
        """手続きを呼び出し"""
        if path not in self._procedures:
            raise KeyError(f"Procedure not found: {path}")
        return self._procedures[path](*args, **kwargs)

    def list_procedures(self) -> list:
        """登録済み手続き一覧"""
        return list(self._procedures.keys())


# グローバルルーター例
app_router = TRPCRouter(prefix="app")


@app_router.query("health")
def app_health() -> Dict[str, Any]:
    return {"status": "ok", "version": "5.0.0"}


@app_router.query("config")
def app_config() -> Dict[str, Any]:
    return {"debug": False, "api_version": "v1"}
