"""Async image parser implementation using :mod:`pytesseract`."""

import asyncio

from PIL import Image
import pytesseract

from ..models import ExtractedText, PageText
from ..utils import resolve_file_type


async def parse(file_path: str) -> ExtractedText:
    """Parse an image file and return extracted text via OCR asynchronously.

    Parameters
    ----------
    file_path: str
        Path to the image file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the image.
    """
    # Run the synchronous operation in a thread pool
    loop = asyncio.get_event_loop()

    def _parse_sync():
        try:
            with Image.open(file_path) as image:
                try:
                    text = pytesseract.image_to_string(image)
                except Exception as exc:  # pragma: no cover - OCR failures are rare
                    raise RuntimeError(
                        f"Failed to OCR image: {file_path}"
                    ) from exc
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Image file not found: {file_path}") from e
        except Exception as exc:  # pragma: no cover - file read failures are rare
            raise RuntimeError(f"Failed to open image: {file_path}") from exc

        cleaned = text.strip()
        return cleaned

    text = await loop.run_in_executor(None, _parse_sync)

    page = PageText(page_number=1, text=text, ocr=True)
    file_type = resolve_file_type(file_path)
    return ExtractedText(
        text=text,
        file_type=file_type,
        ocr_used=True,
        pages=[page],
    )
