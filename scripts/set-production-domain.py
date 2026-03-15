#!/usr/bin/env python3
"""
本番ドメインを一括設定
Usage: python scripts/set-production-domain.py your-domain.com
Example: python scripts/set-production-domain.py uep.mycompany.co.jp
"""
import os
import re
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/set-production-domain.py <domain>")
        print("Example: python scripts/set-production-domain.py uep.mycompany.co.jp")
        sys.exit(1)
    
    domain = sys.argv[1].strip().lower()
    if not domain:
        print("Error: domain cannot be empty")
        sys.exit(1)
    
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Backend .env
    backend_env = os.path.join(base, "backend", ".env")
    if os.path.exists(backend_env):
        with open(backend_env, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r"CORS_ORIGINS=.*",
            f"CORS_ORIGINS=https://{domain},https://app.{domain},http://localhost:3000,http://localhost:3018,http://127.0.0.1:3000",
            content
        )
        with open(backend_env, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {backend_env}")
    
    # Frontend .env.production
    frontend_env = os.path.join(base, "frontend", ".env.production")
    if os.path.exists(frontend_env):
        with open(frontend_env, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r"REACT_APP_API_URL=.*",
            f"REACT_APP_API_URL=https://api.{domain}",
            content
        )
        content = re.sub(
            r"REACT_APP_INDUSTRY_UNIFIED_URL=.*",
            f"REACT_APP_INDUSTRY_UNIFIED_URL=https://industry.{domain}",
            content
        )
        content = re.sub(
            r"REACT_APP_EOH_URL=.*",
            f"REACT_APP_EOH_URL=https://eoh.{domain}",
            content
        )
        with open(frontend_env, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {frontend_env}")
    
    print(f"\nDone. Domain set to: {domain}")
    print("  - API: https://api." + domain)
    print("  - Frontend: https://" + domain + ", https://app." + domain)

if __name__ == "__main__":
    main()
