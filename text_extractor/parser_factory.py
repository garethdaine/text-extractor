"""Factory for selecting the appropriate parser based on file type."""

from typing import Protocol

from .models import ExtractedText
from .parsers import (
    csv_parser,
    docx_parser,
    image_parser,
    pdf_parser,
    txt_parser,
)
from .plugin_registry import get_plugin_registry
from .utils import resolve_file_type


class Parser(Protocol):
    """Callable parser interface."""

    def __call__(self, file_path: str) -> ExtractedText:  # pragma: no cover - protocol
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

_PARSERS: dict[str, Parser] = {
    "pdf": pdf_parser.parse,
    "docx": docx_parser.parse,
    "csv": csv_parser.parse,
    "txt": txt_parser.parse,
    "png": image_parser.parse,
    "jpg": image_parser.parse,
    "webp": image_parser.parse,
}


def select_parser(file_path: str, mime_type: str | None = None) -> Parser:
    """Select a parser callable for the given file.

    Parameters
    ----------
    file_path : str
        Path to the file to parse.
    mime_type : str | None
        Optional MIME type hint. If provided, it is used to resolve the
        parser; otherwise the file extension is used.

    Returns
    -------
    Parser
        A callable parser implementing the unified interface.

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
        return _PARSERS[file_type]
    except KeyError as err:
        # Check if there's a plugin parser for this file type
        plugin_registry = get_plugin_registry()
        plugin_parser = plugin_registry.get_sync_parser(file_type)
        if plugin_parser:
            return plugin_parser
        raise ValueError(f"No parser available for file type: {file_type}") from err
