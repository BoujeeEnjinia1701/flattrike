---
doc_id: FTK-DEC-001
title: FlatTrike design decisions register
project: FlatTrike
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
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
---

# FlatTrike design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, all Proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Review the design-for-construction changes P1 to P15 (joints, stay bolts, dropouts, chain side, bottom bracket, seat tube, yokes as head tube clamps, steering column, parallelogram steering linkage, steering arms under the knuckle posts, knuckle posts, bulkhead, halving joints, box fixing, front hub width) | Accept; or reject single changes | Accept: each one is needed for the trike to be built and none changes what it does | The whole build plan follows them | FTK-DDR-003, Table 1 |
| 2 | Rated load and empty mass: the construction changes add 1.4 kg, so R1 and R8 fail by 1.2 kg (empty 71.2 kg, gross 301.2 kg) | (a) cargo 148 kg with a rider up to 80 kg and 138 kg with a rider up to 90 kg, R8 72 kg; (b) find 1.2 kg (windows in the knuckle post arms and yokes, a lighter box); (c) both | (c): (a) now, so the rating is true; (b) in the FEA session | The load label and the first load check | FTK-DDR-003, A1 |
| 3 | Repair time of a knuckle post plate: about 53 min against R14's 30 min, because both collar plates and the headset cups come off to release it | (a) allow 60 min for knuckle post plates; (b) redesign the post | (a) | None now | FTK-DDR-003, A2 |
| 4 | Assembly time about 4.04 h against R7's 4 h | (a) accept and time it at TRL 4; (b) relax R7 to 4.5 h | (a) | None | FTK-DDR-003, A3 |
| 5 | Steering lock stops: nothing in the model stops the steering at 40° | (a) two M8 stop bolts through the lower yoke that the drop arm meets at full lock; (b) stops on the knuckle posts that the steering arm clamp plates meet | (a): one pair of stops sets both wheels through the linkage | A part to add before the first ride, not before the build | Build plan work |
| 6 | Steering ratio: the parallelogram drop arm turns the left wheel 1:1 with the handlebar (the concept's linkage would have been about 1.7:1 had it worked) | (a) keep 1:1; (b) a longer drop arm for a slower ratio, with the linkage rechecked | (a): a direct ratio suits a low-speed load carrier and keeps the linkage simple | Drop arm length | FTK-DDR-003, P9 |
| 7 | Steering geometry beyond the ideal: caster, trail, kingpin inclination and self-centring with bought forks | Study at the FEA session; or test at TRL 4 | Study on paper first | None now | FTK-PRC-001, open questions |
| 8 | First partner organization and city | Pick per area later (portfolio rule) | None (partners are picked per area later) | Wholesale prices (R18), laser shop | FTK-DDR-002, item 10 |
| 9 | Render frame colour: teal and graphite powder coat in the photoreal renders; BOM line 13 leaves the finish open | Accept as the render finish only; or choose now | Accept for renders; choose the coating with the partner | None | Review note 2026-09-26, item 1 |
| 10 | Appearance model details: bent fork legs, round tyre section, box hardware positions, a flat-cut ring chain guard, brake cable runs in the context group | Accept each as appearance only; or change | Accept; the renders are redone anyway after FTK-DDR-003 | None | Review note 2026-09-26, items 4 to 8 |

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
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

Value-engineering target: USD 800 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 724 (USD 76 under the target). Main cost drivers and savings worth trying:

- The largest prototype lines are the two front wheels with drum brakes (USD 110), the rear wheel with 3-speed drum hub (USD 95), the steering column, knuckles and linkage (USD 92) and the front bed and knuckle post plates (USD 85). The construction changes (FTK-DDR-003) added USD 15 (USD 709 to USD 724).
- The optional route C assist kit (USD 300, without the SwapCell pack) is outside the prototype target.
- Production target: USD 300 per trike at 100 units (R18) against an estimate of about USD 465, USD 165 over the target. Bought bicycle parts are USD 324 of it at 65 % of retail, with USD 74 of steel (one full sheet), USD 17 of cutting, the plywood box at 60 % and USD 15 of assembly labour.
- Savings worth trying: wholesale prices for wheels, hubs and forks once the first partner supplies them (FTK-DDR-002, item 18), and the one-sheet nest that already keeps the steel and cutting low.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 9, 11 and 12: tadpole front loader; box steering first with Ackermann assessed; no assist in the prototype, route C (SwapCell) preferred; 3 mm S235 or A36 plate, painted; M8 8.8 bolts with all-metal locknuts; bought head tube and bottom bracket sections; 20 in wheels with drum brakes and a 3-speed rear hub; design changes before relaxing R8 and R10; $300 production target (R18); `budget_usd` $800 for the pedal-only prototype; problem line reworded | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | FTK-DDR-001 |
| 2026-09-25 | Cross-cutting: SwapCell interface v0.3 items W, C and V for assist route C; a SwapCell pack is priced once in the SwapCell repo; partners are picked per area later | Amish, same instruction | FTK-DDR-001 |
| 2026-09-25 | Items 13 to 19: Ackermann steering with a fixed box; R8 70 kg; R10 rider-only 0.22 g with a cornering-speed label; 140 kg cargo for riders over 80 kg; R14 90 min for a spine side plate; keep the $300 target; 200 mm head tube | Amish: "i accept all your recommendations, go with them across all repos." | FTK-DDR-002 |
| 2026-09-25 | TRL 4 on hold; the repo stays at TRL 3 | Amish's instruction | `project.yaml`; review note |
| 2026-09-26 | FlatTrike in the first batch of product renders | Amish | Review note, 2026-09-26 |
| 2026-09-30 | Write the illustrated build plan and make the design physically buildable as it is drawn; keep open decisions out of the build plan, in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." and "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | FTK-DDR-003 (Draft, open for review); this register |
