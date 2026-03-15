/**
 * 産業統合プラットフォーム 共通型定義
 */
import type { ReactNode } from 'react';

export interface TabPanelProps {
  children?: ReactNode;
  index: number;
  value: number;
}

export type LearnStep = {
  q: string;
  opts: string[];
  correct: number;
  correctReason?: string;
  wrongReasons?: string[]; // opts[i]が不正解のときの説明（i !== correct）
};
