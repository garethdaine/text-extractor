"""Async PDF file parser implementation using :mod:`pdfminer.six`."""

import asyncio

from ..models import ExtractedText, PageText


async def parse(file_path: str) -> ExtractedText:
    """Parse a PDF file and return extracted text asynchronously.

    Parameters
    ----------
    file_path: str
        Path to the PDF file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the PDF.
    """
    # Run the synchronous operation in a thread pool
    loop = asyncio.get_event_loop()

    def _parse_sync():
        # Import lazily to avoid heavy dependency at module import time.
        import pytesseract
        from pdf2image import convert_from_path
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
        except Exception:  # pragma: no cover - conversion failures are rare
            # If OCR conversion fails, return empty result instead of raising error
            return ExtractedText(
                text="",
                file_type="pdf",
                ocr_used=False,
                pages=[PageText(page_number=1, text="", ocr=False)],
            )

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

    result = await loop.run_in_executor(None, _parse_sync)
    return result
