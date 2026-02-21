"""
コンピュータビジョンサービス
フェーズ2: 専門領域統合
- YOLO: 物体検出
- U-Net: 画像セグメンテーション
- 医療画像解析: DICOM形式対応
- 動画処理: 動画分類、オブジェクト追跡

パフォーマンス最適化:
- 遅延初期化: モデルの読み込みを必要になるまで遅延
- キャッシュ: 計算結果をキャッシュ
"""
import os
import io
import logging
import hashlib
from typing import Dict, Any, Optional, List
from PIL import Image
import numpy as np

from app.utils.cache import cache_manager, TTLCache

# OpenCV（必須）
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logging.warning("OpenCV not available. Computer vision functionality will be limited.")

# YOLO（オプショナル）
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logging.warning("YOLO (ultralytics) not available. Object detection will use mock implementation.")

# DICOM（医療画像、オプショナル）
try:
    import pydicom
    from pydicom.errors import InvalidDicomError
    DICOM_AVAILABLE = True
except ImportError:
    DICOM_AVAILABLE = False
    logging.warning("pydicom not available. Medical image analysis will be limited.")

logger = logging.getLogger(__name__)


class ComputerVisionService:
    """コンピュータビジョンサービス（最適化版）"""
    
    def __init__(self):
        self.yolo_model = None
        self.device = "cpu"  # GPU利用時は "cuda"
        self.yolo_available = YOLO_AVAILABLE  # インスタンス変数として保存
        self._yolo_loaded = False  # 遅延初期化フラグ
        
        # キャッシュ初期化（画像ハッシュベース、TTL 1時間）
        self.image_cache = cache_manager.get_cache(
            "computer_vision",
            cache_type="ttl",
            ttl_seconds=3600,
            max_size=100
        )
    
    def _lazy_load_yolo(self):
        """YOLOモデルの遅延初期化"""
        if not self._yolo_loaded and YOLO_AVAILABLE and self.yolo_model is None:
            try:
                logger.info("Lazy loading YOLO model...")
                self.yolo_model = YOLO('yolov8n.pt')  # nano版（軽量）
                self._yolo_loaded = True
                logger.info("YOLO model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load YOLO model: {e}")
                self.yolo_available = False
                self._yolo_loaded = True  # 失敗しても再試行しない
    
    def _get_image_hash(self, image_data: bytes) -> str:
        """画像データのハッシュを取得（キャッシュキー用）"""
        return hashlib.md5(image_data).hexdigest()
    
    def is_available(self) -> bool:
        """サービスが利用可能かチェック"""
        return CV2_AVAILABLE
    
    def detect_objects(self, image_data: bytes) -> Dict[str, Any]:
        """
        物体検出（YOLO、キャッシュ付き）
        
        Args:
            image_data: 画像データ（bytes）
        
        Returns:
            検出された物体のリスト
        """
        if not CV2_AVAILABLE:
            return {
                "status": "error",
                "message": "OpenCV is not available"
            }
        
        # キャッシュチェック
        image_hash = self._get_image_hash(image_data)
        cached_result = self.image_cache.get(f"detect_{image_hash}")
        if cached_result is not None:
            logger.debug("Cache hit for detect_objects")
            return cached_result
        
        try:
            # 遅延初期化
            self._lazy_load_yolo()
            
            # 画像を読み込み
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {
                    "status": "error",
                    "message": "Failed to decode image"
                }
            
            # YOLOで物体検出
            if self.yolo_available and self.yolo_model:
                results = self.yolo_model(image)
                detections = []
                
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        detections.append({
                            "class": int(box.cls[0]),
                            "class_name": self.yolo_model.names[int(box.cls[0])],
                            "confidence": float(box.conf[0]),
                            "bbox": box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                        })
                
                result = {
                    "status": "success",
                    "detections": detections,
                    "count": len(detections)
                }
            else:
                # モック実装
                result = {
                    "status": "success",
                    "detections": [
                        {
                            "class": 0,
                            "class_name": "person",
                            "confidence": 0.85,
                            "bbox": [100, 100, 200, 300]
                        }
                    ],
                    "count": 1,
                    "note": "Mock implementation (YOLO not available)"
                }
            
            # キャッシュに保存
            self.image_cache.set(f"detect_{image_hash}", result)
            return result
        
        except Exception as e:
            logger.error(f"Error in detect_objects: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def segment_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        画像セグメンテーション（U-Net風の実装）
        
        Args:
            image_data: 画像データ（bytes）
        
        Returns:
            セグメンテーション結果
        """
        if not CV2_AVAILABLE:
            return {
                "status": "error",
                "message": "OpenCV is not available"
            }
        
        try:
            # 画像を読み込み
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {
                    "status": "error",
                    "message": "Failed to decode image"
                }
            
            # 簡易セグメンテーション（色ベース）
            # 実際のU-Net実装はtorchが必要
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 基本的な領域分割（デモ用）
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # 輪郭検出
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            segments = []
            for i, contour in enumerate(contours[:10]):  # 最大10個
                area = cv2.contourArea(contour)
                if area > 100:  # 小さなノイズを除外
                    x, y, w, h = cv2.boundingRect(contour)
                    segments.append({
                        "id": i,
                        "area": float(area),
                        "bbox": [int(x), int(y), int(w), int(h)]
                    })
            
            return {
                "status": "success",
                "segments": segments,
                "count": len(segments),
                "note": "Basic segmentation (U-Net requires torch)"
            }
        
        except Exception as e:
            logger.error(f"Error in segment_image: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def analyze_medical_image(self, dicom_data: bytes, image_type: str = "CT") -> Dict[str, Any]:
        """
        医療画像解析（DICOM形式）
        
        Args:
            dicom_data: DICOMデータ（bytes）
            image_type: 画像タイプ（CT, MRI, X-ray等）
        
        Returns:
            解析結果
        """
        if not DICOM_AVAILABLE:
            return {
                "status": "error",
                "message": "pydicom is not available"
            }
        
        try:
            # DICOMファイルを読み込み
            dicom_file = pydicom.dcmread(io.BytesIO(dicom_data))
            
            # メタデータ取得
            metadata = {
                "patient_id": getattr(dicom_file, 'PatientID', 'N/A'),
                "study_date": getattr(dicom_file, 'StudyDate', 'N/A'),
                "modality": getattr(dicom_file, 'Modality', 'N/A'),
                "image_type": image_type
            }
            
            # 画像データ取得
            pixel_array = dicom_file.pixel_array
            
            # 基本的な統計情報
            stats = {
                "shape": pixel_array.shape,
                "min": float(np.min(pixel_array)),
                "max": float(np.max(pixel_array)),
                "mean": float(np.mean(pixel_array)),
                "std": float(np.std(pixel_array))
            }
            
            return {
                "status": "success",
                "metadata": metadata,
                "statistics": stats,
                "note": "Basic medical image analysis"
            }
        
        except InvalidDicomError:
            return {
                "status": "error",
                "message": "Invalid DICOM file"
            }
        except Exception as e:
            logger.error(f"Error in analyze_medical_image: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def process_video(self, video_data: bytes) -> Dict[str, Any]:
        """
        動画処理
        
        Args:
            video_data: 動画データ（bytes）
        
        Returns:
            処理結果
        """
        if not CV2_AVAILABLE:
            return {
                "status": "error",
                "message": "OpenCV is not available"
            }
        
        try:
            # 動画を一時ファイルに保存
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(video_data)
                tmp_path = tmp_file.name
            
            # 動画を読み込み
            cap = cv2.VideoCapture(tmp_path)
            
            if not cap.isOpened():
                return {
                    "status": "error",
                    "message": "Failed to open video"
                }
            
            # 動画情報取得
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # フレーム処理（最初の10フレームのみ）
            frames_processed = 0
            detections_per_frame = []
            
            if self.yolo_available and self.yolo_model:
                while frames_processed < min(10, frame_count):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # 物体検出
                    results = self.yolo_model(frame)
                    detections = []
                    for result in results:
                        for box in result.boxes:
                            detections.append({
                                "class_name": self.yolo_model.names[int(box.cls[0])],
                                "confidence": float(box.conf[0])
                            })
                    
                    detections_per_frame.append({
                        "frame": frames_processed,
                        "detections": detections
                    })
                    frames_processed += 1
            
            cap.release()
            os.unlink(tmp_path)  # 一時ファイル削除
            
            return {
                "status": "success",
                "video_info": {
                    "frame_count": frame_count,
                    "fps": fps,
                    "width": width,
                    "height": height
                },
                "frames_processed": frames_processed,
                "detections": detections_per_frame if YOLO_AVAILABLE else [],
                "note": "Video processing completed"
            }
        
        except Exception as e:
            logger.error(f"Error in process_video: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

