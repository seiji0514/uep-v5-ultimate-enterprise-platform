"""
Vaultクライアントモジュール
HashiCorp Vaultへの接続と操作を実装
"""
import os
from typing import Any, Dict, List, Optional

import hvac


class VaultClient:
    """Vaultクライアントクラス"""

    def __init__(
        self, vault_url: Optional[str] = None, vault_token: Optional[str] = None
    ):
        """
        Vaultクライアントを初期化

        Args:
            vault_url: VaultのURL（デフォルト: 環境変数から取得）
            vault_token: Vaultトークン（デフォルト: 環境変数から取得）
        """
        self.vault_url = vault_url or os.getenv("VAULT_ADDR", "http://vault:8200")
        self.vault_token = vault_token or os.getenv("VAULT_TOKEN", "root")

        # Vaultクライアントを作成
        self.client = hvac.Client(url=self.vault_url, token=self.vault_token)

    def is_authenticated(self) -> bool:
        """認証状態を確認"""
        try:
            return self.client.is_authenticated()
        except Exception:
            return False

    def read_secret(self, path: str) -> Optional[Dict[str, Any]]:
        """
        シークレットを読み取り

        Args:
            path: シークレットパス（例: "secret/data/myapp/database"）

        Returns:
            シークレットデータ
        """
        try:
            # KV v2エンジンの場合
            if path.startswith("secret/data/"):
                response = self.client.secrets.kv.v2.read_secret_version(
                    path=path.replace("secret/data/", "")
                )
                return response.get("data", {}).get("data", {})
            else:
                # KV v1エンジンの場合
                response = self.client.secrets.kv.v1.read_secret(path=path)
                return response.get("data", {})
        except Exception as e:
            print(f"Failed to read secret: {e}")
            return None

    def write_secret(self, path: str, data: Dict[str, Any]) -> bool:
        """
        シークレットを書き込み

        Args:
            path: シークレットパス
            data: シークレットデータ

        Returns:
            成功したかどうか
        """
        try:
            # KV v2エンジンの場合
            if path.startswith("secret/data/"):
                self.client.secrets.kv.v2.create_or_update_secret(
                    path=path.replace("secret/data/", ""), secret=data
                )
            else:
                # KV v1エンジンの場合
                self.client.secrets.kv.v1.create_or_update_secret(
                    path=path, secret=data
                )
            return True
        except Exception as e:
            print(f"Failed to write secret: {e}")
            return False

    def delete_secret(self, path: str) -> bool:
        """シークレットを削除"""
        try:
            # KV v2エンジンの場合
            if path.startswith("secret/data/"):
                self.client.secrets.kv.v2.delete_metadata_and_all_versions(
                    path=path.replace("secret/data/", "")
                )
            else:
                # KV v1エンジンの場合
                self.client.secrets.kv.v1.delete_secret(path=path)
            return True
        except Exception as e:
            print(f"Failed to delete secret: {e}")
            return False

    def list_secrets(self, path: str = "secret") -> List[str]:
        """シークレット一覧を取得"""
        try:
            # KV v2エンジンの場合
            if path.startswith("secret/data/"):
                response = self.client.secrets.kv.v2.list_secrets(
                    path=path.replace("secret/data/", "")
                )
                return response.get("data", {}).get("keys", [])
            else:
                # KV v1エンジンの場合
                response = self.client.secrets.kv.v1.list_secrets(path=path)
                return response.get("data", {}).get("keys", [])
        except Exception as e:
            print(f"Failed to list secrets: {e}")
            return []

    def generate_dynamic_credentials(
        self, role: str, mount_point: str = "database"
    ) -> Optional[Dict[str, Any]]:
        """
        動的認証情報を生成（データベース等）

        Args:
            role: ロール名
            mount_point: マウントポイント（デフォルト: database）

        Returns:
            認証情報（username, password等）
        """
        try:
            response = self.client.secrets.database.generate_credentials(
                name=role, mount_point=mount_point
            )
            return response.get("data", {})
        except Exception as e:
            print(f"Failed to generate dynamic credentials: {e}")
            return None

    def revoke_lease(self, lease_id: str) -> bool:
        """リースを取り消し"""
        try:
            self.client.sys.revoke_lease(lease_id=lease_id)
            return True
        except Exception as e:
            print(f"Failed to revoke lease: {e}")
            return False


# グローバルインスタンス
vault_client = VaultClient()
