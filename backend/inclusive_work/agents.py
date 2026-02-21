"""
AIエージェント基盤
マッチング・相談・評価エージェントのオーケストレーション
"""
from typing import Any, Dict, List

from .matching import match_jobs
from .models import DisabilityType, MatchingRequest, WorkStyle


class AgentOrchestrator:
    """エージェントオーケストレーター"""

    async def execute(
        self, task_type: str, query: str, context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        タスクタイプに応じてエージェントを起動
        matching: マッチングエージェント
        consultation: 相談エージェント
        evaluation: 評価エージェント
        """
        context = context or {}

        if task_type == "matching":
            return await self._matching_agent(query, context)
        elif task_type == "consultation":
            return await self._consultation_agent(query, context)
        elif task_type == "evaluation":
            return await self._evaluation_agent(query, context)
        else:
            return {
                "task_type": task_type,
                "status": "unknown",
                "message": f"未対応のタスクタイプ: {task_type}",
            }

    async def _matching_agent(
        self, query: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """マッチングエージェント"""
        # クエリからスキル等を簡易抽出（実際はLLMで解析）
        skills = context.get("skills", [])
        if not skills and query:
            # クエリをカンマで分割してスキルとして扱う
            skills = [s.strip() for s in query.split(",") if s.strip()]
        work_style = context.get("work_style")
        if work_style is None and ("リモート" in query or "在宅" in query):
            work_style = "remote"
        try:
            ws = WorkStyle(work_style) if work_style else None
        except ValueError:
            ws = None

        request = MatchingRequest(
            skills=skills,
            work_style=ws,
            keywords=context.get("keywords"),
        )
        jobs = match_jobs(request)
        return {
            "task_type": "matching",
            "status": "success",
            "query": query,
            "matches": jobs,
            "count": len(jobs),
        }

    async def _consultation_agent(
        self, query: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """相談エージェント（就労相談・制度案内）"""
        # 簡易応答（実際はLLM連携）
        responses = {
            "障害者雇用": "障害者雇用率2.3%以上の法定雇用率があります。障害者手帳をお持ちの方は、企業の障害者雇用枠での応募が可能です。",
            "リモート": "リモート勤務は障害者雇用で人気が高く、通勤負担を軽減できます。求人検索で「リモート」「在宅」で絞り込み可能です。",
            "手帳": "身体障害者手帳、療育手帳、精神障害者保健福祉手帳のいずれかをお持ちの場合、障害者雇用枠での応募が可能です。",
        }
        answer = "就労に関するご相談ですね。"
        for kw, resp in responses.items():
            if kw in query:
                answer = resp
                break
        return {
            "task_type": "consultation",
            "status": "success",
            "query": query,
            "answer": answer,
        }

    async def _evaluation_agent(
        self, query: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """評価エージェント（UX評価のトリガー）"""
        url = context.get("url") or query
        if not url.startswith("http"):
            url = f"https://{url}"
        return {
            "task_type": "evaluation",
            "status": "pending",
            "message": f"UX評価をキューに追加しました: {url}",
            "url": url,
        }


agent_orchestrator = AgentOrchestrator()
