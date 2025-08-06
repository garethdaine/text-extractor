"""Data models for text extraction results."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PageText:
    """Text content for a single page."""

    page_number: int
    text: str
    ocr: bool = False


@dataclass
class ExtractedText:
    """Structured text extracted from a document."""

    text: str
    file_type: str
    ocr_used: bool = False
    pages: List[PageText] = field(default_factory=list)
