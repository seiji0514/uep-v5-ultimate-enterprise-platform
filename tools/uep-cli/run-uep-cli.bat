@echo off
REM uep-cli 実行用バッチ（Windows）
REM Python版を使用（Go exe は McAfee 等で隔離されるため）
REM 使い方: run-uep-cli.bat version
REM 使い方: run-uep-cli.bat health
REM 使い方: run-uep-cli.bat events list

cd /d "%~dp0"
python uep-cli.py %*
