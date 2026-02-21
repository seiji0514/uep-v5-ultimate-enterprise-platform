"""
当事者視点のUX評価ツール
企業サイト・採用システムのアクセシビリティを評価
"""
from typing import Any, Dict, List

from .models import UXEvaluationRequest

# WCAG 2.1 に基づく当事者視点チェック項目
EVALUATION_ITEMS = [
    {
        "id": "contrast",
        "name": "コントラスト比",
        "description": "文字と背景のコントラスト比（4.5:1以上推奨）",
        "weight": 0.2,
    },
    {
        "id": "alt_text",
        "name": "代替テキスト",
        "description": "画像のalt属性の適切な設定",
        "weight": 0.15,
    },
    {
        "id": "keyboard",
        "name": "キーボード操作",
        "description": "キーボードのみでの操作可能性",
        "weight": 0.2,
    },
    {
        "id": "focus",
        "name": "フォーカス表示",
        "description": "フォーカスインジケーターの可視性",
        "weight": 0.15,
    },
    {"id": "heading", "name": "見出し構造", "description": "適切な見出し階層（h1-h6）", "weight": 0.1},
    {
        "id": "form_labels",
        "name": "フォームラベル",
        "description": "入力欄とラベルの関連付け",
        "weight": 0.1,
    },
    {
        "id": "readable",
        "name": "読みやすさ",
        "description": "フォントサイズ・行間・簡潔な表現",
        "weight": 0.1,
    },
]


def evaluate_url(request: UXEvaluationRequest) -> Dict[str, Any]:
    """
    URLのアクセシビリティを評価
    ※実際の実装では axe-core や pa11y 等でクロール評価
    デモではシミュレーション結果を返す
    """
    items_to_check = request.check_items or [i["id"] for i in EVALUATION_ITEMS]
    results = []
    total_score = 0.0
    total_weight = 0.0

    for item in EVALUATION_ITEMS:
        if item["id"] not in items_to_check:
            continue
        # デモ用: 擬似スコア（実際はURLをクロールして評価）
        import random

        random.seed(hash(request.url) % (2**32) + hash(item["id"]))
        score = round(random.uniform(0.5, 1.0), 2)
        results.append(
            {
                "id": item["id"],
                "name": item["name"],
                "description": item["description"],
                "score": score,
                "status": "pass" if score >= 0.7 else "fail",
                "recommendation": _get_recommendation(item["id"], score),
            }
        )
        total_score += score * item["weight"]
        total_weight += item["weight"]

    overall = round(total_score / total_weight if total_weight > 0 else 0, 2)
    return {
        "url": request.url,
        "overall_score": overall,
        "grade": _score_to_grade(overall),
        "items": results,
        "summary": _get_summary(overall),
    }


def _get_recommendation(item_id: str, score: float) -> str:
    """改善推奨メッセージ"""
    recs = {
        "contrast": "コントラスト比を4.5:1以上に調整してください。",
        "alt_text": "すべての意味のある画像にalt属性を設定してください。",
        "keyboard": "Tabキーで全要素にアクセスできることを確認してください。",
        "focus": "フォーカス時に視認可能な枠線を表示してください。",
        "heading": "h1から順に階層を飛ばさず使用してください。",
        "form_labels": "label要素で入力欄とラベルを関連付けてください。",
        "readable": "本文は16px以上、行間1.5以上を推奨します。",
    }
    return recs.get(item_id, "当事者視点での利用性を確認してください。")


def _score_to_grade(score: float) -> str:
    if score >= 0.9:
        return "A"
    if score >= 0.8:
        return "B"
    if score >= 0.7:
        return "C"
    return "D"


def _get_summary(score: float) -> str:
    if score >= 0.9:
        return "アクセシビリティが良好です。障害者雇用の観点でも評価が高い状態です。"
    if score >= 0.7:
        return "改善の余地があります。当事者視点での利用テストを推奨します。"
    return "アクセシビリティの改善が必要です。障害者雇用を検討する企業は早めの対応を推奨します。"
