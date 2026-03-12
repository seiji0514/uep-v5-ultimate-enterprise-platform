#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI自動音声応答システム 起動スクリプト（Python版）
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """ヘッダーを表示"""
    print("=" * 40)
    print("AI自動音声応答システム 起動スクリプト")
    print("=" * 40)
    print()

def check_python_version():
    """Pythonのバージョンを確認"""
    print("[1/4] Pythonのバージョン確認...")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("エラー: Python 3.8以上が必要です")
        print("現在のバージョンでは動作しません")
        return False
    return True

def check_dependencies():
    """依存関係を確認・インストール"""
    print()
    print("[2/4] 依存関係の確認...")
    
    try:
        # pip listでfastapiがインストールされているか確認
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        if "fastapi" in result.stdout.lower():
            print("依存関係は既にインストールされています")
            return True
        else:
            print("依存関係をインストール中...")
            print("初回インストールには時間がかかります...")
            
            # requirements.txtをインストール
            requirements_file = Path(__file__).parent / "requirements.txt"
            if not requirements_file.exists():
                print(f"エラー: {requirements_file} が見つかりません")
                return False
            
            install_result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                encoding="utf-8"
            )
            
            if install_result.returncode != 0:
                print("エラー: 依存関係のインストールに失敗しました")
                print("手動でインストールしてください: pip install -r requirements.txt")
                return False
            
            print("依存関係のインストールが完了しました")
            return True
            
    except Exception as e:
        print(f"エラー: 依存関係の確認中に問題が発生しました: {e}")
        return False

def check_config():
    """設定ファイルを確認"""
    print()
    print("[3/4] 設定ファイルの確認...")
    
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print(".envファイルが見つかりません")
        print("オプション: .envファイルを作成してOpenAI API Keyを設定できます")
        print("ローカルモデルのみ使用する場合は設定不要です")
    else:
        print(".envファイルが見つかりました")

def start_server():
    """サーバーを起動"""
    print()
    print("[4/4] バックエンドサーバーを起動中...")
    print()
    # 設定ファイルからポート番号を取得
    try:
        import config
        server_port = config.SERVER_PORT
    except:
        server_port = 8001  # デフォルトポート: 8001
    
    print("=" * 40)
    print("サーバー起動完了後、ブラウザで以下を開いてください:")
    print(f"http://localhost:{server_port}")
    print("=" * 40)
    print()
    print("停止するには Ctrl+C を押してください")
    print()
    
    # バックエンドディレクトリに移動
    backend_dir = Path(__file__).parent / "backend"
    if not backend_dir.exists():
        print(f"エラー: {backend_dir} が見つかりません")
        return False
    
    main_py = backend_dir / "main.py"
    if not main_py.exists():
        print(f"エラー: {main_py} が見つかりません")
        return False
    
    # サーバーを起動
    try:
        os.chdir(backend_dir)
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nサーバーを停止しました")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print("ログを確認してください")
        return False
    
    return True

def main():
    """メイン関数"""
    # プロジェクトルートに移動
    os.chdir(Path(__file__).parent)
    
    print_header()
    
    # Pythonバージョン確認
    if not check_python_version():
        input("\nEnterキーを押して終了してください...")
        sys.exit(1)
    
    # 依存関係確認・インストール
    if not check_dependencies():
        input("\nEnterキーを押して終了してください...")
        sys.exit(1)
    
    # 設定ファイル確認
    check_config()
    
    # サーバー起動
    start_server()
    
    # Windowsの場合、終了前に待機
    if platform.system() == "Windows":
        input("\nEnterキーを押して終了してください...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n中断されました")
        sys.exit(0)
    except Exception as e:
        print(f"\n予期しないエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
