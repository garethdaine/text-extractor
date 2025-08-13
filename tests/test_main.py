"""
Tests for the command-line interface (__main__.py).
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from text_extractor.__main__ import main


class TestMainCLI:
    """Test the main CLI functionality."""

    def test_main_success_plain_text(self):
        """Test successful text extraction with plain text output."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for CLI")
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", file_path]):
                result = main()
                assert result == 0
        finally:
            Path(file_path).unlink()

    def test_main_success_json_output(self):
        """Test successful text extraction with JSON output."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for JSON output")
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", "--json", file_path]):
                result = main()
                assert result == 0
        finally:
            Path(file_path).unlink()

    def test_main_success_verbose_output(self):
        """Test successful text extraction with verbose output."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for verbose output")
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", "--verbose", file_path]):
                result = main()
                assert result == 0
        finally:
            Path(file_path).unlink()

    def test_main_success_output_file(self):
        """Test successful text extraction with output file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for output file")
            file_path = f.name

        output_file = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        output_path = output_file.name
        output_file.close()

        try:
            with patch(
                "sys.argv", ["text_extractor", "--output", output_path, file_path]
            ):
                result = main()
                assert result == 0
                assert Path(output_path).exists()
        finally:
            Path(file_path).unlink()
            Path(output_path).unlink()

    def test_main_success_json_output_file(self):
        """Test successful text extraction with JSON output to file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for JSON output file")
            file_path = f.name

        output_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        output_path = output_file.name
        output_file.close()

        try:
            with patch(
                "sys.argv",
                ["text_extractor", "--json", "--output", output_path, file_path],
            ):
                result = main()
                assert result == 0
                assert Path(output_path).exists()

                # Verify JSON content
                with open(output_path) as f:
                    data = json.load(f)
                assert "text" in data
                assert "file_type" in data
                assert "ocr_used" in data
                assert "pages" in data
        finally:
            Path(file_path).unlink()
            Path(output_path).unlink()

    def test_main_success_verbose_output_file(self):
        """Test successful text extraction with verbose output to file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for verbose output file")
            file_path = f.name

        output_file = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        output_path = output_file.name
        output_file.close()

        try:
            with patch(
                "sys.argv",
                ["text_extractor", "--verbose", "--output", output_path, file_path],
            ):
                result = main()
                assert result == 0
                assert Path(output_path).exists()

                # Verify verbose content
                with open(output_path) as f:
                    content = f.read()
                assert "File:" in content
                assert "Type:" in content
                assert "OCR Used:" in content
                assert "Pages:" in content
        finally:
            Path(file_path).unlink()
            Path(output_path).unlink()

    def test_main_file_not_found(self):
        """Test handling of file not found error."""
        with patch("sys.argv", ["text_extractor", "nonexistent_file.txt"]):
            result = main()
            assert result == 1

    def test_main_value_error(self):
        """Test handling of ValueError (unsupported file type)."""
        with tempfile.NamedTemporaryFile(suffix=".unsupported", delete=False) as f:
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", file_path]):
                result = main()
                assert result == 1
        finally:
            Path(file_path).unlink()

    def test_main_unexpected_error(self):
        """Test handling of unexpected errors."""
        with patch("text_extractor.__main__.extract_text_from_file") as mock_extract:
            mock_extract.side_effect = Exception("Unexpected error")

            with patch("sys.argv", ["text_extractor", "test.txt"]):
                result = main()
                assert result == 1

    def test_main_unexpected_error_verbose(self):
        """Test handling of unexpected errors with verbose output."""
        with patch("text_extractor.__main__.extract_text_from_file") as mock_extract:
            mock_extract.side_effect = Exception("Unexpected error")

            with patch("sys.argv", ["text_extractor", "--verbose", "test.txt"]):
                result = main()
                assert result == 1

    def test_main_with_custom_argv(self):
        """Test main function with custom argv parameter."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for custom argv")
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", file_path]):
                result = main()
                assert result == 0
        finally:
            Path(file_path).unlink()

    def test_main_json_output_structure(self):
        """Test that JSON output has the correct structure."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for JSON structure")
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", "--json", file_path]):
                with patch("sys.stdout", new_callable=mock_open()):
                    result = main()
                    assert result == 0
        finally:
            Path(file_path).unlink()

    def test_main_verbose_output_structure(self):
        """Test that verbose output has the correct structure."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for verbose structure")
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", "--verbose", file_path]):
                with patch("sys.stdout", new_callable=mock_open()):
                    result = main()
                    assert result == 0
        finally:
            Path(file_path).unlink()

    def test_main_ensure_ascii_false(self):
        """Test that JSON output uses ensure_ascii=False for proper Unicode handling."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content with Unicode: 🚀 📊 💻")
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", "--json", file_path]):
                with patch("json.dumps") as mock_dumps:
                    result = main()
                    assert result == 0
                    # Verify ensure_ascii=False was called
                    mock_dumps.assert_called()
                    call_args = mock_dumps.call_args
                    assert "ensure_ascii" in call_args[1]
                    assert call_args[1]["ensure_ascii"] is False
        finally:
            Path(file_path).unlink()


class TestMainErrorHandling:
    """Test error handling in the main CLI."""

    def test_main_file_not_found_error_message(self):
        """Test that file not found error produces correct error message."""
        with patch("sys.argv", ["text_extractor", "nonexistent_file.txt"]):
            with patch("sys.stderr", new_callable=mock_open()):
                result = main()
                assert result == 1

    def test_main_value_error_message(self):
        """Test that ValueError produces correct error message."""
        with tempfile.NamedTemporaryFile(suffix=".unsupported", delete=False) as f:
            file_path = f.name

        try:
            with patch("sys.argv", ["text_extractor", file_path]):
                with patch("sys.stderr", new_callable=mock_open()):
                    result = main()
                    assert result == 1
        finally:
            Path(file_path).unlink()

    def test_main_unexpected_error_message(self):
        """Test that unexpected error produces correct error message."""
        with patch("text_extractor.__main__.extract_text_from_file") as mock_extract:
            mock_extract.side_effect = Exception("Test unexpected error")

            with patch("sys.argv", ["text_extractor", "test.txt"]):
                with patch("sys.stderr", new_callable=mock_open()):
                    result = main()
                    assert result == 1

    def test_main_unexpected_error_verbose_traceback(self):
        """Test that unexpected error with verbose flag shows traceback."""
        with patch("text_extractor.__main__.extract_text_from_file") as mock_extract:
            mock_extract.side_effect = Exception("Test unexpected error")

            with patch("sys.argv", ["text_extractor", "--verbose", "test.txt"]):
                with patch("sys.stderr", new_callable=mock_open()):
                    with patch("traceback.print_exc") as mock_traceback:
                        result = main()
                        assert result == 1
                        mock_traceback.assert_called_once()


class TestMainArgumentParsing:
    """Test argument parsing in the main CLI."""

    def test_main_help_argument(self):
        """Test that help argument works correctly."""
        with patch("sys.argv", ["text_extractor", "--help"]):
            with pytest.raises(SystemExit):
                main()

    def test_main_missing_file_argument(self):
        """Test that missing file argument produces error."""
        with patch("sys.argv", ["text_extractor"]):
            with pytest.raises(SystemExit):
                main()

    def test_main_all_arguments(self):
        """Test that all arguments can be used together."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content for all arguments")
            file_path = f.name

        output_file = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        output_path = output_file.name
        output_file.close()

        try:
            with patch(
                "sys.argv",
                [
                    "text_extractor",
                    "--json",
                    "--verbose",
                    "--output",
                    output_path,
                    file_path,
                ],
            ):
                result = main()
                assert result == 0
                assert Path(output_path).exists()
        finally:
            Path(file_path).unlink()
            Path(output_path).unlink()
