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

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation (items 13 to 19) is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (FTK-DDR-002 v0.1) and marked in FTK-DDR-001 v0.2. Item 10 has no recommendation and stays open. **TRL 4 remains on hold by Amish's instruction**; `trl` and `trl_target` stay at 3.

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| 13 | Ackermann steering with a fixed box for the first prototype | Box steering on one kingpin; rider-only tipping 0.11 g (5.8 km/h) at full lock | Fixed bed; two 20 in forks on knuckle headsets in closed knuckle posts, tie rod, drag link; rider-only 0.24 g at any lock; 27 plates to 34; box 795 x 700 to 820 x 560 mm, floor 400 to 470 mm, 184 to 151 L, lid 0.77 to 0.84 m; turning circle 5.67 to 5.95 m; BOM item 5 $25 to $85 |
| 14 | R8 relaxed to 70 kg with the box | Target 55 kg; 67.5 kg (not met) | Target 70 kg; 69.8 kg (met, 0.2 kg margin) after larger windows in the axle beam, rails and bulkhead |
| 15 | R10 rider-only case 0.22 g with Ackermann and a cornering-speed label | Target 0.30 g; 0.24 g straight (not met) | Target 0.22 g; 0.24 g (met); label "6 km/h in full-lock turns when empty" added to BOM item 14; loaded 0.43 to 0.41 g |
| 16 | Cargo 140 kg for riders over 80 kg | 307.5 kg gross with a 90 kg rider (not met) | 299.8 kg with 90 kg and 140 kg, and with 80 kg and 150 kg (met, 0.2 kg margin) |
| 17 | R14 allows 90 min for the spine side plates only | 78 min against 30 min (not met) | 78 min against 90 min (met); knuckle post plate 27 min |
| 18 | Keep the $300 production target; wholesale prices from the first partner first | $414 estimate | Target unchanged; estimate $456 with the steering parts (not met); prices wait on item 10 |
| 19 | Longer head tube | 150 mm; 3.34 kN per headset bearing in roll | 200 mm; roll couple 2.56 kN, carried by the collar and yoke clamps of the fixed bed, not the bearings |

Other changes: prototype parts $647 to $709 (`budget_usd` stays $800; R15 met); empty mass 67.5 to 69.8 kg; assembly 3.6 to 4.0 h; bolt sets 112 to 116; 5 % climb 238 to 240 W; crate 0.39 to 0.30 m³. FTK-CAL-001 v0.2 adds a true-shape raster nest, because 34 plates no longer fit by bounding rectangles (2,805 mm); the true-shape nest uses 2,190 of 2,500 mm. Files: `cad/src/model.py` (STEP and STL re-exported), `cad/src/sheets.py` and FTK-DWG-001 Rev P2, `cad/src/concept_media.py` and `media/`, `docs/04-calcs/sizing.py`, `results.csv` and `01-sizing.md` (v0.2), `bom/bom.csv`, `bom/bom-notes.md`, FTK-PRB-001, FTK-PRC-001 and FTK-REQ-001 (v0.4), `project.yaml` (evidence list) and `README.md`.

README: added "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" before "## Problem". The inspiration point is the Global Vehicle Trust OX flat-pack truck by Gordon Murray Design (CarsGuide, 2016). All generated files were re-rendered with designmolecule.com.

### Requirement status (FTK-CAL-001 v0.2; 12 met, 2 not met, 3 at risk, 1 not verifiable)

| ID | Status | Value |
| --- | --- | --- |
| R13 | **Not met** unassisted | 240 W at the pedals needed; 6.0 km/h with route C assist |
| R18 | **Not met** | about $456 at 100 units against $300 |
| R2 | At risk | stresses 47 MPa or less (knuckle post column); stay buckling SF 2.09 |
| R7 | At risk | about 4.0 h for two people, at the limit |
| R11 | At risk | about 37 N·m per drum needed; fade after about 1.9 km of 5 % descent |
| R16 | Not verifiable at TRL 3 | coating-dependent |
| R1, R8 | Met, 0.2 kg margin | 299.8 kg gross; 69.8 kg empty |
| R3, R4, R5, R6, R9, R10, R12, R14, R15, R17 | Met | 34 flat plates; 2,190 mm of sheet; standard parts; 0.30 m³; 0.986 m wide, 5.95 m turning circle; 0.41 and 0.24 g; 7.6 km/h; 78 min; $709; 151 L and 0.84 m |

### Still awaiting Amish

- Item 10: first partner organization and city (no recommendation; partners are picked per area later). Item 18's wholesale prices wait on it.

### Cross-repo actions

None. Assist route C still cites SwapCell interface v0.3 items W, C and V, unchanged.

### Safety concerns

- The empty trike still tips at 0.24 g; the bar label (6 km/h in full-lock turns when empty) is the control.
- The knuckle post columns (47 MPa, 155 MPa without their cheek plates) and the head tube clamps now carry the highest loads; the tie rod and drag link rod ends are single points of failure for steering.
- Mass has only 0.2 kg of margin against the 300 kg class; any added part reduces the rated cargo.
- Earlier concerns (stay buckling, drum fade, cut edges, lithium-ion hazards on route C) are unchanged.

### Recommended next step

A TRL 3 refinement on paper: plate-and-joint FEA of the knuckle posts, head tube clamps, spine box and stays; a steering geometry study (caster, trail, kingpin inclination, self-centering with bought forks); and a mass review to recover margin under 70 kg. **TRL 4 is on hold by Amish's instruction.** For the record only, TRL 4 would need a partner and laser shop, DXF files, one frame cut and assembled, and lab tests of the proof load, knuckle posts, tipping threshold and braking.

## Session 2026-09-26: sources strengthened

Amish asked for the weaker sources to be fixed. README sections "Concept rationale" to "What sparked the idea" were checked link by link; every kept link was fetched and supports its claim.

| Where | Old source | New source |
| --- | --- | --- |
| What sparked the idea (Global Vehicle Trust OX) | CarsGuide, 2016 (trade press, alone) | TechCrunch, 27 September 2016, "The OX is a flat-pack truck for the developing world". The claim now states only what that report supports: six per shipping crate flat-packed, a trained team of three, about 12 hours. The 40 ft container, spanner and Allen key details were removed because they could not be verified from a primary or reputable source. |
| By country or region, row "Latin America (for example Mexico and Peru)" | None (uncited claim about *triciclo* vendors) | Rewritten as "The Americas (for example Mexico and Peru)", citing ILO, 2018: 40.0 % of employment in the Americas is informal |
| Burning platform, ITDP rickshaw sentence | ITDP, 2006 (kept) | Same source; wording corrected to match it: a single high gear, and a wooden passenger structure replaced every two to three years |

Kept and re-verified: ILO, 2018 (two billion, 61 %, 85.8 % Africa, 68.2 % Asia and the Pacific); Press Information Bureau, 2025 (more than 68 lakh vendors, lending extended to 31 March 2030); NYC DOT commercial cargo bicycle pilot evaluation report. The Gordon Murray Design press page could not be reached from this session, so no primary OX page is cited. `INSPIRATIONS.md` line for flattrike updated to the new source. No budget change. `docs/01-problem.md` does not cite CarsGuide, so it is unchanged; its IndiaMART price listing (a marketplace, cited alone) is outside this session's scope and is left for a later pass.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; it changes no dimension, interface, decision or number in the design.

### What was added

- `cad/src/product_model.py`: `product_parts()` returns 107 named parts (colour, material, BOM line, group and explode offset), plus `TITLE` and three `RENDER_VIEWS` (hero, exploded and a close "detail" of the core frame and drivetrain). It imports `PARAMS`, the plate profiles (`SPINE`, `STAY` and the bed profiles), `plate()` and the helpers from `model.py`, so every main dimension and interface is unchanged. It adds:
  - powder-coated flat 3 mm plates with laser-cut corner radii, the left and right plates as separate parts so the exploded view shows the flat-cut kit;
  - rib tabs showing through their slots, zinc M8 bolt heads, washers and locknuts at the spine, stay, bed and knuckle-post joints, and grooved cut spacer-washer stacks;
  - tyres with tread, 36-spoke wheels, drum brake hubs with brake arms, the 3-speed rear hub and its click box, axle nuts;
  - a toothed 32T chainring and 24T sprocket, a roller chain, a flat-cut chain guard ring, tapered cranks and platform pedals with pins;
  - headset cups, filleted fork crowns, rod ends on the drag link and tie rod;
  - a sprung saddle, rubber grips, brake levers, the parking latch, a bell and the cornering-speed label on the bar;
  - the plywood box with panel seams, counter lid, hinges, hasp and padlock, rubber corner bumpers, a name plate and reflectors; mudguards;
  - context: a produce crate strapped to the lid and the shared clay mannequin (1.76 m, pose "ride"), fitted from its landmarks so it sits on the saddle, its feet meet the pedals at the model's 55 degree crank angle and its hands meet the grips.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files are produced later by the orchestrator.

### Where the appearance model differs from model.py (each Proposed, awaiting Amish)

1. **Frame colour.** The spine side plates, stays, bed rails and knuckle posts are shown in the kit accent teal (#0F766E) powder coat, with graphite covers, ribs, yokes, bulkhead, axle beams and collar plates. BOM item 13 leaves the finish open. Recommendation: accept teal and graphite as the render finish only; choose the production coating with the partner.
2. **Chain side.** `model.py` puts the chain line at +44 mm on +Y, which its own axes call the left, while the precis (step 5) says the chain runs on the right. The appearance model keeps `model.py`, so the drivetrain is on the left and the detail view is taken from the front left. Recommendation: confirm right-hand drive (standard bicycle parts expect it) and flip the sign in `model.py` in the next CAD session.
3. **Yoke-to-collar bolts.** Four bolts are drawn just ahead of the head tube; BOM item 4 counts eight and `model.py` does not place them. Recommendation: accept as representative; place all eight in the plate-and-joint FEA session.
4. **Fork legs.** The bought forks are drawn with a small forward bend (18 mm) and a filleted crown; `model.py` shows straight legs. Dropout, crown height and width are unchanged. Recommendation: accept as appearance only; rake and trail belong to the steering geometry study.
5. **Tyre section.** Tyres are round in section (torus) with tread blocks instead of the flat-sided massing ring. Outer radius (254 mm) and width (54 mm) are unchanged. Recommendation: accept.
6. **Box hardware positions.** Hinges on the rear edge, hasp and padlock centred on the front face, corner bumpers and a name plate are placed for the render; BOM items 9 and 14 do not fix their positions. Recommendation: accept for renders; revisit with the lid-as-counter use once a partner is chosen.
7. **Chain guard.** BOM item 8 lists a chain guard without a form; it is shown as a flat-cut ring guard outside the chainring. Recommendation: accept, since it can be cut from the same sheet offcuts.
8. **Brake cable runs.** The long cable runs sit in the "context" group so they appear in the assembled hero but not across the exploded view. Recommendation: accept.

### TRL status

This is an appearance model only: no tolerances, no fabrication detail, no PCB or cut files. `trl` stays 3 and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: build plan and design for construction (kit 1.7.0)

Following Amish's 2026-09-30 approval of the build plan format, with outstanding decisions kept in a separate register, and his instruction: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- `cad/src/model.py` rewritten so every physical piece is its own solid: 35 cut plates with their tabs, slots, bolt holes and T-slots, the bought parts and 95 bolt sets (163 pieces). `python cad/src/model.py --check` runs the constructability checks: every tab, slot, hole and T-slot lies on solid plate; no two pieces overlap; every piece touches the assembly; and the wheels, forks, arms, drag link, tie rod and steering column sweep from full left to full right lock without touching the fixed structure. **All pass.** `build_parts()` still returns the twelve BOM groups for the calculations, concept media and drawing.
- `docs/decisions/0003-design-for-construction.md` (FTK-DDR-003, Draft): every change below, with the reason, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `cad/src/build_plan_media.py`: overview, making sketches FTK-DWG-101 to 123 (23 sheets), 14 joint close-ups and 21 assembly step pictures, all drawn from the model.
- `docs/05-build-plan.md` (FTK-BLD-001 v0.1) and `docs/06-design-decisions.md` (FTK-DEC-001 v0.1).
- `docs/04-calcs/sizing.py` now reads bolt, tab and node counts from the model; FTK-CAL-001 v0.3, FTK-REQ-001 v0.5 and FTK-PRC-001 v0.5 carry the new numbers. `bom/bom.csv` lines 1, 3, 4, 5, 8, 9, 10 and 11 respecified ($724, was $709). FTK-DWG-001 Rev P3; concept media regenerated (concept sheet Rev P2). `project.yaml`: `design_state: constructable`, evidence list. README: links line and "Building the prototype".

### Design changes made for construction (FTK-DDR-003)

1. Every plate joint made physical: tabs in slots carry the load; M8 bolts go through the face plate into a T-slot in the edge plate, with the all-metal locknut held in a window. Spine covers widened to 90 mm so their bolt holes have plate round them; ten tabs per edge in the closed box.
2. Two stay-to-spine bolts moved off the spine's rear window; a spacer tube inside the spine on each of the four bolts.
3. Rear dropouts opened to the stays' rear edge (they were closed holes).
4. Chain moved to the right-hand side (standard parts are right-hand drive).
5. Bottom bracket shell 60 mm, between the spine plates; its cups clamp the plates.
6. Bought seat tube in two cut saddles with shaft collars; the rib at 380 mm removed; oval hole in the top cover.
7. Yokes made the head tube clamps (cups through them); upper yoke between the spine plates, lower yoke under a new level edge of the spine; the two head tube collar plates removed.
8. Steering column from a bought forged-crown fork with its legs cut off; drop arm bolted under the crown.
9. Steering linkage made a parallelogram (120 mm drop arm parallel to the left steering arm): the concept's linkage locked after about 10° of right turn. The handlebar now turns as far as the left wheel.
10. Steering arms moved below the knuckle posts (321 mm up) on clamp plates held to the inboard fork legs by two U-bolts; knuckle posts and axle beams start at 350 mm (were 290 mm); axle beams 120 mm deep.
11. Knuckle posts rebuilt: post plates 25 mm either side of the head tube so the cup flange loads them directly (the concept's collar plates were bent by the wheel load); inner cheek a face plate; outer cheek inset; post plates step clear of the fork crown's sweep.
12. Bulkhead window split, bulkhead bottom raised 6 mm; rails extended 20 mm behind the bulkhead, rear lower edge raised, first window reduced.
13. Rails and axle beams joined by halving joints; beam windows moved off the crossings.
14. Box fixed by six bolts into the rails and two into the bulkhead on 9 mm washer stacks (box 9 mm further forward); counterbores in the box sides for the knuckle post bolt heads.
15. Front hubs 100 mm (they were drawn 106 mm in 100 mm forks).

### Key results (FTK-CAL-001 v0.3)

- Empty mass 71.2 kg (was 69.8 kg); gross 301.2 kg with the rated loads. **R1 and R8 are not met by 1.2 kg.**
- **R14 not met** for a knuckle post plate (about 53 min against 30 min); spine side plate about 80 min (met).
- R7 at risk: about 4.04 h for two people (95 bolt sets, was 116).
- R13 not met as before (241 W); R18 over its value-engineering target as before (about $465 against $300, USD 165 over). R2 and R11 at risk; R16 not verifiable.
- Plates 35 (was 34); true-shape nest 1,940 mm of 2,500 mm; stay buckling safety factor 2.01; knuckle post column 40 MPa (was 47 MPa); axle beam 36 MPa; tab bearing 87 MPa; tyre to knuckle post 36 mm at full lock (was 19 mm).
- Prototype parts $724 against the $800 value-engineering target (unchanged; USD 76 under).

### Proposed, awaiting Amish (all in `docs/06-design-decisions.md`)

1. Review and accept the design-for-construction changes (FTK-DDR-003).
2. Rated load and mass: cargo 148 kg (80 kg rider) and 138 kg (90 kg rider) and R8 72 kg now, and look for 1.2 kg at the FEA session (recommended).
3. R14: allow 60 min for knuckle post plates (recommended).
4. R7: accept 4.04 h and time it at TRL 4 (recommended).
5. Steering lock stops: two stop bolts on the lower yoke (recommended).
6. Steering ratio: keep 1:1 (recommended).
7. Steering geometry study; first partner (item 10); render colour and appearance model details from the 2026-09-26 session.

### Stale files (made on Amish's Mac, not regenerated here)

`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: the chain on the left, the head tube collar plates, steering arms at 400 mm, wider knuckle posts with windows, narrow spine covers and no visible tabs. They need updating with `/render-product`. The appearance deviations of 2026-09-26 item 2 (chain side) and item 3 (yoke-to-collar bolts) are now settled by FTK-DDR-003.

### Safety concerns

- The steering arms are held by U-bolt friction on the fork legs; their grip must be checked before any ride (build plan safety stops).
- The tab-and-slot joints carry the frame loads by bearing; they need FEA and a proof load (R2).
- Nothing stops the steering at 40° until stop bolts are added (open decision 5).
- Earlier concerns stand: rider-only tipping at 0.24 g, stay buckling, drum fade, cut edges.

### Recommended next step

Amish reviews FTK-DDR-003 and the register. Then a TRL 3 refinement on paper: plate-and-joint FEA with the tab joints, the mass review for decision 2, the steering stops and a steering geometry study; and new renders on the Mac. **TRL 4 remains on hold by Amish's instruction.**

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved the recommendations for every open decision: "i approve your recommendations for all 555 open decisions." The 10 open decisions of the design decisions register are now in its Decisions made table, dated 2026-10-02.

FTK-DDR-003 (design for construction) is accepted, with A1 to A3 decided as recommended. The cargo rating is restated at 148 kg with a rider up to 80 kg and 138 kg with a rider up to 90 kg, R8 at 72 kg and R14 at 60 min for a knuckle post plate, so R1, R8 and R14 are met on paper; R13 stays not met without assist and R18 over its value-engineering target. The calculation script still computes at the old rating until it is updated (follow-up 1). Item 5 was decided on a changed recommendation: steering lock stops at the knuckle posts rather than through-bolts in the lower yoke; the stop and the steering geometry study are now in safety stop S6 of the build plan.

### Documents changed

- `docs/06-design-decisions.md` (FTK-DEC-001 v0.3)
- `docs/decisions/0003-design-for-construction.md` (FTK-DDR-003 v0.3)
- `docs/01-problem.md` (FTK-PRB-001 v0.5)
- `docs/02-concept.md` (FTK-PRC-001 v0.7)
- `docs/03-requirements.md` (FTK-REQ-001 v0.7)
- `docs/04-calcs/01-sizing.md` (FTK-CAL-001 v0.5)
- `docs/05-build-plan.md` (FTK-BLD-001 v0.3)
- `README.md` (not a controlled document)

### Follow-up actions to carry approved decisions into the design

1. Decision 2: Calculations: change the rated cargo in `docs/04-calcs/sizing.py` to 148 kg (80 kg rider) and 138 kg (90 kg rider) and R8 to 72 kg, and rerun so the mass, tipping and braking figures and `results.csv` use the restated rating and statuses.
2. Decision 2: Model and calculations: try lightening windows in the knuckle post arms and yokes (about 0.5 kg) and a lighter box in the FEA session; set the final load label from the weighed trike.
3. Decision 3: Calculations: change R14's target in `sizing.py` to 60 min for a knuckle post plate.
4. Decision 5: Model: add a steering lock stop at each knuckle post that its steering arm clamp plate meets at 40 degrees, with a constructability check that the stop is met at 40 degrees on both sides.
5. Decision 5: Drawings: add a making sketch for the lock stop and show it on FTK-DWG-001.
6. Decision 5: Build plan pictures: show the lock stops in the knuckle post making sketch and in steps 14 and 17, and list the stop in the build plan's parts (review flag 2).
7. Decision 5: BOM: add the two lock stops (and their bolts) to the knuckle post line.
8. Decision 7: Calculations: add a steering geometry study (caster, trail, kingpin inclination, scrub radius, self-centring) to FTK-CAL-001 in the FEA session, with the bought fork's rake as input, before the first ride.
9. Decision 1: Calculations: compute the turning circle from the built linkage (31.3 degrees at the outer wheel) instead of ideal Ackermann (review flag 1).
10. Decision 1: Renders: regenerate the photoreal renders, `media/card.png` and `media/social-preview.png` on Amish's Mac to show the accepted design for construction (items 9 and 10 follow with them).

### Points found in the review

1. The turning circle calculation still uses ideal Ackermann, while the built linkage gives 31.3 degrees at the outer wheel against 29.5 degrees ideal.
2. Item 5 says the stop is 'a part to add before the first ride, not before the build'; since it is safety-critical, it should be in the build plan's parts list.

No CAD model, BOM quantity or price, calculation result or picture was changed. TRL stays at 3; TRL 4 remains on hold.

## Session 2026-10-02: approved follow-ups carried out

Amish approved carrying out every follow-up action from the open-decision sign-off ("APPROVED CHANGES, COMPLETE THESE") and preparing the render scenes. This session carried the decisions of 2026-10-02 into the model, BOM, calculations, drawings, pictures and appearance model. TRL stays at 3; TRL 4 remains on hold.

### Follow-ups

1. Rated cargo 148 and 138 kg and R8 72 kg in `sizing.py`: **done.** Re-run on the model with the lock stops: empty 71.7 kg (0.3 kg under R8), gross 299.7 kg in both cases; tipping, braking and `results.csv` at the restated rating.
2. Lightening windows and a lighter box; final load label: **not done:** the decision places the trial in the FEA session and the label on the weighed trike (TRL 4). The R8 margin is now only 0.3 kg, so the trial matters.
3. R14 60 min for a knuckle post plate in `sizing.py`: **done** (53 min, 7 min margin).
4. Steering lock stop at each knuckle post with a constructability check: **done.** A 77 x 130 mm fin tabbed and bolted to each front knuckle post plate; the steering arm clamp plates lengthened to 93 mm so their front inboard corner meets it. `python cad/src/model.py --check` passes: 167 components, 37 plates, 97 bolt sets, no overlaps, no sweep issues, each clamp plate meets its stop at 40° and not 1° before. STEP and STL regenerated.
5. Making sketch for the lock stop and the stop on FTK-DWG-001: **done** (FTK-DWG-124 P1; FTK-DWG-001 Rev P4 with a lock stop note and the new figures).
6. Lock stops in the knuckle post making sketch, steps 14 and 17 and the build plan parts: **done** (FTK-DWG-114 P2, FTK-DWG-119 P2, new section 3.24, steps 13 to 21 and joints 9 and 11 redrawn).
7. Two lock stops and bolts in BOM line 3: **done** ($89, was $85; basis in `bom/bom-notes.md`). Base prototype $728.
8. Steering geometry study: **done as a first pass** (FTK-CAL-001 section 5a): head tubes vertical, so no caster, kingpin inclination or scrub; a fork fitted with its offset forward gives negative trail (about 6.6 N·m per wheel pulling into the turn at 0.2 g with a 30 mm offset). The repeat with the chosen fork's measured rake stays in the FEA session, as decided.
9. Turning circle from the built linkage: **done.** 31.3° at the outer wheel; 5.64 m outer tyre circle (5.95 m upper bound).
10. Photoreal renders, `media/card.png` and `media/social-preview.png`: **not done:** made on Amish's Mac. The appearance model and render scenes are prepared (below).

### Requirement status changes

None. R1, R8 and R14 stay met on paper (now computed rather than restated); R8's margin fell from 0.8 kg to 0.3 kg. R7 is about 4.07 h (97 bolt sets), still at risk as accepted. R9 improves to 5.64 m. R15: Value-engineering target: USD 800. Estimated cost of the constructable design: USD 728 (USD 72 under the target). R18 about $466, USD 166 over its target.

### Documents changed

- `cad/src/model.py`, `cad/step/*`, `cad/stl/*` (lock stops, longer clamp plates, lock stop check)
- `bom/bom.csv`, `bom/bom-notes.md`
- `docs/04-calcs/sizing.py`, `docs/04-calcs/results.csv`, `docs/04-calcs/01-sizing.md` (FTK-CAL-001 v0.6)
- `docs/03-requirements.md` (FTK-REQ-001 v0.8)
- `docs/02-concept.md` (FTK-PRC-001 v0.8)
- `docs/05-build-plan.md` (FTK-BLD-001 v0.4): new section 3.24 and Figure 37 (later figures renumbered); "Pictures unchanged" no longer applies
- `docs/06-design-decisions.md` (FTK-DEC-001 v0.4): value engineering restated
- `cad/drawings/FTK-DWG-001` Rev P4; `FTK-DWG-114` P2, `FTK-DWG-119` P2, `FTK-DWG-124` P1 (new)
- `docs/05-build-plan/overview.png`, `joint-09.png`, `joint-11.png`, `step-13.png` to `step-21.png`
- `media/` concept media (blueprint FTK-DWG-010 P3, hero, exploded, flow, model.glb)
- `cad/src/product_model.py`: the frame, bed, knuckle posts, lock stops, steering and every bolt set now come from `model.build_components()`; chain guard and crank spider moved outboard of the right-hand chain line. Render scenes exported to `/home/claude/renders/flattrike` (hero, exploded, detail)
- `README.md` (not a controlled document)

### Appearance model deviations (each Proposed, awaiting Amish)

- The plates are drawn as cut (no extra corner radii), and the wheels, drivetrain, seat, bars, box hardware and cable runs keep their 2026-09-26 appearance detail. Recommendation: accept as appearance only.

### Cross-repo actions

None.

### Safety concerns

- A knuckle fork fitted as sold, offset forward, gives negative trail on the vertical knuckle head tubes; the steering would pull into turns. Settle fork orientation or caster in the FEA-session study before the first ride (S6).
- The lock stop takes the whole bar torque on one side (about 0.84 kN); its fin and bolt are within limits on paper.

### Recommended next step

Renders on Amish's Mac from the exported scenes; then the FEA session (plate-and-joint FEA, lightening windows for the 0.3 kg R8 margin, and the steering geometry study with the chosen fork). **TRL 4 remains on hold by Amish's instruction.**

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.

## Session 2026-10-03: fork direction settled (forks turned to trail)

On 2026-10-03 Amish wrote: "FlatTrike - i accept your design recommendation, proceed and execute the solution for fork direction or caster". The first-pass study (FTK-CAL-001 v0.6, section 5a) had named turning each knuckle fork round so its offset trails as the first option; this session carried it out. TRL stays at 3; TRL 4 remains on hold.

### Solution and why

- Each knuckle fork is a 20 in steel fork with a threaded 1 1/8 in steerer and straight BMX-type legs parallel to the steerer, 30 to 40 mm offset, fitted turned round so the axle trails the vertical knuckle head tube. Mechanical trail 35 mm in the model (30 to 40 mm over the fork range); caster 0°, kingpin inclination 0°, scrub 0 mm, all measured on the model by `model.py --check`.
- Why this and not head tube caster: it needs no new or angled plates, keeps the knuckle posts, collar plates, headsets, ride height and linkage as they are, and gives no wheel flop. Caster would have meant redrawing the knuckle posts round a tilted head tube. Straight legs are needed because the steering arm clamps to the leg; a bent-leg fork turned round would put the clamp on the bend.
- Why 35 mm: 30 to 70 mm is the target band (below about 30 mm the centring torque is small against the friction of three headsets and two rod-end links; above about 70 mm the 2.25 kN front load makes the bar heavy and kicks back). The lower part of the band suits a slow, tightly steered front loader, and 35 mm comes from stock forks. Centring torque at the column 15.7 N·m at 0.2 g loaded (26 N per grip).

### Knock-on changes and effects

- Wheelbase 1.45 to 1.415 m (kingpins unchanged at 1.45 m). Turning circle 5.64 to **5.52 m** (R9 met; 5.86 m upper bound). Tipping thresholds rise slightly (0.42 g loaded, 0.24 g rider only; R10 met). Lock 40°, Ackermann arms, tie rod, toe (zero) and 1:1 bar ratio unchanged; tyre scrub at full lock 0.20 m (was 0.18 m).
- Bed rails: a tyre notch 55 mm up into the lower edge, 1,200 to 1,305 mm from the rear axle, because the trailing inner tyre swings 22.5 mm further across at full lock and otherwise struck the rail. 39 MPa in the 55 mm of plate left. Two rail windows shortened.
- Knuckle post plates: lower lip 8 mm past the outer cheek (was 10 mm) for the fork crown's larger swing.
- Steering arm clamp plates 67 x 40 mm (inboard end 104 mm from the kingpin, was 130 mm), steering arms shorter, lock stop fins 34 x 130 mm (were 77 x 130 mm). Stop force 0.82 kN at 109 mm.
- Least running clearances over the sweep (new check, 5 mm minimum): inner tyre to the box side **7.7 mm** at full lock (about 33 mm before); fork crown to knuckle post plate 5.9 mm.
- Mass 71.6 kg empty (0.4 kg under R8). Rear axle load falls (0.69 kN loaded); rear tyre grip needed on 5 % rises from 0.26 to 0.28.
- Cost: BOM line 5 $92 to $100 (straight-leg forks about $4 more each). Base prototype **$736** (USD 64 under the $800 target); production about $471 (R18 USD 171 over).

### Files changed

- `cad/src/model.py` (FORK_OFFSET, axle_x(), TRAIL_RANGE, RAIL_NOTCH, POST_LIP, CLAMP_IN; new trail, scrub and running-clearance checks), `cad/step/*`, `cad/stl/*`. `python cad/src/model.py --check`: PASS (167 components, 0 overlaps, 0 floating, 0 joint, sweep, lock stop, clearance or geometry issues).
- `docs/04-calcs/sizing.py`, `results.csv`, `01-sizing.md` (FTK-CAL-001 v0.7; section 5a rewritten)
- `docs/03-requirements.md` (FTK-REQ-001 v0.9), `docs/02-concept.md` (FTK-PRC-001 v0.9), `docs/05-build-plan.md` (FTK-BLD-001 v0.5), `docs/06-design-decisions.md` (FTK-DEC-001 v0.5), `bom/bom.csv`, `bom/bom-notes.md`, `README.md`
- Drawings: FTK-DWG-001 Rev P5; FTK-DWG-112 P2, 114 P3, 116 P2, 118 P2, 119 P3, 124 P2
- Build plan pictures: `overview.png`, `joint-08.png`, `joint-09.png`, `joint-11.png`, `step-11.png` to `step-21.png`
- Concept media (blueprint FTK-DWG-010 P4, hero, exploded, flow, model.glb)
- `cad/src/product_model.py`: front wheels and mudguards at the trailing axle; forks come from the model (straight legs). Render scenes exported to `/home/claude/renders/flattrike` (hero, exploded, detail). Photoreal renders, `media/card.png` and `media/social-preview.png` not redone (Amish's Mac).

### Proposed, awaiting Amish

1. Front mudguards: with 7.7 mm from tyre to box side at full lock, a full-length front mudguard would rub the box. Options: (a) short front mudguards that stop above the axle at the rear; (b) reduce the inner lock to about 37° (turning circle about 5.8 m, R9 still met); (c) no front mudguards. Recommendation: (a).
2. The 2026-10-02 appearance decision accepted "bent fork legs" as appearance only; the forks are now straight-leg by design and the appearance model already shows them straight. Recommendation: note that item as superseded.

### Safety concerns

- A fork fitted as sold (legs forward) gives 35 mm of negative trail and pulls the steering into turns. Step 16 now has a hold point and S6 requires both forks checked turned round before the first ride.
- Pneumatic trail, shimmy and kickback with 35 mm trail are not quantified; the FEA session repeats the geometry with the chosen fork's measured offset.

### Recommended next step

Photoreal renders and cards on Amish's Mac from the exported scenes; then the FEA session (plate-and-joint FEA, lightening windows for the 0.4 kg R8 margin, steering geometry with the measured fork). **TRL 4 remains on hold by Amish's instruction.**

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
