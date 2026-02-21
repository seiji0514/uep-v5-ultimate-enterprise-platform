"""
コード生成支援モジュール
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from generative_ai.llm_integration import llm_client


class CodeGenerator:
    """コード生成クラス"""

    async def generate_code(
        self,
        description: str,
        language: str = "python",
        framework: Optional[str] = None,
        requirements: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        コードを生成

        Args:
            description: コードの説明
            language: プログラミング言語
            framework: フレームワーク（オプション）
            requirements: 要件リスト（オプション）

        Returns:
            生成されたコード
        """
        requirements_text = (
            "\n".join([f"- {req}" for req in requirements]) if requirements else ""
        )
        framework_text = f" using {framework}" if framework else ""

        prompt = f"""以下の要件に基づいて{language}{framework_text}のコードを生成してください。

説明: {description}

要件:
{requirements_text}

コード:"""

        result = await llm_client.generate(prompt, max_tokens=2000)

        return {
            "code": result.get("text", ""),
            "language": language,
            "framework": framework,
            "description": description,
        }

    async def generate_test_code(
        self, code: str, language: str = "python", test_framework: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        テストコードを生成

        Args:
            code: テスト対象のコード
            language: プログラミング言語
            test_framework: テストフレームワーク（オプション）

        Returns:
            生成されたテストコード
        """
        test_framework_text = f" using {test_framework}" if test_framework else ""

        prompt = f"""以下のコードに対する{language}{test_framework_text}のテストコードを生成してください。

コード:
{code}

テストコード:"""

        result = await llm_client.generate(prompt, max_tokens=1500)

        return {
            "test_code": result.get("text", ""),
            "language": language,
            "test_framework": test_framework,
            "target_code": code,
        }

    async def refactor_code(
        self,
        code: str,
        language: str = "python",
        improvements: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        コードをリファクタリング

        Args:
            code: リファクタリング対象のコード
            language: プログラミング言語
            improvements: 改善点リスト（オプション）

        Returns:
            リファクタリングされたコード
        """
        improvements_text = (
            "\n".join([f"- {imp}" for imp in improvements])
            if improvements
            else "コードの品質を向上"
        )

        prompt = f"""以下の{language}コードをリファクタリングしてください。

改善点:
{improvements_text}

元のコード:
{code}

リファクタリング後のコード:"""

        result = await llm_client.generate(prompt, max_tokens=2000)

        return {
            "refactored_code": result.get("text", ""),
            "language": language,
            "original_code": code,
            "improvements": improvements,
        }


# グローバルインスタンス
code_generator = CodeGenerator()
