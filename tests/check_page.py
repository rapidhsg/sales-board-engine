"""Fails if the board page's script has a syntax error (a broken page shows only "Loading the engine's plan...").
Usage: python tests/check_page.py   (needs node; skips if node isn't installed)"""
import re, shutil, subprocess, sys, tempfile
from pathlib import Path
page = (Path(__file__).resolve().parents[1] / "dashboard" / "index.html").read_text()
if not shutil.which("node"): print("page check skipped (no node)"); sys.exit(0)
bad = []
for i, js in enumerate(re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", page, re.S)):
    if not js.strip(): continue
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f: f.write(js)
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    if r.returncode: bad.append(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "syntax error")
print("page OK" if not bad else "PAGE BROKEN: " + "; ".join(bad))
sys.exit(1 if bad else 0)
