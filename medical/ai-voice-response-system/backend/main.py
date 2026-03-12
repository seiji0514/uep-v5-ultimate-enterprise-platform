"""
AI自動音声応答システム - バックエンドサーバー
"""
import os
import sys
import logging
import asyncio
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import json

# プロジェクトルートをパスに追加
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from services.voice_response_service import VoiceResponseService
from services.interview_response_service import InterviewResponseService
from services.integrated_interview_service import IntegratedInterviewService
from services.external_integration_service import ExternalIntegrationService
from services.domain_specific_service import DomainSpecificService
import config

load_dotenv()

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# プロジェクトルートのパスを取得
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="AI自動音声応答システム")

# 静的ファイルの配信
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 音声応答サービス
voice_service = VoiceResponseService()

# 面談応答サービス（オプション）
interview_service = InterviewResponseService()

# 統合面談支援サービス（既存システム統合）
integrated_service = IntegratedInterviewService()

# 外部システム統合サービス
external_service = ExternalIntegrationService()

# 分野別サービス（接続ごと）
domain_services: dict[int, DomainSpecificService] = {}

# WebSocket接続管理
active_connections: dict[int, WebSocket] = {}

# 接続ごとの面談モード管理
interview_mode: dict[int, bool] = {}

# 接続ごとの分野設定
domain_mode: dict[int, str] = {}  # "healthcare", "legal", "finance", etc.


@app.get("/")
async def read_root():
    """メインページ"""
    index_path = STATIC_DIR / "index.html"
    return FileResponse(str(index_path))


@app.websocket("/ws/voice-chat")
async def websocket_voice_chat(websocket: WebSocket):
    """
    WebSocket経由でリアルタイム音声チャット
    """
    await websocket.accept()
    connection_id = id(websocket)
    active_connections[connection_id] = websocket
    logger.info(f"WebSocket接続が確立されました: {connection_id}")
    
    try:
        # 初期化メッセージ
        await websocket.send_json({
            "type": "connected",
            "message": "接続が確立されました。マイクに向かって話してください。"
        })
        
        while True:
            # メッセージを受信
            data = await websocket.receive()
            
            if "bytes" in data:
                # 音声データ（バイナリ）
                audio_chunk = data["bytes"]
                await process_audio_chunk(websocket, connection_id, audio_chunk)
            
            elif "text" in data:
                # テキストメッセージ（制御コマンド）
                message = json.loads(data["text"])
                await handle_control_message(websocket, connection_id, message)
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket接続が切断されました: {connection_id}")
        if connection_id in active_connections:
            del active_connections[connection_id]
    except Exception as e:
        logger.error(f"WebSocketエラー: {e}")
        if connection_id in active_connections:
            del active_connections[connection_id]


async def process_audio_chunk(websocket: WebSocket, connection_id: int, audio_chunk: bytes):
    """音声チャンクを処理"""
    try:
        # 音声認識
        transcription_result = await voice_service.transcribe_audio_chunk(audio_chunk, connection_id)
        
        if transcription_result.get("status") == "success" and transcription_result.get("text"):
            text = transcription_result["text"]
            
            # 認識結果を送信
            await websocket.send_json({
                "type": "transcription",
                "text": text,
                "status": "success"
            })
            
            # 面談モードかどうか確認
            is_interview_mode = interview_mode.get(connection_id, False)
            
            # 分野モードかどうか確認
            current_domain = domain_mode.get(connection_id)
            
            # 外部システム統合: 意図を検出
            intent_result = await external_service.detect_intent(text)
            external_response = None
            
            # 外部システムで処理可能な場合は処理
            if intent_result["confidence"] > 0.5:
                external_response = await external_service.handle_external_request(
                    intent_result["intent"],
                    text,
                    intent_result["entities"]
                )
            
            # AI応答生成
            if external_response:
                # 外部システムからの応答を使用
                response_text = external_response
            elif current_domain:
                # 分野モード: 分野特化の応答生成
                if connection_id not in domain_services:
                    domain_services[connection_id] = DomainSpecificService(current_domain)
                domain_service = domain_services[connection_id]
                response_text = await domain_service.handle_domain_query(text)
            elif is_interview_mode:
                # 面談モード: 面談特化の応答生成
                response_text = await interview_service.generate_interview_response(
                    text, connection_id, interview_type="general"
                )
            else:
                # 通常モード: 汎用応答生成
                response_text = await voice_service.generate_response(text, connection_id)
            
            if response_text:
                # 応答テキストを送信
                await websocket.send_json({
                    "type": "response_text",
                    "text": response_text,
                    "status": "success"
                })
                
                # 音声合成
                audio_response = await voice_service.text_to_speech(response_text)
                
                if audio_response.get("status") == "success":
                    # 音声データを送信
                    await websocket.send_bytes(audio_response["audio_data"])
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": "音声合成に失敗しました"
                    })
        
        elif transcription_result.get("status") == "processing":
            # 処理中
            await websocket.send_json({
                "type": "processing",
                "message": "音声を認識しています..."
            })
    
    except Exception as e:
        logger.error(f"音声処理エラー: {e}")
        await websocket.send_json({
            "type": "error",
            "message": f"処理エラー: {str(e)}"
        })


async def handle_control_message(websocket: WebSocket, connection_id: int, message: dict):
    """制御メッセージを処理"""
    msg_type = message.get("type")
    
    if msg_type == "start":
        # 会話開始
        await voice_service.start_conversation(connection_id)
        await websocket.send_json({
            "type": "started",
            "message": "会話を開始しました"
        })
    
    elif msg_type == "stop":
        # 会話終了
        await voice_service.end_conversation(connection_id)
        await websocket.send_json({
            "type": "stopped",
            "message": "会話を終了しました"
        })
    
    elif msg_type == "reset":
        # 会話履歴リセット
        await voice_service.reset_conversation(connection_id)
        interview_service.reset_conversation(connection_id)
        await websocket.send_json({
            "type": "reset",
            "message": "会話履歴をリセットしました"
        })
    
    elif msg_type == "set_interview_mode":
        # 面談モードの設定
        enabled = message.get("enabled", False)
        interview_mode[connection_id] = enabled
        if enabled:
            domain_mode[connection_id] = None  # 面談モード時は分野モードを無効化
        await websocket.send_json({
            "type": "interview_mode_set",
            "enabled": enabled,
            "message": "面談モードを" + ("有効" if enabled else "無効") + "にしました"
        })
    
    elif msg_type == "set_domain_mode":
        # 分野モードの設定
        domain = message.get("domain", None)
        if domain:
            domain_mode[connection_id] = domain
            interview_mode[connection_id] = False  # 分野モード時は面談モードを無効化
            domain_services[connection_id] = DomainSpecificService(domain)
            await websocket.send_json({
                "type": "domain_mode_set",
                "domain": domain,
                "message": f"{domain}分野モードを有効にしました"
            })
        else:
            domain_mode[connection_id] = None
            if connection_id in domain_services:
                del domain_services[connection_id]
            await websocket.send_json({
                "type": "domain_mode_set",
                "domain": None,
                "message": "分野モードを無効にしました"
            })
    
    elif msg_type == "ping":
        # 接続確認
        await websocket.send_json({
            "type": "pong"
        })


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "service": "AI自動音声応答システム",
        "connections": len(active_connections)
    }


@app.post("/api/interview/set-info")
async def set_interview_info(request: dict):
    """
    面談情報を設定
    
    リクエスト例:
    {
        "candidate_info": {
            "name": "山田太郎",
            "experience": "5年間のエンジニア経験",
            "skills": ["Python", "FastAPI", "AI"],
            "motivation": "AI技術を活用したサービス開発に貢献したい",
            "strengths": "問題解決能力",
            "weaknesses": "完璧主義"
        },
        "company_info": {
            "name": "AIexe株式会社",
            "industry": "AI・機械学習",
            "business": "AI技術を活用したWebアプリケーション開発",
            "values": "技術革新とチームワーク",
            "culture": "フルリモート、裁量労働制",
            "benefits": "健康診断、書籍購入補助"
        },
        "interviewer_info": {
            "name": "中山様",
            "position": "代表取締役",
            "department": "経営",
            "background": "AI技術の専門家"
        }
    }
    """
    try:
        candidate_info = request.get("candidate_info")
        company_info = request.get("company_info")
        interviewer_info = request.get("interviewer_info")
        
        interview_service.set_all_info(
            candidate_info=candidate_info,
            company_info=company_info,
            interviewer_info=interviewer_info
        )
        
        summary = interview_service.get_info_summary()
        
        return {
            "status": "success",
            "message": "面談情報を設定しました",
            "summary": summary
        }
    except Exception as e:
        logger.error(f"面談情報設定エラー: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/interview/get-info")
async def get_interview_info():
    """設定されている面談情報を取得"""
    try:
        summary = interview_service.get_info_summary()
        return {
            "status": "success",
            "summary": summary
        }
    except Exception as e:
        logger.error(f"面談情報取得エラー: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/api/interview/load-preparation/{company_name}")
async def load_preparation_data(company_name: str):
    """
    既存の準備資料を読み込む
    
    Args:
        company_name: 企業名（例: "AIexe", "Fusic"）
    
    Returns:
        読み込み結果
    """
    try:
        results = integrated_service.load_all_preparation_data(company_name)
        
        # 統合サービスを面談サービスに設定
        interview_service.set_all_info(
            candidate_info=integrated_service.interview_service.candidate_info,
            company_info=integrated_service.interview_service.company_info,
            interviewer_info=integrated_service.interview_service.interviewer_info
        )
        
        summary = integrated_service.get_info_summary()
        
        return {
            "status": "success",
            "message": f"{company_name}の準備資料を読み込みました",
            "results": results,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"準備資料読み込みエラー: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/interview/practice-questions")
async def get_practice_questions():
    """練習用の質問リストを取得"""
    try:
        questions = integrated_service.get_practice_questions()
        return {
            "status": "success",
            "questions": questions,
            "count": len(questions)
        }
    except Exception as e:
        logger.error(f"質問リスト取得エラー: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/api/external/integrate-rag")
async def integrate_rag_service(request: dict):
    """
    RAGサービスと統合
    
    リクエスト例:
    {
        "rag_service_path": "llm-rag-chatbot/rag_engine.py",
        "config": {
            "vectorstore_path": "...",
            "embedding_model": "..."
        }
    }
    """
    try:
        # RAGサービスを統合（実装は既存システムに依存）
        # await external_service.integrate_with_rag(rag_service)
        
        return {
            "status": "success",
            "message": "RAGサービスと統合しました"
        }
    except Exception as e:
        logger.error(f"RAG統合エラー: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/api/external/add-api")
async def add_external_api(request: dict):
    """
    外部APIを追加
    
    リクエスト例:
    {
        "name": "weather",
        "api_config": {
            "base_url": "https://api.openweathermap.org",
            "api_key": "...",
            "endpoints": {
                "current": "/data/2.5/weather"
            }
        }
    }
    """
    try:
        name = request.get("name")
        api_config = request.get("api_config", {})
        
        await external_service.add_external_api(name, api_config)
        
        return {
            "status": "success",
            "message": f"外部API「{name}」を追加しました"
        }
    except Exception as e:
        logger.error(f"外部API追加エラー: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/api/domain/{domain}/set")
async def set_domain_mode(domain: str, request: dict):
    """
    分野モードを設定
    
    Args:
        domain: 分野（healthcare, legal, finance, education, manufacturing, retail, etc.）
        request: 設定情報
    """
    try:
        connection_id = request.get("connection_id")
        
        if connection_id:
            domain_mode[connection_id] = domain
            domain_services[connection_id] = DomainSpecificService(domain)
            
            return {
                "status": "success",
                "message": f"{domain}分野モードを設定しました",
                "domain": domain
            }
        else:
            return {
                "status": "error",
                "message": "connection_idが必要です"
            }
    
    except Exception as e:
        logger.error(f"分野モード設定エラー: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/domain/list")
async def get_available_domains():
    """利用可能な分野のリストを取得"""
    return {
        "status": "success",
        "domains": [
            {
                "id": "healthcare",
                "name": "医療・ヘルスケア",
                "description": "症状相談、健康管理、医療情報検索"
            },
            {
                "id": "legal",
                "name": "法務・法律",
                "description": "契約書分析、法務Q&A、法令検索"
            },
            {
                "id": "finance",
                "name": "金融・FinTech",
                "description": "不正検知、リスク評価、金融相談"
            },
            {
                "id": "education",
                "name": "教育・学習",
                "description": "学習支援、クイズ生成、言語学習"
            },
            {
                "id": "manufacturing",
                "name": "製造業",
                "description": "品質管理、異常検知、設備管理"
            },
            {
                "id": "retail",
                "name": "小売・EC",
                "description": "商品検索、レコメンデーション、カスタマーサポート"
            },
            {
                "id": "real_estate",
                "name": "不動産",
                "description": "物件検索、価格情報、契約相談"
            },
            {
                "id": "agriculture",
                "name": "農業",
                "description": "病害虫診断、気象情報、収穫予測"
            },
            {
                "id": "transportation",
                "name": "交通・物流",
                "description": "経路検索、交通情報、物流管理"
            },
            {
                "id": "entertainment",
                "name": "エンターテイメント",
                "description": "コンテンツ検索、レコメンデーション"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    # 設定ファイルからポート番号を取得
    server_host = config.SERVER_HOST
    server_port = config.SERVER_PORT
    logger.info(f"サーバーを起動します: http://{server_host}:{server_port}")
    uvicorn.run(app, host=server_host, port=server_port)
