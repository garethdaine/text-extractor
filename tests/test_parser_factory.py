"""Tests for parser factory functionality."""

import pytest

from text_extractor.parser_factory import _MIME_TYPE_MAP, _PARSERS, select_parser


class TestParserSelection:
    """Test parser selection functionality."""

    def test_select_parser_by_extension(self):
        """Test parser selection using file extension."""
        parsers = {
            "document.pdf": _PARSERS["pdf"],
            "report.docx": _PARSERS["docx"],
            "data.csv": _PARSERS["csv"],
            "notes.txt": _PARSERS["txt"],
            "image.png": _PARSERS["png"],
            "photo.jpg": _PARSERS["jpg"],
        }

        for file_path, expected_parser in parsers.items():
            selected_parser = select_parser(file_path)
            assert selected_parser == expected_parser

    def test_select_parser_by_mime_type(self):
        """Test parser selection using MIME type."""
        mime_test_cases = [
            ("application/pdf", _PARSERS["pdf"]),
            ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", _PARSERS["docx"]),
            ("text/csv", _PARSERS["csv"]),
            ("text/plain", _PARSERS["txt"]),
            ("image/png", _PARSERS["png"]),
            ("image/jpeg", _PARSERS["jpg"]),
        ]

        for mime_type, expected_parser in mime_test_cases:
            selected_parser = select_parser("dummy.file", mime_type=mime_type)
            assert selected_parser == expected_parser

    def test_unsupported_mime_type(self):
        """Test that unsupported MIME types raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported MIME type"):
            select_parser("dummy.file", mime_type="application/unknown")

    def test_unsupported_file_type(self):
        """Test that unsupported file types raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported file type"):
            select_parser("document.xyz")

    def test_mime_type_override_extension(self):
        """Test that MIME type overrides file extension."""
        # Use a .txt file but specify PDF MIME type
        selected_parser = select_parser("document.txt", mime_type="application/pdf")
        assert selected_parser == _PARSERS["pdf"]


class TestParserRegistry:
    """Test parser registry completeness."""

    def test_all_supported_types_have_parsers(self):
        """Test that all supported file types have corresponding parsers."""
        from text_extractor.utils import _SUPPORTED_TYPES

        for _extension, file_type in _SUPPORTED_TYPES.items():
            assert file_type in _PARSERS, f"No parser for file type: {file_type}"

    def test_all_mime_types_have_parsers(self):
        """Test that all MIME types have corresponding parsers."""
        for mime_type, file_type in _MIME_TYPE_MAP.items():
            assert file_type in _PARSERS, f"No parser for MIME type: {mime_type}"
