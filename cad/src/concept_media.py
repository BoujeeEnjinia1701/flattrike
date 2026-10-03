"""FlatTrike concept media (TRL 3), generated from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Massing-plus model; CONCEPT, NOT FOR FABRICATION.

Coordinates in mm. X forward, Y to the left, Z up, ground at Z = 0, rear axle at X = 0.
Layout (decided by Amish, 2026-09-25, FTK-DDR-001): tadpole front loader; Ackermann steering
with a fixed box (decided by Amish, 2026-09-25, FTK-DDR-002). Every steel part is a flat 3 mm plate that bolts to its neighbors;
nothing is welded.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from concept import Part, render_all

from model import NAMES, build_parts  # noqa: E402  (single source of geometry: cad/src/model.py)

_p = build_parts()
_style = {1: ("#64748B", (0, 0, 0)), 2: ("#94A3B8", (50, 0, -700)), 3: ("#475569", (550, 0, 0)),
          4: ("#D4A017", (450, 0, -1100)), 5: ("#0F766E", (150, -450, 450)), 6: ("#1F2937", (1000, 0, -550)),
          7: ("#374151", (-450, 0, -1350)), 8: ("#7C3AED", (-250, 0, -1150)), 9: ("#C08A4A", (650, 0, 750)),
          10: ("#111827", (150, 0, 500)), 11: ("#2563EB", (150, 0, 750)), 12: ("#DC2626", (-100, 0, -2000))}
parts = [Part(NAMES[k], _p[k], _style[k][0], k, _style[k][1]) for k in sorted(_p)]

if __name__ == "__main__":
    render_all(
        parts, project="FlatTrike", title="Bolt-together cargo tricycle concept", dwg_no="FTK-DWG-010",
        date="2026-10-02",
        key_figures=["Tadpole front loader, Ackermann steering, fixed box (decided)",
                     "2.15 x 0.98 x 0.93 m; 1.45 m wheelbase; 0.84 m track",
                     "148 kg cargo plus 80 kg rider; 299.7 kg gross (rated 2026-10-02)",
                     "Empty 71.7 kg (72 kg target); lock stops at the knuckle posts",
                     "37 flat 3 mm plates on one 1.25 x 2.5 m sheet, tab-and-slot, bolted",
                     "Pedal-only prototype parts $728 (target $800)"],
        cut=False, rev="P3",
        flow={"title": "rider power to the road, W (estimates, FTK-CAL-001: 299.7 kg gross, flat dirt road, 7.6 km/h)",
              "unit": "W",
              "stages": [("Rider at pedals", 110), ("At the rear wheel", 98), ("Rolling on dirt road", 93)],
              "losses": [(0, "Chain and 3-speed hub (11 %)", 12), (1, "Air drag", 5)]},
    )
    import shutil
    for d in Path("media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
