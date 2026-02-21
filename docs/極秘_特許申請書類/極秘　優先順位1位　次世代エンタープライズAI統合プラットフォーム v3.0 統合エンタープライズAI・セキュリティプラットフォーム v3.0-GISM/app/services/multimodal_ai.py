"""
マルチモーダルAIサービス
- CLIP: テキスト-画像統合
- BLIP: 画像キャプション生成
"""
import os
import io
from typing import Dict, Any, Optional, List
import logging
from PIL import Image

# torchをオプショナルにする（Dockerビルドエラー回避）
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    logging.warning("torch not available. Some multimodal AI functionality will be limited.")

try:
    from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("transformers not available. Multimodal AI functionality will be limited.")

logger = logging.getLogger(__name__)


class MultimodalAIService:
    """マルチモーダルAIサービス"""
    
    def __init__(self):
        self.clip_model = None
        self.clip_processor = None
        self.blip_model = None
        self.blip_processor = None
        self.device = "cuda" if (TORCH_AVAILABLE and torch.cuda.is_available()) else "cpu"
        
        if TRANSFORMERS_AVAILABLE and TORCH_AVAILABLE:
            self._init_models()
        else:
            logging.warning("Multimodal AI models will use mock implementations due to missing dependencies.")
    
    def _init_models(self):
        """モデル初期化"""
        try:
            # CLIPモデル初期化
            logger.info("Loading CLIP model...")
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_model.to(self.device)
            self.clip_model.eval()
            logger.info("CLIP model loaded successfully")
            
            # BLIPモデル初期化
            logger.info("Loading BLIP model...")
            self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.blip_model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            self.blip_model.to(self.device)
            self.blip_model.eval()
            logger.info("BLIP model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")
            self.clip_model = None
            self.blip_model = None
    
    def is_available(self) -> bool:
        """サービス利用可能性チェック"""
        return (
            TRANSFORMERS_AVAILABLE and
            self.clip_model is not None and
            self.blip_model is not None
        )
    
    async def process_text(self, text: str) -> Dict[str, Any]:
        """
        テキスト処理
        """
        try:
            # テキストの特徴量抽出（CLIP使用）
            if self.clip_processor and self.clip_model:
                inputs = self.clip_processor(
                    text=text,
                    return_tensors="pt",
                    padding=True,
                    truncation=True
                ).to(self.device)
                
                with torch.no_grad():
                    text_features = self.clip_model.get_text_features(**inputs)
                    text_embedding = text_features[0].cpu().numpy().tolist()
                
                return {
                    "status": "success",
                    "text": text,
                    "embedding": text_embedding,
                    "embedding_dim": len(text_embedding)
                }
            else:
                return {
                    "status": "success",
                    "text": text,
                    "length": len(text)
                }
        except Exception as e:
            logger.error(f"Text processing error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def generate_caption(self, image_data: bytes) -> Dict[str, Any]:
        """
        BLIPを使用した画像キャプション生成
        """
        if not TRANSFORMERS_AVAILABLE or self.blip_model is None:
            return {
                "status": "error",
                "message": "BLIP model is not available"
            }
        
        try:
            # 画像読み込み
            image = Image.open(io.BytesIO(image_data))
            
            # キャプション生成
            inputs = self.blip_processor(image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                generated_ids = self.blip_model.generate(**inputs, max_length=50)
                caption = self.blip_processor.decode(generated_ids[0], skip_special_tokens=True)
            
            return {
                "status": "success",
                "caption": caption
            }
        except Exception as e:
            logger.error(f"Caption generation error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def text_image_similarity(
        self,
        text: str,
        image_data: bytes
    ) -> Dict[str, Any]:
        """
        CLIPを使用したテキスト-画像類似度計算
        """
        if not TRANSFORMERS_AVAILABLE or self.clip_model is None:
            return {
                "status": "error",
                "message": "CLIP model is not available"
            }
        
        try:
            # 画像読み込み
            image = Image.open(io.BytesIO(image_data))
            
            # テキストと画像の特徴量抽出
            inputs = self.clip_processor(
                text=text,
                images=image,
                return_tensors="pt",
                padding=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.clip_model(**inputs)
                similarity = torch.cosine_similarity(
                    outputs.text_embeds,
                    outputs.image_embeds
                ).item()
            
            return {
                "status": "success",
                "similarity": similarity,
                "text": text
            }
        except Exception as e:
            logger.error(f"Similarity calculation error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def fuse_modalities(
        self,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        マルチモーダル融合
        """
        try:
            fused_result = {
                "status": "success",
                "modalities": list(results.keys()),
                "fused_features": {}
            }
            
            # テキストと画像の特徴量を融合
            if "text" in results and "image" in results:
                text_embedding = results["text"].get("embedding")
                image_similarity = results["image"].get("similarity")
                
                if text_embedding and image_similarity:
                    fused_result["fused_features"] = {
                        "text_embedding_dim": len(text_embedding),
                        "image_text_similarity": image_similarity
                    }
            
            return fused_result
        except Exception as e:
            logger.error(f"Modality fusion error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

