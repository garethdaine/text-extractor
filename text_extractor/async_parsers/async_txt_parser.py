"""Async text file parser implementation."""

import asyncio

from ..models import ExtractedText, PageText
from ..utils import detect_file_encoding


async def parse(file_path: str) -> ExtractedText:
    """Parse a text file and return extracted text asynchronously.

    Parameters
    ----------
    file_path: str
        Path to the text file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the text file.
    """
    # Run the synchronous operation in a thread pool
    loop = asyncio.get_event_loop()

    def _parse_sync():
        encoding = detect_file_encoding(file_path)
        with open(file_path, encoding=encoding) as file:
            text = file.read()
        return text

    text = await loop.run_in_executor(None, _parse_sync)

    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="txt", pages=pages)
