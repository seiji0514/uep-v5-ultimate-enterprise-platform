"""
LLM統合モジュール
大規模言語モデルの統合（キャッシュ・フェイルオーバー対応）
"""
import hashlib
import json
import os
from enum import Enum
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel

# 推論レイテンシ低減: キャッシュ（Redis またはメモリ）
_llm_cache: Optional[Dict[str, Any]] = None
_llm_cache_ttl = 3600  # 1時間


def _get_llm_cache():
    """LLMキャッシュを取得（Redis があれば使用、なければメモリ）"""
    global _llm_cache
    if _llm_cache is None:
        try:
            import redis

            r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
            r.ping()
            return ("redis", r)
        except Exception:
            _llm_cache = {}
    return ("memory", _llm_cache)


def _llm_cache_key(prompt: str, model: str, max_tokens: int, temperature: float) -> str:
    """キャッシュキーを生成"""
    data = json.dumps(
        {"p": prompt[:500], "m": model, "t": max_tokens, "temp": temperature},
        sort_keys=True,
    )
    return "llm:" + hashlib.sha256(data.encode()).hexdigest()


def _get_cached(
    prompt: str, model: str, max_tokens: int, temperature: float
) -> Optional[Dict[str, Any]]:
    """キャッシュから取得"""
    key = _llm_cache_key(prompt, model, max_tokens, temperature)
    cache_type, cache = _get_llm_cache()
    if cache_type == "redis":
        try:
            val = cache.get(key)
            if val:
                return json.loads(val)
        except Exception:
            pass
    else:
        entry = cache.get(key)
        if entry and entry.get("expires", 0) > __import__("time").time():
            return entry.get("value")
    return None


def _set_cached(
    prompt: str, model: str, max_tokens: int, temperature: float, value: Dict[str, Any]
):
    """キャッシュに保存"""
    import time

    key = _llm_cache_key(prompt, model, max_tokens, temperature)
    cache_type, cache = _get_llm_cache()
    expires = int(time.time()) + _llm_cache_ttl
    if cache_type == "redis":
        try:
            cache.setex(key, _llm_cache_ttl, json.dumps(value))
        except Exception:
            pass
    else:
        cache[key] = {"value": value, "expires": expires}


class LLMProvider(str, Enum):
    """LLMプロバイダー"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"


class LLMClient:
    """LLMクライアントクラス"""

    def __init__(self, provider: LLMProvider = LLMProvider.OPENAI):
        """
        LLMクライアントを初期化

        Args:
            provider: LLMプロバイダー
        """
        self.provider = provider
        self.api_key = os.getenv(f"{provider.upper()}_API_KEY", "")
        self.base_url = self._get_base_url(provider)

    def _get_base_url(self, provider: LLMProvider) -> str:
        """プロバイダーに応じたベースURLを取得"""
        urls = {
            LLMProvider.OPENAI: "https://api.openai.com/v1",
            LLMProvider.ANTHROPIC: "https://api.anthropic.com/v1",
            LLMProvider.GOOGLE: "https://generativelanguage.googleapis.com/v1",
            LLMProvider.LOCAL: os.getenv("LOCAL_LLM_URL", "http://localhost:8001"),
        }
        return urls.get(provider, "")

    async def generate(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        use_cache: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        テキストを生成（キャッシュ対応でレイテンシ低減）

        Args:
            prompt: プロンプト
            model: モデル名
            max_tokens: 最大トークン数
            temperature: 温度パラメータ
            use_cache: キャッシュを使用するか
            **kwargs: その他のパラメータ

        Returns:
            生成結果
        """
        if use_cache:
            cached = _get_cached(prompt, model, max_tokens, temperature)
            if cached:
                return {**cached, "cached": True}

        async def _primary():
            if self.provider == LLMProvider.OPENAI:
                return await self._generate_openai(
                    prompt, model, max_tokens, temperature, **kwargs
                )
            elif self.provider == LLMProvider.LOCAL:
                return await self._generate_local(
                    prompt, model, max_tokens, temperature, **kwargs
                )
            else:
                return {
                    "text": f"[{self.provider}] Generated response for: {prompt[:50]}...",
                    "model": model,
                    "provider": self.provider.value,
                }

        try:
            from core.health_failover import failover_execute

            result = await failover_execute(
                _primary,
                fallback_value={
                    "text": "[フェイルオーバー] 一時的に応答できません。しばらくしてから再試行してください。",
                    "model": model,
                    "provider": self.provider.value,
                    "error": "failover",
                },
            )
        except ImportError:
            result = await _primary()

        if use_cache and result.get("text") and not result.get("error"):
            _set_cached(prompt, model, max_tokens, temperature, result)
        return result

    async def _generate_openai(
        self, prompt: str, model: str, max_tokens: int, temperature: float, **kwargs
    ) -> Dict[str, Any]:
        """OpenAI APIを使用して生成"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        **kwargs,
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "text": data["choices"][0]["message"]["content"],
                        "model": model,
                        "provider": "openai",
                        "usage": data.get("usage", {}),
                    }
                else:
                    return {
                        "text": f"Error: {response.status_code}",
                        "model": model,
                        "provider": "openai",
                        "error": response.text,
                    }
        except Exception as e:
            return {
                "text": f"Error: {str(e)}",
                "model": model,
                "provider": "openai",
                "error": str(e),
            }

    async def _generate_local(
        self, prompt: str, model: str, max_tokens: int, temperature: float, **kwargs
    ) -> Dict[str, Any]:
        """ローカルLLMを使用して生成"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "prompt": prompt,
                        "model": model,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        **kwargs,
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "text": data.get("text", ""),
                        "model": model,
                        "provider": "local",
                    }
                else:
                    return {
                        "text": f"Error: {response.status_code}",
                        "model": model,
                        "provider": "local",
                        "error": response.text,
                    }
        except Exception as e:
            return {
                "text": f"Error: {str(e)}",
                "model": model,
                "provider": "local",
                "error": str(e),
            }

    async def embed(
        self, text: str, model: str = "text-embedding-ada-002"
    ) -> List[float]:
        """テキストを埋め込みベクトルに変換"""
        # 簡易実装
        return [0.0] * 1536  # ダミーベクトル


# グローバルインスタンス
llm_client = LLMClient()
