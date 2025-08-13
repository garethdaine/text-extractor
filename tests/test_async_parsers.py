"""
Tests for async parsers.
"""

import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from text_extractor.async_parsers import (
    async_csv_parser,
    async_docx_parser,
    async_image_parser,
    async_pdf_parser,
    async_txt_parser,
)
from text_extractor.models import ExtractedText


class TestAsyncCsvParser:
    """Test async CSV parser."""

    @pytest.mark.asyncio
    async def test_async_csv_parser_success(self):
        """Test successful async CSV parsing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("name,age,city\nJohn,30,New York\nJane,25,Boston")
            file_path = f.name

        try:
            result = await async_csv_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "csv"
            assert result.ocr_used is False
            assert len(result.pages) == 1
            assert "John" in result.text
            assert "Jane" in result.text
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_csv_parser_empty_file(self):
        """Test async CSV parsing with empty file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("")
            file_path = f.name

        try:
            result = await async_csv_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "csv"
            assert result.ocr_used is False
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_csv_parser_with_quotes(self):
        """Test async CSV parsing with quoted values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(
                'name,description\n"John Doe","Software Engineer"\n"Jane Smith","Data Scientist"'
            )
            file_path = f.name

        try:
            result = await async_csv_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "csv"
            assert "John Doe" in result.text
            assert "Jane Smith" in result.text
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_csv_parser_file_not_found(self):
        """Test async CSV parser with non-existent file."""
        with pytest.raises(FileNotFoundError):
            await async_csv_parser.parse("nonexistent.csv")

    @pytest.mark.asyncio
    async def test_async_csv_parser_error_handling(self):
        """Test async CSV parser error handling."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            # Create a file that's not readable as CSV
            f.write("invalid,csv,content\nwith,malformed,data\n")
            file_path = f.name

        try:
            result = await async_csv_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "csv"
        finally:
            Path(file_path).unlink()


class TestAsyncDocxParser:
    """Test async DOCX parser."""

    @pytest.mark.asyncio
    async def test_async_docx_parser_success(self):
        """Test successful async DOCX parsing."""
        # Create a simple DOCX file for testing
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            # This is a minimal DOCX file structure
            file_path = f.name

        try:
            # Mock the docx.Document to avoid actual DOCX parsing
            with patch("docx.Document") as mock_docx:
                mock_doc = AsyncMock()
                mock_doc.paragraphs = [
                    AsyncMock(text="Test paragraph 1"),
                    AsyncMock(text="Test paragraph 2"),
                ]
                mock_doc.tables = []
                mock_docx.return_value = mock_doc

                result = await async_docx_parser.parse(file_path)
                assert isinstance(result, ExtractedText)
                assert result.file_type == "docx"
                assert result.ocr_used is False
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_docx_parser_empty_document(self):
        """Test async DOCX parsing with empty document."""
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            file_path = f.name

        try:
            with patch("docx.Document") as mock_docx:
                mock_doc = AsyncMock()
                mock_doc.paragraphs = []
                mock_doc.tables = []
                mock_docx.return_value = mock_doc

                result = await async_docx_parser.parse(file_path)
                assert isinstance(result, ExtractedText)
                assert result.file_type == "docx"
                assert result.text == ""
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_docx_parser_file_not_found(self):
        """Test async DOCX parser with non-existent file."""
        with pytest.raises(FileNotFoundError):
            await async_docx_parser.parse("nonexistent.docx")

    @pytest.mark.asyncio
    async def test_async_docx_parser_error_handling(self):
        """Test async DOCX parser error handling."""
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            file_path = f.name

        try:
            with patch("docx.Document") as mock_docx:
                mock_docx.side_effect = Exception("DOCX parsing error")

                with pytest.raises(Exception, match="DOCX parsing error"):
                    await async_docx_parser.parse(file_path)
        finally:
            Path(file_path).unlink()


class TestAsyncImageParser:
    """Test async image parser."""

    @pytest.mark.asyncio
    async def test_async_image_parser_success(self):
        """Test successful async image parsing."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            file_path = f.name

        try:
            with patch("text_extractor.async_parsers.async_image_parser.Image.open"):
                with patch(
                    "text_extractor.async_parsers.async_image_parser.pytesseract.image_to_string"
                ) as mock_ocr:
                    mock_ocr.return_value = "Test OCR text from image"

                    result = await async_image_parser.parse(file_path)
                    assert isinstance(result, ExtractedText)
                    assert result.file_type == "png"
                    assert result.ocr_used is True
                    assert "Test OCR text from image" in result.text
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_image_parser_jpg(self):
        """Test async image parsing with JPG file."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            file_path = f.name

        try:
            with patch("text_extractor.async_parsers.async_image_parser.Image.open"):
                with patch(
                    "text_extractor.async_parsers.async_image_parser.pytesseract.image_to_string"
                ) as mock_ocr:
                    mock_ocr.return_value = "JPG OCR text"

                    result = await async_image_parser.parse(file_path)
                    assert isinstance(result, ExtractedText)
                    assert result.file_type == "jpg"
                    assert result.ocr_used is True
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_image_parser_webp(self):
        """Test async image parsing with WEBP file."""
        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as f:
            file_path = f.name

        try:
            with patch("text_extractor.async_parsers.async_image_parser.Image.open"):
                with patch(
                    "text_extractor.async_parsers.async_image_parser.pytesseract.image_to_string"
                ) as mock_ocr:
                    mock_ocr.return_value = "WEBP OCR text"

                    result = await async_image_parser.parse(file_path)
                    assert isinstance(result, ExtractedText)
                    assert result.file_type == "webp"
                    assert result.ocr_used is True
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_image_parser_empty_ocr_result(self):
        """Test async image parsing with empty OCR result."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            file_path = f.name

        try:
            with patch("text_extractor.async_parsers.async_image_parser.Image.open"):
                with patch(
                    "text_extractor.async_parsers.async_image_parser.pytesseract.image_to_string"
                ) as mock_ocr:
                    mock_ocr.return_value = ""

                    result = await async_image_parser.parse(file_path)
                    assert isinstance(result, ExtractedText)
                    assert result.file_type == "png"
                    assert result.ocr_used is True
                    assert result.text == ""
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_image_parser_file_not_found(self):
        """Test async image parser with non-existent file."""
        with pytest.raises(FileNotFoundError):
            await async_image_parser.parse("nonexistent.png")

    @pytest.mark.asyncio
    async def test_async_image_parser_ocr_error(self):
        """Test async image parser with OCR error."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            file_path = f.name

        try:
            # Create a mock image that can be used as a context manager
            mock_image = MagicMock()
            mock_image.__enter__ = MagicMock(return_value=mock_image)
            mock_image.__exit__ = MagicMock(return_value=None)

            with patch(
                "text_extractor.async_parsers.async_image_parser.Image.open",
                return_value=mock_image,
            ):
                with patch(
                    "text_extractor.async_parsers.async_image_parser.pytesseract.image_to_string"
                ) as mock_ocr:
                    mock_ocr.side_effect = Exception("OCR error")

                    with pytest.raises(RuntimeError):
                        await async_image_parser.parse(file_path)
        finally:
            Path(file_path).unlink()


class TestAsyncPdfParser:
    """Test async PDF parser."""

    @pytest.mark.asyncio
    async def test_async_pdf_parser_success(self):
        """Test successful async PDF parsing."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            file_path = f.name

        try:
            with patch("pdfminer.high_level.extract_pages") as mock_extract:
                # Mock PDF page layout with text containers
                from pdfminer.layout import LTTextContainer

                mock_text_container = AsyncMock(spec=LTTextContainer)
                mock_text_container.get_text.return_value = "Test PDF text"
                mock_extract.return_value = [[mock_text_container]]

                result = await async_pdf_parser.parse(file_path)
                assert isinstance(result, ExtractedText)
                assert result.file_type == "pdf"
                assert result.ocr_used is False
                assert "Test PDF text" in result.text
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_pdf_parser_multiple_pages(self):
        """Test async PDF parsing with multiple pages."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            file_path = f.name

        try:
            with patch("pdfminer.high_level.extract_pages") as mock_extract:
                # Mock multiple PDF pages with text containers
                from pdfminer.layout import LTTextContainer

                mock_text_container1 = AsyncMock(spec=LTTextContainer)
                mock_text_container1.get_text.return_value = "Page 1 text"
                mock_text_container2 = AsyncMock(spec=LTTextContainer)
                mock_text_container2.get_text.return_value = "Page 2 text"
                mock_extract.return_value = [
                    [mock_text_container1],
                    [mock_text_container2],
                ]

                result = await async_pdf_parser.parse(file_path)
                assert isinstance(result, ExtractedText)
                assert result.file_type == "pdf"
                assert result.ocr_used is False
                assert "Page 1 text" in result.text
                assert "Page 2 text" in result.text
                assert len(result.pages) == 2
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_pdf_parser_empty_pdf(self):
        """Test async PDF parsing with empty PDF."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            file_path = f.name

        try:
            with patch("pdfminer.high_level.extract_pages") as mock_extract:
                mock_extract.return_value = []

                result = await async_pdf_parser.parse(file_path)
                assert isinstance(result, ExtractedText)
                assert result.file_type == "pdf"
                assert result.ocr_used is False
                assert result.text == ""
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_pdf_parser_file_not_found(self):
        """Test async PDF parser with non-existent file."""
        with pytest.raises(FileNotFoundError):
            await async_pdf_parser.parse("nonexistent.pdf")

    @pytest.mark.asyncio
    async def test_async_pdf_parser_error_handling(self):
        """Test async PDF parser error handling."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            file_path = f.name

        try:
            with patch("pdfminer.high_level.extract_pages") as mock_extract:
                mock_extract.side_effect = Exception("PDF parsing error")

                with pytest.raises(Exception, match="PDF parsing error"):
                    await async_pdf_parser.parse(file_path)
        finally:
            Path(file_path).unlink()


class TestAsyncTxtParser:
    """Test async TXT parser."""

    @pytest.mark.asyncio
    async def test_async_txt_parser_success(self):
        """Test successful async TXT parsing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test text content for async parsing")
            file_path = f.name

        try:
            result = await async_txt_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "txt"
            assert result.ocr_used is False
            assert "Test text content for async parsing" in result.text
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_txt_parser_empty_file(self):
        """Test async TXT parsing with empty file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            file_path = f.name

        try:
            result = await async_txt_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "txt"
            assert result.ocr_used is False
            assert result.text == ""
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_txt_parser_multiline_content(self):
        """Test async TXT parsing with multiline content."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Line 1\nLine 2\nLine 3")
            file_path = f.name

        try:
            result = await async_txt_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "txt"
            assert result.ocr_used is False
            assert "Line 1" in result.text
            assert "Line 2" in result.text
            assert "Line 3" in result.text
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_txt_parser_unicode_content(self):
        """Test async TXT parsing with Unicode content."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Unicode content: 🚀 📊 💻")
            file_path = f.name

        try:
            result = await async_txt_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "txt"
            assert result.ocr_used is False
            assert "Unicode content" in result.text
        finally:
            Path(file_path).unlink()

    @pytest.mark.asyncio
    async def test_async_txt_parser_file_not_found(self):
        """Test async TXT parser with non-existent file."""
        with pytest.raises(FileNotFoundError):
            await async_txt_parser.parse("nonexistent.txt")

    @pytest.mark.asyncio
    async def test_async_txt_parser_encoding_error(self):
        """Test async TXT parser with encoding error."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            # Write binary data that's not valid UTF-8
            f.write(b"\xff\xfe\x00\x00")  # Invalid UTF-8
            file_path = f.name

        try:
            result = await async_txt_parser.parse(file_path)
            assert isinstance(result, ExtractedText)
            assert result.file_type == "txt"
        finally:
            Path(file_path).unlink()
