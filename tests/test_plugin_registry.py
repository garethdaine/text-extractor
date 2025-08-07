"""Tests for plugin registry functionality."""

import pytest
import tempfile
import os
from pathlib import Path

from text_extractor.plugin_registry import (
    PluginRegistry,
    get_plugin_registry,
    register_sync_parser,
    register_async_parser,
)
from text_extractor.models import ExtractedText, PageText


class TestPluginRegistry:
    """Test plugin registry functionality."""

    def test_register_sync_parser(self):
        """Test registering a synchronous parser."""
        registry = PluginRegistry()

        def test_parser(file_path: str) -> ExtractedText:
            return ExtractedText(
                text="Test content",
                file_type="test",
                pages=[PageText(page_number=1, text="Test content", ocr=False)]
            )

        registry.register_sync_parser(
            file_type="test",
            parser=test_parser,
            extensions=[".test"],
            mime_types=["application/test"]
        )

        # Test that parser is registered
        parser = registry.get_sync_parser("test")
        assert parser is not None

        # Test file extension mapping
        file_type = registry.get_file_type_from_extension(".test")
        assert file_type == "test"

        # Test MIME type mapping
        file_type = registry.get_file_type_from_mime_type("application/test")
        assert file_type == "test"

    def test_register_async_parser(self):
        """Test registering an asynchronous parser."""
        registry = PluginRegistry()

        async def test_async_parser(file_path: str) -> ExtractedText:
            return ExtractedText(
                text="Test content",
                file_type="test",
                pages=[PageText(page_number=1, text="Test content", ocr=False)]
            )

        registry.register_async_parser(
            file_type="test",
            parser=test_async_parser,
            extensions=[".test"],
            mime_types=["application/test"]
        )

        # Test that parser is registered
        parser = registry.get_async_parser("test")
        assert parser is not None

    def test_list_registered_parsers(self):
        """Test listing registered parsers."""
        registry = PluginRegistry()

        def test_parser(file_path: str) -> ExtractedText:
            return ExtractedText(
                text="Test content",
                file_type="test",
                pages=[PageText(page_number=1, text="Test content", ocr=False)]
            )

        registry.register_sync_parser(
            file_type="test",
            parser=test_parser,
            extensions=[".test"],
            mime_types=["application/test"]
        )

        parsers = registry.list_registered_parsers()
        assert "test" in parsers
        assert ".test" in parsers["test"]
        assert "application/test" in parsers["test"]

    def test_global_registry(self):
        """Test global registry functions."""
        def test_parser(file_path: str) -> ExtractedText:
            return ExtractedText(
                text="Test content",
                file_type="test",
                pages=[PageText(page_number=1, text="Test content", ocr=False)]
            )

        # Test global registration
        register_sync_parser(
            file_type="test",
            parser=test_parser,
            extensions=[".test"]
        )

        registry = get_plugin_registry()
        parser = registry.get_sync_parser("test")
        assert parser is not None

    def test_load_plugin_from_file(self):
        """Test loading a plugin from a file."""
        registry = PluginRegistry()

        # Create a temporary plugin file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from text_extractor.models import ExtractedText, PageText

def test_parser(file_path: str) -> ExtractedText:
    return ExtractedText(
        text="Plugin content",
        file_type="plugin",
        pages=[PageText(page_number=1, text="Plugin content", ocr=False)]
    )

def register_parsers(registry):
    registry.register_sync_parser(
        file_type="plugin",
        parser=test_parser,
        extensions=[".plugin"]
    )
''')
            plugin_path = f.name

        try:
            # Test loading the plugin
            success = registry.load_plugin_from_file(plugin_path)
            assert success is True

            # Test that parser is registered
            parser = registry.get_sync_parser("plugin")
            assert parser is not None

            # Test file extension mapping
            file_type = registry.get_file_type_from_extension(".plugin")
            assert file_type == "plugin"

        finally:
            # Clean up
            os.unlink(plugin_path)

    def test_load_plugin_from_directory(self):
        """Test loading plugins from a directory."""
        registry = PluginRegistry()

        # Create a temporary directory with plugins
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create plugin files
            plugin1_path = os.path.join(temp_dir, "plugin1.py")
            with open(plugin1_path, 'w') as f:
                f.write('''
from text_extractor.models import ExtractedText, PageText

def test_parser1(file_path: str) -> ExtractedText:
    return ExtractedText(
        text="Plugin 1 content",
        file_type="plugin1",
        pages=[PageText(page_number=1, text="Plugin 1 content", ocr=False)]
    )

def register_parsers(registry):
    registry.register_sync_parser(
        file_type="plugin1",
        parser=test_parser1,
        extensions=[".plugin1"]
    )
''')

            plugin2_path = os.path.join(temp_dir, "plugin2.py")
            with open(plugin2_path, 'w') as f:
                f.write('''
from text_extractor.models import ExtractedText, PageText

def test_parser2(file_path: str) -> ExtractedText:
    return ExtractedText(
        text="Plugin 2 content",
        file_type="plugin2",
        pages=[PageText(page_number=1, text="Plugin 2 content", ocr=False)]
    )

def register_parsers(registry):
    registry.register_sync_parser(
        file_type="plugin2",
        parser=test_parser2,
        extensions=[".plugin2"]
    )
''')

            # Create an invalid plugin file
            invalid_path = os.path.join(temp_dir, "invalid.py")
            with open(invalid_path, 'w') as f:
                f.write('''
# This plugin doesn't have a register_parsers function
def some_function():
    pass
''')

            # Test loading plugins from directory
            loaded_count = registry.load_plugin_from_directory(temp_dir)
            assert loaded_count == 2  # Should load 2 valid plugins

            # Test that parsers are registered
            parser1 = registry.get_sync_parser("plugin1")
            parser2 = registry.get_sync_parser("plugin2")
            assert parser1 is not None
            assert parser2 is not None

            # Test file extension mappings
            file_type1 = registry.get_file_type_from_extension(".plugin1")
            file_type2 = registry.get_file_type_from_extension(".plugin2")
            assert file_type1 == "plugin1"
            assert file_type2 == "plugin2"
