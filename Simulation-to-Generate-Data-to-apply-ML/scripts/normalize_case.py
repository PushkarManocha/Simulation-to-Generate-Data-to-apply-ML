import os
from pathlib import Path

ROOT = Path(r"c:\Users\pushk\Simulation-to-Generate-Data-to-apply-ML")
TEXT_EXTS = {'.py', '.md', '.ipynb', '.csv', '.txt', '.json', '.yaml', '.yml', '.html', '.rst', '.cfg', '.ini', '.tex'}

replacements = [
    ("Pushkar Manocha", "Pushkar Manocha"),
    ("c:\\users\\PUSHKAR\\", "c:\\users\\Pushkar\\"),
    ("c:\\users\\PUSHKAR\\anaconda3", "c:\\users\\Pushkar\\anaconda3"),
    ("PUSHKAR\\anaconda3", "Pushkar\\anaconda3")
]

modified = []
for p, d, files in os.walk(ROOT):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in TEXT_EXTS:
            continue
        path = Path(p) / f
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            continue
        new = text
        for old, newv in replacements:
            new = new.replace(old, newv)
        if new != text:
            path.write_text(new, encoding='utf-8')
            modified.append(str(path))

print('Modified:', len(modified))
for m in modified:
    print(m)
