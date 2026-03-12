"""
推論AI（o1系）モデルルーティング
タスク難度に応じて CoT（推論モデル）／直接推論（高速モデル）を自動選択
"""
import re
from typing import Any, Dict, Tuple

# 推論が必要なキーワード（高難度と判定）
REASONING_KEYWORDS = [
    "証明",
    "推論",
    "なぜ",
    "理由",
    "計算",
    "比較",
    "分析",
    "評価",
    "説明",
    "根拠",
    "論理",
    "因果",
    "仮説",
    "検証",
    "検討",
    "考察",
    "prove",
    "reason",
    "why",
    "compare",
    "analyze",
    "evaluate",
]

# 簡易なキーワード（低難度と判定）
SIMPLE_KEYWORDS = [
    "はい",
    "いいえ",
    "簡単",
    "簡単に",
    "要約",
    "一言",
    "簡潔",
    "yes",
    "no",
    "simple",
    "brief",
    "summary",
]


def assess_task_difficulty(problem: str) -> Tuple[float, str]:
    """
    タスク難度を評価（0.0〜1.0）

    Args:
        problem: 入力問題

    Returns:
        (難度スコア, 判定理由)
    """
    text = problem.strip()
    if not text:
        return 0.0, "空の入力"

    score = 0.0
    reasons = []

    # 1. 文字数（長いほど複雑）
    length = len(text)
    if length > 500:
        score += 0.3
        reasons.append("長文")
    elif length > 200:
        score += 0.15
        reasons.append("中文")

    # 2. 推論キーワード
    lower = text.lower()
    for kw in REASONING_KEYWORDS:
        if kw in text or kw in lower:
            score += 0.25
            reasons.append(f"推論キーワード:{kw}")
            break

    # 3. 簡易キーワード（スコアを下げる）
    for kw in SIMPLE_KEYWORDS:
        if kw in text or kw in lower:
            score -= 0.2
            reasons.append(f"簡易キーワード:{kw}")
            break

    # 4. 数式・複雑なパターン
    if re.search(r"\d+\s*[\+\-\*\/\^]\s*\d+", text) or re.search(r"\[.*\]", text):
        score += 0.2
        reasons.append("数式・構造")

    # 5. 複数質問
    if text.count("?") + text.count("？") > 1:
        score += 0.15
        reasons.append("複数質問")

    score = max(0.0, min(1.0, score))
    reason = "; ".join(reasons) if reasons else "デフォルト"

    return score, reason


def get_routing_decision(difficulty: float) -> Dict[str, Any]:
    """
    難度に応じたルーティング決定（モデル選択の見直し）

    Args:
        difficulty: 難度スコア（0.0〜1.0）

    Returns:
        ルーティング情報
    """
    if difficulty >= 0.7:
        return {
            "model_type": "reasoning",
            "reasoning_type": "cot",
            "description": "推論モデル（CoT）: 高難度のため多段階推論で処理",
            "max_steps": 7,
            "recommended_model": "gpt-4",
        }
    elif difficulty >= 0.5:
        return {
            "model_type": "reasoning",
            "reasoning_type": "cot",
            "description": "推論モデル（CoT）: 中難度のため段階的推論で処理",
            "max_steps": 5,
            "recommended_model": "gpt-4o-mini",
        }
    else:
        return {
            "model_type": "fast",
            "reasoning_type": "direct",
            "description": "高速モデル: 低難度のため直接推論で処理",
            "max_steps": 1,
            "recommended_model": "gpt-3.5-turbo",
        }
