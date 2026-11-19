---
title: "Carpet plots, part 2: A third variable, checks, and sensitivities"
short_title: Third variable and sensitivities
---

This is the second part of Lecture 12, *Carpet Plots and Sensitivity Analysis*. It adds a third design variable, lists the checks and the common mistakes, computes the sensitivities at the lightest feasible point, and sets out your team's {term}`carpet plot`. The example and the six steps are in [](carpet-plot.md).

:::{note} What to take from this lecture
- A third design variable, such as the aspect ratio, takes one {term}`sizing matrix` per value and a fit of the lightest feasible $W_{TO}$ against that variable.
- Check the runs and the crossings before you report the plot. Report the {term}`lightest feasible point` with its active constraints and margins.
- The sensitivities at that point show which variable or input moves $W_{TO}$ most.
:::

## A third variable: aspect ratio

1. Choose three aspect ratios. The example uses 4, 5, and 6.
2. Repeat steps 1 to 5 of [part 1](carpet-plot.md) at each: nine runs, a {term}`sizing plot`, and a lightest feasible point.
3. Plot the lightest feasible $W_{TO}$ against $AR$, fit a quadratic, and read the minimum.
4. Run the matrix at that $AR$, build its carpet plot, and rerun its lightest feasible point.

The study takes 27 matrix runs, plus nine at the chosen $AR$.

:::{figure} figures/aspect-ratio-study.svg
:label: fig-aspect-ratio-study
:alt: Four small panels; the weight axes carry no scale. Three of them are sizing plots, takeoff weight against wing loading, at aspect ratios of 4, 5, and 6. Each has three curves of thrust-to-weight ratio, 0.9 dashed, 1.0 solid, and 1.1 dash-dot, from bottom to top; three solid black constraint lines with ticks on the failing side; and a shaded feasible region inside the matrix, below the 1.1 curve. At an aspect ratio of 4 the region is a narrow strip at the high wing-loading end. At 5 it is larger and reaches lowest. At 6 it spans most of the matrix from the low wing-loading end. The fourth panel plots the lightest feasible takeoff weight against aspect ratio, with ticks at 4, 5, and 6, one cross at each, and a quadratic through them. The cross at 5 is the lowest, the cross at 6 the highest, and the curve has its minimum just below 5.
:width: 100%

A third variable on a published example, a fighter: sizing plots at three aspect ratios and the lightest feasible $W_{TO}$ against $AR$. Schematic, shapes only; the values are not those of [part 1](carpet-plot.md). Solid black: constraint lines, with ticks on the failing side. Curves, bottom to top: $T_{SL}/W_{TO}$ = 0.9, 1.0, and 1.1. Crosses: the lightest feasible $W_{TO}$ at each $AR$. Shaded: feasible, inside the matrix. After Raymer (2012), Section 19.4.
:::

## Checks and common mistakes

### Checks before reporting

- The center run matches the earlier converged run of the sizing code at the design point.
- All nine runs converged.
- Each constraint is computed at its own weight, altitude, speed, and {term}`rating`, as on the {term}`constraint diagram`.
- Every {term}`crossing` read lies inside the matrix.
- The rerun of the lightest feasible point meets every {term}`limit`.

:::{warning} Common mistakes
- A crossing extrapolated beyond the runs. Add a run.
- The best of the nine runs reported as the answer. The lightest feasible point lies between the runs; read it off the plot and rerun it.
- The carpet-plot abscissa read as wing loading. Read $W_{TO}/S$ from the lines of the grid.
- Marks not shifted with their curve. Shift every {term}`mark` with {eq}`eq-carpet-offset` of [part 1](carpet-plot.md).
- The lightest feasible point reported without its active constraints and margins.
- A {term}`fixed engine` treated as a {term}`rubber engine`. With a fixed engine $T_{SL}$ is fixed, and $T_{SL}/W_{TO}$ follows from $W_{TO}$; it is not a free variable.
:::

An active constraint closes the {term}`feasible region` at the lightest feasible point, as an {term}`active boundary` does at the design point of [Lecture 9](../lecture-09/trainer-boundaries.md). The active constraint has no margin at the lightest feasible point. In the example the takeoff constraint is active. The others are reported with their margins to the limit: $P_s$ = 217 ft/s against 0 ft/s, and an acceleration time of 47.3 s against 50 s.

## Sensitivities at the lightest feasible point

Let $x$ be a design variable or an input of the sizing code, and $h$ a small step in it, about 2% of $x$. The derivative of $W_{TO}$ by central difference is

:::{math}
:label: eq-sens-derivative
\frac{\partial W_{TO}}{\partial x} \approx \frac{W_{TO}(x + h) - W_{TO}(x - h)}{2h}
:::

and the {term}`sensitivity` is the derivative normalized by $x$ and $W_{TO}$:

:::{math}
:label: eq-sens-normalized
s_x = \frac{x}{W_{TO}}\,\frac{\partial W_{TO}}{\partial x}
:::

$s_x$ is the percent change in $W_{TO}$ per percent change in $x$. With $s_x$ = 2, 1% more $x$ gives 2% more $W_{TO}$.

At the lightest feasible point of the example, from the fitted matrix with 2% steps:

- $W_{TO}/S$: $\partial W_{TO}/\partial(W_{TO}/S) \approx -481$ lb per lb/ft², and $s_x$ = −0.58.
- $T_{SL}/W_{TO}$: $\partial W_{TO}/\partial(T_{SL}/W_{TO}) \approx$ 56,300 lb per unit, and $s_x$ = 1.24.
- Along the takeoff line the two effects cancel at the point, and $W_{TO}$ stays within 200 lb from 53 to 60 lb/ft². The minimum along the line is flat.

For the other inputs, rerun the sizing code:

1. Change one input at a time by ±2%: TSFC, $C_{D_0}$, a factor on the empty weight, payload, and range.
2. Halve the step and check that $s_x$ does not change.
3. Rank the inputs by $|s_x|$.

:::{iframe} ../quickcheck/sensitivity.html
:label: qc-sensitivity
:width: 100%

Quick check: the derivative by central difference, {eq}`eq-sens-derivative`, and the sensitivity, {eq}`eq-sens-normalized`, from three runs of an invented aircraft. Shuffle gives new values; the solution shows the steps.
:::

:::{admonition} Navy Jet Trainer
:class: navy

A sensitivity holds at the point where it was taken. At which point do you report each sensitivity, and which input of your sizing code has the largest $|s_x|$ there?
:::

## Your team's carpet plot

- **Measure of merit**: the takeoff weight, or the cost.
- **Variables**: $W_{TO}/S$ and $T_{SL}/W_{TO}$. Add a third variable with the study of {numref}`fig-aspect-ratio-study`.
- **Constraints**: those of your constraint diagram, computed by the sizing code: the maximum operating speed, the specific excess power, the sustained load factor, the takeoff distance, the critical field length, and the landing distance of [Lecture 9](../lecture-09/trainer-boundaries.md).
- **Report**: the matrix, the {term}`cross-plots <cross-plot>`, the carpet plot, the lightest feasible point with its active constraints and margins, and the rerun.

:::{admonition} Navy Jet Trainer
:class: navy

The maximum operating speed, the specific excess power, and the sustained load factor each have a threshold and an objective ({numref}`tbl-rfp-performance` in [](../navy-rfp/navy-rfp.md)). If you add the objective values as a second set of limits, which constraint lines move, and how far does the lightest feasible point move with them?
:::

:::{important} Summary
- A carpet plot shows the takeoff weight over a grid of two design variables, with the constraint lines drawn on it.
- The lightest feasible point lies between the runs. Rerun it.
- Report its active constraints, margins, and sensitivities.
:::

:::{exercise} For discussion
:label: ex-carpet-plot

In the example the takeoff line closes the region at the lightest feasible point, and the acceleration time there is 47.3 s against a limit of 50 s. If the acceleration limit were tighter, which constraint line would close the region near the point, and would the point move up or down the grid? Along the takeoff line $W_{TO}$ stays within 200 lb from 53 to 60 lb/ft². What would you use to choose a point on that flat stretch? With a fixed engine, which points of the carpet plot can the aircraft reach?
:::

:::{seealso} Reading
Raymer (2012), Section 19.4; Gudmundsson (2022), Section 3.3.1; and ESDU Data Item 04008.
:::

## Quiz

:::{iframe} ../quickcheck/quiz-lecture-12.html
:label: quiz-lecture-12
:width: 100%

Quiz on Lecture 12: eight questions, one at a time, with the explanation after each answer. It is not graded and nothing is recorded.
:::

## References

- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 5th ed., AIAA Education Series, 2012. Section 19.4: the sizing matrix, the fighter example, the constraint cross-plots, and carpet plots.
- Gudmundsson, S., *General Aviation Aircraft Design: Applied Methods and Procedures*, 2nd ed., Butterworth-Heinemann, 2022. Section 3.3.1: parametric analysis, the nine-point analysis, and carpet plots.
- ESDU, *Use of Carpet Plots to Represent Functions of Two Variables*, Data Item 04008. Carpet plots, and lattice plots for three variables.
- AIAA 2026-27 Undergraduate Team Aircraft Design Competition RFP, *Design of a Navy Jet Training Aircraft*; see [](../navy-rfp/navy-rfp.md).
