---
doc_id: FTK-DDR-001
title: FlatTrike TRL 2 review decisions
project: FlatTrike
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 9, 11 and 12); items 13 to 19 accepted later the same day and recorded in FTK-DDR-002; item 10 remains proposed, awaiting Amish

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eleven items as "Proposed, awaiting Amish", plus a suggested nuance to the problem line. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." The same instruction approved three cross-cutting SwapCell interface additions, a pricing rule for shared SwapCell packs, and a rule that community designs pick co-design partners per area later.

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 section) and FTK-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Layout | Decided by Amish, 2026-09-25: go with recommendation. Tadpole front loader (option A) | FTK-PRC-001 v0.3, `cad/src/model.py` |
| 2 | Steering | Decided by Amish, 2026-09-25: go with recommendation. Box steering on one kingpin (option A) for the first prototype, with Ackermann steering (option B) assessed at TRL 3 because of R10. The assessment is in FTK-CAL-001 section 5 and leads to open item 13 | FTK-PRC-001 v0.3, FTK-CAL-001 |
| 3 | Electric assist | Decided by Amish, 2026-09-25: go with recommendation. No assist in the prototype (option A), with the bottom bracket housing able to take a mid-drive later; route C (48 V mid-drive on a SwapCell pack) is the preferred assist route | FTK-PRC-001 v0.3, FTK-REQ-001 R13 and R15, `bom/bom.csv` line 15 |
| 4 | Plate material | Decided by Amish, 2026-09-25: go with recommendation. 3 mm S235JR or A36 class steel, primed and painted or powder coated | FTK-PRC-001 v0.3, `bom/bom.csv` |
| 5 | Joint hardware | Decided by Amish, 2026-09-25: go with recommendation. M8 class 8.8 bolts with all-metal prevailing-torque locknuts | FTK-PRC-001 v0.3, `bom/bom.csv` line 4 |
| 6 | Head tube and bottom bracket housings | Decided by Amish, 2026-09-25: go with recommendation. Bought steel head tube and bottom bracket shell sections clamped between plates (option A) | FTK-PRC-001 v0.3, FTK-DWG-001 |
| 7 | Wheels and brakes | Decided by Amish, 2026-09-25: go with recommendation. 20 in (ISO 406) wheels on all three positions with drum brakes; 3-speed drum hub at the rear | FTK-PRC-001 v0.3, FTK-REQ-001 R5 |
| 8 | R8 and R10 shortfalls | Decided by Amish, 2026-09-25: go with recommendation. Try design changes first at TRL 3 before any target is relaxed. Done: lightening windows, 9 mm box walls, seat moved forward, track widened to 0.84 m. The changes did not close either gap (FTK-CAL-001), so open items 14 and 15 follow | FTK-CAL-001, FTK-REQ-001 R8 and R10 |
| 9 | Production cost target | Decided by Amish, 2026-09-25: go with recommendation. $300 or less per trike at 100 units | FTK-REQ-001 new R18 |
| 11 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Keep `budget_usd: 800`; it covers the pedal-only prototype. The assist kit and any SwapCell pack are outside it | `project.yaml` (unchanged), FTK-REQ-001 R15 |
| 12 | Problem line | Decided by Amish, 2026-09-25: go with recommendation. Add that cheap local workshop tricycles are heavy, flexible and short-lived, so the case rests on durability, mass, gears and repair as well as price | `project.yaml`, `README.md`, FTK-PRB-001 v0.3 |

Cross-cutting approvals from the same instruction, recorded here:

- **SwapCell interface v0.3.** Decided by Amish, 2026-09-25 (cross-cutting): the SwapCell interface adds a wake method for hosts without CAN (item W), a charge-while-discharging mode (item C) and a latch vibration rating for vehicles (item V, latch class V1). If assist route C is built, FlatTrike cites **SwapCell interface v0.3** items W, C and V: its vehicle receiver meets latch class V1, fits the 10 kΩ coded INTERLOCK loop so a controller without CAN can wake the pack, and leaves the back and lid faces of the pack open to air (SWC-PRC-001 v0.3).
- **Shared packs are priced once.** Decided by Amish, 2026-09-25 (cross-cutting): the SwapCell pack is priced in the SwapCell repo only and excluded from the FlatTrike budget. `bom/bom.csv` line 15 prices the mid-drive kit and receiver only.
- **Co-design partners per area later.** Decided by Amish, 2026-09-25 (cross-cutting): community designs pick co-design partners per area later. Partners stay open.

### Items raised at TRL 3

Items 13 to 19 were raised by the TRL 3 calculations (FTK-CAL-001 v0.1). Amish accepted their recommendations on 2026-09-25 ("i accept all your recommendations, go with them across all repos"); FTK-DDR-002 records what changed. Item 10 has no recommendation and stays open.

*Table 2. Items raised at TRL 3, and item 10.*

| # | Item | Status and recommendation |
| --- | --- | --- |
| 10 | First partner organization and city | Proposed, awaiting Amish. No recommendation was made; portfolio rule: partners are chosen per area later |
| 13 | Steering for the first prototype after the TRL 3 assessment | Decided by Amish, 2026-09-25: go with recommendation. Switch the first prototype to Ackermann steering (option B) with a fixed box (FTK-DDR-002). Before the decision: Box steering lets the empty trike tip at 5.8 km/h at full lock (0.11 g). Recommendation: switch the first prototype to Ackermann steering (option B, about $40 more) |
| 14 | R8 empty mass (67.5 kg against 55 kg) | Decided by Amish, 2026-09-25: go with recommendation. R8 relaxed to 70 kg for the vehicle with its box (FTK-DDR-002). Before the decision: Options: relax R8 to 70 kg (still lighter than the 80 kg traditional rickshaw), count the box separately from the vehicle, or study aluminium plate (about a third of the plate mass, but fatigue and cost risk). Recommendation: relax R8 to 70 kg for the vehicle with its box |
| 15 | R10 with no cargo (0.24 g against 0.30 g) | Decided by Amish, 2026-09-25: go with recommendation. R10 rider-only case relaxed to 0.22 g together with Ackermann steering and a cornering-speed label (FTK-DDR-002). Before the decision: Options: relax the rider-only case to 0.22 g with a cornering-speed label, specify 30 kg of low ballast when running empty, or accept a 1.0 m track and break R9. Recommendation: relax the rider-only case to 0.22 g together with Ackermann steering (item 13) |
| 16 | R1 with a 90 kg rider (307.5 kg gross) | Decided by Amish, 2026-09-25: go with recommendation. Cargo rated at 140 kg for riders over 80 kg, keeping the 300 kg class limit (FTK-DDR-002). Before the decision: Recommendation: rate the cargo at 140 kg for riders over 80 kg, keeping the 300 kg class limit |
| 17 | R14 spine side plate repair (about 78 min) | Decided by Amish, 2026-09-25: go with recommendation. R14 accepts 90 min for the spine side plates only (FTK-DDR-002). Before the decision: Recommendation: accept 90 min for the spine side plates only, since they are the least likely plates to be damaged |
| 18 | R18 production cost (about $414 against $300) | Decided by Amish, 2026-09-25: go with recommendation. Keep the $300 target and get wholesale prices for wheels and hubs from the first partner before any change (FTK-DDR-002; waits on item 10). Before the decision: Recommendation: keep the target and get wholesale prices for wheels and hubs from the first partner before any change |
| 19 | Headset under roll load (3.34 kN per bearing) | Decided by Amish, 2026-09-25: go with recommendation. Longer head tube, 150 to 200 mm; taper roller bearings not needed once the bed is fixed (FTK-DDR-002). Before the decision: Recommendation: a longer head tube or taper roller bearings, sized in the FEA step |

## Consequences

- FTK-PRB-001, FTK-PRC-001 and FTK-REQ-001 move to v0.3 with these decisions; the precis no longer lists items 1 to 9 as proposed.
- FTK-REQ-001 R15 now states that the $800 budget covers the pedal-only prototype, and a new R18 holds the production cost target.
- The TRL 3 model, drawing FTK-DWG-001 and FTK-CAL-001 follow the decided layout, steering, materials and hardware.
- Items 13 to 19 are implemented at TRL 3 as set out in FTK-DDR-002.
- TRL 4 work (building, testing, purchasing) is on hold by Amish's instruction, whatever the outcome of the open items.
