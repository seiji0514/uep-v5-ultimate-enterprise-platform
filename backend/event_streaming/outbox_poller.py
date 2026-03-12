"""
アウトボックスパターン: 未公開イベントを Kafka へポーリング発行
補強スキル: イベント駆動（アウトボックスパターン）
"""
import asyncio
import logging
from typing import Optional

from .kafka_client import KafkaClient
from .saga import OutboxStore

logger = logging.getLogger(__name__)


async def poll_and_publish_outbox(
    kafka_client: KafkaClient,
    topic: str = "uep-outbox-events",
    interval_sec: float = 5.0,
) -> None:
    """未公開アウトボックスイベントを Kafka へ発行（バックグラウンドポーリング）"""
    while True:
        try:
            events = OutboxStore.get_unpublished()
            for event in events:
                try:
                    success = kafka_client.publish_event(
                        topic=topic,
                        event_type=event.event_type,
                        data={
                            "event_id": event.event_id,
                            "aggregate_type": event.aggregate_type,
                            "aggregate_id": event.aggregate_id,
                            "payload": event.payload,
                            "created_at": event.created_at.isoformat(),
                        },
                        key=event.aggregate_id,
                    )
                    if success:
                        OutboxStore.mark_published(event.event_id)
                        logger.info(f"Outbox published: {event.event_id}")
                except Exception as e:
                    logger.warning(f"Outbox publish failed {event.event_id}: {e}")
        except Exception as e:
            logger.error(f"Outbox poll error: {e}")
        await asyncio.sleep(interval_sec)
