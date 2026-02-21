"""
LLM統合モジュール
大規模言語モデルの統合
"""
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel
import httpx
import os


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
        **kwargs
    ) -> Dict[str, Any]:
        """
        テキストを生成

        Args:
            prompt: プロンプト
            model: モデル名
            max_tokens: 最大トークン数
            temperature: 温度パラメータ
            **kwargs: その他のパラメータ

        Returns:
            生成結果
        """
        if self.provider == LLMProvider.OPENAI:
            return await self._generate_openai(prompt, model, max_tokens, temperature, **kwargs)
        elif self.provider == LLMProvider.LOCAL:
            return await self._generate_local(prompt, model, max_tokens, temperature, **kwargs)
        else:
            # その他のプロバイダーは簡易実装
            return {
                "text": f"[{self.provider}] Generated response for: {prompt[:50]}...",
                "model": model,
                "provider": self.provider.value
            }

    async def _generate_openai(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> Dict[str, Any]:
        """OpenAI APIを使用して生成"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        **kwargs
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "text": data["choices"][0]["message"]["content"],
                        "model": model,
                        "provider": "openai",
                        "usage": data.get("usage", {})
                    }
                else:
                    return {
                        "text": f"Error: {response.status_code}",
                        "model": model,
                        "provider": "openai",
                        "error": response.text
                    }
        except Exception as e:
            return {
                "text": f"Error: {str(e)}",
                "model": model,
                "provider": "openai",
                "error": str(e)
            }

    async def _generate_local(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        **kwargs
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
                        **kwargs
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "text": data.get("text", ""),
                        "model": model,
                        "provider": "local"
                    }
                else:
                    return {
                        "text": f"Error: {response.status_code}",
                        "model": model,
                        "provider": "local",
                        "error": response.text
                    }
        except Exception as e:
            return {
                "text": f"Error: {str(e)}",
                "model": model,
                "provider": "local",
                "error": str(e)
            }

    async def embed(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """テキストを埋め込みベクトルに変換"""
        # 簡易実装
        return [0.0] * 1536  # ダミーベクトル


# グローバルインスタンス
llm_client = LLMClient()
