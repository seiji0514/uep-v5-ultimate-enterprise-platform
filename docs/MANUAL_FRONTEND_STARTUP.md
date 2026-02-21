# フロントエンド手動起動手順

**作成日**: 2026年2月11日  
**目的**: フロントエンドを手動で起動する手順と、Reactエラーの解決方法

---

## 🚀 手動起動手順

### ステップ1: コマンドプロンプトを開く

1. **Windowsキー + R**を押す
2. `cmd`と入力してEnter
3. または、スタートメニューで「コマンドプロンプト」を検索

---

### ステップ2: プロジェクトディレクトリに移動

```cmd
cd c:\uep-v5-ultimate-enterprise-platform
```

---

### ステップ3: フロントエンドディレクトリに移動

```cmd
cd frontend
```

---

### ステップ4: Node.jsとnpmの確認

```cmd
node --version
npm --version
```

**期待される出力**:
- Node.js: `v18以上` または `v22.14.0`
- npm: `9以上` または `11.3.0`

**エラーが出る場合**:
- Node.jsがインストールされていない可能性があります
- https://nodejs.org/ からインストールしてください

---

### ステップ5: 依存パッケージのインストール（初回のみ、または必要に応じて）

```cmd
npm install
```

**注意**: 
- これには数分かかる場合があります
- インターネット接続が必要です
- 既に`node_modules`フォルダが存在する場合は、このステップはスキップできます

---

### ステップ6: フロントエンドの起動

```cmd
npm start
```

**期待される動作**:
- コンパイルが開始されます
- 「Compiled successfully!」と表示されます
- ブラウザが自動的に開き、`http://localhost:3000`にアクセスします
- または、手動で`http://localhost:3000`にアクセスします

---

### ステップ7: 動作確認

1. **ブラウザで`http://localhost:3000`にアクセス**
2. **ログイン画面が表示されることを確認**
3. **ログイン情報を入力**:
   - ユーザー名: `kaho0525`
   - パスワード: `kaho052514`
4. **ログインが成功することを確認**

---

## ⚠️ Reactエラーの解決方法

### 問題: `removeChild`エラーが発生する

**症状**:
```
NotFoundError: 'Node' で 'removeChild' を実行できませんでした: 削除するノードはこのノードの子ではありません。
```

**原因**:
- ReactのDOM操作に関するエラー
- ナビゲーション時のタイミング問題
- ブラウザのキャッシュの問題

---

### 解決方法1: ブラウザのキャッシュをクリア

1. **ブラウザの開発者ツールを開く**
   - `F12`キーを押す
   - または、右クリック → 「検証」

2. **ネットワークタブを開く**
   - 「Disable cache」にチェックを入れる
   - または、`Ctrl + Shift + Delete`でキャッシュをクリア

3. **ページを再読み込み**
   - `Ctrl + Shift + R`（強制リロード）
   - または、`Ctrl + F5`

---

### 解決方法2: フロントエンドを再起動

1. **フロントエンドを停止**
   - コマンドプロンプトで`Ctrl + C`を押す

2. **`node_modules`を削除（オプション）**
   ```cmd
   rmdir /s /q node_modules
   ```

3. **依存パッケージを再インストール**
   ```cmd
   npm install
   ```

4. **フロントエンドを再起動**
   ```cmd
   npm start
   ```

---

### 解決方法3: ブラウザを変更

1. **別のブラウザで試す**
   - Chrome → Edge
   - Edge → Chrome
   - Firefox

2. **シークレットモード（プライベートモード）で試す**
   - Chrome: `Ctrl + Shift + N`
   - Edge: `Ctrl + Shift + P`
   - Firefox: `Ctrl + Shift + P`

---

### 解決方法4: ポートを変更

ポート3000が使用されている場合、別のポートで起動：

```cmd
set PORT=3001
npm start
```

その後、`http://localhost:3001`にアクセス

---

## 📋 完全な手動起動手順（まとめ）

### 初回セットアップ

```cmd
cd c:\uep-v5-ultimate-enterprise-platform\frontend
node --version
npm --version
npm install
npm start
```

### 2回目以降

```cmd
cd c:\uep-v5-ultimate-enterprise-platform\frontend
npm start
```

---

## 🔧 トラブルシューティング

### 問題1: `npm install`が失敗する

**解決方法**:
1. インターネット接続を確認
2. プロキシ設定を確認（会社のネットワークの場合）
3. `npm cache clean --force`を実行してから再試行

---

### 問題2: ポート3000が使用されている

**症状**: `npm start`を実行すると、ポート3000が使用中というエラーが表示される

**解決方法**:
1. ポート3000を使用しているプロセスを確認:
   ```cmd
   netstat -ano | findstr :3000
   ```
2. プロセスを終了:
   ```cmd
   taskkill /PID <プロセスID> /F
   ```
3. または、別のポートで起動:
   ```cmd
   set PORT=3001
   npm start
   ```

---

### 問題3: コンパイルエラーが発生する

**症状**: `npm start`を実行すると、TypeScriptのエラーが表示される

**解決方法**:
1. エラーメッセージを確認
2. 該当するファイルを修正
3. フロントエンドを再起動

---

### 問題4: ブラウザが自動的に開かない

**解決方法**:
1. 手動で`http://localhost:3000`にアクセス
2. または、コマンドプロンプトに表示されているURLを確認

---

## 💡 面談時の推奨手順

### 事前準備（面談前日までに）

1. **フロントエンドの起動確認**
   ```cmd
   cd c:\uep-v5-ultimate-enterprise-platform\frontend
   npm start
   ```

2. **動作確認**
   - `http://localhost:3000`にアクセス
   - ログイン画面が表示されることを確認
   - ログインが成功することを確認

3. **エラーが発生する場合**
   - ブラウザのキャッシュをクリア
   - フロントエンドを再起動
   - 別のブラウザで試す

---

### 面談当日

1. **バックエンドを起動**（既に起動済み）
   - `http://localhost:8000`で動作確認

2. **フロントエンドを起動**（新しいコマンドプロンプトで）
   ```cmd
   cd c:\uep-v5-ultimate-enterprise-platform\frontend
   npm start
   ```

3. **動作確認**
   - `http://localhost:3000`にアクセス
   - ログイン画面が表示されることを確認

4. **エラーが発生する場合**
   - ブラウザのキャッシュをクリア（`Ctrl + Shift + R`）
   - Swagger UIでAPIを実演（`http://localhost:8000/docs`）

---

## 🚨 緊急時の対応（面談中にエラーが発生した場合）

### フロントエンドが起動しない、またはエラーが発生する場合

1. **Swagger UIでAPIを実演**
   - `http://localhost:8000/docs`を開く
   - APIの動作を実演
   - 「フロントエンドの起動に問題が発生しましたが、バックエンドAPIの動作をご確認いただけます」と説明

2. **事前に準備したスクリーンショットを共有**
   - フロントエンドの画面のスクリーンショットを準備しておく
   - 必要に応じて共有

3. **コードを直接共有**
   - `frontend/src/App.tsx`などの主要なコードファイルを開く
   - コードの説明を行う

---

## ✅ 確認チェックリスト

フロントエンドを起動する前に、以下を確認してください：

- [ ] Node.jsがインストールされている（`node --version`で確認）
- [ ] npmがインストールされている（`npm --version`で確認）
- [ ] フロントエンドディレクトリが存在する（`c:\uep-v5-ultimate-enterprise-platform\frontend`）
- [ ] `package.json`が存在する（`frontend\package.json`）
- [ ] ポート3000が使用されていない（必要に応じて確認）
- [ ] インターネット接続がある（`npm install`が必要な場合）
- [ ] ブラウザのキャッシュをクリア済み（エラーが発生する場合）

---

## 📝 コマンド一覧（コピー&ペースト用）

### 初回セットアップ

```cmd
cd c:\uep-v5-ultimate-enterprise-platform\frontend
node --version
npm --version
npm install
npm start
```

### 2回目以降

```cmd
cd c:\uep-v5-ultimate-enterprise-platform\frontend
npm start
```

### トラブル時（再インストール）

```cmd
cd c:\uep-v5-ultimate-enterprise-platform\frontend
rmdir /s /q node_modules
npm install
npm start
```

### 別のポートで起動

```cmd
cd c:\uep-v5-ultimate-enterprise-platform\frontend
set PORT=3001
npm start
```

---

## 💡 まとめ

### 基本的な起動手順

1. **コマンドプロンプトを開く**
2. **プロジェクトディレクトリに移動**: `cd c:\uep-v5-ultimate-enterprise-platform\frontend`
3. **フロントエンドを起動**: `npm start`
4. **ブラウザで確認**: `http://localhost:3000`

### エラーが発生する場合

1. **ブラウザのキャッシュをクリア**（`Ctrl + Shift + R`）
2. **フロントエンドを再起動**
3. **別のブラウザで試す**
4. **Swagger UIでAPIを実演**（緊急時）

---

以上
