"""
生成AI APIエンドポイント
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
from .llm_integration import llm_client, LLMProvider
from .rag import get_rag_system
from .reasoning import get_reasoning_engine
from .models import (
    GenerateRequest, RAGRequest, ReasoningRequest
)
from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

router = APIRouter(prefix="/api/v1/generative-ai", tags=["生成AI"])


@router.post("/generate")
@require_permission("read")
async def generate_text(
    request: GenerateRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """テキストを生成"""
    result = await llm_client.generate(
        prompt=request.prompt,
        model=request.model,
        max_tokens=request.max_tokens,
        temperature=request.temperature
    )
    return result


@router.post("/rag")
@require_permission("read")
async def rag_query(
    request: RAGRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """RAGを使用して回答を生成（ChromaDB ベクトル検索 + 評価指標）"""
    system = get_rag_system()
    # コレクション未指定時はデモ用 uep_docs を使用
    collection = request.collection or "uep_docs"
    result = await system.generate(
        query=request.query,
        collection=collection,
        context=request.context
    )
    return result


@router.post("/reasoning")
@require_permission("read")
async def reasoning(
    request: ReasoningRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """推論を実行（CoT / 直接推論）"""
    problem = request.get_problem()
    if not problem:
        raise HTTPException(status_code=422, detail="problem または question が必要です")
    engine = get_reasoning_engine()
    if request.reasoning_type == "cot":
        result = await engine.chain_of_thought(
            problem=problem,
            max_steps=request.max_steps or 5
        )
        # フロントエンド互換: answer を追加
        result["answer"] = result.get("final_answer", "")
    else:
        result = await engine.solve_problem(
            problem=problem,
            reasoning_type=request.reasoning_type
        )
    return result


@router.get("/rag/status")
@require_permission("read")
async def rag_status(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """RAG システムの状態（ChromaDB 利用可否・コレクション数）"""
    from .rag import CHROMADB_AVAILABLE, get_rag_system, _get_chroma_client
    system = get_rag_system()
    client = _get_chroma_client()
    collections = []
    if client:
        try:
            collections = [c.name for c in client.list_collections()]
        except Exception:
            pass
    return {
        "chromadb_available": CHROMADB_AVAILABLE,
        "chromadb_connected": client is not None,
        "collections": collections,
        "backend": "vector" if getattr(system, "_use_chromadb", False) else "memory",
    }


@router.post("/rag/documents")
@require_permission("manage_ai")
async def add_document(
    collection: str,
    document: str,
    metadata: Optional[Dict[str, Any]] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """ドキュメントをRAGシステムに追加"""
    system = get_rag_system()
    system.add_document(collection, document, metadata)
    return {
        "message": "Document added successfully",
        "collection": collection
    }
