"""DOCX parser stub."""

from ..models import ExtractedText


def parse(file_path: str) -> ExtractedText:
    """Parse a DOCX file and return extracted text.

    Parameters
    ----------
    file_path: str
        Path to the DOCX file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the DOCX document.
    """
    raise NotImplementedError("DOCX parsing not implemented yet")
