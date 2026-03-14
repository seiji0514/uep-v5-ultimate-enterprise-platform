/**
 * Web Speech API ユーティリティ
 */
const getJapaneseVoice = (): SpeechSynthesisVoice | null => {
  if (typeof window === 'undefined' || !window.speechSynthesis) return null;
  const voices = window.speechSynthesis.getVoices();
  const ja = voices.filter((v) => v.lang.startsWith('ja'));
  return ja.length > 0 ? ja[0] : null;
};

export const speak = (text: string, lang = 'ja-JP', onEnd?: () => void): boolean => {
  if (typeof window === 'undefined' || !window.speechSynthesis) return false;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = lang;
  u.rate = 0.9;
  u.volume = 1;
  const voice = getJapaneseVoice();
  if (voice) u.voice = voice;
  if (onEnd) u.onend = onEnd;
  u.onerror = (e) => console.warn('SpeechSynthesis error:', e);
  window.speechSynthesis.speak(u);
  return true;
};

export const cancelSpeech = () => {
  if (typeof window !== 'undefined' && window.speechSynthesis) {
    window.speechSynthesis.cancel();
  }
};

export const pauseSpeech = () => {
  if (typeof window !== 'undefined' && window.speechSynthesis) {
    window.speechSynthesis.pause();
  }
};

export const resumeSpeech = () => {
  if (typeof window !== 'undefined' && window.speechSynthesis) {
    window.speechSynthesis.resume();
  }
};

export const isSpeaking = (): boolean => {
  if (typeof window === 'undefined' || !window.speechSynthesis) return false;
  return window.speechSynthesis.speaking;
};

export const isPaused = (): boolean => {
  if (typeof window === 'undefined' || !window.speechSynthesis) return false;
  return window.speechSynthesis.paused;
};

/** 複数テキストを順に読み上げ、各読み上げ前に onBefore を実行（スクロール連動用） */
export const speakSequence = (
  items: { text: string; onBefore?: () => void }[],
  lang = 'ja-JP',
  onAllEnd?: () => void
): boolean => {
  if (typeof window === 'undefined' || !window.speechSynthesis || items.length === 0) return false;
  window.speechSynthesis.cancel();

  let index = 0;
  const playNext = () => {
    if (index >= items.length) {
      onAllEnd?.();
      return;
    }
    const item = items[index];
    item.onBefore?.();
    const voice = getJapaneseVoice();
    const u = new SpeechSynthesisUtterance(item.text);
    u.lang = lang;
    u.rate = 0.9;
    u.volume = 1;
    if (voice) u.voice = voice;
    u.onend = () => {
      index++;
      setTimeout(playNext, 400);
    };
    u.onerror = () => {
      index++;
      setTimeout(playNext, 400);
    };
    window.speechSynthesis.speak(u);
  };
  setTimeout(playNext, 300);
  return true;
};
