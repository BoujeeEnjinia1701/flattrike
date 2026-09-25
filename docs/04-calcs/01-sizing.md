---
doc_id: FTK-CAL-001
title: FlatTrike sizing and first-principles checks
project: FlatTrike
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (geometry, nesting, mass, power, stability, structure, braking, assembly, cost) against every requirement
---

# FlatTrike sizing and first-principles checks

On paper the flat-plate frame is strong enough in bending, but three structural features of the TRL 2 concept would have failed and are changed in the TRL 3 model: the open twin-plate spine (torsion), the flat fork bridges (bending) and the narrow stay strips (buckling). With those changes, eight of the eighteen requirements are met, three are at risk and one cannot be verified at TRL 3. Six are **not met**: R1 with a 90 kg rider (307.5 kg gross), R8 (empty mass 67.5 kg against 55 kg), R10 (rider-only tipping at 0.24 g, and 0.11 g at full box-steering lock), R13 without assist (238 W needed at the pedals), R14 for the spine side plates (about 78 min to replace), and R18 (about $414 per trike at 100 units against $300).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads plate areas, part centroids and key dimensions from the parametric model `cad/src/model.py`, and prices from `bom/bom.csv`, so the model, the drawing FTK-DWG-001 and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Layout and steering | Tadpole front loader, box steering on one kingpin, 35° lock | Decided, FTK-DDR-001 items 1 and 2; lock angle assumed from bed-to-frame clearance |
| Rated load | 150 kg cargo, 80 kg rider (90 kg for the upper case) | FTK-REQ-001 R1 |
| Plate | 3 mm S235JR or A36, 7,850 kg/m³ (23.6 kg/m²), yield 235 MPa, E = 210 GPa | Decided, item 4 |
| Plywood | 700 kg/m³; 12 mm floor, 9 mm walls and lid | Exterior grade; TRL 3 choice within the TRL 2 range |
| Rider centre of mass | 20 mm ahead of the saddle, 160 mm above its top: 0.42 m ahead of the rear axle, 1.09 m high | Upright seated rider; saddle on a 73° seat line |
| Cargo centre of mass | Centre of the box interior: 1.46 m ahead, 0.59 m high | Uniform load |
| Bought part masses | Front wheels 5.8 kg (pair), rear wheel 3.8, drivetrain 3.0, headset and head tube 1.3, seat 1.4, bars 1.2, brakes 0.7, box hardware 1.0, paint 0.6, accessories 1.5 kg | Typical steel-rim utility parts |
| Fasteners | 112 M8 class 8.8 bolt sets at 28 g; 72 cut spacer washers | Joint count in `sizing.py`; all-metal locknuts decided (item 5) |
| Riding | Crr 0.015, CdA 0.9 m², air 1.2 kg/m³, drivetrain 89 %, rider 110 W sustained | As TRL 2 |
| Gearing | 32T chainring, 24T sprocket, hub ratios 0.75, 1.00 and 1.33 | Typical 3-speed hub |
| Dynamic factor | 2.5 on static loads for potholes and curbs | As TRL 2; EN 17860 test loads not read (see section 10) |
| Bolted joints | Preload 15.6 kN at 25 N·m (K = 0.2); slip factor 0.20 on painted faces | Typical |
| Fatigue | Plate with holes treated as a 90 MPa detail, constant-amplitude limit 66 MPa | Eurocode 3 practice for members with holes; to confirm |
| Drums | 0.35 kg iron drum and 0.30 kg aluminium shell per hub; heat loss 0.5 W/K at 10 km/h | Assumed; no hub data read |
| Assist (route C only) | 250 W mid-drive, 80 % motor and controller, SwapCell 457 Wh per cycle at the terminals | SWC-CAL-001 |
| Production (R18) | One full sheet at $1.0/kg, cutting at $0.30/m, bought parts at 65 % of prototype retail, plywood at 60 %, $15 assembly labour | Assumed volume rates; no quotes |

## 2. Geometry, plates and nesting

The parametric model is 2.11 m long, 0.986 m wide and 0.93 m high to the saddle, on a 1.45 m wheelbase and 0.84 m track. It has 27 cut plates with a net area of 1.22 m² (28.6 kg), plus 72 spacer washers cut from the offcuts, so every steel part is still flat 3 mm plate (R3). The head tube and bottom bracket shell are bought steel sections (decided, item 6).

A first-fit shelf nest of the plates' bounding rectangles, with 8 mm gaps and 10 mm edge margins, uses 2,486 mm of a 1,250 x 2,500 mm sheet (R4). This is conservative, because true-shape nesting interlocks the spine and stay plates, but the margin is only 14 mm, so any plate growth must be checked against the DXF nest. The plates use 38.9 % of the sheet by net area.

The box holds 184 L with the lid (counter) at 0.77 m (R17). Plates and box panels stack about 172 mm deep on a 0.80 x 0.80 m footprint; with the three wheels stacked beside them the crate is about 1.35 x 0.80 x 0.36 m, or 0.39 m³ (R6). The longest cut plate is the 800 mm bed rail and the longest piece is the 795 mm box floor.

## 3. Mass and centre of mass

The empty trike is **67.5 kg** against the 55 kg target (R8 **not met**). Plates are 42 % of it (28.6 kg) and the box 22 % (14.7 kg); bolts and washers add 3.9 kg. The TRL 2 figure of about 68 kg was close by chance: the lightening windows saved about 6 kg, but the TRL 2 box mass was low by about 3 kg and the new cover and crown plates add weight.

*Table 2. Mass and axle loads.*

| Quantity | Value |
| --- | --- |
| Empty mass | 67.5 kg |
| Gross, 80 kg rider and 150 kg cargo | 297.5 kg (R1 met, 2.5 kg margin) |
| Gross, 90 kg rider and 150 kg cargo | 307.5 kg (R1 **not met**) |
| Cargo allowed with a 90 kg rider inside 300 kg | 142.5 kg |
| Empty trike centre of mass | 0.98 m ahead of the rear axle, 0.47 m high |
| Axle loads, loaded | front 2.16 kN, rear 0.76 kN |

The loaded trike carries about three quarters of its weight on the front wheels, so the single driven rear wheel is lightly loaded (section 4).

## 4. Riding power, gearing and assist

At 297.5 kg gross, rolling resistance is 43.8 N and 110 W at the pedals gives 97.9 W at the wheel, for a flat cruise of **7.6 km/h** (R12 met): 92.8 W goes to rolling and 5.1 W to drag (media Figure: `media/flow.png`).

A 5 % grade needs 189.7 N, which is 211.5 W at the wheel and **238 W at the pedals** at 4 km/h, more than twice sustained rider output (R13 **not met** unassisted). On 110 W the trike climbs at only 1.9 km/h. The rear tyre needs a grip coefficient of 0.25 to drive up the grade, which is adequate on dry asphalt but at risk on wet or loose surfaces.

With a 32/24 drive and the hub's 0.75 low ratio, the development is 1.60 m per crank turn in low gear (2.13 and 2.84 m in middle and high). At 4 km/h in low gear the cadence is 42 rpm, the mean crank torque 54 N·m and the mean pedal force 319 N; in high gear at 70 rpm the trike does 11.9 km/h. The hub maker's input torque limit must be checked for this low gearing.

With assist route C (a 250 W mid-drive on a SwapCell pack, FTK-DDR-001 item 3), the loaded trike climbs 5 % at 6.0 km/h, which meets R13. It uses about 8.0 Wh/km on the flat at 12 km/h, about 57 km per SwapCell pack, and about 52 Wh/km on a 5 % climb.

## 5. Steering, turning and stability

At 35° of box-steering lock the outer tyre sweeps a **5.67 m** turning circle and the box corner 5.53 m (R9 met, with the 0.986 m width 14 mm inside the 1.0 m limit). At full lock the outer front wheel moves 334 mm inward, because the kingpin is 450 mm behind the front axle.

The tipping threshold is the distance from the centre of mass to the axis through the rear contact and the outer front contact, divided by the height of the centre of mass. The script moves every bed-mounted mass (bed plates, box, cargo, front wheels, handlebar) with the steering angle.

*Table 3. Tipping thresholds (R10 target 0.30 g in every case).*

| Case | Straight | Box steering, full lock | Option B (Ackermann), any lock |
| --- | --- | --- | --- |
| Loaded, 80 kg rider | 0.43 g (16.6 km/h on a 5 m radius) | 0.31 g (tips at 9.8 km/h) | 0.43 g |
| Rider only, 80 kg | **0.24 g** (12.2 km/h on a 5 m radius) | **0.11 g** (tips at 5.8 km/h) | **0.24 g** |
| Rider only, 90 kg | **0.23 g** | | |

R10 is **not met** with no cargo. Moving the seat forward to a 73° seat angle raised the rider-only threshold from the TRL 2 value of 0.18 g to 0.24 g, but closing the gap needs one of: the rider 350 mm further forward (not practical with a rear-drive layout), 30 kg of ballast low in the box, or a wider track (0.25 g at 0.90 m and 0.28 g at 1.0 m, both breaking R9). The more serious finding is box steering at full lock: an empty trike tips at 5.8 km/h in its tightest turn. Ackermann steering (option B) keeps the track constant and removes that case. This is proposed for the first prototype, awaiting Amish (FTK-DDR-001 open item 13).

## 6. Structure (R2)

Bending stresses in the plates are low. The TRL 3 checks found that stability, torsion and joint behavior govern, which is what ITDP found in traditional rickshaws. The rear frame and rider (112 kg) hang on a single rear wheel, so any roll moment passes through the kingpin into the spine as torsion.

*Table 4. Structural checks (dynamic factor 2.5 unless stated).*

| Check | TRL 2 concept | TRL 3 model | Result |
| --- | --- | --- | --- |
| Spine torsion, 0.5 g roll (501 N·m) | 556 MPa shear in two open 3 x 150 mm plates | 9.0 MPa in a closed 63 x 150 mm box with top and bottom covers | Fixed by the covers; GJ rises from 219 to about 196,000 N·m² |
| Cover tabs, shear flow 27 N/mm | | 84 MPa bearing, 10 tabs per edge over 280 mm | Acceptable; tab count to confirm in FEA |
| Fork crown, 1.35 kN outer fork plate load | 619 MPa in a flat 160 x 3 mm bridge | 23 MPa in two vertical 80 mm crown plates | Fixed by the crown plates |
| Upper stay strip, 2.53 kN compression per plate | SF 1.13 with a 55 mm strip braced at 300 mm | SF 2.06 with a 100 mm strip braced at 300 mm (SF 0.50 if the stay bridge were omitted) | Marginal; buckling governs the stays |
| Front axle beam, 5.40 kN on a 730 mm span | | 45 MPa (twin 3 x 110 mm plates with windows) | Met; 24.5 MPa under the R2 proof load of 2.94 kN |
| Spine bending at the stay front node | | 0.7 MPa; the bed carries almost no vertical load into the kingpin (-2 N loaded, 39 N empty) | Negligible |
| Headset under roll | | 3.34 kN radial on each bearing (150 mm spacing) | At risk: a bicycle headset is not designed for this moment |
| Stay-to-spine nodes, 2.53 kN per plate | | Slip load 3.12 kN per bolt per face; 2 bolts per plate per node; bearing use 7 % if slipped | Met on paper if preload is kept |
| Fatigue at M8 holes | | Net stress range 3.7 MPa per road cycle and 11 MPa per pothole, against a 66 MPa limit; about 3 million cycles in 5 years | Met on paper; fretting and slip not assessed |

R2 is **at risk**: the nominal numbers pass, but the stay strips have only about twice the buckling load, the headset carries a roll moment it was not designed for, and joint slip, fretting and the EN 17860 load cases are unassessed. A plate-and-joint FEA is the next step on paper.

## 7. Braking and parking (R11)

Stopping from 15 km/h in 6 m needs 1.45 m/s² (2.22 m/s² if 0.5 s of reaction is counted inside the 6 m), from 2.58 kJ of kinetic energy. Shared equally, each drum must give about **36 N·m**, and the front pair alone needs a tyre grip coefficient of only 0.20. Parking on a 10 % grade needs 290 N, or **37 N·m** per front drum with the latch on the front pair. The drum torque rating of the chosen hubs has not been read, so these are requirements on the hub, not checks.

Holding 10 km/h down a 5 % grade puts 272 W into the drums. With the assumed drum heat capacity (431 J/K each) and cooling (0.5 W/K), the steady rise would be 182 K, and the drums reach a 100 K rise after 11.5 min, or about **1.9 km** of continuous descent. R11 is **at risk** for long descents and cannot be verified at TRL 3 for stopping and parking torque.

## 8. Assembly, repair and service life (R7, R14, R16)

At 1.5 min per bolt set plus the wheels, headset, drivetrain, brakes, seat, bars, box and a final torque check, assembly is about 5.6 person-hours, or **3.6 h** for two people working 70 % in parallel (R7 **at risk**: under 4 h but with little margin and no timed build).

Replacing a fork plate disturbs 6 bolts and takes about 24 min, but a spine side plate disturbs 42 bolts (covers, ribs, stay nodes, collars and bottom bracket) and takes about **78 min** (R14 **not met** for the spine side plates).

Unprotected 3 mm steel at the upper first-year corrosion rate of ISO 9223 category C3 (50 µm) or C4 (80 µm), with a time exponent of 0.6, loses about 0.26 to 0.42 mm of thickness over 5 years across both faces. The paint system and sealed joint faces must hold that off; R16 **cannot be verified at TRL 3**.

## 9. Cost (R15, R18)

The pedal-only prototype costs **$647** in `bom/bom.csv` (15 lines, every line priced), $153 inside the $800 budget (R15 met). The optional route C assist kit is $300 without the SwapCell pack, which is priced once in the SwapCell repo and excluded here (decided, cross-cutting).

At 100 units the estimate is **$414** per trike: $74 of steel (one full sheet), $15 of cutting (about 51 m at $0.30/m), $274 of bought parts at 65 % of retail, the plywood box at 60 % and $15 of assembly labour. R18 ($300 at 100 units) is **not met**; bought bicycle parts are two thirds of the cost, so the target depends on the partner's wholesale prices more than on the frame.

## 10. Results against every requirement

*Table 5. Requirement status at TRL 3. Not met items first.*

| ID | Requirement (target) | Value | Status |
| --- | --- | --- | --- |
| R1 | Gross 300 kg or less with 150 kg cargo and a rider up to 90 kg | 297.5 kg (80 kg rider); 307.5 kg (90 kg rider) | **Not met** at 90 kg |
| R8 | Empty mass 55 kg or less | 67.5 kg | **Not met** |
| R10 | Tipping threshold 0.30 g loaded and rider only | 0.43 g loaded; 0.24 g rider only; 0.11 g rider only at full box-steering lock | **Not met** (rider only) |
| R13 | 5 % grade at 4 km/h without dismounting | 238 W at the pedals needed unassisted; 6.0 km/h with route C assist | **Not met** unassisted |
| R14 | Any plate or part replaced in 30 min or less | 24 min for a fork plate; 78 min for a spine side plate | **Not met** (spine side plate) |
| R18 | Production cost $300 or less at 100 units | about $414 | **Not met** |
| R2 | Frame strength and fatigue | Stresses 45 MPa or less; stay buckling SF 2.06; headset 3.34 kN per bearing | At risk |
| R7 | Two people, 4 h or less, hand tools | about 3.6 h | At risk |
| R11 | Stop from 15 km/h in 6 m; park on 10 % | 36 to 37 N·m per drum needed; fade after about 1.9 km of 5 % descent | At risk |
| R16 | 5 years of commercial service | Up to 0.42 mm corrosion loss if unprotected | Not verifiable at TRL 3 |
| R3 | Flat 3 mm plate only, bolted | 27 plates and 72 washers, all flat | Met |
| R4 | One 1,250 x 2,500 mm sheet | 2,486 mm used by bounding rectangles | Met (14 mm margin) |
| R5 | Standard bicycle parts | 20 in ISO 406, 1 1/8 in headset, 68 mm BB, 27.2 mm post | Met by design; availability survey pending |
| R6 | 0.4 m³ or less; no piece over 1.0 m | 0.39 m³; longest piece 0.80 m | Met |
| R9 | Width 1.0 m, length 2.2 m, turning circle 6 m or less | 0.986 m, 2.11 m, 5.67 m | Met |
| R12 | 7 km/h on the flat at 110 W | 7.6 km/h | Met |
| R15 | Pedal-only prototype $800 or less | $647 | Met |
| R17 | 150 L box; counter at 0.75 to 0.95 m | 184 L; 0.77 m | Met |

Counts: 8 met, 6 not met, 3 at risk, 1 not verifiable at TRL 3.

## 11. Limits of this note

- EN 17860 test loads and cycle counts were not read. A public summary confirms the series covers multi-track cargo cycles up to 300 kg and that commercial use doubles the pedaling-force test cycles ([ACT Lab](https://act-lab.com/cargo-bike-safety-en-17860/)); the numeric load cases need the standard itself.
- Stress checks are hand calculations on simplified members. A plate-and-joint FEA of the spine box, stays and bed is needed before any build decision.
- Hub torque ratings, headset bearing ratings, drum heat data and laser-cutting prices are assumptions until supplier data or quotes are obtained.

> **Safety:** These are paper estimates. Nothing in this note shows the frame is safe to ride. The empty trike can tip at walking pace at full box-steering lock, the headset carries an unusual roll moment, and drum brakes may fade on long loaded descents.
