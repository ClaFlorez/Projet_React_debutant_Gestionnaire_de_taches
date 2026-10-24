"""Vérifie les ressources référencées et l’inventaire de l’archive."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '.venv', 'venv', 'node_modules', 'dist', '__pycache__', 'output'}
TEXT = {'.md', '.py', '.js', '.jsx', '.json', '.txt', '.yml', '.yaml', '.css', '.html', '.svg'}
INDEX = ROOT / 'docs' / 'INVENTAIRE_SHA256.json'

def payload(p):
    data = p.read_bytes()
    if p.suffix in TEXT or p.name in {'.gitignore', '.gitattributes'}:
        data = data.replace(b'\r\n', b'\n')
    return data

def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(part in EXCLUDED for part in p.relative_to(ROOT).parts)
                  and p.suffix not in {'.log', '.pyc'} and p != INDEX)

def main():
    all_files = files()
    for p in all_files:
        if p.suffix != '.md':
            continue
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            if target.startswith(('http:', 'https:', '#', 'mailto:')):
                continue
            clean = target.split('#')[0].strip('<>')
            if clean and not (p.parent / clean).resolve().exists():
                raise AssertionError(f'Lien absent : {p.relative_to(ROOT)} -> {clean}')
    records = [{'path': p.relative_to(ROOT).as_posix(),
                'sha256': hashlib.sha256(payload(p)).hexdigest()}
               for p in all_files]
    if '--write' in sys.argv:
        INDEX.write_text(json.dumps({'text_normalization': 'CRLF -> LF; binary unchanged',
                                     'files': records}, ensure_ascii=False, indent=2) + '\n',
                         encoding='utf-8')
        print(f'Inventaire écrit : {len(records)} fichiers')
    else:
        expected = json.loads(INDEX.read_text(encoding='utf-8'))['files']
        assert records == expected, 'L’inventaire ne correspond pas aux fichiers actuels'
        print(f'Intégrité confirmée : {len(records)} fichiers et liens locaux valides')

if __name__ == '__main__':
    main()
