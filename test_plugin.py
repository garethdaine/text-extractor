#!/usr/bin/env python3
"""Test script for plugin functionality."""

from text_extractor import get_plugin_registry, register_sync_parser
from text_extractor.models import ExtractedText, PageText


def test_parser(file_path):
    """Test parser function."""
    return ExtractedText(
        text='Plugin content',
        file_type='test',
        pages=[PageText(page_number=1, text='Plugin content', ocr=False)]
    )


def main():
    """Test plugin registration."""
    # Register a test parser
    register_sync_parser('test', test_parser, ['.test'])

    # Get the registry and list parsers
    registry = get_plugin_registry()
    print('Registered parsers:', registry.list_registered_parsers())

    # Test that the parser is registered
    parser = registry.get_sync_parser('test')
    if parser:
        print('✓ Test parser registered successfully')
    else:
        print('✗ Test parser registration failed')


if __name__ == '__main__':
    main()
