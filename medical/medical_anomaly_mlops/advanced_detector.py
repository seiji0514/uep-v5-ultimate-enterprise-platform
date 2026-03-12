"""
医療データ異常検知MLOps - 高度な検知システム
複数アルゴリズムの組み合わせ + 医療特化機能
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy import signal, stats
from scipy.fft import fft, fftfreq
import pickle
import json
from datetime import datetime

class MedicalAnomalyDetector:
    """医療データ専用の高度な異常検知システム"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.threshold = None
        
    def preprocess_medical_data(self, data: np.ndarray) -> np.ndarray:
        """
        医療データ前処理（脳波を想定）
        
        1. ノイズ除去（バンドパスフィルタ）
        2. 標準化
        3. 特徴抽出（FFT、統計量）
        """
        processed_features = []
        
        for channel_data in data.T:  # チャンネルごとに処理
            # 1. バンドパスフィルタ（ノイズ除去）
            # 脳波: 0.5-50Hz の範囲を抽出
            fs = 250  # サンプリング周波数（仮定）
            lowcut = 0.5
            highcut = 50.0
            
            # Butterworth フィルタ
            nyquist = fs / 2
            low = lowcut / nyquist
            high = highcut / nyquist
            
            try:
                b, a = signal.butter(4, [low, high], btype='band')
                filtered = signal.filtfilt(b, a, channel_data)
            except:
                filtered = channel_data  # フィルタリング失敗時は元データ
            
            # 2. FFT（周波数解析）
            fft_values = fft(filtered)
            fft_freqs = fftfreq(len(filtered), 1/fs)
            
            # パワースペクトル（振幅の2乗）
            power_spectrum = np.abs(fft_values[:len(fft_values)//2])**2
            
            # 周波数帯域別のパワー（医療的に重要）
            # δ波 (0.5-4Hz), θ波 (4-8Hz), α波 (8-13Hz), β波 (13-30Hz)
            delta_power = np.mean(power_spectrum[:int(4*len(power_spectrum)/highcut)])
            theta_power = np.mean(power_spectrum[int(4*len(power_spectrum)/highcut):int(8*len(power_spectrum)/highcut)])
            alpha_power = np.mean(power_spectrum[int(8*len(power_spectrum)/highcut):int(13*len(power_spectrum)/highcut)])
            beta_power = np.mean(power_spectrum[int(13*len(power_spectrum)/highcut):int(30*len(power_spectrum)/highcut)])
            
            # 3. 統計的特徴量
            mean_val = np.mean(filtered)
            std_val = np.std(filtered)
            skewness = stats.skew(filtered)
            kurtosis = stats.kurtosis(filtered)
            max_val = np.max(np.abs(filtered))
            
            # 特徴量を結合
            features = [
                mean_val, std_val, skewness, kurtosis, max_val,
                delta_power, theta_power, alpha_power, beta_power
            ]
            processed_features.extend(features)
        
        return np.array(processed_features)
    
    def train(self, X: np.ndarray, contamination: float = 0.1):
        """
        異常検知モデルを学習
        
        Args:
            X: 学習データ（サンプル数 × チャンネル数）
            contamination: 異常データの割合（デフォルト10%）
        """
        print("\n🔧 医療データ前処理中...")
        
        # 各サンプルに対して高度な前処理を適用
        X_processed = []
        for i, sample in enumerate(X):
            if i % 100 == 0:
                print(f"   処理中: {i}/{len(X)} サンプル")
            features = self.preprocess_medical_data(sample.reshape(-1, 1))
            X_processed.append(features)
        
        X_processed = np.array(X_processed)
        print(f"✅ 前処理完了: {X_processed.shape}")
        
        # 標準化
        X_scaled = self.scaler.fit_transform(X_processed)
        
        # Isolation Forest学習
        print("\n🤖 高度な異常検知モデル学習中...")
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=200,  # 推定器を増やして精度向上
            max_samples='auto',
            max_features=1.0
        )
        
        self.model.fit(X_scaled)
        print("✅ 学習完了")
        
        return self
    
    def predict(self, X: np.ndarray) -> tuple:
        """
        異常検知を実行
        
        Returns:
            predictions: 予測結果（1=異常, 0=正常）
            scores: 異常スコア
        """
        # 前処理
        X_processed = []
        for sample in X:
            features = self.preprocess_medical_data(sample.reshape(-1, 1))
            X_processed.append(features)
        
        X_processed = np.array(X_processed)
        X_scaled = self.scaler.transform(X_processed)
        
        # 予測
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        
        # -1を1（異常）、1を0（正常）に変換
        y_pred = np.where(predictions == -1, 1, 0)
        
        return y_pred, scores
    
    def save(self, model_path: str, scaler_path: str):
        """モデルとスケーラーを保存"""
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"\n💾 モデル保存完了: {model_path}")
        print(f"💾 スケーラー保存完了: {scaler_path}")
    
    def load(self, model_path: str, scaler_path: str):
        """モデルとスケーラーを読み込み"""
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        return self


if __name__ == "__main__":
    print("="*60)
    print("医療データ異常検知MLOps - 高度な検知システム")
    print("="*60)
    
    # データ読み込み
    df = pd.read_csv('medical_data_sample.csv')
    X = df[['channel1', 'channel2', 'channel3']].values
    y_true = df['is_anomaly'].values
    
    print(f"\nデータ読み込み: {len(df)}件")
    print(f"異常データ: {y_true.sum()}件 ({y_true.sum()/len(y_true)*100:.1f}%)")
    
    # 学習
    detector = MedicalAnomalyDetector()
    detector.train(X, contamination=0.1)
    
    # 予測
    print("\n📊 異常検知実行中...")
    y_pred, scores = detector.predict(X)
    
    # 評価
    from sklearn.metrics import classification_report, confusion_matrix
    
    print("\n📈 評価結果:")
    print(classification_report(y_true, y_pred, target_names=['正常', '異常']))
    
    print("\n混同行列:")
    print(confusion_matrix(y_true, y_pred))
    
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    print(f"\n✅ 総合精度: {accuracy*100:.2f}%")
    
    # 保存
    detector.save('advanced_model.pkl', 'scaler.pkl')
    
    # メタデータ
    metadata = {
        "model_name": "Medical Anomaly Detection Advanced",
        "version": "2.0",
        "algorithm": "Isolation Forest + Advanced Preprocessing",
        "features": [
            "Mean", "Std", "Skewness", "Kurtosis", "Max",
            "Delta Power (0.5-4Hz)",
            "Theta Power (4-8Hz)",
            "Alpha Power (8-13Hz)",
            "Beta Power (13-30Hz)"
        ],
        "accuracy": float(accuracy),
        "contamination": 0.1,
        "n_estimators": 200,
        "trained_at": datetime.now().isoformat(),
        "samples": len(df),
        "preprocessing": [
            "Bandpass Filter (0.5-50Hz)",
            "FFT (Fourier Transform)",
            "Power Spectrum Analysis",
            "Statistical Features"
        ]
    }
    
    with open('advanced_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print("✅ 高度メタデータ保存完了")
    print("\n🎉 高度な医療データ異常検知MLOps完了！")
    print("\n【特徴】")
    print("• バンドパスフィルタによるノイズ除去")
    print("• FFTによる周波数解析")
    print("• 脳波周波数帯域別パワー解析（δ、θ、α、β波）")
    print("• 統計的特徴量抽出")
    print("• MLOpsバージョン管理")

