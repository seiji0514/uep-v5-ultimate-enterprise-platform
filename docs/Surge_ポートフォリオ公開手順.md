# Surge.sh でポートフォリオを公開する手順

## 概要

Surge はコマンド1つで静的サイトをデプロイできるサービスです。無料で利用でき、Node.js が入っていればすぐに使えます。

---

## 前提条件

- **Node.js** がインストールされていること（[nodejs.org](https://nodejs.org) から取得）
- ターミナル（PowerShell または コマンドプロンプト）が使えること

---

## 手順

### 1. Surge をインストール

```bash
npm install -g surge
```

---

### 2. デプロイ用フォルダに移動

```bash
cd c:\uep-v5-ultimate-enterprise-platform\docs
```

※`docs/` には `ポートフォリオ_汎用.html` と `portfolio_images/` が含まれています。

---

### 3. デプロイ実行

**推奨**: パスとドメインを一度に指定して実行（プロンプトの混同を防げます）:

```bash
surge . ogawa-portfolio.surge.sh
```

- `.` = カレント（docs）フォルダをデプロイ
- `ogawa-portfolio.surge.sh` = 公開するドメイン

**初回のみ**、メールアドレスとパスワードの入力を求められます（無料登録）。

---

### 4. 対話形式で実行する場合

`surge` のみで実行する場合:

- **「project path」** と聞かれたら → `.` または `.\` と入力（カレントフォルダ）
- **「domain」** と聞かれたら → `ogawa-portfolio.surge.sh` と入力

※「domain」を「project path」に入力してしまうとエラーになります。

---

### 5. 公開 URL

デプロイ後、次の URL でアクセスできます:

```
https://ogawa-portfolio.surge.sh/ポートフォリオ_汎用.html
```

※日本語ファイル名は URL エンコードされますが、リンクは正常に動作します。

---

### 6. トップページをポートフォリオにする場合（任意）

`docs/index.html` として `ポートフォリオ_汎用.html` をコピーする場合:

```bash
copy ポートフォリオ_汎用.html index.html
surge
```

この場合、`https://ogawa-portfolio.surge.sh/` でアクセスできます。

---

## 再デプロイ（更新時）

```bash
cd c:\uep-v5-ultimate-enterprise-platform\docs
surge
```

同じドメインを指定すれば、同じ URL で上書きされます。

---

## Wantedly への登録

公開できたら、次の URL を Wantedly プロフィールの「リンク」欄に登録してください。

```
https://ogawa-portfolio.surge.sh/ポートフォリオ_汎用.html
```

※`ogawa-portfolio` は実際に指定したドメイン名に置き換えてください。

---

## 注意点

| 項目 | 内容 |
|------|------|
| **無料** | 個人利用は無料 |
| **HTTPS** | 自動で HTTPS が有効になります |
| **画像** | `portfolio_images/` は `docs/` 内にあるため、そのままデプロイされます |
| **カスタムドメイン** | 有料プランで利用可能 |
