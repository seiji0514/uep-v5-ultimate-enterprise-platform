/**
 * LearnPanel - 実務学習パネル共通コンポーネント
 */
import React from 'react';
import { Box, Typography, Paper, Stack, Button } from '@mui/material';
import { CheckCircle, ArrowForward } from '@mui/icons-material';
import type { LearnStep } from './types';

export interface LearnPanelProps {
  steps: LearnStep[];
  stepIndex: number;
  setStepIndex: (v: number | ((s: number) => number)) => void;
  selected: number | null;
  setSelected: (v: number | null) => void;
  feedback: 'correct' | 'wrong' | null;
  setFeedback: (v: 'correct' | 'wrong' | null) => void;
  onReset: () => void;
}

export function LearnPanel({
  steps,
  stepIndex,
  setStepIndex,
  selected,
  setSelected,
  feedback,
  setFeedback,
  onReset,
}: LearnPanelProps) {
  const step = steps[stepIndex];
  const isComplete = stepIndex >= steps.length;
  return (
    <Paper variant="outlined" sx={{ p: 2, bgcolor: 'action.hover' }}>
      <Typography variant="subtitle2" color="primary" gutterBottom>
        順番通りに進めれば実務が学べます（ステップ {Math.min(stepIndex + 1, steps.length)} / {steps.length}）
      </Typography>
      {!isComplete && step ? (
        <>
          <Typography variant="body1" sx={{ mb: 2 }}>{step.q}</Typography>
          <Stack spacing={1}>
            {step.opts.map((opt, i) => (
              <Button
                key={i}
                variant={selected === i ? 'contained' : 'outlined'}
                onClick={() => {
                  if (feedback === 'correct') return;
                  setSelected(i);
                  setFeedback(i === step.correct ? 'correct' : 'wrong');
                }}
                color={feedback === 'correct' && selected === i ? 'success' : feedback === 'wrong' && selected === i ? 'error' : 'primary'}
                startIcon={feedback && selected === i && i === step.correct ? <CheckCircle /> : undefined}
              >
                {i + 1}. {opt}
              </Button>
            ))}
          </Stack>
          {feedback === 'correct' && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="success.main" fontWeight={600}>正解です。</Typography>
              {step.correctReason && <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>【なぜ正解か】{step.correctReason}</Typography>}
              <Button size="small" variant="contained" endIcon={<ArrowForward />} sx={{ mt: 2 }} onClick={() => { setStepIndex((s) => s + 1); setSelected(null); setFeedback(null); }}>
                次へ
              </Button>
            </Box>
          )}
          {feedback === 'wrong' && selected !== null && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="error" fontWeight={600}>不正解です。</Typography>
              {step.wrongReasons && step.wrongReasons[selected] && <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>【なぜ間違いか】{step.wrongReasons[selected]}</Typography>}
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>もう一度選んでください。</Typography>
            </Box>
          )}
        </>
      ) : (
        <Box>
          <Typography variant="h6" color="success.main" gutterBottom><CheckCircle /> 完了</Typography>
          <Typography variant="body2">順番通りに進めることで実務が身につきます。</Typography>
          <Button sx={{ mt: 2 }} variant="outlined" onClick={onReset}>最初からやり直す</Button>
        </Box>
      )}
    </Paper>
  );
}
