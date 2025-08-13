"""Core package for the text extraction tool."""

from .async_parser_factory import extract_text_from_file_async
from .language_detection import (
    LanguageInfo,
    detect_language,
    detect_language_simple,
    get_supported_languages,
    is_english,
)
from .models import ExtractedText, PageText
from .parser_factory import select_parser
from .plugin_registry import (
    get_plugin_registry,
    register_async_parser,
    register_sync_parser,
)
from .utils import resolve_file_type

__all__ = [
    "ExtractedText",
    "PageText",
    "resolve_file_type",
    "extract_text_from_file",
    "extract_text_from_file_async",
    "detect_language",
    "detect_language_simple",
    "is_english",
    "get_supported_languages",
    "LanguageInfo",
    "get_plugin_registry",
    "register_sync_parser",
    "register_async_parser",
]


def extract_text_from_file(file_path: str) -> ExtractedText:
    """Extract text from a file using the appropriate parser.

    This is the main entry point for the text extraction tool. It automatically
    selects the appropriate parser based on the file extension and returns
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
    >>> from text_extractor import extract_text_from_file
    >>> result = extract_text_from_file("document.pdf")
    >>> print(result.text)
    >>> print(f"File type: {result.file_type}")
    >>> print(f"OCR used: {result.ocr_used}")
    """
    # Select the appropriate parser
    parser = select_parser(file_path)

    # Parse the file and return results
    return parser(file_path)
