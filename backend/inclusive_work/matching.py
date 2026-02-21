"""
障害者雇用マッチング
求職者と求人のマッチングロジック
"""
from typing import List, Dict, Any, Optional
from .models import MatchingRequest, DisabilityType, WorkStyle


# デモ用求人データ
DEMO_JOBS = [
    {
        "id": "job_001",
        "company": "テックソリューション株式会社",
        "title": "フロントエンドエンジニア",
        "skills": ["React", "TypeScript", "HTML", "CSS"],
        "work_style": "remote",
        "location": "東京都",
        "disability_support": ["リモート勤務可", "フレックス", "障害者手帳優遇"],
        "description": "Webアプリケーション開発。リモート中心。",
        "match_score": 0,
    },
    {
        "id": "job_002",
        "company": "アクセシビリティラボ",
        "title": "アクセシビリティエンジニア",
        "skills": ["WCAG", "a11y", "HTML", "ARIA"],
        "work_style": "hybrid",
        "location": "大阪府",
        "disability_support": ["完全リモート可", "障害者雇用実績あり"],
        "description": "アクセシビリティ評価・改善。当事者視点を重視。",
        "match_score": 0,
    },
    {
        "id": "job_003",
        "company": "AIスタートアップ",
        "title": "AIエンジニア",
        "skills": ["Python", "MLOps", "LLM", "RAG"],
        "work_style": "remote",
        "location": "福岡県",
        "disability_support": ["フルリモート", "在宅勤務", "通院配慮"],
        "description": "生成AI・RAG開発。リモート完結。",
        "match_score": 0,
    },
    {
        "id": "job_004",
        "company": "障害者雇用推進企業",
        "title": "システムエンジニア",
        "skills": ["Python", "FastAPI", "Docker"],
        "work_style": "hybrid",
        "location": "長崎県",
        "disability_support": ["障害者雇用率2.5%達成", "通勤支援", "柔軟勤務"],
        "description": "バックエンド開発。障害者雇用に積極的。",
        "match_score": 0,
    },
    {
        "id": "job_005",
        "company": "リモートワーク推進社",
        "title": "QAエンジニア",
        "skills": ["テスト", "自動化", "Pytest"],
        "work_style": "remote",
        "location": "全国",
        "disability_support": ["100%リモート", "障害者手帳優遇"],
        "description": "品質保証・テスト自動化。完全在宅。",
        "match_score": 0,
    },
]


def match_jobs(request: MatchingRequest) -> List[Dict[str, Any]]:
    """
    求職者と求人のマッチング
    スキル・勤務形態・障害支援でスコアリング
    """
    results = []
    for job in DEMO_JOBS:
        score = 0.0
        reasons = []

        # スキルマッチ
        if request.skills:
            matched = set(request.skills) & set(job["skills"])
            if matched:
                score += 0.4 * (len(matched) / len(request.skills))
                reasons.append(f"スキル一致: {', '.join(matched)}")
        else:
            score += 0.2

        # 勤務形態
        if request.work_style and job["work_style"] == request.work_style.value:
            score += 0.3
            reasons.append("勤務形態一致")
        elif not request.work_style:
            score += 0.15

        # リモート優先（障害者雇用で重要）
        if job["work_style"] == "remote":
            score += 0.2
            reasons.append("リモート勤務可")

        # キーワード
        if request.keywords:
            for kw in request.keywords:
                if kw.lower() in str(job).lower():
                    score += 0.1
                    break

        job_copy = {**job, "match_score": round(min(score, 1.0), 2), "match_reasons": reasons}
        results.append(job_copy)

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:10]
