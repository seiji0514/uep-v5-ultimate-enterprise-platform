"""
gRPC サーバー
マイクロサービス間の gRPC 通信を提供

セットアップ: pip install grpcio-tools
生成: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc_service/proto/uep_internal.proto
"""
import grpc
from concurrent import futures
import os
import sys

# プロト生成コードのインポート（grpc_service/proto/ に生成される）
try:
    from .proto import uep_internal_pb2
    from .proto import uep_internal_pb2_grpc
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False


if GRPC_AVAILABLE:

    class UepInternalServicer(uep_internal_pb2_grpc.UepInternalServiceServicer):
        """UEP 内部サービス実装"""

        def HealthCheck(self, request, context):
            return uep_internal_pb2.HealthResponse(
                status="healthy",
                version="5.0.0",
                service="uep-grpc-internal",
            )

        def GetMetrics(self, request, context):
            return uep_internal_pb2.MetricsResponse(
                request_count=0,
                avg_latency_ms=0.0,
                error_count=0,
            )


def serve(port: int = 50051):
    """gRPC サーバーを起動"""
    if not GRPC_AVAILABLE:
        print(
            "gRPC: proto 生成コードがありません。\n"
            "  pip install grpcio-tools\n"
            "  python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "
            "grpc_service/proto/uep_internal.proto",
            file=sys.stderr,
        )
        return
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    uep_internal_pb2_grpc.add_UepInternalServiceServicer_to_server(
        UepInternalServicer(), server
    )
    # 127.0.0.1 でバインド（IPv6 [::] が失敗する環境向け）
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    print(f"gRPC server listening on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    port = int(os.getenv("GRPC_PORT", "50051"))
    serve(port)
