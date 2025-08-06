"""Plain text parser using built-in IO."""

from ..models import ExtractedText, PageText


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
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="txt", pages=pages)
