# 仮想環境の修復ガイド

**作成日**: 2026年1月30日

---

## 問題の症状

以下のエラーが発生している場合、仮想環境が破損しています：

- `No module named pip`
- `Permission denied: 'venv\Scripts\python.exe'`
- `Virtual environment is corrupted`
- `Failed to activate virtual environment`

---

## 解決方法

### 方法1: 自動削除スクリプトを使用（推奨）

1. **すべてのコマンドプロンプトとエディタを閉じる**

2. **削除スクリプトを実行**:
   ```cmd
   delete-venv.bat
   ```

   このスクリプトは：
   - Pythonプロセスを終了
   - 仮想環境フォルダを強制的に削除
   - 複数回試行して確実に削除

3. **再構築スクリプトを実行**:
   ```cmd
   rebuild-backend-simple.bat
   ```

4. **バックエンドを起動**:
   ```cmd
   start-backend.bat
   ```

### 方法2: 手動で削除

1. **すべてのコマンドプロンプトとエディタを閉じる**

2. **Pythonプロセスを終了**:
   ```cmd
   taskkill /F /IM python.exe /T
   taskkill /F /IM pythonw.exe /T
   ```

3. **エクスプローラーで削除**:
   - `backend\venv`フォルダを開く
   - フォルダを右クリックして「削除」
   - 削除できない場合は、コンピューターを再起動してから再試行

4. **再構築スクリプトを実行**:
   ```cmd
   rebuild-backend-simple.bat
   ```

### 方法3: 管理者権限で実行

1. **コマンドプロンプトを管理者として実行**:
   - Windowsキーを押す
   - 「cmd」と入力
   - 「コマンドプロンプト」を右クリック
   - 「管理者として実行」を選択

2. **プロジェクトディレクトリに移動**:
   ```cmd
   cd C:\uep-v5-ultimate-enterprise-platform
   ```

3. **削除スクリプトを実行**:
   ```cmd
   delete-venv.bat
   ```

4. **再構築スクリプトを実行**:
   ```cmd
   rebuild-backend-simple.bat
   ```

---

## 確認事項

再構築後、以下を確認してください：

1. **仮想環境が正しく作成されている**:
   ```cmd
   dir backend\venv\Scripts
   ```
   `python.exe`と`pip.exe`が存在することを確認

2. **pipが動作する**:
   ```cmd
   cd backend
   venv\Scripts\activate
   pip --version
   ```

3. **バックエンドが起動する**:
   ```cmd
   start-backend.bat
   ```

---

## トラブルシューティング

### 削除できない場合

1. **ファイルエクスプローラーで確認**:
   - `backend\venv`フォルダ内のファイルが使用中でないか確認
   - 特に`.pyd`ファイルや`python.exe`がロックされていないか確認

2. **コンピューターを再起動**:
   - すべてのプロセスを終了してから再試行

3. **アンチウイルスソフトを一時的に無効化**:
   - アンチウイルスがファイルをスキャンしている可能性があります

### 再作成できない場合

1. **Pythonのバージョンを確認**:
   ```cmd
   python --version
   ```
   Python 3.11以上が必要です

2. **Pythonのパスを確認**:
   ```cmd
   where python
   ```

3. **仮想環境モジュールを確認**:
   ```cmd
   python -m venv --help
   ```

---

## 注意事項

- 仮想環境を削除すると、インストール済みのパッケージも削除されます
- 再構築後、`requirements.txt`からすべてのパッケージを再インストールする必要があります
- カスタム設定がある場合は、再構築前にバックアップを取ってください

---

以上
