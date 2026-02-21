"""
ドキュメント生成モジュール
"""
from typing import Any, Dict, Optional

from generative_ai.llm_integration import llm_client


class DocumentationGenerator:
    """ドキュメント生成クラス"""

    async def generate_api_docs(
        self, code: str, language: str = "python"
    ) -> Dict[str, Any]:
        """
        APIドキュメントを生成

        Args:
            code: APIコード
            language: プログラミング言語

        Returns:
            生成されたAPIドキュメント
        """
        prompt = f"""以下の{language}コードからAPIドキュメントを生成してください。

コード:
{code}

APIドキュメント（エンドポイント、パラメータ、レスポンス形式を含む）:"""

        result = await llm_client.generate(prompt, max_tokens=2000)

        return {
            "api_documentation": result.get("text", ""),
            "language": language,
            "source_code": code,
        }

    async def generate_readme(
        self,
        project_name: str,
        description: str,
        features: Optional[list] = None,
        installation: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        READMEを生成

        Args:
            project_name: プロジェクト名
            description: プロジェクトの説明
            features: 機能リスト（オプション）
            installation: インストール手順（オプション）

        Returns:
            生成されたREADME
        """
        features_text = "\n".join([f"- {f}" for f in features]) if features else ""
        installation_text = installation or "標準的なインストール手順"

        prompt = f"""以下の情報からREADME.mdを生成してください。

プロジェクト名: {project_name}
説明: {description}

機能:
{features_text}

インストール:
{installation_text}

README.md:"""

        result = await llm_client.generate(prompt, max_tokens=2000)

        return {"readme": result.get("text", ""), "project_name": project_name}

    async def generate_code_comments(
        self, code: str, language: str = "python"
    ) -> Dict[str, Any]:
        """
        コードコメントを生成

        Args:
            code: 対象コード
            language: プログラミング言語

        Returns:
            コメント付きコード
        """
        prompt = f"""以下の{language}コードに適切なコメントを追加してください。

コード:
{code}

コメント付きコード:"""

        result = await llm_client.generate(prompt, max_tokens=2000)

        return {
            "commented_code": result.get("text", ""),
            "language": language,
            "original_code": code,
        }


# グローバルインスタンス
documentation_generator = DocumentationGenerator()
