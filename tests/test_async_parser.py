"""Tests for async parser functionality."""

import pytest

from text_extractor import extract_text_from_file_async
from text_extractor.async_parser_factory import select_async_parser


class TestAsyncParser:
    """Test async parser functionality."""

    @pytest.mark.asyncio
    async def test_async_txt_parser(self, tmp_path):
        """Test async text file parsing."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!\nThis is a test file."
        test_file.write_text(test_content, encoding="utf-8")

        result = await extract_text_from_file_async(str(test_file))

        assert result.file_type == "txt"
        assert result.ocr_used is False
        assert "Hello, World!" in result.text
        assert "This is a test file." in result.text
        assert len(result.pages) == 1
        assert result.pages[0].page_number == 1
        assert result.pages[0].ocr is False

    @pytest.mark.asyncio
    async def test_async_csv_parser(self, tmp_path):
        """Test async CSV file parsing."""
        test_file = tmp_path / "test.csv"
        test_content = """Name,Age,City
John Doe,30,New York
Jane Smith,25,Los Angeles"""
        test_file.write_text(test_content, encoding="utf-8")

        result = await extract_text_from_file_async(str(test_file))

        assert result.file_type == "csv"
        assert result.ocr_used is False
        assert "Name" in result.text
        assert "John Doe" in result.text
        assert "Jane Smith" in result.text

    @pytest.mark.asyncio
    async def test_async_parser_selection(self):
        """Test async parser selection."""
        # Test that we can select async parsers
        parser = select_async_parser("test.txt")
        assert parser is not None

        # Test unsupported file type
        with pytest.raises(ValueError, match="Unsupported file type"):
            select_async_parser("test.xyz")

    @pytest.mark.asyncio
    async def test_async_parser_error_handling(self):
        """Test async parser error handling."""
        with pytest.raises(FileNotFoundError):
            await extract_text_from_file_async("nonexistent.txt")

        with pytest.raises(ValueError, match="Unsupported file type"):
            await extract_text_from_file_async("test.xyz")
