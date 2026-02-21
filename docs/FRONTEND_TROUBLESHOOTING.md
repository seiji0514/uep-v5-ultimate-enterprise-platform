# フロントエンド トラブルシューティングガイド

**作成日**: 2026年1月30日

---

## start-frontend.batが開かない/すぐに閉じる

### 問題の症状

- `start-frontend.bat`をダブルクリックしても何も表示されない
- コマンドプロンプトが一瞬表示されてすぐに閉じる
- エラーメッセージが表示されない

### 解決方法

#### 方法1: コマンドプロンプトから実行

1. **コマンドプロンプトを開く**
   - Windowsキー + R
   - `cmd`と入力してEnter

2. **プロジェクトディレクトリに移動**
   ```cmd
   cd C:\uep-v5-ultimate-enterprise-platform
   ```

3. **スクリプトを実行**
   ```cmd
   start-frontend.bat
   ```

これで、エラーメッセージが表示され、問題を特定できます。

#### 方法2: 手動で起動

1. **コマンドプロンプトを開く**

2. **フロントエンドディレクトリに移動**
   ```cmd
   cd C:\uep-v5-ultimate-enterprise-platform\frontend
   ```

3. **依存関係を確認**
   ```cmd
   npm --version
   node --version
   ```

4. **依存関係をインストール（必要に応じて）**
   ```cmd
   npm install
   ```

5. **フロントエンドを起動**
   ```cmd
   npm start
   ```

---

## よくあるエラーと解決方法

### エラー1: Node.jsがインストールされていない

**症状:**
```
エラー: Node.jsがインストールされていません
```

**解決方法:**
1. Node.jsをインストール: https://nodejs.org/
2. インストール後、コマンドプロンプトを再起動
3. `node --version`で確認

### エラー2: npmがインストールされていない

**症状:**
```
エラー: npmがインストールされていません
```

**解決方法:**
- Node.jsをインストールすると、npmも一緒にインストールされます
- `npm --version`で確認

### エラー3: 依存パッケージのインストールに失敗

**症状:**
```
エラー: 依存パッケージのインストールに失敗しました
```

**解決方法:**
1. インターネット接続を確認
2. プロキシ設定を確認（企業ネットワークの場合）
3. キャッシュをクリア:
   ```cmd
   npm cache clean --force
   ```
4. 再インストール:
   ```cmd
   cd frontend
   rmdir /s /q node_modules
   del package-lock.json
   npm install
   ```

### エラー4: ポート3000が使用中

**症状:**
```
Error: listen EADDRINUSE: address already in use :::3000
```

**解決方法:**
1. 既存のプロセスを終了:
   ```cmd
   netstat -ano | findstr :3000
   taskkill /PID <PID番号> /F
   ```
2. または、別のポートを使用:
   ```cmd
   set PORT=3001
   npm start
   ```

### エラー5: package.jsonが見つからない

**症状:**
```
エラー: package.jsonが見つかりません
```

**解決方法:**
1. `frontend`ディレクトリが存在するか確認
2. `frontend\package.json`が存在するか確認
3. 存在しない場合は、フロントエンドを再作成

---

## デバッグ方法

### ステップ1: 基本確認

```cmd
cd C:\uep-v5-ultimate-enterprise-platform\frontend
dir
```

以下のファイルが存在するか確認:
- `package.json`
- `src\App.tsx`
- `node_modules`（インストール後）

### ステップ2: Node.jsとnpmの確認

```cmd
node --version
npm --version
```

### ステップ3: 依存関係の確認

```cmd
cd frontend
npm list --depth=0
```

### ステップ4: 手動起動

```cmd
cd frontend
npm start
```

---

## スクリプトの改善

`start-frontend.bat`は以下の改善が行われています:

1. ✅ エラーハンドリングの強化
2. ✅ 詳細なエラーメッセージ
3. ✅ 各ステップでの確認
4. ✅ `pause`コマンドでウィンドウが閉じないように

---

## サポート

問題が解決しない場合:

1. コマンドプロンプトから実行してエラーメッセージを確認
2. `docs/FRONTEND_IMPLEMENTATION.md`を参照
3. `docs/FRONTEND_SECURITY.md`を参照

---

以上
