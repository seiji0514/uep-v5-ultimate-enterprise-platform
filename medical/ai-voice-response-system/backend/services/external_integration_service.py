"""
外部システム統合サービス
既存システム以外の外部サービスと連携
"""
import logging
import httpx
from typing import Dict, Optional, List
import json

logger = logging.getLogger(__name__)


class ExternalIntegrationService:
    """
    外部システム統合サービス
    
    機能:
    - 外部APIとの連携
    - RAGシステムとの統合
    - データベースとの連携
    - タスク管理システムとの連携
    """
    
    def __init__(self):
        self.rag_service = None
        self.external_apis = {}
        self._initialize_services()
    
    def _initialize_services(self):
        """サービスを初期化"""
        # RAGサービスの初期化（既存システムから）
        try:
            # 既存のRAGサービスをインポート
            import sys
            from pathlib import Path
            
            # プロジェクトルートを追加
            project_root = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(project_root))
            
            # 既存のRAGサービスを探す
            rag_paths = [
                project_root / "llm-rag-chatbot" / "rag_engine.py",
                project_root / "ultimate-ai-platform" / "backend" / "services" / "rag_service.py",
            ]
            
            for rag_path in rag_paths:
                if rag_path.exists():
                    logger.info(f"RAGサービスが見つかりました: {rag_path}")
                    # 動的にインポート（実装は後で）
                    break
        
        except Exception as e:
            logger.warning(f"RAGサービスの初期化に失敗: {e}")
    
    async def detect_intent(self, text: str) -> Dict[str, any]:
        """
        ユーザーの意図を検出
        
        Returns:
            {
                "intent": "weather|calendar|task|email|file|code|learning|health|smart_home|general",
                "entities": {...},
                "confidence": 0.0-1.0
            }
        """
        text_lower = text.lower()
        
        # 意図の検出
        intents = {
            "weather": ["天気", "weather", "気温", "温度"],
            "calendar": ["予定", "スケジュール", "calendar", "カレンダー"],
            "task": ["タスク", "task", "todo", "やること"],
            "email": ["メール", "email", "メッセージ"],
            "file": ["ファイル", "file", "ドキュメント"],
            "code": ["コード", "code", "プログラム", "実行"],
            "learning": ["勉強", "学習", "learn", "study"],
            "health": ["健康", "health", "体重", "歩数"],
            "smart_home": ["電気", "light", "エアコン", "air"],
            "rag": ["検索", "search", "調べて", "教えて"],
        }
        
        detected_intent = "general"
        max_matches = 0
        
        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > max_matches:
                max_matches = matches
                detected_intent = intent
        
        return {
            "intent": detected_intent,
            "confidence": max_matches / max(len(intents[detected_intent]), 1),
            "entities": self._extract_entities(text, detected_intent)
        }
    
    def _extract_entities(self, text: str, intent: str) -> Dict:
        """エンティティを抽出"""
        entities = {}
        
        if intent == "weather":
            # 場所を抽出
            import re
            location_patterns = [
                r"(.+?)の天気",
                r"(.+?)の気温",
            ]
            for pattern in location_patterns:
                match = re.search(pattern, text)
                if match:
                    entities["location"] = match.group(1)
                    break
        
        elif intent == "task":
            # タスク情報を抽出
            if "作成" in text:
                entities["action"] = "create"
            elif "一覧" in text or "確認" in text:
                entities["action"] = "list"
            elif "完了" in text:
                entities["action"] = "complete"
        
        return entities
    
    async def handle_external_request(
        self,
        intent: str,
        text: str,
        entities: Dict
    ) -> Optional[str]:
        """
        外部システムへのリクエストを処理
        
        Returns:
            応答テキスト（Noneの場合は通常の応答生成を使用）
        """
        try:
            if intent == "weather":
                return await self._handle_weather(entities)
            
            elif intent == "calendar":
                return await self._handle_calendar()
            
            elif intent == "task":
                return await self._handle_task(text, entities)
            
            elif intent == "rag":
                return await self._handle_rag_search(text)
            
            # その他の意図は通常の応答生成を使用
            return None
        
        except Exception as e:
            logger.error(f"外部リクエスト処理エラー: {e}")
            return None
    
    async def _handle_weather(self, entities: Dict) -> str:
        """天気情報を取得"""
        location = entities.get("location", "東京")
        
        try:
            # OpenWeatherMap API等を使用（実装例）
            # 実際の実装では、APIキーが必要
            async with httpx.AsyncClient() as client:
                # 例: 天気APIを呼び出し
                # response = await client.get(f"https://api.openweathermap.org/...")
                # weather_data = response.json()
                
                # モック応答
                return f"{location}の天気は晴れ、気温は25度です。"
        
        except Exception as e:
            logger.error(f"天気情報取得エラー: {e}")
            return f"{location}の天気情報を取得できませんでした。"
    
    async def _handle_calendar(self) -> str:
        """カレンダー情報を取得"""
        try:
            # Google Calendar API等を使用
            # 実装例（モック）
            events = [
                {"title": "会議", "time": "14:00"},
                {"title": "面談", "time": "16:00"},
            ]
            
            if events:
                events_text = "\n".join([
                    f"- {event['time']}: {event['title']}"
                    for event in events
                ])
                return f"今日の予定は以下の通りです:\n{events_text}"
            else:
                return "今日の予定はありません。"
        
        except Exception as e:
            logger.error(f"カレンダー情報取得エラー: {e}")
            return "カレンダー情報を取得できませんでした。"
    
    async def _handle_task(self, text: str, entities: Dict) -> str:
        """タスク管理を処理"""
        action = entities.get("action", "list")
        
        try:
            if action == "create":
                # タスク情報を抽出
                task_title = text.replace("タスクを作成", "").replace("タスクを追加", "").strip()
                # タスク管理APIを呼び出し
                # await create_task(task_title)
                return f"タスク「{task_title}」を作成しました。"
            
            elif action == "list":
                # タスク一覧を取得
                # tasks = await get_tasks()
                tasks = ["会議の準備", "資料作成"]
                if tasks:
                    tasks_text = "\n".join([f"- {task}" for task in tasks])
                    return f"タスク一覧:\n{tasks_text}"
                else:
                    return "タスクはありません。"
            
            elif action == "complete":
                # タスクを完了
                task_id = entities.get("task_id")
                # await complete_task(task_id)
                return "タスクを完了しました。"
        
        except Exception as e:
            logger.error(f"タスク管理エラー: {e}")
            return "タスクの処理に失敗しました。"
    
    async def _handle_rag_search(self, text: str) -> Optional[str]:
        """RAG検索を実行"""
        try:
            if not self.rag_service:
                return None
            
            # RAGサービスで検索
            # response, sources = await self.rag_service.query_with_rag(text)
            # return response
            
            # 実装は既存のRAGサービスと統合が必要
            return None
        
        except Exception as e:
            logger.error(f"RAG検索エラー: {e}")
            return None
    
    async def integrate_with_rag(self, rag_service):
        """既存のRAGサービスと統合"""
        self.rag_service = rag_service
        logger.info("RAGサービスと統合しました")
    
    async def add_external_api(self, name: str, api_config: Dict):
        """外部APIを追加"""
        self.external_apis[name] = api_config
        logger.info(f"外部APIを追加しました: {name}")
