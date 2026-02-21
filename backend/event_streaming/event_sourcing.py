"""
Event Sourcingモジュール
イベントソーシングパターンの実装
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from .kafka_client import KafkaClient


class EventType(str, Enum):
    """イベントタイプ"""
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    STATE_CHANGED = "state_changed"


class DomainEvent(BaseModel):
    """ドメインイベント"""
    event_id: str
    aggregate_id: str
    aggregate_type: str
    event_type: str
    event_data: Dict[str, Any]
    timestamp: datetime
    version: int
    metadata: Optional[Dict[str, Any]] = None


class EventStore:
    """イベントストアクラス"""

    def __init__(self, kafka_client: KafkaClient):
        """
        イベントストアを初期化

        Args:
            kafka_client: Kafkaクライアントインスタンス
        """
        self.kafka_client = kafka_client
        self.topic_prefix = "events-"

    def _get_topic_name(self, aggregate_type: str) -> str:
        """集約タイプからトピック名を生成"""
        return f"{self.topic_prefix}{aggregate_type}"

    def append_event(self, event: DomainEvent) -> bool:
        """イベントを追加"""
        topic = self._get_topic_name(event.aggregate_type)

        # トピックが存在しない場合は作成
        try:
            self.kafka_client.create_topic(topic)
        except:
            pass  # 既に存在する場合は無視

        return self.kafka_client.publish_event(
            topic=topic,
            event_type=event.event_type,
            data={
                "event_id": event.event_id,
                "aggregate_id": event.aggregate_id,
                "aggregate_type": event.aggregate_type,
                "event_data": event.event_data,
                "timestamp": event.timestamp.isoformat(),
                "version": event.version,
                "metadata": event.metadata
            },
            key=event.aggregate_id
        )

    def get_events(
        self,
        aggregate_type: str,
        aggregate_id: Optional[str] = None,
        max_events: int = 100
    ) -> List[DomainEvent]:
        """イベントを取得"""
        topic = self._get_topic_name(aggregate_type)
        group_id = f"event-store-{aggregate_type}"

        messages = self.kafka_client.consume_events(
            topic=topic,
            group_id=group_id,
            max_messages=max_events
        )

        events = []
        for msg in messages:
            value = msg["value"]
            if aggregate_id is None or value.get("aggregate_id") == aggregate_id:
                events.append(DomainEvent(
                    event_id=value["event_id"],
                    aggregate_id=value["aggregate_id"],
                    aggregate_type=value["aggregate_type"],
                    event_type=value["event_type"],
                    event_data=value["event_data"],
                    timestamp=datetime.fromisoformat(value["timestamp"]),
                    version=value["version"],
                    metadata=value.get("metadata")
                ))

        # バージョン順にソート
        events.sort(key=lambda e: e.version)
        return events


class EventSourcingHandler:
    """イベントソーシングハンドラークラス"""

    def __init__(self, event_store: EventStore):
        """
        イベントソーシングハンドラーを初期化

        Args:
            event_store: イベントストアインスタンス
        """
        self.event_store = event_store
        self._aggregates: Dict[str, Dict[str, Any]] = {}  # 簡易的な集約状態ストア

    def apply_event(self, event: DomainEvent) -> Dict[str, Any]:
        """イベントを適用して集約状態を更新"""
        aggregate_key = f"{event.aggregate_type}:{event.aggregate_id}"

        if aggregate_key not in self._aggregates:
            self._aggregates[aggregate_key] = {
                "id": event.aggregate_id,
                "type": event.aggregate_type,
                "version": 0,
                "state": {}
            }

        aggregate = self._aggregates[aggregate_key]

        # イベントを適用
        self._apply_event_to_state(aggregate["state"], event)
        aggregate["version"] = event.version

        return aggregate

    def _apply_event_to_state(self, state: Dict[str, Any], event: DomainEvent):
        """イベントを状態に適用"""
        if event.event_type == EventType.CREATED:
            state.update(event.event_data)
        elif event.event_type == EventType.UPDATED:
            state.update(event.event_data)
        elif event.event_type == EventType.DELETED:
            state["deleted"] = True
            state["deleted_at"] = event.timestamp.isoformat()
        elif event.event_type == EventType.STATE_CHANGED:
            if "state" in event.event_data:
                state["state"] = event.event_data["state"]

    def rebuild_aggregate(
        self,
        aggregate_type: str,
        aggregate_id: str
    ) -> Optional[Dict[str, Any]]:
        """イベント履歴から集約を再構築"""
        events = self.event_store.get_events(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id
        )

        if not events:
            return None

        # 最初のイベントから集約を作成
        aggregate = {
            "id": aggregate_id,
            "type": aggregate_type,
            "version": 0,
            "state": {}
        }

        # すべてのイベントを適用
        for event in events:
            self._apply_event_to_state(aggregate["state"], event)
            aggregate["version"] = event.version

        return aggregate

    def get_aggregate_state(
        self,
        aggregate_type: str,
        aggregate_id: str
    ) -> Optional[Dict[str, Any]]:
        """集約状態を取得"""
        aggregate_key = f"{aggregate_type}:{aggregate_id}"
        return self._aggregates.get(aggregate_key)
