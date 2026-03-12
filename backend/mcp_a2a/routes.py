"""
MCP / A2A プロトコル API
Model Context Protocol 風のツール呼び出し・エージェント間連携
"""
from typing import Any, Callable, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission


class MCPToolCall(BaseModel):
    """MCP風ツール呼び出しリクエスト"""

    tool_name: str
    arguments: Dict[str, Any] | None = None


class MCPToolCallResponse(BaseModel):
    """ツール呼び出しレスポンス"""

    tool_name: str
    result: Any
    status: str = "success"


# 利用可能なツール（デモ用）
AVAILABLE_TOOLS: Dict[str, Callable[..., Any]] = {}


def _register_tools():
    """ツールを登録"""
    def tool_echo(args: Dict) -> str:
        return str(args.get("message", ""))

    def tool_calc(args: Dict) -> float:
        a = float(args.get("a", 0))
        b = float(args.get("b", 0))
        op = args.get("op", "add")
        if op == "add":
            return a + b
        if op == "sub":
            return a - b
        if op == "mul":
            return a * b
        if op == "div":
            return a / b if b != 0 else 0
        return 0

    def tool_search(args: Dict) -> str:
        query = args.get("query", "")
        return f"[検索結果] '{query}' に関する情報（デモ応答）"

    AVAILABLE_TOOLS["echo"] = tool_echo
    AVAILABLE_TOOLS["calc"] = tool_calc
    AVAILABLE_TOOLS["search"] = tool_search


_register_tools()

router = APIRouter(prefix="/api/v1/mcp-a2a", tags=["MCP/A2A"])


@router.get("/tools")
@require_permission("read")
async def list_tools(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """利用可能なツール一覧（MCP風）"""
    return {
        "tools": [
            {"name": "echo", "description": "メッセージをエコー", "args": ["message"]},
            {"name": "calc", "description": "簡易計算", "args": ["a", "b", "op"]},
            {"name": "search", "description": "検索（デモ）", "args": ["query"]},
        ]
    }


@router.post("/tool-call", response_model=MCPToolCallResponse)
@require_permission("read")
async def mcp_tool_call(
    request: MCPToolCall,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """MCP風ツール呼び出しを実行"""
    tool = AVAILABLE_TOOLS.get(request.tool_name)
    if not tool:
        return MCPToolCallResponse(
            tool_name=request.tool_name,
            result=None,
            status="error: tool not found",
        )
    try:
        args = request.arguments or {}
        result = tool(args)
        return MCPToolCallResponse(tool_name=request.tool_name, result=result)
    except Exception as e:
        return MCPToolCallResponse(
            tool_name=request.tool_name,
            result=str(e),
            status="error",
        )


@router.post("/agent-message")
@require_permission("read")
async def a2a_agent_message(
    agent_id: str,
    message: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """A2A風エージェント間メッセージ（デモ: エコー応答）"""
    return {
        "from_agent": agent_id,
        "message": message,
        "response": f"[Agent {agent_id}] 受信: {message[:100]}...",
        "status": "delivered",
    }
