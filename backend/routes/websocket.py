"""
WebSocketエンドポイント
リアルタイム通信
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Optional
from datetime import datetime
from core.websocket import connection_manager
from auth.jwt_auth import get_current_user_websocket

router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, room: str = "default"):
    """基本的なWebSocketエンドポイント"""
    await connection_manager.connect(websocket, room=room)
    try:
        while True:
            data = await websocket.receive_json()

            # メッセージをルーム内の全員にブロードキャスト
            await connection_manager.send_to_room(
                {
                    "type": "message",
                    "room": room,
                    "data": data,
                    "timestamp": str(datetime.utcnow())
                },
                room=room
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room=room)


@router.websocket("/user/{user_id}")
async def user_websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
    current_user: Optional[dict] = Depends(get_current_user_websocket)
):
    """ユーザー専用WebSocketエンドポイント"""
    await connection_manager.connect(websocket, room=f"user_{user_id}", user_id=user_id)
    try:
        while True:
            data = await websocket.receive_json()

            # ユーザーにメッセージを送信
            await connection_manager.send_to_user(
                {
                    "type": "user_message",
                    "user_id": user_id,
                    "data": data,
                    "timestamp": str(datetime.utcnow())
                },
                user_id=user_id
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room=f"user_{user_id}", user_id=user_id)


@router.websocket("/notifications")
async def notifications_websocket_endpoint(
    websocket: WebSocket,
    current_user: Optional[dict] = Depends(get_current_user_websocket)
):
    """通知用WebSocketエンドポイント"""
    user_id = current_user.get("username") if current_user else "anonymous"
    await connection_manager.connect(websocket, room="notifications", user_id=user_id)
    try:
        while True:
            data = await websocket.receive_json()
            # 通知処理
            await connection_manager.send_personal_message(
                {
                    "type": "notification",
                    "data": data,
                    "timestamp": str(datetime.utcnow())
                },
                websocket
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room="notifications", user_id=user_id)
