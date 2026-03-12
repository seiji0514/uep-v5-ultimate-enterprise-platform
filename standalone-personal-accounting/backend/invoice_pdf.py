"""
請求書のPDF生成
"""
import os
from datetime import date, timedelta
from io import BytesIO
from typing import Optional

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_invoice_pdf(
    client_name: str,
    amount: int,
    client_address: str = "",
    client_contact: str = "",
    description: str = "業務委託料",
    invoice_no: str = "OGT-2026-001",
    bank_name: str = "〇〇銀行",
    bank_branch: str = "〇〇支店",
    bank_account: str = "〇〇〇〇〇〇〇",
    bank_holder: str = "オガワ セイジ",
) -> Optional[bytes]:
    """
    請求書PDFを生成（バイト列で返す）
    """
    if not REPORTLAB_AVAILABLE:
        return None

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=20 * mm, bottomMargin=20 * mm)

    styles = getSampleStyleSheet()
    font_name = "Helvetica"
    for path in [
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
    ]:
        try:
            if os.path.exists(path):
                pdfmetrics.registerFont(TTFont("JpFont", path, subfontIndex=0))
                font_name = "JpFont"
                break
        except Exception:
            continue

    title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontName=font_name, fontSize=18, alignment=1)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontName=font_name, fontSize=10)

    story = []
    story.append(Paragraph("請 求 書", title_style))
    story.append(Spacer(1, 10 * mm))

    # 請求先・請求元
    header_data = [
        ["請求先", "請求元"],
        [
            f"{client_name} 御中<br/>{client_address}<br/>{client_contact}",
            "Ogawa Tech（オガワ・テック）<br/>小川 清志<br/>口座名義: オガワ セイジ",
        ],
    ]
    header_table = Table(header_data, colWidths=[90 * mm, 90 * mm])
    header_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8 * mm))

    # 請求書番号・発行日・支払期限
    today = date.today()
    due = today + timedelta(days=30)
    info_data = [
        ["請求書番号", invoice_no, "発行日", today.strftime("%Y年%m月%d日")],
        ["支払期限", due.strftime("%Y年%m月%d日"), "", ""],
    ]
    info_table = Table(info_data, colWidths=[25 * mm, 40 * mm, 25 * mm, 40 * mm])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 8 * mm))

    # 明細
    tax = int(amount * 0.1)
    total = amount + tax
    detail_data = [
        ["項目", "内容", "数量", "単価（税抜）", "金額（税抜）"],
        ["業務委託料", description, "1", f"¥{amount:,}", f"¥{amount:,}"],
        ["", "", "", "小計（税抜）", f"¥{amount:,}"],
        ["", "", "", "消費税（10%）", f"¥{tax:,}"],
        ["", "", "", "合計（税込）", f"¥{total:,}"],
    ]
    detail_table = Table(detail_data, colWidths=[25 * mm, 50 * mm, 20 * mm, 35 * mm, 35 * mm])
    detail_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (2, 0), (4, -1), "RIGHT"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("BACKGROUND", (0, 4), (-1, 4), colors.lightgrey),
    ]))
    story.append(detail_table)
    story.append(Spacer(1, 8 * mm))

    # 振込先
    bank_text = f"【お振込先】 {bank_name} {bank_branch} 口座番号: {bank_account} 口座名義: {bank_holder}"
    story.append(Paragraph(bank_text, body_style))
    story.append(Paragraph("※振込手数料はお客様のご負担でお願いいたします。", ParagraphStyle("Note", parent=body_style, fontSize=8, textColor=colors.grey)))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("以上", ParagraphStyle("End", parent=body_style, alignment=2)))

    doc.build(story)
    return buf.getvalue()
