"""Sample RTF parser plugin for the text extraction tool.

This plugin demonstrates how to create a custom parser for RTF files.
"""

from text_extractor.models import ExtractedText, PageText


def parse_rtf(file_path: str) -> ExtractedText:
    """Parse an RTF file and return extracted text.

    This is a simple implementation that strips RTF markup.
    In a real implementation, you would use a proper RTF parser.

    Parameters
    ----------
    file_path : str
        Path to the RTF file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the RTF file.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Simple RTF markup removal (this is a basic implementation)
    # In practice, you'd use a proper RTF parser like striprtf
    import re

    # Remove RTF control words and braces
    text = re.sub(r'\\[a-z]+\d*', '', content)
    text = re.sub(r'[{}]', '', text)
    text = re.sub(r'\\\'[0-9a-f]{2}', '', text)  # Remove hex codes

    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    pages = [PageText(page_number=1, text=text, ocr=False)]
    return ExtractedText(text=text, file_type="rtf", pages=pages)


async def parse_rtf_async(file_path: str) -> ExtractedText:
    """Parse an RTF file and return extracted text asynchronously.

    Parameters
    ----------
    file_path : str
        Path to the RTF file.

    Returns
    -------
    ExtractedText
        Structured text extracted from the RTF file.
    """
    import asyncio

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, parse_rtf, file_path)
    return result


def register_parsers(registry):
    """Register the RTF parser with the plugin registry.

    Parameters
    ----------
    registry : PluginRegistry
        The plugin registry to register parsers with.
    """
    registry.register_sync_parser(
        file_type="rtf",
        parser=parse_rtf,
        extensions=[".rtf"],
        mime_types=["application/rtf", "text/rtf"]
    )

    registry.register_async_parser(
        file_type="rtf",
        parser=parse_rtf_async,
        extensions=[".rtf"],
        mime_types=["application/rtf", "text/rtf"]
    )
