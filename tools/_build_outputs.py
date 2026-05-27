#!/usr/bin/env python
"""One-off: build PDFs for outputs/generated/ master prompts."""
import sys, io, subprocess, pathlib, platform
import markdown

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME_WIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """
@page { size: A4; margin: 20mm 18mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
       font-size: 10.5pt; line-height: 1.55; color: #1a1a1a; max-width: 100%; }
h1 { font-size: 22pt; color: #6b2c00; border-bottom: 3px solid #d4a017; padding-bottom: 6pt; margin-top: 24pt; }
h2 { font-size: 16pt; color: #6b2c00; margin-top: 18pt; border-left: 4px solid #d4a017; padding-left: 10pt; }
h3 { font-size: 13pt; color: #8a3b00; margin-top: 14pt; }
h4, h5, h6 { font-size: 11.5pt; color: #555; }
p { margin: 8pt 0; }
code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: "Consolas", "Courier New", monospace; font-size: 9pt; color: #b8860b; }
pre { background: #2a1a0a; color: #f0e6c8; padding: 12pt; border-radius: 6pt; overflow: auto; font-size: 8.5pt; line-height: 1.4; white-space: pre-wrap; word-break: break-word; }
pre code { background: transparent; color: inherit; padding: 0; }
ul, ol { margin: 8pt 0 8pt 22pt; }
li { margin: 3pt 0; }
strong { color: #6b2c00; }
em { color: #8a3b00; }
blockquote { border-left: 3px solid #d4a017; padding-left: 12pt; color: #555; margin: 8pt 0; font-style: italic; }
table { border-collapse: collapse; margin: 10pt 0; width: 100%; font-size: 9.5pt; }
th, td { border: 1px solid #ccc; padding: 5pt 8pt; text-align: left; }
th { background: #6b2c00; color: #f0e6c8; }
tr:nth-child(even) { background: #fafafa; }
hr { border: none; border-top: 2px dashed #d4a017; margin: 18pt 0; }
.footer { position: fixed; bottom: 10mm; left: 18mm; right: 18mm; text-align: center; font-size: 8pt; color: #999; border-top: 1px solid #eee; padding-top: 4pt; }
"""

TARGETS = [
    ROOT / "outputs" / "generated" / "historical-reconstructions-v3.md",
    ROOT / "outputs" / "generated" / "abandoned-home-restoration-v2.md",
]

def md_to_html(md_path, title):
    md_text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(md_text, extensions=["extra", "tables", "fenced_code", "toc"])
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>
<body>{html_body}
<div class="footer">Reborn Forge v2.4.0 &bull; {title}</div>
</body></html>"""

def build(md_path, out_dir):
    title = md_path.stem.replace("-", " ").title()
    html = md_to_html(md_path, title)
    html_dir = ROOT / "_html"
    html_dir.mkdir(exist_ok=True)
    html_path = html_dir / (md_path.stem + ".html")
    html_path.write_text(html, encoding="utf-8")
    pdf_path = out_dir / (md_path.stem + ".pdf")
    print(f"Building {pdf_path.name} ...")
    user_data = ROOT / "_chrome_profile"
    user_data.mkdir(exist_ok=True)
    r = subprocess.run([
        CHROME_WIN, "--headless=new", "--disable-gpu", "--no-sandbox",
        f"--user-data-dir={user_data}",
        "--no-pdf-header-footer",
        "--virtual-time-budget=2000",
        f"--print-to-pdf={pdf_path}",
        f"file:///{html_path.as_posix()}"
    ], capture_output=True, text=True)
    if r.returncode != 0:
        print("  STDERR:", r.stderr[:500])
        return False
    print(f"  OK {pdf_path.stat().st_size // 1024} KB -> {pdf_path}")
    return True

if __name__ == "__main__":
    pdf_root = ROOT / "PDF"
    pdf_root.mkdir(exist_ok=True)
    for t in TARGETS:
        if not t.exists():
            print(f"MISSING {t}")
            continue
        per_project = pdf_root / t.stem
        per_project.mkdir(exist_ok=True)
        build(t, per_project)
    print("Done.")
