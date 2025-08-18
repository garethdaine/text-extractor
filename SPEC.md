

# SPEC.md – Text Extraction Tool (MVP)

## 🎯 Purpose

The purpose of this component is to extract clean, structured text from supported document formats. This tool is modular and self-contained, with no responsibilities for file uploads, storage, user interfaces, or database integration.

---

## 📂 Supported File Types and Parsers

| File Type        | Parsing Method                         | Notes                            |
|------------------|-----------------------------------------|----------------------------------|
| `.pdf`           | `pdfminer.six`, fallback: OCR via `pytesseract` | Native text or scanned PDF       |
| `.docx`          | `python-docx`                           | Structured Word documents        |
| `.csv`           | `pandas`                                | Tabular text extraction          |
| `.txt`           | `open().read()`                         | Plain text files                 |
| `.jpg/.png/.webp`| `pytesseract` via `pdf2image` and `PIL` | Image OCR only                   |

---

## 🔄 Extraction Flow

1. Accepts a file path or byte stream input
2. Determines the file type
3. Parses content using the appropriate library
4. Returns structured JSON output

Example output:
```json
{
  "text": "...",
  "file_type": "pdf",
  "ocr_used": false,
  "pages": [
    { "page_number": 1, "text": "...", "ocr": false }
  ]
}
```

---

## 🧪 Validation Criteria

- ✅ Correct parser selected based on file MIME or extension
- ✅ Text accurately extracted (page-level granularity)
- ✅ OCR used only when needed
- ✅ Structured output matches required JSON schema
- ✅ Handles corrupt or malformed documents gracefully

---

## 🔧 Additional Features

### Async Processing
- Non-blocking text extraction with `extract_text_from_file_async()`
- Concurrent processing of multiple documents
- Full async parser implementations for all supported formats

### Language Detection
- Automatic language detection with confidence scoring
- Support for 55+ languages
- Simple language checks and utilities

### Plugin System
- Extensible architecture for custom parsers
- Dynamic loading of parser plugins from files and directories
- Support for both synchronous and asynchronous custom parsers

---

## 🧰 Dependencies

### Core Dependencies
- `pdfminer.six>=20221105` - PDF text extraction
- `python-docx>=0.8.11` - DOCX document parsing
- `pandas>=1.5.0` - CSV data processing
- `pytesseract>=0.3.10` - OCR text recognition
- `pdf2image>=1.16.0` - PDF to image conversion
- `Pillow>=9.0.0` - Image processing
- `chardet>=5.0.0` - Character encoding detection

### Optional Dependencies
- `langdetect>=1.0.9` - Language detection capabilities

---

## ✅ Implemented Enhancements

- ✅ Multi-language OCR support via Tesseract
- ✅ Automatic language detection with confidence scoring
- ✅ Async batch extraction for concurrent processing
- ✅ Plugin system for custom parser extensions
- ✅ Command-line interface with multiple output formats
- ✅ Comprehensive error handling and edge case coverage

## 🧩 Design Principles

- ✅ Single Responsibility: Only handles parsing and text extraction.
- ✅ Decoupled: No coupling to file upload, HTTP interfaces, or storage logic.
- ✅ Reusable: Can be used as a standalone library or within other services.
- ✅ Extensible: Easy to add support for more file types or alternate parsing strategies.
