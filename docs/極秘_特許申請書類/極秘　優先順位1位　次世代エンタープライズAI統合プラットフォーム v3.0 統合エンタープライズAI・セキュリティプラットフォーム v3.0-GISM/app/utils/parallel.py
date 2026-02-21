"""
並列処理ユーティリティ
- マルチプロセシング
- 非同期処理
- バッチ処理
"""
import asyncio
import logging
from typing import List, Callable, Any, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

logger = logging.getLogger(__name__)


class ParallelProcessor:
    """並列処理マネージャー"""
    
    def __init__(self, max_workers: Optional[int] = None):
        """
        Args:
            max_workers: 最大ワーカー数（Noneの場合はCPU数）
        """
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=self.max_workers)
    
    def process_parallel(
        self,
        items: List[Any],
        func: Callable,
        use_processes: bool = False
    ) -> List[Any]:
        """
        アイテムを並列処理
        
        Args:
            items: 処理するアイテムのリスト
            func: 処理関数
            use_processes: プロセスプールを使用するか（デフォルトはスレッドプール）
        
        Returns:
            処理結果のリスト
        """
        pool = self.process_pool if use_processes else self.thread_pool
        
        try:
            results = list(pool.map(func, items))
            return results
        except Exception as e:
            logger.error(f"Error in parallel processing: {e}")
            raise
    
    async def process_async(
        self,
        items: List[Any],
        func: Callable,
        batch_size: int = 10
    ) -> List[Any]:
        """
        アイテムを非同期でバッチ処理
        
        Args:
            items: 処理するアイテムのリスト
            func: 処理関数（非同期関数）
            batch_size: バッチサイズ
        
        Returns:
            処理結果のリスト
        """
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = await asyncio.gather(*[func(item) for item in batch])
            results.extend(batch_results)
        
        return results
    
    def shutdown(self) -> None:
        """プールをシャットダウン"""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)


class BatchProcessor:
    """バッチ処理マネージャー"""
    
    def __init__(self, batch_size: int = 100):
        """
        Args:
            batch_size: バッチサイズ
        """
        self.batch_size = batch_size
    
    def process_batch(
        self,
        items: List[Any],
        func: Callable,
        parallel: bool = False,
        processor: Optional[ParallelProcessor] = None
    ) -> List[Any]:
        """
        アイテムをバッチ処理
        
        Args:
            items: 処理するアイテムのリスト
            func: 処理関数
            parallel: 並列処理を使用するか
            processor: 並列プロセッサー（parallel=Trueの場合）
        
        Returns:
            処理結果のリスト
        """
        results = []
        
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            
            if parallel and processor:
                batch_results = processor.process_parallel(batch, func)
            else:
                batch_results = [func(item) for item in batch]
            
            results.extend(batch_results)
        
        return results


# グローバル並列プロセッサー
parallel_processor = ParallelProcessor()

