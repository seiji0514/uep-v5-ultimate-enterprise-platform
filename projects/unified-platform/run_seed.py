#!/usr/bin/env python3
"""Seed runner - call from host: docker compose exec -T app python run_seed.py"""
from seed_data import seed
seed()
print("OK")
