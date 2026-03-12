"""
分野管理サービス
分野別モジュールを管理・統合
"""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DomainManager:
    """
    分野管理サービス
    
    機能:
    - 分野別モジュールの管理
    - 分野別クエリのルーティング
    - モジュール間の連携
    """
    
    def __init__(self, domain_modules: Dict):
        """
        初期化
        
        Args:
            domain_modules: 分野別モジュールの辞書
        """
        self.domain_modules = domain_modules
        logger.info(f"分野管理サービスを初期化しました: {len(domain_modules)}分野")
    
    async def process_domain_query(
        self,
        domain: str,
        text: str,
        connection_id: int
    ) -> str:
        """
        分野別クエリを処理
        
        Args:
            domain: 分野ID
            text: 質問文
            connection_id: 接続ID
        
        Returns:
            応答テキスト
        """
        try:
            if domain not in self.domain_modules:
                return f"未対応の分野です: {domain}"
            
            module = self.domain_modules[domain]
            
            # モジュールが利用可能か確認
            if hasattr(module, "is_available") and not module.is_available():
                return f"{domain}分野のサービスが利用できません。"
            
            # モジュールで処理
            response = await module.handle_query(text, connection_id)
            
            return response
        
        except Exception as e:
            logger.error(f"分野クエリ処理エラー: {e}")
            return f"エラーが発生しました: {str(e)}"
    
    def get_available_domains(self) -> list:
        """利用可能な分野のリストを取得"""
        available = []
        for domain_id, module in self.domain_modules.items():
            if hasattr(module, "is_available"):
                if module.is_available():
                    available.append(domain_id)
            else:
                available.append(domain_id)
        return available
    
    def get_domain_info(self, domain: str) -> Optional[Dict]:
        """分野情報を取得"""
        if domain not in self.domain_modules:
            return None
        
        module = self.domain_modules[domain]
        return {
            "id": domain,
            "name": module.get_display_name() if hasattr(module, "get_display_name") else domain,
            "description": module.get_description() if hasattr(module, "get_description") else "",
            "available": module.is_available() if hasattr(module, "is_available") else True
        }
