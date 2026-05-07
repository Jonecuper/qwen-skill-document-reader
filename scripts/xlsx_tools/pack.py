#!/usr/bin/env python3
"""
Pack XML back to XLSX after editing.
Preserves all Excel features including formulas, pivot tables, VBA macros.
"""

import sys
import os
import zipfile
from pathlib import Path


def pack_xlsx(input_dir: str, output_file: str) -> dict:
    """
    Pack directory with XML contents back to xlsx file.

    Args:
        input_dir: Directory with unpacked XML files
        output_file: Path for output .xlsx file

    Returns:
        dict with status
    """
    input_path = Path(input_dir)
    output_path = Path(output_file)

    if not input_path.exists():
        return {"error": f"Directory not found: {input_dir}"}

    if not output_path.suffix.lower() == '.xlsx':
        return {"error": f"Output must be .xlsx file: {output_file}"}

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(input_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(input_dir)
                    zipf.write(file_path, arcname)

        return {
            "success": True,
            "output_file": str(output_path),
            "size_bytes": os.path.getsize(output_file)
        }

    except Exception as e:
        return {"error": f"Failed to pack: {str(e)}"}


def main():
    if len(sys.argv) < 3:
        print("Usage: python pack.py <input_dir> <output.xlsx>")
        print("\nPacks directory with XML back to xlsx file.")
        print("All Excel features (formulas, pivot tables, VBA) are preserved.")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    result = pack_xlsx(input_dir, output_file)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"Successfully packed to: {result['output_file']}")
    print(f"Size: {result['size_bytes']} bytes")


if __name__ == '__main__':
    main()