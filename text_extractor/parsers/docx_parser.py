"""DOCX parser implementation using :mod:`python-docx`."""

from ..models import ExtractedText, PageText


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
    from docx import Document  # Imported lazily

    document = Document(file_path)
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="docx", pages=pages)
