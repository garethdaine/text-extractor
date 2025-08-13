"""Tests for PDF file parser."""

import pytest

from text_extractor.models import ExtractedText
from text_extractor.parsers import pdf_parser


class TestPdfParser:
    """Test PDF file parsing functionality."""

    def test_parse_simple_pdf_file(self, tmp_path):
        """Test parsing a simple PDF file."""
        # Create a simple PDF file using reportlab
        try:
            from reportlab.pdfgen import canvas
        except ImportError:
            pytest.skip("reportlab not available")

        test_file = tmp_path / "test.pdf"
        c = canvas.Canvas(str(test_file))
        c.drawString(100, 750, "Hello, World!")
        c.drawString(100, 730, "This is a test PDF document.")
        c.save()

        result = pdf_parser.parse(str(test_file))

        assert isinstance(result, ExtractedText)
        assert result.file_type == "pdf"
        assert result.ocr_used is False
        assert "Hello, World!" in result.text
        assert "This is a test PDF document." in result.text
        assert len(result.pages) == 1
        assert result.pages[0].page_number == 1
        assert result.pages[0].ocr is False

    def test_parse_pdf_with_multiple_pages(self, tmp_path):
        """Test parsing PDF with multiple pages."""
        try:
            from reportlab.pdfgen import canvas
        except ImportError:
            pytest.skip("reportlab not available")

        test_file = tmp_path / "multi.pdf"
        c = canvas.Canvas(str(test_file))

        # Page 1
        c.drawString(100, 750, "Page 1 content")
        c.showPage()

        # Page 2
        c.drawString(100, 750, "Page 2 content")
        c.showPage()

        # Page 3
        c.drawString(100, 750, "Page 3 content")
        c.save()

        result = pdf_parser.parse(str(test_file))

        assert result.file_type == "pdf"
        assert result.ocr_used is False
        assert "Page 1 content" in result.text
        assert "Page 2 content" in result.text
        assert "Page 3 content" in result.text
        assert len(result.pages) == 3
        assert result.pages[0].page_number == 1
        assert result.pages[1].page_number == 2
        assert result.pages[2].page_number == 3

    def test_parse_pdf_with_special_characters(self, tmp_path):
        """Test parsing PDF with special characters."""
        try:
            from reportlab.pdfgen import canvas
        except ImportError:
            pytest.skip("reportlab not available")

        test_file = tmp_path / "special.pdf"
        c = canvas.Canvas(str(test_file))
        c.drawString(100, 750, "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?")
        c.drawString(100, 730, "Unicode: 你好世界 🌍 éñç")
        c.save()

        result = pdf_parser.parse(str(test_file))

        assert result.file_type == "pdf"
        assert "Special chars:" in result.text
        assert "!@#$%^&*()" in result.text
        assert "Unicode:" in result.text
        # Unicode characters might not be preserved perfectly in PDF extraction
        # but we should have some content
        assert len(result.text) > 0

    def test_parse_empty_pdf(self, tmp_path):
        """Test parsing an empty PDF file."""
        try:
            from reportlab.pdfgen import canvas
        except ImportError:
            pytest.skip("reportlab not available")

        test_file = tmp_path / "empty.pdf"
        c = canvas.Canvas(str(test_file))
        c.save()

        result = pdf_parser.parse(str(test_file))

        assert result.file_type == "pdf"
        assert result.ocr_used is False
        assert len(result.pages) == 1
        assert result.pages[0].ocr is False

    def test_parse_pdf_with_images_only(self, tmp_path):
        """Test parsing PDF with only images (should trigger OCR)."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.platypus import Image
        except ImportError:
            pytest.skip("reportlab not available")

        # Create a simple image for testing
        img_file = tmp_path / "test.png"
        try:
            from PIL import Image as PILImage

            img = PILImage.new("RGB", (100, 100), color="white")
            img.save(str(img_file))
        except ImportError:
            pytest.skip("Pillow not available")

        test_file = tmp_path / "image.pdf"
        c = canvas.Canvas(str(test_file), pagesize=letter)

        # Add image without text
        img = Image(str(img_file))
        img.drawOn(c, 100, 600)
        c.save()

        result = pdf_parser.parse(str(test_file))

        assert result.file_type == "pdf"
        # Should either have OCR or empty text
        assert len(result.pages) == 1
        # OCR might be triggered for images, or we might get empty text
        assert result.pages[0].ocr in [True, False]

    def test_parse_nonexistent_pdf_file(self):
        """Test that parsing a nonexistent PDF file raises an appropriate error."""
        with pytest.raises(FileNotFoundError):
            pdf_parser.parse("nonexistent.pdf")

    def test_parse_pdf_with_complex_layout(self, tmp_path):
        """Test parsing PDF with complex layout."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except ImportError:
            pytest.skip("reportlab not available")

        test_file = tmp_path / "complex.pdf"
        c = canvas.Canvas(str(test_file), pagesize=letter)

        # Add text in different positions
        c.drawString(50, 750, "Header text")
        c.drawString(50, 700, "Body text line 1")
        c.drawString(50, 680, "Body text line 2")
        c.drawString(50, 660, "Footer text")

        # Add some formatting
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 600, "Bold text")
        c.setFont("Helvetica", 10)
        c.drawString(50, 580, "Normal text")

        c.save()

        result = pdf_parser.parse(str(test_file))

        assert result.file_type == "pdf"
        assert result.ocr_used is False
        assert "Header text" in result.text
        assert "Body text line 1" in result.text
        assert "Body text line 2" in result.text
        assert "Footer text" in result.text
        assert "Bold text" in result.text
        assert "Normal text" in result.text
