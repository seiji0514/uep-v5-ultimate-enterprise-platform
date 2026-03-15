# Cursor → VS Code + Continue 移行チェックリスト

**対象期間**: 3/18 23:00 まで Cursor → 3/19 以降 VS Code + Continue + Ollama

---

## 18日23時までに実施（Cursor 使用中）

### ✅ 1. ルール・プロンプトを Continue に移す
- [x] `.cursorrules` / `AGENT_INSTRUCTIONS.md` の内容を `.continue/config.yaml` の `systemMessage` に転記済み
- [x] ユーザー設定 `~/.continue/config.yaml` にも `systemMessage` 追加済み

### 2. 大規模な作業は Cursor で済ませる
- [ ] 複数ファイル編集が必要なリファクタがあれば Cursor Composer で実施
- [ ] Background Agent が必要な作業があれば実施

### 3. コミット・プッシュで最終状態を保存する
```powershell
cd c:\uep-v5-ultimate-enterprise-platform
git status
git add .
git commit -m "Cursor移行準備: Continue設定・ルール移行"
git push
```

### 4. VS Code + Continue の動作確認
- [ ] Ollama で DeepSeek Coder 2 Lite を取得: `ollama pull deepseek-coder-v2:lite`
- [ ] VS Code でプロジェクトを開く
- [ ] Ctrl+L で Continue チャットを開く
- [ ] DeepSeek Coder 2 Lite を選択
- [ ] 「このプロジェクトの概要を教えて」で応答確認

---

## 19日以降（VS Code メイン運用）

### 作業フロー
1. VS Code でプロジェクトを開く
2. Ollama が起動していることを確認
3. Continue で AI 支援（Ctrl+L チャット、Ctrl+I インライン編集）
4. 作業後: コミット → プッシュ（バックアップ）

### ショートカット
| 操作 | キー |
|------|------|
| Continue チャット | Ctrl+L |
| インライン編集 | Ctrl+I |
| コンテキスト追加 | @ |

---

## 内定後の使い分け

| 用途 | 推奨 |
|------|------|
| 大規模リファクタ・複数ファイル編集 | Cursor |
| 日常コーディング・オフライン | VS Code + Continue |
| 切り替え時 | 保存 → 終了 → もう一方を起動 |

---

## 参考

- `docs/セットアップ_VSCode_Continue_Ollama.md` - セットアップ手順
- `.continue/config.yaml` - プロジェクト用 Continue 設定
