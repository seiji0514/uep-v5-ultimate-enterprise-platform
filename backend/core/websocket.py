"""
WebSocketサポートモジュール
リアルタイム通信
"""
from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List, Set
import json
import asyncio
from datetime import datetime
from auth.jwt_auth import get_current_user_websocket


class ConnectionManager:
    """WebSocket接続管理クラス"""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.user_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str = "default", user_id: str = None):
        """WebSocket接続を確立"""
        await websocket.accept()

        if room not in self.active_connections:
            self.active_connections[room] = set()
        self.active_connections[room].add(websocket)

        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, room: str = "default", user_id: str = None):
        """WebSocket接続を切断"""
        if room in self.active_connections:
            self.active_connections[room].discard(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

        if user_id and user_id in self.user_connections:
            self.user_connections[user_id].discard(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """個人メッセージを送信"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message: {e}")

    async def send_to_room(self, message: dict, room: str):
        """ルーム内の全員にメッセージを送信"""
        if room in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[room]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)

            # 切断された接続を削除
            for connection in disconnected:
                self.active_connections[room].discard(connection)

    async def send_to_user(self, message: dict, user_id: str):
        """特定ユーザーにメッセージを送信"""
        if user_id in self.user_connections:
            disconnected = set()
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)

            # 切断された接続を削除
            for connection in disconnected:
                self.user_connections[user_id].discard(connection)

    async def broadcast(self, message: dict):
        """全接続にブロードキャスト"""
        all_connections = set()
        for room_connections in self.active_connections.values():
            all_connections.update(room_connections)

        disconnected = set()
        for connection in all_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # 切断された接続を削除
        for connection in disconnected:
            for room_connections in self.active_connections.values():
                room_connections.discard(connection)


# グローバルインスタンス
connection_manager = ConnectionManager()
