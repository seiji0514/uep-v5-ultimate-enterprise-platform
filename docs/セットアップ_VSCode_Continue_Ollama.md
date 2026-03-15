# VS Code + Continue.dev + Ollama セットアップガイド

**完全無料**でAIコーディングアシスタントを使用するための手順です。

---

## 前提条件

- **RAM**: 8GB以上（16GB推奨）
- **ストレージ**: 10GB以上の空き
- **OS**: Windows 10/11

---

## ステップ1: Ollama のインストール

### 1-1. ダウンロード・インストール

1. [ollama.ai](https://ollama.ai) にアクセス
2. **Download for Windows** をクリック
3. インストーラーを実行（OllamaSetup.exe）
4. インストール完了後、Ollama がバックグラウンドで起動します

### 1-2. モデルのダウンロード

PowerShell または コマンドプロンプトで実行:

```powershell
# 軽量・おすすめ（約4GB）
ollama pull deepseek-coder:6.7b

# または より高品質（約7GB）
ollama pull qwen2.5-coder:7b

# 動作確認
ollama list
```

**おすすめモデル一覧:**

| モデル | コマンド | サイズ | 用途 |
|--------|----------|--------|------|
| DeepSeek Coder | `ollama pull deepseek-coder:6.7b` | 約4GB | 軽量・補完 |
| DeepSeek Coder 2 Lite | `ollama pull deepseek-coder-v2:lite` | 約9GB | 高品質・推奨 |
| Qwen 2.5 Coder | `ollama pull qwen2.5-coder:7b` | 約5GB | バランス |
| Code Llama | `ollama pull codellama:7b` | 約4GB | コード補完 |
| Codestral | `ollama pull codestral` | 約13GB | 高品質（VRAM多め） |

---

## ステップ2: VS Code のインストール

1. [code.visualstudio.com](https://code.visualstudio.com/) からダウンロード
2. インストール実行
3. 既にインストール済みの場合はスキップ

---

## ステップ3: Continue 拡張機能のインストール

1. VS Code を起動
2. **Ctrl+Shift+X** で拡張機能パネルを開く
3. 「**Continue**」で検索
4. **Continue**（作者: Continue.dev）をインストール
5. インストール後、VS Code を再起動

**または コマンドで:**
```powershell
code --install-extension Continue.continue
```

---

## ステップ4: Continue の設定（Ollama連携）

### 方法A: 自動検出（推奨）

1. **Ctrl+Shift+P** → 「Continue: Open config」と入力
2. 設定ファイルが開いたら、以下を追加または確認:

```yaml
name: My Config
version: 0.0.1
schema: v1

models:
  - name: DeepSeek Coder
    provider: ollama
    model: deepseek-coder:6.7b
    apiBase: http://localhost:11434
```

### 方法B: プロジェクト用テンプレート

プロジェクトの `.continue/config.yaml` が既に用意されています。VS Code でこのプロジェクトを開くと自動で読み込まれます。

### 設定ファイルの場所（Windows）

- ユーザー設定: `C:\Users\<ユーザー名>\.continue\config.yaml`
- プロジェクト: `<プロジェクトルート>\.continue\config.yaml`

---

## ステップ5: 動作確認

1. VS Code でプロジェクトを開く
2. **Ctrl+L** で Continue チャットを開く
3. 「このファイルの概要を説明して」などと入力
4. 応答が返ればOK

---

## トラブルシューティング

### Ollama が起動しない

```powershell
# 手動起動
ollama serve
```

### モデルが見つからない

```powershell
ollama list
# 一覧に表示されないモデルは pull する
ollama pull deepseek-coder:6.7b
```

### Continue が応答しない

1. Ollama が起動しているか確認（タスクマネージャーで「Ollama」を検索）
2. `http://localhost:11434` にブラウザでアクセス → 「Ollama is running」と表示されればOK
3. Continue の設定で `apiBase: http://localhost:11434` を確認

### メモリ不足

- より小さいモデルを試す: `ollama pull qwen2.5-coder:1.5b`
- 他のアプリを閉じてRAMを確保

---

## Cursor からの移行メモ

- **移行チェックリスト**: `docs/CursorからVSCode移行チェックリスト.md` を参照
- **ルール・プロンプト**: Cursor の `.cursorrules` や `AGENT_INSTRUCTIONS.md` の内容は、`.continue/config.yaml` の `systemMessage` に転記済み
- **ショートカット**: Continue は **Ctrl+L** でチャット、**Ctrl+I** でインライン編集
- **コンテキスト**: @ でファイルやフォルダを参照可能

---

## 参考リンク

- [Ollama](https://ollama.ai)
- [Continue.dev ドキュメント](https://docs.continue.dev)
- [Continue + Ollama ガイド](https://docs.continue.dev/guides/ollama-guide)
