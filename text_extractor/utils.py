"""Utility helpers for the text extraction tool."""

from pathlib import Path

try:  # Optional dependency for encoding detection
    import chardet  # type: ignore

    HAS_CHARDET = True
except ImportError:  # pragma: no cover - chardet is optional
    chardet = None  # type: ignore
    HAS_CHARDET = False

_SUPPORTED_TYPES = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".csv": "csv",
    ".txt": "txt",
    ".png": "png",
    ".jpg": "jpg",
    ".jpeg": "jpg",
    ".webp": "webp",
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

    # Check if there's a plugin parser for this extension
    try:
        from .plugin_registry import get_plugin_registry

        plugin_registry = get_plugin_registry()
        plugin_file_type = plugin_registry.get_file_type_from_extension(suffix)
        if plugin_file_type:
            return plugin_file_type
    except ImportError:
        pass

    raise ValueError(f"Unsupported file type: {suffix}")


def read_file_with_encoding_detection(
    file_path: str, default: str = "utf-8"
) -> tuple[bytes, str]:
    """Read a file in binary and detect its encoding.

    Parameters
    ----------
    file_path:
        Path to the file to inspect.
    default:
        Fallback encoding when detection fails or ``chardet`` is unavailable.

    Returns
    -------
    tuple[bytes, str]
        The file's raw bytes and the detected encoding.
    """

    with open(file_path, "rb") as file:
        raw_data = file.read()

    if HAS_CHARDET:
        result = chardet.detect(raw_data)
        encoding = result.get("encoding") or default
    else:
        encoding = default

    return raw_data, encoding


def detect_file_encoding(
    file_path: str, default: str = "utf-8", sample_size: int = 1 << 16
) -> str:
    """Detect a file's text encoding without loading the entire file.

    Parameters
    ----------
    file_path:
        Path to the file to inspect.
    default:
        Fallback encoding when detection fails or ``chardet`` is unavailable.
    sample_size:
        Number of bytes to sample for detection.

    Returns
    -------
    str
        The detected encoding or ``default`` when detection fails.
    """

    with open(file_path, "rb") as file:
        raw_sample = file.read(sample_size)

    if HAS_CHARDET:
        result = chardet.detect(raw_sample)
        encoding = result.get("encoding") or default
    else:
        encoding = default

    return encoding
