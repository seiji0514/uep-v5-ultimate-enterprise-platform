"""
Chaos/GraphQL エンドポイントの診断スクリプト
ブラウザを経由せず、直接 localhost に接続してテスト
環境変数 PORT でポート指定可能（例: set PORT=8001 && python test_chaos_endpoint.py）
"""
import json
import os
import sys
import urllib.request


def test_url(url: str) -> dict:
    """URL に GET リクエストを送信"""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return {"status": resp.status, "body": resp.read().decode()}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": e.read().decode()}
    except Exception as e:
        return {"status": "error", "body": str(e)}


def main():
    # 127.0.0.1 を明示的に使用（localhost の IPv4/IPv6 の違いを回避）
    # 環境変数 PORT でポート指定可能（ポート8001で起動した場合）
    port = int(os.environ.get("PORT", "8000"))
    base = f"http://127.0.0.1:{port}"

    print("=" * 50)
    print("Chaos/GraphQL エンドポイント診断")
    print("=" * 50)

    for path in ["/", "/chaos-ok", "/api/v1/chaos/status", "/graphql"]:
        url = base + path
        print(f"\n{path}")
        result = test_url(url)
        print(f"  Status: {result['status']}")
        try:
            body = json.loads(result["body"])
            if "instance_id" in body:
                print(f"  Instance ID: {body['instance_id']}")
            if "error" in body:
                print(f"  Error: {body['error'].get('message', body['error'])}")
        except:
            print(f"  Body: {result['body'][:100]}...")

    print("\n" + "=" * 50)
    print("診断完了")
    print("=" * 50)


if __name__ == "__main__":
    main()
