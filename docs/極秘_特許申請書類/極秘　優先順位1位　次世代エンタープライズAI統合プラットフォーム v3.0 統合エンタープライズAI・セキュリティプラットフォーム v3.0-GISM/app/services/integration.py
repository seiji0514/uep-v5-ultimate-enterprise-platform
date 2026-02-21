"""
既存システム統合サービス
- スーパーコンピューターAIプラットフォーム v7.0との統合
"""
import os
import logging
from typing import Dict, Any, List
import httpx

logger = logging.getLogger(__name__)


class IntegrationService:
    """既存システム統合サービス"""
    
    def __init__(self):
        self.existing_systems = {
            "supercomputer_ai_platform_v7": {
                "name": "スーパーコンピューターAIプラットフォーム v7.0",
                "base_url": os.getenv(
                    "SUPERCOMPUTER_AI_V7_URL",
                    "http://localhost:8001"
                ),
                "status": "disconnected"
            }
        }
    
    def is_available(self) -> bool:
        """サービス利用可能性チェック"""
        return True
    
    async def connect_existing_systems(self) -> Dict[str, Any]:
        """
        既存システムとの接続
        """
        connected = []
        failed = []
        
        for system_id, system_info in self.existing_systems.items():
            try:
                # ヘルスチェック
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(f"{system_info['base_url']}/health")
                    
                    if response.status_code == 200:
                        system_info["status"] = "connected"
                        connected.append(system_id)
                    else:
                        system_info["status"] = "failed"
                        failed.append(system_id)
            except Exception as e:
                logger.error(f"Failed to connect to {system_id}: {e}")
                system_info["status"] = "failed"
                failed.append(system_id)
        
        return {
            "connected": connected,
            "failed": failed,
            "systems": self.existing_systems
        }
    
    async def call_existing_system(
        self,
        system_id: str,
        endpoint: str,
        method: str = "GET",
        data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        既存システムへのAPI呼び出し
        """
        if system_id not in self.existing_systems:
            return {
                "status": "error",
                "message": f"System {system_id} not found"
            }
        
        system_info = self.existing_systems[system_id]
        
        if system_info["status"] != "connected":
            return {
                "status": "error",
                "message": f"System {system_id} is not connected"
            }
        
        try:
            url = f"{system_info['base_url']}{endpoint}"
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method == "GET":
                    response = await client.get(url)
                elif method == "POST":
                    response = await client.post(url, json=data)
                else:
                    return {
                        "status": "error",
                        "message": f"Unsupported method: {method}"
                    }
                
                return {
                    "status": "success",
                    "data": response.json(),
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error(f"API call error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

