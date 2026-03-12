"""見積書PDF生成"""
import os
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


def generate_estimate_pdf(
    client_name: str,
    title: str,
    amount: int,
    valid_until: str = "",
    description: str = "",
    estimate_no: str = "EST-001",
) -> Optional[bytes]:
    if not REPORTLAB_AVAILABLE:
        return None
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    font_name = "Helvetica"
    for path in ["C:/Windows/Fonts/msgothic.ttc", "C:/Windows/Fonts/meiryo.ttc"]:
        try:
            if os.path.exists(path):
                pdfmetrics.registerFont(TTFont("JpFont", path, subfontIndex=0))
                font_name = "JpFont"
                break
        except Exception:
            continue
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontName=font_name, fontSize=10)
    story = []
    story.append(Paragraph("見 積 書", ParagraphStyle("Title", parent=styles["Heading1"], fontName=font_name, fontSize=18, alignment=1)))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(f"{client_name} 御中", body_style))
    story.append(Paragraph("Ogawa Tech 小川 清志", ParagraphStyle("Right", parent=body_style, alignment=2)))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(f"見積番号: {estimate_no}" + (f"  有効期限: {valid_until}" if valid_until else ""), body_style))
    story.append(Spacer(1, 8 * mm))
    detail_data = [["項目", "内容", "金額（税抜）"], [title, description or "業務委託", f"¥{amount:,}"]]
    t = Table(detail_data, colWidths=[40 * mm, 80 * mm, 50 * mm])
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), font_name), ("BOX", (0, 0), (-1, -1), 0.5, colors.black), ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.grey)]))
    story.append(t)
    story.append(Spacer(1, 15 * mm))
    story.append(Paragraph("以上、ご検討のほどよろしくお願いいたします。", body_style))
    doc.build(story)
    return buf.getvalue()
