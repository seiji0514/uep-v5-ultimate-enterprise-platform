"""
推論エンジンモジュール
Chain of Thought (CoT) 推論の実装（プロンプト強化版）
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .llm_integration import LLMClient

# CoT 強化プロンプトテンプレート
COT_STEP_PROMPT = """あなたは論理的推論の専門家です。以下の問題を段階的に分析し、根拠に基づいて推論してください。

## 問題
{problem}

## これまでの推論
{prior_steps}

## ステップ {step_num} の指示
1. 現時点で分かっている事実を整理する
2. 次の論理的な推論ステップを明確に述べる
3. その推論の根拠・理由を説明する
4. 結論に到達した場合は「結論:」で明示する

推論:"""

COT_FINAL_PROMPT = """以下の問題に対する推論プロセスを踏まえ、最終回答を導出してください。

## 問題
{problem}

## 推論プロセス
{steps}

## 最終回答の指示
- 推論プロセスを要約し、結論を明確に述べる
- 不確実な部分があればその旨を記載する

最終回答:"""


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
        self, problem: str, max_steps: int = 5, model: Optional[str] = None
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
        prior_steps_text = ""
        for step_num in range(1, max_steps + 1):
            prompt = COT_STEP_PROMPT.format(
                problem=problem,
                prior_steps=prior_steps_text or "（初回）",
                step_num=step_num,
            )

            gen_kw = {"max_tokens": 600, "temperature": 0.5}
            if model:
                gen_kw["model"] = model
            result = await self.llm_client.generate(prompt, **gen_kw)

            reasoning_text = result.get("text", "")

            # ステップを解析（簡易実装）
            step = ReasoningStep(
                step_number=step_num,
                thought=f"ステップ{step_num}の思考",
                reasoning=reasoning_text,
            )

            steps.append(step)

            if "結論" in reasoning_text or "答え" in reasoning_text or "最終" in reasoning_text:
                step.conclusion = reasoning_text
                prior_steps_text += f"\nステップ{step_num}: {reasoning_text}"
                break

            prior_steps_text += f"\nステップ{step_num}: {reasoning_text}"

        steps_text = "\n".join([f"ステップ{s.step_number}: {s.reasoning}" for s in steps])
        final_prompt = COT_FINAL_PROMPT.format(problem=problem, steps=steps_text)
        final_kw = {"temperature": 0.3}
        if model:
            final_kw["model"] = model
        final_result = await self.llm_client.generate(final_prompt, **final_kw)

        return {
            "problem": problem,
            "steps": [step.dict() for step in steps],
            "final_answer": final_result.get("text", ""),
            "total_steps": len(steps),
        }

    async def solve_problem(
        self, problem: str, reasoning_type: str = "cot", model: Optional[str] = None
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
            return await self.chain_of_thought(problem, model=model)
        else:
            gen_kw = {}
            if model:
                gen_kw["model"] = model
            result = await self.llm_client.generate(problem, **gen_kw)
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
