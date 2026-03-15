# DB 定期バックアップ 設定手順

**対象**: UEP v5.0 本体（SQLite / PostgreSQL）

---

## 実行方法

### 手動実行

```batch
scripts\backup_db_uep.bat
```

### バックアップ先

`backups\db\YYYY-MM-DD\` に日付フォルダで保存されます。

---

## タスクスケジューラで定期実行（Windows）

1. **タスクスケジューラ**を開く（Win + R → `taskschd.msc`）
2. **基本タスクの作成**
3. 名前: `UEP DB バックアップ`
4. トリガー: **毎日**、時刻 **2:00** など
5. 操作: **プログラムの開始**
6. プログラム: `scripts\backup_db_uep.bat` の**フルパス**
   - 例: `C:\uep-v5-ultimate-enterprise-platform\scripts\backup_db_uep.bat`
7. 開始: `C:\uep-v5-ultimate-enterprise-platform`（プロジェクトルート）

---

## 注意

- SQLite の場合は `backend\uep_db.sqlite` が存在する場合にコピー
- PostgreSQL の場合は `pg_dump` が PATH にあり、`DATABASE_URL` が設定されている場合に実行
- バックアップ先は USB 等にコピーするか、既存の `scripts\バックアップ_O_N_P.bat` に含める
