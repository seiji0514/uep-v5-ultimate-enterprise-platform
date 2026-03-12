"""
経費カテゴリと経費判定ロジック
"""

EXPENSE_CATEGORIES = {
    "communication": {"name": "通信費", "is_expense": True, "note": "インターネット、スマホ按分"},
    "pc_equipment": {"name": "PC・周辺機器", "is_expense": True, "note": "10万円超は減価償却"},
    "software": {"name": "ソフト", "is_expense": True, "note": "開発ツール、クラウドサービス"},
    "books": {"name": "書籍", "is_expense": True, "note": "技術書、資格関連"},
    "seminar": {"name": "セミナー・勉強会", "is_expense": True, "note": "参加費、オンライン講座"},
    "transport": {"name": "交通費", "is_expense": True, "note": "打ち合わせ、出張"},
    "supplies": {"name": "消耗品", "is_expense": True, "note": "メモリ、USB、紙・インク"},
    "entertainment": {"name": "接待交際費", "is_expense": True, "note": "1人5,000円以下等"},
    "bank_fee": {"name": "支払手数料", "is_expense": True, "note": "振込、決済手数料"},
    "insurance": {"name": "保険", "is_expense": True, "note": "業務用賠償保険"},
    "rent_utility": {"name": "家賃・光熱費", "is_expense": True, "note": "按分"},
    "coworking": {"name": "コワーキング", "is_expense": True, "note": "全額経費"},
}

NON_EXPENSE_CATEGORIES = {
    "commute": {"name": "通勤", "is_expense": False, "note": "自宅が事務所の場合は該当しない"},
    "personal": {"name": "私用", "is_expense": False, "note": "プライベート"},
    "living": {"name": "生活費", "is_expense": False, "note": "食費、日用品"},
    "medical": {"name": "医療費", "is_expense": False, "note": "医療費控除の対象"},
    "life_insurance": {"name": "生命保険", "is_expense": False, "note": "生命保険料控除"},
    "hobby": {"name": "趣味", "is_expense": False, "note": "小説、娯楽"},
}

ALL_CATEGORIES = {**EXPENSE_CATEGORIES, **NON_EXPENSE_CATEGORIES}

# 店名・キーワード → カテゴリID（領収書OCRの自動判別用）
MERCHANT_TO_CATEGORY = {
    "コンビニ": "supplies",
    "セブン": "supplies",
    "ファミマ": "supplies",
    "ファミリーマート": "supplies",
    "ローソン": "supplies",
    "ミニストップ": "supplies",
    "ガソリンスタンド": "transport",
    "エネオス": "transport",
    "コスモ": "transport",
    "シェル": "transport",
    "出光": "transport",
    "JR": "transport",
    "電車": "transport",
    "地下鉄": "transport",
    "タクシー": "transport",
    "バス": "transport",
    "新幹線": "transport",
    "ホテル": "transport",
    "宿泊": "transport",
    "Amazon": "supplies",
    "アマゾン": "supplies",
    "楽天": "supplies",
    "ヨドバシ": "pc_equipment",
    "ビックカメラ": "pc_equipment",
    "ヤマダ": "pc_equipment",
    "書店": "books",
    "本屋": "books",
    "丸善": "books",
    "紀伊國屋": "books",
    "Udemy": "seminar",
    "udemy": "seminar",
    "zoom": "communication",
    "Zoom": "communication",
    "AWS": "software",
    "GCP": "software",
    "Azure": "software",
    "GitHub": "software",
    "飲み": "entertainment",
    "食事": "entertainment",
    "居酒屋": "entertainment",
    "レストラン": "entertainment",
    "スタバ": "entertainment",
    "スターバックス": "entertainment",
    "ドトール": "entertainment",
    "タリーズ": "entertainment",
    "コワーキング": "coworking",
    "WeWork": "coworking",
    "レンタルオフィス": "coworking",
    "家賃": "rent_utility",
    "電気": "rent_utility",
    "ガス": "rent_utility",
    "水道": "rent_utility",
    "通信": "communication",
    "スマホ": "communication",
    "ドコモ": "communication",
    "au": "communication",
    "ソフトバンク": "communication",
}


def get_expense_judgment(category_id: str) -> dict:
    cat = ALL_CATEGORIES.get(category_id)
    if not cat:
        return {"is_expense": None, "message": "要確認", "category_name": "不明"}
    return {
        "is_expense": cat["is_expense"],
        "message": "経費" if cat["is_expense"] else "経費外",
        "category_name": cat["name"],
        "note": cat.get("note", ""),
    }


def suggest_category(keyword: str) -> list:
    keyword_lower = keyword.lower()
    results = []
    for cid, cat in ALL_CATEGORIES.items():
        if keyword_lower in cat["name"].lower() or keyword_lower in cid.lower():
            results.append({"id": cid, "name": cat["name"], "is_expense": cat["is_expense"]})
    return results[:5]


def suggest_category_from_merchant(description: str):
    """
    店名・内容からカテゴリを自動判別（領収書OCR用）
    マッチしたキーワードが長いほど優先（より具体的なマッチを採用）
    """
    if not description or not description.strip():
        return None
    text = description.strip()
    best_match: tuple[str, int] | None = None  # (category_id, match_len)
    for keyword, cat_id in MERCHANT_TO_CATEGORY.items():
        if keyword in text:
            if best_match is None or len(keyword) > best_match[1]:
                best_match = (cat_id, len(keyword))
    if best_match:
        return best_match[0]
    # フォールバック: カテゴリ名との部分一致
    suggestions = suggest_category(text[:20])
    return suggestions[0]["id"] if suggestions else None
