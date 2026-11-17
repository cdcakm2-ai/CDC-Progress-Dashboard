import zipfile
import xml.etree.ElementTree as ET
import os

print("--- Inspecting nw.docx ---")
docx_path = 'raw_drive_data/new_imports/nw.docx'
if os.path.exists(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as z:
            # List files inside docx
            names = z.namelist()
            print("Files in docx:", names[:10])
            if 'word/document.xml' in names:
                xml_content = z.read('word/document.xml').decode('utf-8', errors='ignore')
                # Extract text
                tree = ET.fromstring(xml_content)
                namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                paragraphs = []
                for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                    texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
                    if texts:
                        paragraphs.append(''.join(texts))
                print(f"Total paragraphs in nw.docx: {len(paragraphs)}")
                for i, p in enumerate(paragraphs[:30]):
                    print(f"[{i+1}] {p}")
                with open('raw_drive_data/new_imports/nw_docx_extracted.txt', 'w', encoding='utf-8') as out:
                    out.write('\n'.join(paragraphs))
                print("Saved raw_drive_data/new_imports/nw_docx_extracted.txt")
    except Exception as e:
        print("Error reading docx:", e)

print("\n--- Inspecting XLSX files ---")
xlsx_files = [
    'sheet_main_responses.xlsx',
    'sheet_august_copy_copy.xlsx',
    'sheet_august_copy.xlsx',
    'sheet_monthly_responses.xlsx',
    'sheet_officers_monthly_responses.xlsx'
]

for xf in xlsx_files:
    xpath = os.path.join('raw_drive_data/new_imports', xf)
    print(f"\n==================== {xf} ====================")
    try:
        with zipfile.ZipFile(xpath) as z:
            # Find sheet names from workbook.xml
            wb_xml = z.read('xl/workbook.xml').decode('utf-8', errors='ignore')
            sheets = []
            for m in ET.fromstring(wb_xml).iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
                sheets.append((m.attrib.get('name'), m.attrib.get('sheetId')))
            print(f"Sheets in {xf}: {sheets}")
    except Exception as e:
        print(f"Error inspecting {xf}: {e}")
