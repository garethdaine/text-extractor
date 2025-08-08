"""
Tests for language detection edge cases.
"""

import pytest
from unittest.mock import patch

from text_extractor.language_detection import (
    detect_language,
    detect_language_simple,
    is_english,
    get_supported_languages,
    LanguageInfo,
)


class TestLanguageDetectionEdgeCases:
    """Test language detection edge cases and error handling."""

    def test_detect_language_import_error(self):
        """Test language detection when langdetect is not available."""
        with patch('langdetect.detect') as mock_detect:
            mock_detect.side_effect = ImportError("langdetect not available")

            result = detect_language("Test text")
            assert result is None

    def test_detect_language_langdetect_exception(self):
        """Test language detection when langdetect raises an exception."""
        with patch('langdetect.detect') as mock_detect:
            from langdetect.lang_detect_exception import LangDetectException
            mock_detect.side_effect = LangDetectException("Detection failed", "message")

            result = detect_language("Test text")
            assert result is None

    def test_detect_language_empty_text(self):
        """Test language detection with empty text."""
        result = detect_language("")
        assert result is None

    def test_detect_language_whitespace_only(self):
        """Test language detection with whitespace-only text."""
        result = detect_language("   \n\t   ")
        assert result is None

    def test_detect_language_none_text(self):
        """Test language detection with None text."""
        result = detect_language(None)
        assert result is None

    def test_detect_language_simple_import_error(self):
        """Test simple language detection when langdetect is not available."""
        with patch('text_extractor.language_detection.detect_language') as mock_detect:
            mock_detect.return_value = None

            result = detect_language_simple("Test text")
            assert result is None

    def test_detect_language_simple_success(self):
        """Test simple language detection with successful detection."""
        with patch('text_extractor.language_detection.detect_language') as mock_detect:
            mock_result = LanguageInfo(language="en", confidence=0.9, is_reliable=True)
            mock_detect.return_value = mock_result

            result = detect_language_simple("Test text")
            assert result == "en"

    def test_is_english_detection_fails(self):
        """Test is_english when language detection fails."""
        with patch('text_extractor.language_detection.detect_language') as mock_detect:
            mock_detect.return_value = None

            result = is_english("Test text")
            assert result is False

    def test_is_english_not_english(self):
        """Test is_english when text is not English."""
        with patch('text_extractor.language_detection.detect_language') as mock_detect:
            mock_result = LanguageInfo(language="es", confidence=0.9, is_reliable=True)
            mock_detect.return_value = mock_result

            result = is_english("Texto en español")
            assert result is False

    def test_is_english_not_reliable(self):
        """Test is_english when detection is not reliable."""
        with patch('text_extractor.language_detection.detect_language') as mock_detect:
            mock_result = LanguageInfo(language="en", confidence=0.5, is_reliable=False)
            mock_detect.return_value = mock_result

            result = is_english("Test text")
            assert result is False

    def test_is_english_success(self):
        """Test is_english when text is reliably detected as English."""
        with patch('text_extractor.language_detection.detect_language') as mock_detect:
            mock_result = LanguageInfo(language="en", confidence=0.9, is_reliable=True)
            mock_detect.return_value = mock_result

            result = is_english("This is English text")
            assert result is True

    def test_get_supported_languages(self):
        """Test that get_supported_languages returns a comprehensive list."""
        languages = get_supported_languages()

        # Check that it's a list
        assert isinstance(languages, list)

        # Check that it contains common languages
        assert "en" in languages  # English
        assert "es" in languages  # Spanish
        assert "fr" in languages  # French
        assert "de" in languages  # German
        assert "it" in languages  # Italian
        assert "pt" in languages  # Portuguese
        assert "ru" in languages  # Russian
        assert "zh-cn" in languages  # Chinese (Simplified)
        assert "zh-tw" in languages  # Chinese (Traditional)
        assert "ja" in languages  # Japanese
        assert "ko" in languages  # Korean

        # Check that all language codes are strings
        for lang in languages:
            assert isinstance(lang, str)
            assert len(lang) > 0

    def test_language_info_structure(self):
        """Test LanguageInfo dataclass structure."""
        info = LanguageInfo(language="en", confidence=0.95, is_reliable=True)

        assert info.language == "en"
        assert info.confidence == 0.95
        assert info.is_reliable is True

    def test_language_info_repr(self):
        """Test LanguageInfo string representation."""
        info = LanguageInfo(language="es", confidence=0.8, is_reliable=False)
        repr_str = repr(info)

        assert "LanguageInfo" in repr_str
        assert "language='es'" in repr_str
        assert "confidence=0.8" in repr_str
        assert "is_reliable=False" in repr_str
