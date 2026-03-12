# UEP v5.0 WebAssembly (WASM)

補強スキル: WebAssembly、オンデバイス AI、エッジ推論

## 概要

- ブラウザ内推論、エッジ推論のサポート
- Rust / C++ で WASM モジュールをビルドし、フロントエンドから呼び出し

## ディレクトリ構成

```
tools/wasm/
├── README.md          # 本ファイル
├── rust/              # Rust で WASM ビルド（例）
│   └── Cargo.toml
└── scripts/           # ビルドスクリプト
    └── build.sh
```

## セットアップ（Rust + wasm-pack）

```bash
# wasm-pack インストール
cargo install wasm-pack

# サンプルプロジェクト作成
cd tools/wasm
cargo new --lib rust-wasm
cd rust-wasm
# Cargo.toml に [lib] crate-type = ["cdylib"] を追加
wasm-pack build --target web
```

## フロントエンド連携

```javascript
// フロントエンドから WASM を読み込み
const wasm = await import('./pkg/rust_wasm.js');
await wasm.default();
// wasm.function_name() で呼び出し
```

## 参照

- [UEP_v5_追加スキル・技術案.md](../../docs/UEP_v5_追加スキル・技術案.md)
- [frontend/src/utils/onDeviceInference.ts](../../frontend/src/utils/onDeviceInference.ts) - オンデバイス推論
