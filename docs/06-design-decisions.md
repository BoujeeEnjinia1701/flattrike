---
doc_id: FTK-DEC-001
title: FlatTrike design decisions register
project: FlatTrike
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open items from the review note, the decision records and the build work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for all open decisions 1 to 10 on 2026-10-02 (FTK-DDR-003 accepted; rating 148 and 138 kg, R8 72 kg, R14 60 min for knuckle post plates; steering stops at the knuckle posts); moved to decisions made"
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Value engineering restated after the 2026-10-02 decisions were carried into the design (lock stops in BOM line 3; FTK-CAL-001 v0.6)"
- version: "0.5"
  date: '2026-10-03'
  author: Amish Chadha
  change: "Fork direction decided by Amish 2026-10-03 (knuckle forks turned to trail, 35 mm mechanical trail); knuckle fork added to the items to confirm; value engineering restated (BOM line 5 $100; FTK-CAL-001 v0.7)"
---

# FlatTrike design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 1. Items to confirm when parts are bought.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1a | The two knuckle forks: 20 in steel, 100 mm dropouts, threaded 1 1/8 in steerer, straight legs parallel to the steerer with 30 to 40 mm offset (measure it); 22 mm legs | Fitted turned round, the offset is the trail (30 to 40 mm); a bent-leg fork would put the steering arm clamp on the bend | FTK-CAL-001 section 5a; decided 2026-10-03 |
| 1 | The steering column fork: threaded 1 1/8 in steel fork with a separate forged crown (roadster type) solid enough to drill two 9 mm holes 32 mm either side of the steerer; steerer at least 250 mm | The drop arm bolts under the crown | FTK-DDR-003, P8 |
| 2 | A quill stem with about 350 mm of quill for a 1 1/8 in threaded steerer, 70 mm or more inside the steerer | It sets the handlebar height of 850 mm | FTK-DDR-003, P8 |
| 3 | Front fork leg diameter (22 mm assumed) and M6 U-bolts that fit it; the U-bolts' grip holds the steering arm under a firm push on the bar | The steering arms are held by friction on the leg | FTK-DDR-003, P10 |
| 4 | Front drum hub body 90 mm across or less where the steering arm clamp plate passes over it | The clamp plates clear a 90 mm hub by about 6 mm | FTK-DDR-003, P10 |
| 5 | Rod ends for M8 bolts with at least ±10° misalignment | The drag link slopes about 6° | FTK-DDR-003, P9 |
| 6 | Headset cups' spigots long enough to pass a 3 mm plate and still seat 10 mm in the head tube | The cups clamp the yokes and collar plates | FTK-DDR-003, P7 and P11 |
| 7 | A cartridge bottom bracket for a 68 mm shell that works with 66 mm between the cup flanges (60 mm shell and two 3 mm plates) | The cups clamp the spine plates | FTK-DDR-003, P5 |
| 8 | Hub axles long enough for 3 mm dropouts plus non-turn washers and nuts; front drum reaction arms that fit the forks | The dropouts are thinner than a bicycle frame's | FTK-DDR-003, P3 |
| 9 | Drum brake torque of about 37 N·m per wheel, and the 3-speed hub's input torque limit for 32/24 gearing | R11 and the hub's life | FTK-CAL-001; BOM lines 6 and 7 |
| 10 | The laser or waterjet shop holds slot widths to about 0.1 mm (3.4 mm slots for 3 mm tabs) | Tabs must enter by hand and not rattle | FTK-DDR-003, P1 |
| 11 | Seat tube 31.8 x 2.3 mm whose bore takes a 27.2 mm seatpost | The seatpost clamps in it | FTK-DDR-003, P6 |

## Value engineering

Value-engineering target: USD 800 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 736 (USD 64 under the target). Main cost drivers and savings worth trying:

- The largest prototype lines are the two front wheels with drum brakes (USD 110), the rear wheel with 3-speed drum hub (USD 95), the steering column, knuckles and linkage (USD 100) and the front bed and knuckle post plates with the steering lock stops (USD 89). The construction changes (FTK-DDR-003) added USD 15 (USD 709 to USD 724), the two lock stops and their bolts USD 4 (USD 724 to USD 728), and the straight-leg knuckle forks fitted turned to trail USD 8 (USD 728 to USD 736).
- The optional route C assist kit (USD 300, without the SwapCell pack) is outside the prototype target.
- Production target: USD 300 per trike at 100 units (R18) against an estimate of about USD 471, USD 171 over the target. Bought bicycle parts are USD 329 of it at 65 % of retail, with USD 74 of steel (one full sheet), USD 17 of cutting, the plywood box at 60 % and USD 15 of assembly labour.
- Savings worth trying: wholesale prices for wheels, hubs and forks once the first partner supplies them (FTK-DDR-002, item 18), and the one-sheet nest that already keeps the steel and cutting low.

## Decisions made

*Table 2. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 9, 11 and 12: tadpole front loader; box steering first with Ackermann assessed; no assist in the prototype, route C (SwapCell) preferred; 3 mm S235 or A36 plate, painted; M8 8.8 bolts with all-metal locknuts; bought head tube and bottom bracket sections; 20 in wheels with drum brakes and a 3-speed rear hub; design changes before relaxing R8 and R10; $300 production target (R18); `budget_usd` $800 for the pedal-only prototype; problem line reworded | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | FTK-DDR-001 |
| 2026-09-25 | Cross-cutting: SwapCell interface v0.3 items W, C and V for assist route C; a SwapCell pack is priced once in the SwapCell repo; partners are picked per area later | Amish, same instruction | FTK-DDR-001 |
| 2026-09-25 | Items 13 to 19: Ackermann steering with a fixed box; R8 70 kg; R10 rider-only 0.22 g with a cornering-speed label; 140 kg cargo for riders over 80 kg; R14 90 min for a spine side plate; keep the $300 target; 200 mm head tube | Amish: "i accept all your recommendations, go with them across all repos." | FTK-DDR-002 |
| 2026-09-25 | TRL 4 on hold; the repo stays at TRL 3 | Amish's instruction | `project.yaml`; review note |
| 2026-09-26 | FlatTrike in the first batch of product renders | Amish | Review note, 2026-09-26 |
| 2026-09-30 | Write the illustrated build plan and make the design physically buildable as it is drawn; keep open decisions out of the build plan, in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." and "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | FTK-DDR-003 (Draft, open for review); this register |
| 2026-10-02 | Design for construction accepted: the changes P1 to P15 of FTK-DDR-003 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | FTK-DDR-003, Tables 1 and 2 |
| 2026-10-02 | Rated load (option c): rated now at 148 kg of cargo with a rider up to 80 kg, or 138 kg with a rider up to 90 kg, and R8 relaxed to 72 kg; the lightening windows are tried in the FEA session, and the final load label is set from the weighed trike | Amish: "i approve your recommendations for all 555 open decisions." | FTK-DDR-003, A1 |
| 2026-10-02 | Repair time: 60 min allowed for a knuckle post plate (R14) | Amish: "i approve your recommendations for all 555 open decisions." | FTK-DDR-003, A2 |
| 2026-10-02 | Assembly time: about 4.04 h accepted against R7's 4 h, timed at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | FTK-DDR-003, A3 |
| 2026-10-02 | Steering lock stops (option b, changed from a): a stop at each knuckle post that its steering arm clamp plate meets at 40 degrees, fitted before the first ride | Amish: "i approve your recommendations for all 555 open decisions." | Build plan work; this register |
| 2026-10-02 | Steering ratio: the 1:1 parallelogram linkage is kept | Amish: "i approve your recommendations for all 555 open decisions." | FTK-DDR-003, P9 |
| 2026-10-02 | Steering geometry: caster, trail, kingpin inclination, scrub radius and self-centring are studied on paper in the FEA session, with the bought fork's rake as input, before the first ride | Amish: "i approve your recommendations for all 555 open decisions." | FTK-PRC-001, open questions |
| 2026-10-02 | First partner and city: kept open under the portfolio rule, chosen as a city with dense goods delivery on narrow streets, a laser-cutting shop and a bicycle parts market. First candidate type to approach: a cycle-rickshaw or cargo-bike programme such as those the Institute for Transportation and Development Policy (ITDP) has documented in South Asia | Amish: "i approve your recommendations for all 555 open decisions." | FTK-DDR-002, item 10 |
| 2026-10-02 | Render frame colour: teal and graphite for the renders only; the coating is chosen with the partner | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, item 1 |
| 2026-10-02 | Appearance model details (bent fork legs, round tyre section, box hardware positions, flat-cut chain guard, brake cable runs) accepted as appearance only | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, items 4 to 8 |
| 2026-10-03 | Fork direction (steering geometry before the first ride): each knuckle fork is a straight-leg fork with 30 to 40 mm offset, fitted turned round so the wheel trails its vertical steering axis; 35 mm of mechanical trail, no caster; bed rails notched and knuckle post lip trimmed for the swinging tyre and crown; wheelbase 1.415 m, turning circle 5.52 m | Amish: "FlatTrike - i accept your design recommendation, proceed and execute the solution for fork direction or caster" | FTK-CAL-001 section 5a; review note 2026-10-03 |
