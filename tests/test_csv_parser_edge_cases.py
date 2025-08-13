"""
Tests for CSV parser edge cases.
"""

from unittest.mock import patch

import pytest
from pandas.errors import EmptyDataError, ParserError

from text_extractor.parsers.csv_parser import parse


class TestCsvParserEdgeCases:
    """Test CSV parser edge cases and error handling."""

    def test_csv_parser_unicode_decode_error_with_chardet(self):
        """Test CSV parser with Unicode decode error when chardet is available."""
        with patch(
            "text_extractor.parsers.csv_parser.detect_file_encoding"
        ) as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch("text_extractor.parsers.csv_parser.HAS_CHARDET", True):
                with patch("pandas.read_csv") as mock_read:
                    mock_read.side_effect = UnicodeDecodeError(
                        "utf-8", b"", 0, 1, "invalid utf-8"
                    )

                    with pytest.raises(ValueError, match="Failed to decode CSV file"):
                        parse("test.csv")

    def test_csv_parser_unicode_decode_error_without_chardet(self):
        """Test CSV parser with Unicode decode error when chardet is not available."""
        with patch(
            "text_extractor.parsers.csv_parser.detect_file_encoding"
        ) as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch("text_extractor.parsers.csv_parser.HAS_CHARDET", False):
                with patch("pandas.read_csv") as mock_read:
                    mock_read.side_effect = UnicodeDecodeError(
                        "utf-8", b"", 0, 1, "invalid utf-8"
                    )

                    with pytest.raises(
                        ValueError,
                        match="Failed to decode CSV file and 'chardet' is not installed",
                    ):
                        parse("test.csv")

    def test_csv_parser_parser_error(self):
        """Test CSV parser with pandas ParserError."""
        with patch(
            "text_extractor.parsers.csv_parser.detect_file_encoding"
        ) as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch("pandas.read_csv") as mock_read:
                mock_read.side_effect = ParserError("Invalid CSV format")

                with pytest.raises(ValueError, match="Failed to parse CSV file"):
                    parse("test.csv")

    def test_csv_parser_empty_data_error(self):
        """Test CSV parser with pandas EmptyDataError."""
        with patch(
            "text_extractor.parsers.csv_parser.detect_file_encoding"
        ) as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch("pandas.read_csv") as mock_read:
                mock_read.side_effect = EmptyDataError("Empty CSV file")

                result = parse("test.csv")
                assert result.text == ""
                assert result.file_type == "csv"
                assert result.ocr_used is False
                assert len(result.pages) == 1
                assert result.pages[0].text == ""

    def test_csv_parser_unicode_decode_error_with_file_path(self):
        """Test CSV parser Unicode decode error includes file path in error message."""
        with patch(
            "text_extractor.parsers.csv_parser.detect_file_encoding"
        ) as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch("text_extractor.parsers.csv_parser.HAS_CHARDET", True):
                with patch("pandas.read_csv") as mock_read:
                    mock_read.side_effect = UnicodeDecodeError(
                        "utf-8", b"", 0, 1, "invalid utf-8"
                    )

                    with pytest.raises(
                        ValueError, match="Failed to decode CSV file 'test.csv'"
                    ):
                        parse("test.csv")

    def test_csv_parser_parser_error_with_file_path(self):
        """Test CSV parser ParserError includes file path in error message."""
        with patch(
            "text_extractor.parsers.csv_parser.detect_file_encoding"
        ) as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch("pandas.read_csv") as mock_read:
                mock_read.side_effect = ParserError("Invalid CSV format")

                with pytest.raises(
                    ValueError, match="Failed to parse CSV file 'test.csv'"
                ):
                    parse("test.csv")

    def test_csv_parser_unicode_decode_error_with_encoding_info(self):
        """Test CSV parser Unicode decode error includes encoding information."""
        with patch(
            "text_extractor.parsers.csv_parser.detect_file_encoding"
        ) as mock_detect:
            mock_detect.return_value = "latin-1"
            with patch("text_extractor.parsers.csv_parser.HAS_CHARDET", True):
                with patch("pandas.read_csv") as mock_read:
                    mock_read.side_effect = UnicodeDecodeError(
                        "latin-1", b"", 0, 1, "invalid latin-1"
                    )

                    with pytest.raises(
                        ValueError,
                        match="Failed to decode CSV file 'test.csv' with encoding 'latin-1'",
                    ):
                        parse("test.csv")

    def test_csv_parser_empty_data_error_structure(self):
        """Test CSV parser EmptyDataError returns correct structure."""
        with patch(
            "text_extractor.parsers.csv_parser.detect_file_encoding"
        ) as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch("pandas.read_csv") as mock_read:
                mock_read.side_effect = EmptyDataError("Empty CSV file")

                result = parse("test.csv")
                assert result.text == ""
                assert result.file_type == "csv"
                assert result.ocr_used is False
                assert len(result.pages) == 1
                assert result.pages[0].page_number == 1
                assert result.pages[0].text == ""
                assert result.pages[0].ocr is False

    def test_csv_parser_unicode_decode_error_different_encodings(self):
        """Test CSV parser Unicode decode error with different encodings."""
        test_encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]

        for encoding in test_encodings:
            with patch(
                "text_extractor.parsers.csv_parser.detect_file_encoding"
            ) as mock_detect:
                mock_detect.return_value = encoding
                with patch("text_extractor.parsers.csv_parser.HAS_CHARDET", True):
                    with patch("pandas.read_csv") as mock_read:
                        mock_read.side_effect = UnicodeDecodeError(
                            encoding, b"", 0, 1, f"invalid {encoding}"
                        )

                        with pytest.raises(
                            ValueError,
                            match=f"Failed to decode CSV file 'test.csv' with encoding '{encoding}'",
                        ):
                            parse("test.csv")

    def test_csv_parser_parser_error_different_messages(self):
        """Test CSV parser ParserError with different error messages."""
        test_messages = [
            "Invalid CSV format",
            "Expected 3 columns, got 2",
            "Error tokenizing data",
            "No columns to parse from file",
        ]

        for message in test_messages:
            with patch(
                "text_extractor.parsers.csv_parser.detect_file_encoding"
            ) as mock_detect:
                mock_detect.return_value = "utf-8"
                with patch("pandas.read_csv") as mock_read:
                    mock_read.side_effect = ParserError(message)

                    with pytest.raises(
                        ValueError,
                        match=f"Failed to parse CSV file 'test.csv': {message}",
                    ):
                        parse("test.csv")
