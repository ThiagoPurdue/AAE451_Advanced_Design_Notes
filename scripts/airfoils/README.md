# Airfoil data used by the figure scripts

Published coordinates and measured curves. Nothing here is computed or invented.

| File | Airfoil | Ordinates published in | Fetched from |
|---|---|---|---|
| `naca652415.dat` | NACA 65(2)-415 | Abbott, von Doenhoff and Stivers (1945), NACA Report 824 | https://m-selig.ae.illinois.edu/ads/coord/naca652415.dat |
| `naca64a410.dat` | NACA 64A410 | Loftin (1948), NACA Report 903 | https://m-selig.ae.illinois.edu/ads/coord/naca64a410.dat |
| `nlf416.dat` | NASA NLF(1)-0416 | Somers (1981), NASA TP-1861 | https://m-selig.ae.illinois.edu/ads/coord/nlf416.dat |
| `sc20710.dat` | NASA SC(2)-0710 | Harris (1990), NASA TP-2969 | https://m-selig.ae.illinois.edu/ads/coord/sc20710.dat |
| `sc20714.dat` | NASA SC(2)-0714 | Harris (1990), NASA TP-2969 | https://m-selig.ae.illinois.edu/ads/coord/sc20714.dat |

The `.dat` files hold the numbers of the UIUC Airfoil Coordinates Database files (fetched
2026-11-16), rewritten in one order: upper surface from the trailing edge to the leading
edge, then the lower surface. The report named for each airfoil is the one the database
and Gudmundsson (2022), Table 8-10, give; the ordinates were not checked against the
reports themselves.

`gudmundsson-fig-8-74.json`: the lift curves and drag polars of the NACA 23015 and the
NACA 65(2)-415 (data of NACA Report 824), read from the plotted curves of Gudmundsson
(2022), Figure 8-74, by color segmentation of the figure image. The figure and its text
give no Reynolds number, so none is stated here or on the page. The dashed NACA 23015
curves are medians over bins (1 degree of angle of attack on the lift curve, 0.03 in lift
coefficient on the polar). Reading accuracy is about 0.01 in lift coefficient, 0.0002 in
drag coefficient and 0.2 degrees in angle of attack.

What the scripts assert about the read curves: `section_data` checks the NACA 65(2)-415
against Gudmundsson's Table 8-9 (lift-curve slope 0.107 per degree, zero-lift angle -2.6
degrees, minimum drag 0.0042, drag 0.0084 at a lift coefficient of 0.8) and against the
maximum lift coefficient of 1.62 printed on Figure 8-74; `airfoil_comparison` checks the
1.62 and the 1.69 printed on the figure for the two airfoils. The NACA 23015 curves are not
checked against Table 8-9, and they differ from it (the table lists a maximum lift
coefficient of 1.72 and a drag coefficient of 0.0072 at lift coefficients of 0 and 0.8).

`gudmundsson-fig-10-9.json`: the lift curves of a Clark Y wing model with and without a
fixed slot at a Reynolds number of 0.63 million (Weick and Wenzinger 1933, NACA Report 407),
read the same way from Gudmundsson (2022), Figure 10-9. The peaks reproduce the values
printed on that figure (1.297 and 1.751) within 0.01.

The NACA 4-digit and 5-digit sections are not stored here: `make_aero_figures.py`
computes them from the NACA equations (`naca4`, `naca230`).
