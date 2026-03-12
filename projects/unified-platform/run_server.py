#!/usr/bin/env python3
"""
本番バックエンド起動（PostgreSQL + Redis）
環境変数を先に設定してから uvicorn を起動する
"""
import os

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "50000"))
    host = os.environ.get("HOST", "0.0.0.0")
    print("バックエンド起動中（PostgreSQL + Redis）...")
    print(f"http://localhost:{port}/health で確認")
    print("ログイン: kaho0525 / 0525")
    print()
    uvicorn.run("main:app", host=host, port=port)
