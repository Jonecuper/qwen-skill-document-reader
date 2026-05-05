# Document Reader — Расширенная документация

## Содержание
1. [Установка](#установка)
2. [PDF](#pdf)
3. [DOCX](#docx)
4. [XLSX](#xlsx)
5. [OCR — распознавание](#ocr--распознавание)
6. [Создание документов](#создание-документов)
7. [Конвертация](#конвертация)

---

## Установка

```bash
pip install -r ~/.qwen/skills/document-reader/requirements.txt
```

---

## PDF

### Библиотеки
- **PyPDF2** — базовые операции, метаданные
- **pdfplumber** — извлечение текста и таблиц

### Извлечение текста с layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        # Текст сохраняет позиции
        text = page.extract_text()
        print(text)
```

### Извлечение таблиц
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

    # Объединить все таблицы
    if all_tables:
        combined = pd.concat(all_tables, ignore_index=True)
        combined.to_excel("tables.xlsx", index=False)
```

### Метаданные
```python
from PyPDF2 import PdfReader

reader = PdfReader("document.pdf")
meta = reader.metadata

print(f"Страниц: {len(reader.pages)}")
print(f"Заголовок: {meta.title}")
print(f"Автор: {meta.author}")
print(f"Тема: {meta.subject}")
```

### Merge PDF
```python
from PyPDF2 import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Split PDF
```python
from PyPDF2 import PdfWriter, PdfReader

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### Rotate pages
```python
from PyPDF2 import PdfWriter, PdfReader

reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # 90, 180, 270
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

---

## DOCX

### Библиотека
- **python-docx** — чтение и создание Word документов

### Чтение текста
```python
from docx import Document

doc = Document("document.docx")

# Все параграфы
for para in doc.paragraphs:
    print(para.text)

# Только непустые
non_empty = [p.text for p in doc.paragraphs if p.text.strip()]
```

### Чтение таблиц
```python
from docx import Document

doc = Document("document.docx")

for i, table in enumerate(doc.tables):
    print(f"Таблица {i+1}:")
    for row in table.rows:
        cells = [cell.text for cell in row.cells]
        print(" | ".join(cells))
```

### Метаданные
```python
from docx import Document

doc = Document("document.docx")
props = doc.core_properties

print(f"Автор: {props.author}")
print(f"Заголовок: {props.title}")
print(f"Тема: {props.subject}")
print(f"Ключевые слова: {props.keywords}")
```

### Чтение с сохранением стилей
```python
from docx import Document

doc = Document("document.docx")

for para in doc.paragraphs:
    if para.style and para.text.strip():
        print(f"[{para.style.name}] {para.text}")
```

### Навигация по заголовкам
```python
from docx import Document

doc = Document("document.docx")

# Найти все заголовки
for para in doc.paragraphs:
    if para.style.name.startswith("Heading"):
        level = para.style.name  # Heading 1, Heading 2, etc.
        print(f"{level}: {para.text}")
```

---

## XLSX

### Библиотеки
- **openpyxl** — формулы, форматирование
- **pandas** — анализ данных

### Чтение через pandas
```python
import pandas as pd

# Один лист
df = pd.read_excel("file.xlsx")
print(df.head())

# Все листы
all_sheets = pd.read_excel("file.xlsx", sheet_name=None)
for name, sheet in all_sheets.items():
    print(f"{name}: {len(sheet)} строк")

# Определённые столбцы
df = pd.read_excel("file.xlsx", usecols=["A", "C", "E"])

# Типы данных
df = pd.read_excel("file.xlsx", dtype={"id": str, "amount": float})
```

### Чтение через openpyxl
```python
from openpyxl import load_workbook

wb = load_workbook("file.xlsx", data_only=True)

# Список листов
print(wb.sheetnames)

# Работа с листом
sheet = wb["Sheet1"]
print(f"Строк: {sheet.max_row}, Столбцов: {sheet.max_column}")

# Итерация
for row in sheet.iter_rows(min_row=1, max_row=10, values_only=True):
    print(row)

# Конкретная ячейка
value = sheet["A1"].value
```

### Чтение формул (НЕ вычисленных значений)
```python
from openpyxl import load_workbook

# По умолчанию читает формулы
wb = load_workbook("file.xlsx")
cell = wb["A1"]
print(cell.value)  # "=SUM(B1:B10)"

# Для вычисленных значений
wb = load_workbook("file.xlsx", data_only=True)
cell = wb["A1"]
print(cell.value)  # 42
```

### Работа с формулами
```python
from openpyxl import Workbook

wb = Workbook()
sheet = wb.active

# Формула
sheet["A1"] = 10
sheet["A2"] = 20
sheet["A3"] = "=SUM(A1:A2)"  # 30

# Формула с функциями
sheet["B1"] = "=AVERAGE(A1:A2)"
sheet["B2"] = '=IF(A1>5, "Да", "Нет")'

wb.save("output.xlsx")
```

---

## OCR — распознавание

### Установка

**Tesseract OCR** (системная установка):
- **Windows:** https://github.com/UB-Mannheim/tesseract/wiki
- **Linux:** `sudo apt install tesseract-ocr tesseract-ocr-rus`
- **macOS:** `brew install tesseract tesseract-lang`

**Python библиотека:**
```bash
pip install pytesseract Pillow
```

### Базовое использование

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

# Простое извлечение текста
lines = pytesseract.image_to_string(img)
print(lines)

# С координатами
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
```

### Настройка Tesseract

```python
import pytesseract

# Указать путь к tesseract (если не в PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Распознать с улучшенными параметрами
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(img, config=custom_config, lang='rus+eng')
```

### PSM режимы (Page Segmentation Mode)

| Режим | Описание |
|-------|----------|
| 3 | Полностью автоматически (по умолчанию) |
| 4 | Разделение на колонки |
| 6 | Единый блок текста |
| 11 | Разделение на строки |
| 12 | Разделение на слова |

### OEM режимы (OCR Engine Mode)

| Режим | Описание |
|-------|----------|
| 3 | Нейросетевой (лучший результат) |
| 1 | Legacy + LSTM |
| 0 | Только legacy |

---

## Создание документов

### Создание PDF (reportlab)
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=A4)
width, height = A4

c.drawString(100, height - 100, "Привет, мир!")
c.drawString(100, height - 120, "Это PDF созданный с reportlab")

c.save()
```

### Создание DOCX
```python
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()

# Заголовок
doc.add_heading("Заголовок документа", level=1)

# Параграф
p = doc.add_paragraph("Обычный текст")
p.add_run("Жирный").bold = True
p.add_run(" и ")
p.add_run("курсив").italic = True

# Таблица
table = doc.add_table(rows=2, cols=3)
table.cell(0, 0).text = "Заголовок 1"
table.cell(0, 1).text = "Заголовок 2"

doc.save("output.docx")
```

### Создание XLSX
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
sheet = wb.active
sheet.title = "Данные"

# Заголовок
sheet["A1"] = "Имя"
sheet["B1"] = "Возраст"
sheet["A1"].font = Font(bold=True)
sheet["A1"].fill = PatternFill("solid", fgColor="CCCCCC")

# Данные
sheet["A2"] = "Иван"
sheet["B2"] = 25

# Формула
sheet["B3"] = "=SUM(B2)"

wb.save("output.xlsx")
```

---

## Конвертация

### Через extract_text.py (рекомендуется)

```bash
# DOCX → PDF
python extract_text.py doc.docx --convert --to pdf

# DOCX → Markdown
python extract_text.py doc.docx --convert --to md

# DOCX → HTML
python extract_text.py doc.docx --convert --to html

# Markdown → DOCX
python extract_text.py doc.md --convert --to docx

# XLSX → PDF
python extract_text.py table.xlsx --convert --to pdf
```

### Вручную через Pandoc

```bash
# DOCX → Markdown
pandoc document.docx -o output.md

# DOCX → HTML
pandoc document.docx -o output.html

# Markdown → DOCX
pandoc document.md -o output.docx

# HTML → Markdown
pandoc document.html -o output.md

# С track changes
pandoc --track-changes=all document.docx -o output.md
```

### Вручную через LibreOffice

```bash
# DOCX → PDF
soffice --headless --convert-to pdf document.docx

# XLSX → PDF
soffice --headless --convert-to pdf spreadsheet.xlsx

# Все файлы в папке
soffice --headless --convert-to pdf --outdir ./output ./input/*.docx
```

### Python конвертация (docx2pdf)

```python
# pip install docx2pdf
from docx2pdf import convert

convert("input.docx", "output.pdf")
convert("input.docx")  # Сохранит рядом с .docx
```

### XLSX → CSV
```python
import pandas as pd

df = pd.read_excel("file.xlsx")
df.to_csv("file.csv", index=False)
```

### PDF → изображения
```bash
# Установка: sudo apt install poppler-utils
pdftoppm -jpeg -r 150 document.pdf page
# Создаёт page-1.jpg, page-2.jpg и т.д.
```

---

## Требования для конвертации

### LibreOffice
- **Windows:** https://www.libreoffice.org/download/
- **Linux:** `sudo apt install libreoffice`
- **macOS:** `brew install --cask libreoffice`

### Pandoc
- **Windows:** https://pandoc.org/installing.html
- **Linux:** `sudo apt install pandoc`
- **macOS:** `brew install pandoc`

### docx2pdf
```bash
pip install docx2pdf
```

---

## Полезные команды

| Задача | Команда |
|--------|---------|
| Извлечь текст из PDF | `pdftotext file.pdf -` |
| PDF в HTML | `pdftotext -htmlmeta file.pdf -` |
| Информация о PDF | `pdfinfo file.pdf` |
| Конвертация DOCX | `pandoc file.docx -o file.md` |
