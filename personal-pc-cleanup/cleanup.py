#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
個人用 PC 容量確保ツール
- Docker クリーンアップ
- Cドライブ容量確保（一時ファイル、開発キャッシュ等）

UEP v5.0・産業統合・EOH とは無関係のスタンドアロン版
"""
import os
import sys

# Windows で日本語表示
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

# Cドライブ
C_DRIVE = Path("C:/")
USER_PROFILE = Path(os.environ.get("USERPROFILE", "C:/Users"))
LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", USER_PROFILE / "AppData" / "Local"))
TEMP_DIR = Path(os.environ.get("TEMP", LOCALAPPDATA / "Temp"))
WINDOWS_TEMP = Path("C:/Windows/Temp")

# 検出対象（Cドライブ内）
# フォルダ名, 説明, 再生成方法, 削除可否（safe=削除可, caution=注意・データ消える可能性）
CLEANUP_TARGETS = [
    ("node_modules", "npm パッケージ", "npm install", "safe"),
    ("venv", "Python 仮想環境", "pip install -r requirements.txt", "safe"),
    (".venv", "Python 仮想環境", "pip install -r requirements.txt", "safe"),
    ("__pycache__", "Python キャッシュ", "自動生成", "safe"),
    (".pytest_cache", "Pytest キャッシュ", "自動生成", "safe"),
    ("build", "ビルド成果物", "npm run build", "safe"),
    ("dist", "ビルド成果物", "再ビルド", "safe"),
    ("htmlcov", "カバレッジ", "pytest --cov", "safe"),
    (".next", "Next.js キャッシュ", "npm run build", "safe"),
    (".nuxt", "Nuxt キャッシュ", "npm run build", "safe"),
    (".cache", "各種キャッシュ", "自動生成", "safe"),
    ("minio_data", "MinIO データ", "Docker起動時", "caution"),
    ("postgres_data", "PostgreSQL データ", "Docker起動時", "caution"),
    ("prometheus_data", "Prometheus データ", "Docker起動時", "caution"),
    ("grafana_data", "Grafana データ", "Docker起動時", "caution"),
]

# スキャン対象のベースパス（Cドライブ内）
SCAN_BASES = [
    USER_PROFILE,
    C_DRIVE / "Projects" if (C_DRIVE / "Projects").exists() else None,
    C_DRIVE / "dev" if (C_DRIVE / "dev").exists() else None,
]
SCAN_BASES = [p for p in SCAN_BASES if p and p.exists()]

# 除外パス（.git 等は絶対削除しない）
EXCLUDE_PARTS = [".git", "AppData\\Local\\Docker", "Program Files", "Program Files (x86)"]


def format_size_mb(mb: float) -> str:
    if mb >= 1024:
        return f"{mb / 1024:.1f} GB"
    return f"{mb:.1f} MB"


def get_dir_size_mb(path: Path) -> float:
    """フォルダのサイズを MB で取得"""
    try:
        total = 0
        for entry in path.rglob("*"):
            try:
                if entry.is_file():
                    total += entry.stat().st_size
            except (PermissionError, OSError):
                pass
        return total / (1024 * 1024)
    except (PermissionError, OSError):
        return 0.0


def get_file_size_mb(path: Path) -> float:
    try:
        return path.stat().st_size / (1024 * 1024)
    except (PermissionError, OSError):
        return 0.0


def should_exclude(full_path: str) -> bool:
    for part in EXCLUDE_PARTS:
        if part in full_path:
            return True
    return False


def scan_c_drive(max_depth: int = 12) -> List[Tuple[str, float, str, str]]:
    """Cドライブ内の削除候補をスキャン（max_depth: スキャン深度制限）"""
    found = []
    seen = set()
    target_names = {t[0] for t in CLEANUP_TARGETS}

    for base in SCAN_BASES:
        if not base.exists():
            continue
        try:
            base_parts = len(base.parts)
            for root, dirs, _ in os.walk(base, topdown=True):
                root_path = Path(root)
                # 深度制限（深すぎるパスはスキップ）
                if len(root_path.parts) - base_parts > max_depth:
                    dirs.clear()
                    continue
                # 除外パスをスキップ
                dirs[:] = [d for d in dirs if not should_exclude(str(root_path / d))]
                for d in dirs:
                    if d in target_names:
                        full = root_path / d
                        key = str(full).lower()
                        if key in seen:
                            continue
                        seen.add(key)
                        if full.exists() and full.is_dir():
                            size = get_dir_size_mb(full)
                            if size > 0.1:
                                tup = next((t for t in CLEANUP_TARGETS if t[0] == d), (d, "不明", "-", "safe"))
                                desc, safe = tup[1], tup[3]
                                found.append((str(full), size, desc, safe))
        except PermissionError:
            pass
    return found


def scan_temp_dirs() -> List[Tuple[str, float, str, str]]:
    """一時フォルダをスキャン（safe=削除可）"""
    found = []
    for path, desc in [
        (TEMP_DIR, "ユーザー一時フォルダ"),
        (LOCALAPPDATA / "Temp", "LocalAppData Temp"),
        (USER_PROFILE / "AppData" / "Local" / "Microsoft" / "Windows" / "INetCache", "IE/Edge キャッシュ"),
    ]:
        if path.exists():
            try:
                size = get_dir_size_mb(path)
                if size > 1:
                    found.append((str(path), size, desc, "safe"))
            except PermissionError:
                pass
    return found


def docker_available() -> bool:
    try:
        subprocess.run(
            ["docker", "version"],
            capture_output=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def docker_df() -> Optional[str]:
    """Docker のディスク使用量を取得"""
    try:
        r = subprocess.run(
            ["docker", "system", "df", "-v"],
            capture_output=True,
            text=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def docker_prune(dry_run: bool = True) -> Tuple[bool, str]:
    """Docker クリーンアップ（未使用コンテナ・イメージ・ボリューム・ビルドキャッシュ）"""
    if dry_run:
        return True, "（dry-run: 実際には削除しません）"
    try:
        # 段階的に実行
        for cmd, desc in [
            (["docker", "container", "prune", "-f"], "停止中コンテナ"),
            (["docker", "image", "prune", "-a", "-f"], "未使用イメージ"),
            (["docker", "volume", "prune", "-f"], "未使用ボリューム"),
            (["docker", "builder", "prune", "-a", "-f"], "ビルドキャッシュ"),
        ]:
            subprocess.run(
                cmd,
                capture_output=True,
                timeout=120,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )
        return True, "Docker クリーンアップ完了"
    except Exception as e:
        return False, str(e)


def delete_path(path: str) -> Tuple[bool, str]:
    """パスを削除"""
    p = Path(path)
    if not p.exists():
        return False, "存在しません"
    try:
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        return True, "削除完了"
    except Exception as e:
        return False, str(e)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="個人用 PC 容量確保ツール")
    parser.add_argument("--detect", action="store_true", help="検出のみ（削除しない）")
    parser.add_argument("--clean", action="store_true", help="削除を実行")
    parser.add_argument("--docker", action="store_true", help="Docker クリーンアップを実行")
    parser.add_argument("--c-drive", action="store_true", help="Cドライブの開発キャッシュ等をスキャン")
    parser.add_argument("--temp", action="store_true", help="一時フォルダをスキャン")
    parser.add_argument("--all", action="store_true", help="全スキャン（デフォルト）")
    args = parser.parse_args()

    if not args.detect and not args.clean and not args.docker:
        args.detect = True

    do_scan = args.c_drive or args.temp or args.all or (not args.docker)
    do_docker = args.docker or args.all

    print("=" * 50)
    print("個人用 PC 容量確保ツール")
    print("=" * 50)

    # Cドライブ空き容量
    try:
        total, used, free = shutil.disk_usage(C_DRIVE)
        print(f"\n[Cドライブ] 空き: {format_size_mb(free / (1024*1024))} / 合計: {format_size_mb(total / (1024*1024))}")
    except Exception:
        pass

    # Docker
    if do_docker:
        print("\n--- Docker ---")
        if docker_available():
            df_out = docker_df()
            if df_out:
                for line in df_out.splitlines()[:15]:
                    print(line)
            if args.clean:
                ok, msg = docker_prune(dry_run=False)
                print(f"\n{msg}")
            elif args.detect:
                print("\nDocker クリーンアップ: --clean で実行すると docker container/image/volume/builder prune を実行します")
        else:
            print("Docker がインストールされていないか、起動していません")

    # Cドライブ・一時フォルダ
    if do_scan:
        all_found = []
        if args.temp or args.all:
            all_found.extend(scan_temp_dirs())
        if args.c_drive or args.all:
            all_found.extend(scan_c_drive())

        if all_found:
            total_mb = sum(f[1] for f in all_found)
            print(f"\n--- 削除候補（合計: {format_size_mb(total_mb)}）---")
            print("  [safe]=削除可（再生成可能） [caution]=注意（データ消える可能性）")
            for item in sorted(all_found, key=lambda x: -x[1]):
                path, size, desc, safe = item[0], item[1], item[2], item[3]
                tag = "[safe]" if safe == "safe" else "[caution]"
                print(f"  {format_size_mb(size):>10}  {tag:10}  {desc:20}  {path[:50]}...")
            if args.clean:
                confirm = input("\n上記を削除しますか？ (y/N): ")
                if confirm.lower() == "y":
                    freed = 0
                    for item in all_found:
                        path, size = item[0], item[1]
                        ok, msg = delete_path(path)
                        if ok:
                            freed += size
                            print(f"  [OK] {path[:50]}...")
                        else:
                            print(f"  [NG] {path[:50]}... {msg}")
                    print(f"\n約 {format_size_mb(freed)} を解放しました")
        else:
            print("\n削除候補は検出されませんでした")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
