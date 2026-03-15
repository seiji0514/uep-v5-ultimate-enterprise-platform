# Sentry アラート - Slack 以外の設定

Sentry の障害通知は **Slack 以外** でも設定可能です。

---

## 利用可能な通知先

| 通知先 | 設定方法 |
|--------|----------|
| **Email** | Sentry プロジェクト設定 → Alerts → メールアドレスを追加 |
| **Webhook** | Sentry → Settings → Integrations → Webhook。任意の URL に POST |
| **Discord** | Webhook で Discord の Incoming Webhook URL を指定 |
| **Microsoft Teams** | Sentry → Integrations → Microsoft Teams |
| **PagerDuty** | Sentry → Integrations → PagerDuty |

---

## 設定手順（例: Email）

1. [sentry.io](https://sentry.io) にログイン
2. プロジェクト選択 → **Settings** → **Alerts**
3. **Add Member** で通知先のメールアドレスを追加
4. アラートルールで「メール送信」を有効化

---

## 設定手順（例: Discord Webhook）

1. Discord で サーバー設定 → 連携サービス → Webhook を作成
2. Webhook URL をコピー
3. Sentry → Settings → Integrations → **Webhooks** を有効化
4. Webhook URL に Discord の URL を設定

---

## 参考

- [Sentry Alerts](https://docs.sentry.io/product/alerts/)
- [Sentry Integrations](https://docs.sentry.io/product/integrations/)
