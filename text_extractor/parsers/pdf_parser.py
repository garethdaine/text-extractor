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
    if combined_text:
        return ExtractedText(text=combined_text, file_type="pdf", pages=pages)

    # Fallback to OCR when no text was extracted
    ocr_pages: list[PageText] = []
    try:
        images = convert_from_path(file_path)
    except Exception as exc:  # pragma: no cover - conversion failures are rare
        raise RuntimeError(
            f"Failed to convert PDF to images for OCR: {file_path}"
        ) from exc

    for page_number, image in enumerate(images, start=1):
        try:
            text = pytesseract.image_to_string(image).strip()
        except Exception as exc:  # pragma: no cover - OCR failures are rare
            raise RuntimeError(
                f"Failed to OCR PDF page {page_number} from {file_path}"
            ) from exc
        ocr_pages.append(PageText(page_number=page_number, text=text, ocr=True))

    combined_text = "\n".join(page.text for page in ocr_pages).strip()
    return ExtractedText(
        text=combined_text,
        file_type="pdf",
        ocr_used=True,
        pages=ocr_pages,
    )
