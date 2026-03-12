@echo off
REM バックアップ先に保存内容一覧（README）を出力
REM 呼び出し: call backup_create_manifest.bat DEST_PATH [BACKUP_DATE]
setlocal
set "DEST=%~1"
set "BDATE=%~2"
if "%DEST%"=="" exit /b 0

set "MANIFEST=%DEST%\バックアップ内容一覧.txt"
if not "%BDATE%"=="" set "MANIFEST=%DEST%\%BDATE%\バックアップ内容一覧.txt"

(
echo ==========================================
echo UEP v5.0 バックアップ内容一覧
echo ==========================================
echo.
echo バックアップ日時: %date% %time%
if not "%BDATE%"=="" echo 日付フォルダ: %BDATE%
echo.
echo ------------------------------------------
echo 保存対象（uep-v5-ultimate-enterprise-platform 配下）
echo ------------------------------------------
echo   - UEP v5.0 ^(backend, frontend^)
echo   - 統合セキュリティ・防衛プラットフォーム
echo   - 製造・IoTプラットフォーム
echo   - 医療・ヘルスケアプラットフォーム
echo   - 金融・FinTechプラットフォーム
echo   - 産業統合プラットフォーム
echo   - 企業横断オペレーション基盤
echo   - 個人会計（スタンドアロン版^)
echo   - 個人用 PC 容量確保
echo.
echo ------------------------------------------
echo フォルダ構成
echo ------------------------------------------
echo   uep-v5-ultimate-enterprise-platform\  ... 上記すべてを含む
echo   standalone-personal-accounting\       ... 個人会計（別途トップレベルにも^)
echo   docs\                                 ... 職務経歴書・ポートフォリオ等
echo.
echo ------------------------------------------
echo 除外項目
echo ------------------------------------------
echo   node_modules, venv, __pycache__, .git, *.sqlite, *.db
echo.
) > "%MANIFEST%"
exit /b 0
