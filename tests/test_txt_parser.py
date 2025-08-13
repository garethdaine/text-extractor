"""Tests for text file parser."""

import pytest

from text_extractor.models import ExtractedText
from text_extractor.parsers import txt_parser


class TestTxtParser:
    """Test text file parsing functionality."""

    def test_parse_simple_text_file(self, tmp_path):
        """Test parsing a simple text file."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!\nThis is a test file."
        test_file.write_text(test_content, encoding="utf-8")

        result = txt_parser.parse(str(test_file))

        assert isinstance(result, ExtractedText)
        assert result.file_type == "txt"
        assert result.ocr_used is False
        assert "Hello, World!" in result.text
        assert "This is a test file." in result.text
        assert len(result.pages) == 1
        assert result.pages[0].page_number == 1
        assert result.pages[0].ocr is False

    def test_parse_multiline_text_file(self, tmp_path):
        """Test parsing a multi-line text file."""
        test_file = tmp_path / "test.txt"
        test_content = """Line 1
Line 2
Line 3
Line 4"""
        test_file.write_text(test_content, encoding="utf-8")

        result = txt_parser.parse(str(test_file))

        assert result.file_type == "txt"
        assert result.ocr_used is False
        assert "Line 1" in result.text
        assert "Line 2" in result.text
        assert "Line 3" in result.text
        assert "Line 4" in result.text

    def test_parse_empty_file(self, tmp_path):
        """Test parsing an empty text file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("", encoding="utf-8")

        result = txt_parser.parse(str(test_file))

        assert result.file_type == "txt"
        assert result.ocr_used is False
        assert result.text == ""
        assert len(result.pages) == 1
        assert result.pages[0].text == ""

    def test_parse_file_with_special_characters(self, tmp_path):
        """Test parsing a file with special characters."""
        test_file = tmp_path / "special.txt"
        test_content = "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        test_file.write_text(test_content, encoding="utf-8")

        result = txt_parser.parse(str(test_file))

        assert result.file_type == "txt"
        assert "Special chars:" in result.text
        assert "!@#$%^&*()" in result.text

    def test_parse_file_with_unicode(self, tmp_path):
        """Test parsing a file with Unicode characters."""
        test_file = tmp_path / "unicode.txt"
        test_content = "Unicode: 你好世界 🌍 éñç"
        test_file.write_text(test_content, encoding="utf-8")

        result = txt_parser.parse(str(test_file))

        assert result.file_type == "txt"
        assert "Unicode:" in result.text
        assert "你好世界" in result.text
        assert "🌍" in result.text
        assert "éñç" in result.text

    def test_parse_nonexistent_file(self):
        """Test that parsing a nonexistent file raises an appropriate error."""
        with pytest.raises(FileNotFoundError):
            txt_parser.parse("nonexistent.txt")

    def test_parse_with_different_encodings(self, tmp_path):
        """Test parsing files with different encodings."""
        test_content = "Test content with encoding"

        # Test UTF-8
        utf8_file = tmp_path / "utf8.txt"
        utf8_file.write_text(test_content, encoding="utf-8")
        result_utf8 = txt_parser.parse(str(utf8_file))
        assert result_utf8.text == test_content

        # Test ASCII
        ascii_file = tmp_path / "ascii.txt"
        ascii_file.write_text(test_content, encoding="ascii")
        result_ascii = txt_parser.parse(str(ascii_file))
        assert result_ascii.text == test_content
