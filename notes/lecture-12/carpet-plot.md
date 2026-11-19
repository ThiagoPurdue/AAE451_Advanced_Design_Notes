---
title: "Carpet plots, part 1: The idea and the six steps"
short_title: The carpet plot in six steps
---

This is the first part of Lecture 12, *Carpet Plots and Sensitivity Analysis*. The lecture has two parts. This page states the question a carpet plot answers, shows how to read a finished one, and builds it in six steps from nine runs of the sizing code. The second part, [](third-variable-and-sensitivities.md), adds a third design variable, the checks and the common mistakes, the sensitivities, and your team's carpet plot.

The nine sizing runs come from a published example, the fighter sizing study of Raymer (2012), Section 19.4; the curves, crossings, lightest feasible point, and sensitivities on these pages are computed from them. No number on these pages is computed for the Navy Jet Trainer.

:::{note} What to take from this lecture
- The {term}`constraint diagram` gives the feasible wing loading and thrust-to-weight ratio. It does not give the takeoff weight. A {term}`carpet plot` shows the takeoff weight over a grid of the two, with the constraints drawn on it.
- Six steps build the plot from nine converged runs of the sizing code: the matrix, the sizing plot, the cross-plots, the marks, the lightest feasible point, and the offset.
- The lightest feasible point usually lies between the runs. Read it off the plot, then rerun the sizing code there.
:::

## The question a carpet plot answers

:::{figure} figures/question-constraint-axes.svg
:label: fig-carpet-question
:alt: Thrust-to-weight ratio, 0.9 to 1.1, against wing loading, 50 to 70 pounds per square foot. Nine dots, one per sizing run, each labeled with its takeoff weight in thousands of pounds. At a thrust-to-weight ratio of 0.9 the labels are 43.5, 39.0, and 36.0 at wing loadings of 50, 60, and 70; at 1.0 they are 48.5, 43.7, and 41.0; at 1.1 they are 56.0, 49.0, and 45.0. Three constraint lines carry ticks on the failing side: the takeoff line rises from the left edge of the grid to its top edge, the specific excess power line rises from the bottom edge to the right edge, and the acceleration line falls from left to right. The feasible region is shaded above the takeoff and acceleration lines, below 1.1, and right of a wing loading of 50. The runs labeled 56.0 and 49.0 lie on its edge, and their labels are bold; the other seven lie outside it.
:width: 80%

Nine sizing runs of a published example, a fighter, on the axes of the constraint diagram, with the takeoff weight of each run in 1,000 lb; bold: the two runs that meet all three limits. Runs from Raymer (2012), Section 19.4; constraint lines computed from them.
:::

- The constraint diagram of [Lecture 9](../lecture-09/constraint-method.md) gives the feasible $W_{TO}/S$ and $T_{SL}/W_{TO}$. It does not show $W_{TO}$.
- The sizing code does. Run it at nine points on the same axes; {numref}`fig-carpet-question` labels each dot with its $W_{TO}$ in 1,000 lb. The constraint lines, the boundaries of Lecture 9, come from those runs.
- Two runs meet every constraint: 56,000 lb and 49,000 lb, the bold labels.
- The {term}`lightest feasible point` lies between the runs. The carpet plot finds it.

:::{admonition} Navy Jet Trainer
:class: navy

Item 1 of the performance data the RFP requires is the trade study results that find the minimum weight aircraft ({numref}`tbl-rfp-performance-data` in [](../navy-rfp/navy-rfp.md)). Which two design variables does your {term}`trade study` vary, and which requirements does it carry as constraints?
:::

## Reading a carpet plot

:::{prf:definition} Carpet plot
:label: def-carpet-plot

A {term}`carpet plot` shows the takeoff weight $W_{TO}$ over a grid of the wing loading $W_{TO}/S$ and the thrust-to-weight ratio $T_{SL}/W_{TO}$, with the constraint lines drawn on it. Each node of the grid is one sizing run.
:::

:::{prf:definition} Curve and line
:label: def-curve-line

On the sizing plot (step 2) and the carpet plot, a curve joins the runs of constant $T_{SL}/W_{TO}$, and a line joins the runs of constant $W_{TO}/S$.
:::

:::{figure} figures/carpet-plot.svg
:label: fig-carpet-plot
:alt: The finished carpet plot of the example. The vertical axis is takeoff weight, labeled from 35,000 to 55,000 pounds; there is no horizontal axis. Three curves of constant thrust-to-weight ratio, 0.9, 1.0, and 1.1, run down to the right, each shifted to the right of the one below it. Three gray lines of constant wing loading, 50, 60, and 70 pounds per square foot, join the runs into a grid, and the nine runs are open circles at its nodes. The takeoff, specific excess power, and acceleration constraint lines cross the grid with ticks on the failing side. The feasible region is shaded at the top of the grid. A diamond at its lowest point, on the takeoff line, marks the lightest feasible point: 46,300 pounds, 56 pounds per square foot, and a thrust-to-weight ratio of 1.017.
:width: 85%

The carpet plot of a published example, a fighter, with $W_{TO}/S$ in lb/ft². Runs from Raymer (2012), Section 19.4; curves, constraint lines, and the lightest feasible point computed from them. The steps below build this plot.
:::

- Each curve is shifted sideways to open the grid, so only the vertical axis has a scale; step 6 shows how.
- The lowest point that no constraint cuts off is the lightest feasible point. Read its $W_{TO}$, $W_{TO}/S$, and $T_{SL}/W_{TO}$ off the grid.

## The example and the six steps

:::{table} A published example: a fighter sizing study. After Raymer (2012), Section 19.4.
:label: tbl-carpet-example

| Item | Fighter sizing study |
| --- | --- |
| {term}`Measure of merit` | Takeoff weight $W_{TO}$, minimized |
| Variables | Wing loading $W_{TO}/S$; thrust-to-weight ratio $T_{SL}/W_{TO}$ |
| Constraints | Takeoff distance at most 500 ft; $P_s \ge 0$ at Mach 0.9, 5 g, and 30,000 ft; acceleration from Mach 0.9 to 1.5 in at most 50 s |
| Held fixed | Aspect ratio, sweep, taper, $C_{L_{max}}$, and the mission |

:::

:::{prf:definition} Limit
:label: def-limit

The {term}`limit` of a constraint is its required value: 500 ft, 0 ft/s, and 50 s in {numref}`tbl-carpet-example`.
:::

The six steps:

1. Run the sizing matrix.
2. Draw the sizing plot.
3. Cross-plot each constraint and read the crossings.
4. Mark the crossings on the sizing plot.
5. Read the lightest feasible point and rerun it.
6. Offset the curves: the carpet plot.

:::{admonition} Navy Jet Trainer
:class: navy

Your constraints are those of your own constraint diagram: the maximum operating speed, the specific excess power, the sustained load factor, the takeoff distance, the critical field length, and the landing distance of [Lecture 9](../lecture-09/trainer-boundaries.md). Does your sizing code compute each one at the weight and altitude the RFP states? At which rating?
:::

## Step 1: run the sizing matrix

1. Center the matrix on the {term}`design point` chosen from the constraint diagram.
2. Take three values of each variable, 10% to 20% apart. The nine combinations are the {term}`sizing matrix`.
3. Converge the sizing code at all nine combinations.
4. Record $W_{TO}$ and the value of every constraint for each run.

In the example the center is $W_{TO}/S$ = 60 lb/ft² and $T_{SL}/W_{TO}$ = 1.0, with steps of 10 lb/ft² and 0.1.

:::{table} The sizing matrix of a published example, a fighter: nine converged runs. Values in bold miss their limit: a takeoff distance above 500 ft, a $P_s$ below 0 ft/s, or an acceleration time above 50 s. The last column names the two runs that meet all limits. Runs from Raymer (2012), Section 19.4.
:label: tbl-sizing-matrix

| $T_{SL}/W_{TO}$ | $W_{TO}/S$ (lb/ft²) | $W_{TO}$ (lb) | Takeoff distance (ft) | $P_s$ (ft/s) | Acceleration time (s) | Meets all limits |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0.9 | 50 | 43,500 | **670** | 140 | **56** | no |
| 0.9 | 60 | 39,000 | **810** | **−230** | **53** | no |
| 0.9 | 70 | 36,000 | **1,070** | **−320** | **51** | no |
| 1.0 | 50 | 48,500 | 450 | 430 | **50.5** | no |
| 1.0 | 60 | 43,700 | **595** | 30 | 47 | no |
| 1.0 | 70 | 41,000 | **800** | **−190** | 45 | no |
| 1.1 | 50 | 56,000 | 340 | 700 | 46 | yes |
| 1.1 | 60 | 49,000 | 430 | 330 | 42 | yes |
| 1.1 | 70 | 45,000 | **660** | 30 | 39 | no |

:::

The sizing code is more detailed than the constraint diagram. Here the center run, chosen from the diagram, misses the takeoff limit: 595 ft against 500 ft.

:::{admonition} Navy Jet Trainer
:class: navy

How far apart do you space the three values of each variable, and does every run of your matrix converge?
:::

## Step 2: draw the sizing plot

1. Plot $W_{TO}$ against $W_{TO}/S$.
2. Draw one curve per $T_{SL}/W_{TO}$ through its three runs. The example fits a quadratic.
3. Join the runs of equal $W_{TO}/S$ with three lines. Curves and lines together are the {term}`sizing plot`.

:::{figure} figures/sizing-plot.svg
:label: fig-sizing-plot
:alt: Takeoff weight against wing loading, 50 to 70 pounds per square foot. Three curves, one per thrust-to-weight ratio, each through three runs drawn as open circles. At a thrust-to-weight ratio of 1.1 the runs are 56,000, 49,000, and 45,000 pounds at wing loadings of 50, 60, and 70; at 1.0 they are 48,500, 43,700, and 41,000; at 0.9 they are 43,500, 39,000, and 36,000. All three curves fall as the wing loading rises, and the curve of higher thrust-to-weight ratio lies higher. Three gray vertical lines at 50, 60, and 70 join the runs of equal wing loading.
:width: 80%

The sizing plot of a published example, a fighter: the nine runs of {numref}`tbl-sizing-matrix`, with the quadratic through the three runs of each $T_{SL}/W_{TO}$. Values from Raymer (2012), Section 19.4.
:::

- In the example, higher $W_{TO}/S$ gives a smaller wing and a lower $W_{TO}$.
- Higher $T_{SL}/W_{TO}$ gives a larger engine, more fuel, and a higher $W_{TO}$.

## Step 3: cross-plot each constraint

:::{prf:definition} Crossing
:label: def-crossing

A {term}`crossing` is the point where a curve or a line meets the limit of a constraint.
:::

1. For each constraint, plot its value against $W_{TO}/S$, one curve per $T_{SL}/W_{TO}$ through its three runs. This is a {term}`cross-plot`.
2. Draw the limit. Shade the side where the constraint fails.
3. Read the crossings: the $W_{TO}/S$ at which each curve meets the limit. Read them inside the matrix only.
4. Repeat against $T_{SL}/W_{TO}$, one line per $W_{TO}/S$, to read the crossings on the $W_{TO}/S$ lines.

:::{figure} figures/cross-plots.svg
:label: fig-cross-plots
:alt: Four panels, each with a dotted limit, a gray band on the failing side, and filled dots at the crossings. Takeoff distance against wing loading, limit 500 feet: the 1.0 curve crosses at 53.9 pounds per square foot and the 1.1 curve at 63.8; the 0.9 curve fails everywhere. Specific excess power against wing loading, limit 0: the 0.9 curve crosses at 53.0 and the 1.0 curve at 61.0; the 1.1 curve passes everywhere. Acceleration time against wing loading, limit 50 seconds: only the 1.0 curve crosses, at 51.2; the 0.9 curve fails and the 1.1 curve passes. Takeoff distance against thrust-to-weight ratio, one line per wing loading: the 50 line crosses at 0.972 and the 60 line at 1.054; the 70 line fails everywhere.
:width: 100%

Cross-plots of a published example, a fighter. Three panels against $W_{TO}/S$ in lb/ft², one curve per $T_{SL}/W_{TO}$; the fourth, takeoff distance against $T_{SL}/W_{TO}$, one line per $W_{TO}/S$. Gray band: the constraint fails. Filled dots: the crossings. Runs from Raymer (2012), Section 19.4; curves and crossings computed from them, each curve the quadratic through three runs.
:::

A curve with no crossing inside the matrix passes everywhere or fails everywhere. In {numref}`fig-cross-plots` the 0.9 curve fails the takeoff limit at every wing loading, and the 1.1 curve passes the $P_s$ limit at every one.

:::{warning}
Do not extrapolate a crossing beyond the runs. If the lowest point of the feasible region falls on an edge of the matrix, extend the matrix past that edge with new runs.
:::

## Step 4: mark the crossings on the sizing plot

:::{prf:definition} Mark
:label: def-mark

A {term}`mark` is a crossing drawn on the sizing plot. The marks of one constraint, joined, form its constraint line.
:::

1. For a crossing on a curve, put the mark on that curve at the crossing's $W_{TO}/S$. Mark **a** in {numref}`fig-marked-sizing-plot`: takeoff, the 1.0 curve, 53.9 lb/ft².
2. For a crossing on a line, fit $W_{TO}$ against $T_{SL}/W_{TO}$ through the three runs of that line and read $W_{TO}$ at the crossing's $T_{SL}/W_{TO}$. Put the mark on the line at that weight. Mark **b**: takeoff, the 50 lb/ft² line, 0.972, which gives 46,900 lb.
3. Join the marks of each constraint and tick the failing side of the line.

:::{table} The crossings of a published example, a fighter, read inside the matrix. On a curve the crossing is a $W_{TO}/S$ in lb/ft², read from the first three panels of {numref}`fig-cross-plots`. On a line it is a $T_{SL}/W_{TO}$: the last panel shows the takeoff crossings, and the $P_s$ and acceleration crossings are read the same way from cross-plots not drawn here. "none": no crossing inside the matrix. Runs from Raymer (2012), Section 19.4; crossings computed from them with the quadratic through three runs.
:label: tbl-crossings

| Curve or line | Crossing read as | Takeoff | $P_s$ | Acceleration |
| --- | --- | ---: | ---: | ---: |
| Curve $T_{SL}/W_{TO}$ = 0.9 | $W_{TO}/S$ (lb/ft²) | none | 53.0 | none |
| Curve $T_{SL}/W_{TO}$ = 1.0 | $W_{TO}/S$ (lb/ft²) | 53.9 | 61.0 | 51.2 |
| Curve $T_{SL}/W_{TO}$ = 1.1 | $W_{TO}/S$ (lb/ft²) | 63.8 | none | none |
| Line $W_{TO}/S$ = 50 lb/ft² | $T_{SL}/W_{TO}$ | 0.972 | none | 1.010 |
| Line $W_{TO}/S$ = 60 lb/ft² | $T_{SL}/W_{TO}$ | 1.054 | 0.989 | 0.948 |
| Line $W_{TO}/S$ = 70 lb/ft² | $T_{SL}/W_{TO}$ | none | 1.088 | 0.917 |

:::

:::{figure} figures/marked-sizing-plot.svg
:label: fig-marked-sizing-plot
:alt: The sizing plot of the example, takeoff weight against wing loading from 50 to 70 pounds per square foot, with the three thrust-to-weight curves and the three gray wing-loading lines. Filled dots mark the crossings, and three constraint lines join them, with ticks on the failing side. The takeoff line runs nearly level from 46,900 pounds on the wing-loading line of 50 to the 1.1 curve at 63.8 pounds per square foot. The specific excess power line runs from the 0.9 curve at 53.0 to the 70 line near 44,600 pounds. The acceleration line falls steeply from the 50 line near 49,100 pounds to the 70 line near 36,900 pounds. Two circled marks are labeled: a, on the 1.0 curve at 53.9 pounds per square foot, and b, on the 50 line at 46,900 pounds.
:width: 80%

The sizing plot of a published example, a fighter, with the marks, the three constraint lines, and the ticks on the failing side. Mark **a** is a crossing on a curve and mark **b** a crossing on a line. Runs from Raymer (2012), Section 19.4; crossings and constraint lines computed from them.
:::

The example draws each constraint line where the fit of that constraint equals its limit, and reads $W_{TO}$ from the same fit. Straight segments between the marks put the lowest point at mark **a**, 46,400 lb at 53.9 lb/ft²: nearly the same weight at a different wing loading. A fit other than the quadratic moves a crossing by up to about 1 lb/ft².

## Step 5: read the lightest feasible point

1. Find the feasible side of each constraint line. A constraint that eases with thrust, as all three of the example do, is feasible on the side of higher $T_{SL}/W_{TO}$, above the line. A constraint set by the wing loading alone, such as the landing distance, is feasible on the side of lower $W_{TO}/S$.
2. Shade the region that all the constraints allow: the {term}`feasible region`.
3. Read the lowest shaded point: its $W_{TO}$, $W_{TO}/S$, and $T_{SL}/W_{TO}$. This is the {term}`lightest feasible point`.
4. Rerun the sizing code there and check that the rerun meets every limit.

:::{figure} figures/lightest-feasible-point.svg
:label: fig-lightest-feasible
:alt: The sizing plot of the example with its three constraint lines and the feasible region shaded. The region lies above the takeoff and acceleration lines, below the 1.1 curve, and to the right of the 50 line. A diamond at the lowest point of the region, on the takeoff line, marks the lightest feasible point: 46,300 pounds at 56 pounds per square foot and a thrust-to-weight ratio of 1.017. The specific excess power line lies below the region.
:width: 80%

The feasible region and the lightest feasible point of a published example, a fighter, on the sizing plot: 46,300 lb at 56 lb/ft² and $T_{SL}/W_{TO}$ = 1.017, on the takeoff line. Runs from Raymer (2012), Section 19.4; the region and the point computed from them.
:::

- Takeoff is stricter than $P_s$ everywhere in the matrix, so $P_s$ never closes the region.
- The lowest shaded point is 46,300 lb at 56 lb/ft² and $T_{SL}/W_{TO}$ = 1.017, on the takeoff line.
- It is 2,700 lb lighter than the best single run, 49,000 lb.
- At the diamond $P_s$ = 217 ft/s and the acceleration time is 47.3 s.
- The matrix edges, not constraints, close the region at $T_{SL}/W_{TO}$ = 1.1 and at 50 lb/ft². $W_{TO}$ rises toward both edges, so no run is added outside them.

:::{tip}
The plot interpolates between runs; only the rerun is a converged design.
:::

## Step 6: offset the curves

1. Shift each $T_{SL}/W_{TO}$ curve to the right by a fixed step per curve, the {term}`offset`. The step is arbitrary, except that it must differ from the spacing of the $W_{TO}/S$ values, or runs of different curves share an abscissa; the example uses 6 lb/ft².
2. Join the runs of equal $W_{TO}/S$. These are the lines of the grid.
3. Shift every mark the same way, with {eq}`eq-carpet-offset`. Join the marks, tick the failing side, and shade the feasible region.
4. Delete the horizontal axis. It no longer reads as $W_{TO}/S$.

The abscissa of a run or a mark on the carpet plot is

:::{math}
:label: eq-carpet-offset
\xi = \frac{W_{TO}}{S} + k\left[\frac{T_{SL}}{W_{TO}} - \left(\frac{T_{SL}}{W_{TO}}\right)_{1}\right]
:::

where $(T_{SL}/W_{TO})_1$ is the lowest value of the matrix and $k$ the shift per unit of $T_{SL}/W_{TO}$. In the example $(T_{SL}/W_{TO})_1$ = 0.9 and $k$ = 60 lb/ft²: the 0.9 curve stays in place, the 1.0 curve moves 6 lb/ft² to the right, and the 1.1 curve 12 lb/ft².

:::{figure} figures/offset-curves.svg
:label: fig-offset-curves
:alt: Two panels with takeoff weight on the vertical axis. Left, the three thrust-to-weight curves against wing loading plus the offset. The 0.9 curve stays in place. The 1.0 curve is shifted 6 pounds per square foot to the right and the 1.1 curve 12, with arrows labeled plus 6 and plus 12; dotted copies show the 1.0 and 1.1 curves before the shift. Right, the finished carpet plot with no horizontal axis: the shifted curves, the gray lines of wing loading 50, 60, and 70 joining the runs, the three constraint lines with their marks and ticks, the shaded feasible region, and a diamond at the lightest feasible point.
:width: 100%

Step 6 on a published example, a fighter. Left: the curves before (dotted) and after the shift. Right: the carpet plot, with both variables read from the grid and neither from an axis. Same data as {numref}`fig-lightest-feasible`: runs from Raymer (2012), Section 19.4; curves, constraint lines, and the lightest feasible point computed from them.
:::

The offset moves only the abscissa. The diamond and the weights are those of step 5.

:::{warning}
The abscissa of the carpet plot is not the wing loading. Read $W_{TO}/S$ from the lines of the grid, and shift every mark with its curve.
:::

:::{seealso}
Continue with [](third-variable-and-sensitivities.md): a third design variable, the checks and the common mistakes, the sensitivities at the lightest feasible point, and your team's carpet plot. The references for both parts are at the end of that page.
:::
