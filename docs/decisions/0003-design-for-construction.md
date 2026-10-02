---
doc_id: FTK-DDR-003
title: FlatTrike design for construction
project: FlatTrike
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish on 2026-10-02, including the recommendations for A1 to A3"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A1 to A3 in Table 3, which are now decided as recommended and recorded in the design decisions register (FTK-DEC-001).

## Context

On 2026-09-30 Amish asked for a build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of FTK-DDR-002 showed what FlatTrike does and passed its calculations, but it modelled the plates as loose shapes: none of the tabs, slots or bolts the precis describes were drawn, and checking the model with build123d found parts that cut through each other, joints with no material for a bolt, a steering linkage that locks, and steering arms that hit the frame.

`cad/src/model.py` now builds every piece as its own solid (35 cut plates, the bought parts and 95 bolt sets) and runs constructability checks (`python cad/src/model.py --check`): every tab, slot, bolt hole and T-slot lies on solid plate with at least about 5 mm of material round it; no two pieces overlap; every piece touches the assembly; and the wheels, forks, steering arms, drag link, tie rod and steering column are swept from full left to full right lock without touching the fixed structure. All checks pass.

The changes keep what the trike does: the same layout, wheelbase, track, wheels, seat position, box size and height, Ackermann steering with a fixed box, flat 3 mm plates cut from one sheet, and no welding or bending. Nothing here changes the pitch. Two consequences touch requirements (Table 3).

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | No joints were modelled. The spine covers were exactly as wide as the spine, so a bolt through a cover into a side plate's edge would break out of the cover's edge; the ribs, yokes and covers had nothing holding them. | One joint for every place where a plate's edge meets another plate's face: tabs on the edge sit in slots in the face (they carry the load), and between tabs an M8 bolt passes through the face into a T-slot in the edge, where an all-metal locknut sits in a window and cannot turn. The covers are 90 mm wide (12 mm past each side plate). In the closed part of the spine box the tabs are 22 mm apart, ten per edge. | It is the tab-and-slot joint the precis describes, made physical, and it keeps the decided M8 8.8 bolts and all-metal locknuts (FTK-DDR-001 item 5). Ten tabs per edge give the 87 MPa tab bearing stress the calculation note already assumed. |
| P2 | Two of the four stay-to-spine bolts passed through the spine's rear lightening window, so they bore on nothing; a bolt across the spine had nothing to stop it squeezing the side plates together. | Rear bolts moved to 335 mm ahead of the rear axle, 697 mm up, and 545 mm, 650 mm up; a smaller rear window clear of them; a 60 mm spacer tube (16 x 2 mm steel tube) inside the spine on every stay bolt. | Every bolt now clamps solid plate; the truss nodes of the stay calculation move by less than 10 mm. |
| P3 | The rear dropout was a closed rectangular hole: the wheel could not be fitted. | An open slot 10 mm wide cut into the stays' rear edge, the axle 53 mm from its mouth; the wheel slides in from behind and moves back to tension the chain. | As on any bicycle with a hub gear. |
| P4 | The chain was on the rider's left. | Moved to the right, at the same 44 mm chain line. | Standard cranks, bottom brackets and hub gears are right-hand drive. |
| P5 | The bottom bracket shell passed through holes in both side plates with "bolted collars" that were not drawn. | The shell is 60 mm long and sits between the side plates; each bottom bracket cup screws in through a 35.5 mm hole and its flange clamps the plate against the shell's end. | Uses the bought cups as the clamp; no collars. |
| P6 | The seatpost stood in the open spine with no tube or clamp. | A bought 31.8 x 2.3 mm seat tube, 225 mm long, passes through an oval hole in the top cover and through two cut saddles across the spine, with a shaft collar on the outside of each saddle; the 27.2 mm seatpost clamps in it. The rearmost spine rib (at 380 mm) is gone: the saddles are now the cross plates there. | The seat line, saddle height and position are unchanged. |
| P7 | The head tube collar plates cut through the spine side plates; the lower yoke sat where the steering fork's crown and lower headset are; the eight yoke-to-collar bolts were not placed. | The yokes are now the head tube's clamp plates: the 200 mm head tube is exactly the gap between them, and each pressed headset cup passes through a 34.5 mm hole in its yoke and clamps the yoke to the tube's end. The upper yoke tabs into both side plates; the lower yoke lies under a new 75 mm level edge at the bottom of the spine's front. The two head tube collar plates are gone. | Fewer parts, and the roll couple at the head tube (2.58 kN at 0.5 g) passes through the cups into the yokes and through the yokes' tabs into the spine (27 MPa bearing). |
| P8 | The steering column had no lower bearing seat and no way to fix the drop arm. | The column is a bought threaded fork with a forged crown, legs sawn off at the crown, and a tall quill stem; the drop arm bolts flat under the crown with two M8 bolts drilled through it. | The crown carries the lower bearing race; two bolts make the drop arm rigid. |
| P9 | The steering linkage locked: with a 70 mm drop arm pointing sideways, no column angle could follow the left steering arm past about 10° of right turn. | The drop arm is 120 mm long and parallel to the left steering arm, so column, drop arm, drag link and left arm form a parallelogram. The handlebar turns as far as the left wheel; full lock is 40° each way. | Works through the whole range; the drag link now runs well below the bulkhead and rails. |
| P10 | The steering arms had no fixing to the forks. At the concept height (400 mm) they swept the space beside the knuckle post columns, passing within a few millimetres at full lock, and into the columns once the posts moved in (P11). | The arms are 321 mm up, below the knuckle posts, each tabbed and bolted into a clamp plate that two M6 U-bolts hold against the inboard fork leg. The knuckle posts and axle beams now start 350 mm up (were 290 mm), so the beams are 120 mm deep (were 180 mm) and the arms, tie rod and drag link pass beneath them. | The steering sweep check passes from lock to lock. Axle beam stress rises from 16 to 36 MPa, still low. |
| P11 | The knuckle collar plates carried each wheel's load in bending across a 90 mm span (over 200 MPa by a simple beam estimate); the knuckle posts' corners were flush, with no room for bolts; the fork crown would hit the post plates at lock. | The two post plates stand 25 mm either side of the knuckle head tube (were 45 mm), so each cup flange bears on its collar plate within 2.5 mm of the plates and the load goes straight into them. The inner cheek is a 76 mm face plate the post plates tab into; the outer cheek sits 10 mm in from the plates' outer edges. Above the tyre the plates step out of the fork crown's path. | The cheeks still close the column: column stress 40 MPa (was 47 MPa). The tyre clears the post by 36 mm at full lock (was 19 mm). |
| P12 | The upper yoke met the bulkhead in its window; the rails began at the bulkhead, leaving no plate round the bulkhead's slots. | The bulkhead window is split into two, with solid plate where both yokes meet it; the rails start 20 mm behind the bulkhead; the bulkhead's bottom edge is 6 mm higher (298 mm) to clear the steering fork crown and the drag link. | Every slot has solid plate round it. |
| P13 | The rails and axle beam plates passed through each other, and the beams' windows sat where the rails cross. | Halving joints: a 55 mm slot up from the rail's bottom edge, a 55 mm slot down from the beam's top edge. The beam windows are moved clear of the crossings; the rails' rear lower edge is raised to 310 mm. | The box floor sits on both and holds the halvings closed. |
| P14 | The box had no fixing to the bed, and bolt heads on the bulkhead's front face would have stood in the box's back. | Six M8 bolts down through the floor into T-slots in the rails' top edges, and two through the back into the bulkhead on stacks of three spacer washers, so the box stands 9 mm in front of the bulkhead. Two 20 mm counterbores 5 mm deep in each box side clear the knuckle post bolt heads. | The box size and floor height are unchanged; the trike is 9 mm longer (2.146 m). |
| P15 | The front hubs were 106 mm long in 100 mm forks. | Hubs 100 mm over locknuts, as bought for 100 mm forks. | Matches the bought parts. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Plates | 35 plates (was 34): two seat tube saddles, two clamp plates added; one rib and two head tube collar plates removed. 78 spacer washers (was 72). 95 bolt sets (was 116). True-shape nest 1,940 mm of the 2,500 mm sheet (was 2,190 mm). | P1 to P14. |
| Mass | Empty 71.2 kg (was 69.8 kg): plates 30.5 kg (was 29.4 kg), the seat tube, collars, spacer tubes and U-bolts 0.75 kg, fewer bolts 0.5 kg lighter. | Wider covers, solid plate round every joint, the bought parts above. See Table 3. |
| Structure | Stay buckling safety factor 2.01 (was 2.09); axle beam 36 MPa; knuckle post column 40 MPa; knuckle post arm 16 MPa; tab bearing 87 MPa; yoke tab bearing 27 MPa. | FTK-CAL-001 v0.3. R2 stays at risk. |
| Steering | Outer wheel 31.3° at 40° inner lock through the real tie rod (ideal Ackermann 29.5°); handlebar turns 1:1 with the left wheel. | P9; the turning circle calculation still uses ideal Ackermann. |
| Assembly and repair | Assembly about 4.04 h for two people (was 4.00 h); a spine side plate about 80 min (was 78 min); a knuckle post plate about 53 min (was 27 min), because both collar plates and the headset cups must come off to release it. | See Table 3. |
| Cost | BOM lines 4, 5, 10 and 11 respecified and repriced: pedal-only prototype $724 (was $709), USD 76 under the unchanged $800 value-engineering target (`budget_usd`). | Seat tube and collars, U-bolts, the cut-down steering fork and a tall quill stem. |
| Drawings | FTK-DWG-001 Rev P3; making sketches FTK-DWG-101 to 123 added. | Follows the model. |
| Renders | `media/render-*.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept (chain on the left, collar plates, steering arms at 400 mm, wider knuckle posts). They need updating on Amish's Mac. | Not regenerated here. |

*Table 3. Items that change a requirement or the rated load: proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | R1 and R8 now fail by 1.2 kg: empty 71.2 kg against 70 kg, gross 301.2 kg against 300 kg with the rated loads. | (a) rate the cargo at 148 kg with a rider up to 80 kg and 138 kg with a rider up to 90 kg, keeping the 300 kg class, and relax R8 to 72 kg; (b) keep 150 and 140 kg and look for 1.2 kg (lightening windows in the knuckle post arms and yokes, about 0.5 kg, and a lighter box); (c) both. | (c): adopt (a) now so the stated rating is true, and try (b) in the FEA session; the final load label is set from the weighed trike. Accepted 2026-10-02. |
| A2 | R14: a knuckle post plate now takes about 53 min to replace against 30 min. | (a) allow 60 min for knuckle post plates, as for the spine side plates; (b) redesign the post so a plate comes out without the collar plates. | (a). Accepted 2026-10-02. |
| A3 | R7: assembly is about 4.04 h against 4 h. | (a) accept, time it at TRL 4; (b) relax R7 to 4.5 h. | (a): the estimate is within its own accuracy of the target. Accepted 2026-10-02. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan FTK-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); the open items are in the design decisions register FTK-DEC-001.
- Requirement status (FTK-CAL-001 v0.3): R1 and R8 not met by 1.2 kg (A1); R7 at the limit (A3); R14 not met for the knuckle post plates (A2); R13 not met as before and R18 over its value-engineering target as before; R2 and R11 at risk; R16 not verifiable at TRL 3.
- With A1 accepted, the rating is 148 kg of cargo with a rider up to 80 kg or 138 kg with a rider up to 90 kg (gross 299.2 kg) and R8 is 72 kg, so R1 and R8 are met on paper; with A2 accepted, R14 allows 60 min for a knuckle post plate and is met on paper (53 min); with A3 accepted, R7 stays at risk and is timed at TRL 4. FTK-CAL-001's script still states the old targets until it is updated (register, follow-up actions in `docs/REVIEW.md`).
- Parts to confirm when bought are listed in the register: the steering fork with a forged crown, the tall quill stem, the rod ends' misalignment, the hub axle lengths and the U-bolts' grip on the fork legs.
