

# 🧾 Text Extractor

A modular, framework-agnostic Python library for extracting and structuring text from documents. Supports both native parsing and OCR-based extraction for a variety of file types, with async processing, language detection, and extensible plugin architecture.

---

## ✨ Features

- **Multi-format support**: PDF, DOCX, CSV, TXT, PNG, JPG, WEBP
- **OCR integration**: Automatic fallback to OCR for images and image-only PDFs
- **Async processing**: Non-blocking text extraction with `extract_text_from_file_async()`
- **Language detection**: Automatic language detection with confidence scoring
- **Plugin system**: Extensible architecture for custom parsers
- **CLI interface**: Command-line tool with JSON output support
- **Clean, structured output**: Consistent JSON schema with page-level details
- **Fully decoupled**: No storage, upload, or API dependencies
- **Production-ready**: Comprehensive testing and error handling

---

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd text-extractor

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Requirements

- Python 3.11+
- Core dependencies: `pdfminer.six`, `python-docx`, `pandas`, `pytesseract`, `pdf2image`, `Pillow`
- Optional: `chardet` (for encoding detection), `langdetect` (for language detection)

---

## 🔧 Basic Usage

### Synchronous Text Extraction

```python
from text_extractor import extract_text_from_file

# Extract text from any supported file
result = extract_text_from_file("path/to/document.pdf")

print(f"File type: {result.file_type}")
print(f"OCR used: {result.ocr_used}")
print(f"Text: {result.text}")
print(f"Pages: {len(result.pages)}")

# Access page-level details
for page in result.pages:
    print(f"Page {page.page_number}: {page.text[:100]}...")
```

### Asynchronous Text Extraction

```python
import asyncio
from text_extractor import extract_text_from_file_async

async def process_documents():
    # Process multiple files concurrently
    tasks = [
        extract_text_from_file_async("document1.pdf"),
        extract_text_from_file_async("document2.docx"),
        extract_text_from_file_async("document3.csv")
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        print(f"Extracted {len(result.text)} characters from {result.file_type}")

# Run the async function
asyncio.run(process_documents())
```

### Language Detection

```python
from text_extractor import detect_language, is_english, get_supported_languages

# Detect language with confidence
result = detect_language("Hello, world! This is English text.")
if result:
    print(f"Language: {result.language}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reliable: {result.is_reliable}")

# Quick language checks
if is_english("Hello, world!"):
    print("Text is in English")

# Get supported languages
languages = get_supported_languages()
print(f"Supports {len(languages)} languages")
```

### Plugin System

```python
from text_extractor import register_sync_parser, get_plugin_registry
from text_extractor.models import ExtractedText, PageText

# Define a custom parser
def my_custom_parser(file_path: str) -> ExtractedText:
    with open(file_path, 'r') as f:
        content = f.read()

    return ExtractedText(
        text=content,
        file_type="custom",
        pages=[PageText(page_number=1, text=content, ocr=False)]
    )

# Register the parser
register_sync_parser(
    file_type="custom",
    parser=my_custom_parser,
    extensions=[".custom"],
    mime_types=["application/custom"]
)

# Now you can use it like any other parser
result = extract_text_from_file("document.custom")
```

---

## 🖥️ Command Line Interface

### Basic Usage

```bash
# Extract text and print to stdout
python -m text_extractor document.pdf

# Output in JSON format
python -m text_extractor --json document.pdf

# Save output to file
python -m text_extractor --output result.txt document.pdf

# Verbose mode with file information
python -m text_extractor --verbose document.pdf
```

### CLI Examples

```bash
# Extract from PDF
python -m text_extractor document.pdf

# Extract from DOCX with JSON output
python -m text_extractor --json document.docx

# Extract from CSV and save to file
python -m text_extractor --output extracted.txt data.csv

# Verbose extraction from image
python -m text_extractor --verbose image.png
```

### CLI Output Examples

**Standard output:**
```
Hello, world! This is the extracted text from the document.
```

**JSON output:**
```json
{
  "text": "Hello, world! This is the extracted text from the document.",
  "file_type": "pdf",
  "ocr_used": false,
  "pages": [
    {
      "page_number": 1,
      "text": "Hello, world! This is the extracted text from the document.",
      "ocr": false
    }
  ]
}
```

**Verbose output:**
```
File: document.pdf
Type: pdf
OCR Used: False
Pages: 1
----------------------------------------
Hello, world! This is the extracted text from the document.
```

---

## 📁 Supported File Types

| File Type        | Parser Used              | Notes                     |
|------------------|--------------------------|---------------------------|
| `.pdf`           | `pdfminer.six` + OCR     | OCR fallback for scanned |
| `.docx`          | `python-docx`            | Native Word support       |
| `.csv`           | `pandas`                 | Tabular content parsing   |
| `.txt`           | built-in                 | Plain text                |
| `.png/.jpg/.webp`| `pytesseract` + `Pillow` | OCR for image content     |

---

## 🔌 Plugin System

### Creating Custom Parsers

Create a Python file with your custom parser:

```python
# my_parser.py
from text_extractor.models import ExtractedText, PageText

def parse_my_format(file_path: str) -> ExtractedText:
    # Your parsing logic here
    with open(file_path, 'r') as f:
        content = f.read()

    return ExtractedText(
        text=content,
        file_type="myformat",
        pages=[PageText(page_number=1, text=content, ocr=False)]
    )

def register_parsers(registry):
    """Register parsers with the plugin registry."""
    registry.register_sync_parser(
        file_type="myformat",
        parser=parse_my_format,
        extensions=[".myf"],
        mime_types=["application/myformat"]
    )
```

### Loading Plugins

```python
from text_extractor import get_plugin_registry

# Load a single plugin
registry = get_plugin_registry()
registry.load_plugin_from_file("my_parser.py")

# Load all plugins from a directory
registry.load_plugin_from_directory("./plugins")

# Now you can use your custom format
result = extract_text_from_file("document.myf")
```

---

## 🌍 Language Detection

### Supported Languages

The language detection module supports 55+ languages including:
- English (en), Spanish (es), French (fr), German (de)
- Chinese (zh-cn, zh-tw), Japanese (ja), Korean (ko)
- Arabic (ar), Russian (ru), Portuguese (pt)
- And many more...

### Usage Examples

```python
from text_extractor import detect_language, detect_language_simple, is_english

# Full language detection with confidence
result = detect_language("Bonjour, comment allez-vous?")
if result:
    print(f"Detected: {result.language}")
    print(f"Confidence: {result.confidence:.2f}")

# Simple language code detection
lang_code = detect_language_simple("Hola, mundo!")
print(f"Language: {lang_code}")  # Output: es

# Quick English check
if is_english("Hello, world!"):
    print("Text is English")
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=text_extractor --cov-report=term-missing

# Run specific test categories
pytest tests/test_async_parser.py
pytest tests/test_language_detection.py
pytest tests/test_plugin_registry.py
```

### Test Coverage

- **78 tests** covering all functionality
- **68% code coverage** with comprehensive edge case testing
- Async functionality testing with pytest-asyncio
- Plugin system testing with temporary files
- Language detection testing with multiple languages

---

## 📊 Output Schema

All text extraction methods return an `ExtractedText` object with the following structure:

```python
@dataclass
class ExtractedText:
    text: str                    # Combined text from all pages
    file_type: str              # File type identifier
    ocr_used: bool = False      # Whether OCR was used
    pages: List[PageText]       # Page-level details

@dataclass
class PageText:
    page_number: int            # Page number (1-indexed)
    text: str                   # Text from this page
    ocr: bool = False          # Whether OCR was used for this page
```

### JSON Output Format

```json
{
  "text": "Combined text from all pages",
  "file_type": "pdf",
  "ocr_used": false,
  "pages": [
    {
      "page_number": 1,
      "text": "Text from page 1",
      "ocr": false
    },
    {
      "page_number": 2,
      "text": "Text from page 2",
      "ocr": true
    }
  ]
}
```

---

## 🔧 Advanced Usage

### Error Handling

```python
from text_extractor import extract_text_from_file

try:
    result = extract_text_from_file("document.pdf")
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Unsupported file type: {e}")
except Exception as e:
    print(f"Parsing error: {e}")
```

### Plugin Registry Management

```python
from text_extractor import get_plugin_registry

registry = get_plugin_registry()

# List all registered parsers
parsers = registry.list_registered_parsers()
for file_type, extensions in parsers.items():
    print(f"{file_type}: {extensions}")

# Check if a parser exists
if registry.get_sync_parser("pdf"):
    print("PDF parser is available")
```

### Language Detection with Custom Confidence

```python
from text_extractor import detect_language

# Use custom confidence threshold
result = detect_language("Short text", min_confidence=0.9)
if result and result.is_reliable:
    print(f"Confident detection: {result.language}")
```

---

## 🚀 Performance

### Async Processing

For high-throughput applications, use the async interface:

```python
import asyncio
from text_extractor import extract_text_from_file_async

async def process_batch(file_paths):
    tasks = [extract_text_from_file_async(path) for path in file_paths]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Error processing {file_paths[i]}: {result}")
        else:
            print(f"Processed {file_paths[i]}: {len(result.text)} chars")

# Process multiple files concurrently
asyncio.run(process_batch(["doc1.pdf", "doc2.docx", "doc3.csv"]))
```

---

## 🧠 Project Philosophy

- **Single Responsibility**: Only handles text extraction
- **Decoupled by Design**: No storage, web, or auth dependencies
- **Composable**: Can be used in CLI tools, APIs, or applications
- **Extensible**: Add support for new formats via plugins
- **Async-First**: Non-blocking operations for high performance
- **Language-Aware**: Built-in language detection capabilities

---

## 📜 License

MIT License - see LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run linting
ruff check .

# Run formatting
black .

# Run tests
pytest
```
