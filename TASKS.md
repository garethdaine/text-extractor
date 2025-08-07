

# TASKS.md – Text Extraction Tool (MVP)

A modular, test-driven document parsing engine that supports multiple file types with native and OCR-based extraction.

---

## ✅ Phase 1: Core Infrastructure

- [x] Create project scaffolding (`text_extractor/`, `tests/`)
- [x] Define output schema in `models.py` (e.g. `ExtractedText`, `PageText`)
- [x] Implement utility helpers in `utils.py` (e.g. file type resolver)

---

## 🧠 Phase 2: Parser Interfaces

- [x] Define unified parser interface in `parser_factory.py`
- [x] Implement parser selector based on file extension/MIME

---

## 📄 Phase 3: Native Format Parsers

- [x] Implement `pdf_parser.py` using `pdfminer.six`
- [x] Implement `docx_parser.py` using `python-docx`
- [x] Implement `csv_parser.py` using `pandas`
- [x] Implement `txt_parser.py` using built-in Python IO

---

## 🖼️ Phase 4: Image/OCR Parser

- [x] Implement `image_parser.py` using `pytesseract`, `pdf2image`, `Pillow`
- [x] Detect and fallback to OCR if PDF has no extractable text

---

## 🧪 Phase 5: Testing

- [ ] Configure `pytest` test suite
- [ ] Add fixture files for each supported file type
- [ ] Write unit tests for each parser module
- [ ] Validate OCR vs non-OCR behaviour
- [ ] Ensure JSON structure matches `models.py`

---

## 🔌 Phase 6: Integration Layer

- [ ] Implement `extract_text_from_file(path: str)` entry point
- [ ] Ensure it returns the full structured output for any supported file
- [ ] Raise meaningful errors for unsupported or malformed inputs

---

## 🧹 Phase 7: Cleanup & Linting

- [ ] Configure `ruff` or `flake8` + `black` for linting/formatting
- [ ] Add pre-commit hook for formatting
- [ ] Document all public interfaces with docstrings

---

## 🚀 Optional: Post-MVP Enhancements

- [ ] CLI runner for local usage (`python -m text_extractor`)
- [ ] Async parser interface
- [ ] Language detection module
- [ ] Plugin registration for custom parsers
