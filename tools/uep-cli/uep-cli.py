#!/usr/bin/env python3
"""
uep-cli: UEP v5.0 CLI（Python版）
Go exe の代わりに使用。McAfee 等のセキュリティソフトで隔離されない。

使い方:
  python uep-cli.py version
  python uep-cli.py health
  python uep-cli.py events list
  python uep-cli.py events outbox
  python uep-cli.py grpc status
  python uep-cli.py graphql query -q "{ hello health { status } }"
"""
import argparse
import json
import socket
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

VERSION = "1.1.0"
DEFAULT_API_URL = "http://localhost:8000"
DEFAULT_GRPC_ADDR = "localhost:50051"


def _request(method: str, url: str, token: str = "", data: dict = None) -> dict:
    """HTTP リクエスト"""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, headers=headers, method=method)
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        print(f"Error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def cmd_version(_args):
    """バージョン表示"""
    print(f"uep-cli v{VERSION} (UEP v5.0)")


def cmd_health(args):
    """API ヘルスチェック"""
    url = f"{args.url}/api/v1/health"
    result = _request("GET", url, args.token)
    if args.output == "table":
        for k, v in result.items():
            print(f"{k:<15} {v}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    print("OK: Backend is healthy")


def cmd_events_list(args):
    """トピック一覧取得"""
    url = f"{args.url}/api/v1/events/topics"
    result = _request("GET", url, args.token)
    _print_output(result, args.output)


def cmd_events_outbox(args):
    """未公開アウトボックス一覧"""
    url = f"{args.url}/api/v1/events/outbox/unpublished"
    result = _request("GET", url, args.token)
    _print_output(result, args.output)


def _print_output(data, fmt: str):
    if fmt == "table" and isinstance(data, dict):
        for k, v in data.items():
            print(f"{k}: {v}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_grpc_status(args):
    """gRPC 疎通確認（TCP 接続テスト）"""
    host, _, port_str = args.addr.rpartition(":")
    port = int(port_str or "50051") if port_str else 50051
    try:
        with socket.create_connection((host or "localhost", port), timeout=5):
            if args.output == "table":
                print(f"{'Address':<20} {args.addr}")
                print(f"{'Status':<20} connected")
            else:
                print(json.dumps({"address": args.addr, "status": "connected", "message": "gRPC service reachable"}))
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        print(f"Error: gRPC connection failed - {e}", file=sys.stderr)
        sys.exit(1)


def cmd_graphql_query(args):
    """GraphQL クエリ実行"""
    query = args.query or "{ hello health { status version } }"
    url = f"{args.url}/graphql"
    result = _request("POST", url, args.token, {"query": query})
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(prog="uep-cli", description="UEP v5.0 CLI（Python版）")
    parser.add_argument("-u", "--url", default=DEFAULT_API_URL, help="API base URL")
    parser.add_argument("-t", "--token", default="", help="JWT token")
    parser.add_argument("-o", "--output", choices=["json", "table"], default="json", help="Output format")

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("version", help="バージョン表示")

    health_p = sub.add_parser("health", help="API ヘルスチェック")
    health_p.set_defaults(func=cmd_health)

    events_p = sub.add_parser("events", help="イベント操作")
    events_sub = events_p.add_subparsers(dest="events_cmd", required=True)
    el = events_sub.add_parser("list", help="トピック一覧")
    el.set_defaults(func=cmd_events_list)
    eo = events_sub.add_parser("outbox", help="未公開アウトボックス一覧")
    eo.set_defaults(func=cmd_events_outbox)

    grpc_p = sub.add_parser("grpc", help="gRPC 操作")
    grpc_sub = grpc_p.add_subparsers(dest="grpc_cmd", required=True)
    gs = grpc_sub.add_parser("status", help="gRPC 疎通確認")
    gs.add_argument("-a", "--addr", default=DEFAULT_GRPC_ADDR, help="gRPC address")
    gs.set_defaults(func=cmd_grpc_status)

    gql_p = sub.add_parser("graphql", help="GraphQL 操作")
    gql_sub = gql_p.add_subparsers(dest="graphql_cmd", required=True)
    gq = gql_sub.add_parser("query", help="GraphQL クエリ実行")
    gq.add_argument("-q", "--query", default="", help="GraphQL query")
    gq.set_defaults(func=cmd_graphql_query)

    args = parser.parse_args()

    if args.cmd == "version":
        cmd_version(args)
        return

    # events / grpc / graphql はサブコマンドで func が設定される
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
