#!/bin/bash
# gRPC Python コード生成
# 実行: bash scripts/generate_grpc_proto.sh
# 必要: pip install grpcio-tools
cd "$(dirname "$0")/.."
mkdir -p backend/grpc_service
python -m grpc_tools.protoc \
  -I. \
  --python_out=backend/grpc_service \
  --grpc_python_out=backend/grpc_service \
  backend/grpc_service/proto/uep_internal.proto
# 生成ファイルの import パス修正（proto ディレクトリ参照）
sed -i 's/from backend.grpc_service.proto/from grpc_service.proto/g' backend/grpc_service/uep_internal_pb2_grpc.py 2>/dev/null || true
echo "Generated: backend/grpc_service/uep_internal_pb2.py, uep_internal_pb2_grpc.py"
