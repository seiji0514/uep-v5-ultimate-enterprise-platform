"""
MinIOクライアントモジュール
MinIOへの接続と操作を実装
"""
from minio import Minio
from minio.error import S3Error
from typing import List, Optional, Dict, Any
import os
from io import BytesIO


class MinIOClient:
    """MinIOクライアントクラス"""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        secure: bool = False
    ):
        """
        MinIOクライアントを初期化

        Args:
            endpoint: MinIOエンドポイント（デフォルト: 環境変数から取得）
            access_key: アクセスキー（デフォルト: 環境変数から取得）
            secret_key: シークレットキー（デフォルト: 環境変数から取得）
            secure: HTTPSを使用するかどうか
        """
        self.endpoint = endpoint or os.getenv("MINIO_ENDPOINT", "minio:9000")
        self.access_key = access_key or os.getenv("MINIO_ROOT_USER", "minioadmin")
        self.secret_key = secret_key or os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
        self.secure = secure

        # MinIOクライアントを作成
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )

    def list_buckets(self) -> List[Dict[str, Any]]:
        """バケット一覧を取得"""
        try:
            buckets = self.client.list_buckets()
            return [
                {
                    "name": bucket.name,
                    "creation_date": bucket.creation_date.isoformat() if bucket.creation_date else None
                }
                for bucket in buckets
            ]
        except S3Error as e:
            raise Exception(f"Failed to list buckets: {str(e)}")

    def create_bucket(self, bucket_name: str, region: Optional[str] = None) -> bool:
        """バケットを作成"""
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name, location=region)
                return True
            return False
        except S3Error as e:
            raise Exception(f"Failed to create bucket: {str(e)}")

    def delete_bucket(self, bucket_name: str) -> bool:
        """バケットを削除"""
        try:
            if self.client.bucket_exists(bucket_name):
                self.client.remove_bucket(bucket_name)
                return True
            return False
        except S3Error as e:
            raise Exception(f"Failed to delete bucket: {str(e)}")

    def bucket_exists(self, bucket_name: str) -> bool:
        """バケットが存在するか確認"""
        try:
            return self.client.bucket_exists(bucket_name)
        except S3Error as e:
            raise Exception(f"Failed to check bucket existence: {str(e)}")

    def list_objects(
        self,
        bucket_name: str,
        prefix: Optional[str] = None,
        recursive: bool = True
    ) -> List[Dict[str, Any]]:
        """オブジェクト一覧を取得"""
        try:
            objects = self.client.list_objects(
                bucket_name,
                prefix=prefix,
                recursive=recursive
            )
            return [
                {
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
                    "etag": obj.etag
                }
                for obj in objects
            ]
        except S3Error as e:
            raise Exception(f"Failed to list objects: {str(e)}")

    def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        file_data: bytes,
        content_type: Optional[str] = None
    ) -> bool:
        """ファイルをアップロード"""
        try:
            file_stream = BytesIO(file_data)
            self.client.put_object(
                bucket_name,
                object_name,
                file_stream,
                length=len(file_data),
                content_type=content_type or "application/octet-stream"
            )
            return True
        except S3Error as e:
            raise Exception(f"Failed to upload file: {str(e)}")

    def download_file(self, bucket_name: str, object_name: str) -> bytes:
        """ファイルをダウンロード"""
        try:
            response = self.client.get_object(bucket_name, object_name)
            return response.read()
        except S3Error as e:
            raise Exception(f"Failed to download file: {str(e)}")

    def delete_object(self, bucket_name: str, object_name: str) -> bool:
        """オブジェクトを削除"""
        try:
            self.client.remove_object(bucket_name, object_name)
            return True
        except S3Error as e:
            raise Exception(f"Failed to delete object: {str(e)}")

    def get_object_info(self, bucket_name: str, object_name: str) -> Dict[str, Any]:
        """オブジェクト情報を取得"""
        try:
            stat = self.client.stat_object(bucket_name, object_name)
            return {
                "name": object_name,
                "size": stat.size,
                "last_modified": stat.last_modified.isoformat() if stat.last_modified else None,
                "etag": stat.etag,
                "content_type": stat.content_type
            }
        except S3Error as e:
            raise Exception(f"Failed to get object info: {str(e)}")
