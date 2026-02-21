/**
 * WebAssembly 計算モジュール
 * フロントエンドの計算処理を WASM で実行
 * WASM が利用できない場合は JS フォールバック
 */

const WASM_URL = process.env.PUBLIC_URL
  ? `${process.env.PUBLIC_URL}/wasm/compute.wasm`
  : '/wasm/compute.wasm';

let wasmModule: {
  add: (a: number, b: number) => number;
  multiply: (a: number, b: number) => number;
  sum: (n: number) => number;
} | null = null;

/** JS フォールバック実装 */
const jsFallback = {
  add: (a: number, b: number) => a + b,
  multiply: (a: number, b: number) => a * b,
  sum: (n: number) => (n * (n - 1)) / 2,
};

/**
 * WASM モジュールをロード
 */
export async function loadWasm(): Promise<boolean> {
  if (wasmModule) return true;
  try {
    const res = await fetch(WASM_URL);
    if (!res.ok) {
      wasmModule = jsFallback;
      return false;
    }
    const buffer = await res.arrayBuffer();
    const { instance } = await WebAssembly.instantiate(buffer);
    wasmModule = {
      add: (instance.exports.add as (a: number, b: number) => number),
      multiply: (instance.exports.multiply as (a: number, b: number) => number),
      sum: (instance.exports.sum as (n: number) => number),
    };
    return true;
  } catch {
    wasmModule = jsFallback;
    return false;
  }
}

/**
 * WASM で加算（未ロード時は JS フォールバック）
 */
export function wasmAdd(a: number, b: number): number {
  if (!wasmModule) return jsFallback.add(a, b);
  return wasmModule.add(a, b);
}

/**
 * WASM で乗算
 */
export function wasmMultiply(a: number, b: number): number {
  if (!wasmModule) return jsFallback.multiply(a, b);
  return wasmModule.multiply(a, b);
}

/**
 * WASM で 0..n-1 の合計
 */
export function wasmSum(n: number): number {
  if (!wasmModule) return jsFallback.sum(n);
  return wasmModule.sum(n);
}

/** WASM ロード済みか */
export function isWasmLoaded(): boolean {
  return wasmModule !== null && wasmModule !== jsFallback;
}
