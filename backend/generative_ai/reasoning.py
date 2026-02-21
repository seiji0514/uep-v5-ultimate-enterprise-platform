"""
推論エンジンモジュール
Chain of Thought (CoT) 推論の実装
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .llm_integration import LLMClient


class ReasoningStep(BaseModel):
    """推論ステップ"""

    step_number: int
    thought: str
    reasoning: str
    conclusion: Optional[str] = None


class ReasoningEngine:
    """推論エンジンクラス"""

    def __init__(self, llm_client: LLMClient):
        """
        推論エンジンを初期化

        Args:
            llm_client: LLMクライアント
        """
        self.llm_client = llm_client

    async def chain_of_thought(
        self, problem: str, max_steps: int = 5
    ) -> Dict[str, Any]:
        """
        Chain of Thought推論を実行

        Args:
            problem: 問題
            max_steps: 最大ステップ数

        Returns:
            推論結果
        """
        steps: List[ReasoningStep] = []
        current_problem = problem

        for step_num in range(1, max_steps + 1):
            # 推論ステップを生成
            prompt = f"""問題: {current_problem}

ステップ {step_num}:
1. 現在の状況を分析してください
2. 次の推論ステップを考えてください
3. 結論に到達できるか判断してください

推論:"""

            result = await self.llm_client.generate(
                prompt, max_tokens=500, temperature=0.7
            )

            reasoning_text = result.get("text", "")

            # ステップを解析（簡易実装）
            step = ReasoningStep(
                step_number=step_num,
                thought=f"ステップ{step_num}の思考",
                reasoning=reasoning_text,
            )

            steps.append(step)

            # 結論に到達したかチェック（簡易実装）
            if "結論" in reasoning_text or "答え" in reasoning_text:
                step.conclusion = reasoning_text
                break

            # 次のステップのための問題を更新
            current_problem = f"{problem}\n\nこれまでの推論:\n{reasoning_text}"

        # 最終回答を生成
        final_prompt = f"""問題: {problem}

推論プロセス:
{chr(10).join([f"ステップ{s.step_number}: {s.reasoning}" for s in steps])}

最終回答:"""

        final_result = await self.llm_client.generate(final_prompt)

        return {
            "problem": problem,
            "steps": [step.dict() for step in steps],
            "final_answer": final_result.get("text", ""),
            "total_steps": len(steps),
        }

    async def solve_problem(
        self, problem: str, reasoning_type: str = "cot"
    ) -> Dict[str, Any]:
        """
        問題を解決

        Args:
            problem: 問題
            reasoning_type: 推論タイプ（cot, direct等）

        Returns:
            解決結果
        """
        if reasoning_type == "cot":
            return await self.chain_of_thought(problem)
        else:
            # 直接推論
            result = await self.llm_client.generate(problem)
            return {
                "problem": problem,
                "answer": result.get("text", ""),
                "reasoning_type": "direct",
            }


# グローバルインスタンス（遅延初期化で循環インポートを回避）
_reasoning_engine_cache = None


def get_reasoning_engine() -> ReasoningEngine:
    """推論エンジンを取得（遅延初期化）"""
    global _reasoning_engine_cache
    if _reasoning_engine_cache is None:
        from .llm_integration import llm_client

        _reasoning_engine_cache = ReasoningEngine(llm_client)
    return _reasoning_engine_cache


# 後方互換性のため（モジュール読み込み時は初期化しない）
reasoning_engine = None
