#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高度衛星軌道追跡システム - テスト実行ランチャー
"""
import subprocess
import sys
import os

def main():
    print("=" * 50)
    print("高度衛星軌道追跡システム - テスト実行")
    print("=" * 50)
    print()
    
    # カレントディレクトリをスクリプトの場所に変更
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # pytestを実行
        result = subprocess.run(
            ["pytest", "test_api.py", "test_tle.py", "-v"],
            capture_output=False,
            text=True
        )
        
        print()
        print("=" * 50)
        print("テスト完了")
        print("=" * 50)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print()
        print("pytestがインストールされていない可能性があります。")
        print("以下のコマンドでインストールしてください:")
        print("pip install pytest")
    
    input("\n続行するには Enter キーを押してください...")

if __name__ == "__main__":
    main()

