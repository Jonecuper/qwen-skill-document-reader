# Qwen Code Skill: Document Reader

> 🇺🇸 [English version](./README_en.md)

Универсальный навык для AI-агента **Qwen Code** для чтения, анализа и конвертации документов: PDF, Word (DOCX), Excel (XLSX).

## Возможности

| Операция | PDF | DOCX | XLSX | Markdown |
|----------|-----|------|------|----------|
| Чтение текста | ✅ | ✅ | ✅ | ✅ |
| Извлечение таблиц | ✅ | ✅ | ✅ | — |
| Метаданные | ✅ | ✅ | ✅ | — |
| Конвертация | — | →PDF/MD/HTML | →PDF | →DOCX/PDF/HTML |

## Установка

### Быстрая установка

```bash
# Склонировать репозиторий
git clone https://github.com/Jonecuper/qwen-skill-document-reader.git ~/.qwen/skills/document-reader

# Установить зависимости
pip install -r ~/.qwen/skills/document-reader/requirements.txt
```

### Для конвертации (опционально)

```bash
# LibreOffice — для DOCX/XLSX → PDF
# https://www.libreoffice.org/download/download/

# Pandoc — для DOCX ↔ Markdown
# https://pandoc.org/installing.html
```

## Использование

### Извлечение текста

```bash
python ~/.qwen/skills/document-reader/scripts/extract_text.py document.pdf
python ~/.qwen/skills/document-reader/scripts/extract_text.py file.xlsx --tables
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.docx --metadata
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

### Через Qwen Code

```
Проанализируй этот PDF
Конвертируй DOCX в PDF
Извлеки таблицы из Excel
Преобразуй в Markdown
```

## Структура

```
document-reader/
├── SKILL.md              # Инструкции для модели
├── requirements.txt      # Python зависимости
├── reference.md          # Расширенная документация
└── scripts/
    └── extract_text.py   # Извлечение + конвертация
```

## Зависимости (Python)

```
PyPDF2>=3.0.0       # PDF чтение
pdfplumber>=0.10.0  # PDF текст и таблицы
python-docx>=1.0.0  # DOCX чтение
openpyxl>=3.1.0     # XLSX чтение
pandas>=2.0.0       # Анализ данных
```

## Совместимость

- **Qwen Code** — основная цель
- Может быть адаптирован для других AI-агентов

## Лицензия

MIT

## Авторы

Вдохновлено [claude-code-skills](https://github.com/LeoLin990405/claude-code-skills)
