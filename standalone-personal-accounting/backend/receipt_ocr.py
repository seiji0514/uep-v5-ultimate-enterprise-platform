"""
領収書OCR - 画像から日付・金額・店名を抽出
pytesseract 使用（Tesseract-OCR のインストールが必要）
"""
import os
import re
from io import BytesIO
from typing import Optional

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
    # PATH 未設定時用: 既定の Windows インストール先を試す
    _tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for p in _tesseract_paths:
        if os.path.isfile(p):
            pytesseract.pytesseract.tesseract_cmd = p
            break
except ImportError:
    OCR_AVAILABLE = False


def _extract_amount(text: str) -> Optional[int]:
    """テキストから金額を抽出（円・¥・, を考慮）"""
    patterns = [
        r"合計[:\s]*[¥￥]?\s*([0-9,]+)\s*円?",
        r"税込[:\s]*[¥￥]?\s*([0-9,]+)",
        r"計[:\s]*[¥￥]?\s*([0-9,]+)",
        r"[¥￥]\s*([0-9,]+)\s*円?",
        r"([0-9,]+)\s*円",
        r"([0-9]{3,})\s*(?:円|¥)?",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            try:
                return int(m.group(1).replace(",", ""))
            except ValueError:
                continue
    return None


def _extract_date(text: str) -> Optional[str]:
    """テキストから日付を抽出（YYYY-MM-DD形式で返す）"""
    patterns = [
        r"(\d{4})[年/\-](\d{1,2})[月/\-](\d{1,2})",
        r"(\d{4})/(\d{1,2})/(\d{1,2})",
        r"(\d{4})-(\d{1,2})-(\d{1,2})",
        r"令和\s*(\d+)\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            try:
                g = m.groups()
                if "令和" in pat:
                    y = int(g[0]) + 2018  # 令和1年=2019
                    return f"{y}-{int(g[1]):02d}-{int(g[2]):02d}"
                return f"{int(g[0])}-{int(g[1]):02d}-{int(g[2]):02d}"
            except (ValueError, IndexError):
                continue
    return None


def _extract_merchant(text: str) -> str:
    """テキストから店名・内容を推測（最初の非数字行など）"""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines[:5]:
        if len(line) >= 2 and not re.match(r"^[\d\s¥￥,\.]+$", line):
            if "合計" not in line and "税" not in line and "日" not in line:
                return line[:50]
    return ""


def extract_from_image(image_bytes: bytes) -> dict:
    """
    画像バイトから領収書情報を抽出

    Returns:
        { "date": "YYYY-MM-DD", "amount": int, "description": str, "raw_text": str, "ocr_available": bool }
    """
    if not OCR_AVAILABLE:
        return {
            "date": None,
            "amount": None,
            "description": "",
            "suggested_category_id": None,
            "raw_text": "",
            "ocr_available": False,
            "error": "pytesseract または Pillow がインストールされていません。pip install pytesseract Pillow",
        }

    try:
        img = Image.open(BytesIO(image_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        try:
            text = pytesseract.image_to_string(img, lang="jpn+eng")
        except Exception:
            text = pytesseract.image_to_string(img, lang="eng")
    except Exception as e:
        return {
            "date": None,
            "amount": None,
            "description": "",
            "suggested_category_id": None,
            "raw_text": "",
            "ocr_available": True,
            "error": f"OCR エラー: {str(e)}。Tesseract-OCR がインストールされているか確認してください。",
        }

    description = _extract_merchant(text)
    suggested_category_id = None
    try:
        from expense_categories import suggest_category_from_merchant
        suggested_category_id = suggest_category_from_merchant(description)
    except Exception:
        pass

    return {
        "date": _extract_date(text),
        "amount": _extract_amount(text),
        "description": description,
        "suggested_category_id": suggested_category_id,
        "raw_text": text[:500],
        "ocr_available": True,
    }
