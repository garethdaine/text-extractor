

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

## 🔐 Security & Scope

- All actions are **user-scoped** using Supabase RLS
- Uploaded files are private by default
- Extracted text is not exposed outside the authenticated session

---

## 🧰 Dependencies

- `pdfminer.six`
- `python-docx`
- `pandas`
- `pytesseract`
- `pdf2image`
- `PIL` (Pillow)
- `uuid`, `json`, `datetime`, `typing`

---

## 🚧 Future Considerations

- Add support for multi-language OCR
- Perform automatic language detection
- Introduce async batch extraction for large files

## 🧩 Design Principles

- ✅ Single Responsibility: Only handles parsing and text extraction.
- ✅ Decoupled: No coupling to file upload, HTTP interfaces, or storage logic.
- ✅ Reusable: Can be used as a standalone library or within other services.
- ✅ Extensible: Easy to add support for more file types or alternate parsing strategies.
