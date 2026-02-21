"""
CQRSモジュール
Command Query Responsibility Segregationパターンの実装
イベントストリーミング（Kafka）と連携し、コマンド実行時にイベントを発行
"""
from typing import Dict, Any, Optional, Callable
from abc import ABC, abstractmethod
from pydantic import BaseModel
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

# Kafka イベント発行（オプション）
_cqrs_kafka_client = None


def set_cqrs_kafka_client(client):
    """CQRS 用 Kafka クライアントを設定（イベントストリーミング連携）"""
    global _cqrs_kafka_client
    _cqrs_kafka_client = client


class Command(BaseModel):
    """コマンド（書き込み操作）"""
    command_id: str
    command_type: str
    aggregate_id: Optional[str] = None
    command_data: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[str] = None


class Query(BaseModel):
    """クエリ（読み取り操作）"""
    query_id: str
    query_type: str
    query_params: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[str] = None


class CommandHandler(ABC):
    """コマンドハンドラーの基底クラス"""

    @abstractmethod
    async def handle(self, command: Command) -> Dict[str, Any]:
        """コマンドを処理"""
        pass


class QueryHandler(ABC):
    """クエリハンドラーの基底クラス"""

    @abstractmethod
    async def handle(self, query: Query) -> Dict[str, Any]:
        """クエリを処理"""
        pass


class CQRSBus:
    """CQRSバスクラス"""

    def __init__(self):
        """CQRSバスを初期化"""
        self._command_handlers: Dict[str, CommandHandler] = {}
        self._query_handlers: Dict[str, QueryHandler] = {}

    def register_command_handler(
        self,
        command_type: str,
        handler: CommandHandler
    ):
        """コマンドハンドラーを登録"""
        self._command_handlers[command_type] = handler

    def register_query_handler(
        self,
        query_type: str,
        handler: QueryHandler
    ):
        """クエリハンドラーを登録"""
        self._query_handlers[query_type] = handler

    async def execute_command(self, command: Command) -> Dict[str, Any]:
        """コマンドを実行し、成功時に Kafka へイベント発行（CQRS + イベントストリーミング連携）"""
        handler = self._command_handlers.get(command.command_type)
        if not handler:
            raise ValueError(f"No handler registered for command type: {command.command_type}")

        result = await handler.handle(command)

        # コマンド成功時に Kafka へイベント発行（Event Sourcing 連携）
        if _cqrs_kafka_client:
            try:
                _cqrs_kafka_client.publish_event(
                    topic="cqrs-commands",
                    event_type=f"command.{command.command_type}",
                    data={
                        "command_id": command.command_id,
                        "command_type": command.command_type,
                        "aggregate_id": command.aggregate_id,
                        "result": result,
                        "user_id": command.user_id,
                    },
                    key=command.aggregate_id or command.command_id,
                )
            except Exception as e:
                logger.warning("CQRS event publish failed: %s", e)

        return result

    async def execute_query(self, query: Query) -> Dict[str, Any]:
        """クエリを実行"""
        handler = self._query_handlers.get(query.query_type)
        if not handler:
            raise ValueError(f"No handler registered for query type: {query.query_type}")

        return await handler.handle(query)


class UserCommandHandler(CommandHandler):
    """ユーザーコマンドハンドラー（例）"""

    async def handle(self, command: Command) -> Dict[str, Any]:
        """ユーザーコマンドを処理"""
        if command.command_type == "create_user":
            # ユーザー作成処理
            return {
                "status": "success",
                "message": "User created",
                "user_id": command.command_data.get("user_id")
            }
        elif command.command_type == "update_user":
            # ユーザー更新処理
            return {
                "status": "success",
                "message": "User updated",
                "user_id": command.aggregate_id
            }
        else:
            raise ValueError(f"Unknown command type: {command.command_type}")


class UserQueryHandler(QueryHandler):
    """ユーザークエリハンドラー（例）"""

    async def handle(self, query: Query) -> Dict[str, Any]:
        """ユーザークエリを処理"""
        if query.query_type == "get_user":
            # ユーザー取得処理
            user_id = query.query_params.get("user_id")
            return {
                "user_id": user_id,
                "username": "example_user",
                "email": "user@example.com"
            }
        elif query.query_type == "list_users":
            # ユーザー一覧取得処理
            return {
                "users": [
                    {"user_id": "1", "username": "user1"},
                    {"user_id": "2", "username": "user2"}
                ],
                "total": 2
            }
        else:
            raise ValueError(f"Unknown query type: {query.query_type}")


# グローバルCQRSバスインスタンス
cqrs_bus = CQRSBus()

# デフォルトハンドラーを登録
cqrs_bus.register_command_handler("create_user", UserCommandHandler())
cqrs_bus.register_command_handler("update_user", UserCommandHandler())
cqrs_bus.register_query_handler("get_user", UserQueryHandler())
cqrs_bus.register_query_handler("list_users", UserQueryHandler())
