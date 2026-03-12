# uep-cli

UEP v5.0 CLIツール（Python版・Go版）

## Python版（推奨・McAfee等で隔離されない）

```cmd
python uep-cli.py version
python uep-cli.py health
python uep-cli.py events list
python uep-cli.py events outbox
python uep-cli.py grpc status
python uep-cli.py graphql query -q "{ hello health { status } }"
```

**バッチで実行**:
```cmd
run-uep-cli.bat version
run-uep-cli.bat health
```

## Go版（オプション）

```bash
cd tools/uep-cli
go mod tidy
go build -o uep-cli.exe .
uep-cli.exe health
```

## 使い方（共通）

```bash
# ヘルスチェック
uep-cli health
uep-cli health -u http://localhost:8000 -o table

# 認証付き
uep-cli health -t <JWT_TOKEN>

# イベント
uep-cli events list -t <TOKEN>
uep-cli events outbox -t <TOKEN>

# GraphQL
uep-cli graphql query -q "{ hello health { status } }"

# バージョン
uep-cli version
```
