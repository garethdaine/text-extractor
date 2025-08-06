"""CSV parser implementation using :mod:`pandas`."""

from ..models import ExtractedText, PageText

try:  # Optional dependency for encoding detection
    import chardet  # type: ignore

    _HAS_CHARDET = True
except ImportError:  # pragma: no cover - chardet is optional
    chardet = None  # type: ignore
    _HAS_CHARDET = False


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

    try:
        dataframe = pd.read_csv(file_path)
    except UnicodeDecodeError:
        if not _HAS_CHARDET:
            raise ValueError(
                "Failed to decode CSV file and 'chardet' is not installed for encoding detection"
            )
        with open(file_path, "rb") as file:
            raw_data = file.read()
        result = chardet.detect(raw_data) if _HAS_CHARDET else None
        encoding = result.get("encoding") if result else "utf-8"
        try:
            dataframe = pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError as e:
            raise ValueError(
                f"Failed to decode CSV file '{file_path}' with encoding '{encoding}': {e}"
            ) from e
        except pd.errors.ParserError as e:
            raise ValueError(
                f"Failed to parse CSV file '{file_path}': {e}"
            ) from e
    except pd.errors.ParserError as e:
        raise ValueError(
            f"Failed to parse CSV file '{file_path}': {e}"
        ) from e

    text = dataframe.to_string(index=False)
    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="csv", pages=pages)
