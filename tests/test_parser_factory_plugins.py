"""
Tests for parser factory plugin functionality.
"""

from unittest.mock import Mock, patch

import pytest

from text_extractor.parser_factory import _PARSERS, select_parser


class TestParserFactoryPlugins:
    """Test parser factory plugin functionality."""

    def test_select_parser_with_plugin_fallback(self):
        """Test selecting parser with plugin fallback."""
        # Mock a plugin parser
        mock_plugin_parser = Mock()

        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry_instance = Mock()
                mock_registry_instance.get_sync_parser.return_value = mock_plugin_parser
                mock_registry.return_value = mock_registry_instance

                # Test with a file type that's not in the main parsers but has a plugin
                parser = select_parser("test.rtf")
                assert parser == mock_plugin_parser

    def test_select_parser_plugin_not_found(self):
        """Test selecting parser when plugin is not found."""
        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "unsupported"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry_instance = Mock()
                mock_registry_instance.get_sync_parser.return_value = None
                mock_registry.return_value = mock_registry_instance

                # Test with a file type that's not supported
                with pytest.raises(
                    ValueError, match="No parser available for file type"
                ):
                    select_parser("test.unsupported")

    def test_select_parser_plugin_registry_error(self):
        """Test selecting parser when plugin registry fails."""
        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry.side_effect = Exception("Plugin registry error")

                # Test with a file type that's not in main parsers
                with pytest.raises(Exception, match="Plugin registry error"):
                    select_parser("test.rtf")

    def test_select_parser_plugin_registry_import_error(self):
        """Test selecting parser when plugin registry import fails."""
        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry.side_effect = ImportError("Plugin registry not available")

                # Test with a file type that's not in main parsers
                with pytest.raises(ImportError, match="Plugin registry not available"):
                    select_parser("test.rtf")

    def test_select_parser_plugin_registry_returns_none(self):
        """Test selecting parser when plugin registry returns None."""
        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry.return_value = None

                # Test with a file type that's not in main parsers
                with pytest.raises(AttributeError):
                    select_parser("test.rtf")

    def test_select_parser_plugin_registry_get_sync_parser_returns_none(self):
        """Test selecting parser when plugin registry get_sync_parser returns None."""
        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry_instance = Mock()
                mock_registry_instance.get_sync_parser.return_value = None
                mock_registry.return_value = mock_registry_instance

                # Test with a file type that's not in main parsers
                with pytest.raises(
                    ValueError, match="No parser available for file type"
                ):
                    select_parser("test.rtf")

    def test_select_parser_plugin_registry_get_sync_parser_returns_parser(self):
        """Test selecting parser when plugin registry get_sync_parser returns a parser."""
        # Mock a plugin parser
        mock_plugin_parser = Mock()

        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry_instance = Mock()
                mock_registry_instance.get_sync_parser.return_value = mock_plugin_parser
                mock_registry.return_value = mock_registry_instance

                # Test with a file type that's not in main parsers but has a plugin
                parser = select_parser("test.rtf")
                assert parser == mock_plugin_parser
                mock_registry_instance.get_sync_parser.assert_called_once_with("rtf")

    def test_select_parser_plugin_registry_get_sync_parser_called_with_correct_type(
        self,
    ):
        """Test that plugin registry get_sync_parser is called with correct file type."""
        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry_instance = Mock()
                mock_registry_instance.get_sync_parser.return_value = None
                mock_registry.return_value = mock_registry_instance

                # Test with different file types
                try:
                    select_parser("test.rtf")
                except ValueError:
                    pass
                mock_registry_instance.get_sync_parser.assert_called_once_with("rtf")

                # Reset mock for second test
                mock_registry_instance.get_sync_parser.reset_mock()
                mock_resolve.return_value = "odt"

                try:
                    select_parser("test.odt")
                except ValueError:
                    pass
                mock_registry_instance.get_sync_parser.assert_called_once_with("odt")

    def test_select_parser_plugin_registry_get_sync_parser_called_only_when_needed(
        self,
    ):
        """Test that plugin registry get_sync_parser is only called for unsupported types."""
        with patch(
            "text_extractor.parser_factory.get_plugin_registry"
        ) as mock_registry:
            mock_registry_instance = Mock()
            mock_registry_instance.get_sync_parser.return_value = None
            mock_registry.return_value = mock_registry_instance

            # Test with a supported file type (should not call plugin registry)
            parser = select_parser("test.txt")
            assert parser == _PARSERS["txt"]
            mock_registry_instance.get_sync_parser.assert_not_called()

    def test_select_parser_plugin_registry_get_sync_parser_called_for_unsupported_type(
        self,
    ):
        """Test that plugin registry get_sync_parser is called for unsupported types."""
        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry_instance = Mock()
                mock_registry_instance.get_sync_parser.return_value = None
                mock_registry.return_value = mock_registry_instance

                # Test with an unsupported file type (should call plugin registry)
                try:
                    select_parser("test.rtf")
                except ValueError:
                    pass
                mock_registry_instance.get_sync_parser.assert_called_once_with("rtf")

    def test_select_parser_plugin_registry_get_sync_parser_returns_callable(self):
        """Test that plugin registry get_sync_parser returns a callable parser."""
        # Mock a plugin parser that is callable
        mock_plugin_parser = Mock()
        mock_plugin_parser.__call__ = Mock()

        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "rtf"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry_instance = Mock()
                mock_registry_instance.get_sync_parser.return_value = mock_plugin_parser
                mock_registry.return_value = mock_registry_instance

                # Test with a file type that's not in main parsers but has a plugin
                parser = select_parser("test.rtf")
                assert parser == mock_plugin_parser
                assert callable(parser)

    def test_select_parser_plugin_registry_get_sync_parser_returns_none_for_unsupported(
        self,
    ):
        """Test that plugin registry get_sync_parser returns None for unsupported types."""
        with patch("text_extractor.parser_factory.resolve_file_type") as mock_resolve:
            mock_resolve.return_value = "unsupported"
            with patch(
                "text_extractor.parser_factory.get_plugin_registry"
            ) as mock_registry:
                mock_registry_instance = Mock()
                mock_registry_instance.get_sync_parser.return_value = None
                mock_registry.return_value = mock_registry_instance

                # Test with an unsupported file type
                with pytest.raises(
                    ValueError, match="No parser available for file type"
                ):
                    select_parser("test.unsupported")
