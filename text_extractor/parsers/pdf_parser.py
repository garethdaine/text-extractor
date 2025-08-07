"""PDF parser implementation using :mod:`pdfminer.six`."""

from pdf2image import convert_from_path
import pytesseract

from ..models import ExtractedText, PageText


def parse(file_path: str) -> ExtractedText:
    """Parse a PDF file and return extracted text.

    Parameters
    ----------
    file_path: str
        Path to the PDF file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the PDF.
    """
    # Import lazily to avoid heavy dependency at module import time.
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer

    pages: list[PageText] = []
    for page_number, page_layout in enumerate(extract_pages(file_path), start=1):
        parts: list[str] = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                parts.append(element.get_text())
        page_text = "".join(parts).strip()
        pages.append(PageText(page_number=page_number, text=page_text, ocr=False))

    combined_text = "\n".join(page.text for page in pages).strip()
    if len(combined_text) > 0:
        return ExtractedText(text=combined_text, file_type="pdf", pages=pages)

    # Fallback to OCR when no text was extracted
    ocr_pages: list[PageText] = []
    images = convert_from_path(file_path)
    for page_number, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image).strip()
        ocr_pages.append(PageText(page_number=page_number, text=text, ocr=True))

    combined_text = "\n".join(page.text for page in ocr_pages).strip()
    return ExtractedText(
        text=combined_text,
        file_type="pdf",
        ocr_used=True,
        pages=ocr_pages,
    )
