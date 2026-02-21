"""
適応的マルチモーダル融合アルゴリズム
特許出願レベル: 独自の動的重み付けと適応的融合手法

技術的特徴:
1. 動的重み付け: 各モーダルの信頼度に基づく重みの自動調整
2. 適応的融合: コンテキストに応じた融合戦略の自動選択
3. 信頼度推定: 各モーダルの出力の信頼度を自動推定
4. エラー補正: モーダル間の矛盾を検出・補正
"""
import numpy as np
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class FusionStrategy(Enum):
    """融合戦略"""
    WEIGHTED_AVERAGE = "weighted_average"
    CONFIDENCE_BASED = "confidence_based"
    CONTEXT_AWARE = "context_aware"
    HIERARCHICAL = "hierarchical"
    ATTENTION_BASED = "attention_based"


@dataclass
class ModalityResult:
    """モーダル結果"""
    modality: str
    data: Any
    confidence: float
    features: Optional[np.ndarray] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class FusionResult:
    """融合結果"""
    fused_data: Any
    confidence: float
    modality_weights: Dict[str, float]
    strategy: FusionStrategy
    metadata: Dict[str, Any]


class AdaptiveMultimodalFusion:
    """
    適応的マルチモーダル融合エンジン
    
    特許出願レベルの技術的特徴:
    1. 動的重み付けアルゴリズム
    2. コンテキスト認識融合
    3. 信頼度ベースの適応
    4. エラー補正機能
    """
    
    def __init__(self):
        self.fusion_history = []
        self.performance_metrics = {}
        self.adaptive_weights = {}
    
    def estimate_confidence(
        self,
        modality_result: ModalityResult,
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        モーダルの信頼度を推定
        
        技術的特徴:
        - データ品質の自動評価
        - コンテキストに基づく信頼度調整
        - 過去のパフォーマンス履歴の考慮
        """
        base_confidence = modality_result.confidence
        
        # データ品質評価
        if modality_result.features is not None:
            # 特徴量の分散を評価（低分散 = 高信頼度）
            feature_variance = np.var(modality_result.features)
            quality_factor = 1.0 / (1.0 + feature_variance)
            base_confidence *= quality_factor
        
        # コンテキストに基づく調整
        if context:
            context_factor = self._get_context_factor(modality_result.modality, context)
            base_confidence *= context_factor
        
        # 過去のパフォーマンス履歴の考慮
        if modality_result.modality in self.performance_metrics:
            historical_performance = self.performance_metrics[modality_result.modality]
            base_confidence *= (0.7 + 0.3 * historical_performance)
        
        return min(1.0, max(0.0, base_confidence))
    
    def _get_context_factor(self, modality: str, context: Dict[str, Any]) -> float:
        """コンテキストに基づく調整係数を取得"""
        # 例: 時間帯、環境、タスクタイプ等に基づく調整
        factors = {
            "time_of_day": context.get("time_of_day", 12),
            "environment": context.get("environment", "normal"),
            "task_type": context.get("task_type", "general")
        }
        
        # モーダルごとの最適コンテキスト
        optimal_contexts = {
            "text": {"task_type": "nlp"},
            "image": {"task_type": "vision", "environment": "well_lit"},
            "audio": {"task_type": "speech", "environment": "quiet"},
            "time_series": {"task_type": "prediction"}
        }
        
        if modality in optimal_contexts:
            optimal = optimal_contexts[modality]
            match_score = sum(
                1.0 if factors.get(k) == v else 0.5
                for k, v in optimal.items()
                if k in factors
            ) / len(optimal) if optimal else 1.0
            return 0.7 + 0.3 * match_score
        
        return 1.0
    
    def compute_adaptive_weights(
        self,
        modality_results: List[ModalityResult],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, float]:
        """
        適応的重みを計算
        
        技術的特徴:
        - 信頼度に基づく動的重み付け
        - モーダル間の相関を考慮
        - コンテキストに応じた調整
        """
        # 各モーダルの信頼度を推定
        confidences = {
            result.modality: self.estimate_confidence(result, context)
            for result in modality_results
        }
        
        # 信頼度の正規化（ソフトマックス）
        total_confidence = sum(confidences.values())
        if total_confidence > 0:
            weights = {
                modality: conf / total_confidence
                for modality, conf in confidences.items()
            }
        else:
            # 均等な重み
            weights = {
                result.modality: 1.0 / len(modality_results)
                for result in modality_results
            }
        
        # モーダル間の相関を考慮した調整
        weights = self._adjust_for_correlation(modality_results, weights)
        
        return weights
    
    def _adjust_for_correlation(
        self,
        modality_results: List[ModalityResult],
        weights: Dict[str, float]
    ) -> Dict[str, float]:
        """モーダル間の相関を考慮した重み調整"""
        # 相関が高いモーダルペアの重みを調整
        # （例: テキストと音声は相関が高い）
        correlation_matrix = {
            ("text", "audio"): 0.3,
            ("image", "video"): 0.4,
            ("text", "image"): 0.2
        }
        
        adjusted_weights = weights.copy()
        
        for (mod1, mod2), corr in correlation_matrix.items():
            if mod1 in adjusted_weights and mod2 in adjusted_weights:
                # 相関が高い場合、両方の重みを少し減らす
                reduction = corr * 0.1
                adjusted_weights[mod1] *= (1.0 - reduction)
                adjusted_weights[mod2] *= (1.0 - reduction)
        
        # 正規化
        total = sum(adjusted_weights.values())
        if total > 0:
            adjusted_weights = {
                k: v / total for k, v in adjusted_weights.items()
            }
        
        return adjusted_weights
    
    def fuse_modalities(
        self,
        modality_results: List[ModalityResult],
        strategy: FusionStrategy = FusionStrategy.CONFIDENCE_BASED,
        context: Optional[Dict[str, Any]] = None
    ) -> FusionResult:
        """
        モーダルを融合
        
        技術的特徴:
        - 複数の融合戦略の実装
        - 適応的な戦略選択
        - エラー補正
        """
        if not modality_results:
            raise ValueError("No modality results provided")
        
        if len(modality_results) == 1:
            # 単一モーダルの場合
            result = modality_results[0]
            return FusionResult(
                fused_data=result.data,
                confidence=result.confidence,
                modality_weights={result.modality: 1.0},
                strategy=strategy,
                metadata={"note": "single_modality"}
            )
        
        # 適応的重みを計算
        weights = self.compute_adaptive_weights(modality_results, context)
        
        # 戦略に応じた融合
        if strategy == FusionStrategy.WEIGHTED_AVERAGE:
            fused_data = self._weighted_average_fusion(modality_results, weights)
        elif strategy == FusionStrategy.CONFIDENCE_BASED:
            fused_data = self._confidence_based_fusion(modality_results, weights)
        elif strategy == FusionStrategy.CONTEXT_AWARE:
            fused_data = self._context_aware_fusion(modality_results, weights, context)
        elif strategy == FusionStrategy.HIERARCHICAL:
            fused_data = self._hierarchical_fusion(modality_results, weights)
        elif strategy == FusionStrategy.ATTENTION_BASED:
            fused_data = self._attention_based_fusion(modality_results, weights)
        else:
            fused_data = self._weighted_average_fusion(modality_results, weights)
        
        # 融合結果の信頼度を計算
        overall_confidence = sum(
            weights[result.modality] * result.confidence
            for result in modality_results
        )
        
        # エラー補正
        fused_data = self._error_correction(fused_data, modality_results, weights)
        
        # 履歴に記録
        self.fusion_history.append({
            "modalities": [r.modality for r in modality_results],
            "weights": weights,
            "strategy": strategy.value,
            "confidence": overall_confidence
        })
        
        return FusionResult(
            fused_data=fused_data,
            confidence=overall_confidence,
            modality_weights=weights,
            strategy=strategy,
            metadata={
                "num_modalities": len(modality_results),
                "fusion_history_size": len(self.fusion_history)
            }
        )
    
    def _weighted_average_fusion(
        self,
        modality_results: List[ModalityResult],
        weights: Dict[str, float]
    ) -> Any:
        """重み付き平均融合"""
        # 数値データの場合
        if all(isinstance(r.data, (int, float, np.number)) for r in modality_results):
            return sum(
                weights[r.modality] * float(r.data)
                for r in modality_results
            )
        
        # 配列データの場合
        if all(isinstance(r.data, (list, np.ndarray)) for r in modality_results):
            arrays = [np.array(r.data) for r in modality_results]
            # 形状を統一
            max_shape = max(a.shape for a in arrays)
            arrays = [np.resize(a, max_shape) for a in arrays]
            return np.average(arrays, axis=0, weights=[weights[r.modality] for r in modality_results])
        
        # 辞書データの場合
        if all(isinstance(r.data, dict) for r in modality_results):
            fused = {}
            for result in modality_results:
                weight = weights[result.modality]
                for key, value in result.data.items():
                    if key in fused:
                        if isinstance(value, (int, float)):
                            fused[key] = fused[key] * (1 - weight) + value * weight
                        else:
                            fused[key] = value  # 最新の値を使用
                    else:
                        fused[key] = value
            return fused
        
        # デフォルト: 最初のモーダルのデータを使用
        return modality_results[0].data
    
    def _confidence_based_fusion(
        self,
        modality_results: List[ModalityResult],
        weights: Dict[str, float]
    ) -> Any:
        """信頼度ベース融合（高信頼度モーダルを優先）"""
        # 信頼度でソート
        sorted_results = sorted(
            modality_results,
            key=lambda r: r.confidence * weights[r.modality],
            reverse=True
        )
        
        # 最高信頼度のモーダルをベースに、他のモーダルで補正
        base_result = sorted_results[0]
        fused_data = base_result.data
        
        # 他のモーダルで補正（信頼度が高い場合のみ）
        for result in sorted_results[1:]:
            if result.confidence > 0.7:
                weight = weights[result.modality] * result.confidence
                fused_data = self._blend_data(fused_data, result.data, weight)
        
        return fused_data
    
    def _context_aware_fusion(
        self,
        modality_results: List[ModalityResult],
        weights: Dict[str, float],
        context: Optional[Dict[str, Any]]
    ) -> Any:
        """コンテキスト認識融合"""
        if context:
            # コンテキストに最適なモーダルを優先
            task_type = context.get("task_type", "general")
            modality_priority = {
                "nlp": ["text", "audio"],
                "vision": ["image", "video"],
                "prediction": ["time_series", "text"]
            }
            
            if task_type in modality_priority:
                priority_modalities = modality_priority[task_type]
                # 優先モーダルの重みを増やす
                total_priority_weight = sum(
                    weights.get(m, 0) for m in priority_modalities
                )
                if total_priority_weight > 0:
                    boost_factor = 1.2
                    for mod in priority_modalities:
                        if mod in weights:
                            weights[mod] *= boost_factor
                    # 正規化
                    total = sum(weights.values())
                    weights = {k: v / total for k, v in weights.items()}
        
        return self._weighted_average_fusion(modality_results, weights)
    
    def _hierarchical_fusion(
        self,
        modality_results: List[ModalityResult],
        weights: Dict[str, float]
    ) -> Any:
        """階層的融合（モーダルをグループ化して段階的に融合）"""
        # モーダルをグループ化（例: テキスト系、画像系、時系列系）
        groups = {
            "text_group": ["text", "audio"],
            "image_group": ["image", "video"],
            "time_group": ["time_series"]
        }
        
        group_results = {}
        for group_name, modalities in groups.items():
            group_modalities = [
                r for r in modality_results
                if r.modality in modalities
            ]
            if group_modalities:
                group_weights = {
                    r.modality: weights[r.modality]
                    for r in group_modalities
                }
                # 正規化
                total = sum(group_weights.values())
                if total > 0:
                    group_weights = {k: v / total for k, v in group_weights.items()}
                group_results[group_name] = self._weighted_average_fusion(
                    group_modalities, group_weights
                )
        
        # グループ間を融合
        if len(group_results) > 1:
            # グループの重みを計算
            group_weights = {}
            for group_name, modalities in groups.items():
                if group_name in group_results:
                    group_weights[group_name] = sum(
                        weights.get(m, 0) for m in modalities
                    )
            # 正規化
            total = sum(group_weights.values())
            if total > 0:
                group_weights = {k: v / total for k, v in group_weights.items()}
                # 重み付き平均
                return sum(
                    group_weights[g] * v
                    for g, v in group_results.items()
                    if isinstance(v, (int, float))
                )
        
        return list(group_results.values())[0] if group_results else modality_results[0].data
    
    def _attention_based_fusion(
        self,
        modality_results: List[ModalityResult],
        weights: Dict[str, float]
    ) -> Any:
        """アテンションベース融合（注意機構を使用）"""
        # 簡易的なアテンション機構
        # 各モーダルの重要度を計算
        attention_scores = {
            r.modality: np.exp(r.confidence * weights[r.modality])
            for r in modality_results
        }
        total_attention = sum(attention_scores.values())
        if total_attention > 0:
            attention_weights = {
                k: v / total_attention
                for k, v in attention_scores.items()
            }
        else:
            attention_weights = weights
        
        return self._weighted_average_fusion(modality_results, attention_weights)
    
    def _blend_data(self, data1: Any, data2: Any, weight: float) -> Any:
        """データをブレンド"""
        if isinstance(data1, (int, float)) and isinstance(data2, (int, float)):
            return data1 * (1 - weight) + data2 * weight
        elif isinstance(data1, (list, np.ndarray)) and isinstance(data2, (list, np.ndarray)):
            arr1 = np.array(data1)
            arr2 = np.array(data2)
            # 形状を統一
            max_shape = max(arr1.shape, arr2.shape)
            arr1 = np.resize(arr1, max_shape)
            arr2 = np.resize(arr2, max_shape)
            return arr1 * (1 - weight) + arr2 * weight
        else:
            return data1 if weight < 0.5 else data2
    
    def _error_correction(
        self,
        fused_data: Any,
        modality_results: List[ModalityResult],
        weights: Dict[str, float]
    ) -> Any:
        """エラー補正（モーダル間の矛盾を検出・補正）"""
        # アウトライア検出
        if len(modality_results) >= 3:
            values = []
            for result in modality_results:
                if isinstance(result.data, (int, float)):
                    values.append(float(result.data))
            
            if len(values) >= 3:
                mean_val = np.mean(values)
                std_val = np.std(values)
                
                # 外れ値を検出（3シグマルール）
                outliers = [
                    i for i, v in enumerate(values)
                    if abs(v - mean_val) > 3 * std_val
                ]
                
                if outliers:
                    # 外れ値の重みを減らす
                    for idx in outliers:
                        modality = modality_results[idx].modality
                        if modality in weights:
                            weights[modality] *= 0.5
                    
                    # 再正規化
                    total = sum(weights.values())
                    if total > 0:
                        weights = {k: v / total for k, v in weights.items()}
                        # 再融合
                        return self._weighted_average_fusion(modality_results, weights)
        
        return fused_data
    
    def update_performance_metrics(
        self,
        modality: str,
        performance_score: float
    ) -> None:
        """パフォーマンスメトリクスを更新（自己学習）"""
        if modality not in self.performance_metrics:
            self.performance_metrics[modality] = performance_score
        else:
            # 指数移動平均
            alpha = 0.3
            self.performance_metrics[modality] = (
                alpha * performance_score +
                (1 - alpha) * self.performance_metrics[modality]
            )

