#!/bin/bash
# UEP v5.0 - ヘルスチェックスクリプト

echo "=========================================="
echo "UEP v5.0 - ヘルスチェック"
echo "=========================================="

echo ""
echo "1. Backend API (直接):"
curl -s http://localhost:8000/health | jq . || curl -s http://localhost:8000/health
echo ""

echo "2. Backend API (Kong経由):"
curl -s http://localhost:8002/api/v1/health | jq . || curl -s http://localhost:8002/api/v1/health
echo ""

echo "3. Backend API (Envoy経由):"
curl -s http://localhost:8080/api/v1/health | jq . || curl -s http://localhost:8080/api/v1/health
echo ""

echo "4. Kong Admin:"
curl -s http://localhost:8001/status | jq . || curl -s http://localhost:8001/status
echo ""

echo "5. Envoy Admin:"
curl -s http://localhost:9901/stats | head -20 || echo "Envoy Admin APIに接続できません"
echo ""

echo "6. Prometheus:"
curl -s http://localhost:9090/-/healthy || echo "Prometheusに接続できません"
echo ""

echo "7. Grafana:"
curl -s http://localhost:3000/api/health | jq . || echo "Grafanaに接続できません"
echo ""

echo "=========================================="
echo "ヘルスチェック完了"
echo "=========================================="
