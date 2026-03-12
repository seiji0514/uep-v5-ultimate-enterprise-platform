# 株式会社SEZO 書類送付手順

作成日: 2026年2月21日

---

## 面接情報（SEZO返信より）

| 項目 | 内容 |
|------|------|
| **日時** | 2月23日（月）10:00〜 |
| **形式** | Google Meet |
| **URL** | https://meet.google.com/cau.qad1.ish |

---

## 添付する書類一覧

| 書類 | ファイル | 備考 |
|------|----------|------|
| 職務経歴書 | `職務経歴書_株式会社SEZO_インフラエンジニア_小川清志.md` | PDFに変換して送付 |
| 履歴書 | （JIS形式の履歴書） | 志望動機は `履歴書_志望動機_SEZO.md` を参照 |
| 障害説明書 | `障害説明書_株式会社SEZO_インフラエンジニア_小川清志.md` | PDFに変換して送付（任意） |

---

## 送付先（SEZO返信で指定）

- **宛先**: **sang@sezo.co.jp**
- **送付書類**: 職務経歴書・履歴書（障害説明書も同封可）

---

## PDF変換の方法

### 方法1: VS Code / Cursor
- Markdown を開き、右クリック → 「Markdown PDF」拡張機能でエクスポート（拡張機能が必要）

### 方法2: オンラインツール
- https://www.markdowntopdf.com/ 等で .md を PDF に変換

### 方法3: Word経由
- .md を Word に貼り付け → 名前を付けて保存 → PDF で保存

---

## 履歴書について

履歴書は JIS 形式（市販の履歴書用紙またはテンプレート）を使用してください。
志望動機欄には `履歴書_志望動機_SEZO.md` の「履歴書用（短め）」の内容を記入してください。

---

## 送付時のメール件名例

```
【書類送付】小川清志・インフラエンジニア応募書類（2月23日10:00面談予定）
```

---

## 面談当日のデモ起動手順

### 方法A: ローカル起動（推奨・安定）

**ステップ1: システムの起動（面談開始5分前）**

| 順番 | 操作 |
|------|------|
| 1 | バックエンド: `start-backend.bat` を実行 |
| 2 | フロントエンド: `cd frontend` → `npm start`（初回は `npm install` を先に実行） |

**ステップ2: ブラウザの準備**

| URL | 用途 |
|-----|------|
| http://localhost:3000 | フロントエンド（ログイン・デモ） |
| http://localhost:8000/docs または http://localhost:8001/docs | Swagger UI |
| http://localhost:8000/health または http://localhost:8001/health | ヘルスチェック |

※ ポート8000が使用中の場合は8001で起動されます。

---

### 方法B: クラウド起動（起動不要・事前にRenderを起こす）

**ステップ1: 面談開始5分前にRenderを起こす**

1. ブラウザで `https://uep-backend-9m5v.onrender.com/health` にアクセス
2. 50秒〜1分待つ（起動完了まで）
3. JSON が表示されればOK

**ステップ2: デモ用URL**

| URL | 用途 |
|-----|------|
| https://uep-v5-ultimate-enterprise-platform.vercel.app | フロントエンド（ログイン・デモ） |
| https://uep-backend-9m5v.onrender.com/docs | Swagger UI |

**ログイン**: kaho0525 / kaho052514 または developer / dev123

---

以上
