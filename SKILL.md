---
name: document-reader
description: Универсальный навык для чтения, анализа, извлечения данных и конвертации PDF, DOCX, XLSX файлов. Используй когда пользователь просит проанализировать документ, извлечь текст, таблицы или конвертировать файл.
agent_instruction: |
  При получении задачи на чтение/анализ документа — сразу запускай:
  python ~/.qwen/skills/document-reader/scripts/extract_text.py <путь_к_файлу> [опции]

  Опции:
    --tables      Извлечь таблицы
    --metadata     Показать метаданные
    --json         Вывод в JSON
    --output FILE  Сохранить в файл
    --convert      Конвертировать файл
    --to FORMAT    Формат конвертации: pdf, docx, md, html
    --ocr          Распознать текст (OCR, требует Tesseract)

  Для конвертации: --convert --to pdf|docx|md|html
  Для OCR: --ocr --lang rus+eng
---

# Document Reader Skill

Универсальный набор для работы с документами: PDF, Word (DOCX), Excel (XLSX) — чтение, анализ и конвертация.

## Возможности

| Операция | PDF | DOCX | XLSX | Markdown |
|----------|-----|------|------|----------|
| Чтение текста | ✅ | ✅ | ✅ | ✅ |
| Извлечение таблиц | ✅ | ✅ | ✅ | — |
| Метаданные | ✅ | ✅ | ✅ | — |
| Конвертация | — | →PDF/MD/HTML | →PDF | →DOCX/HTML |
| OCR (сканы) | ✅ | — | — | — |

---

## Использование

### Извлечение текста

```bash
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл>
```

### Извлечение таблиц

```bash
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл> --tables
```

### Показать метаданные

```bash
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл> --metadata
```

### Сохранить в JSON

```bash
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл> --json --output result.json
```

---

## Конвертация

### DOCX → PDF
```bash
python extract_text.py doc.docx --convert --to pdf
```

### DOCX → Markdown
```bash
python extract_text.py doc.docx --convert --to md
```

### Markdown → DOCX
```bash
python extract_text.py doc.md --convert --to docx
```

### DOCX → HTML
```bash
python extract_text.py doc.docx --convert --to html
```

### XLSX → PDF
```bash
python extract_text.py table.xlsx --convert --to pdf
```

---

## OCR — Распознавание текста

Для распознавания текста со сканов и изображений.

### Установка

1. **Tesseract OCR:**
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt install tesseract-ocr tesseract-ocr-rus`
   - macOS: `brew install tesseract tesseract-lang`

2. **Python:**
   ```bash
   pip install pytesseract Pillow
   ```

### Использование

```bash
# Распознать текст с изображения
python extract_text.py scan.jpg --ocr --lang rus+eng

# Распознать текст из PDF-скана
python extract_text.py scanned.pdf --ocr --lang rus+eng

# Только русский
python extract_text.py scan.jpg --ocr --lang rus
```

### Опции OCR

| Опция | Описание |
|-------|----------|
| `--ocr` | Включить режим OCR |
| `--lang LANG` | Язык: `rus`, `eng`, `rus+eng` (по умолчанию) |

---

## Поддерживаемые форматы

| Формат | Расширения | Возможности |
|--------|------------|-------------|
| PDF | `.pdf` | Текст, таблицы, метаданные, OCR |
| Word | `.docx`, `.doc` | Текст, таблицы, конвертация |
| Excel | `.xlsx`, `.xls` | Данные, листы, конвертация в PDF |
| Markdown | `.md` | Конвертация в DOCX/HTML |
| Изображения | `.jpg`, `.png`, `.tif` | OCR |

---

## Требования

### Python зависимости
```bash
pip install -r ~/.qwen/skills/document-reader/requirements.txt
```

### Системные инструменты (опционально)

| Инструмент | Для чего | Ссылка |
|------------|----------|--------|
| LibreOffice | DOCX/XLSX → PDF | https://www.libreoffice.org/download/ |
| Pandoc | DOCX ↔ Markdown | https://pandoc.org/installing.html |
| Tesseract | OCR | https://github.com/UB-Mannheim/tesseract/wiki |

---

## Примеры задач

- "Прочитай содержимое этого PDF"
- "Извлеки таблицы из Excel"
- "Конвертируй DOCX в PDF"
- "Распознай текст с этого скана"
- "Сохрани содержимое в JSON"

---

## См. также

- `reference.md` — расширенная документация
- `scripts/extract_text.py --help` — справка по скрипту
