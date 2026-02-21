"""
アクセシビリティ特化AI
音声・簡易UI対応のチャット応答
"""
from typing import Any, Dict, Optional

try:
    from generative_ai.llm_integration import llm_client

    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    llm_client = None


# アクセシビリティ特化の定型応答（LLM未接続時用）
ACCESSIBILITY_RESPONSES = {
    "求人": "求人検索は「マッチング」タブから、スキルや勤務形態で検索できます。リモート勤務可の求人も多数あります。",
    "マッチング": "スキル（カンマ区切り）を入力すると、適合する求人が表示されます。例：Python, React, リモート",
    "相談": "就労相談は「相談」タブをご利用ください。障害者雇用制度やリモート勤務についてお答えします。",
    "評価": "企業サイトのアクセシビリティ評価は「UX評価」タブからURLを入力してください。",
    "リモート": "リモート勤務可能な求人は多数あります。マッチングで「リモート」と検索してみてください。",
    "障害者雇用": "障害者手帳をお持ちの方は、障害者雇用枠での応募が可能です。企業によって支援内容が異なります。",
    "デフォルト": "インクルーシブ雇用AIです。求人マッチング、就労相談、企業サイトのUX評価ができます。何をお手伝いしましょうか？",
}


async def chat(
    message: str, voice_input: bool = False, simple_ui: bool = False
) -> Dict[str, Any]:
    """
    アクセシビリティ特化AIチャット
    - 簡潔な応答（読み上げ・簡易UI向け）
    - キーワードに応じた定型応答 or LLM
    """
    message_lower = message.strip().lower()
    response_text = ACCESSIBILITY_RESPONSES["デフォルト"]

    for kw, resp in ACCESSIBILITY_RESPONSES.items():
        if kw != "デフォルト" and kw in message:
            response_text = resp
            break

    # LLMが利用可能な場合は補足を生成
    if LLM_AVAILABLE and llm_client and len(message) > 20:
        try:
            prompt = f"""障害者雇用・アクセシビリティに関する質問に、簡潔に（100字以内）答えてください。
質問: {message}
回答:"""
            result = await llm_client.generate(prompt, max_tokens=150, temperature=0.3)
            if result.get("text") and "Error" not in result.get("text", ""):
                response_text = result["text"][:200]
        except Exception:
            pass

    # 簡易UI・音声入力時はさらに短く
    if simple_ui or voice_input:
        if len(response_text) > 100:
            response_text = response_text[:100] + "…"

    return {
        "answer": response_text,
        "voice_input": voice_input,
        "simple_ui": simple_ui,
        "source": "accessibility_ai",
    }
