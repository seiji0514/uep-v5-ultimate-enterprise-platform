"""
完全統合AI音声応答プラットフォーム
AI自動音声応答システム + 様々な分野モジュール
"""
import os
import sys
import logging
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import json

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# コアサービス
from services.voice_response_service import VoiceResponseService

# 分野別モジュール
from modules.healthcare_module import HealthcareModule
from modules.legal_module import LegalModule
from modules.finance_module import FinanceModule
from modules.education_module import EducationModule
from modules.manufacturing_module import ManufacturingModule
from modules.retail_module import RetailModule

# 統合サービス
from services.domain_manager import DomainManager
from api.gateway import UnifiedAPIGateway

load_dotenv()

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# プロジェクトルートのパスを取得
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "frontend"

# 静的ディレクトリが存在しない場合は作成
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="完全統合AI音声応答プラットフォーム")

# 静的ファイルの配信
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# コアサービス
voice_service = VoiceResponseService()

# 分野別モジュールの初期化
domain_modules = {
    "healthcare": HealthcareModule(),
    "legal": LegalModule(),
    "finance": FinanceModule(),
    "education": EducationModule(),
    "manufacturing": ManufacturingModule(),
    "retail": RetailModule(),
}

# 統合サービス
domain_manager = DomainManager(domain_modules)
api_gateway = UnifiedAPIGateway(voice_service, domain_manager)

# WebSocket接続管理
active_connections: dict[int, WebSocket] = {}

# 接続ごとの設定
connection_settings: dict[int, dict] = {}


@app.get("/")
async def read_root():
    """メインページ"""
    index_path = STATIC_DIR / "index.html"
    return FileResponse(str(index_path))


@app.websocket("/ws/unified-voice")
async def websocket_unified_voice(websocket: WebSocket):
    """
    統合音声WebSocketエンドポイント
    """
    await websocket.accept()
    connection_id = id(websocket)
    active_connections[connection_id] = websocket
    
    # 接続設定の初期化
    connection_settings[connection_id] = {
        "domain": None,
        "interview_mode": False
    }
    
    logger.info(f"WebSocket接続が確立されました: {connection_id}")
    
    try:
        # 初期化メッセージ
        await websocket.send_json({
            "type": "connected",
            "message": "完全統合AI音声応答プラットフォームに接続しました",
            "available_domains": list(domain_modules.keys())
        })
        
        while True:
            # メッセージを受信
            data = await websocket.receive()
            
            if "bytes" in data:
                # 音声データ（バイナリ）
                audio_chunk = data["bytes"]
                await process_unified_voice(websocket, connection_id, audio_chunk)
            
            elif "text" in data:
                # テキストメッセージ（制御コマンド）
                message = json.loads(data["text"])
                await handle_unified_control_message(websocket, connection_id, message)
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket接続が切断されました: {connection_id}")
        if connection_id in active_connections:
            del active_connections[connection_id]
        if connection_id in connection_settings:
            del connection_settings[connection_id]
    except Exception as e:
        logger.error(f"WebSocketエラー: {e}")
        if connection_id in active_connections:
            del active_connections[connection_id]


async def process_unified_voice(websocket: WebSocket, connection_id: int, audio_chunk: bytes):
    """統合音声処理"""
    try:
        settings = connection_settings.get(connection_id, {})
        domain = settings.get("domain")
        
        # 統合APIゲートウェイで処理
        audio_response, text_response = await api_gateway.process_voice_request(
            audio_chunk, domain, connection_id
        )
        
        # 認識結果を送信
        if text_response:
            await websocket.send_json({
                "type": "response_text",
                "text": text_response,
                "domain": domain,
                "status": "success"
            })
            
            # 音声データを送信
            if audio_response:
                await websocket.send_bytes(audio_response)
    
    except Exception as e:
        logger.error(f"統合音声処理エラー: {e}")
        await websocket.send_json({
            "type": "error",
            "message": f"処理エラー: {str(e)}"
        })


async def handle_unified_control_message(websocket: WebSocket, connection_id: int, message: dict):
    """統合制御メッセージを処理"""
    msg_type = message.get("type")
    settings = connection_settings.get(connection_id, {})
    
    if msg_type == "set_domain":
        # 分野の設定
        domain = message.get("domain")
        if domain in domain_modules:
            settings["domain"] = domain
            await websocket.send_json({
                "type": "domain_set",
                "domain": domain,
                "message": f"{domain}分野モードを設定しました"
            })
        else:
            await websocket.send_json({
                "type": "error",
                "message": f"未対応の分野: {domain}"
            })
    
    elif msg_type == "get_available_domains":
        # 利用可能な分野を取得
        await websocket.send_json({
            "type": "available_domains",
            "domains": list(domain_modules.keys())
        })
    
    elif msg_type == "ping":
        # 接続確認
        await websocket.send_json({
            "type": "pong"
        })


@app.get("/api/domains")
async def get_domains():
    """利用可能な分野のリストを取得"""
    return {
        "status": "success",
        "domains": [
            {
                "id": domain_id,
                "name": module.get_display_name(),
                "description": module.get_description(),
                "available": module.is_available()
            }
            for domain_id, module in domain_modules.items()
        ]
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "service": "完全統合AI音声応答プラットフォーム",
        "connections": len(active_connections),
        "available_domains": len(domain_modules),
        "domains": list(domain_modules.keys())
    }


if __name__ == "__main__":
    import uvicorn
    import config
    import socket
    
    server_host = config.SERVER_HOST
    server_port = config.SERVER_PORT
    
    # ポートが使用中の場合の処理
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', server_port))
    except OSError:
        # ポートが使用中の場合は次のポートを試す
        logger.warning(f"ポート{server_port}が使用中のため、別のポートを検索します...")
        for port in range(server_port + 1, server_port + 10):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    server_port = port
                    logger.info(f"ポート{port}を使用します。")
                    break
            except OSError:
                continue
        else:
            logger.error(f"ポート{server_port}から{server_port + 10}まで使用中です。別のポートを設定してください。")
            sys.exit(1)
    
    logger.info(f"完全統合AI音声応答プラットフォームを起動します: http://{server_host}:{server_port}")
    logger.info(f"ブラウザで http://localhost:{server_port} にアクセスしてください。")
    uvicorn.run(app, host=server_host, port=server_port)
