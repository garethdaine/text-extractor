"""
Unit tests for text-extractor models.
"""

import pytest
from text_extractor.models import PageText, ExtractedText


class TestPageText:
    """Test PageText model."""

    def test_valid_page_text(self):
        """Test creating valid PageText."""
        page = PageText(
            page_number=1,
            text="Test content",
            ocr=False
        )
        assert page.page_number == 1
        assert page.text == "Test content"
        assert page.ocr is False

    def test_page_text_default_ocr(self):
        """Test PageText with default OCR value."""
        page = PageText(page_number=1, text="Test content")
        assert page.ocr is False

    def test_page_text_with_ocr(self):
        """Test PageText with OCR enabled."""
        page = PageText(
            page_number=2,
            text="OCR extracted content",
            ocr=True
        )
        assert page.page_number == 2
        assert page.text == "OCR extracted content"
        assert page.ocr is True


class TestExtractedText:
    """Test ExtractedText model."""

    def test_valid_extracted_text(self):
        """Test creating valid ExtractedText."""
        extracted = ExtractedText(
            text="Test content",
            file_type="pdf",
            ocr_used=False,
            pages=[]
        )
        assert extracted.text == "Test content"
        assert extracted.file_type == "pdf"
        assert extracted.ocr_used is False
        assert extracted.pages == []

    def test_extracted_text_default_values(self):
        """Test ExtractedText with default values."""
        extracted = ExtractedText(text="Test content", file_type="txt")
        assert extracted.text == "Test content"
        assert extracted.file_type == "txt"
        assert extracted.ocr_used is False
        assert extracted.pages == []

    def test_extracted_text_with_pages(self):
        """Test ExtractedText with pages."""
        pages = [
            PageText(page_number=1, text="Page 1 content"),
            PageText(page_number=2, text="Page 2 content", ocr=True)
        ]
        extracted = ExtractedText(
            text="Combined content",
            file_type="pdf",
            ocr_used=True,
            pages=pages
        )
        assert extracted.text == "Combined content"
        assert extracted.file_type == "pdf"
        assert extracted.ocr_used is True
        assert len(extracted.pages) == 2
        assert extracted.pages[0].page_number == 1
        assert extracted.pages[0].text == "Page 1 content"
        assert extracted.pages[0].ocr is False
        assert extracted.pages[1].page_number == 2
        assert extracted.pages[1].text == "Page 2 content"
        assert extracted.pages[1].ocr is True

    def test_extracted_text_empty_pages(self):
        """Test ExtractedText with empty pages list."""
        extracted = ExtractedText(
            text="Test content",
            file_type="txt",
            pages=[]
        )
        assert extracted.pages == []

    def test_extracted_text_with_ocr(self):
        """Test ExtractedText with OCR used."""
        extracted = ExtractedText(
            text="OCR extracted content",
            file_type="pdf",
            ocr_used=True
        )
        assert extracted.text == "OCR extracted content"
        assert extracted.file_type == "pdf"
        assert extracted.ocr_used is True
