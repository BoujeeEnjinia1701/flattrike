---
doc_id: FTK-CAL-001
title: FlatTrike sizing and first-principles checks
project: FlatTrike
doc_type: Calculation note
version: "0.6"
status: Draft
date: '2026-10-02'
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
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Re-run on the constructable design (FTK-DDR-003); bolt, tab and node counts read from the model; R1 and R8 not met by 1.2 kg, R14 not met for knuckle post plates
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Requirement table restated for the 2026-10-02 decisions (R1 148 and 138 kg, R8 72 kg, R14 60 min for knuckle post plates); text only, no computed number changed"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Re-run with the 2026-10-02 decisions carried into the script and model: rated cargo 148 and 138 kg, R8 72 kg, R14 60 min for a knuckle post plate, steering lock stops added, turning circle from the built linkage, first-pass steering geometry study (section 5a)"
---

# FlatTrike sizing and first-principles checks

This version checks the constructable design of FTK-DDR-003: every plate joint drawn (tabs, slots and bolts into T-slots), the yokes clamping the head tube, a parallelogram steering linkage, steering arms below the knuckle posts and the knuckle posts rebuilt. It includes the decisions of 2026-10-02 (FTK-DEC-001): the cargo is rated at 148 kg with a rider up to 80 kg or 138 kg with a rider up to 90 kg, R8 is 72 kg, R14 allows 60 min for a knuckle post plate, and a steering lock stop is fitted at each knuckle post. On paper, twelve of the eighteen requirements are met, three are at risk and one cannot be verified at TRL 3. One is **not met**: R13 without assist (239 W needed at the pedals on a 5 % grade). R18 is over its value-engineering target (about $466 per trike at 100 units against $300, USD 166 over). Assembly (R7) sits about 4 minutes over its 4 h limit, accepted on 2026-10-02 and timed at TRL 4. The empty mass leaves only 0.3 kg under R8.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads plate outlines, areas, part centroids and key dimensions from the parametric model `cad/src/model.py`, and prices from `bom/bom.csv`, so the model, the drawing FTK-DWG-001 and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Layout and steering | Tadpole front loader; Ackermann steering with a fixed box; kingpins on the front wheel centre lines; 40° inner lock, set by a lock stop at each knuckle post | Decided, FTK-DDR-001 item 1 and FTK-DDR-002 item 13; lock set by tyre clearance under the box |
| Rated load | 148 kg cargo with an 80 kg rider; 138 kg cargo with a 90 kg rider | FTK-REQ-001 R1, restated on 2026-10-02 (FTK-DDR-003, A1); the final label is set from the weighed trike |
| Plate | 3 mm S235JR or A36, 7,850 kg/m³ (23.6 kg/m²), yield 235 MPa, E = 210 GPa | Decided, FTK-DDR-001 item 4 |
| Plywood | 700 kg/m³; 12 mm floor, 9 mm walls and lid | Exterior grade |
| Rider centre of mass | 20 mm ahead of the saddle, 160 mm above its top: 0.42 m ahead of the rear axle, 1.09 m high | Upright seated rider; saddle on a 73° seat line |
| Cargo centre of mass | Centre of the box interior: 1.48 m ahead, 0.66 m high | Uniform load |
| Bought part masses | Front wheels 5.8 kg (pair), rear wheel 3.8, drivetrain 3.0, steering 4.7 (central headset, 200 mm head tube and column 1.25; two knuckle headsets and 120 mm head tubes 1.05; two 20 in steel forks 1.8; drag link, tie rod and rod ends 0.6), seat 1.4, bars 1.2, brakes 0.7, box hardware 1.0, paint 0.6, accessories 1.5 kg | Typical steel utility parts |
| Fasteners | 97 M8 class 8.8 bolt sets at 28 g, counted from the model's joints; 78 cut spacer washers; four 60 mm spacer tubes and four U-bolts (0.30 kg); seat tube and collars (0.45 kg) | `cad/src/model.py`; all-metal locknuts decided |
| Riding | Crr 0.015, CdA 0.9 m², air 1.2 kg/m³, drivetrain 89 %, rider 110 W sustained | As TRL 2 |
| Gearing | 32T chainring, 24T sprocket, hub ratios 0.75, 1.00 and 1.33 | Typical 3-speed hub |
| Dynamic factor | 2.5 on static loads for potholes and curbs | EN 17860 test loads not read (section 11) |
| Bolted joints | Preload 15.6 kN at 25 N·m (K = 0.2); slip factor 0.20 on painted faces | Typical |
| Fatigue | Plate with holes treated as a 90 MPa detail, constant-amplitude limit 66 MPa | Eurocode 3 practice for members with holes; to confirm |
| Drums | 0.35 kg iron drum and 0.30 kg aluminium shell per hub; heat loss 0.5 W/K at 10 km/h | Assumed; no hub data read |
| Assist (route C only) | 250 W mid-drive, 80 % motor and controller, SwapCell 457 Wh per cycle at the terminals | SWC-CAL-001 |
| Production (R18) | One full sheet at $1.0/kg, cutting at $0.30/m, bought parts at 65 % of prototype retail, plywood at 60 %, $15 assembly labour | Assumed volume rates; no quotes |

## 2. Geometry, plates and nesting

The parametric model is 2.15 m long, 0.984 m wide and 0.93 m high to the saddle, on a 1.45 m wheelbase and 0.84 m track. It has 37 cut plates with a net area of 1.31 m² (31.0 kg), plus 78 spacer washers cut from the offcuts, so every frame part is still flat 3 mm plate (R3). The head tubes, seat tube, bottom bracket shell and spacer tubes are bought steel sections, and the forks are bought bicycle forks (one cut down as the steering column).

Ackermann steering replaced the four fork plates and four crown plates with two closed knuckle posts and added a drop arm and two steering arms (27 to 34 plates); making the design constructable added two seat tube saddles and two steering arm clamp plates and removed a rib and the two head tube collar plates (35 plates); the two steering lock stops of 2026-10-02 make 37. A shelf nest of bounding rectangles would need 2,669 mm of a 2,500 mm sheet. The script therefore also runs a true-shape nest: each plate outline, less its windows, is rasterized at 5 mm, grown by one cell for raster error and by two more for a 10 mm gap, and placed largest first, bottom-left, in four orientations, with small parts allowed inside the windows of large ones. That nest uses **1,940 mm** of the sheet (R4 met, 560 mm spare). The plates use 42.1 % of the sheet by net area. A DXF nest by the cutting shop is still needed.

The box, now 820 x 560 x 360 mm with its floor at 0.47 m, holds 151 L with the lid (counter) at 0.84 m (R17). Plates and box panels stack about 205 mm deep on a 0.86 x 0.62 m footprint; with the three wheels and forks stacked beside them the crate is about 1.38 x 0.62 x 0.36 m, or 0.31 m³ (R6). The longest cut plate is the 852 mm bed rail.

## 3. Mass and centre of mass

The empty trike is **71.7 kg** against the 72 kg target of 2026-10-02 (R8 met on paper, 0.3 kg under). Plates are 43 % of it (31.0 kg) and the box 18 % (12.7 kg); bolts and washers add 3.6 kg. The two steering lock stops, their bolts and the longer steering arm clamp plates add about 0.5 kg to the 71.2 kg of v0.5. Against v0.2 (69.8 kg), the plates gain 1.1 kg (covers 12 mm wider each side, solid plate round every joint, smaller windows where joints cross them), the seat tube, collars, spacer tubes and U-bolts add 0.75 kg, and 21 fewer bolt sets save 0.5 kg.

*Table 2. Mass and axle loads.*

| Quantity | Value |
| --- | --- |
| Empty mass | 71.7 kg (R8 met on paper, 0.3 kg under 72 kg) |
| Gross, 80 kg rider and 148 kg cargo | 299.7 kg (R1 met on paper) |
| Gross, 90 kg rider and 138 kg cargo | 299.7 kg (R1 met on paper) |
| Cargo inside 300 kg | 148.3 kg with an 80 kg rider; 138.3 kg with a 90 kg rider |
| Empty trike centre of mass | 0.99 m ahead of the rear axle, 0.50 m high |
| Axle loads, loaded | front 2.19 kN, rear 0.75 kN |

On 2026-10-02 Amish accepted rating the cargo at 148 kg with a rider up to 80 kg and 138 kg with a rider up to 90 kg, and R8 at 72 kg (FTK-DDR-003, A1), and every figure in this note and `results.csv` is computed at that rating. Any growth in mass comes straight off the rated cargo: only 0.3 kg is left before the 148 kg and 138 kg ratings must fall again. Lightening windows in the knuckle post arms and yokes (about 0.5 kg) and a lighter box are to be tried in the FEA session, and the final load label is set from the weighed trike.

## 4. Riding power, gearing and assist

At 299.7 kg gross, rolling resistance is 44.1 N and 110 W at the pedals gives 97.9 W at the wheel, for a flat cruise of **7.6 km/h** (R12 met): 92.9 W goes to rolling and 5.0 W to drag (`media/flow.png`).

A 5 % grade needs 191.1 N, which is 213.1 W at the wheel and **239 W at the pedals** at 4 km/h, more than twice sustained rider output (R13 **not met** unassisted). On 110 W the trike climbs at only 1.8 km/h. The rear tyre needs a grip coefficient of 0.26 to drive up the grade.

With a 32/24 drive and the hub's 0.75 low ratio, the development is 1.60 m per crank turn in low gear (2.13 and 2.84 m in middle and high). At 4 km/h in low gear the cadence is 42 rpm, the mean crank torque 55 N·m and the mean pedal force 321 N; in high gear at 70 rpm the trike does 11.9 km/h.

With assist route C (a 250 W mid-drive on a SwapCell pack), the loaded trike climbs 5 % at 6.0 km/h, which meets R13. It uses about 8.1 Wh/km on the flat at 12 km/h, about 56 km per SwapCell pack, and about 52 Wh/km on a 5 % climb.

## 5. Steering, turning and stability

Each front wheel turns in a standard 20 in fork on its own headset, with the kingpin on the wheel centre line, and the steering arms point at the rear axle centre, so the wheels follow Ackermann geometry about a turn centre on the rear axle line. At the 40° inner lock ideal Ackermann geometry would put the outer wheel at 29.5°. The built linkage (the model's tie rod and arms, a trapezoid that only approximates Ackermann) puts it at 31.3°, so the outer wheel's axle line meets the rear axle line 1.97 m from the centre line against 2.15 m for the inner wheel's, and the tyres scrub by about 0.18 m at full lock. Taking the turn centre on the outer wheel's axle line, the outer tyre sweeps a **5.64 m** turning circle; even if the turn centre stayed on the inner wheel's line the circle would be 5.95 m (R9 met either way). The box front corner sweeps at most 6.16 m. The drag link, drop arm and left steering arm form a parallelogram, so the handlebar turns as far as the left wheel (40° at full lock). The model sweeps every moving part from full left to full right lock against the fixed structure (`python cad/src/model.py --check`) and nothing touches.

A steering lock stop at each knuckle post (decided 2026-10-02) sets the 40° inner lock: a 77 x 130 mm fin, tabbed and bolted to the front knuckle post plate, which the steering arm clamp plate's front inboard corner meets at 40° and not before (checked on both sides by the model). If the rider forces the bar into the lock with 300 N at one grip, one stop takes about 0.84 kN at 107 mm from the kingpin axis. The fin's 30 mm leg carries it at 47 MPa in its own plane and 94 MPa out of plane from contact friction, against 235 MPa yield, and the fin bolt sees 1.4 kN against a 15.6 kN preload.

The inner lock is set by clearance. At full lock the steered inner tyre reaches 313 mm from the centre line at the height of the box floor, against the box side at 280 mm, and 364 mm at the knuckle post plates, against the post's outer edge at 338 mm. The gaps are 26 to 33 mm, before mudguards.

Because the kingpins pass through the wheel centres and the box no longer turns, the contact triangle and every mass stay where they are at any lock, so the tipping threshold is the same straight or at full lock.

*Table 3. Tipping thresholds (R10: 0.30 g loaded; 0.22 g rider only, with a cornering-speed label).*

| Case | Threshold, any lock | Speed at the threshold |
| --- | --- | --- |
| Loaded, 80 kg rider, 148 kg cargo | 0.41 g | 16.2 km/h on a 5 m radius; 11.2 km/h at full lock |
| 90 kg rider, 138 kg cargo | 0.39 g | 15.7 km/h on a 5 m radius |
| Rider only, 80 kg | 0.24 g | 12.3 km/h on a 5 m radius; 8.2 km/h at full lock |
| Rider only, 90 kg | 0.23 g | 12.0 km/h on a 5 m radius |

R10 as restated is **met**. Under box steering (v0.1) the empty trike tipped at 0.11 g and 5.8 km/h at full lock; that case is gone. The rider-only margin is small, so the cornering-speed label (BOM item 14) is set at 70 % of the tip-up lateral acceleration, rounded down: **6 km/h in full-lock turns when empty**, and 14 km/h on a 10 m radius. Raising the rider-only case to 0.30 g would still need about 30 kg of low ballast. The raised box floor costs the loaded case 0.02 g (0.43 to 0.41 g).

## 5a. Steering geometry, first pass

Decided on 2026-10-02: caster, trail, kingpin inclination, scrub radius and self-centring are studied on paper before the first ride, with the bought fork's rake as input. This first pass uses the model as drawn; the FEA session repeats it with the rake measured on the chosen fork.

*Table 3a. Steering geometry of the model as drawn.*

| Quantity | Value | Effect |
| --- | --- | --- |
| Caster angle | 0° (knuckle head tubes vertical) | No gravity self-centring |
| Kingpin inclination | 0° | No gravity self-centring |
| Scrub radius | 0 mm (steering axis in the wheel's centre plane) | Little brake steer from an uneven drum |
| Trail, straight fork (0 mm offset) | 0 mm | Neutral |
| Trail, 30 mm offset fork fitted as sold (crown forward) | 30 mm negative; about 6.6 N·m per wheel pulling into the turn at 0.2 g, loaded | Steering would run into the turn |
| Trail, 30 mm offset fork turned to trail | 30 mm; about 6.6 N·m per wheel centring at 0.2 g | Self-centring |
| Trail, 45 mm offset fork, either way | 45 mm; about 9.9 N·m per wheel | As above, stronger |

With vertical head tubes, any fork offset ahead of the steering axis gives negative trail, so a fork fitted as sold would pull the steering into a turn. Turning each knuckle fork round so its offset trails, or a fork with no offset, is the first option to study; head tube caster would need the knuckle posts redrawn. This is a safety point before the first ride (build plan safety stop S6).

## 6. Structure (R2)

Bending stresses in the plates are low. Stability, torsion and joint behavior govern, as ITDP found in traditional rickshaws. The rear frame and rider (117 kg) hang on a single rear wheel, so any roll moment passes through the head tube joint into the spine as torsion. With the bed now fixed, that joint is a clamped connection, not a bearing.

*Table 4. Structural checks (dynamic factor 2.5 unless stated).*

| Check | Value | Result |
| --- | --- | --- |
| Spine torsion, 0.5 g roll (516 N·m) | 9.3 MPa in the closed 63 x 150 mm box (573 MPa if the covers were left out) | Met |
| Cover tabs, shear flow 28 N/mm | 87 MPa bearing on 3 x 3 mm faces, 10 tabs per edge over the 280 mm closed box (the model's count) | Acceptable; confirm in FEA |
| Upper stay strip, 2.59 kN compression per plate | Buckling safety factor 2.01 with a 100 mm strip braced at 300 mm (0.49 without the stay bridge) | Marginal; buckling governs the stays |
| Bed-to-spine joint, fixed bed | 406 N shear and 150 N·m pitch moment (static, loaded) | Carried by the yokes' tabs and bolts |
| Spine bending at the stay front node | 877 N·m, 17 MPa (joint moment and shear, dynamic, plus 0.5 g braking) | Met |
| Head tube joint under 0.5 g roll | Couple 2.58 kN with the 200 mm head tube (3.44 kN with 150 mm), from the cups into the yokes; 27 MPa bearing on one yoke's two tabs | Met on paper; the headset bearings do not carry it |
| Front axle beam, 5.49 kN on a 566 mm span | 36 MPa (twin 3 x 120 mm plates with windows, shallower so the steering arms pass beneath); 19 MPa under the R2 proof load of 2.94 kN | Met |
| Knuckle post arm, 2.74 kN per wheel | 16 MPa at its root (two plates, 120 mm deep) | Met |
| Knuckle collar plates | The cup flange bears on the lower collar plate within 2.5 mm of the post plates, so the plate is not bent | Met by layout |
| Knuckle post column, 314 N·m | 40 MPa in the closed 45 x 50 mm box (155 MPa if the cheeks were left out) | At risk: highest stress in the frame; FEA needed |
| Knuckle headsets | 2.74 kN axial per headset, dynamic | Within bicycle headset use; rating to confirm |
| Stay-to-spine nodes, 2.59 kN per plate | Slip load 3.12 kN per bolt per face; bearing use 7 % if slipped | Met on paper if preload is kept |
| Fatigue at M8 holes | 3.8 MPa per road cycle and 11.3 MPa per pothole, against a 66 MPa limit; about 3 million cycles in 5 years | Met on paper; fretting and slip not assessed |

R2 is **at risk**: the nominal numbers pass, but the stay strips have only about twice their buckling load, the knuckle post columns depend on their cheek plates, and joint slip, fretting and the EN 17860 load cases are unassessed. A plate-and-joint FEA is the next step on paper.

## 7. Braking and parking (R11)

Stopping from 15 km/h in 6 m needs 1.45 m/s² (2.22 m/s² if 0.5 s of reaction is counted inside the 6 m), from 2.6 kJ of kinetic energy. Shared equally, each drum must give about **37 N·m**, and the front pair alone needs a tyre grip coefficient of only 0.20. Parking on a 10 % grade needs 293 N, or **37 N·m** per front drum with the latch on the front pair. The drum torque rating of the chosen hubs has not been read.

Holding 10 km/h down a 5 % grade puts 274 W into the drums. With the assumed heat capacity (431 J/K each) and cooling (0.5 W/K), the steady rise would be 183 K, and the drums reach a 100 K rise after 11.4 min, or about **1.9 km** of continuous descent. R11 is **at risk**.

## 8. Assembly, repair and service life (R7, R14, R16)

At 1.5 min per bolt set (97, counted from the model) plus the wheels, steering column, knuckle headsets and forks, pressing the headset and bottom bracket cups, the seat tube, spacer tubes and U-bolts, tie rod and drag link, drivetrain, brakes, seat, bars, box and a final torque check, assembly is about 6.3 person-hours, or **4.07 h** for two people working 70 % in parallel (R7 **at risk**, about 4 minutes over the limit; accepted on 2026-10-02 and to be timed at TRL 4).

A spine side plate's edge tabs sit in the covers and the lower yoke, so replacing one disturbs 30 bolts and takes the steering column and bottom bracket out: about **80 min**, inside the 90 min allowed for that plate (R14 met for it). A knuckle post plate's tabs sit in both collar plates, so the headset cups, fork and wheel come off with them: 12 bolts and about **53 min** against the 60 min allowed for a knuckle post plate on 2026-10-02 (R14 met on paper, 7 min margin).

Unprotected 3 mm steel at the upper first-year corrosion rate of ISO 9223 category C3 (50 µm) or C4 (80 µm), with a time exponent of 0.6, loses about 0.26 to 0.42 mm over 5 years across both faces. R16 **cannot be verified at TRL 3**.

## 9. Cost (R15, R18)

Value-engineering target: USD 800. Estimated cost of the constructable design: USD 728 (USD 72 under the target). That is the pedal-only prototype in `bom/bom.csv` (15 lines, every line priced; R15 within the target). The construction changes added $15: a seat tube and collars, a cut-down fork for the column, U-bolts and a tall quill stem, less 21 bolt sets; the two steering lock stops and their bolts added $4. The optional route C assist kit is $300 without the SwapCell pack, which is priced once in the SwapCell repo.

At 100 units the estimate is **$466** per trike: $74 of steel (one full sheet), $17 of cutting (about 58 m at $0.30/m), $324 of bought parts at 65 % of retail, the plywood box at 60 % and $15 of assembly labour. R18 ($300 at 100 units) is **over the value-engineering target by USD 166**. By Amish's decision the target stays until the first partner supplies wholesale prices for wheels, hubs and forks (FTK-DDR-002 item 18).

## 10. Results against every requirement

*Table 5. Requirement status at TRL 3. Not met items first.*

| ID | Requirement (target) | Value | Status |
| --- | --- | --- | --- |
| R13 | 5 % grade at 4 km/h without dismounting | 239 W at the pedals needed unassisted; 6.0 km/h with route C assist | **Not met** unassisted |
| R18 | Production cost $300 or less at 100 units | about $466 | **Over the value-engineering target by USD 166** |
| R2 | Frame strength and fatigue | Stresses 40 MPa or less; stay buckling SF 2.01; knuckle post column 40 MPa | At risk |
| R7 | Two people, 4 h or less, hand tools | about 4.07 h | At risk (about 4 minutes over; accepted 2026-10-02, timed at TRL 4) |
| R11 | Stop from 15 km/h in 6 m; park on 10 % | 37 N·m per drum needed; fade after about 1.9 km of 5 % descent | At risk |
| R16 | 5 years of commercial service | Up to 0.42 mm corrosion loss if unprotected | Not verifiable at TRL 3 |
| R1 | Gross 300 kg or less: 148 kg cargo with an 80 kg rider, 138 kg with a 90 kg rider (restated 2026-10-02) | 299.7 kg in both cases | Met on paper (FTK-DDR-003, A1); final label from the weighed trike |
| R3 | Flat 3 mm plate only, bolted | 37 plates and 78 washers, all flat; bought tube sections cut to length | Met |
| R4 | One 1,250 x 2,500 mm sheet | 1,940 mm used by the true-shape nest | Met (560 mm margin) |
| R5 | Standard bicycle parts | 20 in ISO 406 wheels and forks, 1 1/8 in headsets, 68 mm BB, 27.2 mm post | Met by design; availability survey pending |
| R6 | 0.4 m³ or less; no piece over 1.0 m | 0.31 m³; longest piece 0.85 m | Met |
| R8 | Empty mass 72 kg or less including the box (relaxed 2026-10-02) | 71.7 kg | Met on paper, 0.3 kg margin (FTK-DDR-003, A1) |
| R9 | Width 1.0 m, length 2.2 m, turning circle 6 m or less | 0.984 m, 2.15 m, 5.64 m through the built linkage (5.95 m upper bound) | Met |
| R10 | 0.30 g loaded; 0.22 g rider only with a label | 0.41 g loaded; 0.24 g rider only, at any lock; label 6 km/h at full lock | Met |
| R12 | 7 km/h on the flat at 110 W | 7.6 km/h | Met |
| R14 | 30 min per plate or part; 90 min for a spine side plate; 60 min for a knuckle post plate (2026-10-02) | 80 min spine side plate; 53 min knuckle post plate | Met on paper (FTK-DDR-003, A2) |
| R15 | Pedal-only prototype $800 or less | $728 | Met |
| R17 | 150 L box; counter at 0.75 to 0.95 m | 151 L; 0.84 m | Met |

Counts: 12 met, 1 not met, 1 over its value-engineering target (R18), 3 at risk, 1 not verifiable at TRL 3.

## 11. Limits of this note

- EN 17860 test loads and cycle counts were not read. A public summary confirms the series covers multi-track cargo cycles up to 300 kg and that commercial use doubles the pedaling-force test cycles ([ACT Lab](https://act-lab.com/cargo-bike-safety-en-17860/)); the numeric load cases need the standard itself.
- Stress checks are hand calculations on simplified members. A plate-and-joint FEA of the spine box, stays, knuckle posts, yokes and bed, with the tab-and-slot joints modelled, is needed before any build decision.
- The steering arms are held to the fork legs by U-bolt friction; the grip needed is not calculated here and is a check at TRL 4.
- The steering geometry study (section 5a) is a first pass on the model as drawn; it is repeated with the measured rake of the chosen fork in the FEA session, before the first ride. Steering feel and brake steer are not quantified.
- The raster nest is a check that the plates fit, not a cutting layout.
- Hub, fork and headset ratings, drum heat data and laser-cutting prices are assumptions until supplier data or quotes are obtained.

> **Safety:** These are paper estimates. Nothing in this note shows the frame is safe to ride. The empty trike can still tip in brisk turns (0.24 g), the knuckle post columns and the yokes at the head tube carry the highest loads in the frame, and drum brakes may fade on long loaded descents.
