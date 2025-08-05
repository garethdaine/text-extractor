

# 🧾 Text Extractor

A modular, framework-agnostic Python library for extracting and structuring text from documents. Supports both native parsing and OCR-based extraction for a variety of file types.

---

## ✨ Features

- Native support for `.pdf`, `.docx`, `.csv`, `.txt`
- OCR support for scanned PDFs and images (`.png`, `.jpg`, `.webp`)
- Clean, structured JSON output
- Fully decoupled from storage, upload, or API layers
- Easily extendable with new parser modules
- Test-driven, production-ready design

---

## 📦 Installation

```bash
pip install -e .
```

> Requires Python 3.11+

---

## 🔧 Usage

```python
from text_extractor import extract_text_from_file

result = extract_text_from_file("path/to/document.pdf")

print(result)
```

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

## 📁 Supported File Types

| File Type        | Parser Used              | Notes                     |
|------------------|--------------------------|---------------------------|
| `.pdf`           | `pdfminer.six` + OCR     | OCR fallback for scanned |
| `.docx`          | `python-docx`            | Native Word support       |
| `.csv`           | `pandas`                 | Tabular content parsing   |
| `.txt`           | built-in                 | Plain text                |
| `.png/.jpg/...`  | `pytesseract` + `Pillow` | OCR for image content     |

---

## 🧪 Running Tests

```bash
pytest
```

Each parser has dedicated test coverage with real-world samples. See `tests/`.

---

## 🧠 Project Philosophy

- **Single Responsibility**: Only does text extraction.
- **Decoupled by Design**: No storage, web, or auth logic.
- **Composable**: Can be used in CLI tools, APIs, or apps.
- **Extensible**: Add support for more formats via plugins.

---

## 📜 License

MIT
