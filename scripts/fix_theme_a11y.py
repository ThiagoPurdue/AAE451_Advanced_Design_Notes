"""Post-build accessibility fixes for the MyST book theme.

Run after `jupyter-book build --html`:  python3 scripts/fix_theme_a11y.py _build/html

The theme gives two kinds of links an aria-label that differs from their
visible text, which fails WCAG 2.1 success criterion 2.5.3 (Label in Name):

1. Figure, table, definition and exercise number links in captions
   ("Figure 1:") are labelled "Link to this figure" and so on. The label is kept only for the pilcrow anchors next
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

# Regular expressions, not literal strings: the minifier renames variables and
# switches between "..." and `...` quotes from one theme release to the next.
# The bundle sits in build/ (themes before November 2026) or _assets/ (after).
JS_PATCHES = [
    ("caption link label",
     re.compile(r'title:(\w+),"aria-label":\1,children:(\w+)\}\)'),
     r'title:\1,"aria-label":\2==="\\xB6"?\1:void 0,children:\2})'),
    ("footer link label",
     re.compile(r'"aria-label":`\$\{\w+\?["`]Previous: ["`]:["`]Next: ["`]\}\$\{\w+\}`,'),
     ""),
]

applied = {name: 0 for name, _, _ in JS_PATCHES}
for js in [*root.glob("build/**/*.js"), *root.glob("_assets/**/*.js")]:
    text = js.read_text(encoding="utf-8")
    new = text
    for name, pattern, rep in JS_PATCHES:
        new, n = pattern.subn(rep, new)
        applied[name] += n
    if new != text:
        js.write_text(new, encoding="utf-8")

missing = [name for name, n in applied.items() if n == 0]
if missing:
    sys.exit("Theme code changed; patch not applied: " + "; ".join(missing))

caption_label = re.compile(
    r'(<a [^>]*title="Link to this [A-Za-z ]+") aria-label="Link to this [A-Za-z ]+"(>(?!¶))')
footer_label = re.compile(r' aria-label="(?:Next|Previous): [^"]*"')
# The {iframe} directive writes no title attribute (WCAG 4.1.2). Quick-check
# widgets get the <title> of their own HTML file; anything else a plain name.
iframe_tag = re.compile(r'<iframe(?![^>]*\btitle=)([^>]*\bsrc="[^"]*?([^"/]+)\.html"[^>]*)>')
title_tag = re.compile(r"<title>(.*?)</title>", re.S)


def iframe_title(m):
    name = m.group(2)
    src = Path("quickcheck") / f"{name}.html"
    title = "Embedded content"
    if src.exists():
        found = title_tag.search(src.read_text(encoding="utf-8"))
        if found:
            title = found.group(1).strip()
    return f'<iframe title="{title}"{m.group(1)}>'


pages = 0
for html in root.glob("**/*.html"):
    text = html.read_text(encoding="utf-8")
    new = caption_label.sub(r"\1\2", text)
    new = footer_label.sub("", new)
    new = iframe_tag.sub(iframe_title, new)
    if new != text:
        html.write_text(new, encoding="utf-8")
        pages += 1

print(f"Patched the theme bundle ({sum(applied.values())} changes) and {pages} HTML pages.")
