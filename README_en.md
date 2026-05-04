# Qwen Code Skill: Document Reader

> 🇷🇺 [Русская версия](./README.md)

A universal skill for **Qwen Code** AI agent for reading and analyzing documents: PDF, Word (DOCX), Excel (XLSX).

## Features

| Format | Read | Tables | Metadata |
|--------|------|--------|----------|
| PDF | ✅ | ✅ | ✅ |
| DOCX | ✅ | ✅ | ✅ |
| XLSX | ✅ | ✅ | ✅ |

## Installation

### Quick install

```bash
# Clone repository to skills folder
git clone https://github.com/YOUR_ACCOUNT/qwen-skill-document-reader.git ~/.qwen/skills/document-reader

# Install dependencies
pip install -r ~/.qwen/skills/document-reader/requirements.txt
```

### Manual

1. Copy `document-reader/` folder to `~/.qwen/skills/`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Via script

```bash
# Extract text from file
python ~/.qwen/skills/document-reader/scripts/extract_text.py document.pdf

# With tables
python ~/.qwen/skills/document-reader/scripts/extract_text.py file.xlsx --tables

# With metadata
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.docx --metadata

# JSON output
python ~/.qwen/skills/document-reader/scripts/extract_text.py file.pdf --json

# Save to file
python ~/.qwen/skills/document-reader/scripts/extract_text.py file.pdf --output result.json
```

### Via Qwen Code

Just describe the task in natural language:

```
Analyze this PDF file
Extract tables from Excel
What's in this Word document?
```

The model will automatically load the skill and use it.

## Structure

```
document-reader/
├── SKILL.md              # Instructions for the model
├── requirements.txt      # Python dependencies
├── reference.md          # Extended documentation
└── scripts/
    └── extract_text.py   # Universal parser
```

## Dependencies

```
PyPDF2>=3.0.0       # PDF reading
pdfplumber>=0.10.0  # PDF text and tables
python-docx>=1.0.0  # DOCX reading
openpyxl>=3.1.0     # XLSX reading
pandas>=2.0.0       # Data analysis
```

## Extended Documentation

See [`reference.md`](reference.md) for detailed information:
- Extracting data from each format
- Working with tables
- Metadata extraction
- Creating documents
- Format conversion

## Compatibility

- **Qwen Code** — primary target
- Can be adapted for other AI agents (Claude Code, etc.)

## License

MIT

## Author

Inspired by [claude-code-skills](https://github.com/LeoLin990405/claude-code-skills)
