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
    from pandas.errors import ParserError

    try:
        dataframe = pd.read_csv(file_path)
    except ParserError as e:
        raise ValueError(
            f"Failed to parse CSV file '{file_path}': {e}"
        ) from e
    except UnicodeDecodeError as e:
        raise ValueError(
            f"Failed to decode CSV file '{file_path}': {e}"
        ) from e

    text = dataframe.to_string(index=False)
    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="csv", pages=pages)
