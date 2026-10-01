# BOM notes

- All costs are indicative USD prices for a single prototype, updated at TRL 3 (2026-09-25). No supplier quotes have been obtained; they are needed from the target city once a partner is chosen.
- Item numbers 1 to 12 match the callouts in `media/exploded.png` and the parts in `cad/src/model.py`. Items 13 to 15 are not modelled.
- Plate costs assume 3 mm S235JR or A36 class steel at about $1.2 per kg and small-batch laser cutting. Net plate areas come from the model: spine 0.34 m², stays 0.30 m², front bed and knuckle posts 0.54 m² (FTK-CAL-001 v0.2).
- Base prototype, pedal only (items 1 to 14): **$724**, within the $800 `budget_usd` in `project.yaml` (FTK-REQ-001 R15). `docs/04-calcs/sizing.py` checks this total from this file.
- Item 15, the route C assist kit (48 V mid-drive and a SwapCell vehicle receiver to latch class V1), is optional and **not** in the base cost. The SwapCell pack is priced once in the SwapCell repo and excluded here (decided by Amish, 2026-09-25, FTK-DDR-001).
- Item 5 rose from $25 to $85 when Ackermann steering with a fixed box was decided (FTK-DDR-002 item 13): central steering column, two knuckle headsets and head tubes, two 20 in forks, drag link and tie rod. Item 14 now includes the cornering-speed label (FTK-DDR-002 item 15, R10).
- Production estimate at 100 units: about $456 per trike against the $300 target (R18, not met). The target stays until the first partner supplies wholesale prices (FTK-DDR-002). See FTK-CAL-001 section 9.
- Design for construction (FTK-DDR-003, 2026-10-01): line 4 now counts 95 bolt sets (was 116), two seat tube saddles, 78 washers and four spacer tubes ($35, was $38); line 5 adds a third fork cut down as the steering column and four U-bolts ($92, was $85); line 10 adds a bought seat tube and two shaft collars ($24, was $18); line 11 a tall quill stem ($20, was $15). Base prototype $724 (was $709).
