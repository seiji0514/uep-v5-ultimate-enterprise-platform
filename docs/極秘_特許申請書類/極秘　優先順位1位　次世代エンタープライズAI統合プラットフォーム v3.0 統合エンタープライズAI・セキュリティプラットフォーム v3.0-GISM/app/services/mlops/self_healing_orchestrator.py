"""
自己修復型オーケストレーター
Self-Healing Orchestrator

Kubernetes統合、自動障害検知・修復
"""

import logging
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import json

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """ヘルスステータス"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class IncidentSeverity(Enum):
    """インシデント重大度"""
    CRITICAL = "critical"  # サービス停止
    HIGH = "high"  # 重大な性能劣化
    MEDIUM = "medium"  # 軽微な問題
    LOW = "low"  # 情報のみ


class HealingAction(Enum):
    """修復アクション"""
    RESTART_POD = "restart_pod"
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    ROLLBACK = "rollback"
    FAILOVER = "failover"
    CIRCUIT_BREAK = "circuit_break"
    RATE_LIMIT = "rate_limit"
    RETRAIN_MODEL = "retrain_model"
    RELOAD_CONFIG = "reload_config"


@dataclass
class HealthMetric:
    """ヘルスメトリクス"""
    timestamp: datetime
    cpu_usage: float  # パーセント
    memory_usage: float  # パーセント
    latency_p50: float  # ms
    latency_p95: float  # ms
    latency_p99: float  # ms
    error_rate: float  # パーセント
    qps: float  # Queries per second
    model_accuracy: Optional[float] = None  # モデル精度


@dataclass
class Incident:
    """インシデント"""
    incident_id: str
    timestamp: datetime
    severity: IncidentSeverity
    description: str
    affected_components: List[str]
    root_cause: Optional[str] = None
    healing_actions: List[HealingAction] = None
    resolved: bool = False
    resolution_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.healing_actions is None:
            self.healing_actions = []


@dataclass
class HealingPolicy:
    """修復ポリシー"""
    name: str
    condition: Callable[[HealthMetric], bool]  # 発動条件
    actions: List[HealingAction]  # 実行するアクション
    cooldown: timedelta = timedelta(minutes=5)  # クールダウン期間
    max_retries: int = 3  # 最大リトライ回数
    last_executed: Optional[datetime] = None


class SelfHealingOrchestrator:
    """
    自己修復型オーケストレーター
    
    機能:
    1. リアルタイムヘルスモニタリング
    2. 自動障害検知
    3. 根本原因分析
    4. 自動修復アクション実行
    5. カナリアデプロイメント
    6. 自動ロールバック
    """
    
    def __init__(
        self,
        cluster_name: str = "default",
        namespace: str = "mlops",
        enable_auto_healing: bool = True,
        enable_auto_scaling: bool = True,
        enable_auto_rollback: bool = True
    ):
        self.cluster_name = cluster_name
        self.namespace = namespace
        self.enable_auto_healing = enable_auto_healing
        self.enable_auto_scaling = enable_auto_scaling
        self.enable_auto_rollback = enable_auto_rollback
        
        # Kubernetesクライアントの初期化
        self._init_k8s_client()
        
        # ヘルスメトリクスの履歴
        self.health_history: List[HealthMetric] = []
        
        # インシデントの履歴
        self.incidents: List[Incident] = []
        
        # 修復ポリシー
        self.healing_policies: List[HealingPolicy] = []
        self._init_default_policies()
        
        # モニタリングタスク
        self.monitoring_task = None
        
    def _init_k8s_client(self):
        """Kubernetesクライアントの初期化"""
        try:
            from kubernetes import client, config
            
            # クラスタ内実行かローカルかを自動検出
            try:
                config.load_incluster_config()
                logger.info("Running inside Kubernetes cluster")
            except:
                config.load_kube_config()
                logger.info("Running outside Kubernetes cluster (using kubeconfig)")
                
            self.k8s_core = client.CoreV1Api()
            self.k8s_apps = client.AppsV1Api()
            self.k8s_autoscaling = client.AutoscalingV1Api()
            
            self.k8s_enabled = True
            logger.info("Kubernetes client initialized")
            
        except ImportError:
            logger.warning("Kubernetes client not installed, using simulation mode")
            self.k8s_enabled = False
            
    def _init_default_policies(self):
        """デフォルトの修復ポリシーを初期化"""
        
        # ポリシー1: 高CPU使用率
        self.healing_policies.append(
            HealingPolicy(
                name="high_cpu_usage",
                condition=lambda m: m.cpu_usage > 80,
                actions=[HealingAction.SCALE_UP],
                cooldown=timedelta(minutes=5)
            )
        )
        
        # ポリシー2: 高メモリ使用率
        self.healing_policies.append(
            HealingPolicy(
                name="high_memory_usage",
                condition=lambda m: m.memory_usage > 85,
                actions=[HealingAction.RESTART_POD, HealingAction.SCALE_UP],
                cooldown=timedelta(minutes=10)
            )
        )
        
        # ポリシー3: 高レイテンシ
        self.healing_policies.append(
            HealingPolicy(
                name="high_latency",
                condition=lambda m: m.latency_p95 > 1000,  # 1秒以上
                actions=[
                    HealingAction.SCALE_UP,
                    HealingAction.CIRCUIT_BREAK
                ],
                cooldown=timedelta(minutes=3)
            )
        )
        
        # ポリシー4: 高エラー率
        self.healing_policies.append(
            HealingPolicy(
                name="high_error_rate",
                condition=lambda m: m.error_rate > 5,  # 5%以上
                actions=[
                    HealingAction.ROLLBACK,
                    HealingAction.RESTART_POD
                ],
                cooldown=timedelta(minutes=15)
            )
        )
        
        # ポリシー5: モデル精度低下
        self.healing_policies.append(
            HealingPolicy(
                name="model_accuracy_degradation",
                condition=lambda m: (
                    m.model_accuracy is not None and
                    m.model_accuracy < 0.8
                ),
                actions=[HealingAction.RETRAIN_MODEL],
                cooldown=timedelta(hours=1)
            )
        )
        
        logger.info(f"Initialized {len(self.healing_policies)} healing policies")
        
    async def start_monitoring(self, interval: int = 30):
        """
        ヘルスモニタリングを開始
        
        Args:
            interval: モニタリング間隔（秒）
        """
        logger.info(f"Starting health monitoring (interval={interval}s)")
        
        while True:
            try:
                # メトリクスの収集
                metrics = await self.collect_metrics()
                self.health_history.append(metrics)
                
                # ヘルスステータスの評価
                status = self.evaluate_health(metrics)
                
                if status != HealthStatus.HEALTHY:
                    logger.warning(f"Health status: {status.value}")
                    
                    # 修復ポリシーのチェック
                    await self.check_and_execute_policies(metrics)
                    
                # 履歴のクリーンアップ（過去24時間のみ保持）
                cutoff_time = datetime.now() - timedelta(hours=24)
                self.health_history = [
                    m for m in self.health_history
                    if m.timestamp > cutoff_time
                ]
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                
            await asyncio.sleep(interval)
            
    async def collect_metrics(self) -> HealthMetric:
        """
        現在のメトリクスを収集
        
        Returns:
            HealthMetric
        """
        if self.k8s_enabled:
            return await self._collect_k8s_metrics()
        else:
            return await self._collect_simulated_metrics()
            
    async def _collect_k8s_metrics(self) -> HealthMetric:
        """Kubernetesからメトリクスを収集"""
        # Prometheusと連携してメトリクスを取得
        # ここでは簡略化
        
        # Podのリソース使用率を取得
        pods = self.k8s_core.list_namespaced_pod(self.namespace)
        
        cpu_total = 0.0
        memory_total = 0.0
        pod_count = len(pods.items)
        
        for pod in pods.items:
            # メトリクスサーバーからCPU/メモリ使用率を取得
            # 実際にはkubernetes.client.CustomObjectsApiを使用
            pass
            
        return HealthMetric(
            timestamp=datetime.now(),
            cpu_usage=cpu_total / pod_count if pod_count > 0 else 0.0,
            memory_usage=memory_total / pod_count if pod_count > 0 else 0.0,
            latency_p50=50.0,  # Prometheusから取得
            latency_p95=95.0,
            latency_p99=99.0,
            error_rate=0.5,
            qps=1000.0,
            model_accuracy=0.95
        )
        
    async def _collect_simulated_metrics(self) -> HealthMetric:
        """シミュレーションメトリクスを生成"""
        import random
        
        return HealthMetric(
            timestamp=datetime.now(),
            cpu_usage=random.uniform(20, 80),
            memory_usage=random.uniform(30, 70),
            latency_p50=random.uniform(10, 100),
            latency_p95=random.uniform(50, 200),
            latency_p99=random.uniform(100, 500),
            error_rate=random.uniform(0, 2),
            qps=random.uniform(500, 1500),
            model_accuracy=random.uniform(0.85, 0.98)
        )
        
    def evaluate_health(self, metrics: HealthMetric) -> HealthStatus:
        """
        ヘルスステータスを評価
        
        Args:
            metrics: ヘルスメトリクス
            
        Returns:
            HealthStatus
        """
        unhealthy_count = 0
        
        # CPU使用率チェック
        if metrics.cpu_usage > 90:
            unhealthy_count += 2
        elif metrics.cpu_usage > 80:
            unhealthy_count += 1
            
        # メモリ使用率チェック
        if metrics.memory_usage > 90:
            unhealthy_count += 2
        elif metrics.memory_usage > 85:
            unhealthy_count += 1
            
        # レイテンシチェック
        if metrics.latency_p95 > 1000:
            unhealthy_count += 2
        elif metrics.latency_p95 > 500:
            unhealthy_count += 1
            
        # エラー率チェック
        if metrics.error_rate > 10:
            unhealthy_count += 3
        elif metrics.error_rate > 5:
            unhealthy_count += 2
            
        # ステータスの判定
        if unhealthy_count >= 5:
            return HealthStatus.UNHEALTHY
        elif unhealthy_count >= 2:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY
            
    async def check_and_execute_policies(self, metrics: HealthMetric):
        """
        修復ポリシーをチェックし、必要に応じて実行
        
        Args:
            metrics: ヘルスメトリクス
        """
        if not self.enable_auto_healing:
            return
            
        for policy in self.healing_policies:
            # 条件チェック
            if not policy.condition(metrics):
                continue
                
            # クールダウンチェック
            if policy.last_executed:
                elapsed = datetime.now() - policy.last_executed
                if elapsed < policy.cooldown:
                    logger.debug(
                        f"Policy {policy.name} in cooldown "
                        f"({elapsed.total_seconds():.0f}s / "
                        f"{policy.cooldown.total_seconds():.0f}s)"
                    )
                    continue
                    
            # ポリシーの実行
            logger.info(f"Executing healing policy: {policy.name}")
            
            incident = Incident(
                incident_id=f"incident-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                timestamp=datetime.now(),
                severity=self._determine_severity(policy),
                description=f"Policy {policy.name} triggered",
                affected_components=[self.namespace],
                healing_actions=policy.actions.copy()
            )
            
            self.incidents.append(incident)
            
            # アクションの実行
            for action in policy.actions:
                try:
                    await self.execute_healing_action(action, incident)
                except Exception as e:
                    logger.error(f"Failed to execute {action.value}: {e}")
                    
            policy.last_executed = datetime.now()
            
    def _determine_severity(self, policy: HealingPolicy) -> IncidentSeverity:
        """ポリシーから重大度を判定"""
        if HealingAction.ROLLBACK in policy.actions:
            return IncidentSeverity.CRITICAL
        elif HealingAction.FAILOVER in policy.actions:
            return IncidentSeverity.HIGH
        elif HealingAction.SCALE_UP in policy.actions:
            return IncidentSeverity.MEDIUM
        else:
            return IncidentSeverity.LOW
            
    async def execute_healing_action(
        self,
        action: HealingAction,
        incident: Incident
    ):
        """
        修復アクションを実行
        
        Args:
            action: 修復アクション
            incident: インシデント情報
        """
        logger.info(f"Executing healing action: {action.value}")
        
        if action == HealingAction.RESTART_POD:
            await self._restart_pods()
        elif action == HealingAction.SCALE_UP:
            await self._scale_deployment(scale_up=True)
        elif action == HealingAction.SCALE_DOWN:
            await self._scale_deployment(scale_up=False)
        elif action == HealingAction.ROLLBACK:
            await self._rollback_deployment()
        elif action == HealingAction.FAILOVER:
            await self._failover_to_backup()
        elif action == HealingAction.CIRCUIT_BREAK:
            await self._enable_circuit_breaker()
        elif action == HealingAction.RATE_LIMIT:
            await self._enable_rate_limiting()
        elif action == HealingAction.RETRAIN_MODEL:
            await self._trigger_model_retraining()
        elif action == HealingAction.RELOAD_CONFIG:
            await self._reload_configuration()
            
    async def _restart_pods(self):
        """Podを再起動"""
        if not self.k8s_enabled:
            logger.info("[SIMULATION] Restarting pods")
            return
            
        try:
            # Deploymentのローリングリスタート
            deployments = self.k8s_apps.list_namespaced_deployment(self.namespace)
            
            for deployment in deployments.items:
                # アノテーションを更新してローリングリスタートをトリガー
                body = {
                    "spec": {
                        "template": {
                            "metadata": {
                                "annotations": {
                                    "kubectl.kubernetes.io/restartedAt": 
                                        datetime.now().isoformat()
                                }
                            }
                        }
                    }
                }
                
                self.k8s_apps.patch_namespaced_deployment(
                    deployment.metadata.name,
                    self.namespace,
                    body
                )
                
            logger.info("Pods restarted successfully")
            
        except Exception as e:
            logger.error(f"Failed to restart pods: {e}")
            
    async def _scale_deployment(self, scale_up: bool = True):
        """Deploymentをスケール"""
        if not self.k8s_enabled:
            direction = "up" if scale_up else "down"
            logger.info(f"[SIMULATION] Scaling {direction}")
            return
            
        try:
            deployments = self.k8s_apps.list_namespaced_deployment(self.namespace)
            
            for deployment in deployments.items:
                current_replicas = deployment.spec.replicas
                
                if scale_up:
                    new_replicas = min(current_replicas + 2, 20)  # 最大20
                else:
                    new_replicas = max(current_replicas - 1, 1)  # 最小1
                    
                if new_replicas != current_replicas:
                    body = {"spec": {"replicas": new_replicas}}
                    
                    self.k8s_apps.patch_namespaced_deployment(
                        deployment.metadata.name,
                        self.namespace,
                        body
                    )
                    
                    logger.info(
                        f"Scaled {deployment.metadata.name}: "
                        f"{current_replicas} -> {new_replicas}"
                    )
                    
        except Exception as e:
            logger.error(f"Failed to scale deployment: {e}")
            
    async def _rollback_deployment(self):
        """Deploymentをロールバック"""
        if not self.k8s_enabled:
            logger.info("[SIMULATION] Rolling back deployment")
            return
            
        try:
            deployments = self.k8s_apps.list_namespaced_deployment(self.namespace)
            
            for deployment in deployments.items:
                # 前のリビジョンにロールバック
                body = {
                    "spec": {
                        "rollbackTo": {
                            "revision": 0  # 0は直前のリビジョン
                        }
                    }
                }
                
                self.k8s_apps.patch_namespaced_deployment(
                    deployment.metadata.name,
                    self.namespace,
                    body
                )
                
            logger.info("Deployment rolled back successfully")
            
        except Exception as e:
            logger.error(f"Failed to rollback deployment: {e}")
            
    async def _failover_to_backup(self):
        """バックアップシステムにフェイルオーバー"""
        logger.info("[ACTION] Failing over to backup system")
        # 実装省略
        
    async def _enable_circuit_breaker(self):
        """サーキットブレーカーを有効化"""
        logger.info("[ACTION] Enabling circuit breaker")
        # Istioのサーキットブレーカー設定を更新
        
    async def _enable_rate_limiting(self):
        """レート制限を有効化"""
        logger.info("[ACTION] Enabling rate limiting")
        # API Gatewayのレート制限を設定
        
    async def _trigger_model_retraining(self):
        """モデルの再学習をトリガー"""
        logger.info("[ACTION] Triggering model retraining")
        # MLflowやKubeflowでモデル再学習ジョブを起動
        
    async def _reload_configuration(self):
        """設定をリロード"""
        logger.info("[ACTION] Reloading configuration")
        # ConfigMapを更新してPodに通知
        
    def get_incident_summary(self) -> Dict[str, Any]:
        """インシデントサマリーを取得"""
        total_incidents = len(self.incidents)
        resolved_incidents = len([i for i in self.incidents if i.resolved])
        
        severity_counts = {
            "critical": len([i for i in self.incidents 
                           if i.severity == IncidentSeverity.CRITICAL]),
            "high": len([i for i in self.incidents 
                        if i.severity == IncidentSeverity.HIGH]),
            "medium": len([i for i in self.incidents 
                          if i.severity == IncidentSeverity.MEDIUM]),
            "low": len([i for i in self.incidents 
                       if i.severity == IncidentSeverity.LOW])
        }
        
        # 平均解決時間
        resolved_with_time = [
            i for i in self.incidents
            if i.resolved and i.resolution_time
        ]
        
        if resolved_with_time:
            avg_resolution_time = sum(
                (i.resolution_time - i.timestamp).total_seconds()
                for i in resolved_with_time
            ) / len(resolved_with_time)
        else:
            avg_resolution_time = 0
            
        return {
            "total_incidents": total_incidents,
            "resolved_incidents": resolved_incidents,
            "unresolved_incidents": total_incidents - resolved_incidents,
            "resolution_rate": (
                resolved_incidents / total_incidents * 100
                if total_incidents > 0 else 0
            ),
            "severity_counts": severity_counts,
            "avg_resolution_time_seconds": avg_resolution_time,
            "recent_incidents": [
                {
                    "incident_id": i.incident_id,
                    "timestamp": i.timestamp.isoformat(),
                    "severity": i.severity.value,
                    "description": i.description,
                    "resolved": i.resolved
                }
                for i in self.incidents[-10:]  # 最新10件
            ]
        }


# エクスポート
__all__ = [
    'SelfHealingOrchestrator',
    'HealthStatus',
    'IncidentSeverity',
    'HealingAction',
    'HealthMetric',
    'Incident',
    'HealingPolicy'
]

