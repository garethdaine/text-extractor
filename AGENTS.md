# AGENTS.md – Text Extraction Tool

## 🧠 Purpose for Agents

This document is intended for AI coding agents (e.g. OpenAI Codex) to understand how to interact with and extend the text-extraction tool. This module is designed to be completely decoupled from any frontend, storage, or web framework logic.

---

## 📦 What This Module Does

- Accepts a file path or byte stream input.
- Identifies the file type using extension or MIME.
- Uses the appropriate parser to extract textual content:
  - Native parsing for PDF, DOCX, CSV, TXT
  - OCR for scanned PDFs or images
- Returns a structured JSON output with:
  - Combined plain text
  - Page-level breakdown
  - Whether OCR was used

---

## 🚫 What This Module Does *Not* Do

- Handle HTTP requests or routes
- Store data in databases or Supabase
- Manage user sessions or auth
- Perform file uploads or downloads

---

## 📂 Directory Structure (Expected)

```
/text_extractor
  __init__.py
  parser_factory.py
  parsers/
    pdf_parser.py
    docx_parser.py
    csv_parser.py
    txt_parser.py
    image_parser.py
  models.py
  utils.py
```

---

## 🧰 How to Use

```python
from text_extractor import extract_text_from_file

result = extract_text_from_file("documents/sample.pdf")

# Output
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

## 🧩 How to Extend

When adding support for a new file type:

1. Create a new parser in `parsers/`, following the interface:
```python
def parse(file_path: str) -> dict:
    ...
```
2. Register the new parser in `parser_factory.py`
3. Update unit tests for the new type in the test suite

---

## 🧪 Testing Expectations

- Use `pytest`
- Provide one test file per supported format
- Validate:
  - Extracted text is correct
  - OCR flag is respected
  - Structured output format is preserved
