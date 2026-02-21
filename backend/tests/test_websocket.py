"""
WebSocketのテスト
"""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_websocket_connection():
    """WebSocket接続をテスト"""
    with client.websocket_connect("/ws/") as websocket:
        websocket.send_json({"message": "test"})
        data = websocket.receive_json()
        assert "type" in data
        assert "data" in data
