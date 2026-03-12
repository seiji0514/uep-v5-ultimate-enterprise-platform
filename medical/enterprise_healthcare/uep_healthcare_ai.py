"""
医療AI（Healthcare AI）サービス
フェーズ4: ドメイン特化統合
- 医療画像解析: CT, MRI, X線画像処理（拡張版）
- 診断支援: 疾患分類、異常検知
- 医療データ処理: DICOM形式、HL7標準
"""
import logging
from typing import Dict, Any, Optional, List
import numpy as np

# DICOM（医療画像、必須）
try:
    import pydicom
    from pydicom.errors import InvalidDicomError
    DICOM_AVAILABLE = True
except ImportError:
    DICOM_AVAILABLE = False
    logging.warning("pydicom not available. Healthcare AI functionality will be limited.")

# scikit-learn（診断支援、必須）
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available. Diagnosis support will be limited.")

logger = logging.getLogger(__name__)


class HealthcareAIService:
    """医療AI（Healthcare AI）サービス"""
    
    def __init__(self):
        self.dicom_available = DICOM_AVAILABLE
        self.sklearn_available = SKLEARN_AVAILABLE
        self.diagnosis_model = None
    
    def is_available(self) -> bool:
        """サービスが利用可能かチェック"""
        return DICOM_AVAILABLE
    
    def analyze_medical_image(
        self,
        dicom_data: bytes,
        image_type: str = "CT"
    ) -> Dict[str, Any]:
        """
        医療画像解析（拡張版）
        
        Args:
            dicom_data: DICOMデータ（bytes）
            image_type: 画像タイプ（CT, MRI, X-ray）
        
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
                "image_type": image_type,
                "manufacturer": getattr(dicom_file, 'Manufacturer', 'N/A'),
                "study_description": getattr(dicom_file, 'StudyDescription', 'N/A')
            }
            
            # 画像データ取得
            pixel_array = dicom_file.pixel_array
            
            # 統計情報
            stats = {
                "shape": pixel_array.shape,
                "min": float(np.min(pixel_array)),
                "max": float(np.max(pixel_array)),
                "mean": float(np.mean(pixel_array)),
                "std": float(np.std(pixel_array)),
                "median": float(np.median(pixel_array))
            }
            
            # 異常検知（簡易版）
            # 実際には機械学習モデルを使用
            z_scores = np.abs((pixel_array - stats["mean"]) / stats["std"]) if stats["std"] > 0 else np.zeros_like(pixel_array)
            anomaly_pixels = np.sum(z_scores > 3.0)  # 3標準偏差以上
            
            return {
                "status": "success",
                "metadata": metadata,
                "statistics": stats,
                "anomaly_detection": {
                    "anomaly_pixel_count": int(anomaly_pixels),
                    "anomaly_ratio": float(anomaly_pixels / pixel_array.size) if pixel_array.size > 0 else 0.0,
                    "note": "Basic anomaly detection (ML model recommended for accurate results)"
                }
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
    
    def support_diagnosis(
        self,
        patient_data: Dict[str, Any],
        symptoms: List[str]
    ) -> Dict[str, Any]:
        """
        診断支援
        
        Args:
            patient_data: 患者データ
            symptoms: 症状リスト
        
        Returns:
            診断支援結果
        """
        if not SKLEARN_AVAILABLE:
            return {
                "status": "error",
                "message": "scikit-learn is not available"
            }
        
        try:
            # 簡易的な診断支援（ルールベース）
            # 実際には機械学習モデルを使用
            
            symptom_scores = {}
            common_diseases = {
                "fever": ["influenza", "common_cold", "pneumonia"],
                "cough": ["influenza", "common_cold", "pneumonia", "asthma"],
                "headache": ["migraine", "tension_headache", "sinusitis"],
                "fatigue": ["anemia", "depression", "chronic_fatigue"]
            }
            
            # 症状から疾患の可能性を計算
            disease_scores = {}
            for symptom in symptoms:
                if symptom.lower() in common_diseases:
                    for disease in common_diseases[symptom.lower()]:
                        disease_scores[disease] = disease_scores.get(disease, 0) + 1
            
            # スコアでソート
            sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = [
                {
                    "disease": disease,
                    "probability": min(score / len(symptoms), 1.0),
                    "recommended_tests": self._get_recommended_tests(disease)
                }
                for disease, score in sorted_diseases[:5]
            ]
            
            return {
                "status": "success",
                "patient_id": patient_data.get("patient_id", "unknown"),
                "symptoms": symptoms,
                "recommendations": recommendations,
                "note": "Basic diagnosis support (ML model recommended for accurate results)"
            }
        
        except Exception as e:
            logger.error(f"Error in support_diagnosis: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _get_recommended_tests(self, disease: str) -> List[str]:
        """推奨検査を取得（簡易版）"""
        test_mapping = {
            "influenza": ["rapid_influenza_test", "blood_test"],
            "pneumonia": ["chest_xray", "blood_test", "sputum_culture"],
            "asthma": ["spirometry", "chest_xray"],
            "anemia": ["complete_blood_count", "iron_studies"]
        }
        return test_mapping.get(disease, ["general_blood_test"])
    
    def detect_anomalies_medical(self, medical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        医療データ異常検知
        
        Args:
            medical_data: 医療データ（バイタルサイン、検査値等）
        
        Returns:
            異常検知結果
        """
        if not SKLEARN_AVAILABLE:
            return {
                "status": "error",
                "message": "scikit-learn is not available"
            }
        
        try:
            # バイタルサインを取得
            vital_signs = medical_data.get("vital_signs", {})
            
            # 正常範囲
            normal_ranges = {
                "temperature": (36.0, 37.5),  # 摂氏
                "heart_rate": (60, 100),  # bpm
                "blood_pressure_systolic": (90, 140),  # mmHg
                "blood_pressure_diastolic": (60, 90),  # mmHg
                "respiratory_rate": (12, 20),  # per minute
                "oxygen_saturation": (95, 100)  # %
            }
            
            anomalies = []
            for sign, value in vital_signs.items():
                if sign in normal_ranges:
                    min_val, max_val = normal_ranges[sign]
                    if value < min_val or value > max_val:
                        anomalies.append({
                            "vital_sign": sign,
                            "value": float(value),
                            "normal_range": [min_val, max_val],
                            "severity": "high" if abs(value - (min_val + max_val) / 2) > (max_val - min_val) else "medium"
                        })
            
            return {
                "status": "success",
                "patient_id": medical_data.get("patient_id", "unknown"),
                "anomalies": anomalies,
                "anomaly_count": len(anomalies),
                "overall_status": "critical" if len(anomalies) >= 2 else "normal" if len(anomalies) == 0 else "attention_required"
            }
        
        except Exception as e:
            logger.error(f"Error in detect_anomalies_medical: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

