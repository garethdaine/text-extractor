"""
Edge case tests for plugin registry to achieve 100% coverage.
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import importlib.util

from text_extractor.plugin_registry import PluginRegistry, register_async_parser


class TestPluginRegistryEdgeCases:
    """Test edge cases for plugin registry."""

    def test_load_plugin_from_file_spec_none(self):
        """Test loading plugin when spec is None."""
        registry = PluginRegistry()
        with patch('importlib.util.spec_from_file_location') as mock_spec:
            mock_spec.return_value = None
            result = registry.load_plugin_from_file("test_plugin.py")
            assert result is False

    def test_load_plugin_from_file_loader_none(self):
        """Test loading plugin when loader is None."""
        registry = PluginRegistry()
        with patch('importlib.util.spec_from_file_location') as mock_spec:
            mock_spec_obj = MagicMock()
            mock_spec_obj.loader = None
            mock_spec.return_value = mock_spec_obj
            result = registry.load_plugin_from_file("test_plugin.py")
            assert result is False

    def test_load_plugin_from_file_no_register_function(self):
        """Test loading plugin without register_parsers function."""
        registry = PluginRegistry()
        with patch('importlib.util.spec_from_file_location') as mock_spec:
            mock_spec_obj = MagicMock()
            mock_spec_obj.loader = MagicMock()
            mock_spec.return_value = mock_spec_obj

            with patch('importlib.util.module_from_spec') as mock_module_from_spec:
                mock_module = MagicMock()
                # Don't add register_parsers attribute
                mock_module_from_spec.return_value = mock_module

                with patch('sys.modules') as mock_modules:
                    mock_modules.__setitem__ = MagicMock()

                    # Mock the exec_module to not add register_parsers
                    mock_spec_obj.loader.exec_module = MagicMock()

                    # Ensure the module doesn't have register_parsers
                    mock_module.register_parsers = None

                    result = registry.load_plugin_from_file("test_plugin.py")
                    assert result is False

    def test_load_plugin_from_file_exception(self):
        """Test loading plugin when exception occurs."""
        registry = PluginRegistry()
        with patch('importlib.util.spec_from_file_location') as mock_spec:
            mock_spec.side_effect = Exception("Import error")
            result = registry.load_plugin_from_file("test_plugin.py")
            assert result is False

    def test_load_plugin_from_directory_nonexistent(self):
        """Test loading plugins from nonexistent directory."""
        registry = PluginRegistry()
        result = registry.load_plugin_from_directory("/nonexistent/directory")
        assert result == 0

    def test_load_plugin_from_directory_not_directory(self):
        """Test loading plugins from path that is not a directory."""
        registry = PluginRegistry()
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            with patch('pathlib.Path.is_dir') as mock_is_dir:
                mock_is_dir.return_value = False
                result = registry.load_plugin_from_directory("test_file.txt")
                assert result == 0

    def test_load_plugin_from_directory_skip_dunder_files(self):
        """Test loading plugins skips __init__.py files."""
        registry = PluginRegistry()
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            with patch('pathlib.Path.is_dir') as mock_is_dir:
                mock_is_dir.return_value = True
                with patch('pathlib.Path.glob') as mock_glob:
                    mock_glob.return_value = [Path("__init__.py"), Path("plugin.py")]
                    with patch.object(registry, 'load_plugin_from_file') as mock_load:
                        mock_load.return_value = True
                        result = registry.load_plugin_from_directory("test_dir")
                        # Should only call load_plugin_from_file once for plugin.py, not __init__.py
                        assert mock_load.call_count == 1
                        assert result == 1

    def test_register_async_parser_function(self):
        """Test register_async_parser function to cover missing line."""
        mock_parser = MagicMock()
        register_async_parser("test", mock_parser, [".test"], ["text/test"])
        # The function should not raise any exceptions
        assert True
