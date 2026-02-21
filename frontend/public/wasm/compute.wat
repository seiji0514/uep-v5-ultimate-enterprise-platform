;; UEP v5.0 - WebAssembly 計算モジュール
;; シンプルな加算・乗算（デモ用）
(module
  (func $add (export "add") (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.add
  )
  (func $multiply (export "multiply") (param $a i32) (param $b i32) (result i32)
    local.get $a
    local.get $b
    i32.mul
  )
  (func $sum (export "sum") (param $n i32) (result i32)
    (local $i i32)
    (local $acc i32)
    i32.const 0
    local.set $acc
    i32.const 0
    local.set $i
    (block $exit
      (loop $loop
        local.get $i
        local.get $n
        i32.ge_s
        br_if $exit
        local.get $acc
        local.get $i
        i32.add
        local.set $acc
        local.get $i
        i32.const 1
        i32.add
        local.set $i
        br $loop
      )
    )
    local.get $acc
  )
)
