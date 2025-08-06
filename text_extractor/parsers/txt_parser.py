"""Plain text parser using built-in IO."""

from ..models import ExtractedText, PageText
from ..utils import HAS_CHARDET, read_file_with_encoding_detection


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
        if not HAS_CHARDET:
            raise ValueError(
                "Failed to decode text file and 'chardet' is not installed for encoding detection"
            )
        raw_data, encoding = read_file_with_encoding_detection(file_path)
        try:
            text = raw_data.decode(encoding)
        except UnicodeDecodeError as e:
            raise ValueError(
                f"Failed to decode text file '{file_path}' with encoding '{encoding}': {e}"
            ) from e

    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="txt", pages=pages)
