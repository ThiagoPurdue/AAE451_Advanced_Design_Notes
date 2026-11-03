"""Export every draw.io diagram under notes/ to SVG next to its source.

Run from the book folder:  python3 scripts/export_drawio.py
Needs the draw.io desktop app (macOS: /Applications/draw.io.app; elsewhere
set DRAWIO to the executable). The SVG keeps its text as text.

draw.io writes each color as a light-dark() pair and lets the viewer switch
the background to near black in dark mode, which would leave the dark text
unreadable. The light colors are kept so the figure stays on white, like the
other figures in the book.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

APP = os.environ.get("DRAWIO") or (
    "/Applications/draw.io.app/Contents/MacOS/draw.io" if sys.platform == "darwin"
    else "drawio")
NOTES = Path(__file__).resolve().parents[1] / "notes"
COLOR = r"(?:rgb\([^)]*\)|#[0-9A-Fa-f]{3,8}|[a-zA-Z]+)"

for src in sorted(NOTES.rglob("*.drawio")):
    out = src.with_suffix(".svg")
    subprocess.run([APP, "--export", "--format", "svg", "--border", "8",
                    "--output", str(out), str(src)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    text = out.read_text(encoding="utf-8")
    text = re.sub(rf"light-dark\(\s*({COLOR})\s*,\s*{COLOR}\s*\)", r"\1", text)
    text = text.replace(" color-scheme: light dark;", "")
    out.write_text(text, encoding="utf-8")
    print("exported", out.relative_to(NOTES))
