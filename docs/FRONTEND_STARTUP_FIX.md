# フロントエンド起動エラーの解決方法

**作成日**: 2026年2月11日  
**問題**: `start-all.bat`でフロントエンドが起動できない

---

## 🔍 問題の確認

### エラーメッセージ

画像から確認できるエラー：
- `'e_frontend!"=="Y" ('` が認識されない
- `'js.org'` が認識されない

### 原因

1. **文字エンコーディングの問題**: バッチファイルの文字エンコーディングが正しくない
2. **バッチファイルの構文エラー**: `if`文の比較演算子が正しく解釈されていない

---

## ✅ 解決方法

### 方法1: 修正済みのバッチファイルを使用（推奨）

`start-frontend.bat`を修正しました。以下の手順で再試行してください：

1. **既存のプロセスを停止**
   ```cmd
   stop-all.bat
   ```
   または、各ウィンドウで `Ctrl+C` を押す

2. **フロントエンドを直接起動**
   ```cmd
   start-frontend.bat
   ```

3. **または、一括起動を再試行**
   ```cmd
   start-all.bat
   ```

---

### 方法2: 手動でフロントエンドを起動

バッチファイルに問題がある場合、以下の手順で手動で起動できます：

#### ステップ1: フロントエンドディレクトリに移動

```cmd
cd c:\uep-v5-ultimate-enterprise-platform\frontend
```

#### ステップ2: Node.jsとnpmの確認

```cmd
node --version
npm --version
```

**期待される出力**:
- Node.js: `v18以上` または `v22.14.0`（現在のバージョン）
- npm: `9以上` または `11.3.0`（現在のバージョン）

#### ステップ3: 依存パッケージのインストール（必要に応じて）

```cmd
npm install
```

**注意**: これには数分かかる場合があります

#### ステップ4: フロントエンドの起動

```cmd
npm start
```

**期待される動作**:
- ブラウザが自動的に開き、`http://localhost:3000` にアクセス
- または、手動で `http://localhost:3000` にアクセス

---

### 方法3: 新しいコマンドプロンプトで起動

`start-all.bat`から起動できない場合、新しいコマンドプロンプトで直接起動：

1. **新しいコマンドプロンプトを開く**
   - `Win + R` → `cmd` → Enter

2. **プロジェクトディレクトリに移動**
   ```cmd
   cd c:\uep-v5-ultimate-enterprise-platform
   ```

3. **フロントエンドを起動**
   ```cmd
   start-frontend.bat
   ```

---

## 🔧 トラブルシューティング

### 問題1: ポート3000が既に使用されている

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

### 問題2: 依存パッケージのインストールエラー

**症状**: `npm install`が失敗する

**解決方法**:
1. `node_modules`フォルダを削除:
   ```cmd
   cd c:\uep-v5-ultimate-enterprise-platform\frontend
   rmdir /s /q node_modules
   ```
2. `package-lock.json`を削除（オプション）:
   ```cmd
   del package-lock.json
   ```
3. 依存パッケージを再インストール:
   ```cmd
   npm install
   ```

---

### 問題3: Node.jsやnpmが認識されない

**症状**: `node --version`や`npm --version`がエラーになる

**解決方法**:
1. Node.jsがインストールされているか確認:
   - スタートメニューで「Node.js」を検索
   - または、`C:\Program Files\nodejs\`に存在するか確認

2. 環境変数PATHを確認:
   ```cmd
   echo %PATH%
   ```
   - `C:\Program Files\nodejs\`が含まれているか確認

3. Node.jsを再インストール:
   - https://nodejs.org/ から最新版をダウンロード
   - インストール時に「Add to PATH」オプションを選択

---

### 問題4: バッチファイルの文字エンコーディングエラー

**症状**: `'e_frontend!"=="Y" ('` などのエラーが表示される

**解決方法**:
1. `start-frontend.bat`を修正済みのバージョンに置き換える（既に修正済み）
2. または、手動でフロントエンドを起動（方法2を参照）

---

## 📋 確認チェックリスト

フロントエンドを起動する前に、以下を確認してください：

- [ ] Node.jsがインストールされている（`node --version`で確認）
- [ ] npmがインストールされている（`npm --version`で確認）
- [ ] フロントエンドディレクトリが存在する（`c:\uep-v5-ultimate-enterprise-platform\frontend`）
- [ ] `package.json`が存在する（`frontend\package.json`）
- [ ] ポート3000が使用されていない（必要に応じて確認）
- [ ] インターネット接続がある（`npm install`が必要な場合）

---

## 💡 推奨される起動手順（面談用）

### 事前準備（面談前日までに）

1. **環境確認**
   ```cmd
   node --version
   npm --version
   ```

2. **フロントエンドの起動確認**
   ```cmd
   cd c:\uep-v5-ultimate-enterprise-platform\frontend
   npm install
   npm start
   ```

3. **動作確認**
   - `http://localhost:3000` にアクセス
   - ログイン画面が表示されることを確認

### 面談当日

1. **バックエンドを起動**（既に起動済み）
   ```cmd
   start-backend.bat
   ```

2. **フロントエンドを起動**（新しいコマンドプロンプトで）
   ```cmd
   cd c:\uep-v5-ultimate-enterprise-platform\frontend
   npm start
   ```

3. **または、修正済みのバッチファイルを使用**
   ```cmd
   start-frontend.bat
   ```

---

## 🚨 緊急時の対応（面談中にエラーが発生した場合）

### フロントエンドが起動しない場合

1. **Swagger UIでAPIを実演**
   - `http://localhost:8000/docs` を開く
   - APIの動作を実演
   - 「フロントエンドの起動に問題が発生しましたが、バックエンドAPIの動作をご確認いただけます」と説明

2. **事前に準備したスクリーンショットを共有**
   - フロントエンドの画面のスクリーンショットを準備しておく
   - 必要に応じて共有

3. **コードを直接共有**
   - `frontend/src/App.tsx` などの主要なコードファイルを開く
   - コードの説明を行う

---

## 📝 修正内容の詳細

### `start-frontend.bat`の修正点

1. **`if`文の比較演算子を修正**
   - 変更前: `if /i "!create_frontend!"=="Y" (`
   - 変更後: `if /i "!create_frontend!" EQU "Y" (`
   - 理由: `EQU`を使用することで、文字エンコーディングの問題を回避

2. **URLの表示方法を修正**
   - 変更前: `echo Node.jsをインストールしてください: https://nodejs.org/`
   - 変更後: 
     ```
     echo Node.jsをインストールしてください
     echo URL: https://nodejs.org/
     ```
   - 理由: URLを別の行に分けることで、誤った解釈を回避

---

## ✅ 動作確認

修正後、以下の手順で動作確認してください：

1. **バッチファイルを直接実行**
   ```cmd
   cd c:\uep-v5-ultimate-enterprise-platform
   start-frontend.bat
   ```

2. **期待される動作**:
   - Node.jsとnpmのバージョンが表示される
   - 依存パッケージがインストールされる（必要に応じて）
   - フロントエンドが起動し、`http://localhost:3000` にアクセスできる

3. **エラーメッセージがないことを確認**

---

## 💡 まとめ

### 推奨される解決方法

1. **修正済みのバッチファイルを使用**（方法1）
2. **手動でフロントエンドを起動**（方法2）
3. **新しいコマンドプロンプトで起動**（方法3）

### 面談時の推奨手順

1. **事前にフロントエンドの起動を確認**
2. **面談当日は、バックエンドとフロントエンドを個別に起動**
3. **トラブル時は、Swagger UIでAPIを実演**

---

以上
