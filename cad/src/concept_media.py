"""FlatTrike concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X forward, Y to the left, Z up, ground at Z = 0, rear axle at X = 0.
Layout (proposed, awaiting Amish): tadpole front loader. Two 20 in front wheels carry the
cargo box on a steel bed that pivots about a kingpin behind the box (box steering); the
rider sits over a standard 20 in rear drive wheel. Every steel part is a flat 3 mm plate
that bolts to its neighbors; nothing is welded.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector, Face, Wire, extrude
from concept import Part, render_all

# ---------------- key dimensions ----------------
WHEEL_R = 254.0            # 20 x 2.125 in tyre (ISO 406 rim), outer radius
TYRE_R = 27.0              # tyre section radius
WB = 1450.0                # wheelbase, rear axle to front axle
TRACK = 800.0              # front wheel center-to-center
T = 3.0                    # plate thickness
KP_X = 1000.0              # kingpin axis
BB = (600.0, 265.0)        # bottom bracket (x, z)
SPINE_Y = 30.0             # inner face of each spine plate
STAY_Y = 70.0              # inner face of each rear stay plate
BOX_X0, BOX_X1 = 1065.0, 1860.0
BOX_W, BOX_Z0, BOX_Z1 = 700.0, 400.0, 780.0
PLY = 12.0

STEEL = "#64748B"
STEEL2 = "#94A3B8"
TYRE = "#1F2937"


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def tube3(a, b, r):
    """Round bar between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def plate_xz(pts, y0, t=T, hole=None):
    """Flat plate drawn in the XZ plane (side profile), thickness t from y0 toward +Y."""
    def face(p):
        return Face(Wire.make_polygon([Vector(x, y0, z) for x, z in p], close=True))
    s = extrude(face(pts), amount=t, dir=(0, 1, 0))
    if hole:
        s = s - extrude(Face(Wire.make_polygon([Vector(x, y0 - 1, z) for x, z in hole], close=True)),
                        amount=t + 2, dir=(0, 1, 0))
    return s


def plate_xy(pts, z0, t=T):
    """Flat plate drawn in plan (XY), thickness t from z0 upward."""
    f = Face(Wire.make_polygon([Vector(x, y, z0) for x, y in pts], close=True))
    return extrude(f, amount=t, dir=(0, 0, 1))


def wheel(cx, cy, cz, hub_r=45.0, hub_len=90.0):
    # tyre as a flat ring: coaxial tori in one compound break the hidden-line projector
    tyre = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(WHEEL_R, 2 * TYRE_R) - Cylinder(WHEEL_R - 42, 2 * TYRE_R + 2))
    rim = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(WHEEL_R - 45, 20) - Cylinder(WHEEL_R - 57, 22))
    hub = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(hub_r, hub_len)
    axle = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(6, hub_len + 50)
    spokes = None
    for k in range(12):
        t = math.radians(k * 30 + 15)
        s = tube3((cx, cy, cz), (cx + (WHEEL_R - 55) * math.cos(t), cy, cz + (WHEEL_R - 55) * math.sin(t)), 2.0)
        spokes = s if spokes is None else spokes + s
    return tyre + rim + hub + axle + spokes


def mirror_pair(fn):
    """Build a left and right copy: fn(side) with side = +1 or -1."""
    return fn(1) + fn(-1)


# ---------------- 1 Spine plates (pair), twin-plate box beam from seat to kingpin ----------------
SPINE = [(220, 840), (320, 840), (975, 575), (975, 300), (640, 210), (520, 210), (465, 300)]
SPINE_HOLE = [(365, 715), (880, 515), (880, 365), (625, 295), (525, 325)]
spine = (plate_xz(SPINE, SPINE_Y, hole=SPINE_HOLE)
         + plate_xz(SPINE, -SPINE_Y - T, hole=SPINE_HOLE))

# ---------------- 2 Rear stay plates (pair), carry the rear dropouts ----------------
STAY = [(-45, 215), (35, 200), (545, 225), (545, 305), (305, 835), (215, 825), (-45, 300)]
STAY_HOLE = [(80, 262), (450, 262), (275, 660)]
stays = plate_xz(STAY, STAY_Y, hole=STAY_HOLE) + plate_xz(STAY, -STAY_Y - T, hole=STAY_HOLE)

# ---------------- 3 Front bed plates: yokes, bulkhead, rails, axle beam, wheel fork plates ----------------
lower_yoke = plate_xy([(975, -45), (975, 45), (1250, 300), (1250, -300)], 287)
upper_yoke = plate_xy([(975, -45), (975, 45), (1062, 200), (1062, -200)], 600)
bulkhead = box(1060, 1060 + T, -300, 300, 290, 603)
rails = mirror_pair(lambda s: box(1060, BOX_X1, s * 300 - (T if s > 0 else 0), s * 300 + (0 if s > 0 else T), 290, 400))
axle_beam = (box(1417, 1417 + T, -345, 345, 280, 400) + box(1480, 1480 + T, -345, 345, 280, 400))
FORK_IN = [(1370, 225), (1530, 225), (1530, 525), (1370, 525)]
FORK_OUT = [(1395, 225), (1505, 225), (1505, 525), (1395, 525)]
def fork_plates(s):
    yin = s * 345 - (T if s > 0 else 0)
    yout = s * 455 - (0 if s > 0 else T)
    bridge = box(1370, 1530, min(s * 345, s * 458), max(s * 345, s * 458), 525, 525 + T)
    return plate_xz(FORK_IN, yin) + plate_xz(FORK_OUT, yout) + bridge
front_bed = lower_yoke + upper_yoke + bulkhead + rails + axle_beam + mirror_pair(fork_plates)

# ---------------- 4 Spacers, tab-and-slot ribs and M8 bolts ----------------
spacers = (box(470, 540, -SPINE_Y, SPINE_Y, 230, 300)            # rib under the BB, between spine plates
           + box(700, 760, -SPINE_Y, SPINE_Y, 300, 420)         # mid rib
           + box(900, 960, -SPINE_Y, SPINE_Y, 330, 540)         # front rib
           + box(260, 320, -SPINE_Y, SPINE_Y, 760, 820)         # seat node rib
           + mirror_pair(lambda s: box(470, 540, min(s * (SPINE_Y + T), s * STAY_Y), max(s * (SPINE_Y + T), s * STAY_Y), 235, 295))
           + mirror_pair(lambda s: box(240, 300, min(s * (SPINE_Y + T), s * STAY_Y), max(s * (SPINE_Y + T), s * STAY_Y), 770, 820)))
for (bx, bz) in ((505, 265), (730, 360), (930, 435), (930, 500), (290, 790), (270, 795)):
    spacers = spacers + Pos(bx, 0, bz) * Rot(90, 0, 0) * Cylinder(8, 2 * STAY_Y + 24)

# ---------------- 5 Kingpin: head tube with 1 1/8 in headset, clamped to the spine ----------------
kingpin = (Pos(KP_X, 0, 445) * Cylinder(25, 300)
           + Pos(KP_X, 0, 445) * Cylinder(14, 360)
           + box(955, 1000, -SPINE_Y - T - 8, SPINE_Y + T + 8, 330, 380)
           + box(955, 1000, -SPINE_Y - T - 8, SPINE_Y + T + 8, 500, 550))

# ---------------- 6 Front wheels, 20 in with drum brake hubs ----------------
_fw = wheel(0, 0, 0, 45, 106)
front_wheels = Pos(WB, TRACK / 2, WHEEL_R) * _fw + Pos(WB, -TRACK / 2, WHEEL_R) * _fw

# ---------------- 7 Rear wheel, 20 in with 3-speed drum brake hub ----------------
rear_wheel = wheel(0, 0, WHEEL_R, 50, 130)

# ---------------- 8 Drivetrain: BB, cranks, chainring, chain, sprocket, pedals ----------------
bx, bz = BB
CY = 52.0   # chain line, in the gap between the right spine plate and the right stay plate
drivetrain = (Pos(bx, 0, bz) * Rot(90, 0, 0) * Cylinder(22, 2 * SPINE_Y + 2 * T)
              + Pos(bx, 0, bz) * Rot(90, 0, 0) * Cylinder(9, 190)
              + Pos(bx, CY, bz) * Rot(90, 0, 0) * Cylinder(80, 4)
              + Pos(0, CY, WHEEL_R) * Rot(90, 0, 0) * Cylinder(38, 4)
              + tube3((0, CY, WHEEL_R + 38), (bx, CY, bz + 80), 4)
              + tube3((0, CY, WHEEL_R - 38), (bx, CY, bz - 80), 4)
              + tube3((bx, 92, bz), (bx + 70, 92, bz - 155), 10)
              + tube3((bx, -92, bz), (bx - 70, -92, bz + 155), 10)
              + Pos(bx + 70, 125, bz - 155) * Box(90, 60, 20)
              + Pos(bx - 70, -125, bz + 155) * Box(90, 60, 20))

# ---------------- 9 Cargo box, 12 mm exterior plywood with hinged lid (vendor counter) ----------------
yb = BOX_W / 2
cargo_box = (box(BOX_X0, BOX_X1, -yb, yb, BOX_Z0, BOX_Z1)
             - box(BOX_X0 + PLY, BOX_X1 - PLY, -yb + PLY, yb - PLY, BOX_Z0 + PLY, BOX_Z1 + 1))
lid = box(BOX_X0, BOX_X1, -yb, yb, BOX_Z1, BOX_Z1 + PLY)
cargo_box = cargo_box + lid

# ---------------- 10 Seat: seatpost and saddle ----------------
seat = tube3((262, 0, 740), (285, 0, 890), 13.6) + Pos(290, 0, 915) * Box(260, 160, 55)

# ---------------- 11 Handlebar on a stem bolted to the bulkhead ----------------
handlebar = (tube3((1062, 0, 590), (1030, 0, 830), 14)
             + tube3((1030, 0, 830), (905, 0, 850), 14)
             + tube3((905, -290, 850), (905, 290, 850), 11)
             + tube3((905, 290, 850), (860, 320, 850), 13) + tube3((905, -290, 850), (860, -320, 850), 13))

# ---------------- 12 Brake levers, cables and parking latch ----------------
brakes = (Pos(895, 250, 862) * Box(40, 30, 22) + Pos(895, -250, 862) * Box(40, 30, 22)
          + Pos(895, 200, 862) * Box(30, 22, 30)                               # parking latch
          + tube3((895, 250, 850), (1000, 20, 620), 3)                         # cable to rear via kingpin
          + tube3((1000, 20, 620), (880, 38, 560), 3) + tube3((880, 38, 560), (60, 76, 340), 3)
          + tube3((895, -250, 850), (1070, -320, 600), 3)                      # cable to front splitter
          + tube3((1070, -320, 600), (1450, -330, 330), 3)
          + tube3((1450, -330, 330), (1450, 330, 330), 3))

parts = [
    Part("Spine plates (pair)", spine, STEEL, 1, (0, 0, 0)),
    Part("Rear stay plates (pair)", stays, STEEL2, 2, (50, 0, -700)),
    Part("Front bed plates", front_bed, "#475569", 3, (550, 0, 0)),
    Part("Spacers, ribs and M8 bolts", spacers, "#D4A017", 4, (450, 0, -1100)),
    Part("Kingpin and headset", kingpin, "#0F766E", 5, (150, -450, 450)),
    Part("Front wheels, drum brakes (2)", front_wheels, TYRE, 6, (1000, 0, -550)),
    Part("Rear wheel, 3-speed drum hub", rear_wheel, "#374151", 7, (-450, 0, -1350)),
    Part("Drivetrain", drivetrain, "#7C3AED", 8, (-250, 0, -1150)),
    Part("Cargo box and lid, plywood", cargo_box, "#C08A4A", 9, (650, 0, 750)),
    Part("Seat and seatpost", seat, "#111827", 10, (150, 0, 500)),
    Part("Handlebar and stem", handlebar, "#2563EB", 11, (150, 0, 750)),
    Part("Brake levers, cables, parking latch", brakes, "#DC2626", 12, (-100, 0, -2000)),
]

if __name__ == "__main__":
    render_all(
        parts, project="FlatTrike", title="Bolt-together cargo tricycle concept", dwg_no="FTK-DWG-010",
        date="2026-09-25",
        key_figures=["Tadpole front loader, box steering (proposed)",
                     "About 2.1 x 0.96 x 0.94 m; 1.45 m wheelbase; 0.8 m track",
                     "150 kg cargo plus 80 kg rider; about 300 kg gross (estimate)",
                     "Empty mass about 68 kg (estimate; 55 kg target not met)",
                     "All steel parts 3 mm plate on one 1.25 x 2.5 m sheet, bolted",
                     "Base parts about $640 (indicative)"],
        cut=False,
        flow={"title": "rider power to the road, W (estimates: 300 kg gross, flat dirt road, 7.6 km/h)",
              "unit": "W",
              "stages": [("Rider at pedals", 110), ("At the rear wheel", 98), ("Rolling on dirt road", 93)],
              "losses": [(0, "Chain and 3-speed hub (11 %)", 12), (1, "Air drag", 5)]},
    )
    import shutil
    for d in Path("media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
