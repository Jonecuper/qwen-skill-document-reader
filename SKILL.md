---
name: document-reader
description: Универсальный навык для чтения, анализа и извлечения данных из PDF, DOCX и XLSX файлов. Используй когда пользователь просит проанализировать документ, извлечь текст или таблицы из файла.
---

# Document Reader Skill

Универсальный набор для работы с документами: PDF, Word (DOCX) и Excel (XLSX).

## Быстрый старт

### Извлечение текста из любого документа

```bash
python ~/.qwen/skills/document-reader/scripts/extract_text.py <путь_к_файлу>
```

Скрипт автоматически определяет формат файла и извлекает текст.

### Интерактивный режим

Просто опиши задачу естественным языком:
- "Прочитай содержимое этого PDF"
- "Извлеки таблицы из Excel файла"
- "Что находится в этом документе?"

---

## Поддерживаемые форматы

| Формат | Расширение | Библиотека | Возможности |
|--------|------------|------------|-------------|
| PDF | `.pdf` | PyPDF2, pdfplumber | Текст, таблицы, метаданные |
| Word | `.docx` | python-docx | Текст, таблицы, абзацы |
| Excel | `.xlsx`, `.xls` | openpyxl, pandas | Данные, формулы, листы |

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

## Конвертация в другие форматы

### DOCX → Markdown (через pandoc)
```bash
pandoc document.docx -o output.md
```

### DOCX → PDF (через LibreOffice)
```bash
soffice --headless --convert-to pdf document.docx
```

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
2. **Библиотека python-docx** используется для чтения DOCX
3. **pandas** лучше для анализа данных, **openpyxl** — для работы с формулами
4. Для расширенных возможностей (создание/редактирование) см. `reference.md`

---

## См. также

- `reference.md` — расширенная документация по всем форматам
- `scripts/extract_text.py` — универсальный скрипт извлечения
