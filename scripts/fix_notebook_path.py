from pathlib import Path
p = Path(r"c:\Users\pushk\Simulation-to-Generate-Data-to-apply-ML\mpb_simulation_2.ipynb")
text = p.read_text(encoding='utf-8')
old = "Pushkar Manocha\\\\anaconda3"
old2 = "Pushkar Manocha\\anaconda3"
new = "PUSHKAR\\\\anaconda3"
# Replace both escaped forms
text2 = text.replace(old, new).replace(old2, new)
if text2 != text:
    p.write_text(text2, encoding='utf-8')
    print('Updated notebook file')
else:
    print('No matching patterns found')
