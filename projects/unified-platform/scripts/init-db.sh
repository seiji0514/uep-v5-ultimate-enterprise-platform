#!/bin/sh
# Phase 1: Init DB + Seed
set -e
cd "$(dirname "$0")/.."
export DATABASE_URL_SYNC="postgresql://unified:unified@${DB_HOST:-localhost}:5432/unified"
python seed_data.py
