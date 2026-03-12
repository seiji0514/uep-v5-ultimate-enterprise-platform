#!/bin/bash
# Docker 自動起動を ~/.bashrc に追加
# 実行: bash scripts/wsl-docker-autostart.sh

BASHRC="$HOME/.bashrc"
MARKER="# Docker auto-start (UEP)"

if grep -q "Docker auto-start (UEP)" "$BASHRC" 2>/dev/null; then
    echo "Docker 自動起動は既に設定済みです"
else
    cat >> "$BASHRC" << 'EOF'

# Docker auto-start (UEP)
if service docker status 2>&1 | grep -q "is not running"; then
    sudo service docker start 2>/dev/null
fi
EOF
    echo "~/.bashrc に Docker 自動起動を追加しました"
fi
