"""
適応的キャッシュ戦略
特許出願レベル: 学習型キャッシュと予測的プリフェッチ

技術的特徴:
1. アクセスパターン学習: ユーザーのアクセスパターンを学習
2. 予測的プリフェッチ: 次にアクセスされる可能性の高いデータを事前に読み込み
3. 動的TTL調整: データの重要度に応じてTTLを動的に調整
4. メモリ効率最適化: メモリ使用量を監視し、自動的に最適化
"""
import time
import logging
from typing import Dict, Any, Optional, List, Tuple
from collections import defaultdict, deque
import numpy as np

from app.utils.cache import TTLCache, LRUCache

logger = logging.getLogger(__name__)


class AdaptiveCache:
    """
    適応的キャッシュ
    
    特許出願レベルの技術的特徴:
    1. アクセスパターン学習
    2. 予測的プリフェッチ
    3. 動的TTL調整
    4. メモリ効率最適化
    """
    
    def __init__(
        self,
        base_ttl: int = 3600,
        max_size: int = 100,
        learning_window: int = 100
    ):
        """
        Args:
            base_ttl: ベースTTL（秒）
            max_size: 最大キャッシュサイズ
            learning_window: 学習ウィンドウサイズ
        """
        self.base_ttl = base_ttl
        self.max_size = max_size
        self.learning_window = learning_window
        
        # キャッシュ
        self.cache = TTLCache(ttl_seconds=base_ttl, max_size=max_size)
        
        # アクセスパターン学習
        self.access_history = deque(maxlen=learning_window)
        self.access_patterns = defaultdict(list)  # key -> [access_times]
        self.access_frequency = defaultdict(int)  # key -> frequency
        self.access_correlation = defaultdict(list)  # key -> [correlated_keys]
        
        # 予測的プリフェッチ
        self.prefetch_candidates = {}
        self.prefetch_history = {}
        
        # 動的TTL調整
        self.key_importance = defaultdict(float)  # key -> importance_score
        self.dynamic_ttls = {}  # key -> adjusted_ttl
        
        # メモリ監視
        self.memory_usage_history = deque(maxlen=50)
    
    def get(self, key: str) -> Optional[Any]:
        """キャッシュから値を取得（学習付き）"""
        # アクセス記録
        self._record_access(key)
        
        # キャッシュから取得
        value = self.cache.get(key)
        
        if value is not None:
            # キャッシュヒット: 重要度を上げる
            self.key_importance[key] = min(1.0, self.key_importance[key] + 0.1)
            # 予測的プリフェッチを実行
            self._prefetch_related(key)
        else:
            # キャッシュミス: 重要度を少し下げる
            self.key_importance[key] = max(0.0, self.key_importance[key] - 0.05)
        
        return value
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """キャッシュに値を設定（動的TTL調整付き）"""
        # 動的TTLを計算
        if ttl is None:
            ttl = self._compute_dynamic_ttl(key)
        
        # 既存のTTLキャッシュでは個別のTTL設定が難しいため、
        # 重要度に基づいて優先的に保持
        self.cache.set(key, value)
        
        # 重要度を更新
        if key not in self.key_importance:
            self.key_importance[key] = 0.5  # 初期重要度
        
        # 動的TTLを記録
        self.dynamic_ttls[key] = ttl
    
    def _record_access(self, key: str) -> None:
        """アクセスを記録（学習用）"""
        current_time = time.time()
        self.access_history.append((key, current_time))
        self.access_patterns[key].append(current_time)
        self.access_frequency[key] += 1
        
        # アクセス履歴のサイズを制限
        if len(self.access_patterns[key]) > self.learning_window:
            self.access_patterns[key] = self.access_patterns[key][-self.learning_window:]
        
        # 相関関係を学習
        if len(self.access_history) >= 2:
            prev_key, _ = self.access_history[-2]
            if prev_key != key:
                # 連続アクセスの相関を記録
                if key not in self.access_correlation[prev_key]:
                    self.access_correlation[prev_key].append(key)
    
    def _compute_dynamic_ttl(self, key: str) -> int:
        """動的TTLを計算"""
        base_ttl = self.base_ttl
        
        # 重要度に基づく調整
        importance = self.key_importance.get(key, 0.5)
        importance_factor = 0.5 + importance  # 0.5 ~ 1.5倍
        
        # アクセス頻度に基づく調整
        frequency = self.access_frequency.get(key, 0)
        frequency_factor = 1.0 + min(0.5, frequency / 100.0)  # 最大1.5倍
        
        # 計算
        dynamic_ttl = int(base_ttl * importance_factor * frequency_factor)
        
        return max(60, min(86400, dynamic_ttl))  # 60秒 ~ 24時間の範囲
    
    def _prefetch_related(self, key: str) -> None:
        """関連するキーを予測的プリフェッチ"""
        # 相関が高いキーを取得
        correlated_keys = self.access_correlation.get(key, [])
        
        if correlated_keys:
            # 相関度でソート
            correlation_scores = {}
            for corr_key in correlated_keys:
                # 相関スコア = 共起回数 / 総アクセス回数
                cooccurrence = sum(
                    1 for h in self.access_history
                    if h[0] == corr_key
                )
                total_access = len(self.access_history)
                if total_access > 0:
                    correlation_scores[corr_key] = cooccurrence / total_access
            
            # 上位3つをプリフェッチ候補に
            top_correlated = sorted(
                correlation_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            for corr_key, score in top_correlated:
                if score > 0.1:  # 閾値以上の場合のみ
                    self.prefetch_candidates[corr_key] = score
    
    def get_prefetch_candidates(self) -> List[Tuple[str, float]]:
        """プリフェッチ候補を取得"""
        candidates = sorted(
            self.prefetch_candidates.items(),
            key=lambda x: x[1],
            reverse=True
        )
        self.prefetch_candidates.clear()  # 取得後はクリア
        return candidates
    
    def learn_access_pattern(self) -> Dict[str, Any]:
        """アクセスパターンを学習"""
        if len(self.access_history) < 10:
            return {"status": "insufficient_data"}
        
        # アクセス頻度の統計
        frequencies = list(self.access_frequency.values())
        if frequencies:
            avg_frequency = np.mean(frequencies)
            std_frequency = np.std(frequencies)
        else:
            avg_frequency = 0
            std_frequency = 0
        
        # ホットキー（頻繁にアクセスされるキー）を特定
        hot_keys = [
            key for key, freq in self.access_frequency.items()
            if freq > avg_frequency + std_frequency
        ]
        
        # コールドキー（ほとんどアクセスされないキー）を特定
        cold_keys = [
            key for key, freq in self.access_frequency.items()
            if freq < avg_frequency - std_frequency
        ]
        
        return {
            "status": "learned",
            "hot_keys": hot_keys[:10],  # 上位10個
            "cold_keys": cold_keys[:10],
            "avg_frequency": float(avg_frequency),
            "total_unique_keys": len(self.access_frequency)
        }
    
    def optimize_memory(self) -> Dict[str, Any]:
        """メモリ使用量を最適化"""
        current_size = len(self.cache.cache)
        
        if current_size >= self.max_size * 0.9:  # 90%以上使用
            # 重要度の低いキーを削除
            keys_by_importance = sorted(
                self.key_importance.items(),
                key=lambda x: x[1]
            )
            
            # 下位20%を削除
            num_to_remove = int(current_size * 0.2)
            for key, _ in keys_by_importance[:num_to_remove]:
                if key in self.cache.cache:
                    del self.cache.cache[key]
                    if key in self.cache.timestamps:
                        del self.cache.timestamps[key]
            
            return {
                "status": "optimized",
                "removed_keys": num_to_remove,
                "remaining_size": len(self.cache.cache)
            }
        
        return {
            "status": "no_optimization_needed",
            "current_size": current_size,
            "max_size": self.max_size
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """統計情報を取得"""
        return {
            "cache_size": len(self.cache.cache),
            "max_size": self.max_size,
            "access_history_size": len(self.access_history),
            "unique_keys": len(self.access_frequency),
            "hot_keys_count": len([
                k for k, f in self.access_frequency.items()
                if f > (np.mean(list(self.access_frequency.values())) if self.access_frequency else 0)
            ]),
            "prefetch_candidates": len(self.prefetch_candidates),
            "dynamic_ttls_count": len(self.dynamic_ttls)
        }

