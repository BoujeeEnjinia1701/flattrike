"""FlatTrike general arrangement drawing FTK-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/FTK-DWG-001.svg, .pdf and .png from the parametric model.
The concept sheet in media/ uses FTK-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Compound  # noqa: E402
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, build_parts, plate_schedule, seat_xy  # noqa: E402

parts = build_parts()
asm = Compound(children=[parts[k] for k in sorted(parts)])
bb = asm.bounding_box()
sched = plate_schedule()
n_pl = sum(v["qty"] for v in sched.values())
area = sum(v["qty"] * v["area_m2"] for v in sched.values())

work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="FlatTrike", title="General arrangement, TRL 3 model", dwg_no="FTK-DWG-001",
          rev="P1", author="Amish Chadha", date="2026-09-25", concept=True,
          material="3 mm S235JR or A36 plate, painted; M8 8.8 bolts, all-metal locknuts. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (FTK-CAL-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 80, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions (mm) and data", [
    f"Overall {bb.size.X:.0f} L x {bb.size.Y:.0f} W x {bb.size.Z:.0f} H (saddle top)",
    f"Wheelbase {P['WB']:.0f}; front track {P['TRACK']:.0f}; wheels 20 in (ISO 406)",
    f"Kingpin {P['KP_X']:.0f} ahead of rear axle; head tube {P['HT_LEN']:.0f} long",
    f"Bottom bracket {P['BB_X']:.0f} ahead, {P['BB_Z']:.0f} high; seat angle {P['SEAT_ANGLE']:.0f} deg",
    f"Saddle top {P['SADDLE_TOP']:.0f} high, {seat_xy(P['SADDLE_TOP'] - 25):.0f} ahead of rear axle",
    f"Spine box 63 wide x 150 deep; stays {2 * P['STAY_IN']:.0f} apart (hub OLD)",
    f"Chain line {P['CHAINLINE']:.0f}; {P['RING_T']}T / {P['SPROCKET_T']}T; cranks {P['CRANK']:.0f}",
    f"Box {P['BOX_L']:.0f} x {P['BOX_W']:.0f} x {P['BOX_H']:.0f}; lid {P['BOX_Z0'] + P['BOX_H'] + P['PLY_WALL']:.0f} high",
    f"{n_pl} plates, {area:.2f} m2 net, t = 3; one 1250 x 2500 sheet",
    "Box steering, 35 deg lock; turning circle 5.67 m",
    "Empty 67.5 kg; gross 297.5 kg (FTK-CAL-001)",
    "Frame not verified: R2 at risk; see FTK-CAL-001",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=124, width=140)
s.save(ROOT / "cad/drawings/FTK-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/FTK-DWG-001.svg, .pdf, .png")
