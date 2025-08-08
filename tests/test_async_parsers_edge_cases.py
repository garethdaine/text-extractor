"""
Edge case tests for async parsers to achieve 100% coverage.
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
from docx.opc.exceptions import PackageNotFoundError
from pdf2image.exceptions import PDFPageCountError
import pytesseract

from text_extractor.async_parsers.async_csv_parser import parse as parse_csv
from text_extractor.async_parsers.async_docx_parser import parse as parse_docx
from text_extractor.async_parsers.async_pdf_parser import parse as parse_pdf


class TestAsyncCSVParserEdgeCases:
    """Test edge cases for async CSV parser."""

    @pytest.mark.asyncio
    async def test_csv_parser_unicode_decode_error_with_chardet(self):
        """Test CSV parser Unicode decode error with chardet available."""
        with patch('text_extractor.async_parsers.async_csv_parser.detect_file_encoding') as mock_detect:
            mock_detect.return_value = "latin-1"
            with patch('text_extractor.async_parsers.async_csv_parser.HAS_CHARDET', True):
                with patch('pandas.read_csv') as mock_read:
                    mock_read.side_effect = UnicodeDecodeError("latin-1", b"", 0, 1, "invalid")
                    with pytest.raises(ValueError, match="Failed to decode CSV file 'test.csv' with encoding 'latin-1'"):
                        await parse_csv("test.csv")

    @pytest.mark.asyncio
    async def test_csv_parser_unicode_decode_error_without_chardet(self):
        """Test CSV parser Unicode decode error without chardet."""
        with patch('text_extractor.async_parsers.async_csv_parser.detect_file_encoding') as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch('text_extractor.async_parsers.async_csv_parser.HAS_CHARDET', False):
                with patch('pandas.read_csv') as mock_read:
                    mock_read.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")
                    with pytest.raises(ValueError, match="Failed to decode CSV file and 'chardet' is not installed"):
                        await parse_csv("test.csv")

    @pytest.mark.asyncio
    async def test_csv_parser_parser_error(self):
        """Test CSV parser ParserError handling."""
        with patch('text_extractor.async_parsers.async_csv_parser.detect_file_encoding') as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch('pandas.read_csv') as mock_read:
                mock_read.side_effect = ParserError("Invalid CSV format")
                with pytest.raises(ValueError, match="Failed to parse CSV file 'test.csv'"):
                    await parse_csv("test.csv")

    @pytest.mark.asyncio
    async def test_csv_parser_empty_data_error(self):
        """Test CSV parser EmptyDataError handling."""
        with patch('text_extractor.async_parsers.async_csv_parser.detect_file_encoding') as mock_detect:
            mock_detect.return_value = "utf-8"
            with patch('pandas.read_csv') as mock_read:
                mock_read.side_effect = EmptyDataError("No data")
                result = await parse_csv("test.csv")
                assert result.text == ""
                assert result.file_type == "csv"


class TestAsyncDOCXParserEdgeCases:
    """Test edge cases for async DOCX parser."""

    @pytest.mark.asyncio
    async def test_docx_parser_package_not_found_error(self):
        """Test DOCX parser PackageNotFoundError handling."""
        with patch('docx.Document') as mock_document:
            mock_document.side_effect = PackageNotFoundError("File not found")
            with pytest.raises(FileNotFoundError, match="DOCX file not found: test.docx"):
                await parse_docx("test.docx")

    @pytest.mark.asyncio
    async def test_docx_parser_table_extraction(self):
        """Test DOCX parser table extraction to cover missing lines."""
        with patch('docx.Document') as mock_document:
            # Mock document with tables
            mock_doc = MagicMock()
            mock_table = MagicMock()
            mock_row = MagicMock()
            mock_cell1 = MagicMock()
            mock_cell1.text = "Cell 1"
            mock_cell2 = MagicMock()
            mock_cell2.text = "Cell 2"
            mock_row.cells = [mock_cell1, mock_cell2]
            mock_table.rows = [mock_row]
            mock_doc.tables = [mock_table]
            mock_doc.paragraphs = []
            mock_document.return_value = mock_doc

            result = await parse_docx("test.docx")
            assert "Cell 1 | Cell 2" in result.text


class TestAsyncPDFParserEdgeCases:
    """Test edge cases for async PDF parser."""

    @pytest.mark.asyncio
    async def test_pdf_parser_ocr_conversion_failure(self):
        """Test PDF parser OCR conversion failure."""
        with patch('pdfminer.high_level.extract_pages') as mock_extract:
            # Mock empty text extraction
            mock_page = MagicMock()
            mock_page.get_text.return_value = ""
            mock_extract.return_value = [mock_page]

            with patch('pdf2image.convert_from_path') as mock_convert:
                mock_convert.side_effect = Exception("Conversion failed")

                result = await parse_pdf("test.pdf")
                assert result.text == ""
                assert result.file_type == "pdf"
                assert not result.ocr_used

    @pytest.mark.asyncio
    async def test_pdf_parser_ocr_failure(self):
        """Test PDF parser OCR failure."""
        with patch('pdfminer.high_level.extract_pages') as mock_extract:
            # Mock empty text extraction
            mock_page = MagicMock()
            mock_page.get_text.return_value = ""
            mock_extract.return_value = [mock_page]

            with patch('pdf2image.convert_from_path') as mock_convert:
                mock_image = MagicMock()
                mock_convert.return_value = [mock_image]

                with patch('pytesseract.image_to_string') as mock_ocr:
                    mock_ocr.side_effect = Exception("OCR failed")

                    with pytest.raises(RuntimeError, match="Failed to OCR PDF page 1 from test.pdf"):
                        await parse_pdf("test.pdf")

    @pytest.mark.asyncio
    async def test_pdf_parser_ocr_success(self):
        """Test PDF parser OCR success to cover missing lines."""
        with patch('pdfminer.high_level.extract_pages') as mock_extract:
            # Mock empty text extraction
            mock_page = MagicMock()
            mock_page.get_text.return_value = ""
            mock_extract.return_value = [mock_page]

            with patch('pdf2image.convert_from_path') as mock_convert:
                mock_image = MagicMock()
                mock_convert.return_value = [mock_image]

                with patch('pytesseract.image_to_string') as mock_ocr:
                    mock_ocr.return_value = "OCR extracted text"

                    result = await parse_pdf("test.pdf")
                    assert result.text == "OCR extracted text"
                    assert result.file_type == "pdf"
                    assert result.ocr_used
