import os
from docx import Document

def read_file(fn):
    basename, ext = os.path.splitext(fn)
    if ext == '.docx':
        f = open(fn, 'rb')
        document = Document(f)
        f.close()
        txt = ''
        for para in document.paragraphs:
            try:
                txt = txt + para.text
            except:
                pass
    elif ext == '.txt':
        with open(fn, 'r', errors='ignore', encoding="utf-8") as f:
            txt = f.read()
    else:
        print('Unknown file type: skipping')
        txt = None
    return txt

def write_file(fn, txt):
    basename, ext = os.path.splitext(fn)
    if ext == ".txt":
        with open(fn, 'w', encoding="utf-8") as f:
            f.write(txt)
    elif ext == '.docx':
        document = Document()
        p = document.add_paragraph(txt)
        document.save(fn)
    else:
        print("Unknown file type: Cannot save")
