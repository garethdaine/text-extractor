"""CSV parser implementation using :mod:`pandas`."""

from ..models import ExtractedText, PageText


def parse(file_path: str) -> ExtractedText:
    """Parse a CSV file and return extracted text.

    Parameters
    ----------
    file_path: str
        Path to the CSV file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the CSV.
    """
    import pandas as pd  # Imported lazily

    dataframe = pd.read_csv(file_path)
    text = dataframe.to_csv(index=False)
    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="csv", pages=pages)
