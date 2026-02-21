"""
コードレビュー支援モジュール
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from generative_ai.llm_integration import llm_client


class CodeIssue(BaseModel):
    """コードの問題"""

    severity: str  # info, warning, error
    line_number: Optional[int] = None
    message: str
    suggestion: Optional[str] = None


class CodeReview(BaseModel):
    """コードレビュー"""

    overall_score: float  # 0.0 - 1.0
    issues: List[CodeIssue] = []
    suggestions: List[str] = []
    summary: str


class CodeReviewer:
    """コードレビュークラス"""

    async def review_code(
        self,
        code: str,
        language: str = "python",
        check_style: bool = True,
        check_security: bool = True,
        check_performance: bool = True,
    ) -> CodeReview:
        """
        コードをレビュー

        Args:
            code: レビュー対象のコード
            language: プログラミング言語
            check_style: スタイルチェックを行うか
            check_security: セキュリティチェックを行うか
            check_performance: パフォーマンスチェックを行うか

        Returns:
            レビュー結果
        """
        checks = []
        if check_style:
            checks.append("コードスタイル")
        if check_security:
            checks.append("セキュリティ")
        if check_performance:
            checks.append("パフォーマンス")

        checks_text = "、".join(checks)

        prompt = f"""以下の{language}コードをレビューしてください。{checks_text}の観点から評価してください。

コード:
{code}

レビュー結果を以下の形式で出力してください:
- 総合評価スコア（0.0-1.0）
- 発見された問題（重要度、行番号、メッセージ、改善提案）
- 改善提案
- サマリー"""

        result = await llm_client.generate(prompt, max_tokens=2000)
        review_text = result.get("text", "")

        # レビュー結果を解析（簡易実装）
        issues = []
        suggestions = []

        # 簡易的なパース（実際の実装ではより詳細な解析が必要）
        if "問題" in review_text or "issue" in review_text.lower():
            issues.append(
                CodeIssue(
                    severity="warning",
                    message="コードレビューで問題が検出されました",
                    suggestion="詳細なレビュー結果を確認してください",
                )
            )

        if "改善" in review_text or "improve" in review_text.lower():
            suggestions.append("コードの改善を検討してください")

        # スコアを抽出（簡易実装）
        score = 0.8  # デフォルトスコア

        return CodeReview(
            overall_score=score,
            issues=issues,
            suggestions=suggestions,
            summary=review_text[:500],  # 最初の500文字をサマリーとして使用
        )

    async def suggest_improvements(
        self, code: str, language: str = "python"
    ) -> List[str]:
        """
        改善提案を生成

        Args:
            code: 対象コード
            language: プログラミング言語

        Returns:
            改善提案のリスト
        """
        prompt = f"""以下の{language}コードの改善提案を3つ以上挙げてください。

コード:
{code}

改善提案:"""

        result = await llm_client.generate(prompt, max_tokens=1000)
        improvements_text = result.get("text", "")

        # 改善提案をリストに変換（簡易実装）
        suggestions = []
        for line in improvements_text.split("\n"):
            line = line.strip()
            if line and (
                line.startswith("-") or line.startswith("•") or line[0].isdigit()
            ):
                suggestions.append(line.lstrip("- •1234567890. "))

        return suggestions if suggestions else ["コードの品質向上を検討してください"]


# グローバルインスタンス
code_reviewer = CodeReviewer()
