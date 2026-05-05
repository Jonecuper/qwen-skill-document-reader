---
name: document-reader
description: Универсальный навык для чтения, анализа, извлечения данных и конвертации PDF, DOCX, XLSX файлов. Используй когда пользователь просит проанализировать документ, извлечь текст, таблицы или конвертировать файл.
---

# Document Reader Skill

Универсальный набор для работы с документами: PDF, Word (DOCX), Excel (XLSX) — чтение, анализ и конвертация.

## Возможности

| Операция | PDF | DOCX | XLSX | Markdown | Сканы/Изображения |
|----------|-----|------|------|----------|-------------------|
| Чтение текста | ✅ | ✅ | ✅ | ✅ | ⚠️ OCR |
| Извлечение таблиц | ✅ | ✅ | ✅ | — | ⚠️ OCR |
| Метаданные | ✅ | ✅ | ✅ | — | — |
| Конвертация | — | →PDF/MD/HTML | →PDF | →DOCX/PDF/HTML | — |

> ⚠️ **OCR** — требует Tesseract (установка системная, не pip)

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
- "Распознай текст с этого скана"

---

## OCR — Распознавание текста (сканы, изображения)

OCR позволяет извлекать текст из отсканированных документов и изображений.

### Установка

1. **Tesseract OCR** (системная установка):
   - **Windows:** https://github.com/UB-Mannheim/tesseract/wiki
   - **Linux:** `sudo apt install tesseract-ocr`
   - **macOS:** `brew install tesseract`

2. **Python библиотека:**
   ```bash
   pip install pytesseract Pillow
   ```

### Использование

```python
import pytesseract
from PIL import Image

# Распознать текст с изображения
img = Image.open("scan.jpg")
text = pytesseract.image_to_string(img, lang='rus+eng')
print(text)
```

### Скан PDF → текст

```python
import pytesseract
from PIL import Image
import pdfplumber

with pdfplumber.open("scanned.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        # Конвертируем страницу PDF в изображение
        img = page.to_image()
        # Сохраняем временно
        img_path = f"temp_page_{i}.png"
        img.save(img_path)

        # OCR
        text = pytesseract.image_to_string(Image.open(img_path), lang='rus+eng')
        print(f"=== Страница {i+1} ===")
        print(text)
```

### Распознавание таблиц

```python
import pytesseract
from PIL import Image

img = Image.open("table_scan.jpg")
# Распознать как таблицу
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

# Извлечь табличные данные
lines = pytesseract.image_to_string(img)
print(lines)
```

### Языки

```python
# Русский + английский
text = pytesseract.image_to_string(img, lang='rus+eng')

# Только русский
text = pytesseract.image_to_string(img, lang='rus')

# Только английский
text = pytesseract.image_to_string(img, lang='eng')
```

### Получение координат текста

```python
import pytesseract
from PIL import Image

img = Image.open("document.jpg")
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

for i, text in enumerate(data['text']):
    if text.strip():  # Не пустой текст
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        conf = data['conf'][i]
        print(f"{text} (x:{x}, y:{y}, conf:{conf})")
```

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
