"""
UEP v5.0 負荷テスト - Locust
技術深化: パフォーマンス検証

実行方法:
  locust -f scripts/load_test_locust.py --host=http://localhost:8000

ブラウザで http://localhost:8089 を開き、ユーザー数・スパウンレートを設定して実行。
"""
import os
from locust import HttpUser, task, between


class UEPLoadTestUser(HttpUser):
    """UEP v5.0 API 負荷テスト用ユーザー"""
    wait_time = between(0.5, 1.5)  # リクエスト間隔（秒）

    def on_start(self):
        """ログインしてトークンを取得"""
        try:
            res = self.client.post(
                "/api/v1/auth/login",
                json={"username": "developer", "password": "dev123"},
                name="/api/v1/auth/login"
            )
            if res.status_code == 200:
                data = res.json()
                self.token = data.get("access_token")
            else:
                self.token = None
        except Exception:
            self.token = None

    @task(3)
    def health_check(self):
        """ルート（ヘルスチェック）"""
        self.client.get("/", name="/")

    @task(2)
    def api_docs(self):
        """API ドキュメント"""
        self.client.get("/docs", name="/docs")

    @task(2)
    def openapi_json(self):
        """OpenAPI スキーマ"""
        self.client.get("/openapi.json", name="/openapi.json")

    @task(1)
    def auth_login(self):
        """ログイン（認証なしでアクセス可能）"""
        self.client.post(
            "/api/v1/auth/login",
            json={"username": "developer", "password": "dev123"},
            name="/api/v1/auth/login"
        )

    @task(2)
    def auth_me(self):
        """認証済みエンドポイント /me"""
        if self.token:
            self.client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {self.token}"},
                name="/api/v1/auth/me"
            )

    @task(1)
    def monitoring_metrics(self):
        """Prometheus メトリクス"""
        self.client.get("/metrics", name="/metrics")


if __name__ == "__main__":
    os.environ.setdefault("LOCUST_HOST", "http://localhost:8000")
