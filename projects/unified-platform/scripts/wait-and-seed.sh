#!/bin/sh
# Wait for DB then seed
set -e
until python -c "
import os
import socket
s = socket.socket()
try:
    s.connect((os.getenv('DB_HOST','db'), 5432))
    s.close()
    exit(0)
except: exit(1)
" 2>/dev/null; do
  echo "Waiting for DB..."
  sleep 2
done
echo "DB ready. Seeding..."
python seed_data.py
exec uvicorn main:app --host 0.0.0.0 --port 8000
