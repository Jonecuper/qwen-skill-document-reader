#!/usr/bin/env python3
"""
Batch конвертация файлов.

Использование:
    python batch_convert.py <входная_папка> <выходной_формат> [--pattern "*.docx"]
    python batch_convert.py C:\docs pdf
    python batch_convert.py C:\docs docx --pattern "*.md"
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

# Добавляем путь к основному скрипту
sys.path.insert(0, str(Path(__file__).parent))


def find_files(directory: str, pattern: str = "*") -> list:
    """Найти файлы по шаблону."""
    path = Path(directory)
    if pattern == "*":
        # Все поддерживаемые форматы
        extensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.md', '.html']
        files = []
        for ext in extensions:
            files.extend(path.rglob(f"*{ext}"))
        return files
    else:
        return list(path.rglob(pattern))


def convert_file(file_path: str, to_format: str) -> dict:
    """Конвертировать один файл."""
    from extract_text import convert_document
    
    file_path = Path(file_path)
    output_name = f"{file_path.stem}.{to_format}"
    output_path = file_path.parent / output_name
    
    return convert_document(str(file_path), to_format, str(output_path))


def main():
    parser = argparse.ArgumentParser(description="Batch конвертация файлов")
    parser.add_argument("input_dir", help="Папка с файлами")
    parser.add_argument("output_format", choices=["pdf", "docx", "md", "html"],
                        help="Выходной формат")
    parser.add_argument("--pattern", default="*", help="Шаблон файлов (напр. *.docx)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Рекурсивно")
    
    args = parser.parse_args()
    
    files = find_files(args.input_dir, args.pattern)
    
    if not files:
        print(f"Файлы не найдены в {args.input_dir}")
        return
    
    print(f"Найдено {len(files)} файлов. Конвертация в {args.output_format}...")
    
    success = 0
    errors = 0
    
    for file_path in files:
        print(f"\nКонвертация: {file_path.name}")
        result = convert_file(str(file_path), args.output_format)
        
        if result.get("success"):
            print(f"  ✓ {result.get('output', 'ok')}")
            success += 1
        else:
            print(f"  ✗ {result.get('error', 'ошибка')}")
            errors += 1
    
    print(f"\n{'='*50}")
    print(f"Готово: {success} успешно, {errors} ошибок")


if __name__ == "__main__":
    main()