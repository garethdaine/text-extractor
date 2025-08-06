"""Utility helpers for the text extraction tool."""

from pathlib import Path

_SUPPORTED_TYPES = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".csv": "csv",
    ".txt": "txt",
    ".png": "png",
    ".jpg": "jpg",
    ".jpeg": "jpeg",
}


def resolve_file_type(file_path: str) -> str:
    """Resolve a file's type based on its extension.

    Parameters
    ----------
    file_path:
        The path to the file to inspect.

    Returns
    -------
    str
        Normalized file type in lowercase without leading dot.

    Raises
    ------
    ValueError
        If the extension is not supported.
    """
    suffix = Path(file_path).suffix.lower()
    if suffix in _SUPPORTED_TYPES:
        return _SUPPORTED_TYPES[suffix]
    raise ValueError(f"Unsupported file type: {suffix}")
