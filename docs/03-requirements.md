---
doc_id: FTK-REQ-001
title: FlatTrike requirements
project: FlatTrike
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with concept status
---

# FlatTrike requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see FTK-PRB-001). The status column gives the TRL 2 concept's position against each target from the first-order estimates in FTK-PRC-001. Four requirements are **not met** by the current concept: R8 (empty mass), R10 (stability with no cargo), R13 (hill climb without assist) and R15 when the electric assist option is included.

The **design load case** used throughout is an 80 kg rider and 150 kg of cargo in the box on a trike of about 68 kg: about 300 kg gross, on a flat dry road unless stated.

Table 1. FlatTrike requirements and concept status.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Carry the rated load | 150 kg of cargo in the box plus a rider up to 90 kg; gross mass 300 kg or less, within the EN 17860 cargo cycle class | Mass budget; load case review | Met, no margin: about 298 kg with an 80 kg rider |
| R2 | Frame strength | Frame survives a static proof load of twice the rated payload with no permanent set, and a fatigue load case representative of commercial use under EN 17860 | Hand calculation and FEA of plates and bolted joints; later proof test | Unverified; first-order plate stresses are low (about 26 MPa), fatigue at bolt holes is the open risk |
| R3 | No welding | Every steel part is flat 3 mm plate cut from a DXF file by laser or waterjet; no bending, welding or brazing; joints bolted with locknuts | Design review of the model and part list | Met by design |
| R4 | One standard sheet | All steel frame parts nest on one 1,250 x 2,500 x 3 mm sheet (4 x 8 ft class) | Nesting study | Likely met: about 1.5 m² of parts on a 3.1 m² sheet |
| R5 | Standard bicycle parts | Wheels (20 in, ISO 406), hubs, brakes, headset (1 1/8 in), bottom bracket, cranks, chain (1/8 in), seatpost (27.2 mm) and saddle are standard sizes sold in regional markets | Parts availability survey with the partner | Met by design, except the head tube and bottom bracket housings (see FTK-PRC-001) |
| R6 | Ships flat | Complete kit, wheels included, packs into 0.4 m³ or less with no piece longer than 1.0 m | Packing study | Likely met: about 1.0 x 0.8 x 0.45 m, about 0.36 m³ |
| R7 | Assembled with hand tools | Two people assemble the kit in 4 h or less with spanners to 17 mm, hex keys, cone spanners and a screwdriver; no jig, because the plates locate each other with tabs and slots | Assembly sequence review; later timed build | Unverified |
| R8 | Light enough to ride and push | Empty mass 55 kg or less, matching the improved rickshaw documented by ITDP | Mass estimate; later weighing | **Not met:** about 68 kg (plates about 30 kg, plywood box about 16 kg) |
| R9 | Fits market lanes | Overall width 1.0 m or less; length 2.2 m or less; turning circle 6 m or less | Model check | Met: about 0.96 m wide, 2.11 m long, turning circle about 5.8 m |
| R10 | Resist tipping in turns | Lateral acceleration at the tipping point 0.30 g or more, both loaded and with the rider only | Stability calculation; later tilt-table test | **Not met with no cargo:** about 0.18 g; met loaded, about 0.38 g |
| R11 | Stop and park safely | Stop from 15 km/h in 6 m or less at gross mass on a dry road; drum brakes on all three wheels; a parking brake that holds the loaded trike on a 10 % grade | Braking calculation; later field test | Unverified; the required deceleration (about 1.5 m/s²) is modest, but drum fade on long descents is a risk |
| R12 | Pedal on the flat | Cruise at 7 km/h or more at gross mass on a flat dirt road with 110 W at the pedals | Power calculation | Met: about 7.6 km/h |
| R13 | Climb local hills | Climb a 5 % grade for 100 m at 4 km/h or more at gross mass without the rider dismounting | Power and gearing calculation | **Not met without assist:** needs about 210 W at the wheel, about twice sustained rider output; met with the optional 250 W assist |
| R14 | Repairable locally | Any single plate or standard part replaced in 30 min or less with hand tools; open DXF files let any laser shop re-cut one plate | Design review; later repair trial | Met by design; unverified in practice |
| R15 | Affordable prototype | Prototype parts cost $800 or less (`project.yaml` budget) | Priced BOM (`bom/bom.csv`) | Met for the pedal-only base, about $640. **Not met** with the optional electric assist, about $1,040 |
| R16 | Last in commercial service | Frame life of 5 years or more in daily outdoor commercial use, against 2 to 3 years for traditional wooden rickshaw frames (ITDP) | Corrosion and fatigue review; later field trial | Unverified |
| R17 | Work as a stall | Lockable box of 150 L or more; box lid usable as a counter at 0.75 to 0.95 m height | Model check | Met: about 190 L inside; lid at about 0.79 m |

## Assumptions

- Rolling resistance coefficient about 0.015 on a mix of worn asphalt and packed dirt; drag area about 0.9 m² for an upright rider behind a cargo box; air density 1.2 kg/m³.
- The rider sustains about 110 W at the pedals for an hour; short efforts can reach 200 W or more.
- Drivetrain efficiency (chain and 3-speed hub) about 89 %.
- Plate is 3 mm hot-rolled mild steel (S235JR or ASTM A36 class), density 7,850 kg/m³.
- Plywood is 9 to 12 mm exterior grade, about 700 kg/m³.
- The 300 kg gross limit follows the EN 17860 class for single and multi-track cargo cycles; the standard's detailed test loads have not yet been checked against this design.
