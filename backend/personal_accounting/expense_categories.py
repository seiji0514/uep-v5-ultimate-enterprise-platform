"""
経費カテゴリと経費判定ロジック
docs/フリーランス_経費判定ガイド.md に基づく
"""

# 経費になるカテゴリ（○）
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

# 経費にならないカテゴリ（×）
NON_EXPENSE_CATEGORIES = {
    "commute": {"name": "通勤", "is_expense": False, "note": "自宅が事務所の場合は該当しない"},
    "personal": {"name": "私用", "is_expense": False, "note": "プライベート"},
    "living": {"name": "生活費", "is_expense": False, "note": "食費、日用品"},
    "medical": {"name": "医療費", "is_expense": False, "note": "医療費控除の対象"},
    "life_insurance": {"name": "生命保険", "is_expense": False, "note": "生命保険料控除"},
    "hobby": {"name": "趣味", "is_expense": False, "note": "小説、娯楽"},
}

ALL_CATEGORIES = {**EXPENSE_CATEGORIES, **NON_EXPENSE_CATEGORIES}


def get_expense_judgment(category_id: str) -> dict:
    """カテゴリから経費判定を返す"""
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
    """キーワードからカテゴリを推測"""
    keyword_lower = keyword.lower()
    results = []
    for cid, cat in ALL_CATEGORIES.items():
        if keyword_lower in cat["name"].lower() or keyword_lower in cid.lower():
            results.append(
                {"id": cid, "name": cat["name"], "is_expense": cat["is_expense"]}
            )
    return results[:5]
