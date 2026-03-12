"""
確定申告書（収支内訳書風）のHTML生成
※税務上の正確性は税理士にご確認ください
"""
from datetime import date
from typing import Dict, List

from store import get_expenses, get_income


def _aggregate_by_category(year: int) -> Dict[str, int]:
    """経費をカテゴリ別に集計"""
    expenses = get_expenses(year=year)
    by_cat: Dict[str, int] = {}
    for e in expenses:
        name = e.get("category_name", "その他")
        by_cat[name] = by_cat.get(name, 0) + e.get("amount", 0)
    return by_cat


def generate_tax_declaration_html(year: int, name: str = "小川 清志", address: str = "") -> str:
    """
    収支内訳書風のHTMLを生成
    """
    expenses = get_expenses(year=year)
    income_list = get_income(year=year)
    total_income = sum(i["amount"] for i in income_list)
    total_expense = sum(e["amount"] for e in expenses)
    profit = total_income - total_expense
    by_cat = _aggregate_by_category(year)

    rows = "".join(
        f'<tr><td>{cat}</td><td class="amount">{amt:,}円</td></tr>'
        for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1])
    )

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>収支内訳書（参考）{year}年分</title>
  <style>
    body {{ font-family: "Yu Gothic", "Meiryo", sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }}
    h1 {{ font-size: 1.2rem; text-align: center; }}
    .note {{ color: #666; font-size: 0.85rem; margin-bottom: 1rem; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
    th, td {{ border: 1px solid #333; padding: 0.5rem 0.8rem; }}
    th {{ background: #f5f5f5; width: 40%; }}
    .amount {{ text-align: right; }}
    .total {{ font-weight: bold; }}
  </style>
</head>
<body>
  <p class="note">※本書類は参考用です。確定申告には税務署所定の様式をご使用ください。税理士にご確認ください。</p>
  <h1>収支内訳書（参考） {year}年分</h1>
  <p>氏名: {name}　住所: {address or "（ご記入ください）"}</p>

  <h2>1. 収入の内訳</h2>
  <table>
    <tr><th>項目</th><th class="amount">金額</th></tr>
    <tr><td>業務委託料等</td><td class="amount">{total_income:,}円</td></tr>
    <tr class="total"><td>収入合計</td><td class="amount">{total_income:,}円</td></tr>
  </table>

  <h2>2. 経費の内訳（カテゴリ別）</h2>
  <table>
    <tr><th>項目</th><th class="amount">金額</th></tr>
    {rows}
    <tr class="total"><td>経費合計</td><td class="amount">{total_expense:,}円</td></tr>
  </table>

  <h2>3. 所得金額</h2>
  <table>
    <tr><th>収入合計</th><td class="amount">{total_income:,}円</td></tr>
    <tr><th>経費合計</th><td class="amount">-{total_expense:,}円</td></tr>
    <tr class="total"><th>所得金額</th><td class="amount">{profit:,}円</td></tr>
  </table>

  <p style="margin-top: 2rem; font-size: 0.9rem;">印刷してPDF保存するか、税務署のe-Taxソフト等で正式な申告書を作成してください。</p>
</body>
</html>"""
    return html
