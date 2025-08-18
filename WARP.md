# 🧾 Text Extractor - Warp Commands

Quick access commands and workflows for the Text Extractor project, optimized for Warp terminal.

## 🚀 Quick Start

### Setup & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]
```

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt && pip install -e .[dev]
```

## 🧪 Testing & Quality

### Run Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=text_extractor --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m "not slow"

# Run tests in parallel
pytest -n auto

# Run specific test file
pytest tests/test_async_parser.py

# Run with verbose output
pytest -v --tb=short
```

### Code Quality
```bash
# Format code with Black
black text_extractor tests

# Lint with Ruff
ruff check text_extractor tests

# Fix auto-fixable issues
ruff check --fix text_extractor tests

# Run pre-commit hooks
pre-commit run --all-files

# Type checking (if using mypy)
mypy text_extractor
```

## 📄 Document Processing

### CLI Usage
```bash
# Extract text from PDF
python -m text_extractor document.pdf

# Extract with JSON output
python -m text_extractor --json document.pdf

# Extract and save to file
python -m text_extractor --output result.txt document.pdf

# Verbose extraction
python -m text_extractor --verbose document.pdf

# Process multiple files
for file in documents/*.pdf; do python -m text_extractor --json "$file" > "results/$(basename "$file" .pdf).json"; done
```

### Test Document Processing
```bash
# Create test documents directory
mkdir -p test_docs

# Test with sample documents
echo "Hello World" > test_docs/sample.txt
python -m text_extractor test_docs/sample.txt

# Test JSON output
python -m text_extractor --json test_docs/sample.txt | jq .
```

## 🔧 Development Workflows

### Project Structure
```bash
# View project structure
tree -I '__pycache__|*.pyc|.git|venv|.coverage|htmlcov'

# Find specific files
find . -name "*.py" -not -path "./venv/*" | head -10

# Search for specific patterns
grep -r "extract_text" text_extractor/ --include="*.py"
```

### Development Server
```bash
# Run Python REPL with project loaded
python -c "from text_extractor import *; print('Text Extractor loaded')"

# Interactive testing
python -i -c "from text_extractor import extract_text_from_file, extract_text_from_file_async"
```

### Debugging
```bash
# Run with Python debugger
python -m pdb -c continue -m text_extractor document.pdf

# Debug specific test
python -m pytest --pdb tests/test_async_parser.py::test_specific_function

# Run with verbose logging
PYTHONPATH=. python -c "import logging; logging.basicConfig(level=logging.DEBUG); from text_extractor import extract_text_from_file; print(extract_text_from_file('test.txt'))"
```

## 📊 Performance & Monitoring

### Profiling
```bash
# Profile CLI command
python -m cProfile -o profile.stats -m text_extractor document.pdf

# View profile results
python -c "import pstats; p=pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(10)"

# Memory profiling (if memory-profiler installed)
python -m memory_profiler -m text_extractor document.pdf
```

### Benchmarking
```bash
# Time extraction
time python -m text_extractor document.pdf

# Benchmark multiple runs
for i in {1..5}; do time python -m text_extractor document.pdf; done

# Test async performance
python -c "import asyncio; from text_extractor import extract_text_from_file_async; import time; start=time.time(); asyncio.run(extract_text_from_file_async('document.pdf')); print(f'Async: {time.time()-start:.2f}s')"
```

## 🔍 Debugging & Troubleshooting

### Common Issues
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(text-extractor|pdfminer|python-docx|pytesseract)"

# Test OCR dependencies
python -c "import pytesseract; print(pytesseract.get_tesseract_version())"

# Test PDF processing
python -c "from pdfminer.high_level import extract_text; print('PDF processing works')"

# Check file permissions
ls -la document.pdf
```

### Error Diagnosis
```bash
# Run with full traceback
python -m text_extractor document.pdf 2>&1 | cat

# Test specific parser
python -c "from text_extractor.async_parsers import AsyncPdfParser; print('PDF parser imports OK')"

# Validate file type detection
python -c "from text_extractor.utils import detect_file_type; print(detect_file_type('document.pdf'))"
```

## 🚀 Deployment & Build

### Package Building
```bash
# Clean build artifacts
rm -rf build/ dist/ *.egg-info/

# Build source distribution
python -m build --sdist

# Build wheel
python -m build --wheel

# Build both
python -m build

# Check package
twine check dist/*
```

### Release Preparation
```bash
# Update version
python -c "import re; content=open('pyproject.toml').read(); print(re.search(r'version = \"(.*)\"', content).group(1))"

# Generate changelog
git log --oneline --since="1 week ago"

# Tag release
git tag -a v0.1.0 -m "Release version 0.1.0"
```

## 📝 Documentation

### Generate Docs
```bash
# Generate API documentation (if using sphinx)
sphinx-build -b html docs/ docs/_build/html

# View coverage report
python -m http.server 8000 --directory htmlcov
```

### README Updates
```bash
# Count lines of code
find text_extractor -name "*.py" -exec wc -l {} + | tail -1

# Generate examples
python examples/rtf_parser_plugin.py
```

## 🔄 Git Workflows

### Development
```bash
# Create feature branch
git checkout -b feature/new-parser

# Add all changes
git add .

# Commit with message
git commit -m "feat: add new parser for RTF files"

# Push feature branch
git push -u origin feature/new-parser
```

### Maintenance
```bash
# Clean up branches
git branch --merged | grep -v main | xargs -n 1 git branch -d

# View recent changes
git log --oneline -10

# Check status
git status --short
```

## 🎯 Aliases & Shortcuts

Add these to your shell configuration for faster development:

```bash
# Add to ~/.zshrc or ~/.bashrc
alias te-test="pytest -v"
alias te-cov="pytest --cov=text_extractor --cov-report=html"
alias te-format="black text_extractor tests && ruff check --fix text_extractor tests"
alias te-extract="python -m text_extractor"
alias te-json="python -m text_extractor --json"
alias te-install="pip install -e .[dev]"
alias te-clean="find . -type f -name '*.pyc' -delete && find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true"
```

## 📱 Warp-Specific Features

### Workflows
Create Warp workflows for common tasks:

1. **Setup Project**: `pip install -r requirements.txt && pip install -e .[dev]`
2. **Run Tests**: `pytest --cov=text_extractor --cov-report=html`
3. **Format Code**: `black text_extractor tests && ruff check --fix text_extractor tests`
4. **Extract Text**: `python -m text_extractor --json`

### AI Commands
Use Warp AI for quick tasks:
- "Run pytest with coverage for text_extractor"
- "Format Python code in current directory"
- "Extract text from PDF and output as JSON"
- "Find all Python files modified in last week"

---

*This WARP.md file is optimized for the text-extractor project. Update commands as the project evolves.*
