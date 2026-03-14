/**
 * 自動切替・ナレーション用コンテキスト
 * 5モジュール概要 → 詳細説明 → 製造・IoT → 医療 → 金融・FinTech → インクルーシブ雇用AI → 契約ワークフロー
 */
import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { cancelSpeech, pauseSpeech, resumeSpeech, isPaused as speechIsPaused } from '../lib/speech';

export const AUTO_PLAY_STEPS = [
  { path: '/integrated-modules', title: '5モジュール概要', narration: '統合基盤モジュール、5つのモジュールの概要です。製造・IoT、医療、金融、障害者雇用、契約ワークフローを順にご紹介します。顧客PoC、ピーオーシーでは、各領域の実データ連携に置き換えて検証可能です。' },
  { path: '/integrated-modules/detail', title: '詳細説明', narration: '想定ユースケース。製造と契約の連携で、予知保全アラートから発注フローを自動起動。医療と障害者雇用で、病院の採用マッチングを支援。金融と製造で、設備投資の融資判断を支援。システム構成は、React、FastAPI、各モジュールAPIがRESTで連携。Prometheusでメトリクス収集、Grafanaで可視化。データの出処は、製造はNASA C-MAPSSなど公開データ、契約は実データ運用中、他はPoCで実データ連携可能。公開データの拡張として、MIMIC-III、PhysioNet、Kaggle、厚労省オープンデータなどが利用可能です。' },
  { path: '/manufacturing', title: '製造・IoT', narration: '製造・MLOps。予知保全、センサーデータ、異常検知を提供。製造業DXの需要が高い。設備の残余寿命予測やIoT連携に対応。NASA C-MAPSS、シーマップスなど公開データで実機モードに対応済み。' },
  { path: '/medical', title: '医療', narration: '医療。AI診断支援、音声応答、異常検知機能。MLOps基盤との連携により、医療データの分析・可視化をサポート。患者情報の規制により、デモではサンプルデータを使用。顧客PoCでは実データ連携に置き換えて検証可能。' },
  { path: '/fintech', title: '金融・FinTech', narration: '金融・FinTech。決済API、リスクスコア、取引監視を提供。高可用性・低レイテンシの金融システム基盤。決済・取引データの機密性により、デモではサンプルデータを使用。顧客PoCでは実データ連携に置き換えて検証可能。' },
  { path: '/inclusive-work', title: 'インクルーシブ雇用AI', narration: '障害者雇用。マッチング、アクセシビリティ特化AI、UX評価を統合。インクルーシブな雇用を支援。求人データの提供元との契約が必要。個人開発のデモでは実データの取得が難しいためサンプルを使用。顧客PoCでは実データ連携に置き換えて検証可能。' },
  { path: '/contract-workflow', title: '契約ワークフロー', narration: '契約ワークフロー。見積・契約・納品・請求を一気通貫で管理。DB化・PDF出力・実データ運用に対応。もともと実データのみで運用。' },
] as const;

export type AutoPlayStepIndex = 0 | 1 | 2 | 3 | 4 | 5 | 6;

interface AutoPlayContextType {
  isAutoPlaying: boolean;
  currentStep: AutoPlayStepIndex;
  narrationEnabled: boolean;
  hidePlayBar: boolean;
  isPaused: boolean;
  startAutoPlay: () => void;
  stopAutoPlay: () => void;
  togglePause: () => void;
  setNarrationEnabled: (v: boolean) => void;
  setHidePlayBar: (v: boolean) => void;
  navigateToNextStep: () => void;
}

const AutoPlayContext = createContext<AutoPlayContextType | undefined>(undefined);

export const useAutoPlay = () => {
  const ctx = useContext(AutoPlayContext);
  return ctx;
};

interface AutoPlayProviderProps {
  children: ReactNode;
}

export const AutoPlayProvider: React.FC<AutoPlayProviderProps> = ({ children }) => {
  const navigate = useNavigate();
  const [isAutoPlaying, setIsAutoPlaying] = useState(false);
  const [currentStep, setCurrentStep] = useState<AutoPlayStepIndex>(0);
  const [narrationEnabled, setNarrationEnabled] = useState(true);
  const [hidePlayBar, setHidePlayBar] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  const startAutoPlay = useCallback(() => {
    setIsAutoPlaying(true);
    setCurrentStep(0);
  }, []);

  const stopAutoPlay = useCallback(() => {
    cancelSpeech();
    setIsAutoPlaying(false);
    setIsPaused(false);
  }, []);

  const togglePause = useCallback(() => {
    if (speechIsPaused()) {
      resumeSpeech();
      setIsPaused(false);
    } else {
      pauseSpeech();
      setIsPaused(true);
    }
  }, []);

  const navigateToNextStep = useCallback(() => {
    setIsPaused(false);
    const next = (AUTO_PLAY_STEPS[currentStep + 1] as typeof AUTO_PLAY_STEPS[number] | undefined);
    if (next) {
      const nextStep = (currentStep + 1) as AutoPlayStepIndex;
      setCurrentStep(nextStep);
      // currentStep の更新を反映してから遷移（ナレーション用フックが正しく発火するよう遅延）
      setTimeout(() => navigate(next.path, { state: { autoPlayStep: nextStep } }), 50);
    } else {
      setIsAutoPlaying(false);
      navigate('/integrated-modules');
    }
  }, [currentStep, navigate]);

  return (
    <AutoPlayContext.Provider
      value={{
        isAutoPlaying,
        currentStep,
        narrationEnabled,
        hidePlayBar,
        isPaused,
        setNarrationEnabled,
        setHidePlayBar,
        startAutoPlay,
        stopAutoPlay,
        togglePause,
        navigateToNextStep,
      }}
    >
      {children}
    </AutoPlayContext.Provider>
  );
};
