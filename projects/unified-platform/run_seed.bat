@echo off
cd /d "%~dp0"
docker compose exec -T app python -c "from seed_data import seed; seed(); print('OK')"
