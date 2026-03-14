/**
 * 自動切替ナレーション用フック
 * 各モジュールページで使用し、ナレーション後に次へ遷移
 */
import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { AUTO_PLAY_STEPS, AutoPlayStepIndex, useAutoPlay } from '../contexts/AutoPlayContext';
import { speak } from '../lib/speech';

export const useAutoPlayNarration = (stepIndex: AutoPlayStepIndex) => {
  const location = useLocation();
  const ctx = useAutoPlay();
  const isAutoPlaying = ctx?.isAutoPlaying ?? false;
  const currentStep = ctx?.currentStep ?? 0;
  const narrationEnabled = ctx?.narrationEnabled ?? true;
  const navigateToNextStep = ctx?.navigateToNextStep ?? (() => {});
  const hasPlayedRef = useRef(false);

  // 遷移時に state で渡された step も参照（currentStep の更新タイミング対策）
  const stateStep = (location.state as { autoPlayStep?: number })?.autoPlayStep;
  const shouldSpeak = isAutoPlaying && narrationEnabled && (currentStep === stepIndex || stateStep === stepIndex);

  useEffect(() => {
    if (!shouldSpeak) return;
    if (hasPlayedRef.current) return;
    hasPlayedRef.current = true;

    const step = AUTO_PLAY_STEPS[stepIndex];
    if (!step) return;

    speak(step.narration, 'ja-JP', () => {
      setTimeout(navigateToNextStep, 1500);
    });

    return () => {
      hasPlayedRef.current = false;
    };
  }, [shouldSpeak, stepIndex, navigateToNextStep]);
};
