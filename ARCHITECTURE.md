

# ARCHITECTURE.md – Text Extraction Tool

## 🧩 Overview

This module is a standalone, framework-agnostic Python library designed to extract text from a variety of document formats. It is completely decoupled from storage, APIs, or user interfaces. Its sole responsibility is parsing and returning structured textual data.

---

## 📁 Module Structure

```
text_extractor/
├── __init__.py
├── __main__.py                    # CLI entry point
├── parser_factory.py             # Synchronous parser factory
├── async_parser_factory.py       # Asynchronous parser factory
├── models.py                      # Data models (ExtractedText, PageText)
├── utils.py                       # Utility functions
├── language_detection.py         # Language detection module
├── plugin_registry.py            # Plugin system for custom parsers
├── parsers/                       # Synchronous parsers
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── csv_parser.py
│   ├── txt_parser.py
│   └── image_parser.py
└── async_parsers/                 # Asynchronous parsers
    ├── __init__.py
    ├── async_pdf_parser.py
    ├── async_docx_parser.py
    ├── async_csv_parser.py
    ├── async_txt_parser.py
    └── async_image_parser.py

tests/
├── test_main.py                   # CLI tests
├── test_parser_factory.py        # Sync parser factory tests
├── test_async_parser_factory.py  # Async parser factory tests
├── test_async_parser.py          # General async tests
├── test_models.py                 # Data model tests
├── test_utils.py                  # Utility function tests
├── test_language_detection.py    # Language detection tests
├── test_plugin_registry.py       # Plugin system tests
├── test_parser_factory_plugins.py # Plugin integration tests
├── test_pdf_parser.py             # PDF parser tests
├── test_docx_parser.py            # DOCX parser tests
├── test_csv_parser.py             # CSV parser tests
├── test_txt_parser.py             # TXT parser tests
├── test_image_parser.py           # Image parser tests
├── test_async_parsers.py          # Async parser tests
├── test_*_edge_cases.py           # Edge case test files
└── fixtures/                      # Test fixture files
    ├── sample.txt
    └── sample.csv
```

---

## ⚙️ Core Components

### `parser_factory.py` & `async_parser_factory.py`

- Factory methods that select the appropriate parser class/function based on file extension or MIME type
- Separate factories for synchronous and asynchronous operations
- Integration with plugin registry for custom parsers

### `parsers/` & `async_parsers/`

- Individual modules that implement parsing logic for specific file types
- Synchronous parsers in `parsers/` directory
- Asynchronous parsers in `async_parsers/` directory
- Each module exposes a unified `parse(file_path: str) -> ExtractedText` interface

### `models.py`

- Dataclasses to structure parser output:
  - `ExtractedText` - Main result container
  - `PageText` - Individual page information
  - `LanguageInfo` - Language detection results

### `language_detection.py`

- Automatic language detection with confidence scoring
- Support for 55+ languages via langdetect library
- Utility functions for language validation

### `plugin_registry.py`

- Extensible plugin system for custom parsers
- Dynamic loading from files and directories
- Support for both sync and async custom parsers

### `utils.py`

- File type resolution and MIME detection helpers
- Utility functions shared across parsers

### `__main__.py`

- Command-line interface implementation
- Support for JSON output, file output, and verbose modes

---

## 🔄 Execution Flow

1. Entry point: `extract_text_from_file(path)`
2. `parser_factory` identifies the correct parser
3. Selected parser reads the file and returns structured JSON:
```json
{
  "text": "...",
  "file_type": "pdf",
  "ocr_used": false,
  "pages": [{ "page_number": 1, "text": "...", "ocr": false }]
}
```

---

## 🧪 Testing Strategy

- Uses `pytest` for unit tests
- Each parser has its own test file and fixture data
- Test assertions:
  - Extracted text is valid and non-empty
  - `ocr_used` flag behaves correctly
  - JSON structure conforms to expected schema

---

## ✅ Implemented Extensions

- ✅ CLI interface for batch processing with multiple output formats
- ✅ Full async support with dedicated async parsers
- ✅ Language detection with confidence scoring
- ✅ Extendable plugin system for community parsers
- ✅ Comprehensive error handling and edge case coverage
- ✅ Production-ready testing with 211 test cases

## 🔄 Plugin Architecture

The plugin system allows for easy extension with custom parsers:

1. **Plugin Discovery**: Plugins are loaded from Python files or directories
2. **Registration**: Plugins register parsers via a `register_parsers(registry)` function
3. **Integration**: Custom parsers are automatically integrated into the main factory
4. **Type Safety**: Both sync and async parsers follow strict protocol interfaces
