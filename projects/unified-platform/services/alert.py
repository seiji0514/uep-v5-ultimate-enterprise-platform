"""アラート通知 - Slack Webhook・メール連携"""
import httpx
from config import get_config


async def send_alert(title: str, message: str, severity: str = "info") -> bool:
    """Slack Webhook にアラートを送信（SLACK_WEBHOOK_URL 設定時）"""
    cfg = get_config()
    url = cfg.get("slack_webhook_url", "").strip()
    if not url:
        return False
    try:
        payload = {
            "text": f"[{severity.upper()}] {title}",
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*{title}*\n{message}"}},
            ],
        }
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(url, json=payload)
            return r.status_code == 200
    except Exception:
        return False
