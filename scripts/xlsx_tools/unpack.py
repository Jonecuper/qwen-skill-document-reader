#!/usr/bin/env python3
"""
Unpack XLSX to XML for safe editing.
Excel files are ZIP archives with XML inside - this lets you edit without breaking formulas/VBA.
"""

import sys
import os
import zipfile
import shutil
from pathlib import Path


def unpack_xlsx(input_file: str, output_dir: str) -> dict:
    """
    Unpack xlsx file to directory with XML contents.

    Args:
        input_file: Path to .xlsx file
        output_dir: Directory to extract to

    Returns:
        dict with status and extracted paths
    """
    input_path = Path(input_file)
    output_path = Path(output_dir)

    if not input_path.exists():
        return {"error": f"File not found: {input_file}"}

    if input_path.suffix.lower() != '.xlsx':
        return {"error": f"Not an xlsx file: {input_file}"}

    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)

    try:
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(output_path)

        # Find workbook.xml to get sheet names
        sheet_info = []
        workbook_path = output_path / 'xl' / 'workbook.xml'
        rels_path = output_path / 'xl' / '_rels' / 'workbook.xml.rels'

        if workbook_path.exists() and rels_path.exists():
            import xml.etree.ElementTree as ET

            tree = ET.parse(workbook_path)
            ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

            rels_tree = ET.parse(rels_path)
            rels_ns = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}

            sheets = {}
            for rel in rels_tree.findall('.//rel:Relationship', rels_ns):
                rid = rel.get('Id')
                target = rel.get('Target')
                if target:
                    sheets[rid] = target

            for sheet in tree.findall('.//main:sheet', ns):
                name = sheet.get('name')
                rid = sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                target = sheets.get(rid, 'unknown')
                sheet_info.append({
                    "name": name,
                    "file": f"xl/{target}" if not target.startswith('worksheets/') else f"xl/{target}"
                })

        files_extracted = []
        for root, dirs, files in os.walk(output_path):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(output_path)
                files_extracted.append(str(rel_path))

        return {
            "success": True,
            "output_dir": str(output_path),
            "sheets": sheet_info,
            "files_extracted": len(files_extracted),
            "files": files_extracted[:20]  # Preview first 20
        }

    except Exception as e:
        return {"error": f"Failed to unpack: {str(e)}"}


def main():
    if len(sys.argv) < 3:
        print("Usage: python unpack.py <input.xlsx> <output_dir>")
        print("\nUnpacks xlsx file to XML for safe editing.")
        print("xlsx files are ZIP archives - this extracts the XML inside.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    result = unpack_xlsx(input_file, output_dir)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"Successfully unpacked to: {result['output_dir']}")
    print(f"Files extracted: {result['files_extracted']}")
    if result.get('sheets'):
        print("\nSheets found:")
        for sheet in result['sheets']:
            print(f"  - {sheet['name']}: {sheet['file']}")


if __name__ == '__main__':
    main()