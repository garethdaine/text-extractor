"""Tests for language detection functionality."""

import pytest

from text_extractor.language_detection import (
    detect_language,
    detect_language_simple,
    is_english,
    get_supported_languages,
    LanguageInfo,
)


class TestLanguageDetection:
    """Test language detection functionality."""

    def test_detect_language_english(self):
        """Test detecting English text."""
        result = detect_language("Hello, world! This is a test.")

        assert result is not None
        assert result.language == "en"
        assert result.confidence > 0.5
        assert result.is_reliable is True

    def test_detect_language_spanish(self):
        """Test detecting Spanish text."""
        result = detect_language("Hola, mundo! Esto es una prueba.")

        assert result is not None
        assert result.language == "es"
        assert result.confidence > 0.5

    def test_detect_language_french(self):
        """Test detecting French text."""
        result = detect_language("Bonjour, monde! Ceci est un test.")

        assert result is not None
        assert result.language == "fr"
        assert result.confidence > 0.5

    def test_detect_language_empty_text(self):
        """Test detecting language in empty text."""
        result = detect_language("")
        assert result is None

        result = detect_language("   ")
        assert result is None

    def test_detect_language_simple(self):
        """Test simple language detection."""
        result = detect_language_simple("Hello, world!")
        assert result == "en"

        result = detect_language_simple("Hola, mundo!")
        # langdetect might detect Spanish or Portuguese for this text
        assert result in ["es", "pt"]

    def test_is_english(self):
        """Test English detection."""
        assert is_english("Hello, world! This is English text.")
        assert not is_english("Hola, mundo! Esto es español.")
        assert not is_english("")  # Empty text should not be English

    def test_get_supported_languages(self):
        """Test getting supported languages."""
        languages = get_supported_languages()

        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "en" in languages
        assert "es" in languages
        assert "fr" in languages
        assert "de" in languages

    def test_language_info_structure(self):
        """Test LanguageInfo dataclass structure."""
        result = detect_language("Hello, world!")

        assert isinstance(result, LanguageInfo)
        assert hasattr(result, 'language')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'is_reliable')
        assert isinstance(result.language, str)
        assert isinstance(result.confidence, float)
        assert isinstance(result.is_reliable, bool)

    def test_language_detection_with_confidence_threshold(self):
        """Test language detection with custom confidence threshold."""
        # Test with high confidence threshold
        result = detect_language("Hello, world!", min_confidence=0.9)
        if result:
            assert result.confidence >= 0.9

        # Test with low confidence threshold
        result = detect_language("Hello, world!", min_confidence=0.1)
        if result:
            assert result.confidence >= 0.1
