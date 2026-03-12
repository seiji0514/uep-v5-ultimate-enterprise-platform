"""
OPC-UA クライアント
製造業 IoT、デジタルツイン連携
補強スキル: 製造、OPC-UA
"""
import os
from typing import Any, Dict, List, Optional

# opcua はオプショナル: pip install opcua
try:
    from opcua import Client

    OPCUA_AVAILABLE = True
except ImportError:
    OPCUA_AVAILABLE = False
    Client = None


class OPCUAClient:
    """OPC-UA クライアント（スケルトン）"""

    def __init__(
        self,
        endpoint: Optional[str] = None,
    ):
        self.endpoint = endpoint or os.getenv(
            "OPCUA_ENDPOINT", "opc.tcp://localhost:4840"
        )
        self._client = None

    def _get_client(self):
        if not OPCUA_AVAILABLE:
            raise RuntimeError("opcua not installed. pip install opcua")
        if self._client is None:
            self._client = Client(self.endpoint)
            self._client.connect()
        return self._client

    def read_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """ノードを読み取り"""
        if not OPCUA_AVAILABLE:
            return {"node_id": node_id, "value": "demo", "demo": True}
        try:
            c = self._get_client()
            node = c.get_node(node_id)
            value = node.get_value()
            return {"node_id": node_id, "value": value}
        except Exception:
            return None

    def browse_nodes(self, node_id: str = "i=84") -> List[Dict[str, Any]]:
        """ノードをブラウズ"""
        if not OPCUA_AVAILABLE:
            return [{"node_id": "ns=2;s=Demo", "browse_name": "Demo", "demo": True}]
        try:
            c = self._get_client()
            node = c.get_node(node_id)
            children = node.get_children()
            return [
                {
                    "node_id": c.nodeid.to_string(),
                    "browse_name": str(c.get_browse_name()),
                }
                for c in children[:10]
            ]
        except Exception:
            return []

    def close(self):
        """接続を閉じる"""
        if self._client:
            self._client.disconnect()
            self._client = None


opcua_client = OPCUAClient()
