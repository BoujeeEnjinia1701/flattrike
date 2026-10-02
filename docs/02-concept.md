---
doc_id: FTK-PRC-001
title: FlatTrike design precis
project: FlatTrike
doc_type: Design precis
version: "0.7"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (layout, components, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record decisions (FTK-DDR-001); closed-box spine, fork crown plates, wider stay strips, seat forward; numbers replaced with FTK-CAL-001 values
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design made constructable (FTK-DDR-003); key numbers from FTK-CAL-001 v0.3; build plan FTK-BLD-001
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Decisions of 2026-10-02: design for construction accepted; rating 148 and 138 kg, R8 72 kg, R14 60 min for knuckle post plates; steering lock stops and geometry study before the first ride; partner selection rule"
---

# FlatTrike design precis

FlatTrike is a front-loading cargo tricycle whose whole steel structure is a kit of 35 flat 3 mm plates, cut by any laser or waterjet shop from open files and bolted together through tabs, slots and spacer washers with no welding or bending. Two 20 in front wheels, each turning in a standard bicycle fork on its own headset, carry a fixed, lockable plywood cargo box; a tie rod links them in Ackermann geometry, and the rider sits over a standard 20 in rear wheel with a 3-speed drum brake hub. The TRL 3 calculations (FTK-CAL-001 v0.3, on the constructable design of FTK-DDR-003) show that the trike weighs 71.2 kg empty, carries 150 kg of cargo and an 80 kg rider at 301.2 kg gross, resists tipping to 0.41 g loaded and 0.24 g with the rider only at any steering angle, cruises at 7.5 km/h on the flat on 110 W, nests on one standard sheet, packs into 0.31 m³ and costs an estimated $724 in prototype parts against the $800 value-engineering target (USD 76 under). Four requirements are not met: a loaded 5 % hill needs 241 W at the pedals without assist; making the design buildable added 1.4 kg, so the empty and gross masses are 1.2 kg over their limits (R8, R1); and a knuckle post plate takes about 53 min to replace against 30 min (R14). The production estimate is about $465 against the $300 value-engineering target, USD 165 over (R18). How to settle R1, R8 and R14 is an open decision for Amish. The [prototype build plan](05-build-plan.md) shows how every part is made and fitted.

![Hero render](../media/hero.png)

*Figure 1. FlatTrike TRL 3 model with a 1.75 m person for scale. Every grey and dark steel part is a flat plate; wheels, forks, headsets, drivetrain, seat and bars are standard bicycle parts.*

## How it works

1. **Cut.** A laser or waterjet shop cuts 34 plates and 72 spacer washers from one 1,250 x 2,500 x 3 mm mild steel sheet using open DXF files, with the small plates nested in the windows of the large ones. Tabs, slots and bolt holes are cut in the same pass, so hole positions are as accurate as the cutter.
2. **Assemble.** The two spine side plates (item 1) are closed into a box beam by a top and a bottom cover plate held in slots, three ribs and cross-bolts. The box runs from the seat node to the head tube and has a drop lobe that clamps the bottom bracket shell. The rear stay plates (item 2) bolt to the outside of the spine through stacks of cut spacer washers at two nodes and carry the rear dropouts. The front bed (item 3) is a second bolted assembly: two yoke plates, a bulkhead, two rails, a twin-plate axle beam, and at each end of the beam a closed knuckle post of two transverse plates and two cheeks. No jig is needed because the plates locate one another.
3. **Fix the bed.** A 200 mm steel head tube (item 5) stands between two yoke plates at the front of the spine; each pressed headset cup passes through a yoke and clamps it to the tube's end. The yokes tab into the spine and into the bed's bulkhead, so the bed and box are fixed to the frame (FTK-DDR-003).
4. **Steer.** The handlebar (item 11) turns a steering column, a bought threaded fork cut off at its crown, in a standard 1 1/8 in threaded headset inside the head tube. A drop arm bolted under the crown, parallel to the left steering arm, drives a drag link to that arm, and a tie rod links both steering arms. Each front wheel sits in a bought 20 in fork that turns on its own headset in a 120 mm knuckle head tube, clamped above the tyre between two collar plates on the knuckle post. The steering arms clamp to the inboard fork legs below the knuckle posts and point at the rear axle centre, so the wheels follow Ackermann geometry.
5. **Ride.** A standard bottom bracket and cranks (item 8) drive the 20 in rear wheel (item 7) through a 32/24 chain and a 3-speed hub with a built-in drum brake. The chain runs at a 44 mm chain line in the gap between the right spine plate and the right stay plate.
6. **Stop and park.** Drum brakes in all three hubs (items 6 and 7) are sealed from rain and dust. A lever lock (item 12) holds the front pair when the trike is parked on a slope.
7. **Sell.** The plywood box (item 9) holds 151 L, locks, and has a hinged lid at 0.84 m that doubles as a counter. Its floor sits at 0.47 m so the steered tyres pass beneath it.

![Rider power flow](../media/flow.png)

*Figure 2. Where 110 W of rider power goes at 301.2 kg gross on a flat dirt road (FTK-CAL-001 section 4). All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`. Dimensions are from `cad/src/model.py` and drawing FTK-DWG-001.

Table 1. Main components.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Spine plates and covers | Two 3 mm side plates about 681 x 585 mm, 60 mm apart, with top and bottom cover plates forming a closed 63 mm wide box, 150 to 215 mm deep | The open twin plates would see 569 MPa in torsion, the closed box 9 MPa; deepened at the front to clamp the 200 mm head tube |
| 2 | Rear stay plates (pair) | 3 mm plates about 745 x 555 mm, 120 mm apart for a 120 mm hub, upper strip at least 100 mm wide | Braced by a stay bridge; buckling safety factor 2.09 |
| 3 | Front bed and knuckle post plates | Lower and upper yoke (they clamp the head tube), bulkhead, two rails, twin 120 mm axle beam, and per side a closed knuckle post (two post plates, two cheeks) with two collar plates, all 3 mm | Fixed to the spine; the knuckle post column sees 40 MPa, the highest plate stress |
| 4 | Ribs, saddles, spacer washers and M8 bolts | Two spine ribs, a stay bridge, two seat tube saddles, 78 cut spacer washers, four spacer tubes; 95 M8 class 8.8 bolt sets with all-metal locknuts held in windows in the plates | Decided hardware (FTK-DDR-001 item 5); joints made physical in FTK-DDR-003 |
| 5 | Steering column, knuckles and linkage | Steering column in a 1 1/8 in threaded headset inside a bought 200 mm head tube; two knuckle headsets in 120 mm head tubes; two bought 20 in forks; drop arm, Ackermann steering arms and their clamp plates cut from plate; a cut-down fork as the column; U-bolts; drag link and tie rod with rod ends | Ackermann steering decided (FTK-DDR-002 item 13); 200 mm head tube decided (item 19); linkage made a parallelogram (FTK-DDR-003) |
| 6 | Front wheels (2) | 20 x 2.125 in (ISO 406), 36-hole rims, 90 mm class front drum brake hubs for 100 mm fork dropouts | Each drum needs about 37 N·m |
| 7 | Rear wheel | 20 x 2.125 in with a 3-speed drum brake hub, 120 mm over locknuts, 24T sprocket | Development 1.60 to 2.84 m per crank turn |
| 8 | Drivetrain | Bought 68 mm bottom bracket shell clamped in the spine lobe, 170 mm cranks, 32T chainring, 1/8 in chain | Shell accepts a mid-drive later (assist route C) |
| 9 | Cargo box and lid | Exterior plywood, 820 x 560 x 360 mm, 12 mm floor, 9 mm walls and lid, floor at 0.47 m | 12.7 kg; 151 L; replaceable by a carpenter |
| 10 | Seat and seatpost | Sprung saddle on a 27.2 mm post on a 73° seat line through the bottom bracket | Saddle moved about 110 mm forward at TRL 3 for stability |
| 11 | Handlebar and stem | Steel riser bar on a stem clamped to the steering column | Carries the cornering-speed label |
| 12 | Brake levers, cables and parking latch | Two levers (front pair through a cable splitter, rear drum), lever lock on the front pair | |

Paint, fasteners for the box, mudguards, reflectors and a bell are in the BOM but not modelled. The optional assist kit (route C) is listed but outside the prototype budget.

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

## Key numbers (from FTK-CAL-001)

All values are first-principles estimates, printed by `docs/04-calcs/sizing.py`. The design load case is an 80 kg rider and 150 kg of cargo.

Table 2. Key numbers and requirement status.

| Quantity | Value | Requirement |
| --- | --- | --- |
| Length, width, height | 2.15 x 0.984 x 0.93 m; wheelbase 1.45 m; track 0.84 m | R9 met |
| Turning circle, Ackermann, 40° inner lock | 5.95 m | R9 met |
| Plates | 35 plates, 1.30 m² net, 30.5 kg; 1,940 mm of a 2,500 mm sheet in a true-shape nest | R3 and R4 met |
| Empty mass | 71.2 kg (plates 43 %, box 18 %) | R8 (72 kg, restated 2026-10-02) met on paper |
| Gross mass | 299.2 kg (80 kg rider, 148 kg cargo; or 90 kg rider, 138 kg cargo) | R1 met on paper at the rating restated on 2026-10-02 |
| Flat-pack crate | about 1.38 x 0.62 x 0.36 m, 0.31 m³ | R6 met |
| Cruise on the flat at 110 W | 7.5 km/h | R12 met |
| 5 % grade at 4 km/h | 241 W at the pedals; 6.0 km/h with route C assist | **R13 not met unassisted** |
| Tipping threshold, any lock | 0.41 g loaded; 0.24 g rider only; label 6 km/h in full-lock turns when empty | R10 met |
| Highest plate stress (dynamic) | 40 MPa (knuckle post column); stay buckling safety factor 2.01 | R2 at risk |
| Braking and parking | About 37 N·m per drum; fade after about 1.9 km of 5 % descent | R11 at risk |
| Assembly | About 4.04 h for two people | R7 at risk |
| Repair | Spine side plate about 80 min (90 min allowed); knuckle post plate about 53 min (60 min allowed since 2026-10-02) | R14 met on paper |
| Pedal-only prototype parts | $724 | R15 within the value-engineering target ($800) |
| Production at 100 units | About $465 | **R18 over the value-engineering target by USD 165** (target $300) |

## TRL 3 design changes

The TRL 3 calculations found three failures in the TRL 2 concept and one steering problem. The first three were fixed in the model; the steering problem was fixed after Amish accepted the recommendations on 2026-09-25 (FTK-DDR-002).

- **Closed-box spine.** The single rear wheel cannot resist roll, so the rear frame and rider (116 kg) hang from the head tube joint, and a 0.5 g roll puts 512 N·m of torsion into the spine. Two separate 3 mm plates would see 569 MPa; with top and bottom cover plates the closed box sees 9 MPa.
- **Wider stay strips.** The upper stay strip is a compression member. The smaller TRL 3 window leaves a 100 mm strip with a buckling safety factor of 2.09, and only because the stay bridge braces it.
- **Ackermann steering with a fixed box (FTK-DDR-002 item 13).** Under box steering the outer wheel moved 334 mm inward at full lock and the empty trike could tip at 5.8 km/h. Each front wheel now turns in its own fork, so the track stays at 0.84 m at any lock and the rider-only threshold is 0.24 g throughout. The flat fork plates and crown plates of v0.3 are replaced by closed knuckle posts; the box is narrower (560 mm) and its floor higher (0.47 m) so the steered tyres pass under it.
- **Longer head tube (item 19).** The head tube grew from 150 to 200 mm, cutting the roll couple at the joint from 3.41 to 2.56 kN. With the bed fixed, the couple passes through the yokes rather than the headset bearings.
- **Design for construction (FTK-DDR-003, accepted by Amish on 2026-10-02).** Writing the build plan made every joint physical (tabs in slots, bolts into T-slots with captive locknuts), moved two stay bolts off a window, opened the rear dropouts, put the chain on the right, made the yokes the head tube clamps, made the steering linkage a parallelogram so it no longer locks on right turns, moved the steering arms below the knuckle posts and rebuilt the posts. It added 1.4 kg, so the cargo is now rated at 148 kg with a rider up to 80 kg and 138 kg with a rider up to 90 kg, and R8 at 72 kg (decided 2026-10-02); the final load label is set from the weighed trike.
- **Mass and stability (FTK-DDR-001 item 8, FTK-DDR-002 items 14 to 16).** Lightening windows, a 9 mm box, a seat 110 mm further forward and a 0.84 m track did not reach the original 55 kg and 0.30 g targets. Amish accepted relaxing R8 to 70 kg and the rider-only case of R10 to 0.22 g with a cornering-speed label, and rating the cargo at 140 kg for riders over 80 kg. Larger windows in the axle beam, rails and bulkhead kept the Ackermann version at 69.8 kg before the design-for-construction changes.

## Key design choices

Items marked decided were decided by Amish on 2026-09-25 (FTK-DDR-001 and FTK-DDR-002).

- **Layout.** Tadpole front loader. Decided.
- **Steering.** Ackermann steering with a fixed box for the first prototype. Decided (FTK-DDR-002 item 13), replacing box steering.
- **Joints.** Tabs and slots located by the cut, clamped by M8 class 8.8 bolts with all-metal prevailing-torque locknuts. Decided.
- **Plate material.** 3 mm S235JR or A36 class, primed and painted or powder coated. Decided.
- **Head tube and bottom bracket housings.** Bought steel sections clamped between plates. Decided. Central head tube 200 mm long (FTK-DDR-002 item 19).
- **Wheels and brakes.** 20 in on all three positions with drum brakes; 3-speed drum hub at the rear; bought 20 in forks at the front. Decided.
- **Electric assist.** None in the prototype. Decided. Route C, a 48 V mid-drive on a SwapCell pack, is the preferred route (decided). If built, it cites **SwapCell interface v0.3** items W (wake for hosts without CAN), C (charge while discharging) and V (latch class V1 for vehicles); the receiver meets latch class V1 and leaves the pack's back and lid faces open to air. The pack is priced once in the SwapCell repo and excluded from the FlatTrike budget.
- **Budget.** `budget_usd` stays at $800 for the pedal-only prototype, as a hypothetical value-engineering target, not a limit. Decided.
- **Targets.** R1 restated (148 kg cargo with a rider up to 80 kg, 138 kg with a rider up to 90 kg), R8 72 kg, R10 rider-only 0.22 g with a label, R14 90 min for the spine side plates and 60 min for the knuckle post plates. Decided (FTK-DDR-002; FTK-DDR-003, A1 and A2, 2026-10-02).
- **Production cost target.** $300 or less per trike at 100 units (R18), kept as a value-engineering target until the first partner supplies wholesale prices. Decided; the estimate is USD 165 over it.
- **Partner and city.** Decided 2026-10-02 as a selection rule: a city with dense goods delivery on narrow streets, a laser-cutting shop and a bicycle parts market. First candidate type to approach: a cycle-rickshaw or cargo-bike programme such as those ITDP has documented in South Asia; nothing is agreed.
- **Steering.** 1:1 parallelogram ratio kept; a lock stop at each knuckle post, met by its steering arm clamp plate at 40 degrees, is fitted before the first ride. Decided 2026-10-02.

## Safety

> **Safety:** FlatTrike is a loaded vehicle of about 300 kg that shares the road with traffic, built from cut steel plate and exposed moving parts. Treat structural failure, tipping, braking, cut edges and pinch points as hazards at every stage. Nothing here is verified by test; TRL 4 is on hold by Amish's instruction.

- **Structural failure.** A bolted joint that loosens or slips, a stay strip that buckles, or a crack at a hole can let the frame collapse under load. Structural bolts need all-metal locknuts, a set torque and a check at every service. The frame must not be used on public roads until its strength and fatigue life are verified (R2), and routine overloading must be allowed for.
- **Tipping.** The empty trike tips at about 0.24 g (12 km/h on a 5 m radius, about 8 km/h in its tightest turn). A label on the bar tells riders to keep to 6 km/h in full-lock turns when empty. Keep heavy cargo low.
- **Steering joints.** The head tube clamps and yoke bolts carry the rear frame's roll moment (a 2.6 kN couple at 0.5 g), and the knuckle posts carry each front wheel. The tie rod and drag link rod ends must be secured with locknuts; a loose rod end means loss of steering. Check the clamps, bolts, headsets and rod ends at every service.
- **Braking and descents.** Drum brakes may fade after about 2 km of continuous loaded descent at 5 %. Descend slowly and in stages. The parking latch must hold the loaded trike on a slope, because a runaway trike in a market is a serious hazard.
- **Sharp edges.** Laser- and waterjet-cut edges and corners can be sharp and burred. Deburr every plate and radius every exposed corner before painting; protect hands during assembly.
- **Moving parts and pinch points.** The chain, chainring and spokes can catch clothing and fingers; fit a chain guard. The steered front wheels, tie rod and drag link move beneath the box and beside the rider's feet; keep hands and feet clear of the wheels and linkage. Steering lock stops at each knuckle post (40 degrees) must be fitted, and the steering geometry studied on paper, before the first ride.
- **Traffic visibility.** A slow, wide vehicle in mixed traffic needs reflectors, a bell and, for dusk use, lights.
- **Coatings.** Priming, painting and powder coating involve solvents and fine particles; use ventilation and masks.
- **Electric assist (route C only).** The lithium-ion pack needs its BMS, a fused output and safe charging, as set out in the SwapCell design. A pack that leaves its mount is a projectile with live contacts, so the receiver must meet latch class V1.

## Open questions

- Plate-and-joint FEA of the spine box, stays, knuckle posts, head tube clamps and bed against the EN 17860 load cases, once the standard is obtained.
- Steering geometry beyond the ideal: caster, trail, kingpin inclination and scrub, and whether bought forks give usable self-centering on a trike. To be studied on paper in the FEA session, with the bought fork's rake as input, before the first ride (decided 2026-10-02).
- Drum brake torque, hub input torque, fork and headset ratings from the makers.
- DXF nesting by the cutting shop; the raster nest in FTK-CAL-001 leaves 310 mm spare but relies on cutting small parts from the windows of large ones.
- Partner, city, laser-shop quotes and wholesale prices for wheels, hubs and forks (R18 waits on these).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: `cad/drawings/FTK-DWG-001.pdf`.
