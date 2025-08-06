"""Plain text parser using built-in IO."""

from ..models import ExtractedText, PageText

try:  # Optional dependency for encoding detection
    import chardet  # type: ignore

    _HAS_CHARDET = True
except ImportError:  # pragma: no cover - chardet is optional
    chardet = None  # type: ignore
    _HAS_CHARDET = False


def parse(file_path: str) -> ExtractedText:
    """Parse a text file and return extracted text.

    Parameters
    ----------
    file_path: str
        Path to the text file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except UnicodeDecodeError:
        if not _HAS_CHARDET:
            raise ValueError(
                "Failed to decode text file and 'chardet' is not installed for encoding detection"
            )
        with open(file_path, "rb") as file:
            raw_data = file.read()
        result = chardet.detect(raw_data) if _HAS_CHARDET else None
        encoding = result.get("encoding") if result else "utf-8"
        try:
            text = raw_data.decode(encoding)
        except UnicodeDecodeError as e:
            raise ValueError(
                f"Failed to decode text file '{file_path}' with encoding '{encoding}': {e}"
            ) from e

    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="txt", pages=pages)
