

# ARCHITECTURE.md – Text Extraction Tool

## 🧩 Overview

This module is a standalone, framework-agnostic Python library designed to extract text from a variety of document formats. It is completely decoupled from storage, APIs, or user interfaces. Its sole responsibility is parsing and returning structured textual data.

---

## 📁 Module Structure

```
text_extractor/
├── __init__.py
├── parser_factory.py
├── models.py
├── utils.py
├── parsers/
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── csv_parser.py
│   ├── txt_parser.py
│   └── image_parser.py
tests/
├── test_pdf.py
├── test_docx.py
├── test_csv.py
├── test_txt.py
├── test_image.py
```

---

## ⚙️ Core Components

### `parser_factory.py`

- Factory method that selects the appropriate parser class/function based on file extension or MIME type.

### `parsers/`

- Individual modules that implement parsing logic for a specific file type.
- Each module exposes a `parse(file_path: str) -> dict` interface.

### `models.py`

- Shared Pydantic models or dataclasses to structure parser output:
  - `ExtractedText`
  - `PageText`

### `utils.py`

- File utilities and MIME detection helpers

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

## 🚧 Future Extensions

- CLI interface for batch processing
- Async support
- Language detection pre-parsing
- Extendable plugin system for community parsers
