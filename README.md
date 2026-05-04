# Qwen Code Skill: Document Reader

> 🇺🇸 [English version](./README_en.md)

Универсальный навык для AI-агента **Qwen Code** для чтения и анализа документов: PDF, Word (DOCX), Excel (XLSX).

## Возможности

| Формат | Чтение | Таблицы | Метаданные |
|--------|--------|---------|------------|
| PDF | ✅ | ✅ | ✅ |
| DOCX | ✅ | ✅ | ✅ |
| XLSX | ✅ | ✅ | ✅ |

## Установка

### Быстрая установка

```bash
# Склонировать репозиторий в папку навыков
git clone https://github.com/Jonecuper/qwen-skill-document-reader.git ~/.qwen/skills/document-reader

# Установить зависимости
pip install -r ~/.qwen/skills/document-reader/requirements.txt
```

### Или вручную

1. Скопировать папку `document-reader/` в `~/.qwen/skills/`
2. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

### Через скрипт

```bash
# Извлечь текст из файла
python ~/.qwen/skills/document-reader/scripts/extract_text.py document.pdf

# С таблицами
python ~/.qwen/skills/document-reader/scripts/extract_text.py file.xlsx --tables

# С метаданными
python ~/.qwen/skills/document-reader/scripts/extract_text.py doc.docx --metadata

# В JSON
python ~/.qwen/skills/document-reader/scripts/extract_text.py file.pdf --json

# Сохранить в файл
python ~/.qwen/skills/document-reader/scripts/extract_text.py file.pdf --output result.json
```

### Через Qwen Code

Просто опишите задачу естественным языком:

```
Проанализируй этот PDF файл
Извлеки таблицы из Excel
Что содержится в этом документе Word?
```

Модель автоматически загрузит навык и использует его.

## Структура

```
document-reader/
├── SKILL.md              # Инструкции для модели
├── requirements.txt      # Python зависимости
├── reference.md          # Расширенная документация
└── scripts/
    └── extract_text.py   # Универсальный парсер
```

## Зависимости

```
PyPDF2>=3.0.0       # PDF чтение
pdfplumber>=0.10.0  # PDF текст и таблицы
python-docx>=1.0.0  # DOCX чтение
openpyxl>=3.1.0     # XLSX чтение
pandas>=2.0.0       # Анализ данных
```

## Расширенная документация

См. [`reference.md`](reference.md) для детальной информации:
- Извлечение данных из каждого формата
- Работа с таблицами
- Метаданные
- Создание документов
- Конвертация форматов

## Совместимость

- **Qwen Code** — основная цель
- Может быть адаптирован для других AI-агентов (Claude Code и др.)

## Лицензия

MIT

## Авторы

На основе [claude-code-skills](https://github.com/LeoLin990405/claude-code-skills)
