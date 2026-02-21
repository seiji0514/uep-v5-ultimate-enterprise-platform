#!/bin/bash
# uep-v5-ultimate-enterprise-platform を GitHub に追加するスクリプト
# 実行: bash scripts/add-to-github.sh

set -e
cd "$(dirname "$0")/.."

echo "=== uep-v5-ultimate-enterprise-platform を GitHub に追加 ==="

# 1. Git 初期化（未初期化の場合）
if [ ! -d .git ]; then
    echo ""
    echo "1. Git リポジトリを初期化..."
    git init
    git branch -M main
    echo "   完了"
else
    echo ""
    echo "1. Git リポジトリは既に初期化済み"
fi

# 2. ファイルを追加
echo ""
echo "2. ファイルを追加..."
git add .
git status
echo "   完了"

# 3. 初回コミット（未コミットの場合）
if ! git rev-parse HEAD &>/dev/null; then
    echo ""
    echo "3. 初回コミットを作成..."
    git commit -m "Initial commit: UEP v5.0 - Ultimate Enterprise Platform"
    echo "   完了"
else
    echo ""
    echo "3. 既存のコミットがあります。変更があればコミットしてください。"
fi

# 4. リモート追加と push の案内
echo ""
echo "=== 次のステップ（手動で実行） ==="
echo ""
echo "1. GitHub でリポジトリを作成:"
echo "   https://github.com/new"
echo "   - リポジトリ名: uep-v5-ultimate-enterprise-platform"
echo "   - Public を選択"
echo "   - README 等は追加しない（既存コードを push するため）"
echo ""
echo "2. 以下のコマンドを実行:"
echo ""
echo "   git remote add origin https://github.com/seiji0514/uep-v5-ultimate-enterprise-platform.git"
echo "   git push -u origin main"
echo ""
echo "   ※ seiji0514 はあなたの GitHub ユーザー名に置き換えてください"
echo ""
echo "3. Render でリポジトリを再読み込みすると表示されます"
echo ""
