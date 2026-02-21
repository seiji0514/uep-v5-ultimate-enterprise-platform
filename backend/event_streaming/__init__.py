"""
UEP v5.0 - イベントストリーミングモジュール
"""
from .cqrs import CommandHandler, QueryHandler
from .event_sourcing import EventSourcingHandler, EventStore
from .kafka_client import KafkaClient

__all__ = [
    "KafkaClient",
    "EventStore",
    "EventSourcingHandler",
    "CommandHandler",
    "QueryHandler",
]
