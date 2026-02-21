# デスクトップPC クイックスタートガイド

**作成日**: 2026年1月29日  
**対象**: デスクトップPCでの迅速なセットアップ

---

## 🚀 5分でセットアップ完了

### **ステップ1: WSLを起動**

**Windows側（PowerShellまたはコマンドプロンプト）**:

```powershell
wsl
```

### **ステップ2: プロジェクトディレクトリに移動**

**WSL内**:

```bash
# Windows側のパスにアクセス
cd /mnt/d/AI_system_research/開発プロジェクト/AI\ system\ research\ and\ development\ track\ record/uep-v5-ultimate-enterprise-platform

# または、WSL内にコピー（推奨）
cd ~
mkdir -p projects
cp -r /mnt/d/AI_system_research/開発プロジェクト/AI\ system\ research\ and\ development\ track\ record/uep-v5-ultimate-enterprise-platform ~/projects/
cd ~/projects/uep-v5-ultimate-enterprise-platform
```

### **ステップ3: Dockerをインストール（初回のみ）**

**WSL内**:

```bash
chmod +x install-docker-wsl.sh
sudo ./install-docker-wsl.sh

# WSLを再起動
exit
```

**Windows側**:

```powershell
wsl --shutdown
wsl
```

### **ステップ4: デモンストレーション環境を起動**

**WSL内**:

```bash
cd ~/projects/uep-v5-ultimate-enterprise-platform
chmod +x *.sh
./demo-start.sh
```

### **ステップ5: 動作確認**

**WSL内**:

```bash
./health-check.sh
```

**Windows側（ブラウザ）**:

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin/admin)

---

## ✅ 完了！

デモンストレーションを開始できます。

---

## 🛑 停止方法

```bash
./stop.sh
```

---

## 📚 詳細情報

- [DESKTOP_SETUP_GUIDE.md](docs/DESKTOP_SETUP_GUIDE.md) - 詳細なセットアップ手順
- [DESKTOP_MIGRATION_CHECKLIST.md](DESKTOP_MIGRATION_CHECKLIST.md) - 移行チェックリスト

---

以上
