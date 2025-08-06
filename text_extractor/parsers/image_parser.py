"""Image parser stub."""

from ..models import ExtractedText


def parse(file_path: str) -> ExtractedText:
    """Parse an image file and return extracted text via OCR.

    Parameters
    ----------
    file_path: str
        Path to the image file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the image.
    """
    raise NotImplementedError("Image parsing not implemented yet")
