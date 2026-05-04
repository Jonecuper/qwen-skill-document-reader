---
name: document-reader
description: Универсальный навык для чтения, анализа, извлечения данных и конвертации PDF, DOCX, XLSX файлов. Используй когда пользователь просит проанализировать документ, извлечь текст, таблицы или конвертировать файл.
---

# Document Reader Skill

Универсальный набор для работы с документами: PDF, Word (DOCX), Excel (XLSX) — чтение, анализ и конвертация.

## Возможности

| Операция | PDF | DOCX | XLSX | Markdown |
|----------|-----|------|------|----------|
| Чтение текста | ✅ | ✅ | ✅ | ✅ |
| Извлечение таблиц | ✅ | ✅ | ✅ | — |
| Метаданные | ✅ | ✅ | ✅ | — |
| Конвертация | — | →PDF/MD/HTML | →PDF | →DOCX/PDF/HTML |

---

## Быстрый старт

### Извлечение текста

```bash
python ~/.qwen/skills/document-reader/scripts/extract_text.py <файл>
```

### Конвертация

```bash
# DOCX → PDF
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.docx --convert --to pdf

# DOCX → Markdown
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.docx --convert --to md

# Markdown → DOCX
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.md --convert --to docx
```

### Интерактивный режим

Просто опиши задачу естественным языком:
- "Прочитай содержимое этого PDF"
- "Конвертируй DOCX в PDF"
- "Извлеки таблицы из Excel"
- "Преобразуй документ в Markdown"

---

## Поддерживаемые форматы

| Формат | Расширение | Возможности |
|--------|------------|-------------|
| PDF | `.pdf` | Чтение, таблицы, метаданные |
| Word | `.docx`, `.doc` | Чтение, конвертация |
| Excel | `.xlsx`, `.xls` | Чтение, конвертация в PDF |
| Markdown | `.md` | Чтение, конвертация |
| HTML | `.html` | Конвертация |

---

## Извлечение данных

### PDF — текст
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### PDF — таблицы
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### DOCX — текст
```python
from docx import Document

doc = Document("document.docx")
for para in doc.paragraphs:
    print(para.text)
```

### DOCX — таблицы
```python
from docx import Document

doc = Document("document.docx")
for table in doc.tables:
    for row in table.rows:
        print([cell.text for cell in row.cells])
```

### XLSX — данные (pandas)
```python
import pandas as pd

df = pd.read_excel("spreadsheet.xlsx")
print(df.head())
print(df.describe())
```

### XLSX — данные (openpyxl)
```python
from openpyxl import load_workbook

wb = load_workbook("spreadsheet.xlsx")
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Лист: {sheet_name}")
    for row in sheet.iter_rows(max_row=10, values_only=True):
        print(row)
```

---

## Извлечение метаданных

### PDF метаданные
```python
from PyPDF2 import PdfReader

reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Автор: {meta.author}")
print(f"Заголовок: {meta.title}")
print(f"Страниц: {len(reader.pages)}")
```

### DOCX метаданные
```python
from docx import Document

doc = Document("document.docx")
props = doc.core_properties
print(f"Автор: {props.author}")
print(f"Заголовок: {props.title}")
```

---

## Анализ структуры

### XLSX — список листов
```python
from openpyxl import load_workbook

wb = load_workbook("spreadsheet.xlsx")
print("Листы:", wb.sheetnames)
```

### DOCX — параграфы и стили
```python
from docx import Document

doc = Document("document.docx")
for para in doc.paragraphs:
    if para.style.name:
        print(f"[{para.style.name}] {para.text}")
```

---

## Конвертация документов

### Через скрипт (рекомендуется)

```bash
python extract_text.py input.docx --convert --to pdf
python extract_text.py input.docx --convert --to md
python extract_text.py input.md --convert --to docx
python extract_text.py input.docx --convert --to html
```

### Поддерживаемые направления

| Из | В | Инструмент |
|----|----|------------|
| DOCX | PDF | LibreOffice |
| DOCX | Markdown | Pandoc |
| DOCX | HTML | Pandoc |
| XLSX | PDF | LibreOffice |
| Markdown | DOCX | Pandoc |
| Markdown | HTML | Pandoc |
| HTML | DOCX | Pandoc |
| HTML | Markdown | Pandoc |

### Требования

- **LibreOffice** — для конвертации в PDF: https://www.libreoffice.org/
- **Pandoc** — для конвертации через командную строку: https://pandoc.org/

---

## Работа с файлами

### Получить информацию о файле
```python
import os

path = "document.pdf"
size = os.path.getsize(path)
print(f"Размер: {size / 1024:.1f} KB")
```

### Сохранить извлечённые данные
```python
import pandas as pd

# Сохранить таблицу в Excel
df.to_excel("output.xlsx", index=False)

# Или в CSV
df.to_csv("output.csv", index=False)
```

---

## Важные замечания

1. **Установи зависимости**: `pip install -r ~/.qwen/skills/document-reader/requirements.txt`
2. **Для конвертации** установи LibreOffice и/или Pandoc
3. **python-docx** используется для чтения DOCX
4. **pandas** лучше для анализа данных, **openpyxl** — для работы с формулами
5. Для расширенных возможностей (создание/редактирование) см. `reference.md`

---

## См. также

- `reference.md` — расширенная документация
- `scripts/extract_text.py` — универсальный скрипт с поддержкой конвертации
