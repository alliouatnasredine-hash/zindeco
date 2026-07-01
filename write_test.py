from pathlib import Path
Path('communes').mkdir(exist_ok=True)
Path('communes/index.html').write_text('<h1>ok</h1>', encoding='utf-8')
print('written')
