"""
RAG 精度向上モジュール
ハイブリッド検索、再ランキング、チャンク分割の最適化
"""
import re
from typing import Any, Dict, List, Optional, Tuple


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    separator: str = "\n",
) -> List[str]:
    """
    テキストを適切なチャンクに分割

    Args:
        text: 分割するテキスト
        chunk_size: チャンクの最大文字数
        chunk_overlap: オーバーラップ文字数（文脈の連続性）
        separator: 分割の優先区切り文字

    Returns:
        チャンクのリスト
    """
    if not text or len(text) <= chunk_size:
        return [text] if text else []

    chunks: List[str] = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            # 区切り文字で分割を調整
            last_sep = chunk.rfind(separator)
            if last_sep > chunk_size // 2:
                chunk = chunk[: last_sep + 1]
                end = start + len(chunk)
            else:
                # 句読点で分割
                for sep in ["。", ".", " ", "\n"]:
                    last_sep = chunk.rfind(sep)
                    if last_sep > chunk_size // 2:
                        chunk = chunk[: last_sep + 1]
                        end = start + len(chunk)
                        break

        chunks.append(chunk.strip())
        start = end - chunk_overlap if end < len(text) else len(text)

    return [c for c in chunks if c]


def keyword_search_score(query: str, document: str) -> float:
    """
    キーワードマッチによるスコア（BM25簡易版）

    Args:
        query: 検索クエリ
        document: ドキュメント

    Returns:
        スコア 0.0〜1.0
    """
    words = re.findall(r"\w+", query.lower())
    doc_lower = document.lower()
    if not words:
        return 0.0

    score = 0.0
    for w in words:
        if len(w) < 2:
            continue
        count = doc_lower.count(w)
        if count > 0:
            score += min(1.0, 0.5 + 0.5 * min(count, 5) / 5)
    return min(1.0, score / len(words)) if words else 0.0


def reciprocal_rank_fusion(
    results_list: List[List[Dict[str, Any]]], k: int = 60
) -> List[Dict[str, Any]]:
    """
    RRF（Reciprocal Rank Fusion）による再ランキング

    Args:
        results_list: 複数の検索結果リスト（例: ベクトル検索 + キーワード検索）
        k: RRF の定数（デフォルト60）

    Returns:
        再ランキングされた結果
    """
    if not results_list:
        return []

    scores: Dict[str, float] = {}
    doc_map: Dict[str, Dict[str, Any]] = {}

    for results in results_list:
        for rank, doc in enumerate(results, 1):
            # 同一ドキュメントの識別（textで判定）
            key = doc.get("text", "").strip()[:200]
            if not key:
                continue
            rrf_score = 1.0 / (k + rank)
            scores[key] = scores.get(key, 0) + rrf_score
            if key not in doc_map:
                doc_map[key] = doc.copy()

    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    output = []
    for i, (key, rrf_score) in enumerate(sorted_items):
        doc = doc_map[key].copy()
        doc["rerank_score"] = round(rrf_score, 4)
        doc["rerank_position"] = i + 1
        output.append(doc)
    return output
