# eBPF 観測サンプル（BCC / bpftrace）

補強スキル: eBPF（Cilium、Falco、BCC、bpftrace）

## 前提

- Linux カーネル 4.1+
- BCC: `sudo apt install bpfcc-tools` (Ubuntu)
- bpftrace: `sudo apt install bpftrace` (Ubuntu)

## bpftrace サンプル

### 1. システムコール追跡（openat）

```bash
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'
```

### 2. TCP 接続追跡

```bash
sudo bpftrace -e 'tracepoint:net:netif_receive_skb /args->len > 0/ { printf("packet %d bytes\n", args->len); }'
```

### 3. プロセス起動追跡

```bash
sudo bpftrace -e 'tracepoint:sched:sched_process_exec { printf("exec: %s\n", comm); }'
```

## BCC サンプル（Python）

`opensnoop.py` 等は BCC に同梱。カスタム例:

```python
#!/usr/bin/env python3
# BCC 例: open システムコールを追跡
from bcc import BPF
bpf = BPF(text='''
int trace_open(struct pt_regs *ctx) {
    bpf_trace_printk("open called\\n");
    return 0;
}
''')
bpf.attach_kprobe(event="do_sys_openat2", fn_name="trace_open")
bpf.trace_print()
```

## Falco

Falco は `docker-compose --profile security up` で起動。
ルール: `infrastructure/falco/falco_rules_uep.yaml`
