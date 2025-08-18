# AGENTS.md – Text Extraction Tool

## 🧠 Purpose for Agents

This document is intended for AI coding agents (e.g. OpenAI Codex) to understand how to interact with and extend the text-extraction tool. This module is designed to be completely decoupled from any frontend, storage, or web framework logic.

---

## 📦 What This Module Does

### Core Text Extraction
- Accepts a file path input for various document formats
- Identifies file type using extension or MIME type detection
- Uses appropriate parser to extract textual content:
  - Native parsing for PDF, DOCX, CSV, TXT
  - OCR for scanned PDFs or images (PNG, JPG, WEBP)
- Returns structured data with combined text and page-level breakdown

### Advanced Features
- **Async Processing**: Non-blocking text extraction with `extract_text_from_file_async()`
- **Language Detection**: Automatic language detection with confidence scoring for 55+ languages
- **Plugin System**: Extensible architecture for custom parsers with dynamic loading
- **CLI Interface**: Command-line tool with JSON output, file output, and verbose modes
- **Error Handling**: Comprehensive error handling for unsupported files and edge cases

---

## 🚫 What This Module Does *Not* Do

- Handle HTTP requests or routes
- Store data in databases or Supabase
- Manage user sessions or auth
- Perform file uploads or downloads

---

## 📂 Directory Structure (Current)

```
/text_extractor
  __init__.py                    # Main exports and sync entry point
  __main__.py                    # CLI interface
  parser_factory.py             # Sync parser factory
  async_parser_factory.py       # Async parser factory
  language_detection.py         # Language detection module
  plugin_registry.py            # Plugin system
  models.py                      # Data models
  utils.py                       # Utilities
  parsers/                       # Synchronous parsers
    pdf_parser.py
    docx_parser.py
    csv_parser.py
    txt_parser.py
    image_parser.py
  async_parsers/                 # Asynchronous parsers
    async_pdf_parser.py
    async_docx_parser.py
    async_csv_parser.py
    async_txt_parser.py
    async_image_parser.py
```

---

## 🧰 How to Use

### Synchronous Processing
```python
from text_extractor import extract_text_from_file

result = extract_text_from_file("documents/sample.pdf")
print(f"Extracted {len(result.text)} characters from {result.file_type}")
```

### Asynchronous Processing
```python
import asyncio
from text_extractor import extract_text_from_file_async

async def process_docs():
    result = await extract_text_from_file_async("documents/sample.pdf")
    return result

result = asyncio.run(process_docs())
```

### Language Detection
```python
from text_extractor import detect_language, is_english

# Detect language with confidence
lang_info = detect_language("Hello, world!")
if lang_info:
    print(f"Language: {lang_info.language}, Confidence: {lang_info.confidence}")

# Quick English check
if is_english("Hello, world!"):
    print("Text is English")
```

### Plugin System
```python
from text_extractor import register_sync_parser, get_plugin_registry
from text_extractor.models import ExtractedText, PageText

# Register custom parser
def my_parser(file_path: str) -> ExtractedText:
    # Custom parsing logic
    return ExtractedText(...)

register_sync_parser("myformat", my_parser, [".myf"])

# Load plugins from directory
registry = get_plugin_registry()
registry.load_plugin_from_directory("./plugins")
```

### Output Structure
```python
# ExtractedText dataclass
{
  "text": "Combined text from all pages",
  "file_type": "pdf",
  "ocr_used": False,
  "pages": [
    {"page_number": 1, "text": "Page 1 text", "ocr": False}
  ]
}
```

---

## 🧩 How to Extend

### Adding Custom Parsers via Plugin System

1. **Create a plugin file** with your custom parser:
```python
# my_plugin.py
from text_extractor.models import ExtractedText, PageText

def parse_my_format(file_path: str) -> ExtractedText:
    # Your parsing logic here
    return ExtractedText(...)

def register_parsers(registry):
    registry.register_sync_parser(
        file_type="myformat",
        parser=parse_my_format,
        extensions=[".myf"],
        mime_types=["application/myformat"]
    )
```

2. **Load the plugin**:
```python
from text_extractor import get_plugin_registry
registry = get_plugin_registry()
registry.load_plugin_from_file("my_plugin.py")
```

### Adding Built-in Parsers

1. Create parser in `parsers/` (sync) or `async_parsers/` (async)
2. Follow the `parse(file_path: str) -> ExtractedText` interface
3. Register in the appropriate factory's `_PARSERS` dict
4. Add comprehensive unit tests

---

## 🧪 Testing Expectations

- **Framework**: Use `pytest` with 211 comprehensive tests
- **Coverage**: Test files for each parser, async functionality, language detection, plugins
- **Edge Cases**: Dedicated edge case test files for robust error handling
- **Validation**:
  - Extracted text accuracy
  - OCR flag correctness
  - Structured output format compliance
  - Async/sync behavior consistency
  - Plugin system functionality
  - Language detection accuracy
  - CLI interface behavior

### Test Structure
```
tests/
├── test_*_parser.py           # Individual parser tests
├── test_async_*.py            # Async functionality tests
├── test_language_detection.py # Language detection tests
├── test_plugin_*.py           # Plugin system tests
├── test_*_edge_cases.py       # Edge case coverage
└── fixtures/                  # Test data files
```
