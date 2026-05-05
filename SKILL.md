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

Универсальный набор для работы с документами: PDF, Word (DOCX), Excel (XLSX), Markdown — чтение, анализ, конвертация и заполнение форм.

## Возможности

| Операция | PDF | DOCX | XLSX | Markdown |
|----------|-----|------|------|----------|
| Чтение текста | ✅ | ✅ | ✅ | ✅ |
| Извлечение таблиц | ✅ | ✅ | ✅ | — |
| Метаданные | ✅ | ✅ | ✅ | — |
| Конвертация | — | →PDF/MD/HTML | →PDF | →DOCX/HTML |
| OCR (сканы) | ✅ | — | — | — |
| Заполнение форм | ✅ | — | — | — |
| Пересчёт формул XLSX | — | — | ✅ | — |
| Unpack/Pack DOCX | — | ✅ | — | — |

---

## Извлечение текста

```bash
# Базовое извлечение
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл>

# С таблицами
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл> --tables

# С метаданными
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл> --metadata

# В JSON
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл> --json --output result.json
```

---

## Конвертация

### Один файл

```bash
# DOCX → PDF
python extract_text.py doc.docx --convert --to pdf

# DOCX → Markdown
python extract_text.py doc.docx --convert --to md

# Markdown → DOCX
python extract_text.py doc.md --convert --to docx

# DOCX → HTML
python extract_text.py doc.docx --convert --to html

# XLSX → PDF
python extract_text.py table.xlsx --convert --to pdf
```

### Несколько файлов (batch)

```bash
# Конвертировать все файлы в папке
python ~/.qwen/skills/document-reader/scripts/batch_convert.py <папка> pdf

# Только DOCX файлы
python batch_convert.py <папка> pdf --pattern "*.docx"

# Рекурсивно
python batch_convert.py <папка> docx --pattern "*.md" --recursive
```

---

## OCR — Распознавание текста

Для распознавания текста со сканов и изображений.

### Установка

1. **Tesseract OCR:** https://github.com/UB-Mannheim/tesseract/wiki
2. **Python:** `pip install pytesseract Pillow pymupdf`

### Использование

```bash
# Распознать текст с изображения
python extract_text.py scan.jpg --ocr --lang rus+eng

# Распознать текст из PDF-скана
python extract_text.py scanned.pdf --ocr --lang rus+eng

# Только русский
python extract_text.py scan.jpg --ocr --lang rus
```

---

## PDF Формы — Заполнение анкет

### Проверка типа формы

```bash
# Определить тип формы
python ~/.qwen/skills/document-reader/scripts/pdf_forms/check_fillable_fields.py <файл.pdf>
```

**Результат:**
- "This PDF has fillable form fields" → используйте fill_fillable_fields.py
- "This PDF does not have fillable form fields" → используйте fill_pdf_form_with_annotations.py

### Заполнение fillable форм

```bash
# 1. Извлечь информацию о полях
python pdf_forms/extract_form_field_info.py input.pdf field_info.json

# 2. Конвертировать PDF в изображения для анализа
python pdf_forms/convert_pdf_to_images.py input.pdf output_folder

# 3. Создать файл значений
# Создайте field_values.json:
# [
#   {"field_id": "last_name", "value": "Иванов"},
#   {"field_id": "checkbox1", "value": "/On"}
# ]

# 4. Заполнить форму
python pdf_forms/fill_fillable_fields.py input.pdf field_values.json output.pdf
```

### Заполнение НЕ-fillable форм (по координатам)

```bash
# 1. Конвертировать в изображения
python pdf_forms/convert_pdf_to_images.py input.pdf output_folder

# 2. Проанализировать изображения и определить координаты полей

# 3. Создать fields.json с координатами:
# {
#   "pages": [{"page_number": 1, "image_width": 800, "image_height": 1000}],
#   "form_fields": [
#     {
#       "page_number": 1,
#       "description": "Фамилия",
#       "field_label": "Last name",
#       "label_bounding_box": [30, 125, 95, 142],
#       "entry_bounding_box": [100, 125, 280, 142],
#       "entry_text": {"text": "Петров", "font_size": 14}
#     }
#   ]
# }

# 4. Проверить координаты
python pdf_forms/check_bounding_boxes.py fields.json

# 5. Создать валидационные изображения
python pdf_forms/create_validation_image.py 1 fields.json input.png validation.png

# 6. Заполнить форму
python pdf_forms/fill_pdf_form_with_annotations.py input.pdf fields.json output.pdf
```

---

## DOCX — Работа с XML структурой

### Unpack (распаковка)

```bash
# Распаковать DOCX для редактирования XML
python ~/.qwen/skills/document-reader/scripts/docx_tools/unpack.py doc.docx unpacked_folder

# Скрипт покажет suggested RSID для tracked changes
```

### Pack (упаковка)

```bash
# Упаковать обратно в DOCX
python ~/.qwen/skills/document-reader/scripts/docx_tools/pack.py unpacked_folder output.docx
```

### Пример workflow

```bash
# 1. Распаковать
python docx_tools/unpack.py document.docx temp

# 2. Отредактировать XML файлы в temp/word/

# 3. Упаковать
python docx_tools/pack.py temp document_modified.docx
```

---

## XLSX — Пересчёт формул

```bash
# Пересчитать все формулы в Excel файле
python ~/.qwen/skills/document-reader/scripts/recalc.py spreadsheet.xlsx

# С увеличенным таймаутом
python recalc.py spreadsheet.xlsx 60

# Результат — JSON с ошибками:
# {
#   "status": "success",
#   "total_errors": 0,
#   "total_formulas": 42
# }
#
# При ошибках:
# {
#   "status": "errors_found",
#   "total_errors": 2,
#   "error_summary": {
#     "#REF!": {"count": 1, "locations": ["Sheet1!B5"]}
#   }
# }
```

---

## Поддерживаемые форматы

| Формат | Расширения | Возможности |
|--------|------------|-------------|
| PDF | `.pdf` | Текст, таблицы, метаданные, OCR, формы |
| Word | `.docx`, `.doc` | Текст, таблицы, конвертация, unpack/pack |
| Excel | `.xlsx`, `.xls` | Данные, листы, конвертация в PDF, пересчёт формул |
| Markdown | `.md` | Конвертация в DOCX/HTML |
| Изображения | `.jpg`, `.png`, `.tif` | OCR |

---

## Требования

### Python зависимости

```bash
pip install PyPDF2 pdfplumber python-docx openpyxl pandas pytesseract Pillow pymupdf defusedxml
```

### Системные инструменты

| Инструмент | Для чего | Ссылка |
|------------|----------|--------|
| LibreOffice | DOCX/XLSX → PDF | https://www.libreoffice.org/download/ |
| Pandoc | DOCX ↔ Markdown/HTML | https://pandoc.org/installing.html |
| Tesseract | OCR | https://github.com/UB-Mannheim/tesseract/wiki |

---

## Структура скриптов

```
scripts/
├── extract_text.py          # Основной скрипт (текст, таблицы, конвертация, OCR)
├── batch_convert.py         # Batch конвертация
├── recalc.py               # Пересчёт формул XLSX
├── pdf_forms/               # Работа с PDF формами
│   ├── check_fillable_fields.py
│   ├── extract_form_field_info.py
│   ├── convert_pdf_to_images.py
│   ├── fill_fillable_fields.py
│   ├── check_bounding_boxes.py
│   ├── create_validation_image.py
│   └── fill_pdf_form_with_annotations.py
└── docx_tools/             # Работа с DOCX XML
    ├── unpack.py
    └── pack.py
```

---

## Примеры задач

- "Прочитай содержимое этого PDF"
- "Извлеки таблицы из Excel"
- "Конвертируй DOCX в PDF"
- "Распознай текст с этого скана"
- "Заполни анкету (PDF форма)"
- "Пересчитай формулы в Excel"
- "Редактируй структуру DOCX"
- "Конвертируй все файлы в папке в PDF"