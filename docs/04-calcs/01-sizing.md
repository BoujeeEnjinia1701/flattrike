---
doc_id: FTK-CAL-001
title: FlatTrike sizing and first-principles checks
project: FlatTrike
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (geometry, nesting, mass, power, stability, structure, braking, assembly, cost) against every requirement
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Ackermann steering with a fixed box, knuckle posts, 200 mm head tube, raised and narrower box, restated R1, R8, R10 and R14; true-shape nest added
---

# FlatTrike sizing and first-principles checks

This version checks the design after Amish accepted the TRL 3 recommendations on 2026-09-25 (FTK-DDR-002): Ackermann steering with a fixed box, a 200 mm head tube, and restated targets for R1, R8, R10 and R14. On paper, twelve of the eighteen requirements are met, three are at risk and one cannot be verified at TRL 3. Two are **not met**: R13 without assist (240 W needed at the pedals on a 5 % grade) and R18 (about $456 per trike at 100 units against $300). R1 and R8 are met with only 0.2 kg of margin, and assembly (R7) sits at its 4 h limit.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads plate outlines, areas, part centroids and key dimensions from the parametric model `cad/src/model.py`, and prices from `bom/bom.csv`, so the model, the drawing FTK-DWG-001 and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Layout and steering | Tadpole front loader; Ackermann steering with a fixed box; kingpins on the front wheel centre lines; 40° inner lock | Decided, FTK-DDR-001 item 1 and FTK-DDR-002 item 13; lock set by tyre clearance under the box |
| Rated load | 150 kg cargo with an 80 kg rider; 140 kg cargo with a 90 kg rider | FTK-REQ-001 R1, restated in FTK-DDR-002 item 16 |
| Plate | 3 mm S235JR or A36, 7,850 kg/m³ (23.6 kg/m²), yield 235 MPa, E = 210 GPa | Decided, FTK-DDR-001 item 4 |
| Plywood | 700 kg/m³; 12 mm floor, 9 mm walls and lid | Exterior grade |
| Rider centre of mass | 20 mm ahead of the saddle, 160 mm above its top: 0.42 m ahead of the rear axle, 1.09 m high | Upright seated rider; saddle on a 73° seat line |
| Cargo centre of mass | Centre of the box interior: 1.48 m ahead, 0.66 m high | Uniform load |
| Bought part masses | Front wheels 5.8 kg (pair), rear wheel 3.8, drivetrain 3.0, steering 4.7 (central headset, 200 mm head tube and column 1.25; two knuckle headsets and 120 mm head tubes 1.05; two 20 in steel forks 1.8; drag link, tie rod and rod ends 0.6), seat 1.4, bars 1.2, brakes 0.7, box hardware 1.0, paint 0.6, accessories 1.5 kg | Typical steel utility parts |
| Fasteners | 116 M8 class 8.8 bolt sets at 28 g; 72 cut spacer washers | Joint count in `sizing.py`; all-metal locknuts decided |
| Riding | Crr 0.015, CdA 0.9 m², air 1.2 kg/m³, drivetrain 89 %, rider 110 W sustained | As TRL 2 |
| Gearing | 32T chainring, 24T sprocket, hub ratios 0.75, 1.00 and 1.33 | Typical 3-speed hub |
| Dynamic factor | 2.5 on static loads for potholes and curbs | EN 17860 test loads not read (section 11) |
| Bolted joints | Preload 15.6 kN at 25 N·m (K = 0.2); slip factor 0.20 on painted faces | Typical |
| Fatigue | Plate with holes treated as a 90 MPa detail, constant-amplitude limit 66 MPa | Eurocode 3 practice for members with holes; to confirm |
| Drums | 0.35 kg iron drum and 0.30 kg aluminium shell per hub; heat loss 0.5 W/K at 10 km/h | Assumed; no hub data read |
| Assist (route C only) | 250 W mid-drive, 80 % motor and controller, SwapCell 457 Wh per cycle at the terminals | SWC-CAL-001 |
| Production (R18) | One full sheet at $1.0/kg, cutting at $0.30/m, bought parts at 65 % of prototype retail, plywood at 60 %, $15 assembly labour | Assumed volume rates; no quotes |

## 2. Geometry, plates and nesting

The parametric model is 2.14 m long, 0.986 m wide and 0.93 m high to the saddle, on a 1.45 m wheelbase and 0.84 m track. It has 34 cut plates with a net area of 1.25 m² (29.4 kg), plus 72 spacer washers cut from the offcuts, so every steel part is still flat 3 mm plate (R3). The head tubes and bottom bracket shell are bought steel sections, and the front forks are bought 20 in bicycle forks.

Ackermann steering replaced the four fork plates and four crown plates with two closed knuckle posts (four transverse plates, four cheeks, four collar plates) and added a drop arm and two steering arms, so the plate count rose from 27 to 34. The bounding rectangles of the plates now cover 95 % of the sheet, and a shelf nest of rectangles would need 2,805 mm of a 2,500 mm sheet. The script therefore also runs a true-shape nest: each plate outline, less its windows, is rasterized at 5 mm, grown by one cell for raster error and by two more for a 10 mm gap, and placed largest first, bottom-left, in four orientations, with small parts allowed inside the windows of large ones. That nest uses **2,190 mm** of the sheet (R4 met, 310 mm spare). The plates use 39.9 % of the sheet by net area. A DXF nest by the cutting shop is still needed.

The box, now 820 x 560 x 360 mm with its floor at 0.47 m, holds 151 L with the lid (counter) at 0.84 m (R17). Plates and box panels stack about 195 mm deep on a 0.83 x 0.62 m footprint; with the three wheels and two forks stacked beside them the crate is about 1.35 x 0.62 x 0.36 m, or 0.30 m³ (R6). The longest cut plate is the 825 mm bed rail and the longest piece the 820 mm box floor.

## 3. Mass and centre of mass

The empty trike is **69.8 kg** against the 70 kg target (R8 met; relaxed from 55 kg in FTK-DDR-002 item 14). Plates are 42 % of it (29.4 kg) and the box 18 % (12.7 kg); bolts and washers add 4.1 kg. Against v0.1 (67.5 kg), the steering parts add 3.4 kg and the knuckle posts and deeper rails about 2 kg; the narrower box saves 2.0 kg, and larger windows in the axle beam, rails and bulkhead save about 1.2 kg.

*Table 2. Mass and axle loads.*

| Quantity | Value |
| --- | --- |
| Empty mass | 69.8 kg (R8 met, 0.2 kg margin) |
| Gross, 80 kg rider and 150 kg cargo | 299.8 kg (R1 met, 0.2 kg margin) |
| Gross, 90 kg rider and 140 kg cargo | 299.8 kg (R1 met) |
| Gross, 90 kg rider and 150 kg cargo (not a rated case) | 309.8 kg |
| Empty trike centre of mass | 0.99 m ahead of the rear axle, 0.49 m high |
| Axle loads, loaded | front 2.20 kN, rear 0.75 kN |

Any growth in mass comes straight off the rated cargo: every kilogram added to the trike must be taken off the 150 kg and 140 kg ratings to stay inside the 300 kg class.

## 4. Riding power, gearing and assist

At 299.8 kg gross, rolling resistance is 44.1 N and 110 W at the pedals gives 97.9 W at the wheel, for a flat cruise of **7.6 km/h** (R12 met): 92.9 W goes to rolling and 5.0 W to drag (`media/flow.png`).

A 5 % grade needs 191.2 N, which is 213.2 W at the wheel and **240 W at the pedals** at 4 km/h, more than twice sustained rider output (R13 **not met** unassisted). On 110 W the trike climbs at only 1.8 km/h. The rear tyre needs a grip coefficient of 0.26 to drive up the grade.

With a 32/24 drive and the hub's 0.75 low ratio, the development is 1.60 m per crank turn in low gear (2.13 and 2.84 m in middle and high). At 4 km/h in low gear the cadence is 42 rpm, the mean crank torque 55 N·m and the mean pedal force 321 N; in high gear at 70 rpm the trike does 11.9 km/h.

With assist route C (a 250 W mid-drive on a SwapCell pack), the loaded trike climbs 5 % at 6.0 km/h, which meets R13. It uses about 8.1 Wh/km on the flat at 12 km/h, about 56 km per SwapCell pack, and about 52 Wh/km on a 5 % climb.

## 5. Steering, turning and stability

Each front wheel turns in a standard 20 in fork on its own headset, with the kingpin on the wheel centre line, and the steering arms point at the rear axle centre, so the wheels follow Ackermann geometry about a turn centre on the rear axle line. At the 40° inner lock the outer wheel is at 29.5°, the turn centre is 2.15 m from the centre line, and the outer tyre sweeps a **5.95 m** turning circle (R9 met, 50 mm inside 6 m). The box front corner sweeps 6.15 m.

The inner lock is set by clearance. At full lock the steered inner tyre reaches 313 mm from the centre line at the height of the box floor, against the box side at 280 mm, and 347 mm at the knuckle post plates, against the post's outer face at 328 mm. Both gaps are 19 to 33 mm, before mudguards.

Because the kingpins pass through the wheel centres and the box no longer turns, the contact triangle and every mass stay where they are at any lock, so the tipping threshold is the same straight or at full lock.

*Table 3. Tipping thresholds (R10: 0.30 g loaded; 0.22 g rider only, with a cornering-speed label).*

| Case | Threshold, any lock | Speed at the threshold |
| --- | --- | --- |
| Loaded, 80 kg rider, 150 kg cargo | 0.41 g | 16.2 km/h on a 5 m radius; 11.2 km/h at full lock |
| 90 kg rider, 140 kg cargo | 0.39 g | 15.8 km/h on a 5 m radius |
| Rider only, 80 kg | 0.24 g | 12.3 km/h on a 5 m radius; 8.3 km/h at full lock |
| Rider only, 90 kg | 0.23 g | 12.0 km/h on a 5 m radius |

R10 as restated is **met**. Under box steering (v0.1) the empty trike tipped at 0.11 g and 5.8 km/h at full lock; that case is gone. The rider-only margin is small, so the cornering-speed label (BOM item 14) is set at 70 % of the tip-up lateral acceleration, rounded down: **6 km/h in full-lock turns when empty**, and 14 km/h on a 10 m radius. Raising the rider-only case to 0.30 g would still need about 30 kg of low ballast. The raised box floor costs the loaded case 0.02 g (0.43 to 0.41 g).

## 6. Structure (R2)

Bending stresses in the plates are low. Stability, torsion and joint behavior govern, as ITDP found in traditional rickshaws. The rear frame and rider (116 kg) hang on a single rear wheel, so any roll moment passes through the head tube joint into the spine as torsion. With the bed now fixed, that joint is a clamped connection, not a bearing.

*Table 4. Structural checks (dynamic factor 2.5 unless stated).*

| Check | Value | Result |
| --- | --- | --- |
| Spine torsion, 0.5 g roll (512 N·m) | 9.2 MPa in the closed 63 x 150 mm box (569 MPa if the covers were left out) | Met |
| Cover tabs, shear flow 28 N/mm | 86 MPa bearing, 10 tabs per edge over 280 mm | Acceptable; tab count to confirm in FEA |
| Upper stay strip, 2.49 kN compression per plate | Buckling safety factor 2.09 with a 100 mm strip braced at 300 mm (0.51 without the stay bridge) | Marginal; buckling governs the stays |
| Bed-to-spine joint, fixed bed | 396 N shear and 155 N·m pitch moment (static, loaded) | Carried by the collar and yoke clamps |
| Spine bending at the stay front node | 876 N·m, 17 MPa (joint moment and shear, dynamic, plus 0.5 g braking) | Met |
| Head tube joint under 0.5 g roll | Couple 2.56 kN with the 200 mm head tube (3.41 kN with 150 mm); 640 N per yoke-to-collar bolt against a 3.12 kN slip load | Met on paper; the headset bearings no longer carry it |
| Front axle beam, 5.49 kN on a 566 mm span | 15.5 MPa (twin 3 x 180 mm plates with windows); 8.3 MPa under the R2 proof load of 2.94 kN | Met |
| Knuckle post cantilever, 2.75 kN per wheel | 12.5 MPa at the window | Met |
| Knuckle post column, 314 N·m | 47 MPa in the closed 45 x 90 mm box (155 MPa if the cheeks were left out) | At risk: highest stress in the frame; FEA needed |
| Knuckle headsets | 2.75 kN axial per headset, dynamic | Within bicycle headset use; rating to confirm |
| Stay-to-spine nodes, 2.49 kN per plate | Slip load 3.12 kN per bolt per face; bearing use 7 % if slipped | Met on paper if preload is kept |
| Fatigue at M8 holes | 3.6 MPa per road cycle and 10.8 MPa per pothole, against a 66 MPa limit; about 3 million cycles in 5 years | Met on paper; fretting and slip not assessed |

R2 is **at risk**: the nominal numbers pass, but the stay strips have only about twice their buckling load, the knuckle post columns depend on their cheek plates, and joint slip, fretting and the EN 17860 load cases are unassessed. A plate-and-joint FEA is the next step on paper.

## 7. Braking and parking (R11)

Stopping from 15 km/h in 6 m needs 1.45 m/s² (2.22 m/s² if 0.5 s of reaction is counted inside the 6 m), from 2.6 kJ of kinetic energy. Shared equally, each drum must give about **37 N·m**, and the front pair alone needs a tyre grip coefficient of only 0.20. Parking on a 10 % grade needs 293 N, or **37 N·m** per front drum with the latch on the front pair. The drum torque rating of the chosen hubs has not been read.

Holding 10 km/h down a 5 % grade puts 274 W into the drums. With the assumed heat capacity (431 J/K each) and cooling (0.5 W/K), the steady rise would be 183 K, and the drums reach a 100 K rise after 11.4 min, or about **1.9 km** of continuous descent. R11 is **at risk**.

## 8. Assembly, repair and service life (R7, R14, R16)

At 1.5 min per bolt set plus the wheels, steering column, knuckle headsets and forks, tie rod and drag link, drivetrain, brakes, seat, bars, box and a final torque check, assembly is about 6.2 person-hours, or **4.0 h** for two people working 70 % in parallel (R7 **at risk**, at the limit).

A spine side plate disturbs 42 bolts and takes about **78 min** to replace, inside the 90 min now allowed for that plate alone (R14 met, FTK-DDR-002 item 17). A knuckle post plate disturbs 8 bolts and takes about 27 min; the wheel, fork and collar plates stay in place.

Unprotected 3 mm steel at the upper first-year corrosion rate of ISO 9223 category C3 (50 µm) or C4 (80 µm), with a time exponent of 0.6, loses about 0.26 to 0.42 mm over 5 years across both faces. R16 **cannot be verified at TRL 3**.

## 9. Cost (R15, R18)

The pedal-only prototype costs **$709** in `bom/bom.csv` (15 lines, every line priced), $91 inside the $800 budget (R15 met). The steering line rose from $25 to $85. The optional route C assist kit is $300 without the SwapCell pack, which is priced once in the SwapCell repo.

At 100 units the estimate is **$456** per trike: $74 of steel (one full sheet), $18 of cutting (about 59 m at $0.30/m), $314 of bought parts at 65 % of retail, the plywood box at 60 % and $15 of assembly labour. R18 ($300 at 100 units) is **not met**. By Amish's decision the target stays until the first partner supplies wholesale prices for wheels, hubs and forks (FTK-DDR-002 item 18).

## 10. Results against every requirement

*Table 5. Requirement status at TRL 3. Not met items first.*

| ID | Requirement (target) | Value | Status |
| --- | --- | --- | --- |
| R13 | 5 % grade at 4 km/h without dismounting | 240 W at the pedals needed unassisted; 6.0 km/h with route C assist | **Not met** unassisted |
| R18 | Production cost $300 or less at 100 units | about $456 | **Not met** |
| R2 | Frame strength and fatigue | Stresses 47 MPa or less; stay buckling SF 2.09; knuckle post column 47 MPa | At risk |
| R7 | Two people, 4 h or less, hand tools | about 4.0 h | At risk (at the limit) |
| R11 | Stop from 15 km/h in 6 m; park on 10 % | 37 N·m per drum needed; fade after about 1.9 km of 5 % descent | At risk |
| R16 | 5 years of commercial service | Up to 0.42 mm corrosion loss if unprotected | Not verifiable at TRL 3 |
| R1 | Gross 300 kg or less: 150 kg cargo with an 80 kg rider, 140 kg with a 90 kg rider | 299.8 kg in both cases | Met (0.2 kg margin) |
| R3 | Flat 3 mm plate only, bolted | 34 plates and 72 washers, all flat | Met |
| R4 | One 1,250 x 2,500 mm sheet | 2,190 mm used by the true-shape nest | Met (310 mm margin) |
| R5 | Standard bicycle parts | 20 in ISO 406 wheels and forks, 1 1/8 in headsets, 68 mm BB, 27.2 mm post | Met by design; availability survey pending |
| R6 | 0.4 m³ or less; no piece over 1.0 m | 0.30 m³; longest piece 0.83 m | Met |
| R8 | Empty mass 70 kg or less including the box | 69.8 kg | Met (0.2 kg margin) |
| R9 | Width 1.0 m, length 2.2 m, turning circle 6 m or less | 0.986 m, 2.14 m, 5.95 m | Met |
| R10 | 0.30 g loaded; 0.22 g rider only with a label | 0.41 g loaded; 0.24 g rider only, at any lock; label 6 km/h at full lock | Met |
| R12 | 7 km/h on the flat at 110 W | 7.6 km/h | Met |
| R14 | 30 min per plate or part; 90 min for a spine side plate | 78 min spine side plate; 27 min knuckle post plate | Met |
| R15 | Pedal-only prototype $800 or less | $709 | Met |
| R17 | 150 L box; counter at 0.75 to 0.95 m | 151 L; 0.84 m | Met |

Counts: 12 met, 2 not met, 3 at risk, 1 not verifiable at TRL 3.

## 11. Limits of this note

- EN 17860 test loads and cycle counts were not read. A public summary confirms the series covers multi-track cargo cycles up to 300 kg and that commercial use doubles the pedaling-force test cycles ([ACT Lab](https://act-lab.com/cargo-bike-safety-en-17860/)); the numeric load cases need the standard itself.
- Stress checks are hand calculations on simplified members. A plate-and-joint FEA of the spine box, stays, knuckle posts, head tube clamps and bed is needed before any build decision.
- The steering geometry is idealized: kingpins vertical and through the wheel centres, with no caster, trail or kingpin inclination. Steering feel, self-centering and brake steer need a steering geometry study.
- The raster nest is a check that the plates fit, not a cutting layout.
- Hub, fork and headset ratings, drum heat data and laser-cutting prices are assumptions until supplier data or quotes are obtained.

> **Safety:** These are paper estimates. Nothing in this note shows the frame is safe to ride. The empty trike can still tip in brisk turns (0.24 g), the knuckle post columns and head tube clamps carry the highest loads in the frame, and drum brakes may fade on long loaded descents.
