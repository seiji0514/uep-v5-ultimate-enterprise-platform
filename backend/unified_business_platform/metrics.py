"""
統合ビジネスプラットフォーム - Prometheusメトリクス
実用的最高難易度: 監視・オブザーバビリティ統合
"""
from prometheus_client import Counter, Gauge, Histogram

# 業務効率化・DX
workflow_created_total = Counter(
    "unified_business_workflow_created_total",
    "Total workflows created",
    ["workflow_type"],
)
approval_requests_total = Counter(
    "unified_business_approval_requests_total",
    "Total approval requests",
    ["status"],
)
rpa_jobs_executed_total = Counter(
    "unified_business_rpa_jobs_executed_total",
    "Total RPA jobs executed",
    ["task_type", "status"],
)
rpa_job_duration_seconds = Histogram(
    "unified_business_rpa_job_duration_seconds",
    "RPA job execution duration",
    ["task_type"],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0),
)

# 人材・組織
disability_supports_total = Gauge(
    "unified_business_disability_supports_total",
    "Total registered disability supports",
)
onboarding_tasks_total = Gauge(
    "unified_business_onboarding_tasks_total",
    "Total onboarding tasks",
    ["status"],
)
skill_matches_total = Counter(
    "unified_business_skill_matches_total",
    "Total skill matching queries",
)

# 顧客対応・CX
tickets_total = Counter(
    "unified_business_tickets_total",
    "Total tickets created",
    ["priority", "status"],
)
chatbot_requests_total = Counter(
    "unified_business_chatbot_requests_total",
    "Total chatbot requests",
)
ticket_resolution_seconds = Histogram(
    "unified_business_ticket_resolution_seconds",
    "Ticket resolution time (simulated)",
    buckets=(60, 300, 600, 3600, 86400),
)
