---
doc_id: FTK-PRB-001
title: FlatTrike problem statement
project: FlatTrike
doc_type: Problem statement
version: "0.5"
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record TRL 2 review decisions (FTK-DDR-001); production cost target; open questions updated
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Rated cargo restated (148 and 138 kg) and partner selection rule recorded, decisions of 2026-10-02"
---

# FlatTrike problem statement

Street vendors and micro-logistics operators in emerging markets need durable cargo tricycles, but imported units are expensive and hard to repair, and the locally built alternatives are heavy, flexible and short-lived. FlatTrike aims at the gap between the two: a cargo tricycle whose steel frame is cut from flat plate by any laser or waterjet shop from open files, bolts together without welding, uses standard bicycle parts, and ships flat. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

Street vending and small-scale carrying are among the largest sources of urban self-employment in South Asia, sub-Saharan Africa and Latin America. India alone has an estimated 10 million street vendors, a figure based on about 2.5 % of the urban population ([Observer Research Foundation](https://www.orfonline.org/research/strengthening-urban-india-s-informal-economy-the-case-of-street-vending)). Many of them, and many porters, recyclers and delivery riders, depend on a pedal tricycle or push cart to move 100 to 300 kg of goods every day.

Two kinds of cargo tricycle are on offer, and each fails these users in a different way:

1. **Local workshop tricycles** (loading rickshaws, *thelas* and vending trikes) are cheap, often ₹10,000 to ₹25,000 (about $120 to $300) in Indian online marketplaces ([IndiaMART listings](https://m.indiamart.com/impcat/cycle-rickshaw.html), accessed 2026-09-25). They are built from strengthened bicycle parts and mild steel sections. The Institute for Transportation and Development Policy (ITDP) found that the traditional cycle rickshaw weighs about 80 kg, that its bolted-on structure is "overly flexible and often misaligned", that it has a single gear, and that its wooden frame needs replacing every two to three years ([ITDP, 2006](https://itdp.org/2006/07/01/rickshaws-in-the-new-millennium/)). The rider pays for this in effort, in pushing on every hill and in repairs.
2. **Imported and branded cargo trikes** are lighter, geared and well braked, but cost many times more. Even an open design built under license, such as the XYZ Cargo space-frame bike, retails at about $1,860 ([Bike Hugger](https://www.bikehugger.com/posts/open-source-space-frame-cargo-bike/)). Spares are proprietary, and a broken frame usually means a new vehicle.

Better engineering is possible at low cost. ITDP's India Cycle Rickshaw Improvement Project cut the rickshaw's mass to about 55 kg with an integral tubular frame, added gears, and reported about 50 % higher earnings for operators at a similar price ([ITDP, 2006](https://itdp.org/2006/07/01/rickshaws-in-the-new-millennium/)). But a good tubular frame needs jigs and skilled welding, which is exactly what limits who can build and repair it.

The gap FlatTrike addresses is a frame that is precise without a jig and without welding. Laser and waterjet cutting shops are now common in industrial areas of most mid-sized cities. If the frame is a set of flat plates cut from open files, any such shop can make a new frame or a single replacement plate, and the precision comes from the cutting, not from the builder's skill.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Street vendor | Carry and display 100 to 150 kg of produce, snacks or goods; lock them up; sell from the vehicle | Daily trips of 5 to 20 km; parks for hours; crowded markets and narrow lanes |
| Micro-logistics operator | Deliver or collect goods (parcels, gas cylinders, water cans, recyclables) with the highest load per trip | Stop-start riding in traffic; 20 to 40 km a day; income depends on trips per day |
| Local laser or waterjet shop | Cut a full frame or one plate from open DXF files on a standard sheet | Industrial estate; 3 mm mild steel stock; no bicycle expertise |
| Bicycle mechanic or small fabricator | Assemble, maintain and repair the trike with hand tools and standard bicycle spares | Roadside or market stall; no welding in many cases |
| Cooperative or NGO | Buy frames in batches, train builders, lease trikes to vendors | Municipal vending zones and livelihood programs |

### Operating environment

- **Roads:** asphalt with potholes, speed bumps, broken paving and unpaved lanes; grades up to about 5 % on common routes and short ramps steeper.
- **Loads:** rider 60 to 90 kg; 100 to 150 kg of cargo, often stacked high; occasional overloading well beyond the rating.
- **Climate:** ambient 10 to 45 °C, monsoon rain, dust, coastal salt air in some cities; the vehicle is usually parked outdoors.
- **Use:** 6 to 7 days a week, several years of commercial service, frequent parking on slopes and curbs.
- **Supply chain:** bicycle spares (20 in wheels, 1 1/8 in headsets, 1/8 in chains, drum and hub-gear parts) are available in towns; laser cutting of 3 mm mild steel is available in most industrial areas.

## Constraints

- Garage-buildable pedal-only prototype for about $800 USD in parts (`project.yaml`); the optional electric assist and any SwapCell pack are outside this budget (decided by Amish, 2026-09-25, FTK-DDR-001).
- Production cost of $300 or less per trike at 100 units, so that the design can compete on value with local workshop tricycles (decided by Amish, 2026-09-25; FTK-REQ-001 R18). The target is kept until the first partner supplies wholesale prices (FTK-DDR-002).
- Gross mass of 300 kg or less, so the rated cargo is 148 kg with a rider up to 80 kg and 138 kg with a rider up to 90 kg (decided by Amish, 2026-09-25, FTK-DDR-002, and restated for the constructable design on 2026-10-02, FTK-DDR-003 A1).
- Every steel part is cut from flat sheet by laser or waterjet from open files. No welding.
- Joints are bolted with locknuts and can be taken apart and rebuilt.
- Moving parts (wheels, hubs, brakes, drivetrain, headset, seat) are standard bicycle parts available in regional markets.
- The frame ships flat and is assembled by the user, a mechanic or a cooperative.
- Mass, stiffness and durability must beat the local workshop tricycle, or it will not be adopted at any price.
- Cargo bike standard EN 17860 (in development since 2024) sets requirements for cargo cycles up to 300 kg gross, with stricter limits for commercial use ([ACT Lab](https://act-lab.com/cargo-bike-safety-en-17860/)); it is the reference for load cases even where it is not law.

## Out of scope

- Motor tricycles and petrol or high-power electric three-wheelers (auto-rickshaws, e-rickshaws).
- Passenger rickshaws; FlatTrike carries goods and one rider only.
- Designing a battery or motor. An electric assist option would use an existing kit (see FTK-PRC-001).
- Vending-specific fit-outs (cooking stations, refrigeration, awnings) beyond a lockable box whose lid serves as a counter.
- Heavy-duty cargo platforms such as CargoMule.

## Prior work

- **Traditional and improved cycle rickshaws.** ITDP's work in India documents the weight, flex and single-speed problems of the traditional design and shows that a redesigned rickshaw at about 55 kg with gears raises operator income ([ITDP, 2006](https://itdp.org/2006/07/01/rickshaws-in-the-new-millennium/)).
- **Bolted space-frame cargo bikes.** N55's XYZ Cargo bikes are built from standard aluminium tubes joined with stainless bolts and no welding, published under CC BY-NC-SA 4.0 ([N55](https://www.n55.dk/MANUALS/SPACEFRAMEVEHICLES/XYZCARGO.html)). They prove a bolt-together cargo cycle can carry real loads for years, but the license bars commercial use without a partnership, and tube frames still need accurate cutting and drilling by hand.
- **Home-built bolted trikes.** An open write-up of a bolted aluminium utility trike, built with a hacksaw and drills, shows the approach works for a single maker carrying 45 kg or more ([AprilWick](https://kg6gfq.gitlab.io/bolted-aluminum-utility-trike.html)).
- **Sheet metal bicycle frames.** Ronin Bicycle Works folded laser-cut 0.6 mm aluminium sheet into a riveted frame under 1.4 kg with no welding ([New Atlas](https://newatlas.com/ronin-folded-sheet-metal-bicycles/22120/)). It shows that cut sheet can make a stiff frame, but needs folding and a skilled builder.
- **Rugged utility bicycles.** World Bicycle Relief's Buffalo bicycle is designed for rural loads with a 100 kg carrier rating, local assembly and a mechanic training program ([World Bicycle Relief](https://worldbicyclerelief.org/the-bike/)). It is the model for FlatTrike's repair and training approach.

No open, commercially usable cargo tricycle cut entirely from flat plate was found in this search. That is the niche FlatTrike targets; a wider search is part of TRL 3.

## Open questions

- Which partner organization and which city first (for example a vendor union, a livelihood NGO or a university engineering department)? By the portfolio rule decided on 2026-09-25, co-design partners are picked per area later. Selection rule decided 2026-10-02: a city with dense goods delivery on narrow streets, a laser-cutting shop and a bicycle parts market; first candidate type to approach, a cycle-rickshaw or cargo-bike programme such as those ITDP has documented in South Asia.
- The layout is decided as a front loader (FTK-DDR-001). Do vendors in the partner city accept a front loader rather than the common rear-loading *thela*? This must be checked in co-design before the design is frozen.
- What payload do users actually carry, including routine overloading, and what is the steepest regular grade on their routes? The cargo rating now depends on the rider's weight (148 kg up to 80 kg, 138 kg up to 90 kg); co-design must check that vendors can work with that.
- Can laser shops in the target city cut 3 mm plate to the needed tolerance at the assumed price?
- Can the $300 production target (FTK-REQ-001 R18) be reached with wholesale bicycle parts? FTK-CAL-001 v0.2 estimates about $456 per trike at 100 units with Ackermann steering.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (vendor union, NGO, cooperative or university)
- [ ] Run co-design sessions with vendors and delivery riders; record who, where and what was learned
- [ ] Visit a laser shop and a bicycle market in the target city; confirm stock, tolerances and prices
- [ ] Validate load, distance, terrain, parking and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
