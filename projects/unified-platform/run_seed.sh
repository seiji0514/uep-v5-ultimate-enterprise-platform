#!/usr/bin/env bash
cd "$(dirname "$0" | tr -d '\r')"
docker compose exec -T app python -c "from seed_data import seed; seed(); print('OK')"
