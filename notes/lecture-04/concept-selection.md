---
title: Concept generation and selection
short_title: Concept generation and selection
---

This is Lecture 4, *Concept Generation and Selection*. Lecture 3 listed the arrangement options. This lecture covers building many candidates from those options and narrowing them to one, with methods that leave a record: brainstorming, the morphological chart, Pugh's controlled convergence, and weighted objectives. The reading is Clausing, "Selecting a Winning Concept," on Brightspace.

:::{note} What to take from this lecture
- Generate many concepts before analyzing any of them.
- The morphological chart composes concepts by decomposition.
- Pugh's method scores every concept against a datum, criterion by criterion, and produces new concepts while it narrows the field.
- Weighted objectives make a shortlist. They do not close a decision.
:::

## Purpose

- Concept generation sets the overall arrangement: what the aircraft looks like and where the major components go.
- Geometry affects performance, size, and weight.
- Generate many concepts. Missing a promising one costs more than sketching a weak one.
- Select the most promising few with little analysis. Detailed analysis comes after the down-select.

The process alternates between widening and narrowing the set of concepts ({numref}`fig-controlled-convergence`). Each narrowing is a matrix run. Each widening adds the concepts the run suggested.

:::{figure} figures/pugh-controlled-convergence.svg
:label: fig-controlled-convergence
:alt: A funnel drawn as a zigzag from top to bottom. At the top, the specification feeds concept generation, which spreads into the initial number of concepts. The outline then narrows at each step labeled controlled convergence and widens again at each step labeled concept generation: initial number reduced, new ones added, further reduction, further addition, and so on, until the two sides meet at a point labeled concept selected.
:width: 70%

Controlled convergence, after Pugh (1991). Convergence steps (CC) remove concepts; generation steps (CG) add new ones. The set narrows until one concept is left. PDS is Pugh's product design specification: your requirement set.
:::

:::{admonition} Navy Jet Trainer
:class: navy

The RFP asks the proposal to show the alternative concepts the team considered and the method used to select one, with the strengths and weaknesses of each. Keep the generation record: every concept, every disqualifier, every matrix run.
:::

## Same requirements, different aircraft

The same mission produced several different aircraft. One of them is often the first Pugh datum.

::::{grid} 1 3 3 3

:::{card}
![T-45 Goshawk in flight, a low-wing jet with side inlets and a single fin.](../lecture-03/figures/t45.jpg)

**Boeing T-45 Goshawk.** U.S. Navy photo by Lt. j.g. John A. Ivancic, public domain.
:::

:::{card}
![Northrop T-38 Talon in flight over the desert, a small low-wing jet with two engines in the aft fuselage.](../lecture-03/figures/t38.jpg)

**Northrop T-38 Talon.** U.S. Department of Defense, public domain.
:::

:::{card}
![Boeing T-7A Red Hawk in flight, a jet with a high wing and twin fins.](../lecture-03/figures/t7a.jpg)

**Boeing T-7A Red Hawk.** U.S. Air Force photo by Bryce Bennett, public domain.
:::

::::

Photos via Wikimedia Commons.

## Brainstorming

- Start from a written problem statement or question.
- Mix perspectives: aerodynamics, structures, propulsion, stability and control, manufacturing, the customer.
- A moderator who does not take part runs the session.
- Members write or sketch ideas first, individually. One idea per card.
- Present one idea at a time. Build on and combine the ideas of others.
- Session length: about 30 minutes. Run it before the Pugh sessions.

:::{tip} Rules, enforced by the moderator
1. No criticism during the session.
2. Generate many ideas.
3. Seemingly crazy ideas are welcome.
4. Present ideas briefly.
5. Combine and improve on the ideas of others.
:::

:::{admonition} Navy Jet Trainer
:class: navy

A problem statement that fits the RFP: "What should the Navy's next land-based jet trainer look like?" In A03 Deliverable 2, a model reviews your morphological chart and proposes candidates you did not compose. A suggestion enters the chart only after you check it against your requirements and CONOPS.
:::

## Generation failure modes

- Only one or two alternatives considered, proposed by the most assertive members.
- Other builders' concepts, in related and unrelated products, not examined.
- Only one or two members involved. The rest never commit to the result.
- Promising partial solutions never combined.
- Entire categories of solutions never considered.

What a structured method buys:

- Gathers information from scattered sources.
- Walks the team through the alternatives.
- Combines partial solutions.
- Proceeds step by step, so first-time designers can follow it.

:::{admonition} Navy Jet Trainer
:class: navy

Weigh the certification cost of an unconventional concept from the first session. Your {term}`certification basis` is MIL-HDBK-516C (A02 Deliverable 1).
:::

## The morphological chart

Lecture 3 introduced the {term}`morphological chart` ([illustration](#tbl-morphological-illustration)). It generates concepts by decomposition:

- Decompose the aircraft into the functions it must perform.
- One row per function. One column per way to fulfill it.
- One pick per row is a concept.
- Incompatible combinations are expected. Record the disqualifier.

:::{admonition} Navy Jet Trainer
:class: navy

A03 Deliverable 2: choose the rows from your requirements and CONOPS, then compose at least three distinct configurations. Distinct means different arrangement decisions; resizing one concept does not count.
:::

## Pugh's method

:::{prf:definition} Pugh's method
:label: def-pugh-method

Controlled convergence (Pugh 1991; Clausing 1994) scores every concept against a {term}`datum`, criterion by criterion, as better, worse, or the same, in a {term}`Pugh matrix`. The method runs in ten steps over two or three sessions, and it generates new concepts while it narrows the field.
:::

### Steps 1 and 2: criteria and the matrix

- **Step 1, choose criteria.** Take them from your requirements. Keep the list short. No weights.
- **Step 2, form the matrix.** Concepts across the top, criteria down the side. One concept is the datum: a baseline, often an existing aircraft. For a jet trainer, the T-45 is a natural first datum.

:::{table} Illustration of a Pugh matrix with invented entries. Plus: better than the datum. S: the same. Minus: worse. A dash marks the datum column. The three sums are listed separately.
:label: tbl-pugh-illustration

| Criterion | A (datum) | B | C | D |
| --- | :---: | :---: | :---: | :---: |
| I | — | + | S | − |
| II | — | S | + | S |
| III | — | − | S | + |
| IV | — | + | − | S |
| V | — | S | + | − |
| Sum of + | — | 2 | 2 | 1 |
| Sum of S | — | 2 | 2 | 2 |
| Sum of − | — | 1 | 1 | 2 |

:::

### Steps 3 to 7: running the matrix

- **Step 3, clarify concepts.** Each member presents theirs. The team takes ownership of all of them.
- **Step 4, choose the datum.** One of the better concepts, or an existing aircraft. Vote if needed.
- **Step 5, run the matrix.** Score each concept against the datum: plus for better, minus for worse, and S when it is not clearly either. Use engineering judgment and set a time limit per cell. Record new concepts in added columns.
- **Step 6, evaluate.** Total the plus, S, and minus counts separately. Never compress them into one score.
- **Step 7, attack the negatives, build on the positives.** Remove minus ratings by modifying concepts. Carry plus features across to other concepts. Add hybrids as new columns.

Clausing: "The major advance is the new insight gained by team members."

### Steps 8 to 10: converging on a winner

- **Step 8, new datum, run again.** Promote a promising concept to datum. A different datum tests whether the leader holds.
- **Step 9, plan further work.** List the analyses that settle the uncertain scores.
- **Step 10, iterate to the winning concept.**

:::{figure} figures/pugh-matrix-runs.svg
:label: fig-pugh-matrix-runs
:alt: A sketch with matrix runs on the horizontal axis and the number of concepts on the vertical axis. A line falls steeply from the first run, rises slightly where added hybrids enter, falls again, rises slightly once more, and flattens at a low value where the winner emerges.
:width: 60%

The number of concepts over successive matrix runs. Eliminations dominate; hybrids add columns briefly.
:::

:::{admonition} Navy Jet Trainer
:class: navy

A03 Deliverable 3 requires one re-score with a new datum. State whether the leader holds.
:::

## Limits of Pugh's method

- It is used across engineering design, less often in aircraft design practice.
- It organizes qualitative judgment into a defensible record.
- Not a quantitative trade study. Scores are comparisons against a datum, not measurements.
- Surviving concepts are compared by engineering analysis: sizing, constraints, layout.

:::{admonition} Navy Jet Trainer
:class: navy

The matrix selects what to analyze. The A03 sizing refinement and mission analysis supply the analysis; the A04 layout follows.
:::

## Weighted objectives

- Rank and weight the objectives. The team sets the weights.
- Score each concept against each objective, 1 (worst) to 10 (best).
- Total: the sum of weight times score.

:::{table} Illustration of a weighted objectives matrix with invented weights and scores. Your objectives come from your requirements.
:label: tbl-weighted-objectives

| Objective | Weight | A | B | C |
| --- | ---: | ---: | ---: | ---: |
| Empty weight | 0.30 | 6 | 8 | 5 |
| Field performance | 0.25 | 7 | 5 | 9 |
| Cruise speed | 0.20 | 8 | 6 | 5 |
| Certification risk | 0.15 | 7 | 4 | 6 |
| Maintenance access | 0.10 | 5 | 7 | 8 |
| Weighted total | | 6.70 | 6.15 | 6.45 |

:::

:::{warning}
The arithmetic multiplies subjective weights by subjective scores. The result looks like a measurement and is not. Use {term}`weighted objectives` to shortlist, never to close a decision.
:::

:::{important} Summary
- Generate many concepts. Pugh's method keeps creativity on the design objective and forces fair technical critique.
- Pugh's controlled convergence compares concepts and produces new ones. Do not overemphasize the numbers.
- A03 Deliverable 2 is the morphological chart and at least three distinct configurations. Deliverable 3 is the Pugh selection with one datum re-score.
:::

:::{exercise} For discussion
:label: ex-pugh-criteria

Write the problem statement for your brainstorming session in one sentence. Then pick the first five criteria for your Pugh matrix from your A01 requirement set, and state why each one is there. Pugh gives the criteria no weights. What would a weight add, and what would it hide?
:::

:::{seealso} Reading
Clausing, "Selecting a Winning Concept," on Brightspace. [](../assignments/a03.md) states what Deliverables 2 and 3 ask for.
:::

## References

- Pugh, S., *Total Design: Integrated Methods for Successful Product Engineering*, Addison-Wesley, 1991.
- Clausing, D., *Total Quality Development: A Step-by-Step Guide to World-Class Concurrent Engineering*, ASME Press, 1994.
- Frey, D. D., Herder, P. M., Wijnia, Y., Subrahmanian, E., Katsikopoulos, K., and Clausing, D. P., "The Pugh Controlled Convergence method: model-based evaluation and implications for design theory," *Research in Engineering Design*, Vol. 20, 2009, pp. 41–58, doi 10.1007/s00163-008-0056-z.
