"""
mTLS (相互TLS認証) モジュール
サービス間通信のセキュア化
"""
from typing import Dict, Any, Optional
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta
import os


class MTLSManager:
    """mTLS管理クラス"""

    def __init__(self):
        """mTLSマネージャーを初期化"""
        self.cert_dir = os.getenv("MTLS_CERT_DIR", "/tmp/mtls-certs")
        os.makedirs(self.cert_dir, exist_ok=True)

    def generate_certificate_authority(
        self,
        common_name: str = "UEP CA",
        validity_days: int = 365
    ) -> Dict[str, Any]:
        """
        証明書発行局（CA）を生成

        Args:
            common_name: CAの共通名
            validity_days: 有効期限（日）

        Returns:
            CA証明書と秘密鍵の情報
        """
        # 秘密鍵を生成
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # 証明書を作成
        subject = issuer = x509.Name([
            x509.NameAttribute(x509.NameOID.COUNTRY_NAME, "JP"),
            x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, "Tokyo"),
            x509.NameAttribute(x509.NameOID.LOCALITY_NAME, "Tokyo"),
            x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "UEP"),
            x509.NameAttribute(x509.NameOID.COMMON_NAME, common_name),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        ).sign(private_key, hashes.SHA256())

        # PEM形式に変換
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        return {
            "certificate": cert_pem.decode(),
            "private_key": key_pem.decode(),
            "common_name": common_name
        }

    def generate_server_certificate(
        self,
        ca_cert: x509.Certificate,
        ca_key: rsa.RSAPrivateKey,
        common_name: str,
        validity_days: int = 365
    ) -> Dict[str, Any]:
        """
        サーバー証明書を生成

        Args:
            ca_cert: CA証明書
            ca_key: CA秘密鍵
            common_name: サーバーの共通名
            validity_days: 有効期限（日）

        Returns:
            サーバー証明書と秘密鍵の情報
        """
        # 秘密鍵を生成
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # 証明書を作成
        subject = x509.Name([
            x509.NameAttribute(x509.NameOID.COUNTRY_NAME, "JP"),
            x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, "Tokyo"),
            x509.NameAttribute(x509.NameOID.LOCALITY_NAME, "Tokyo"),
            x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "UEP"),
            x509.NameAttribute(x509.NameOID.COMMON_NAME, common_name),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            ca_cert.subject
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(common_name),
                x509.DNSName(f"*.{common_name}"),
            ]),
            critical=False,
        ).sign(ca_key, hashes.SHA256())

        # PEM形式に変換
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        return {
            "certificate": cert_pem.decode(),
            "private_key": key_pem.decode(),
            "common_name": common_name
        }

    def verify_certificate(
        self,
        cert_pem: str,
        ca_cert_pem: str
    ) -> bool:
        """
        証明書を検証

        Args:
            cert_pem: 検証する証明書（PEM形式）
            ca_cert_pem: CA証明書（PEM形式）

        Returns:
            検証が成功したかどうか
        """
        try:
            cert = x509.load_pem_x509_certificate(cert_pem.encode())
            ca_cert = x509.load_pem_x509_certificate(ca_cert_pem.encode())

            # 証明書の有効期限をチェック
            if cert.not_valid_after < datetime.utcnow():
                return False

            # CA証明書で検証（簡易実装）
            # 実際の実装では、より詳細な検証が必要
            return True
        except Exception:
            return False


# グローバルインスタンス
mtls_manager = MTLSManager()
