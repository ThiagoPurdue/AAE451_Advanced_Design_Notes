"""Post-build accessibility fixes for the MyST book theme.

Run after `jupyter-book build --html`:  python3 scripts/fix_theme_a11y.py _build/html

The theme gives two kinds of links an aria-label that differs from their
visible text, which fails WCAG 2.1 success criterion 2.5.3 (Label in Name):

1. Figure and table number links in captions ("Figure 1:") are labelled
   "Link to this figure". The label is kept only for the pilcrow anchors next
   to headings, whose visible text is a symbol.
2. Previous and next page links in the footer are labelled "Next: <title>".
   Without the label, their name is their visible text.

Both the server-rendered HTML and the JavaScript bundle are patched, so the
pages stay correct after client-side navigation. The script stops with an
error if the theme code has changed and a patch no longer applies.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_build/html")

JS_PATCHES = [
    ('title:r,"aria-label":r,children:n})',
     'title:r,"aria-label":n==="\\xB6"?r:void 0,children:n})'),
    ('"aria-label":`${o?"Previous: ":"Next: "}${a}`,', ""),
]

applied = {old: 0 for old, _ in JS_PATCHES}
for js in root.glob("build/**/*.js"):
    text = js.read_text(encoding="utf-8")
    new = text
    for old, rep in JS_PATCHES:
        if old in new:
            applied[old] += new.count(old)
            new = new.replace(old, rep)
    if new != text:
        js.write_text(new, encoding="utf-8")

missing = [old for old, n in applied.items() if n == 0]
if missing:
    sys.exit("Theme code changed; patch not applied: " + "; ".join(missing))

caption_label = re.compile(
    r'(<a [^>]*title="Link to this [a-z]+") aria-label="Link to this [a-z]+"(>(?!¶))')
footer_label = re.compile(r' aria-label="(?:Next|Previous): [^"]*"')
pages = 0
for html in root.glob("**/*.html"):
    text = html.read_text(encoding="utf-8")
    new = caption_label.sub(r"\1\2", text)
    new = footer_label.sub("", new)
    if new != text:
        html.write_text(new, encoding="utf-8")
        pages += 1

print(f"Patched the theme bundle ({sum(applied.values())} changes) and {pages} HTML pages.")
