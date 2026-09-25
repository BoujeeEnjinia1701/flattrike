---
doc_id: FTK-PRC-001
title: FlatTrike design precis
project: FlatTrike
doc_type: Design precis
version: "0.3"
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
  change: Populate to TRL 2 (layout, components, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record decisions (FTK-DDR-001); closed-box spine, fork crown plates, wider stay strips, seat forward; numbers replaced with FTK-CAL-001 values
---

# FlatTrike design precis

FlatTrike is a front-loading cargo tricycle whose whole steel structure is a kit of 27 flat 3 mm plates, cut by any laser or waterjet shop from open files and bolted together through tabs, slots and spacer washers with no welding or bending. Two 20 in front wheels carry a lockable plywood cargo box on a steel bed that pivots about a single kingpin (box steering), and the rider sits over a standard 20 in rear wheel with a 3-speed drum brake hub. The TRL 3 calculations (FTK-CAL-001) show that the trike carries 150 kg of cargo and an 80 kg rider at 297.5 kg gross, cruises at 7.6 km/h on the flat on 110 W, nests on one standard sheet, packs into 0.39 m³ and costs $647 in prototype parts against the $800 budget. Six requirements are not met: the empty mass is 67.5 kg against 55 kg, the empty trike tips at 0.24 g (and at 0.11 g at full box-steering lock), a loaded 5 % hill needs 238 W at the pedals, a 90 kg rider takes the gross mass to 307.5 kg, a spine side plate takes about 78 min to replace, and the production estimate is about $414 against $300.

![Hero render](../media/hero.png)

*Figure 1. FlatTrike TRL 3 model with a 1.75 m person for scale. Every grey and dark steel part is a flat plate; wheels, drivetrain, seat and bars are standard bicycle parts.*

## How it works

1. **Cut.** A laser or waterjet shop cuts 27 plates and 72 spacer washers from one 1,250 x 2,500 x 3 mm mild steel sheet using open DXF files. Tabs, slots and bolt holes are cut in the same pass, so hole positions are as accurate as the cutter.
2. **Assemble.** The two spine side plates (item 1) are closed into a box beam by a top and a bottom cover plate held in slots, three ribs and cross-bolts. The box runs from the seat node to the kingpin and has a drop lobe that clamps the bottom bracket shell. The rear stay plates (item 2) bolt to the outside of the spine through stacks of cut spacer washers at two nodes and carry the rear dropouts. The front bed (item 3) is a second bolted assembly: two yoke plates around the kingpin, a bulkhead, two rails, a twin-plate axle beam, and for each front wheel an inner and an outer fork plate joined by two vertical crown plates. No jig is needed because the plates locate one another.
3. **Steer.** The whole front bed, with both front wheels and the box, pivots on a standard 1 1/8 in threaded headset inside a 150 mm head tube (item 5) clamped to the front of the spine by two collar plates. The rider steers with a handlebar (item 11) fixed to the bed's bulkhead.
4. **Ride.** A standard bottom bracket and cranks (item 8) drive the 20 in rear wheel (item 7) through a 32/24 chain and a 3-speed hub with a built-in drum brake. The chain runs at a 44 mm chain line in the gap between the right spine plate and the right stay plate.
5. **Stop and park.** Drum brakes in all three hubs (items 6 and 7) are sealed from rain and dust. A lever lock (item 12) holds the front pair when the trike is parked on a slope.
6. **Sell.** The plywood box (item 9) holds 184 L, locks, and has a hinged lid at 0.77 m that doubles as a counter.

![Rider power flow](../media/flow.png)

*Figure 2. Where 110 W of rider power goes at 297.5 kg gross on a flat dirt road (FTK-CAL-001 section 4). All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`. Dimensions are from `cad/src/model.py` and drawing FTK-DWG-001.

Table 1. Main components.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Spine plates and covers | Two 3 mm side plates about 681 x 585 mm, 60 mm apart, with top and bottom cover plates forming a closed 63 x 150 mm box | Closed box added at TRL 3: the open twin plates would see 556 MPa in torsion, the box 9 MPa |
| 2 | Rear stay plates (pair) | 3 mm plates about 745 x 555 mm, 120 mm apart for a 120 mm hub, upper strip at least 100 mm wide | Braced by a stay bridge; buckling safety factor 2.06 |
| 3 | Front bed plates | Lower and upper yoke, bulkhead, two rails, twin axle beam, four fork plates, four crown plates, all 3 mm | Vertical crown plates replace the TRL 2 flat bridges (619 MPa down to 23 MPa) |
| 4 | Ribs, spacer washers and M8 bolts | Three spine ribs, a stay bridge, 72 cut spacer washers; 112 M8 class 8.8 bolt sets with all-metal locknuts | Decided hardware (FTK-DDR-001 item 5) |
| 5 | Kingpin and headset | 1 1/8 in threaded headset in a bought 150 mm steel head tube, clamped by two collar plates | Bought section decided (item 6); carries 3.34 kN per bearing in a 0.5 g roll, to be sized |
| 6 | Front wheels (2) | 20 x 2.125 in (ISO 406), 36-hole rims, 90 mm class drum brake hubs | Each drum needs about 37 N·m |
| 7 | Rear wheel | 20 x 2.125 in with a 3-speed drum brake hub, 120 mm over locknuts, 24T sprocket | Development 1.60 to 2.84 m per crank turn |
| 8 | Drivetrain | Bought 68 mm bottom bracket shell clamped in the spine lobe, 170 mm cranks, 32T chainring, 1/8 in chain | Shell accepts a mid-drive later (assist route C) |
| 9 | Cargo box and lid | Exterior plywood, 795 x 700 x 360 mm, 12 mm floor, 9 mm walls and lid | 14.7 kg; 184 L; replaceable by a carpenter |
| 10 | Seat and seatpost | Sprung saddle on a 27.2 mm post on a 73° seat line through the bottom bracket | Saddle moved about 110 mm forward at TRL 3 for stability |
| 11 | Handlebar and stem | Steel riser bar on a stem bolted to the bulkhead | Fixed to the steering bed |
| 12 | Brake levers, cables and parking latch | Two levers (front pair through a cable splitter, rear drum), lever lock on the front pair | |

Paint, fasteners for the box, mudguards, reflectors and a bell are in the BOM but not modelled. The optional assist kit (route C) is listed but outside the prototype budget.

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

## Key numbers (from FTK-CAL-001)

All values are first-principles estimates, printed by `docs/04-calcs/sizing.py`. The design load case is an 80 kg rider and 150 kg of cargo.

Table 2. Key numbers and requirement status.

| Quantity | Value | Requirement |
| --- | --- | --- |
| Length, width, height | 2.11 x 0.986 x 0.93 m; wheelbase 1.45 m; track 0.84 m | R9 met |
| Turning circle, 35° box-steering lock | 5.67 m | R9 met |
| Plates | 27 plates, 1.22 m² net, 28.6 kg; 2,486 mm of a 2,500 mm sheet by bounding rectangles | R3 and R4 met |
| **Empty mass** | **67.5 kg** (plates 42 %, box 22 %) | **R8 (55 kg) not met** |
| Gross mass | 297.5 kg (80 kg rider); 307.5 kg (90 kg rider) | **R1 not met with a 90 kg rider** |
| Flat-pack crate | about 1.35 x 0.80 x 0.36 m, 0.39 m³ | R6 met |
| Cruise on the flat at 110 W | 7.6 km/h | R12 met |
| 5 % grade at 4 km/h | 238 W at the pedals; 6.0 km/h with route C assist | **R13 not met unassisted** |
| Tipping threshold | 0.43 g loaded; **0.24 g rider only**; **0.11 g rider only at full lock** | **R10 not met** |
| Highest plate stress (dynamic) | 45 MPa (axle beam); stay buckling safety factor 2.06 | R2 at risk |
| Braking and parking | About 37 N·m per drum; fade after about 1.9 km of 5 % descent | R11 at risk |
| Assembly | About 3.6 h for two people | R7 at risk |
| Repair of a spine side plate | About 78 min (42 bolts) | **R14 not met** |
| Pedal-only prototype parts | $647 | R15 met |
| Production at 100 units | About $414 | **R18 ($300) not met** |

## TRL 3 design changes

The calculations found three failures in the TRL 2 concept, now fixed in the model, and one steering problem that needs a decision.

- **Closed-box spine.** The single rear wheel cannot resist roll, so the rear frame and rider (112 kg) hang from the kingpin, and a 0.5 g roll puts 501 N·m of torsion into the spine. Two separate 3 mm plates resist that at 556 MPa; with top and bottom cover plates the closed box sees 9 MPa.
- **Fork crown plates.** The outer fork plate carries half the wheel load through its crown. A flat 3 mm bridge would see 619 MPa; two vertical 80 mm crown plates see 23 MPa.
- **Wider stay strips.** The upper stay strip is a compression member. With the TRL 2 window it would buckle at about 1.1 times its dynamic load; the smaller TRL 3 window leaves a 100 mm strip with a safety factor of 2.06, and only because the stay bridge braces it.
- **Box steering at full lock.** Because the kingpin is 450 mm behind the front axle, the outer wheel moves 334 mm inward at full lock and the empty trike can tip at 5.8 km/h. Ackermann steering keeps the track and removes this case (proposed, awaiting Amish; FTK-DDR-001 item 13).
- **Mass and stability changes (FTK-DDR-001 item 8).** Lightening windows, a 9 mm box and a 360 mm box height, a seat 110 mm further forward and a 0.84 m track raised the rider-only threshold from 0.18 to 0.24 g but did not close R8 or R10.

## Key design choices

Items marked decided were decided by Amish on 2026-09-25 (FTK-DDR-001).

- **Layout.** Tadpole front loader. Decided.
- **Steering.** Box steering on one kingpin for the first prototype. Decided, with Ackermann (option B) assessed at TRL 3. The assessment favors option B for the first prototype; that change is **proposed, awaiting Amish** (FTK-DDR-001 item 13).
- **Joints.** Tabs and slots located by the cut, clamped by M8 class 8.8 bolts with all-metal prevailing-torque locknuts. Decided.
- **Plate material.** 3 mm S235JR or A36 class, primed and painted or powder coated. Decided.
- **Head tube and bottom bracket housings.** Bought steel sections clamped between plates. Decided. The headset bearing choice under roll load is **proposed, awaiting Amish** (item 19).
- **Wheels and brakes.** 20 in on all three positions with drum brakes; 3-speed drum hub at the rear. Decided.
- **Electric assist.** None in the prototype. Decided. Route C, a 48 V mid-drive on a SwapCell pack, is the preferred route (decided). If built, it cites **SwapCell interface v0.3** items W (wake for hosts without CAN), C (charge while discharging) and V (latch class V1 for vehicles); the receiver meets latch class V1 and leaves the pack's back and lid faces open to air. The pack is priced once in the SwapCell repo and excluded from the FlatTrike budget.
- **Budget.** `budget_usd` stays at $800 for the pedal-only prototype. Decided.
- **Production cost target.** $300 or less per trike at 100 units (R18). Decided; not met by the estimate.
- **Targets for R1, R8, R10, R14 and R18.** Proposed changes are open items 14 to 18 in FTK-DDR-001, **awaiting Amish**.
- **Partner and city.** Open; partners are picked per area later.

## Safety

> **Safety:** FlatTrike is a loaded vehicle of about 300 kg that shares the road with traffic, built from cut steel plate and exposed moving parts. Treat structural failure, tipping, braking, cut edges and pinch points as hazards at every stage. Nothing here is verified by test; TRL 4 is on hold by Amish's instruction.

- **Structural failure.** A bolted joint that loosens or slips, a stay strip that buckles, or a crack at a hole can let the frame collapse under load. Structural bolts need all-metal locknuts, a set torque and a check at every service. The frame must not be used on public roads until its strength and fatigue life are verified (R2), and routine overloading must be allowed for.
- **Tipping.** The empty trike tips at about 0.24 g in a straight-bar turn (12 km/h on a 5 m radius) and at about 0.11 g at full box-steering lock, which is about 5.8 km/h in its tightest turn. Riders must slow right down for tight turns, especially empty, and keep heavy cargo low.
- **Headset.** The headset carries the rear frame's roll moment, about 3.3 kN per bearing at 0.5 g. A worn or loose headset would let the rear frame lean; check it at every service.
- **Braking and descents.** Drum brakes may fade after about 2 km of continuous loaded descent at 5 %. Descend slowly and in stages. The parking latch must hold the loaded trike on a slope, because a runaway trike in a market is a serious hazard.
- **Sharp edges.** Laser- and waterjet-cut edges and corners can be sharp and burred. Deburr every plate and radius every exposed corner before painting; protect hands during assembly.
- **Moving parts and pinch points.** The chain, chainring and spokes can catch clothing and fingers; fit a chain guard. The steering bed swings about the kingpin close to the rider's feet; keep hands and feet clear of the gap between the bed and the spine.
- **Traffic visibility.** A slow, wide vehicle in mixed traffic needs reflectors, a bell and, for dusk use, lights.
- **Coatings.** Priming, painting and powder coating involve solvents and fine particles; use ventilation and masks.
- **Electric assist (route C only).** The lithium-ion pack needs its BMS, a fused output and safe charging, as set out in the SwapCell design. A pack that leaves its mount is a projectile with live contacts, so the receiver must meet latch class V1.

## Open questions

- Steering for the first prototype after the TRL 3 assessment (FTK-DDR-001 item 13).
- Revised targets or further changes for R1, R8, R10, R14 and R18 (items 14 to 18).
- Plate-and-joint FEA of the spine box, stays and bed against the EN 17860 load cases, once the standard is obtained.
- Headset bearing sizing under roll load (item 19), and drum brake torque and hub input torque data from the hub makers.
- True-shape nesting from DXF files; the bounding-rectangle nest has only 14 mm of margin.
- Partner, city, laser-shop quotes and wholesale prices for wheels and hubs.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: `cad/drawings/FTK-DWG-001.pdf`.
