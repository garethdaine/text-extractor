"""Tests for CSV file parser."""

import pytest

from text_extractor.models import ExtractedText
from text_extractor.parsers import csv_parser


class TestCsvParser:
    """Test CSV file parsing functionality."""

    def test_parse_simple_csv_file(self, tmp_path):
        """Test parsing a simple CSV file."""
        test_file = tmp_path / "test.csv"
        test_content = """Name,Age,City
John Doe,30,New York
Jane Smith,25,Los Angeles
Bob Johnson,35,Chicago"""
        test_file.write_text(test_content, encoding="utf-8")

        result = csv_parser.parse(str(test_file))

        assert isinstance(result, ExtractedText)
        assert result.file_type == "csv"
        assert result.ocr_used is False
        assert "Name" in result.text
        assert "Age" in result.text
        assert "City" in result.text
        assert "John Doe" in result.text
        assert "Jane Smith" in result.text
        assert "Bob Johnson" in result.text
        assert len(result.pages) == 1
        assert result.pages[0].page_number == 1
        assert result.pages[0].ocr is False

    def test_parse_csv_with_quotes(self, tmp_path):
        """Test parsing CSV with quoted fields."""
        test_file = tmp_path / "quoted.csv"
        test_content = '''Name,Description
"John Doe","Software Engineer, Senior"
"Jane Smith","Data Scientist, ML Expert"
"Bob Johnson","Product Manager, Technical"'''
        test_file.write_text(test_content, encoding="utf-8")

        result = csv_parser.parse(str(test_file))

        assert result.file_type == "csv"
        assert result.ocr_used is False
        assert "John Doe" in result.text
        assert "Software Engineer, Senior" in result.text
        assert "Jane Smith" in result.text
        assert "Data Scientist, ML Expert" in result.text

    def test_parse_csv_with_special_characters(self, tmp_path):
        """Test parsing CSV with special characters."""
        test_file = tmp_path / "special.csv"
        test_content = """Name,Special_Chars
John Doe,!@#$%^&*()
Jane Smith,éñçüöä
Bob Johnson,你好世界"""
        test_file.write_text(test_content, encoding="utf-8")

        result = csv_parser.parse(str(test_file))

        assert result.file_type == "csv"
        assert "John Doe" in result.text
        assert "!@#$%^&*()" in result.text
        assert "Jane Smith" in result.text
        assert "éñçüöä" in result.text
        assert "Bob Johnson" in result.text
        assert "你好世界" in result.text

    def test_parse_empty_csv(self, tmp_path):
        """Test parsing an empty CSV file."""
        test_file = tmp_path / "empty.csv"
        test_file.write_text("", encoding="utf-8")

        result = csv_parser.parse(str(test_file))

        assert result.file_type == "csv"
        assert result.ocr_used is False
        assert result.text == ""
        assert len(result.pages) == 1
        assert result.pages[0].text == ""

    def test_parse_csv_with_only_headers(self, tmp_path):
        """Test parsing CSV with only headers."""
        test_file = tmp_path / "headers.csv"
        test_content = "Name,Age,City"
        test_file.write_text(test_content, encoding="utf-8")

        result = csv_parser.parse(str(test_file))

        assert result.file_type == "csv"
        assert result.ocr_used is False
        assert "Name" in result.text
        assert "Age" in result.text
        assert "City" in result.text

    def test_parse_csv_with_different_delimiters(self, tmp_path):
        """Test parsing CSV with different delimiters (should use comma by default)."""
        test_file = tmp_path / "semicolon.csv"
        test_content = "Name;Age;City\nJohn;30;NY\nJane;25;LA"
        test_file.write_text(test_content, encoding="utf-8")

        result = csv_parser.parse(str(test_file))

        assert result.file_type == "csv"
        # Should still contain the content even if delimiter is not optimal
        assert "Name" in result.text or "John" in result.text

    def test_parse_nonexistent_csv_file(self):
        """Test that parsing a nonexistent CSV file raises an appropriate error."""
        with pytest.raises(FileNotFoundError):
            csv_parser.parse("nonexistent.csv")

    def test_parse_csv_with_missing_values(self, tmp_path):
        """Test parsing CSV with missing values."""
        test_file = tmp_path / "missing.csv"
        test_content = """Name,Age,City
John Doe,30,
Jane Smith,,Los Angeles
,35,Chicago"""
        test_file.write_text(test_content, encoding="utf-8")

        result = csv_parser.parse(str(test_file))

        assert result.file_type == "csv"
        assert result.ocr_used is False
        assert "John Doe" in result.text
        assert "Jane Smith" in result.text
        assert "Los Angeles" in result.text
        assert "Chicago" in result.text
