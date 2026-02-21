"""
RAG (Retrieval-Augmented Generation) モジュール
ChromaDB によるベクトル検索 + 評価指標
"""
import time
import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .llm_integration import LLMClient

# ChromaDB の利用可否
CHROMADB_AVAILABLE = False
_chroma_client = None

try:
    import chromadb
    from chromadb.config import Settings

    CHROMADB_AVAILABLE = True
except ImportError:
    pass


def _get_chroma_client():
    """ChromaDB クライアントを取得（永続化付き）"""
    global _chroma_client
    if _chroma_client is None and CHROMADB_AVAILABLE:
        try:
            import os

            persist_path = os.path.join(
                os.path.dirname(__file__), "..", "data", "chroma_db"
            )
            os.makedirs(persist_path, exist_ok=True)
            _chroma_client = chromadb.PersistentClient(
                path=persist_path, settings=Settings(anonymized_telemetry=False)
            )
        except Exception:
            _chroma_client = False
    return _chroma_client if _chroma_client else None


def _get_or_create_collection(name: str):
    """コレクションを取得または作成"""
    client = _get_chroma_client()
    if not client:
        return None
    try:
        return client.get_or_create_collection(
            name=name, metadata={"hnsw:space": "cosine"}
        )
    except Exception:
        return None


class RAGSystem:
    """RAGシステムクラス（ChromaDB ベクトル検索 + フォールバック）"""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self._knowledge_base: Dict[str, List[Dict[str, Any]]] = {}
        self._use_chromadb = CHROMADB_AVAILABLE and _get_chroma_client() is not None
        self._ensure_default_docs()

    def _ensure_default_docs(self):
        """デモ用のデフォルトドキュメントを投入（初回のみ）"""
        default_docs = [
            (
                "uep_docs",
                "UEP v5.0 は次世代エンタープライズ統合プラットフォームです。MLOps、生成AI、監視、セキュリティ、クラウドインフラを統合しています。",
                {"source": "README"},
            ),
            (
                "uep_docs",
                "RAG（Retrieval-Augmented Generation）は、外部知識を検索してLLMの入力に加え、根拠のある回答を生成する技術です。ハルシネーションを軽減します。",
                {"source": "AI"},
            ),
            (
                "uep_docs",
                "CoT（Chain-of-Thought）推論は、段階的に思考を進めることで複雑な問題を解く手法です。",
                {"source": "AI"},
            ),
            (
                "uep_docs",
                "Contract Testing は、APIの契約（リクエスト・レスポンス形式）を検証するテスト手法です。",
                {"source": "品質"},
            ),
            (
                "uep_docs",
                "Chaos Engineering は、障害を意図的に注入してシステムのレジリエンスを検証する手法です。",
                {"source": "品質"},
            ),
        ]
        # ChromaDB 使用時はコレクションが空の場合のみ投入
        if self._use_chromadb:
            coll = _get_or_create_collection("uep_docs")
            if coll and coll.count() > 0:
                return
        elif self._knowledge_base.get("uep_docs"):
            return
        for coll, text, meta in default_docs:
            self.add_document(coll, text, meta)

    def add_document(
        self, collection: str, document: str, metadata: Optional[Dict[str, Any]] = None
    ):
        """ドキュメントを追加"""
        meta = metadata or {}
        doc_id = str(uuid.uuid4())

        # ChromaDB に追加
        if self._use_chromadb:
            coll = _get_or_create_collection(collection)
            if coll:
                try:
                    coll.add(documents=[document], metadatas=[meta], ids=[doc_id])
                    return
                except Exception:
                    pass

        # フォールバック: メモリ
        if collection not in self._knowledge_base:
            self._knowledge_base[collection] = []
        self._knowledge_base[collection].append(
            {"text": document, "metadata": meta, "id": doc_id}
        )

    async def retrieve(
        self, query: str, collection: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """関連ドキュメントをベクトル検索"""
        # ChromaDB で検索
        if self._use_chromadb:
            coll = _get_or_create_collection(collection)
            if coll:
                try:
                    result = coll.query(
                        query_texts=[query],
                        n_results=top_k,
                        include=["documents", "metadatas", "distances"],
                    )
                    if result and result["documents"] and result["documents"][0]:
                        docs = []
                        for i, doc in enumerate(result["documents"][0]):
                            dist = (
                                result["distances"][0][i]
                                if result.get("distances")
                                else 0
                            )
                            # コサイン距離→類似度（1 - distance）
                            score = 1.0 - dist if dist is not None else 1.0
                            docs.append(
                                {
                                    "text": doc,
                                    "metadata": result["metadatas"][0][i]
                                    if result.get("metadatas")
                                    else {},
                                    "score": round(score, 4),
                                }
                            )
                        return docs
                except Exception:
                    pass

        # フォールバック: キーワードマッチ
        documents = self._knowledge_base.get(collection, [])
        query_lower = query.lower()
        matched = []
        for doc in documents:
            if query_lower in doc["text"].lower():
                matched.append({**doc, "score": 1.0})
        return matched[:top_k]

    async def generate(
        self,
        query: str,
        collection: Optional[str] = None,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """RAG で回答を生成（評価指標付き）"""
        start_time = time.perf_counter()
        retrieved_docs: List[Dict[str, Any]] = []

        if collection:
            retrieved_docs = await self.retrieve(query, collection)

        retrieve_latency_ms = (time.perf_counter() - start_time) * 1000

        context_text = context or ""
        if retrieved_docs:
            context_text += "\n\n".join([d["text"] for d in retrieved_docs])

        prompt = f"""以下のコンテキストを使用して質問に答えてください。

コンテキスト:
{context_text or "（コンテキストなし）"}

質問: {query}

回答:"""

        gen_start = time.perf_counter()
        result = await self.llm_client.generate(prompt)
        gen_latency_ms = (time.perf_counter() - gen_start) * 1000

        answer = result.get("text", "")
        total_latency_ms = (time.perf_counter() - start_time) * 1000

        # 評価指標
        avg_score = (
            sum(d.get("score", 1.0) for d in retrieved_docs) / len(retrieved_docs)
            if retrieved_docs
            else 0.0
        )
        metrics = {
            "retrieve_latency_ms": round(retrieve_latency_ms, 2),
            "generation_latency_ms": round(gen_latency_ms, 2),
            "total_latency_ms": round(total_latency_ms, 2),
            "retrieved_count": len(retrieved_docs),
            "avg_relevance_score": round(avg_score, 4),
            "answer_length": len(answer),
        }

        return {
            "answer": answer,
            "sources": retrieved_docs,
            "model": result.get("model"),
            "provider": result.get("provider"),
            "metrics": metrics,
        }


# グローバルインスタンス（遅延初期化）
_rag_system_cache = None


def get_rag_system() -> RAGSystem:
    """RAGシステムを取得"""
    global _rag_system_cache
    if _rag_system_cache is None:
        from .llm_integration import llm_client

        _rag_system_cache = RAGSystem(llm_client)
    return _rag_system_cache


rag_system = None
