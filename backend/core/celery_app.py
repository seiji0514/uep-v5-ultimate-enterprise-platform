"""
Celery設定モジュール
非同期タスク処理
"""
from celery import Celery
from core.config import settings

# Celeryアプリケーションの作成
celery_app = Celery(
    "uep_v5",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "core.tasks",
        "mlops.tasks",
        "generative_ai.tasks",
        "security_center.tasks"
    ]
)

# Celery設定
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分
    task_soft_time_limit=25 * 60,  # 25分
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    result_expires=3600,  # 1時間
    task_routes={
        "core.tasks.*": {"queue": "default"},
        "mlops.tasks.*": {"queue": "mlops"},
        "generative_ai.tasks.*": {"queue": "ai"},
        "security_center.tasks.*": {"queue": "security"},
    },
    task_default_queue="default",
    task_default_exchange="tasks",
    task_default_exchange_type="direct",
    task_default_routing_key="default",
)
