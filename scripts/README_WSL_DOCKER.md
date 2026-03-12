# WSL2 内で Docker セットアップ

## 実行方法

**WSL ターミナル**（Ubuntu 等）を開いて実行（推奨）:

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform
# Windows の改行を変換（必要な場合）
sed -i 's/\r$//' scripts/wsl-docker-setup.sh
bash scripts/wsl-docker-setup.sh
```

または **PowerShell** から:

```powershell
cd c:\uep-v5-ultimate-enterprise-platform
wsl -e bash -c "sed -i 's/\r$//' /mnt/c/uep-v5-ultimate-enterprise-platform/scripts/wsl-docker-setup.sh && cd /mnt/c/uep-v5-ultimate-enterprise-platform && bash scripts/wsl-docker-setup.sh"
```

## 実行内容

1. パッケージ更新
2. 必要なパッケージ（ca-certificates, curl, gnupg）
3. Docker GPG キー
4. Docker リポジトリ追加
5. Docker インストール
6. ユーザーを docker グループに追加
7. Docker サービス起動
8. hello-world で動作確認
9. ~/.bashrc に Docker 自動起動を追加

## 完了後

1. WSL を `exit` して再起動
2. Kafka 起動:
   ```bash
   cd /mnt/c/uep-v5-ultimate-enterprise-platform
   docker compose up -d zookeeper kafka
   ```
