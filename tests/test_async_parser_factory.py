"""
Tests for async parser factory.
"""

import pytest
from unittest.mock import patch

from text_extractor.async_parser_factory import (
    select_async_parser,
    extract_text_from_file_async,
    _ASYNC_PARSERS,
    _MIME_TYPE_MAP,
)


class TestAsyncParserFactory:
    """Test async parser factory functionality."""

    def test_select_async_parser_by_extension(self):
        """Test selecting async parser by file extension."""
        parser = select_async_parser("test.pdf")
        assert parser == _ASYNC_PARSERS["pdf"]

        parser = select_async_parser("test.docx")
        assert parser == _ASYNC_PARSERS["docx"]

        parser = select_async_parser("test.csv")
        assert parser == _ASYNC_PARSERS["csv"]

        parser = select_async_parser("test.txt")
        assert parser == _ASYNC_PARSERS["txt"]

        parser = select_async_parser("test.png")
        assert parser == _ASYNC_PARSERS["png"]

        parser = select_async_parser("test.jpg")
        assert parser == _ASYNC_PARSERS["jpg"]

        parser = select_async_parser("test.webp")
        assert parser == _ASYNC_PARSERS["webp"]

    def test_select_async_parser_by_mime_type(self):
        """Test selecting async parser by MIME type."""
        parser = select_async_parser("test.unknown", "application/pdf")
        assert parser == _ASYNC_PARSERS["pdf"]

        parser = select_async_parser("test.unknown", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        assert parser == _ASYNC_PARSERS["docx"]

        parser = select_async_parser("test.unknown", "text/csv")
        assert parser == _ASYNC_PARSERS["csv"]

        parser = select_async_parser("test.unknown", "text/plain")
        assert parser == _ASYNC_PARSERS["txt"]

        parser = select_async_parser("test.unknown", "image/png")
        assert parser == _ASYNC_PARSERS["png"]

        parser = select_async_parser("test.unknown", "image/jpeg")
        assert parser == _ASYNC_PARSERS["jpg"]

        parser = select_async_parser("test.unknown", "image/webp")
        assert parser == _ASYNC_PARSERS["webp"]

    def test_select_async_parser_unsupported_mime_type(self):
        """Test selecting async parser with unsupported MIME type."""
        with pytest.raises(ValueError, match="Unsupported MIME type"):
            select_async_parser("test.unknown", "application/unsupported")

    def test_select_async_parser_unsupported_file_type(self):
        """Test selecting async parser with unsupported file type."""
        with pytest.raises(ValueError, match="Unsupported file type"):
            select_async_parser("test.unsupported")

    def test_select_async_parser_mime_type_override_extension(self):
        """Test that MIME type overrides file extension."""
        # Use a file with .txt extension but PDF MIME type
        parser = select_async_parser("test.txt", "application/pdf")
        assert parser == _ASYNC_PARSERS["pdf"]

    @pytest.mark.asyncio
    async def test_extract_text_from_file_async_success(self):
        """Test successful async text extraction."""
        with patch('text_extractor.async_parser_factory.select_async_parser') as mock_select:
            async def mock_parser(file_path):
                return "Mock result"

            mock_select.return_value = mock_parser

            result = await extract_text_from_file_async("test.txt")
            assert result == "Mock result"
            mock_select.assert_called_once_with("test.txt")

    @pytest.mark.asyncio
    async def test_extract_text_from_file_async_parser_error(self):
        """Test async text extraction with parser error."""
        with patch('text_extractor.async_parser_factory.select_async_parser') as mock_select:
            mock_parser = mock_select.return_value
            mock_parser.side_effect = Exception("Parser error")

            with pytest.raises(Exception, match="Parser error"):
                await extract_text_from_file_async("test.txt")

    def test_async_parser_registry_completeness(self):
        """Test that all supported file types have async parsers."""
        supported_types = ["pdf", "docx", "csv", "txt", "png", "jpg", "webp"]

        for file_type in supported_types:
            assert file_type in _ASYNC_PARSERS, f"Missing async parser for {file_type}"

    def test_mime_type_map_completeness(self):
        """Test that all MIME types map to supported file types."""
        supported_types = ["pdf", "docx", "csv", "txt", "png", "jpg", "webp"]

        for mime_type, file_type in _MIME_TYPE_MAP.items():
            assert file_type in supported_types, f"Invalid file type {file_type} for MIME type {mime_type}"

    def test_async_parser_interface(self):
        """Test that all async parsers are callable."""
        for file_type, parser in _ASYNC_PARSERS.items():
            assert callable(parser), f"Async parser for {file_type} is not callable"

    def test_mime_type_mapping_consistency(self):
        """Test that MIME type mappings are consistent with file extensions."""
        # Test that PDF MIME type maps to pdf
        assert _MIME_TYPE_MAP["application/pdf"] == "pdf"

        # Test that DOCX MIME type maps to docx
        assert _MIME_TYPE_MAP["application/vnd.openxmlformats-officedocument.wordprocessingml.document"] == "docx"

        # Test that CSV MIME type maps to csv
        assert _MIME_TYPE_MAP["text/csv"] == "csv"

        # Test that plain text MIME type maps to txt
        assert _MIME_TYPE_MAP["text/plain"] == "txt"

        # Test that image MIME types map to correct file types
        assert _MIME_TYPE_MAP["image/png"] == "png"
        assert _MIME_TYPE_MAP["image/jpeg"] == "jpg"
        assert _MIME_TYPE_MAP["image/webp"] == "webp"
