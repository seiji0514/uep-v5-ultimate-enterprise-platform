"""
顧客対応・CX モジュール
問い合わせ管理、チケット、カスタマーサポート、チャットボット
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional


class TicketManager:
    """チケット管理"""

    def __init__(self):
        self._tickets: Dict[str, Dict[str, Any]] = {}
        self._messages: Dict[str, List[Dict[str, Any]]] = {}

    def create_ticket(
        self,
        customer_id: str,
        subject: str,
        description: str,
        priority: str = "medium",
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """チケットを作成"""
        ticket_id = str(uuid.uuid4())
        ticket = {
            "id": ticket_id,
            "customer_id": customer_id,
            "subject": subject,
            "description": description,
            "priority": priority,
            "category": category or "general",
            "status": "open",
            "assigned_to": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._tickets[ticket_id] = ticket
        self._messages[ticket_id] = []
        return ticket

    def list_tickets(
        self, status: Optional[str] = None, customer_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """チケット一覧"""
        tickets = list(self._tickets.values())
        if status:
            tickets = [t for t in tickets if t["status"] == status]
        if customer_id:
            tickets = [t for t in tickets if t["customer_id"] == customer_id]
        return tickets

    def update_ticket_status(
        self, ticket_id: str, status: str, assigned_to: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """チケットステータスを更新"""
        if ticket_id not in self._tickets:
            return None
        ticket = self._tickets[ticket_id]
        ticket["status"] = status
        if assigned_to is not None:
            ticket["assigned_to"] = assigned_to
        ticket["updated_at"] = datetime.utcnow().isoformat()
        return ticket

    def add_message(
        self, ticket_id: str, message: str, sender: str, is_ai: bool = False
    ) -> Optional[Dict[str, Any]]:
        """チケットにメッセージを追加"""
        if ticket_id not in self._tickets:
            return None
        msg = {
            "id": str(uuid.uuid4()),
            "ticket_id": ticket_id,
            "message": message,
            "sender": sender,
            "is_ai": is_ai,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._messages[ticket_id].append(msg)
        self._tickets[ticket_id]["updated_at"] = datetime.utcnow().isoformat()
        return msg


class ChatbotManager:
    """AIチャットボット"""

    def __init__(self):
        self._responses = {
            "default": "お問い合わせありがとうございます。担当者が確認いたします。少々お待ちください。",
            "faq": {
                "営業時間": "営業時間は平日9:00〜18:00です。",
                "返品": "返品・交換については商品到着後7日以内にご連絡ください。",
                "支払い": "クレジットカード、銀行振込、代引きをご利用いただけます。",
            },
        }

    def get_response(self, message: str) -> str:
        """AI応答を生成（簡易ルールベース）"""
        msg_lower = message.lower().strip()
        for keyword, response in self._responses["faq"].items():
            if keyword in msg_lower:
                return response
        return self._responses["default"]

    def chat(
        self,
        message: str,
        ticket_id: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """チャット応答"""
        response = self.get_response(message)
        return {
            "message": message,
            "response": response,
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "is_ai": True,
            "created_at": datetime.utcnow().isoformat(),
        }


ticket_manager = TicketManager()
chatbot_manager = ChatbotManager()
