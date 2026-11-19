# Aspect-ratio schematic data

`ar-schematic.json` holds the paths that `make_carpet_figures.py` draws in
`notes/lecture-12/figures/aspect-ratio-study.svg`: three sizing plots, at aspect ratio 4,
5 and 6, and the lightest feasible takeoff weight against aspect ratio.

The shapes follow the composite sizing plots of the fighter sizing example in Raymer,
*Aircraft Design: A Conceptual Approach*, 5th ed., AIAA, 2012, Section 19.4. They were
traced from a vector redraw of those plots, not computed. The data is a schematic: the
coordinates are in the axis frame of the redraw (x from 45 to 75, read as
$W_{TO}/S$ in lb/ft²; y from 30,000 to 60,000, read as $W_{TO}$ in lb; the fourth plot
from aspect ratio 3.5 to 6.5 and 42,500 to 50,000 lb), but they are not the values of the
nine-run example of the lecture, and the figure draws no weight scale.

Layout:

- `panels["4"]`, `panels["5"]`, `panels["6"]`, one per aspect ratio:
  - `tw_lo`, `tw_mid`, `tw_hi`: the curves of constant $T_{SL}/W_{TO}$, lowest to highest
    (0.9, 1.0 and 1.1 in the lecture's example), as `[x, y]` points;
  - `constraints`: the three constraint lines, each a list of points;
  - `ticks`: short segments `[[x0, y0], [x1, y1]]` on the failing side of the lines;
  - `matrix_edges`: the first and last $W_{TO}/S$ of the matrix, two segments;
  - `feasible`: the polygon inside the matrix (between the lowest and highest curves)
    on the passing side of all three lines.
- `lightest.marks`: the lightest feasible weight at aspect ratio 4, 5 and 6, as `[AR, y]`;
  `lightest.curve`: the quadratic through the three marks.

The lightest point of each sizing plot and its mark on the fourth plot do not agree in
the source (the marks sit 800 to 3,200 lb above the lowest shaded points). Both put
aspect ratio 5 lightest and 6 heaviest, which is all the schematic shows.
