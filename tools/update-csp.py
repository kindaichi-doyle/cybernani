#!/usr/bin/env python3
"""Ricalcola l'hash SHA-256 dello <script> inline di ogni pagina e aggiorna la
Content-Security-Policy nel <meta>. Da lanciare dopo ogni modifica al JavaScript:

    python3 tools/update-csp.py
"""
import base64, hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["viaggio-messaggio/index.html", "intelligenza-artificiale/index.html"]
META = re.compile(r'(<meta http-equiv="Content-Security-Policy" content="[^"]*script-src )\'[^\']*\'')

for rel in PAGES:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    if len(scripts) != 1:
        raise SystemExit(f"{rel}: atteso 1 <script> inline, trovati {len(scripts)}")
    digest = base64.b64encode(hashlib.sha256(scripts[0].encode("utf-8")).digest()).decode()
    new, n = META.subn(rf"\1'sha256-{digest}'", html)
    if n != 1:
        raise SystemExit(f"{rel}: meta CSP non trovato")
    if new != html:
        path.write_text(new, encoding="utf-8")
    print(f"{rel}: sha256-{digest}")
