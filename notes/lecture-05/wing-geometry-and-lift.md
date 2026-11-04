---
title: "Aerodynamics, part 2: Wing geometry and lift"
short_title: Wing geometry and lift
---

This is the second part of Lecture 5, *Aerodynamics: Airfoil and Wing*. It covers the planform and what each of its choices costs: area, aspect ratio, taper, sweep, twist, and incidence. It then builds the lift model: lift-curve slope, clean maximum lift, and stall speed. The first part, [](airfoil.md), covers the airfoil.

:::{note} What to take from this lecture
- The wing area follows from the takeoff weight and the ASORT wing loading. Everything else is a choice with a cost.
- Thickness, sweep, and airfoil type set the drag divergence Mach number together.
- The lift-curve slope and the clean maximum lift come from the airfoil data and the planform, with a cited method.
- Maximum lift sets the stall speed. Check every speed-linked requirement.
:::

## Planform from S, AR, and λ

With the area $S$, the {term}`aspect ratio` $AR$, and the {term}`taper ratio` $\lambda$, the planform of [the nomenclature figure](#fig-wing-planform) follows:

:::{math}
:label: eq-planform
\begin{aligned}
b &= \sqrt{AR\,S} \\
c_r &= \frac{2S}{b\,(1+\lambda)}, \qquad c_t = \lambda\,c_r \\
c_{MGC} &= \frac{2}{3}\,c_r\,\frac{1+\lambda+\lambda^{2}}{1+\lambda} \\
y_{MGC} &= \frac{b}{6}\,\frac{1+2\lambda}{1+\lambda}, \qquad x_{MGC} = y_{MGC}\tan\Lambda_{LE} \\
\tan\Lambda_{c/4} &= \tan\Lambda_{LE} + \frac{c_r}{2b}\,(\lambda-1)
\end{aligned}
:::

The subsonic aerodynamic center sits near the quarter chord of the mean geometric chord. The CG range is placed against it.

:::{admonition} Navy Jet Trainer
:class: navy

$S$ follows from the converged takeoff weight and the ASORT wing loading. Every value goes into ASORT.
:::

## Wing volume

The airfoil area, with the maximum thickness at $k\,c$ from the leading edge:

:::{math}
:label: eq-section-area
A = \frac{k+3}{6}\left(\frac{t}{c}\right)c^{2}
:::

Between two stations $\Delta y$ apart with chords $c_1$ and $c_2$, linear taper, and constant $t/c$:

:::{math}
:label: eq-wing-volume
V = \frac{k+3}{18}\left(\frac{t}{c}\right)\Delta y\left(c_1^{2}+c_1c_2+c_2^{2}\right)
:::

The formula takes the whole airfoil; count only the part between the spars. 1 US gal = 231 in³. Airfoil area from Gudmundsson (2022), Eq. 9-35; the volume is that equation integrated along the span.

:::{admonition} Navy Jet Trainer
:class: navy

A04 Deliverable 4: required fuel volume against available volume, with the wing the airfoil thickness now defines.
:::

## Wing height

:::{figure} figures/wing-height.svg
:label: fig-wing-height
:alt: Two front views of a fuselage circle with a fin, one with the wing bar above the fuselage center and one with it below, each with the ground line and an arrow h from the ground to the wing.
:width: 70%

High and low wing, front view, with the wing height $h$ above the ground.
:::

::::{grid} 1 1 2 2

:::{card}
:header: High wing
- More dihedral effect: laterally more stable.
- More wing lift, lower stall speed.
- Costs: less ground effect at takeoff and landing, more frontal area, wing downwash on the tail, less roll control.
:::

:::{card}
:header: Low wing
- Ground effect shortens the takeoff.
- Less frontal area, less downwash on the tail, more roll control.
- Costs: less dihedral effect, less wing lift, a higher stall speed, and a longer landing in ground effect.
:::

::::

:::{admonition} Navy Jet Trainer
:class: navy

Wing height comes with your configuration. It also changes the lift model.
:::

## Aspect ratio

:::{figure} figures/aspect-ratio-effects.svg
:label: fig-aspect-ratio
:alt: Two plots for aspect ratios 4, 8, and 16. Left, wing lift coefficient against angle of attack: three straight lines, steeper for higher aspect ratio. Right, wing lift coefficient against drag coefficient: three polars, the aspect ratio 4 polar bending far to the right at high lift and the aspect ratio 16 polar staying close to the minimum drag.
:width: 100%

The effect of aspect ratio, computed from the lift-curve slope equation {eq}`eq-lift-curve-slope` and $C_D = C_{D_0} + C_L^{2}/(\pi e\,AR)$ with example values $C_{D_0}$ = 0.02 and $e$ = 0.85.
:::

::::{grid} 1 1 2 2

:::{card}
:header: High AR
- Low induced drag, high $(L/D)_{max}$.
- Costs: wing weight, roll damping, flutter, less volume.
:::

:::{card}
:header: Low AR
- Light, stiff, fast roll, high $\alpha_{stall}$.
- Costs: induced drag, shallow $C_{L_\alpha}$.
:::

::::

Typical values: fighters 2.5 to 4, aerobatic aircraft 5 to 6, general aviation 6 to 11, jetliners 7 to 10, twin commuters 10 to 14 (Gudmundsson 2022, Tables 9-3 and 9-4). The horizontal tail gets an aspect ratio below the wing's, so the tail stalls after the wing.

:::{admonition} Navy Jet Trainer
:class: navy

Sustained g is paid for in induced drag. What does the +4.0 g (T) to +6.0 g (O) range at 15,000 ft ask of the aspect ratio?
:::

## Taper ratio

:::{figure} figures/taper-lift-distribution.svg
:label: fig-taper
:alt: Normalized lift per unit span against spanwise station for taper ratios 1.0, 0.5, and 0.3, with the elliptical distribution as a thin line. The untapered wing carries more lift at the tip than the ellipse; the 0.3 taper lies closest to the ellipse over most of the span and overshoots it only at the root; the 0.5 taper sits between.
:width: 80%

Spanwise lift distribution of straight tapered wings by Schrenk's approximation, against the elliptical distribution. Lift per unit span; divided by the local chord, the section lift coefficient of the 0.3 wing rises toward the tip, which is the tip loading the table refers to. Computed.
:::

:::{table} What each taper ratio does. After Gudmundsson (2022), Table 9-5.
:label: tbl-taper

| $\lambda$ | Effect |
| ---: | --- |
| 1.0 | Stall starts at the root. Simple to build. High induced drag and bending moment. |
| 0.5 | Balances induced drag against stall behavior. Moderate washout. |
| 0.3 | Near-elliptical loading. Tip loaded, so large washout. The lowest usable value. |

:::

Taper lowers the root bending moment and the roll inertia.

## Sweep

:::{figure} figures/sweep-components.svg
:label: fig-sweep-components
:alt: Top view of a swept wing panel with a dashed sweep line along it. The free-stream velocity arrow points along the flight direction and is resolved into a component normal to the sweep line, labeled V infinity cos Lambda, which sets the pressures, and a component along the sweep line, labeled V infinity sin Lambda. The sweep angle Lambda is marked at the root.
:width: 70%

The free stream resolved along and normal to the sweep line. After Nicolai and Carichner (2010), Figure 2.21.
:::

- The component normal to the sweep line, $V_\infty \cos\Lambda$, sets the pressures.
- Simple sweep theory: $M_{crit}$ rises by $1/\cos\Lambda$. This is the upper bound.
- Costs: lower $C_{L_\alpha}$ and $C_{L_{max}}$, tip stall, pitch-up, wing weight.
- Two reasons to sweep: flight above about Mach 0.65, or the CG position.

:::{admonition} Navy Jet Trainer
:class: navy

Relate sweep and $t/c$ to Mach 0.78 and Mach 0.90.
:::

## Drag divergence of the swept wing

Normal to the sweep line:

:::{math}
:label: eq-sweep-normal
M_N = M\cos\Lambda, \qquad C_{L_N} = \frac{C_L}{\cos^{2}\Lambda}, \qquad \left(\frac{t}{c}\right)_{N} = \frac{t/c}{\cos\Lambda}
:::

The Korn relation for the wing, with $\Lambda$ the sweep of the mid-chord line:

:::{math}
:label: eq-korn-wing
M_{DD} = \frac{\kappa}{\cos\Lambda} - \frac{t/c}{\cos^{2}\Lambda} - \frac{C_L}{10\cos^{3}\Lambda}, \qquad M_{crit} = M_{DD} - 0.108
:::

$\kappa$ = 0.87 for a conventional airfoil and 0.95 for a supercritical one (Gudmundsson 2022, Eqs. 16-95 to 16-106). Gudmundsson writes $M_{DD}$ for the wing and $M_{dd}$ for the airfoil; the notes follow him.

:::{figure} figures/korn-sweep.svg
:label: fig-korn-sweep
:alt: Drag divergence Mach number against mid-chord sweep from 0 to 45 degrees. Three rising curves for conventional airfoils with thickness ratios 0.08, 0.10, and 0.12, the thinner airfoil higher, from about 0.75 at zero sweep to above 0.9 at 45 degrees, and a fourth curve for a supercritical airfoil of thickness 0.10 above them all.
:width: 80%

The Korn relation {eq}`eq-korn-wing` against sweep, at an example $C_L$ of 0.3. Computed.
:::

:::{admonition} Navy Jet Trainer
:class: navy

$t/c$, sweep, and airfoil type against Mach 0.78 (T) and Mach 0.90 (O). Which combinations in {numref}`fig-korn-sweep` reach each one, and what does each cost at low speed?
:::

## The pitch-up boundary of swept wings

:::{math}
:label: eq-pitch-up
AR_{lim} \le 17.714\,(2-\lambda)\,e^{-0.04267\,\Lambda_{c/4}}, \qquad \Lambda_{c/4} \text{ in degrees}
:::

:::{figure} figures/pitch-up-boundary.svg
:label: fig-pitch-up
:alt: Limiting aspect ratio against quarter-chord sweep from 0 to 60 degrees, three falling curves for taper ratios 1.0, 0.5, and 0.3, the lower taper ratios higher. Region I, nose drops at stall, is labeled below the curves; Region II, nose rises at stall, above them.
:width: 80%

The pitch-up boundary from {eq}`eq-pitch-up`, after NACA Report 1339 and TN 1093 (Gudmundsson 2022, Figure 9-89).
:::

- Region I: the nose drops at stall. Region II: the nose rises at stall.
- Flaps, slats, and fences move the boundary.

:::{admonition} Navy Jet Trainer
:class: navy

Check $AR$, $\lambda$, and $\Lambda_{c/4}$ against the boundary.
:::

## Twist and stall progression

- Target: the stall starts inboard. The ailerons stay effective and the nose drops.
- Geometric {term}`washout` of 1° to 4° is typical.
- Aerodynamic washout: a tip airfoil with a higher $\alpha_{stall}$.
- Twist restores near-elliptical loading at the design $C_L$. Away from it, induced drag rises.
- Cost: lift lost at a given $\alpha$.

Gudmundsson (2022), Figure 9-83, shows the stall progression for the rectangular, elliptical, tapered, and swept planforms.

## Wing incidence

:::{figure} figures/wing-incidence.svg
:label: fig-wing-incidence
:alt: Side view of a fuselage with its reference line dashed. The wing chord line sits at the small positive incidence angle i W to the reference line. An arrow for the free stream approaches from the left at the angle of attack alpha.
:width: 80%

The wing incidence $i_W$: the angle between the wing chord line and the fuselage reference line.
:::

- Set $i_W$ so the fuselage flies at its minimum-drag attitude in cruise.
- The cruise angle of attack at the mid-cruise weight:

:::{math}
:label: eq-cruise-alpha
\alpha_C = \frac{1}{C_{L_\alpha}}\,\frac{W_1+W_2}{\rho V_C^{2} S} + \alpha_{ZL}
:::

- Correct the root incidence for washout.

:::{admonition} Navy Jet Trainer
:class: navy

Incidence and $C_{L_\alpha}$ set the approach attitude. Check the view over the nose on the 3.5° glide slope.
:::

## Lift-curve slope

:::{math}
:label: eq-lift-curve-slope
C_{L_\alpha} = \frac{2\pi\,AR}{2+\sqrt{\left(\dfrac{AR\,\beta}{\kappa}\right)^{2}\left(1+\dfrac{\tan^{2}\Lambda_{c/2}}{\beta^{2}}\right)+4}}, \qquad \beta = \sqrt{1-M^{2}}, \quad \kappa = \frac{C_{l_\alpha}}{2\pi}
:::

:::{figure} figures/lift-curve-slope.svg
:label: fig-lift-curve-slope
:alt: Wing lift-curve slope in per radian against aspect ratio from 0 to 16, three rising curves for mid-chord sweeps of 0, 30, and 45 degrees, the unswept wing highest, all below a horizontal line at 2 pi labeled section.
:width: 80%

Lift-curve slope from {eq}`eq-lift-curve-slope` at $M$ = 0 and $\kappa$ = 1 (Gudmundsson 2022, Eq. 9-72). Computed.
:::

- Valid for straight and swept wings to $M$ = 0.8.
- A lower slope means a higher approach attitude and a softer gust response.

## Maximum lift of the clean wing

:::{math}
:label: eq-clmax-wing
C_{L_{max}} = \left(C_{L_{max0}} + \Delta C_{L_{max}}^{LE} + \Delta C_{L_{max}}^{TE}\right) K_\Lambda, \qquad K_\Lambda = \cos\Lambda_{c/4}
:::

- Rapid estimate: $C_{L_{max0}} = 0.9\,C_{l_{max}}$ of the airfoil at the MGC, at the stall Reynolds number.
- Critical section method: raise $\alpha$ until a local $C_l$ reaches the airfoil $C_{l_{max}}$.

:::{admonition} Navy Jet Trainer
:class: navy

A04 Deliverable 2: the clean-wing $C_{L_\alpha}$ and $C_{L_{max}}$, with the method cited. The high-lift increments come with the next lecture.
:::

## Worked example: Cessna 172 clean maximum lift

:::{table} The rapid estimate checked against the handbook value. Gudmundsson (2022), Example 9-9.
:label: tbl-c172-clmax

| Step | Value |
| --- | ---: |
| Wing area, span | 174 ft², 36 ft |
| Weight | 2,550 lb |
| Stall speed, clean, from the handbook | 53 KCAS |
| $C_{L_{max}}$ from the handbook, $2W/(\rho V_S^{2} S)$ | 1.54 |
| Average chord, $S/b$ | 4.83 ft |
| Reynolds number at stall | $2.8 \times 10^{6}$ |
| NACA 2412 $C_{l_{max}}$, NACA Report 824 at $Re = 3.1 \times 10^{6}$ | 1.58 |
| Rapid estimate, $0.9\,C_{l_{max}}$ | 1.42 |

:::

The rapid estimate is 8% below the handbook value. A low estimate of $C_{L_{max}}$ oversizes the wing. State your method's error and its sign.

:::{admonition} Navy Jet Trainer
:class: navy

Check your method on an aircraft from your A02 database before you apply it to your own wing.
:::

## Stall speed

:::{math}
:label: eq-stall-speed
V_S = \sqrt{\frac{2\,(W/S)}{\rho\,C_{L_{max}}}}
:::

:::{figure} figures/stall-speed.svg
:label: fig-stall-speed
:alt: Stall speed in knots equivalent airspeed against wing loading from 0 to 120 pounds per square foot, four rising curves for maximum lift coefficients 1.2, 1.6, 2.0, and 2.4, the lowest lift coefficient giving the highest stall speed.
:width: 80%

Stall speed against wing loading at sea level from {eq}`eq-stall-speed`. Computed.
:::

- Check every speed-linked requirement: stall, approach, takeoff.
- The required $C_{L_{max}}$ from the field length: the method is in the high-lift lecture.

## This week

1. Airfoil: criteria traced to requirements, three candidates with published data, the comparison table, the selection, and the runner-up.
2. Wing: $S$ from the ASORT wing loading. $AR$, $\lambda$, $\Lambda$, and twist justified. $M_{DD}$ against the maximum operating Mach number.
3. Lift: $C_{L_\alpha}$ and the clean $C_{L_{max}}$, method cited. Stall speeds checked against every speed-linked requirement.
4. Layout: the volume check and the CG range against the new wing.

:::{tip}
Where exact wording matters, read the RFP text, not this page.
:::

:::{important} Summary
- The airfoil is chosen against criteria traced to requirements, from published data, with the comparison shown.
- Each planform choice has a cost. Thickness, sweep, and airfoil type set the drag divergence Mach number together.
- Maximum lift sets the stall speed. The field-length method for the required $C_{L_{max}}$ comes with the high-lift lecture.
:::

:::{exercise} For discussion
:label: ex-wing-geometry

Take the wing area and span of the T-45 from your A02 database. Compute $AR$, and with a taper ratio of your choice, $c_r$, $c_t$, and $c_{MGC}$ from {eq}`eq-planform`. Then use {eq}`eq-korn-wing` at $C_L$ = 0.3 to list the sweep and thickness pairs that put $M_{DD}$ above Mach 0.78. What does the Mach 0.90 objective add, and what does each pair cost in {eq}`eq-lift-curve-slope`?
:::

:::{seealso} Reading
Gudmundsson (2022), Chapters 8 and 9. The next lecture covers high-lift systems, with the field-length method for the required $C_{L_{max}}$. [](../assignments/a04.md) states what the deliverables ask for.
:::

## References

- Gudmundsson, S., *General Aviation Aircraft Design: Applied Methods and Procedures*, 2nd ed., Butterworth-Heinemann, 2022. Chapter 8, The Anatomy of the Airfoil; Chapter 9, The Anatomy of the Wing; Chapter 16, Aircraft Drag Analysis, Section 16.3.3.
- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design, Volume 1: Aircraft Design*, AIAA Education Series, 2010. Chapter 2, Review of Practical Aerodynamics.
- Abbott, I. H., von Doenhoff, A. E., and Stivers, L. S., "Summary of Airfoil Data," NACA Report 824, 1945.
- Schrenk, O., "A Simple Approximation Method for Obtaining the Spanwise Lift Distribution," NACA TM 948, 1940.
- Shortal, J. A., and Maggin, B., "Effect of Sweepback and Aspect Ratio on Longitudinal Stability Characteristics of Wings at Low Speeds," NACA TN 1093, 1946.
- Furlong, G. C., and McHugh, J. G., "A Summary and Analysis of the Low-Speed Longitudinal Characteristics of Swept Wings at High Reynolds Number," NACA Report 1339, 1957.
