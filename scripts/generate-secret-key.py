#!/usr/bin/env python3
"""
本番用 SECRET_KEY 生成スクリプト
Usage: python scripts/generate-secret-key.py
"""
import secrets
print(secrets.token_urlsafe(64))
