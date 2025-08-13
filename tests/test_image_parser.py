"""Tests for image file parser."""

import pytest

from text_extractor.models import ExtractedText
from text_extractor.parsers import image_parser


class TestImageParser:
    """Test image file parsing functionality."""

    def test_parse_simple_image_file(self, tmp_path):
        """Test parsing a simple image file."""
        # Create a simple image with text using Pillow
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            pytest.skip("Pillow not available")

        # Create a white image
        img = Image.new("RGB", (400, 200), color="white")
        draw = ImageDraw.Draw(img)

        # Try to add text (OCR might not work without proper font)
        try:
            # Use default font
            draw.text((50, 50), "Hello, World!", fill="black")
            draw.text((50, 80), "This is test text in an image.", fill="black")
        except Exception:
            # If font fails, just create a simple image
            pass

        test_file = tmp_path / "test.png"
        img.save(str(test_file))

        result = image_parser.parse(str(test_file))

        assert isinstance(result, ExtractedText)
        assert result.file_type == "png"
        assert result.ocr_used is True
        assert len(result.pages) == 1
        assert result.pages[0].page_number == 1
        assert result.pages[0].ocr is True

    def test_parse_jpg_image_file(self, tmp_path):
        """Test parsing a JPG image file."""
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            pytest.skip("Pillow not available")

        # Create a simple image
        img = Image.new("RGB", (300, 150), color="white")
        draw = ImageDraw.Draw(img)

        try:
            draw.text((30, 30), "Test JPG image", fill="black")
        except Exception:
            pass

        test_file = tmp_path / "test.jpg"
        img.save(str(test_file))

        result = image_parser.parse(str(test_file))

        assert result.file_type == "jpg"
        assert result.ocr_used is True
        assert len(result.pages) == 1
        assert result.pages[0].page_number == 1
        assert result.pages[0].ocr is True

    def test_parse_image_without_text(self, tmp_path):
        """Test parsing an image without text."""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not available")

        # Create a simple colored image without text
        img = Image.new("RGB", (200, 100), color="blue")

        test_file = tmp_path / "no_text.png"
        img.save(str(test_file))

        result = image_parser.parse(str(test_file))

        assert result.file_type == "png"
        assert result.ocr_used is True
        assert len(result.pages) == 1
        assert result.pages[0].page_number == 1
        assert result.pages[0].ocr is True
        # OCR might return empty text for images without text
        assert isinstance(result.text, str)

    def test_parse_image_with_complex_content(self, tmp_path):
        """Test parsing an image with complex content."""
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            pytest.skip("Pillow not available")

        # Create a more complex image
        img = Image.new("RGB", (500, 300), color="white")
        draw = ImageDraw.Draw(img)

        # Draw some shapes and try to add text
        draw.rectangle([50, 50, 450, 250], outline="black", width=2)
        draw.line([50, 150, 450, 150], fill="red", width=3)

        try:
            draw.text((100, 100), "Complex Image", fill="black")
            draw.text((100, 130), "With multiple elements", fill="blue")
        except Exception:
            pass

        test_file = tmp_path / "complex.png"
        img.save(str(test_file))

        result = image_parser.parse(str(test_file))

        assert result.file_type == "png"
        assert result.ocr_used is True
        assert len(result.pages) == 1
        assert result.pages[0].page_number == 1
        assert result.pages[0].ocr is True

    def test_parse_nonexistent_image_file(self):
        """Test that parsing a nonexistent image file raises an appropriate error."""
        with pytest.raises(FileNotFoundError):
            image_parser.parse("nonexistent.png")

    def test_parse_image_with_different_formats(self, tmp_path):
        """Test parsing images in different formats."""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not available")

        # Create a simple image
        img = Image.new("RGB", (100, 100), color="white")

        # Test PNG
        png_file = tmp_path / "test.png"
        img.save(str(png_file))
        result_png = image_parser.parse(str(png_file))
        assert result_png.file_type == "png"
        assert result_png.ocr_used is True

        # Test JPG
        jpg_file = tmp_path / "test.jpg"
        img.save(str(jpg_file))
        result_jpg = image_parser.parse(str(jpg_file))
        assert result_jpg.file_type == "jpg"
        assert result_jpg.ocr_used is True

    def test_parse_image_with_ocr_fallback(self, tmp_path):
        """Test that image parsing always uses OCR."""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not available")

        # Create a simple image
        img = Image.new("RGB", (50, 50), color="white")

        test_file = tmp_path / "ocr_test.png"
        img.save(str(test_file))

        result = image_parser.parse(str(test_file))

        # Image parser should always use OCR
        assert result.ocr_used is True
        assert result.pages[0].ocr is True
