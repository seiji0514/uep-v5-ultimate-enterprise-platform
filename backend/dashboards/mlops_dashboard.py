"""
統合MLOpsダッシュボードモジュール
"""
from typing import Dict, Any
from mlops.pipeline import pipeline_executor
from mlops.model_registry import model_registry
from mlops.experiment_tracking import experiment_tracker


class MLOpsDashboard:
    """統合MLOpsダッシュボードクラス"""

    def get_dashboard_data(self) -> Dict[str, Any]:
        """MLOpsダッシュボードデータを取得"""
        pipelines = pipeline_executor.list_pipelines()
        models = model_registry.list_models()
        experiments = experiment_tracker.list_experiments()

        # プロダクションモデル
        production_models = [
            m for m in models
            if m.current_version and any(
                v.version == m.current_version and v.status.value == "production"
                for v in m.versions
            )
        ]

        # 実行中のパイプライン
        running_pipelines = [p for p in pipelines if p.status.value == "running"]

        # 最近の実験
        recent_experiments = sorted(experiments, key=lambda e: e.created_at, reverse=True)[:5]

        return {
            "overview": {
                "total_models": len(models),
                "production_models": len(production_models),
                "total_pipelines": len(pipelines),
                "running_pipelines": len(running_pipelines),
                "total_experiments": len(experiments)
            },
            "models": [
                {
                    "id": m.id,
                    "name": m.name,
                    "type": m.model_type,
                    "current_version": m.current_version,
                    "status": m.current_version and next(
                        (v.status.value for v in m.versions if v.version == m.current_version),
                        "development"
                    )
                }
                for m in models[:10]
            ],
            "pipelines": [
                {
                    "id": p.id,
                    "name": p.name,
                    "status": p.status.value,
                    "stages": len(p.stages)
                }
                for p in pipelines[:10]
            ],
            "recent_experiments": [
                {
                    "id": e.id,
                    "name": e.name,
                    "metrics": e.metrics,
                    "status": e.status
                }
                for e in recent_experiments
            ]
        }


# グローバルインスタンス
mlops_dashboard = MLOpsDashboard()
