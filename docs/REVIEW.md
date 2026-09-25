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

## Session 2026-09-25: TRL 3

Amish's instruction for this session (2026-09-25): "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every TRL 2 item with a recommendation is now recorded as decided; items without one stay open. **TRL 4 is on hold by Amish's instruction.**

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (FTK-DDR-001 v0.1): decisions 1 to 9, 11 and 12, the cross-cutting SwapCell and partner rules, and open items 10 and 13 to 19.
- `docs/04-calcs/01-sizing.md` (FTK-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: geometry and nesting, mass and centre of mass, power and gearing, steering and stability (box and Ackermann), structure (torsion, crowns, stay buckling, headset, joints, fatigue), braking and fade, assembly and repair time, corrosion, cost. The script reads the model and the BOM, so the numbers stay in step.
- `cad/src/model.py`: parametric build123d model (key dimensions in `PARAMS`), exporting `cad/step/flattrike-{assembly,frame,front-bed}.step` and matching STL files, and printing the plate schedule. TRL 3 changes: closed-box spine with top and bottom covers, vertical fork crown plates, smaller stay windows, seat on a 73° line about 110 mm further forward, 0.84 m track, 120 mm rear hub spacing, box 360 mm high with 9 mm walls, cut spacer washers instead of tubes.
- `cad/src/sheets.py` and `cad/drawings/FTK-DWG-001.svg`, `.pdf` (and `.png`): general arrangement at Rev P1, "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps FTK-DWG-010, so DWG-001 was the next free number.
- `bom/bom.csv`: 15 lines, every line priced with a supplier type; base $647 against $800. `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds its parts from `model.py`; `media/` refreshed (hero, blueprint, exploded, flow, model.glb, viewer). Every image was checked. In the blueprint isometric the kit's scale figure stands just beyond the box and its outline overlaps the box corner; this is kit placement and reads correctly.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` moved to v0.3 (decisions, R15 redefined, new R18, checked numbers). `project.yaml` (trl 3, trl_target 3, evidence, problem line) and `README.md` updated.

### Requirement status (FTK-CAL-001; 8 met, 6 not met, 3 at risk, 1 not verifiable)

| ID | Status | Value |
| --- | --- | --- |
| R1 | **Not met** with a 90 kg rider | 307.5 kg gross (297.5 kg with 80 kg) |
| R8 | **Not met** | 67.5 kg empty against 55 kg |
| R10 | **Not met** with no cargo | 0.24 g straight, 0.11 g at full box-steering lock (tips at 5.8 km/h); 0.43 g loaded |
| R13 | **Not met** unassisted | 238 W at the pedals needed; 6.0 km/h with route C assist |
| R14 | **Not met** for the spine side plates | about 78 min (42 bolts) |
| R18 | **Not met** | about $414 at 100 units against $300 |
| R2 | At risk | stresses 45 MPa or less; stay buckling SF 2.06; headset 3.34 kN per bearing |
| R7 | At risk | about 3.6 h for two people |
| R11 | At risk | about 37 N·m per drum needed; fade after about 1.9 km of 5 % descent |
| R16 | Not verifiable at TRL 3 | coating-dependent |
| R3, R4, R5, R6, R9, R12, R15, R17 | Met | 27 flat plates; 2,486 of 2,500 mm sheet; standard parts; 0.39 m³; 0.986 m wide and 5.67 m turning circle; 7.6 km/h; $647; 184 L and 0.77 m counter |

Numbers in the TRL 2 documents that changed: empty mass 68 to 67.5 kg (box was underestimated by about 3 kg; windows saved about 6 kg; covers and crowns added), 5 % climb 240 to 238 W, drum power on a 5 % descent 0.4 to 0.27 kW (rolling resistance was left out), rider-only tipping 0.18 to 0.24 g (seat moved), box volume 190 to 184 L, lid 0.79 to 0.77 m, turning circle 5.8 to 5.67 m.

Structural findings: the TRL 2 open twin-plate spine would see 556 MPa in torsion and the flat fork bridges 619 MPa; both are fixed in the TRL 3 model (9 and 23 MPa). Buckling of the stay strips and the headset roll load now govern.

### Decisions recorded (FTK-DDR-001)

Decided by Amish, 2026-09-25, go with recommendation: tadpole front loader; box steering for the first prototype with Ackermann assessed at TRL 3; no assist in the prototype, route C (SwapCell) preferred; 3 mm S235 or A36 painted; M8 8.8 with all-metal locknuts; bought head tube and bottom bracket sections clamped between plates; 20 in wheels with drums and a 3-speed rear hub; design changes tried before relaxing R8 and R10; production target $300 at 100 units (new R18); `budget_usd` kept at $800 for the pedal-only prototype (R15 redefined); problem line reworded. Cross-cutting: route C cites SwapCell interface v0.3 items W, C and V (latch class V1); the SwapCell pack is priced once and excluded; partners are picked per area later.

### Still awaiting Amish

- Item 10: first partner organization and city (no recommendation; picked per area later).
- Item 13: switch the first prototype to Ackermann steering (recommended) because of full-lock tipping.
- Item 14: R8, recommend relaxing to 70 kg including the box.
- Item 15: R10 rider-only case, recommend 0.22 g with Ackermann and a cornering-speed label.
- Item 16: R1, recommend 140 kg rated cargo for riders over 80 kg.
- Item 17: R14, recommend 90 min for the spine side plates only.
- Item 18: R18, recommend keeping $300 and getting wholesale part prices first.
- Item 19: headset under roll load, recommend a longer head tube or taper roller bearings.

### Citations

The TRL 2 note listed no unchecked citations. The EN 17860 summary (ACT Lab) was re-fetched and supports the 300 kg multi-track class and doubled pedaling-force cycles for commercial use; the numeric test loads are not public and were not read. The IndiaMART price range is still a marketplace snapshot to check with a partner.

### Safety concerns

- Empty trike tips at about 5.8 km/h at full box-steering lock (0.11 g) and at 0.24 g straight.
- The headset carries the rear frame's roll moment (about 3.3 kN per bearing at 0.5 g).
- Stay strips are compression members with a buckling safety factor of about 2; removing the stay bridge would halve it.
- Drum fade after about 2 km of loaded 5 % descent; drum and parking torque ratings unconfirmed.
- Bolted joint slip and fretting, cut edges, pinch points at the steering bed, and lithium-ion hazards if route C is built.

### Other notes

- No TRL 4 material exists in this repo (`build-log/README.md` is the scaffold header only; `electronics/` and `firmware/` are empty). Nothing was added to them.
- The bounding-rectangle nest fits the sheet with only 14 mm to spare; true-shape DXF nesting is still needed.

### Recommended next step

Amish decides items 13 to 19 in FTK-DDR-001, then a TRL 3 refinement session on paper: a plate-and-joint FEA of the spine box, stays and bed, Ackermann steering geometry if chosen, headset sizing, true-shape nesting from DXF, and supplier data for hubs, drums and prices. **TRL 4 is on hold by Amish's instruction.** For the record only, TRL 4 would need: the EN 17860 load cases, DXF files and a chosen partner and laser shop, one frame cut and assembled, lab test reports (TST, `environment: lab`) for the proof load, stay buckling, joint slip, tipping threshold and braking, build-log entries, and a build budget decision.
