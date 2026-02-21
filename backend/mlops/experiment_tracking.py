"""
実験追跡モジュール
ML実験の追跡と管理
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Experiment(BaseModel):
    """実験"""

    id: str
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = {}
    metrics: Dict[str, float] = {}
    tags: List[str] = []
    status: str = "running"  # running, completed, failed
    created_at: datetime
    updated_at: datetime
    created_by: str
    artifacts: List[str] = []


class ExperimentTracker:
    """実験追跡クラス"""

    def __init__(self):
        """実験追跡器を初期化"""
        self._experiments: Dict[str, Experiment] = {}

    def create_experiment(
        self,
        name: str,
        created_by: str,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Experiment:
        """実験を作成"""
        experiment_id = str(uuid.uuid4())

        experiment = Experiment(
            id=experiment_id,
            name=name,
            description=description,
            parameters=parameters or {},
            tags=tags or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by=created_by,
        )

        self._experiments[experiment_id] = experiment
        return experiment

    def log_parameters(self, experiment_id: str, parameters: Dict[str, Any]):
        """パラメータを記録"""
        experiment = self._experiments.get(experiment_id)
        if experiment:
            experiment.parameters.update(parameters)
            experiment.updated_at = datetime.utcnow()

    def log_metrics(self, experiment_id: str, metrics: Dict[str, float]):
        """メトリクスを記録"""
        experiment = self._experiments.get(experiment_id)
        if experiment:
            experiment.metrics.update(metrics)
            experiment.updated_at = datetime.utcnow()

    def log_artifact(self, experiment_id: str, artifact_path: str):
        """アーティファクトを記録"""
        experiment = self._experiments.get(experiment_id)
        if experiment:
            if artifact_path not in experiment.artifacts:
                experiment.artifacts.append(artifact_path)
            experiment.updated_at = datetime.utcnow()

    def complete_experiment(self, experiment_id: str):
        """実験を完了"""
        experiment = self._experiments.get(experiment_id)
        if experiment:
            experiment.status = "completed"
            experiment.updated_at = datetime.utcnow()

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """実験を取得"""
        return self._experiments.get(experiment_id)

    def list_experiments(
        self, tags: Optional[List[str]] = None, status: Optional[str] = None
    ) -> List[Experiment]:
        """実験一覧を取得"""
        experiments = list(self._experiments.values())

        if tags:
            experiments = [e for e in experiments if any(tag in e.tags for tag in tags)]

        if status:
            experiments = [e for e in experiments if e.status == status]

        return experiments

    def compare_experiments(self, experiment_ids: List[str]) -> Dict[str, Any]:
        """実験を比較"""
        experiments = [
            self._experiments.get(eid)
            for eid in experiment_ids
            if self._experiments.get(eid)
        ]

        return {
            "experiments": [
                {
                    "id": e.id,
                    "name": e.name,
                    "parameters": e.parameters,
                    "metrics": e.metrics,
                }
                for e in experiments
            ],
            "best_metric": self._find_best_metric(experiments),
        }

    def _find_best_metric(
        self, experiments: List[Experiment]
    ) -> Optional[Dict[str, Any]]:
        """最良のメトリクスを検索"""
        if not experiments:
            return None

        # 簡易実装：accuracyが最も高い実験を選択
        best = None
        best_accuracy = -1

        for exp in experiments:
            accuracy = exp.metrics.get("accuracy", 0)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best = exp

        if best:
            return {
                "experiment_id": best.id,
                "experiment_name": best.name,
                "metrics": best.metrics,
            }

        return None


# グローバルインスタンス
experiment_tracker = ExperimentTracker()
