#!/usr/bin/env python3
"""
本番ユーザー登録スクリプト
UEP バックエンドの /api/v1/auth/register を呼び出してユーザーを登録します。
本番では PRODUCTION_USERS_FILE を設定すると永続化されます。
"""
import argparse
import json
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root))

try:
    import requests
except ImportError:
    print("requests をインストールしてください: pip install requests")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="本番ユーザー登録")
    parser.add_argument("--api-url", default="http://localhost:8080", help="UEP API のベースURL")
    parser.add_argument("--username", required=True, help="ユーザー名")
    parser.add_argument("--email", required=True, help="メールアドレス")
    parser.add_argument("--password", required=True, help="パスワード")
    parser.add_argument("--full-name", default="", help="氏名")
    parser.add_argument("--department", default="一般", help="部署")
    parser.add_argument("--admin", action="store_true", help="管理者ロールで登録（要バックエンド改修）")
    args = parser.parse_args()

    url = f"{args.api_url.rstrip('/')}/api/v1/auth/register"
    data = {
        "username": args.username,
        "email": args.email,
        "password": args.password,
        "full_name": args.full_name or args.username,
        "department": args.department,
    }

    try:
        r = requests.post(url, json=data, timeout=10)
        r.raise_for_status()
        result = r.json()
        print("登録成功:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("\n本番で永続化するには backend/.env に以下を設定:")
        print("  PRODUCTION_USERS_FILE=./data/production_users.json")
        return 0
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            try:
                err = e.response.json()
                print(f"詳細: {err.get('detail', err)}", file=sys.stderr)
            except Exception:
                print(e.response.text[:500], file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
