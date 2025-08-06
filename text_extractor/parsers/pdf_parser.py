"""PDF parser stub."""

from ..models import ExtractedText


def parse(file_path: str) -> ExtractedText:
    """Parse a PDF file and return extracted text.

    Parameters
    ----------
    file_path: str
        Path to the PDF file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the PDF.
    """
    raise NotImplementedError("PDF parsing not implemented yet")
