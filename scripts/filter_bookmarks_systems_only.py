#!/usr/bin/env python3
"""
Chrome ブックマーク抽出結果から「システム」関連のみをフィルタするスクリプト。

使い方:
  python scripts/filter_bookmarks_systems_only.py
  python scripts/filter_bookmarks_systems_only.py docs/chrome_bookmarks_抽出結果.md
  python scripts/filter_bookmarks_systems_only.py --strict   # 厳密モード（ノイズ削減）

出力: docs/chrome_bookmarks_システムのみ.md
"""
import re
import sys
from pathlib import Path


# システム関連キーワード（タイトルに含まれるものを抽出）
SYSTEM_KEYWORDS = [
    "システム", "プラットフォーム", "基盤", "統合",
    "リハビリ", "AI", "機械学習", "ディープラーニング",
    "量子", "メタバース", "AR", "VR", "BCI",
    "ゲーム", "データ駆動", "生体", "センサー",
    "ブロックチェーン", "ロボティクス", "ゲーミフィケーション",
    "プロジェクト", "ポートフォリオ",
]

# 厳密モード用（ノイズを減らす）
STRICT_KEYWORDS = [
    "システム", "プラットフォーム", "基盤", "統合",
    "リハビリ", "機械学習", "ディープラーニング",
    "量子", "メタバース", "BCI", "ブロックチェーン",
    "ロボティクス", "ゲーミフィケーション",
    "データ駆動", "生体認証", "バイオメトリクス",
]

# 除外するキーワード（ノイズ削減）
EXCLUDE_KEYWORDS = [
    "本番・基盤", "デリヘル", "ソープ", "アンインストール",
    "合気道", "空手", "格闘", "武術", "チャンネル",
    "Udemy", "講座", "Course:", "YouTube",
]

# カテゴリ分類（優先順位順、最初にマッチしたカテゴリに分類）
CATEGORIES = [
    ("医療・リハビリ系", ["リハビリ", "医療", "診断", "介護", "病院", "感染症"]),
    ("AI・機械学習系", ["機械学習", "ディープラーニング", "AI", "NLP", "チャットボット"]),
    ("量子コンピューティング系", ["量子"]),
    ("ゲーム・ゲーミフィケーション系", ["ゲーム", "ゲーミフィケーション", "脳トレ"]),
    ("ブロックチェーン系", ["ブロックチェーン"]),
    ("メタバース・VR/AR系", ["メタバース", "AR", "VR", "ホログラム"]),
    ("BCI・脳波制御系", ["BCI", "脳波", "脳科学"]),
    ("セキュリティ・防衛系", ["セキュリティ", "防衛", "ハッカー", "暗号", "ゼロトラスト"]),
    ("ロボティクス系", ["ロボティクス"]),
    ("生体・バイオメトリクス系", ["生体認証", "バイオメトリクス", "生体"]),
    ("航空・宇宙系", ["航空", "宇宙", "衛星"]),
    ("交通・防災系", ["交通", "災害", "防災", "気象", "避難"]),
    ("金融・行政系", ["金融", "行政", "法務", "自治体"]),
    ("IoT・基盤・プラットフォーム系", ["IoT", "5G", "エッジ", "センサー", "プラットフォーム"]),
    ("その他・統合系", []),  # 上記に該当しないもの
]


def parse_markdown_table(content):
    """Markdown テーブルから行を抽出"""
    results = []
    lines = content.split("\n")
    in_table = False
    for line in lines:
        if line.startswith("| No.") or line.startswith("|---"):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            # | 1 | タイトル | URL | フォルダ |
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 3:
                no, title, url = parts[0], parts[1], parts[2]
                title_clean = title.replace("&#124;", "|")
                results.append({"no": no, "title": title_clean, "url": url})
        elif in_table and not line.strip():
            break
    return results


def filter_systems(entries, strict=False):
    """システム関連キーワードでフィルタ"""
    keywords = STRICT_KEYWORDS if strict else SYSTEM_KEYWORDS
    filtered = []
    for e in entries:
        title_lower = e["title"].lower()
        # 除外キーワードチェック
        if any(ex in e["title"] for ex in EXCLUDE_KEYWORDS):
            continue
        for kw in keywords:
            if kw.lower() in title_lower:
                filtered.append(e)
                break
    return filtered


def categorize(entries):
    """エントリをカテゴリ別に分類"""
    result = {cat: [] for cat, _ in CATEGORIES}
    for e in entries:
        title_lower = e["title"].lower()
        assigned = False
        for cat_name, keywords in CATEGORIES[:-1]:  # その他を除く
            if any(kw.lower() in title_lower for kw in keywords):
                result[cat_name].append(e)
                assigned = True
                break
        if not assigned:
            result["その他・統合系"].append(e)
    return result


def main():
    project_root = Path(__file__).resolve().parent.parent
    input_path = project_root / "docs" / "chrome_bookmarks_抽出結果.md"
    strict = "--strict" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--strict"]
    if args:
        input_path = Path(args[0])

    if not input_path.exists():
        print(f"エラー: ファイルが見つかりません: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    entries = parse_markdown_table(content)
    filtered = filter_systems(entries, strict=strict)
    categorized = categorize(filtered)

    output_path = project_root / "docs" / "chrome_bookmarks_システムのみ.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Chrome ブックマーク - システム関連のみ（カテゴリ別）\n\n")
        f.write(f"**元ファイル**: {input_path.name}\n\n")
        f.write(f"**モード**: {'厳密（ノイズ除外）' if strict else '標準'}\n\n")
        f.write(f"**抽出件数**: {len(filtered)} 件（元: {len(entries)} 件）\n\n")
        f.write("**カテゴリ内訳**:\n")
        for cat_name, items in categorized.items():
            if items:
                f.write(f"- {cat_name}: {len(items)} 件\n")
        f.write("\n---\n\n")
        f.write("## カテゴリ別一覧\n\n")

        for cat_name, items in categorized.items():
            if not items:
                continue
            f.write(f"### {cat_name}（{len(items)} 件）\n\n")
            f.write("| No. | タイトル | URL |\n")
            f.write("|-----|----------|-----|\n")
            for i, e in enumerate(items, 1):
                title_esc = e["title"].replace("|", "&#124;")[:100]
                url_esc = (e["url"][:80] + "..." if len(e["url"]) > 80 else e["url"]).replace("|", "&#124;")
                f.write(f"| {i} | {title_esc} | {url_esc} |\n")
            f.write("\n")

        f.write("---\n\n")
        f.write("## タイトルのみ（100システム一覧用）\n\n")
        for cat_name, items in categorized.items():
            if not items:
                continue
            f.write(f"### {cat_name}\n\n")
            for e in items:
                f.write(f"- {e['title']}\n")
            f.write("\n")

    print(f"フィルタ完了: {len(filtered)} 件（元 {len(entries)} 件から）")
    print(f"出力先: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
