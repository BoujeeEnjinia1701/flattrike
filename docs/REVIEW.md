# Review note: FlatTrike

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (FTK-PRB-001 v0.2): problem with sourced figures (street vendor numbers, local rickshaw prices and weight, imported trike price), users, operating environment, constraints, out of scope, prior work with inline sources, open questions and a co-design checklist.
- `docs/03-requirements.md` (FTK-REQ-001 v0.2): 17 measurable requirements (R1 to R17) with targets, a design load case, assumptions and a concept status column that marks the requirements not met.
- `docs/02-concept.md` (FTK-PRC-001 v0.2): how it works, numbered components, first-order numbers (size, mass, riding power, hills, stability, structure, braking, cost), proposed design choices with options, safety section, open questions.
- `cad/src/concept_media.py`: massing model of a tadpole front-loading trike. Every steel part is a flat 3 mm plate (spine pair, rear stay pair, front bed plates) with a BOM number; standard bicycle parts for wheels, drivetrain, seat, bars and brakes.
- `media/`: `hero.png` (1.75 m scale figure), `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with callouts 1 to 12 matching the BOM, `flow.png` (rider power to the road, estimates), `model.glb` and `viewer.html`. No cutaway, because the inside of the design does not carry the idea; the side and top views on the blueprint show the plate layout.
- `bom/bom.csv`: 15 lines with indicative USD prices, items 1 to 12 matching the exploded view; `bom/bom-notes.md` updated to say what the base cost includes.
- `README.md`: hero image and links line before "## Problem"; concept paragraph, key components and safety note updated to match.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Overall size | about 2.11 x 0.96 x 0.94 m; wheelbase 1.45 m; track 0.80 m | R9 met |
| Rated load, gross mass | 150 kg cargo plus 80 kg rider; about 298 kg gross | R1 met, no margin against 300 kg |
| Empty mass | about 68 kg (plates about 30 kg, box about 16 kg) | **R8 (55 kg) not met** |
| Steel plate area | about 1.5 m², against a 3.1 m² standard sheet | R4 likely met |
| Flat pack | about 0.36 m³ | R6 likely met |
| Flat cruise at 110 W | about 7.6 km/h | R12 met |
| 5 % hill at 4 km/h | about 240 W at the pedals needed | **R13 not met unassisted** |
| Tipping threshold | about 0.38 g loaded; about 0.18 g with rider only | **R10 not met empty** |
| Plate bending stress | about 20 to 26 MPa, against about 235 MPa yield | R2 unverified (fatigue and joint slip) |
| Base prototype parts (pedal only) | about $640 | R15 met |
| With optional electric assist | about $1,040 | **R15 not met** |

Requirements not met or at risk:

- **R8 (empty mass) not met:** about 68 kg against 55 kg.
- **R10 (stability) not met with no cargo:** about 0.18 g, a turn on a 5 m radius at about 11 km/h. Box steering makes this worse at full lock.
- **R13 (hill climb) not met without assist:** a loaded 5 % grade needs about twice sustained rider output.
- **R15 (cost) not met if the assist option is included:** about $1,040 against $800.
- **R1 at the limit:** gross mass is within about 2 kg of the 300 kg class limit with an 80 kg rider, and over it with a 90 kg rider.
- **R2, R7, R11, R14 and R16 unverified:** frame fatigue and joint stiffness, assembly time, braking and fade, repair time and service life need TRL 3 work.

### Proposed, awaiting Amish

1. **Layout.** A: tadpole front loader (modelled). B: delta rear loader (*thela* layout; needs a non-standard live rear axle). C: delta front loader. Recommendation: A.
2. **Steering.** A: box steering on one kingpin (modelled; simplest). B: Ackermann steering with a fixed box (better stability, about $40 more). Recommendation: A for the first prototype, B assessed at TRL 3 because of R10.
3. **Electric assist.** A: none in the base, with a bottom bracket housing that accepts a mid-drive later. B: generic 36 V mid-drive with its own pack (about $400). C: 48 V mid-drive on a SwapCell pack, shared with the portfolio (kit about $260 plus pack about $370). Recommendation: A for the prototype, C as the preferred assist route. This is the only place SwapCell is proposed.
4. **Plate material:** 3 mm S235JR or A36 class steel, painted or powder coated, rather than S355 or stainless. Recommendation as stated.
5. **Joint hardware:** M8 class 8.8 bolts with all-metal locknuts rather than nylon-insert nuts.
6. **Head tube and bottom bracket housings:** bought steel sections clamped between plates (recommended), bolt-in bearing housings, or parts salvaged from a donor frame.
7. **Wheels:** 20 in on all three positions with drum brakes; 3-speed hub at the rear.
8. **Revised targets or design changes for R8 and R10.** Options: lighten the plates and box, widen the track (breaks R9), move the seat forward and lower, or relax the targets. Recommendation: try design changes first at TRL 3.
9. **Production cost target.** Local workshop tricycles sell for about ₹10,000 to ₹25,000 (about $120 to $300) in India, so the $800 prototype budget says little about competitiveness. Recommendation: set a production target, for example $300 or less per trike at 100 units, before TRL 3.
10. **First partner and city** for co-design and laser shop quotes.
11. **Budget.** The pedal-only base (about $640) is within `budget_usd` ($800), which is unchanged. No budget change is proposed unless option 3B or 3C is chosen for the prototype, which would need about $1,040.

`project.yaml` pitch and problem are unchanged. The research supports them for imported and branded trikes, but in South Asia the main competitor is the cheap local workshop tricycle, so the case rests on durability, mass, gears and repair rather than price alone. Consider adding that nuance to the problem line (proposed, awaiting Amish).

### Safety concerns

- Structural failure of bolted plate joints (loosening, slip, fatigue cracks at holes) under a 300 kg vehicle, with routine overloading in commercial use. No public-road use before strength and fatigue are verified.
- Tipping of the empty trike in brisk turns, made worse by box steering.
- Drum brake fade on long loaded descents; the parking latch must hold on slopes.
- Sharp and burred laser-cut edges; every plate must be deburred and corners radiused.
- Pinch point between the pivoting front bed and the spine near the rider's feet; exposed chain and spokes.
- If assist is chosen: lithium-ion pack hazards as set out in the SwapCell design.

### Problems and notes

- The kit renderer's hidden-line projector failed on two coaxial tori (the front tyres), so tyres are modelled as flat rings. This does not affect proportions.
- The legacy placeholder `cad/src/model.py` is untouched; the parametric model is TRL 3 work.
- The IndiaMART price range is a marketplace snapshot, not a survey, and should be checked with a partner.
- No cutaway was produced (see above).

### Recommended next step

Review this note and the media, then decide items 1 to 3 and 9. If approved, run `/advance-trl3` to check the plate frame's stiffness and fatigue against EN 17860 load cases, work on the mass and stability shortfalls, design the head tube and bottom bracket clamps, and produce the parametric model, nesting study and drawing sheet.
