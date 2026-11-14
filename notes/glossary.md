---
title: Glossary
---

The notes use these terms in a fixed sense. In the text, a term with a dotted underline opens its definition.

:::{glossary}
Active boundary
: A boundary of the constraint diagram that closes the feasible region. Its requirement is a driving requirement.

Aspect ratio
: $AR = b^2/S$, the span squared over the wing area. High aspect ratio lowers the induced drag and raises the wing weight.

ASORT
: Authoritative source of truth. One parameter file that every script of the sizing code reads, so that no constant is duplicated in code.

Bypass ratio
: The bypass mass flow of a turbofan divided by its core mass flow.

Capture area
: The free-stream cross-section of the streamtube that the engine and the secondary systems take in, $A_{\infty E}$. Also called the demand capture area. The cowl capture area of Nicolai and Carichner (2010) is the opening of the inlet at the lip, which these notes call the lip area.

Certification basis
: The airworthiness document and the sections of it that apply to the aircraft, against which compliance is shown. In this course the Navy Jet Trainer uses MIL-HDBK-516C.

CG envelope
: The CG of every loading state against weight, drawn with the forward and aft CG limits.

Compliance matrix
: A table with one row per requirement: its threshold, its objective or target, and the current value of the design.

Compressibility drag
: $C_{D_c}$, the drag added by shock waves and shock-induced separation as the flight Mach number passes the critical Mach number.

Conceptual design
: Phase 1 of an aircraft program. It selects the configuration, sizes it, and shows that the requirements can be met. Its output is a feasible design.

Configuration
: The type, location, and count of each major component of the aircraft: wing, fuselage, engines, tail, and landing gear.

CONOPS
: Concept of operations. A description of how the system will be operated during its life-cycle phases to meet stakeholder expectations.

Constraint diagram
: The thrust-to-weight ratio against the wing loading, with one boundary for each requirement.

Critical field length
: The runway length at which, after an engine failure at the engine-failure speed, continuing the takeoff and stopping take the same distance. Defined for the Navy Jet Trainer in MIL-STD-3013B.

Critical Mach number
: $M_{crit}$, the flight Mach number at which the flow first reaches sonic speed somewhere on the airfoil.

Datum
: The reference concept in a Pugh matrix. Every other concept is scored against it, criterion by criterion. At the first run it is often an existing aircraft.

Deck angle
: The pitch attitude of the fuselage on the approach, the angle of attack less the glide-slope angle. Flaps lower it; slats raise it.

Density altitude
: The altitude in the standard atmosphere at which the density equals the actual air density.

Design mission
: The most demanding mission the aircraft must fly. The operating mission is the one it usually flies, and it is shorter. The RFP prescribes two missions and the briefs call each a design mission; which one sizes the fuel is known only after both are computed.

Design point
: The wing loading and the thrust-to-weight ratio selected for the aircraft, inside the feasible region of the constraint diagram.

Drag count
: A drag coefficient of 0.0001.

Drag divergence Mach number
: $M_{dd}$, the Mach number at which the drag starts to rise steeply with Mach. Boeing: the section drag 0.002 above its incompressible value. Douglas: the slope $dC_d/dM$ reaching 0.10.

Drag polar
: The drag coefficient of an airfoil or aircraft against its lift coefficient, in one configuration at one Mach number.

Energy height
: $z_e = h + V^2/2g$, the potential plus the kinetic energy of the aircraft per unit weight. The altitude it would reach if all its kinetic energy became altitude.

Engine deck
: Thrust and fuel flow against altitude, speed, ambient temperature, and rating.

FCLP
: Field Carrier Landing Practice. Carrier approaches and landings flown to a land runway marked as a carrier deck.

Feasible region
: The part of the constraint diagram that meets every requirement.

Fixed engine
: An engine selected off the shelf, with known thrust and fuel flow, that does not change during sizing.

Flap
: A trailing-edge device that adds camber and, for the Fowler type, chord. It raises the maximum lift coefficient and lowers the stall angle.

Flat-plate area
: $f = C_{D_0} S_{ref}$, the parasite drag of an aircraft or a component written as an area with a drag coefficient of 1.

Form factor
: $FF$, the factor on skin friction drag that accounts for the pressure drag of a component.

Ground effect
: The drop in induced drag and the rise in lift of a wing close to the ground.

Induced drag
: $C_{D_i}$, the drag due to lift: $K C_L^2$ with $K = 1/(\pi\,AR\,e)$.

Installed thrust
: The thrust of the engine in the aircraft, after the inlet and nozzle losses, the power extraction, and the bleed.

Interference factor
: $Q$, the factor on the drag of a component that accounts for the flow around its neighbors.

Master equation
: The thrust-to-weight ratio that a condition requires at each wing loading, from the energy of the aircraft. Mattingly et al. (2002), Eq. 2.11.

Mean geometric chord
: $c_{MGC}$, the chord-weighted mean chord, $(2/S)\int_0^{b/2} c^2\,dy$; for a trapezoidal wing it is the chord at the spanwise centroid of the half-wing. A04 calls it the mean aerodynamic chord. The subsonic aerodynamic center sits near its quarter chord.

Measure of merit
: A quantity used to rank concepts, such as life-cycle cost or takeoff weight. Trade studies report the change in a measure of merit.

Mission profile
: One mission drawn as altitude against distance or time, divided into numbered segments, each with a stated condition.

MLW
: Maximum landing weight. The highest weight at which the aircraft is allowed to land.

Morphological chart
: A table with one row per major arrangement choice and one column per option. One pick per row is a configuration.

MTOW
: Maximum takeoff weight. The highest weight at which the aircraft is allowed to take off.

Need
: What a stakeholder wants to be able to do, stated independently of any solution.

Neutral point
: The CG position at which the pitching moment does not change with angle of attack, $C_{M\alpha} = 0$.

Nozzle pressure ratio
: The total pressure at the nozzle exit divided by the ambient pressure.

Objective
: The value of a requirement that the customer would like to reach. In the lecture example it is called the target.

Parasite drag
: $C_{D_0}$, the drag at zero lift: skin friction, form, interference, and the miscellaneous items.

PDR
: Preliminary Design Review. The review at the end of this course, where the converged conceptual design is judged against the requirements.

Performance condition
: A point requirement the RFP states at a weight, altitude, and day, outside the mission profiles.

Pressure recovery
: The total pressure at the compressor face of an inlet divided by the total pressure of the free stream.

Pugh matrix
: A selection matrix that scores each concept against a datum, criterion by criterion.

Rating
: A power setting the engine maker names, such as idle, maximum continuous, or takeoff.

Requirement
: An obligation on the system, written as "The system shall...", with a verification method.

Reynolds number
: $Re = \rho V l/\mu$, the ratio of inertial to viscous forces, on a reference length: the mean geometric chord for wing and airfoil data, the component length in the drag build-up.

RFP
: Request for proposal. The document in which a customer states what it needs and the limits a bidder's design must meet.

Rubber engine
: An engine that scales with the aircraft during sizing. It implies new engine development.

Scissor plot
: The tail area ratio that each stability and control requirement needs, against the CG position. Its cut at the chosen area gives the CG limits.

Skin friction coefficient
: $C_f$, the viscous drag of a surface per unit of wetted area and dynamic pressure.

Slat
: A leading-edge device that moves forward and down to open a slot ahead of the wing. It delays separation and raises both the maximum lift coefficient and the stall angle.

Span efficiency
: $e$, the ratio of the induced drag of an elliptic wing to the induced drag of the wing or aircraft at the same lift and aspect ratio.

Specific excess power
: The rate at which the aircraft can gain energy height, (T − D)V/W, in ft/s. It measures the thrust available beyond the drag at a given speed, altitude, and weight.

SRR
: System Requirements Review. The review at which the mission statement, the needs, and the requirements are baselined.

Stakeholder
: Anyone with an interest in the project: customers, operators, maintainers, investors, regulators, suppliers, and end users.

Static margin
: $SM = \bar x_n - \bar x_{cg}$, the distance from the CG to the neutral point in mean chords. Positive for a statically stable aircraft.

Tail volume coefficient
: $V_H = S_t l_t/(S\bar c)$ for the horizontal tail and $V_v = S_v l_v/(S b)$ for the fin: tail area times arm, over wing area times chord or span. The arms run from the wing aerodynamic center, near the quarter chord of $\bar c$, to the aerodynamic center of the horizontal tail or the fin.

Taper ratio
: $\lambda = c_t/c_r$, the tip chord over the root chord.

Technology factor
: A factor applied to a regression result to account for a technology the database never saw, such as a composite structure.

Threshold
: The minimum acceptable value of a requirement. A design that meets every threshold is acceptable.

Throttle ratio
: The value of $\theta_0$, the free-stream total temperature over the sea-level standard temperature, at which the turbine entry temperature reaches its limit. The engine maker sets the throttle ratio.

Thrust lapse
: The thrust available at an altitude, Mach number, and rating, as a fraction of the sea-level static thrust at that rating.

Thrust-to-weight ratio
: $T_{SL}/W_{TO}$ on the constraint diagram: the sea-level static thrust over the takeoff weight. At a flight condition, $T/W$ is the thrust and the weight there: $T/W = (\alpha/\beta)\,T_{SL}/W_{TO}$.

Trade study
: An analysis that changes one requirement or one assumption and measures the effect on the design, usually as a change in a measure of merit.

Trim
: The state in which the moment about the CG is zero and the lift equals the weight.

TRL
: Technology readiness level. A scale from 1, basic principles observed, to 9, proven in operation.

TSFC
: Thrust-specific fuel consumption. The fuel weight flow divided by the thrust, in lb per hour per lb, written 1/h.

Waiver
: A written record of a change to a baselined requirement, with the reason for the change. Kept in the deck appendix.

Washout
: Twist that lowers the incidence of the tip relative to the root, so the stall starts inboard. Geometric washout of 1° to 4° is typical.

Weighted objectives
: A selection method that scores each concept against each objective and sums weight times score. The weights and the scores are both judgments, so the total can only shortlist.

Wetted area
: $S_{wet}$, the surface area of a component exposed to the flow.

Wing loading
: $W/S$, the weight per unit wing area, in lb/ft². With the takeoff weight it gives the wing area; with the maximum lift coefficient it gives the stall speed.
:::
