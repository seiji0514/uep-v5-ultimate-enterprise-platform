"""
UEP v5.0 - イベントストリーミングモジュール
"""
from .kafka_client import KafkaClient
from .event_sourcing import EventStore, EventSourcingHandler
from .cqrs import CommandHandler, QueryHandler

__all__ = [
    "KafkaClient",
    "EventStore",
    "EventSourcingHandler",
    "CommandHandler",
    "QueryHandler",
]
