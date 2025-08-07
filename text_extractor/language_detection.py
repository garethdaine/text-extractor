"""Language detection module for extracted text."""

from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class LanguageInfo:
    """Information about detected language."""

    language: str
    confidence: float
    is_reliable: bool


def detect_language(text: str, min_confidence: float = 0.8) -> Optional[LanguageInfo]:
    """Detect the language of the given text.

    Parameters
    ----------
    text : str
        The text to analyze for language detection.
    min_confidence : float, optional
        Minimum confidence threshold for reliable detection (default: 0.8).

    Returns
    -------
    Optional[LanguageInfo]
        Language information if detection is successful, None otherwise.

    Examples
    --------
    >>> from text_extractor.language_detection import detect_language
    >>> result = detect_language("Hello, world!")
    >>> print(f"Language: {result.language}, Confidence: {result.confidence}")
    """
    try:
        from langdetect import detect, detect_langs, DetectorFactory
        from langdetect.lang_detect_exception import LangDetectException

        # Set seed for reproducible results
        DetectorFactory.seed = 0

        if not text or not text.strip():
            return None

        # Get the primary language
        primary_lang = detect(text)

        # Get all detected languages with probabilities
        lang_probabilities = detect_langs(text)

        # Find the primary language's confidence
        primary_confidence = 0.0
        for lang_prob in lang_probabilities:
            if lang_prob.lang == primary_lang:
                primary_confidence = lang_prob.prob
                break

        is_reliable = primary_confidence >= min_confidence

        return LanguageInfo(
            language=primary_lang,
            confidence=primary_confidence,
            is_reliable=is_reliable
        )

    except (ImportError, LangDetectException):
        # langdetect not available or detection failed
        return None


def detect_language_simple(text: str) -> Optional[str]:
    """Simple language detection that returns just the language code.

    Parameters
    ----------
    text : str
        The text to analyze.

    Returns
    -------
    Optional[str]
        Language code (e.g., 'en', 'es', 'fr') or None if detection fails.
    """
    result = detect_language(text)
    return result.language if result else None


def is_english(text: str) -> bool:
    """Check if the text is in English.

    Parameters
    ----------
    text : str
        The text to check.

    Returns
    -------
    bool
        True if the text is detected as English, False otherwise.
    """
    result = detect_language(text)
    return result is not None and result.language == 'en' and result.is_reliable


def get_supported_languages() -> list[str]:
    """Get a list of supported language codes.

    Returns
    -------
    list[str]
        List of supported language codes.
    """
    return [
        'af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et',
        'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko',
        'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru',
        'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur',
        'vi', 'zh-cn', 'zh-tw'
    ]
