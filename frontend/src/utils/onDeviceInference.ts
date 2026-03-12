/**
 * 端末内AI（オンデバイス）推論
 * APIが利用できない場合のローカルフォールバック
 * プライバシー重視: データをサーバに送信せずブラウザ内で処理
 */

export interface OnDeviceResult {
  text: string;
  source: 'on-device';
  confidence: number;
}

const DEMO_RESPONSES: Record<string, string> = {
  'uep': 'UEP v5.0は次世代エンタープライズ統合プラットフォームです。Level 1〜5の統合、MLOps、生成AI、セキュリティコマンドセンター等を統合しています。',
  'mlops': 'MLOpsは機械学習の運用基盤です。モデル管理、パイプライン、実験追跡、A/Bテストを統合します。',
  'rag': 'RAG（Retrieval-Augmented Generation）は、検索と生成を組み合わせたAI手法です。ChromaDB等のベクトルDBで文脈を検索し、LLMで回答を生成します。',
  'セキュリティ': 'UEP v5.0のセキュリティ基盤には、Zero Trust、mTLS、JWT、RBAC/ABAC、Vaultが含まれます。',
  'デモ': 'オフライン時は端末内AI（オンデバイス）で簡易応答を返します。データはサーバに送信されません。',
};

/**
 * 端末内で簡易推論を実行（オフライン・API失敗時のフォールバック）
 */
export function onDeviceInference(input: string): OnDeviceResult {
  const lower = input.toLowerCase().trim();
  if (!lower) {
    return { text: '入力が空です。', source: 'on-device', confidence: 0 };
  }

  for (const [key, response] of Object.entries(DEMO_RESPONSES)) {
    if (lower.includes(key)) {
      return { text: response, source: 'on-device', confidence: 0.7 };
    }
  }

  return {
    text: `[端末内AI] 「${input.slice(0, 50)}${input.length > 50 ? '...' : ''}」への簡易応答です。詳細はオンライン時にAPIをご利用ください。`,
    source: 'on-device',
    confidence: 0.3,
  };
}

/**
 * API利用可否を簡易チェック
 */
export function isApiAvailable(): boolean {
  return navigator.onLine;
}
