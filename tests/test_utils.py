"""Tests for utility functions."""


import pytest

from text_extractor.utils import (
    detect_file_encoding,
    read_file_with_encoding_detection,
    resolve_file_type,
)


class TestResolveFileType:
    """Test file type resolution."""

    def test_supported_extensions(self):
        """Test that all supported extensions are resolved correctly."""
        test_cases = [
            ("document.pdf", "pdf"),
            ("report.docx", "docx"),
            ("data.csv", "csv"),
            ("notes.txt", "txt"),
            ("image.png", "png"),
            ("photo.jpg", "jpg"),
            ("photo.jpeg", "jpg"),
        ]

        for file_path, expected_type in test_cases:
            assert resolve_file_type(file_path) == expected_type

    def test_case_insensitive(self):
        """Test that file extensions are case insensitive."""
        assert resolve_file_type("document.PDF") == "pdf"
        assert resolve_file_type("report.DOCX") == "docx"

    def test_unsupported_extension(self):
        """Test that unsupported extensions raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported file type"):
            resolve_file_type("document.xyz")


class TestFileEncoding:
    """Test file encoding detection."""

    def test_read_file_with_encoding_detection(self, tmp_path):
        """Test reading file with encoding detection."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World! 你好"
        test_file.write_text(test_content, encoding="utf-8")

        raw_data, encoding = read_file_with_encoding_detection(str(test_file))
        assert raw_data.decode(encoding) == test_content
        assert encoding in ["utf-8", "ascii"]  # chardet might detect either

    def test_detect_file_encoding(self, tmp_path):
        """Test encoding detection without loading entire file."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World! 你好"
        test_file.write_text(test_content, encoding="utf-8")

        encoding = detect_file_encoding(str(test_file))
        assert encoding in ["utf-8", "ascii"]  # chardet might detect either

    def test_detect_file_encoding_with_default(self, tmp_path):
        """Test encoding detection with custom default."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content, encoding="utf-8")

        encoding = detect_file_encoding(str(test_file), default="latin-1")
        assert encoding in ["utf-8", "ascii", "latin-1"]  # chardet might detect any
