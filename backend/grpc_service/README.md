# gRPC サービス

マイクロサービス間の gRPC 通信を提供します。

## セットアップ

```bash
# grpcio-tools をインストール
pip install grpcio-tools

# proto から Python コードを生成
cd backend
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc_service/proto/uep_internal.proto

# サーバー起動（ポート 50051）
python -m grpc_service.server

# 動作確認（別ターミナルで）
python -c "
import grpc
from grpc_service.proto import uep_internal_pb2, uep_internal_pb2_grpc
channel = grpc.insecure_channel('127.0.0.1:50051')
stub = uep_internal_pb2_grpc.UepInternalServiceStub(channel)
print(stub.HealthCheck(uep_internal_pb2.HealthRequest()))
"
```

## プロトコル定義

- `uep_internal.proto`: HealthCheck, GetMetrics RPC
- ポート: 50051（環境変数 GRPC_PORT で変更可）

## FastAPI からの利用

gRPC クライアントで `localhost:50051` に接続して HealthCheck / GetMetrics を呼び出せます。
