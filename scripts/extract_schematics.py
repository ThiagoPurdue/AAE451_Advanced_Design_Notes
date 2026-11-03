"""Extract the configuration schematics from the lecture deck as SVG files.

The Aircraft Configuration deck draws its schematics as vector graphics
(TikZ). This script crops each one out of the deck PDF and saves it as SVG,
so the book shows the same drawing as the slide. Run from the book folder:

    python3 scripts/extract_schematics.py <deck.pdf> notes/lecture-03/figures

Set FIG_PREVIEW=<folder> to also write PNG previews of the crops.
"""
import os
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

# Deck page number -> names of the drawings on that page, left to right.
PLAN = {
    4: ["wing-high", "wing-mid", "wing-low"],
    5: ["xsec-circular", "xsec-rectangular", "xsec-blended"],
    6: ["jet-buried", "jet-pod-wing", "jet-pod-aft"],
    7: ["prop-tractor", "prop-pusher", "prop-wing", "prop-combination"],
    8: ["tail-conventional", "tail-t", "tail-cruciform", "tail-v", "tail-h"],
    10: ["gear-tricycle", "gear-taildragger", "gear-bicycle", "gear-single",
         "gear-quadricycle", "gear-bogey"],
}

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
preview = os.environ.get("FIG_PREVIEW")
SCALE = 3.0
doc = fitz.open(src)

for pno, names in PLAN.items():
    page = doc[pno - 1]
    W, H = page.rect.width, page.rect.height
    # drawings in the upper part of the slide, excluding the wide header rule
    # and the wide box at the bottom
    rects = []
    for d in page.get_drawings():
        r = d["rect"]
        if r.width >= 0.4 * W or r.y0 <= 40 or r.y1 >= 0.62 * H:
            continue
        # a stroked line has a zero-height rect, which PyMuPDF treats as empty
        # in unions; grow every rect by its stroke width so lines count
        pad = (d.get("width") or 0) / 2 + 0.5
        rects.append(fitz.Rect(r.x0 - pad, r.y0 - pad, r.x1 + pad, r.y1 + pad))
    rects.sort(key=lambda r: r.x0)
    clusters = []
    for r in rects:
        if clusters and r.x0 <= clusters[-1].x1 + 12:
            clusters[-1] |= r
        else:
            clusters.append(fitz.Rect(r))
    if len(clusters) != len(names):
        sys.exit(f"page {pno}: found {len(clusters)} drawings, expected {len(names)}: {clusters}")
    for name, box in zip(names, clusters):
        box = fitz.Rect(box.x0 - 4, box.y0 - 4, box.x1 + 4, box.y1 + 4) & page.rect
        if preview:
            page.get_pixmap(dpi=160, clip=box).save(Path(preview) / f"{name}.png")
        page.set_cropbox(box)
        svg = page.get_svg_image()
        page.set_cropbox(page.mediabox)
        # the drawing is a few tens of points wide on the slide; give the SVG a
        # larger intrinsic size so it renders at a readable size on the page
        svg = re.sub(r'width="([0-9.]+)" height="([0-9.]+)"',
                     lambda m: f'width="{float(m.group(1)) * SCALE:.0f}" height="{float(m.group(2)) * SCALE:.0f}"',
                     svg, count=1)
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"page {pno}: {name} {box.width:.0f}x{box.height:.0f} pt")
