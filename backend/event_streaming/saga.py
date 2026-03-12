"""
Sagaパターン・アウトボックスパターンのサンプル実装
補強スキル: イベント駆動（Saga、アウトボックスパターン）
"""
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SagaStatus(str, Enum):
    """Sagaステータス"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"


class SagaStep(BaseModel):
    """Sagaステップ"""

    step_id: str
    action: str
    compensate_action: str
    payload: Dict[str, Any]
    status: SagaStatus = SagaStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class Saga(BaseModel):
    """Sagaオーケストレーター（補正処理対応）"""

    saga_id: str
    saga_type: str
    steps: List[SagaStep]
    status: SagaStatus = SagaStatus.PENDING
    created_at: datetime = None
    updated_at: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def execute_step(
        self, step_index: int, executor: Callable[[str, Dict], Any]
    ) -> bool:
        """ステップを実行。失敗時は補正を開始"""
        if step_index >= len(self.steps):
            self.status = SagaStatus.COMPLETED
            return True
        step = self.steps[step_index]
        step.status = SagaStatus.IN_PROGRESS
        try:
            step.result = executor(step.action, step.payload)
            step.status = SagaStatus.COMPLETED
            return self.execute_step(step_index + 1, executor)
        except Exception as e:
            step.error = str(e)
            step.status = SagaStatus.FAILED
            self.status = SagaStatus.COMPENSATING
            self.compensate(step_index, executor)
            return False

    def compensate(self, from_index: int, executor: Callable[[str, Dict], Any]) -> None:
        """補正処理（逆順で compensate_action を実行）"""
        for i in range(from_index, -1, -1):
            step = self.steps[i]
            if step.status == SagaStatus.COMPLETED:
                try:
                    executor(step.compensate_action, step.payload or step.result or {})
                    step.status = SagaStatus.PENDING
                except Exception as e:
                    logger.error(f"Saga {self.saga_id} compensate failed step {i}: {e}")
        self.status = SagaStatus.FAILED


class OutboxEvent(BaseModel):
    """アウトボックスパターン: トランザクションとイベントを同時に永続化"""

    event_id: str
    aggregate_type: str
    aggregate_id: str
    event_type: str
    payload: Dict[str, Any]
    created_at: datetime
    published: bool = False
    published_at: Optional[datetime] = None


class OutboxStore:
    """アウトボックスストア（DBと連携する想定、ここではメモリ）"""

    _events: List[OutboxEvent] = []

    @classmethod
    def save(cls, event: OutboxEvent) -> None:
        """イベントを保存（トランザクション内でDBに保存する想定）"""
        cls._events.append(event)
        logger.info(f"Outbox saved: {event.event_id} {event.event_type}")

    @classmethod
    def get_unpublished(cls) -> List[OutboxEvent]:
        """未公開イベントを取得"""
        return [e for e in cls._events if not e.published]

    @classmethod
    def mark_published(cls, event_id: str) -> None:
        """公開済みにマーク"""
        for e in cls._events:
            if e.event_id == event_id:
                e.published = True
                e.published_at = datetime.utcnow()
                break


def create_outbox_event(
    aggregate_type: str,
    aggregate_id: str,
    event_type: str,
    payload: Dict[str, Any],
) -> OutboxEvent:
    """アウトボックスイベントを作成"""
    event = OutboxEvent(
        event_id=str(uuid.uuid4()),
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        event_type=event_type,
        payload=payload,
        created_at=datetime.utcnow(),
    )
    OutboxStore.save(event)
    return event
