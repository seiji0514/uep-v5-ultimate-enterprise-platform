# Kafka Streams サンプル

補強スキル: イベント駆動（Kafka Streams）

## 前提

- **Java 17**（Oracle JDK または Temurin 等）
- Kafka 起動済み（`docker-compose up kafka`）

## Gradle 不要

Gradle Wrapper 付属のため、**Gradle のインストールは不要**です。
`gradlew.bat` が自動で Gradle を取得します。

## ビルド・実行

### Windows（Kafka が WSL 内の場合、接続できない可能性あり）

```powershell
cd infrastructure\event-streaming\kafka-streams
.\gradlew.bat run
```

### WSL2 内で実行（推奨・Kafka と同一ネットワーク）

```bash
cd /mnt/c/uep-v5-ultimate-enterprise-platform
bash scripts/wsl-kafka-streams-run.sh
```

初回は Java のインストールで時間がかかります。

## Java 未インストールの場合

1. [Oracle JDK 17](https://www.oracle.com/java/technologies/downloads/#jdk17) をダウンロード・インストール
2. または **管理者** PowerShell で: `.\scripts\install-java-gradle.ps1`

## ロックエラーが出た場合

前回のプロセスが残っている場合、state ディレクトリを削除:

```powershell
Remove-Item -Recurse -Force .\build\kafka-streams-state -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force $env:TEMP\kafka-streams -ErrorAction SilentlyContinue
```

その後、再度 `.\gradlew.bat run` を実行。

## 概要

`uep-events` トピックからメッセージを読み、件数を集計するストリーム処理。
