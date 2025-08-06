"""Text file parser stub."""

from ..models import ExtractedText


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
    raise NotImplementedError("Text parsing not implemented yet")
