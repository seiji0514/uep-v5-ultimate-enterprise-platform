#!/bin/sh
# Phase 4: Blue-Green switch - swap active deployment
# Usage: ./blue-green-switch.sh [blue|green]
TARGET=${1:-green}
kubectl scale deployment unified-platform-$TARGET --replicas=2
CURRENT=$([ "$TARGET" = "blue" ] && echo "green" || echo "blue")
kubectl scale deployment unified-platform-$CURRENT --replicas=0
echo "Switched to $TARGET. Update Ingress/Service to point to unified-platform-$TARGET."
