"""Plugin registry for custom parsers."""

import importlib.util
import sys
from pathlib import Path
from typing import Dict, Optional, Protocol

from .models import ExtractedText


class Parser(Protocol):
    """Callable parser interface."""

    def __call__(self, file_path: str) -> ExtractedText:  # pragma: no cover - protocol
        ...


class AsyncParser(Protocol):
    """Async callable parser interface."""

    async def __call__(
        self, file_path: str
    ) -> ExtractedText:  # pragma: no cover - protocol
        ...


class PluginRegistry:
    """Registry for custom parser plugins."""

    def __init__(self):
        self._sync_parsers: Dict[str, Parser] = {}
        self._async_parsers: Dict[str, AsyncParser] = {}
        self._file_extensions: Dict[str, str] = {}
        self._mime_types: Dict[str, str] = {}

    def register_sync_parser(
        self,
        file_type: str,
        parser: Parser,
        extensions: Optional[list[str]] = None,
        mime_types: Optional[list[str]] = None,
    ) -> None:
        """Register a synchronous parser.

        Parameters
        ----------
        file_type : str
            The file type identifier (e.g., 'rtf', 'odt').
        parser : Parser
            The parser function to register.
        extensions : list[str], optional
            File extensions this parser handles (e.g., ['.rtf', '.odt']).
        mime_types : list[str], optional
            MIME types this parser handles.
        """
        self._sync_parsers[file_type] = parser

        if extensions:
            for ext in extensions:
                self._file_extensions[ext.lower()] = file_type

        if mime_types:
            for mime_type in mime_types:
                self._mime_types[mime_type] = file_type

    def register_async_parser(
        self,
        file_type: str,
        parser: AsyncParser,
        extensions: Optional[list[str]] = None,
        mime_types: Optional[list[str]] = None,
    ) -> None:
        """Register an asynchronous parser.

        Parameters
        ----------
        file_type : str
            The file type identifier (e.g., 'rtf', 'odt').
        parser : AsyncParser
            The async parser function to register.
        extensions : list[str], optional
            File extensions this parser handles (e.g., ['.rtf', '.odt']).
        mime_types : list[str], optional
            MIME types this parser handles.
        """
        self._async_parsers[file_type] = parser

        if extensions:
            for ext in extensions:
                self._file_extensions[ext.lower()] = file_type

        if mime_types:
            for mime_type in mime_types:
                self._mime_types[mime_type] = file_type

    def get_sync_parser(self, file_type: str) -> Optional[Parser]:
        """Get a registered synchronous parser.

        Parameters
        ----------
        file_type : str
            The file type identifier.

        Returns
        -------
        Optional[Parser]
            The registered parser or None if not found.
        """
        return self._sync_parsers.get(file_type)

    def get_async_parser(self, file_type: str) -> Optional[AsyncParser]:
        """Get a registered asynchronous parser.

        Parameters
        ----------
        file_type : str
            The file type identifier.

        Returns
        -------
        Optional[AsyncParser]
            The registered async parser or None if not found.
        """
        return self._async_parsers.get(file_type)

    def get_file_type_from_extension(self, extension: str) -> Optional[str]:
        """Get file type from file extension.

        Parameters
        ----------
        extension : str
            File extension (e.g., '.rtf').

        Returns
        -------
        Optional[str]
            File type identifier or None if not found.
        """
        return self._file_extensions.get(extension.lower())

    def get_file_type_from_mime_type(self, mime_type: str) -> Optional[str]:
        """Get file type from MIME type.

        Parameters
        ----------
        mime_type : str
            MIME type (e.g., 'application/rtf').

        Returns
        -------
        Optional[str]
            File type identifier or None if not found.
        """
        return self._mime_types.get(mime_type)

    def list_registered_parsers(self) -> Dict[str, list[str]]:
        """List all registered parsers.

        Returns
        -------
        Dict[str, list[str]]
            Dictionary mapping parser types to lists of supported file types.
        """
        result = {}

        # Group by file type
        for file_type in set(self._sync_parsers.keys()) | set(
            self._async_parsers.keys()
        ):
            supported = []

            # Find extensions for this file type
            for ext, ft in self._file_extensions.items():
                if ft == file_type:
                    supported.append(ext)

            # Find MIME types for this file type
            for mime, ft in self._mime_types.items():
                if ft == file_type:
                    supported.append(mime)

            result[file_type] = supported

        return result

    def load_plugin_from_file(self, plugin_path: str) -> bool:
        """Load a plugin from a Python file.

        Parameters
        ----------
        plugin_path : str
            Path to the plugin Python file.

        Returns
        -------
        bool
            True if plugin loaded successfully, False otherwise.
        """
        try:
            # Load the plugin module
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            if spec is None or spec.loader is None:
                return False

            module = importlib.util.module_from_spec(spec)
            sys.modules["plugin"] = module
            spec.loader.exec_module(module)

            # Look for registration function
            if hasattr(module, "register_parsers"):
                module.register_parsers(self)
                return True

            return False

        except Exception:
            return False

    def load_plugin_from_directory(self, plugin_dir: str) -> int:
        """Load all plugins from a directory.

        Parameters
        ----------
        plugin_dir : str
            Path to the plugin directory.

        Returns
        -------
        int
            Number of plugins successfully loaded.
        """
        plugin_path = Path(plugin_dir)
        if not plugin_path.exists() or not plugin_path.is_dir():
            return 0

        loaded_count = 0
        for file_path in plugin_path.glob("*.py"):
            if file_path.name.startswith("__"):
                continue
            if self.load_plugin_from_file(str(file_path)):
                loaded_count += 1

        return loaded_count


# Global plugin registry instance
_plugin_registry = PluginRegistry()


def get_plugin_registry() -> PluginRegistry:
    """Get the global plugin registry instance.

    Returns
    -------
    PluginRegistry
        The global plugin registry.
    """
    return _plugin_registry


def register_sync_parser(
    file_type: str,
    parser: Parser,
    extensions: Optional[list[str]] = None,
    mime_types: Optional[list[str]] = None,
) -> None:
    """Register a synchronous parser globally.

    Parameters
    ----------
    file_type : str
        The file type identifier.
    parser : Parser
        The parser function to register.
    extensions : list[str], optional
        File extensions this parser handles.
    mime_types : list[str], optional
        MIME types this parser handles.
    """
    _plugin_registry.register_sync_parser(file_type, parser, extensions, mime_types)


def register_async_parser(
    file_type: str,
    parser: AsyncParser,
    extensions: Optional[list[str]] = None,
    mime_types: Optional[list[str]] = None,
) -> None:
    """Register an asynchronous parser globally.

    Parameters
    ----------
    file_type : str
        The file type identifier.
    parser : AsyncParser
        The async parser function to register.
    extensions : list[str], optional
        File extensions this parser handles.
    mime_types : list[str], optional
        MIME types this parser handles.
    """
    _plugin_registry.register_async_parser(file_type, parser, extensions, mime_types)
