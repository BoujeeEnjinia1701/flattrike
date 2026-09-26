---
doc_id: FTK-REQ-001
title: FlatTrike requirements
project: FlatTrike
doc_type: Requirements
version: "0.4"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from FTK-CAL-001; R15 budget scope redefined; new R18 production cost target (FTK-DDR-001)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# FlatTrike requirements

These requirements are checked by calculation in FTK-CAL-001 v0.2 against the TRL 3 parametric model. Targets are still proposals until co-design sessions with users (see FTK-PRB-001). Amish's decisions of 2026-09-25 redefine what the prototype budget covers (R15) and add a production cost target (R18) (FTK-DDR-001), and then restate R1, R8, R10 and R14 and keep R18 as it is (FTK-DDR-002). Two requirements are **not met** at TRL 3: R13 without assist and R18 (production cost). R1 and R8 are met with only 0.2 kg of margin.

The **design load case** is an 80 kg rider and 150 kg of cargo in the box on a trike of 69.8 kg: 299.8 kg gross, on a flat dry road unless stated. The upper case is a 90 kg rider with 140 kg of cargo, also 299.8 kg.

Table 1. FlatTrike requirements and TRL 3 status (FTK-CAL-001 v0.2).

| ID | Requirement | Target | Verification | TRL 3 status |
| --- | --- | --- | --- | --- |
| R1 | Carry the rated load | 150 kg of cargo in the box with a rider up to 80 kg, or 140 kg with a rider up to 90 kg; gross mass 300 kg or less, within the EN 17860 cargo cycle class (restated, FTK-DDR-002) | Mass budget (FTK-CAL-001 section 3) | Met: 299.8 kg in both cases (0.2 kg margin) |
| R2 | Frame strength | Frame survives a static proof load of twice the rated payload with no permanent set, and a fatigue load case representative of commercial use under EN 17860 | Hand calculation (section 6); FEA next; proof test later | At risk: stresses 47 MPa or less and fatigue ranges below the limit, but stay buckling has a safety factor of only 2.09 and the knuckle post columns reach 47 MPa |
| R3 | No welding | Every steel part is flat 3 mm plate cut from a DXF file by laser or waterjet; no bending, welding or brazing; joints bolted with locknuts | Model review | Met: 34 plates and 72 spacer washers, all flat |
| R4 | One standard sheet | All steel frame parts nest on one 1,250 x 2,500 x 3 mm sheet (4 x 8 ft class) | Nesting check (section 2) | Met: 2,190 mm of sheet used by a true-shape nest; bounding rectangles alone would need 2,805 mm |
| R5 | Standard bicycle parts | Wheels (20 in, ISO 406), hubs, brakes, forks (20 in), headsets (1 1/8 in), bottom bracket, cranks, chain (1/8 in), seatpost (27.2 mm) and saddle are standard sizes sold in regional markets | Parts availability survey with the partner | Met by design, with the head tubes and bottom bracket shell as bought steel sections (decided); survey pending |
| R6 | Ships flat | Complete kit, wheels included, packs into 0.4 m³ or less with no piece longer than 1.0 m | Packing estimate | Met: about 0.30 m³; longest piece 0.83 m |
| R7 | Assembled with hand tools | Two people assemble the kit in 4 h or less with spanners to 17 mm, hex keys, cone spanners and a screwdriver; no jig, because the plates locate each other with tabs and slots | Work-content estimate; later timed build | At risk: about 4.0 h for 116 bolt sets and the steering linkage, at the limit |
| R8 | Light enough to ride and push | Empty mass 70 kg or less including the box (relaxed from 55 kg, FTK-DDR-002); still lighter than the 80 kg traditional rickshaw documented by ITDP | Mass budget | Met: 69.8 kg (0.2 kg margin) |
| R9 | Fits market lanes | Overall width 1.0 m or less; length 2.2 m or less; turning circle 6 m or less | Model and steering geometry | Met: 0.986 m wide, 2.14 m long, 5.95 m turning circle at 40° inner lock |
| R10 | Resist tipping in turns | Lateral acceleration at the tipping point 0.30 g or more loaded, and 0.22 g or more with the rider only together with a cornering-speed label (rider-only case relaxed, FTK-DDR-002) | Stability calculation (section 5); later tilt-table test | Met: 0.41 g loaded and 0.24 g rider only at any lock; label reads 6 km/h for full-lock turns when empty |
| R11 | Stop and park safely | Stop from 15 km/h in 6 m or less at gross mass on a dry road; drum brakes on all three wheels; a parking brake that holds the loaded trike on a 10 % grade | Braking calculation (section 7); later field test | At risk: each drum needs about 37 N·m (rating not yet confirmed); fade after about 1.9 km of loaded 5 % descent |
| R12 | Pedal on the flat | Cruise at 7 km/h or more at gross mass on a flat dirt road with 110 W at the pedals | Power calculation | Met: 7.6 km/h |
| R13 | Climb local hills | Climb a 5 % grade for 100 m at 4 km/h or more at gross mass without the rider dismounting | Power and gearing calculation | **Not met without assist:** 240 W needed at the pedals. Met with assist route C (6.0 km/h), which is not in the prototype |
| R14 | Repairable locally | Any single plate or standard part replaced in 30 min or less with hand tools, except a spine side plate in 90 min or less (FTK-DDR-002); open DXF files let any laser shop re-cut one plate | Bolt-count estimate; later repair trial | Met: spine side plate about 78 min; knuckle post plate about 27 min |
| R15 | Affordable prototype | Parts for the pedal-only prototype cost $800 or less (`project.yaml` budget). The optional assist kit and any SwapCell pack are outside this budget; a SwapCell pack is priced once in the SwapCell repo | Priced BOM (`bom/bom.csv`) | Met: $709 |
| R16 | Last in commercial service | Frame life of 5 years or more in daily outdoor commercial use, against 2 to 3 years for traditional wooden rickshaw frames (ITDP) | Corrosion and fatigue review; later field trial | Not verifiable at TRL 3: unprotected steel could lose up to 0.42 mm in 5 years; depends on coating and sealed joints |
| R17 | Work as a stall | Lockable box of 150 L or more; box lid usable as a counter at 0.75 to 0.95 m height | Model check | Met: 151 L inside; lid at 0.84 m |
| R18 | Competitive in production | Production cost of $300 or less per trike at 100 units (decided by Amish, 2026-09-25; kept, FTK-DDR-002) | Cost estimate (section 9); later partner quotes | **Not met:** about $456, over two thirds of it bought bicycle parts; wholesale prices wait on a partner |

## Assumptions

- Rolling resistance coefficient about 0.015 on a mix of worn asphalt and packed dirt; drag area about 0.9 m² for an upright rider behind a cargo box; air density 1.2 kg/m³.
- The rider sustains about 110 W at the pedals for an hour; short efforts can reach 200 W or more.
- Drivetrain efficiency (chain and 3-speed hub) about 89 %.
- Plate is 3 mm hot-rolled mild steel (S235JR or ASTM A36 class), density 7,850 kg/m³.
- Plywood is 9 to 12 mm exterior grade, about 700 kg/m³.
- Volume prices (R18) assume one full sheet at $1.0/kg, cutting at $0.30/m and bought parts at 65 % of prototype retail; no quotes yet.
- The 300 kg gross limit follows the EN 17860 class for single and multi-track cargo cycles; the standard's detailed test loads have not yet been checked against this design.
