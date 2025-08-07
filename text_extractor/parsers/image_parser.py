"""Image parser implementation using :mod:`pytesseract`."""

from PIL import Image
import pytesseract

from ..models import ExtractedText, PageText
from ..utils import resolve_file_type


def parse(file_path: str) -> ExtractedText:
    """Parse an image file and return extracted text via OCR.

    Parameters
    ----------
    file_path: str
        Path to the image file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the image.
    """

    try:
        with Image.open(file_path) as image:
            try:
                text = pytesseract.image_to_string(image)
            except Exception as exc:  # pragma: no cover - OCR failures are rare
                raise RuntimeError(
                    f"Failed to OCR image: {file_path}"
                ) from exc
    except Exception as exc:  # pragma: no cover - file read failures are rare
        raise RuntimeError(f"Failed to open image: {file_path}") from exc

    cleaned = text.strip()
    page = PageText(page_number=1, text=cleaned, ocr=True)
    file_type = resolve_file_type(file_path)
    return ExtractedText(
        text=cleaned,
        file_type=file_type,
        ocr_used=True,
        pages=[page],
    )
