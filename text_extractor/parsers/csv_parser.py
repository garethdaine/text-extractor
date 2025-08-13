"""CSV parser implementation using :mod:`pandas`."""

from ..models import ExtractedText, PageText
from ..utils import HAS_CHARDET, detect_file_encoding


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

    encoding = detect_file_encoding(file_path)

    try:
        dataframe = pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError as e:
        if not HAS_CHARDET:
            raise ValueError(
                "Failed to decode CSV file and 'chardet' is not installed for encoding detection"
            ) from e
        raise ValueError(
            f"Failed to decode CSV file '{file_path}' with encoding '{encoding}': {e}"
        ) from e
    except ParserError as e:
        raise ValueError(f"Failed to parse CSV file '{file_path}': {e}") from e
    except pd.errors.EmptyDataError:
        # Handle empty CSV files gracefully
        text = ""
        pages = [PageText(page_number=1, text=text, ocr=False)]
        return ExtractedText(text=text, file_type="csv", pages=pages)

    text = dataframe.to_string(index=False)
    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="csv", pages=pages)
