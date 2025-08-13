"""Async factory for selecting the appropriate async parser based on file type."""

from typing import Protocol

# Import async parsers
from .async_parsers import (
    async_csv_parser,
    async_docx_parser,
    async_image_parser,
    async_pdf_parser,
    async_txt_parser,
)
from .models import ExtractedText
from .utils import resolve_file_type


class AsyncParser(Protocol):
    """Async callable parser interface."""

    async def __call__(
        self, file_path: str
    ) -> ExtractedText:  # pragma: no cover - protocol
        ...


_MIME_TYPE_MAP = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "text/csv": "csv",
    "text/plain": "txt",
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/webp": "webp",
}

_ASYNC_PARSERS: dict[str, AsyncParser] = {
    "pdf": async_pdf_parser.parse,
    "docx": async_docx_parser.parse,
    "csv": async_csv_parser.parse,
    "txt": async_txt_parser.parse,
    "png": async_image_parser.parse,
    "jpg": async_image_parser.parse,
    "webp": async_image_parser.parse,
}


def select_async_parser(file_path: str, mime_type: str | None = None) -> AsyncParser:
    """Select an async parser callable for the given file.

    Parameters
    ----------
    file_path : str
        Path to the file to parse.
    mime_type : str | None
        Optional MIME type hint. If provided, it is used to resolve the
        parser; otherwise the file extension is used.

    Returns
    -------
    AsyncParser
        An async callable parser implementing the unified interface.

    Raises
    ------
    ValueError
        If no parser is available for the resolved file type.
    """
    if mime_type:
        file_type = _MIME_TYPE_MAP.get(mime_type)
        if not file_type:
            raise ValueError(f"Unsupported MIME type: {mime_type}")
    else:
        file_type = resolve_file_type(file_path)

    try:
        return _ASYNC_PARSERS[file_type]
    except KeyError as exc:  # pragma: no cover - defensive
        raise ValueError(
            f"No async parser available for file type: {file_type}"
        ) from exc


async def extract_text_from_file_async(file_path: str) -> ExtractedText:
    """Extract text from a file using the appropriate async parser.

    This is the async main entry point for the text extraction tool. It automatically
    selects the appropriate async parser based on the file extension and returns
    structured text extraction results.

    Parameters
    ----------
    file_path : str
        Path to the file to extract text from.

    Returns
    -------
    ExtractedText
        Structured text extraction results containing the extracted text,
        file type information, OCR usage, and page-level details.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the file type is not supported.
    Exception
        Any other errors that occur during parsing (parser-specific).

    Examples
    --------
    >>> import asyncio
    >>> from text_extractor import extract_text_from_file_async
    >>> result = await extract_text_from_file_async("document.pdf")
    >>> print(result.text)
    >>> print(f"File type: {result.file_type}")
    >>> print(f"OCR used: {result.ocr_used}")
    """
    # Select the appropriate async parser
    parser = select_async_parser(file_path)

    # Parse the file and return results
    return await parser(file_path)
