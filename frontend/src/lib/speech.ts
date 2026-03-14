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
