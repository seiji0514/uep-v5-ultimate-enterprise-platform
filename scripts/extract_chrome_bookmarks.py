#!/usr/bin/env python3
"""
Chrome ブックマークからタイトルと URL を抽出するスクリプト。

【Chrome を終了しない方法】推奨
  1. Chrome で Ctrl+Shift+O → 右上 ⋮ → ブックマークをエクスポート
  2. HTML ファイルを保存（例: bookmarks.html）
  3. python scripts/extract_chrome_bookmarks.py --html bookmarks.html

【Chrome を終了する方法】
  python scripts/extract_chrome_bookmarks.py
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_html_bookmarks(html_path):
    """Chrome エクスポート HTML からブックマークを抽出（Chrome 終了不要）"""
    results = []
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    # <A HREF="url">title</A> を抽出
    pattern = r'<A HREF="([^"]+)"[^>]*>([^<]+)</A>'
    for match in re.finditer(pattern, content, re.IGNORECASE):
        url, title = match.groups()
        title = title.strip()
        if title and url.startswith(("http", "file", "chrome")):
            results.append({"title": title, "url": url, "folder": ""})
    return results


def get_default_bookmarks_path():
    """Chrome ブックマークファイルのデフォルトパス"""
    user_home = Path.home()
    return user_home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Bookmarks"


def extract_bookmarks(data, results=None, folder_path=""):
    """再帰的にブックマークを抽出"""
    if results is None:
        results = []

    if isinstance(data, dict):
        if "children" in data:
            name = data.get("name", "")
            new_path = f"{folder_path}/{name}" if folder_path else name
            for child in data["children"]:
                extract_bookmarks(child, results, new_path)
        elif "url" in data:
            results.append({
                "title": data.get("name", ""),
                "url": data.get("url", ""),
                "folder": folder_path,
            })
    elif isinstance(data, list):
        for item in data:
            extract_bookmarks(item, results, folder_path)

    return results


def main():
    # --html オプション: Chrome 終了不要（エクスポート HTML を解析）
    if len(sys.argv) >= 2 and sys.argv[1] in ("--html", "-h"):
        html_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("bookmarks.html")
        if not html_path.exists():
            print(f"エラー: ファイルが見つかりません: {html_path}")
            print("Chrome で Ctrl+Shift+O → ⋮ → ブックマークをエクスポート で HTML を保存してください。")
            sys.exit(1)
        all_results = parse_html_bookmarks(html_path)
        print("(HTML エクスポートから抽出 - Chrome 終了不要)")
    else:
        # JSON ファイルから抽出（Chrome 終了が必要な場合あり）
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            bookmarks_path = Path(sys.argv[1])
        else:
            bookmarks_path = get_default_bookmarks_path()

        if not bookmarks_path.exists():
            print(f"エラー: ブックマークファイルが見つかりません: {bookmarks_path}")
            print("【Chrome 終了不要】python scripts/extract_chrome_bookmarks.py --html bookmarks.html")
            print("  （Chrome で ブックマークをエクスポート で HTML を保存してから実行）")
            sys.exit(1)

        try:
            with open(bookmarks_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"エラー: ファイルの読み込みに失敗しました: {e}")
            print("【Chrome 終了不要】--html オプションでエクスポート HTML を指定してください。")
            sys.exit(1)

        # ルートから抽出（bookmark_bar, other, synced）
        all_results = []
        roots = data.get("roots", {})
        for root_key, root_data in roots.items():
            if isinstance(root_data, dict) and "children" in root_data:
                folder = root_data.get("name", root_key)
                for child in root_data.get("children", []):
                    extract_bookmarks(child, all_results, folder)

    # 出力用 Markdown を生成
    project_root = Path(__file__).resolve().parent.parent
    output_path = project_root / "docs" / "chrome_bookmarks_抽出結果.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Chrome ブックマーク 抽出結果\n\n")
        f.write(f"**抽出日**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**件数**: {len(all_results)} 件\n\n")
        f.write("---\n\n")
        f.write("## タイトル・URL 一覧\n\n")
        f.write("| No. | タイトル | URL | フォルダ |\n")
        f.write("|-----|----------|-----|----------|\n")

        for i, item in enumerate(all_results, 1):
            title = item["title"].replace("|", "&#124;").replace("\n", " ")
            url = item["url"].replace("|", "&#124;")[:80] + ("..." if len(item["url"]) > 80 else "")
            folder = item["folder"].replace("|", "&#124;")
            f.write(f"| {i} | {title} | {url} | {folder} |\n")

        f.write("\n---\n\n")
        f.write("## タイトルのみ（100システム一覧用）\n\n")
        for item in all_results:
            f.write(f"- {item['title']}\n")

    print(f"抽出完了: {len(all_results)} 件")
    print(f"出力先: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
