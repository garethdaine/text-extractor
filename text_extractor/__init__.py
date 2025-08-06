"""Core package for the text extraction tool."""

from .models import ExtractedText, PageText
from .utils import resolve_file_type

__all__ = ["ExtractedText", "PageText", "resolve_file_type"]
