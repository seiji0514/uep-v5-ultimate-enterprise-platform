"""契約書PDF生成"""
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
    import os
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_contract_pdf(
    client_name: str,
    title: str,
    amount: int,
    start_date: str,
    end_date: str,
    description: str = "",
    contractor_name: str = "Ogawa Tech 小川 清志",
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
    story.append(Paragraph("業務委託契約書", ParagraphStyle("Title", parent=styles["Heading1"], fontName=font_name, fontSize=16, alignment=1)))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(f"甲（発注者）: {client_name} 御中", body_style))
    story.append(Paragraph(f"乙（受注者）: {contractor_name}", body_style))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(f"第1条（業務内容）{title}", body_style))
    if description:
        story.append(Paragraph(description, body_style))
    story.append(Paragraph(f"第2条（契約期間）{start_date} から {end_date} まで", body_style))
    story.append(Paragraph(f"第3条（報酬）金{amount:,}円（税別）", body_style))
    story.append(Spacer(1, 15 * mm))
    story.append(Paragraph("以上、甲乙合意の上、本契約を締結する。", body_style))
    doc.build(story)
    return buf.getvalue()
