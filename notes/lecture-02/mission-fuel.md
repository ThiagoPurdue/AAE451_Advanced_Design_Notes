---
title: The design mission, fuel weight and the sizing loop
short_title: Mission fuel and sizing loop
downloads:
  - file: code/sizing_loop.m
    title: sizing_loop.m, the MATLAB example
---

This is the second part of Lecture 2, *Aircraft Sizing*. It covers the design mission, the fuel weight fraction, the segment equations and the iteration that closes the sizing.

## The design mission

:::{prf:definition} Design mission
:label: def-design-mission

The {term}`design mission` is the most demanding mission the aircraft must fly. The operating mission is the one it usually flies, and it is shorter. A 737's design mission is about 3,000 nmi with 150 passengers. Its operating mission is 600 to 800 nmi.
:::

The design mission is drawn as a {term}`mission profile` with numbered points ({numref}`fig-design-mission`).

```{figure} figures/design-mission-profile.svg
:label: fig-design-mission
:alt: Mission profile with numbered points 0 to 4. Warm-up, taxi and takeoff run from point 0 to point 1 at ground level. Climb rises from point 1 to point 2. Cruise-climb slopes gently upward from point 2 to point 3. A no-range descent drops vertically from point 3 to point 4. A horizontal arrow below marks the still-air range from point 1 to point 4.
:width: 90%

The design mission. Simple and initial sizing credit the climb with no range, so the cruise alone covers the still-air range, from the end of the takeoff to the end of the descent.
```

:::{admonition} Navy Jet Trainer
:class: navy

Your RFP states two missions, the training flight and the ferry flight, each with its own fuel reserve. For the fuel weight, the design mission is whichever of the two needs more fuel, and you know which only after computing both. Read which number belongs to which segment: the 600 nm of the ferry flight covers segments 3 to 5, and the 50 nm legs of the training flight run from the start of the climb to the end of the descent, as the RFP figure draws them.
:::

## Fuel weight fraction

The design mission is broken into segments, and the fuel fraction is the product of the segment weight fractions:

```{math}
:label: eq-fuel-fraction
\frac{W_{fuel}}{W_0} = (1 + k)\left[1 - \frac{W_1}{W_0}\cdot\frac{W_2}{W_1}\cdots\frac{W_N}{W_{N-1}}\right]
```

- $N$ is the number of segments in the design mission.
- $k$ allows for trapped fuel, usually 1 percent. With no explicit reserve segments, 5 percent for reserves is a common allowance, so $k = 0.05 + 0.01 = 0.06$.
- Reserve fuel is carried on every mission whether or not it is used. An operational or economic mission does not consume it.

:::{admonition} Navy Jet Trainer
:class: navy

The RFP states the reserves: 30 minutes for the training flight and 45 minutes for the ferry flight, both at maximum endurance speed in cruise configuration. A reserve stated as a time at a speed is a segment. Which of the two equations below models it? Once the reserves are segments, what is left for $k$ to cover?
:::

## Segment fractions from history

Segments with no clean equation, such as taxi, takeoff and landing, use a historical fraction ({numref}`tbl-raymer-fractions`).

:::{table} Historical mission-segment weight fractions, from Raymer (2018), Table 3.2.
:label: tbl-raymer-fractions

| Segment | $W_{i+1}/W_i$ |
| --- | ---: |
| Warmup and takeoff | 0.970 |
| Climb | 0.985 |
| Landing | 0.995 |

:::

Cruise and loiter cannot use a fixed fraction. They depend on how far or how long you fly, so they need the Breguet range and endurance equations.

:::{important}
Fuel weight prediction also needs a drag build-up and an engine model. Drag and thrust are functions of altitude and velocity.
:::

## Breguet range and endurance

::::{grid} 1 1 2 2

:::{card}
:header: Range for jets
```{math}
:label: eq-breguet-range
R = \frac{V}{C}\,\frac{L}{D}\,\ln\frac{W_i}{W_{i+1}}
```
:::

:::{card}
:header: Endurance for jets, loiter and reserves
```{math}
:label: eq-breguet-endurance
E = \frac{1}{C}\,\frac{L}{D}\,\ln\frac{W_i}{W_{i+1}}
```
:::

::::

$V$ is the true airspeed, $C$ the thrust specific fuel consumption, $L/D$ the lift-to-drag ratio, and $W_i/W_{i+1}$ the ratio of the weights at the start and end of the segment. For initial sizing, assume $V$ and $L/D$ constant over the segment. At constant $V$ and $L/D$ the aircraft climbs as $W$ decreases, which is the cruise-climb in {numref}`fig-design-mission`.

:::{admonition} Navy Jet Trainer
:class: navy

Take each segment's speed and altitude from the RFP where it gives them: 250 KCAS for the training-flight climbs, 20,000 ft for the training-flight cruise, Mach 0.60 at 10,000 ft for the maneuvers. Where the RFP says "speed and thrust not specified" or "as desired", your choice is an assumption. State it.
:::

## Closing the loop

Guess $W_0$, compute the empty weight and the fuel weight as functions of that guess, add the crew and the payload, and iterate until the calculated weight matches the guess ({numref}`fig-sizing-loop`).

```{figure} figures/sizing-loop.svg
:label: fig-sizing-loop
:alt: Flow chart of the sizing iteration. An initial guess of W0 and the inputs W/S, T/W, AR and others feed a geometry block that computes the wing area S equals W0 divided by W0/S. The geometry feeds two blocks, empty weight We as a function of W0 and fuel weight Wfuel as a function of W0. Both feed the gross weight, W0 calculated equals Wcrew plus Wpayload plus We plus Wfuel. A decision asks whether the calculated W0 is approximately the guessed W0. If yes, the result is the aircraft W0 and dimensions, which go to cost and performance analysis. If no, the guess is set to the calculated value and the loop returns to the geometry block.
:width: 100%

The sizing iteration.
```

### A short MATLAB example

[](sizing-loop.ipynb) runs the loop of {numref}`fig-sizing-loop` cell by cell in MATLAB, with the lecture's equations: a trend line for the empty weight, and the product of segment fractions for the fuel, with Raymer's historical fractions for takeoff, climb and landing and the Breguet equations for cruise and loiter. The inputs describe a small jet transport with invented values, so the example is not the Navy trainer. The same code is one script, `sizing_loop.m`, which you can download from the link at the top of this page.

:::{exercise} From the example to your code
:label: ex-sizing-script

Change the trend line to the military jet trainer line, then to [Raymer's jet-trainer regression](weight-estimation.md#eq-raymer-jet) from the previous page, which needs the sizing variables as inputs. Then replace the example mission with the segments of your RFP's training flight and ferry flight, reserves included. Which mission needs more fuel?
:::

## What your sizing code needs

- Component weight estimate and empty-weight build-up (Raymer, Chapter 15).
- Mission fuel mass (Raymer, Chapter 19).
- Parasite drag build-up, $C_{D_0}$ (Raymer, Section 12.5).
- Powerplant performance (Raymer, Chapter 13).
- Center of gravity and static margin, which need the aircraft layout plus the component and fuel weights first (Raymer, Section 15.1.3 and Chapter 16).

:::{admonition} Navy Jet Trainer
:class: navy

This is the code your team builds this week. Make it modular, and link it to the authoritative source of truth (ASORT) file that holds your aircraft's design parameters.
:::

:::{important} Three things to carry into your sizing code
- Empty weight and fuel weight are both functions of $W_0$. That relationship is why sizing is iterative.
- State where your technology factor came from.
- The design mission is the hardest mission stated in your RFP, not the one you would fly on an ordinary day.
:::

:::{exercise} For discussion
:label: ex-sizing-code

How can you connect the requirements you have defined with your sizing code, and keep the code modular enough to take changes in those requirements?
:::

## References

- Nicolai, L. M., and Carichner, G. E., *Fundamentals of Aircraft and Airship Design, Volume I: Aircraft Design*, AIAA Education Series, 2010, Chapter 5.
- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., AIAA Education Series, 2018, Chapters 3, 6, 12, 13, 15, 16 and 19.
