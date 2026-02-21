/**
 * WAT から WASM をビルド
 * npm run build:wasm
 * wat-compiler が未インストールの場合はスキップ（exit 0）
 */
const fs = require('fs');
const path = require('path');

try {
  const compile = require('wat-compiler');
  const watPath = path.join(__dirname, '../public/wasm/compute.wat');
  const wasmPath = path.join(__dirname, '../public/wasm/compute.wasm');
  const wat = fs.readFileSync(watPath, 'utf8');
  const buffer = compile(wat);
  fs.writeFileSync(wasmPath, Buffer.from(buffer));
  console.log('Built:', wasmPath);
} catch (e) {
  if (e.code === 'MODULE_NOT_FOUND') {
    console.log('wat-compiler not installed, skipping WASM build (JS fallback will be used)');
  } else {
    console.error('WASM build failed:', e.message);
  }
  process.exit(0); // ビルド全体は続行
}
