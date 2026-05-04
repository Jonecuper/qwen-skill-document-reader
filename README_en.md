# Qwen Code Skill: Document Reader

> 🇷🇺 [Russian version](./README.md)

A universal skill for **Qwen Code** AI agent for reading, analyzing and converting documents: PDF, Word (DOCX), Excel (XLSX).

## Features

| Operation | PDF | DOCX | XLSX | Markdown |
|-----------|-----|------|------|----------|
| Read text | ✅ | ✅ | ✅ | ✅ |
| Extract tables | ✅ | ✅ | ✅ | — |
| Metadata | ✅ | ✅ | ✅ | — |
| Convert | — | →PDF/MD/HTML | →PDF | →DOCX/PDF/HTML |

## Installation

### Quick install

```bash
git clone https://github.com/Jonecuper/qwen-skill-document-reader.git ~/.qwen/skills/document-reader
pip install -r ~/.qwen/skills/document-reader/requirements.txt
```

### For conversion (optional)

```bash
# LibreOffice — for DOCX/XLSX → PDF
# https://www.libreoffice.org/download/download/

# Pandoc — for DOCX ↔ Markdown
# https://pandoc.org/installing.html
```

## Usage

### Extract text

```bash
python ~/.qwen/skills/document-reader/scripts/extract_text.py document.pdf
python ~/.qwen/skills/document-reader/scripts/extract_text.py file.xlsx --tables
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.docx --metadata
```

### Convert

```bash
# DOCX → PDF
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.docx --convert --to pdf

# DOCX → Markdown
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.docx --convert --to md

# Markdown → DOCX
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.md --convert --to docx
```

### Via Qwen Code

```
Analyze this PDF
Convert DOCX to PDF
Extract tables from Excel
Convert to Markdown
```

## Structure

```
document-reader/
├── SKILL.md              # Instructions for the model
├── requirements.txt      # Python dependencies
├── reference.md          # Extended documentation
└── scripts/
    └── extract_text.py   # Extract + Convert
```

## Dependencies (Python)

```
PyPDF2>=3.0.0       # PDF reading
pdfplumber>=0.10.0  # PDF text and tables
python-docx>=1.0.0  # DOCX reading
openpyxl>=3.1.0     # XLSX reading
pandas>=2.0.0       # Data analysis
```

## Compatibility

- **Qwen Code** — primary target
- Can be adapted for other AI agents

## License

MIT

## Author

Inspired by [claude-code-skills](https://github.com/LeoLin990405/claude-code-skills)
