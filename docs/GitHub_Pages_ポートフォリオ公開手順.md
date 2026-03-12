# GitHub Pages で汎用ポートフォリオを公開する手順

## 対象ファイル

- `docs/ポートフォリオ_汎用.html`
- `docs/portfolio_images/`（01_login.png ～ 04_inclusive.png）

---

## 手順

### 1. ファイルをコミット・プッシュ

```bash
git add docs/ポートフォリオ_汎用.html docs/portfolio_images/
git commit -m "Add generic portfolio for GitHub Pages"
git push origin main
```

※ブランチ名が `master` の場合は `main` を `master` に置き換えてください。

---

### 2. GitHub Pages を有効化

1. GitHub でリポジトリを開く
2. **Settings** → 左メニュー **Pages**
3. **Source**: **Deploy from a branch** を選択
4. **Branch**: `main`（または `master`）を選択
5. **Folder**: **/docs** を選択
6. **Save** をクリック

---

### 3. 公開 URL

数分待つと、次の URL でアクセスできます。

```
https://<ユーザー名>.github.io/<リポジトリ名>/ポートフォリオ_汎用.html
```

**例**（リポジトリ名が `uep-v5-ultimate-enterprise-platform` の場合）:

```
https://<ユーザー名>.github.io/uep-v5-ultimate-enterprise-platform/ポートフォリオ_汎用.html
```

---

### 4. Wantedly への登録

公開できたら、上記 URL を Wantedly プロフィールの「リンク」欄に登録してください。

---

## 注意点

| 項目 | 内容 |
|------|------|
| **画像** | `portfolio_images/` は `docs/` 内に配置済み。HTML の相対パスでそのまま表示されます。 |
| **日本語ファイル名** | 問題なく利用できます。 |
| **初回反映** | 有効化後、1〜3分ほどかかることがあります。 |
