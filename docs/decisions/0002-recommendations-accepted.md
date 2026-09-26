---
doc_id: FTK-DDR-002
title: FlatTrike recommendations accepted
project: FlatTrike
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 13 to 19); item 10 remains proposed, awaiting Amish

## Context

After the TRL 3 session, FTK-DDR-001 and `docs/REVIEW.md` listed items 13 to 19 as "Proposed, awaiting Amish", each with a recommendation, and item 10 (first partner and city) with none. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This record lists what that decides, what changed in the repo because of it, and what stays open. TRL 4 remains on hold by Amish's instruction, so nothing here is built, bought or tested.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 13 | Steering for the first prototype | Decided by Amish, 2026-09-25: go with recommendation. Ackermann steering (option B) with a fixed box | `cad/src/model.py`: the front bed now bolts rigidly to the spine (yokes bolted to the head tube collar plates). Each front wheel turns in a bought 20 in fork on its own 1 1/8 in headset, held in a 120 mm knuckle head tube by a closed knuckle post (two transverse plates, two cheeks, two collar plates). Ackermann arms aimed at the rear axle centre, a tie rod, and a drag link from a drop arm on the central steering column. The four fork plates and four crown plates are gone. The box is 820 x 560 x 360 mm (was 795 x 700 x 360 mm) with its floor at 470 mm (was 400 mm) so the steered tyres pass under it; inner lock 40° (was 35° box lock). `bom/bom.csv` item 5 rises from $25 to $85; items 1, 3, 4, 6, 9, 11 and 14 respecified. FTK-DWG-001 Rev P2; FTK-CAL-001 v0.2; media regenerated |
| 14 | R8 empty mass | Decided by Amish, 2026-09-25: go with recommendation. R8 relaxed from 55 kg to 70 kg for the vehicle with its box | FTK-REQ-001 R8. With the Ackermann parts the trike is 69.8 kg (was 67.5 kg); larger windows in the axle beam, rails and bulkhead keep it inside 70 kg |
| 15 | R10 with no cargo | Decided by Amish, 2026-09-25: go with recommendation. Rider-only threshold relaxed from 0.30 g to 0.22 g, with Ackermann steering and a cornering-speed label; the loaded case stays at 0.30 g | FTK-REQ-001 R10. Rider only 0.24 g at any lock (was 0.24 g straight and 0.11 g at full box lock); loaded 0.41 g (was 0.43 g). Label on the bar: empty, 6 km/h in full-lock turns (BOM item 14) |
| 16 | R1 with a 90 kg rider | Decided by Amish, 2026-09-25: go with recommendation. Rated cargo 150 kg with a rider up to 80 kg and 140 kg with a rider up to 90 kg, within 300 kg gross | FTK-REQ-001 R1. Gross 299.8 kg in both cases (was 297.5 kg and 307.5 kg) |
| 17 | R14 spine side plate repair | Decided by Amish, 2026-09-25: go with recommendation. 90 min allowed for a spine side plate only; 30 min for every other plate or part | FTK-REQ-001 R14. Spine side plate about 78 min, knuckle post plate about 27 min |
| 18 | R18 production cost | Decided by Amish, 2026-09-25: go with recommendation. Keep the $300 target at 100 units; get wholesale prices for wheels and hubs from the first partner before any change | FTK-REQ-001 R18 unchanged. The estimate rises from about $414 to about $456 with the steering parts. Getting prices waits on a partner (item 10) |
| 19 | Headset under roll load | Decided by Amish, 2026-09-25: go with recommendation. Longer head tube (the first of the two recommended options) | Central head tube 150 to 200 mm, with the spine plates deepened at the front to clamp it. The roll couple falls from 3.41 to 2.56 kN and, with the bed fixed (item 13), passes through the collar and yoke clamps and eight yoke-to-collar bolts (640 N each against a 3.12 kN slip load) rather than the headset bearings, so taper roller bearings are not needed. Confirming the clamps is part of the plate-and-joint FEA |

`budget_usd` stays at $800. The pedal-only prototype is now $709 in `bom/bom.csv` (was $647), still within it (R15). No decision changed the pitch or the problem line.

## Consequences

- FTK-REQ-001 v0.4, FTK-PRC-001 v0.4, FTK-PRB-001 v0.4, FTK-CAL-001 v0.2 and FTK-DDR-001 v0.2 carry these decisions.
- Requirement status after the change (FTK-CAL-001 v0.2): 12 met, 2 not met (R13 without assist, R18), 3 at risk (R2, R7, R11), 1 not verifiable at TRL 3 (R16). R1 and R8 are met with only 0.2 kg of margin.
- The bounding-rectangle nest no longer fits one sheet with 34 plates; a true-shape raster nest in FTK-CAL-001 uses 2,190 of 2,500 mm, so R4 still holds but depends on nesting small parts in the windows of large ones.
- Assembly rises to about 4.0 h for two people, at the R7 limit.
- The knuckle post column is the new highly stressed member (47 MPa dynamic in the closed box; 155 MPa if the cheeks were left out).

### Items that remain open

*Table 2. Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| 10 | First partner organization and city | Proposed, awaiting Amish. No recommendation; partners are picked per area later. Item 18's wholesale prices wait on it |

### On hold (TRL 4)

Nothing from items 13 to 19 needs a build. The later work they point to (a tilt-table test of R10, a timed build for R7, partner quotes for R18, a proof load on the knuckle posts) is TRL 4 and on hold by Amish's instruction.

### Cross-repo actions

None. Assist route C and the SwapCell interface v0.3 citation are unchanged.
