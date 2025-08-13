"""
Tests for TXT parser edge cases.
"""

from unittest.mock import MagicMock, patch

import pytest

from text_extractor.parsers.txt_parser import parse


class TestTxtParserEdgeCases:
    """Test TXT parser edge cases and error handling."""

    def test_txt_parser_unicode_decode_error_with_chardet(self):
        """Test TXT parser with Unicode decode error when chardet is available."""
        with patch(
            "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
        ) as mock_read:
            # Return bytes that will cause a UnicodeDecodeError when decoded
            mock_read.return_value = (b"\xff\xfe\x00\x00", "utf-8")
            with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", True):
                with pytest.raises(ValueError, match="Failed to decode text file"):
                    parse("test.txt")

    def test_txt_parser_unicode_decode_error_without_chardet(self):
        """Test TXT parser with Unicode decode error when chardet is not available."""
        with patch(
            "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
        ) as mock_read:
            # Return bytes that will cause a UnicodeDecodeError when decoded
            mock_read.return_value = (b"\xff\xfe\x00\x00", "utf-8")
            with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", False):
                with pytest.raises(
                    ValueError,
                    match="Failed to decode text file and 'chardet' is not installed",
                ):
                    parse("test.txt")

    def test_txt_parser_unicode_decode_error_with_file_path(self):
        """Test TXT parser Unicode decode error includes file path in error message."""
        with patch(
            "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
        ) as mock_read:
            # Return bytes that will cause a UnicodeDecodeError when decoded
            mock_read.return_value = (b"\xff\xfe\x00\x00", "utf-8")
            with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", True):
                with pytest.raises(
                    ValueError, match="Failed to decode text file 'test.txt'"
                ):
                    parse("test.txt")

    def test_txt_parser_unicode_decode_error_with_encoding_info(self):
        """Test TXT parser Unicode decode error includes encoding information."""
        with patch(
            "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
        ) as mock_read:
            # Return bytes that will cause a UnicodeDecodeError when decoded
            mock_read.return_value = (b"\xff\xfe\x00\x00", "latin-1")
            with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", True):
                # Create a mock bytes object that raises UnicodeDecodeError when decoded
                mock_bytes = MagicMock()
                mock_bytes.decode.side_effect = UnicodeDecodeError(
                    "latin-1", b"\xff\xfe\x00\x00", 0, 1, "invalid"
                )
                mock_read.return_value = (mock_bytes, "latin-1")
                with pytest.raises(
                    ValueError,
                    match="Failed to decode text file 'test.txt' with encoding 'latin-1'",
                ):
                    parse("test.txt")

    def test_txt_parser_unicode_decode_error_different_encodings(self):
        """Test TXT parser Unicode decode error with different encodings."""
        test_encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]

        for encoding in test_encodings:
            with patch(
                "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
            ) as mock_read:
                # Create a mock bytes object that raises UnicodeDecodeError when decoded
                mock_bytes = MagicMock()
                mock_bytes.decode.side_effect = UnicodeDecodeError(
                    encoding, b"\xff\xfe\x00\x00", 0, 1, "invalid"
                )
                mock_read.return_value = (mock_bytes, encoding)
                with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", True):
                    with pytest.raises(
                        ValueError,
                        match=f"Failed to decode text file 'test.txt' with encoding '{encoding}'",
                    ):
                        parse("test.txt")

    def test_txt_parser_unicode_decode_error_without_chardet_different_encodings(self):
        """Test TXT parser Unicode decode error without chardet with different encodings."""
        test_encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]

        for encoding in test_encodings:
            with patch(
                "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
            ) as mock_read:
                # Create a mock bytes object that raises UnicodeDecodeError when decoded
                mock_bytes = MagicMock()
                mock_bytes.decode.side_effect = UnicodeDecodeError(
                    encoding, b"\xff\xfe\x00\x00", 0, 1, "invalid"
                )
                mock_read.return_value = (mock_bytes, encoding)
                with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", False):
                    with pytest.raises(
                        ValueError,
                        match="Failed to decode text file and 'chardet' is not installed",
                    ):
                        parse("test.txt")

    def test_txt_parser_unicode_decode_error_with_different_file_paths(self):
        """Test TXT parser Unicode decode error with different file paths."""
        test_paths = ["test.txt", "document.txt", "file.txt", "data.txt"]

        for file_path in test_paths:
            with patch(
                "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
            ) as mock_read:
                # Return bytes that will cause a UnicodeDecodeError when decoded
                mock_read.return_value = (b"\xff\xfe\x00\x00", "utf-8")
                with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", True):
                    with pytest.raises(
                        ValueError, match=f"Failed to decode text file '{file_path}'"
                    ):
                        parse(file_path)

    def test_txt_parser_unicode_decode_error_with_chardet_detailed_error(self):
        """Test TXT parser Unicode decode error with chardet includes detailed error information."""
        with patch(
            "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
        ) as mock_read:
            # Return bytes that will cause a UnicodeDecodeError when decoded
            mock_read.return_value = (b"\xff\xfe\x00\x00", "utf-8")
            with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", True):
                with pytest.raises(
                    ValueError,
                    match="Failed to decode text file 'test.txt' with encoding 'utf-8':",
                ):
                    parse("test.txt")

    def test_txt_parser_unicode_decode_error_without_chardet_simple_message(self):
        """Test TXT parser Unicode decode error without chardet has simple error message."""
        with patch(
            "text_extractor.parsers.txt_parser.read_file_with_encoding_detection"
        ) as mock_read:
            # Return bytes that will cause a UnicodeDecodeError when decoded
            mock_read.return_value = (b"\xff\xfe\x00\x00", "utf-8")
            with patch("text_extractor.parsers.txt_parser.HAS_CHARDET", False):
                with pytest.raises(
                    ValueError,
                    match="Failed to decode text file and 'chardet' is not installed for encoding detection",
                ):
                    parse("test.txt")
