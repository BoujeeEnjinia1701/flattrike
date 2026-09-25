"""FlatTrike parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the plate schedule
(flat area and bounding size of every cut plate) used by FTK-CAL-001.

Massing-plus level of detail: correct interfaces and main dimensions, not
fabrication detail. PRELIMINARY, NOT FOR FABRICATION.

Coordinates in mm. X forward, Y to the left, Z up, ground at Z = 0, rear axle at X = 0.
Layout (decided by Amish, 2026-09-25, FTK-DDR-001): tadpole front loader with box
steering on one kingpin for the first prototype. Every steel part is flat 3 mm plate
cut from DXF; nothing is welded or bent. TRL 3 changes from the TRL 2 massing model:
closed-box spine (top and bottom cover plates), vertical fork crown plates, seat moved
forward to a 73 degree seat angle, track 0.84 m, box 360 mm high with 9 mm walls.
"""
from __future__ import annotations

import math
from pathlib import Path

from build123d import (Box, Compound, Cylinder, Face, Plane, Pos, Rot, Solid, Vector, Wire,
                       export_step, export_stl, extrude)

# ---------------- parameters (mm); edit these, not the geometry below ----------------
PARAMS = {
    "T": 3.0,                 # plate thickness, S235JR or A36 class
    "WHEEL_R": 254.0,         # 20 x 2.125 in tyre (ISO 406), outer radius
    "TYRE_W": 54.0,           # tyre section width
    "WB": 1450.0,             # wheelbase, rear axle to front axle
    "TRACK": 840.0,           # front wheel centre to centre
    "KP_X": 1000.0,           # kingpin (steering) axis, ahead of the rear axle
    "HT_Z0": 330.0,           # head tube bottom
    "HT_LEN": 150.0,          # head tube length (headset bearing spacing)
    "HT_OD": 40.0,            # head tube outside diameter, 1 1/8 in threaded headset
    "SPINE_IN": 30.0,         # inner face of each spine side plate from the centre plane
    "STAY_IN": 60.0,          # inner face of each rear stay plate (120 mm hub OLD)
    "BB_X": 600.0,            # bottom bracket centre
    "BB_Z": 265.0,
    "SEAT_ANGLE": 73.0,       # seat tube angle, degrees from horizontal
    "SADDLE_TOP": 930.0,      # saddle top height
    "CHAINLINE": 44.0,        # chain plane from the centre plane
    "RING_T": 32,             # chainring teeth
    "SPROCKET_T": 24,         # rear sprocket teeth
    "CRANK": 170.0,
    "FORK_GAP": 110.0,        # inner to outer fork plate (hub width plus clearance)
    "BOX_X0": 1065.0,         # cargo box rear face
    "BOX_L": 795.0,
    "BOX_W": 700.0,
    "BOX_Z0": 400.0,          # box floor underside (top of bed rails)
    "BOX_H": 360.0,
    "PLY_FLOOR": 12.0,
    "PLY_WALL": 9.0,
    "RAIL_Y": 300.0,          # bed rail centre offset
    "STEER_LOCK": 35.0,       # box steering lock, degrees (assumed clearance limit)
}
P = PARAMS
T = P["T"]

STEEL = "#64748B"
STEEL2 = "#94A3B8"
BED = "#475569"
TYRE = "#1F2937"


# ---------------- helpers ----------------
def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def rod(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def circle_pts(cx, cy, r, n=24):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def poly_area(pts):
    a = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


PLATES = []   # plate schedule: dicts with name, bom, qty, area_mm2, size (w, h)


def plate(name, bom, poly, to3d, normal, holes=(), t=T, record=True):
    """Flat plate: 2D profile poly (u, v) mapped by to3d(u, v) -> (x, y, z), extruded t along normal."""
    f = Face(Wire.make_polygon([Vector(*to3d(u, v)) for u, v in poly], close=True))
    s = extrude(f, amount=t, dir=normal)
    n = Vector(*normal)
    for h in holes:
        hf = Face(Wire.make_polygon([Vector(*to3d(u, v)) - n * 1 for u, v in h], close=True))
        s = s - extrude(hf, amount=t + 2, dir=normal)
    if record:
        us = [u for u, _ in poly]; vs = [v for _, v in poly]
        PLATES.append({"name": name, "bom": bom, "area_mm2": poly_area(poly) - sum(poly_area(h) for h in holes),
                       "size": (max(us) - min(us), max(vs) - min(vs))})
    return s


def xz(y0):   # side-profile plate at y0, thickness toward +Y
    return (lambda u, v: (u, y0, v)), (0, 1, 0)


def yz(x0):   # transverse plate at x0, thickness toward +X
    return (lambda u, v: (x0, u, v)), (1, 0, 0)


def xy(z0):   # plan plate at z0, thickness upward
    return (lambda u, v: (u, v, z0)), (0, 0, 1)


def pair_xz(name, bom, poly, y_in, holes=()):
    """Left and right copies of a side plate whose inner faces are at +/- y_in."""
    fl, nl = xz(y_in)
    fr, nr = xz(-y_in - T)
    return plate(name, bom, poly, fl, nl, holes) + plate(name, bom, poly, fr, nr, holes)


def edge_strip(name, bom, p0, p1, half_w, outward, t=T):
    """Cover plate lying on a straight edge p0 -> p1 of the side profile (XZ), spanning +/- half_w in Y."""
    (x0, z0), (x1, z1) = p0, p1
    L = math.hypot(x1 - x0, z1 - z0); ex, ez = (x1 - x0) / L, (z1 - z0) / L
    nx, nz = (-ez, ex) if outward == "left" else (ez, -ex)
    to3d = lambda u, v: (x0 + ex * u, v, z0 + ez * u)
    return plate(name, bom, [(0, -half_w), (L, -half_w), (L, half_w), (0, half_w)], to3d, (nx, 0, nz), t=t)


def wheel(cx, cy, cz, hub_r, hub_len):
    R = P["WHEEL_R"]; tw = P["TYRE_W"]
    tyre = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(R, tw) - Cylinder(R - 42, tw + 2))
    rim = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(R - 45, 20) - Cylinder(R - 57, 22))
    hub = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(hub_r, hub_len)
    axle = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(6, hub_len + 40)
    s = tyre + rim + hub + axle
    for k in range(12):
        a = math.radians(k * 30 + 15)
        s = s + rod((cx, cy, cz), (cx + (R - 55) * math.cos(a), cy, cz + (R - 55) * math.sin(a)), 2.0)
    return s


# ---------------- derived geometry ----------------
def spine_profile():
    """Side profile of the spine box beam: seat node to kingpin, with a drop lobe to the bottom bracket."""
    top0, top1 = (360.0, 800.0), (P["KP_X"] - 25, 490.0)
    return [top0, top1, (P["KP_X"] - 25, 333.0), (720.0, 457.0), (665.0, 215.0), (540.0, 215.0),
            (520.0, 555.0), (294.0, 665.0)]


SPINE = spine_profile()
SPINE_WIN = [(565, 320), (660, 320), (690, 440), (565, 500)]
SPINE_HOLES = [[(340, 700), (495, 624), (495, 700), (400, 748)]]   # rear lightening window, clear of the closed box
STAY = [(-45, 215), (45, 205), (700, 520), (690, 610), (440, 760), (350, 745), (-45, 300)]
STAY_WIN = [(140, 320), (540, 495), (430, 640), (320, 560)]


def seat_xy(z):
    """Point on the seat tube line through the bottom bracket at height z."""
    return P["BB_X"] - (z - P["BB_Z"]) / math.tan(math.radians(P["SEAT_ANGLE"]))


# ---------------- parts, numbered to match bom/bom.csv ----------------
def build_parts():
    PLATES.clear()
    si = P["SPINE_IN"]; st = P["STAY_IN"]; kp = P["KP_X"]
    parts = {}

    # 1 Spine: twin side plates plus top and bottom cover plates (closed box from the BB lobe to the kingpin)
    bb_hole = circle_pts(P["BB_X"], P["BB_Z"], 19.5)
    spine = pair_xz("Spine side plate", 1, SPINE, si, holes=[SPINE_WIN, bb_hole] + SPINE_HOLES)
    spine = spine + edge_strip("Spine top cover", 1, SPINE[0], SPINE[1], si + T, "left")
    spine = spine + edge_strip("Spine bottom cover", 1, SPINE[3], SPINE[2], si + T, "right")
    parts[1] = spine

    # 2 Rear stay plates with dropout slots
    slot = [(-8, 248), (8, 248), (8, 260), (-8, 260)]
    parts[2] = pair_xz("Rear stay plate", 2, STAY, st, holes=[STAY_WIN, slot])

    # 3 Front bed: yokes, bulkhead, rails, twin axle beam, fork plates and crown plates
    tr = P["TRACK"] / 2; fin = tr - P["FORK_GAP"] / 2; fout = tr + P["FORK_GAP"] / 2
    ly_z = P["HT_Z0"] - 18; uy_z = P["HT_Z0"] + P["HT_LEN"] + 25
    steer_hole = circle_pts(kp, 0, 14)
    f, n = xy(ly_z)
    bed = plate("Lower yoke", 3, [(kp - 45, -45), (kp - 45, 45), (1060, 300), (1060, -300)], f, n, [steer_hole])
    f, n = xy(uy_z)
    bed = bed + plate("Upper yoke", 3, [(kp - 45, -45), (kp - 45, 45), (1060, 200), (1060, -200)], f, n, [steer_hole])
    f, n = yz(1060)
    bed = bed + plate("Bulkhead", 3, [(-300, ly_z), (300, ly_z), (300, 620), (-300, 620)], f, n,
                      [[(-240, ly_z + 50), (240, ly_z + 50), (240, 560), (-240, 560)]])
    rail = [(1060, ly_z), (P["BOX_X0"] + P["BOX_L"], ly_z), (P["BOX_X0"] + P["BOX_L"], P["BOX_Z0"]), (1060, P["BOX_Z0"])]
    rail_holes = [[(xh, ly_z + 25), (xh + 120, ly_z + 25), (xh + 120, P["BOX_Z0"] - 25), (xh, P["BOX_Z0"] - 25)]
                  for xh in (1110, 1250, 1540, 1690)]
    bed = bed + pair_xz("Bed rail", 3, rail, P["RAIL_Y"] - T, holes=rail_holes)
    for xb in (P["WB"] - 33, P["WB"] + 30):
        f, n = yz(xb)
        ab_holes = [[(yh, 320), (yh + 120, 320), (yh + 120, 370), (yh, 370)] for yh in (-300, -140, 20, 180)]
        bed = bed + plate("Axle beam plate", 3, [(-fin, 290), (fin, 290), (fin, P["BOX_Z0"]), (-fin, P["BOX_Z0"])], f, n,
                          ab_holes)
    fork = [(P["WB"] - 50, 200), (P["WB"] + 50, 200), (P["WB"] + 80, 600), (P["WB"] - 80, 600)]
    fork_win = [(P["WB"] - 42, 330), (P["WB"] + 42, 330), (P["WB"] + 55, 490), (P["WB"] - 55, 490)]
    axle_hole = circle_pts(P["WB"], P["WHEEL_R"], 6.5, 12)
    crown = [(fin, 520), (fout, 520), (fout, 600), (fin, 600)]
    for s in (1, -1):
        for y_face in (fin, fout):
            y0 = s * y_face - (T if s > 0 else 0) if y_face == fin else s * y_face - (0 if s > 0 else T)
            f, n = xz(y0)
            bed = bed + plate("Fork plate", 3, fork, f, n, [axle_hole, fork_win])
        for xc in (P["WB"] - 80, P["WB"] + 80 - T):
            cr = [(s * u, v) for u, v in crown] if s > 0 else [(-u, v) for u, v in reversed(crown)]
            f, n = yz(xc)
            bed = bed + plate("Fork crown plate", 3, cr, f, n)
    parts[3] = bed

    # 4 Ribs, spacers and M8 bolts (representative; counts are in FTK-CAL-001)
    ribs = None
    for xr in (380.0, 800.0, 930.0):
        ztop = SPINE[0][1] + (SPINE[1][1] - SPINE[0][1]) * (xr - SPINE[0][0]) / (SPINE[1][0] - SPINE[0][0])
        if xr < 520:
            zbot = SPINE[7][1] + (SPINE[6][1] - SPINE[7][1]) * (xr - SPINE[7][0]) / (SPINE[6][0] - SPINE[7][0])
        else:
            zbot = SPINE[3][1] + (SPINE[2][1] - SPINE[3][1]) * (xr - SPINE[3][0]) / (SPINE[2][0] - SPINE[3][0])
        f, n = yz(xr)
        r = plate("Spine rib", 4, [(-si, zbot + 4), (si, zbot + 4), (si, ztop - 4), (-si, ztop - 4)], f, n)
        ribs = r if ribs is None else ribs + r
    f, n = yz(200)
    ribs = ribs + plate("Stay bridge", 4, [(-st, 480), (st, 480), (st, 560), (-st, 560)], f, n)
    for (bx, bz) in ((400, 700), (470, 660), (620, 560), (680, 540)):
        for s in (1, -1):
            ribs = ribs + Pos(bx, s * (si + T + st) / 2, bz) * Rot(90, 0, 0) * (Cylinder(8, st - si - T) - Cylinder(4.2, st))
        ribs = ribs + Pos(bx, 0, bz) * Rot(90, 0, 0) * Cylinder(4, 2 * st + 24)
    parts[4] = ribs

    # 5 Kingpin: head tube with 1 1/8 in threaded headset, clamped to the spine by two collar plates
    hz = P["HT_Z0"]; hl = P["HT_LEN"]
    king = Pos(kp, 0, hz + hl / 2) * (Cylinder(P["HT_OD"] / 2, hl) - Cylinder(17, hl + 2))
    king = king + Pos(kp, 0, (ly_z + uy_z) / 2 + 10) * Cylinder(14, uy_z - ly_z + 40)
    for zc in (hz + 20, hz + hl - 23):
        f, n = xy(zc)
        king = king + plate("Head tube collar plate", 5, [(kp - 75, -si - T - 6), (kp + 30, -si - T - 6),
                                                          (kp + 30, si + T + 6), (kp - 75, si + T + 6)],
                            f, n, [circle_pts(kp, 0, P["HT_OD"] / 2 + 0.5)])
    parts[5] = king

    # 6 Front wheels, 20 in with drum brake hubs
    fw = wheel(0, 0, 0, 45, 106)
    parts[6] = Pos(P["WB"], tr, P["WHEEL_R"]) * fw + Pos(P["WB"], -tr, P["WHEEL_R"]) * fw

    # 7 Rear wheel, 20 in with 3-speed drum brake hub (120 mm OLD)
    parts[7] = wheel(0, 0, P["WHEEL_R"], 50, 2 * st)

    # 8 Drivetrain: BB shell and spindle, chainring, sprocket, chain runs, cranks, pedals
    bx, bz = P["BB_X"], P["BB_Z"]; cy = P["CHAINLINE"]
    r_ring = P["RING_T"] * 12.7 / (2 * math.pi); r_spr = P["SPROCKET_T"] * 12.7 / (2 * math.pi)
    dt = (Pos(bx, 0, bz) * Rot(90, 0, 0) * Cylinder(19, 68)
          + Pos(bx, 0, bz) * Rot(90, 0, 0) * Cylinder(8, 124)
          + Pos(bx, cy, bz) * Rot(90, 0, 0) * Cylinder(r_ring + 4, 3)
          + Pos(0, cy, P["WHEEL_R"]) * Rot(90, 0, 0) * Cylinder(r_spr + 4, 3)
          + rod((0, cy, P["WHEEL_R"] + r_spr), (bx, cy, bz + r_ring), 4)
          + rod((0, cy, P["WHEEL_R"] - r_spr), (bx, cy, bz - r_ring), 4))
    ca = math.radians(55)
    for s in (1, -1):
        tip = (bx + s * P["CRANK"] * math.cos(ca), s * 72, bz - s * P["CRANK"] * math.sin(ca))
        dt = dt + rod((bx, s * 72, bz), tip, 10) + Pos(tip[0], s * 110, tip[2]) * Box(90, 60, 20)
    parts[8] = dt

    # 9 Cargo box: 12 mm floor, 9 mm walls and lid (lid is the counter)
    x0 = P["BOX_X0"]; x1 = x0 + P["BOX_L"]; yb = P["BOX_W"] / 2; z0 = P["BOX_Z0"]; z1 = z0 + P["BOX_H"]
    w = P["PLY_WALL"]
    cb = box(x0, x1, -yb, yb, z0, z1) - box(x0 + w, x1 - w, -yb + w, yb - w, z0 + P["PLY_FLOOR"], z1 + 1)
    parts[9] = cb + box(x0, x1, -yb, yb, z1, z1 + w)

    # 10 Seat: seatpost on the 73 degree seat line and a sprung saddle
    zs = P["SADDLE_TOP"]
    parts[10] = rod((seat_xy(700), 0, 700), (seat_xy(zs - 40), 0, zs - 40), 13.6) + \
        Pos(seat_xy(zs - 25), 0, zs - 25) * Box(260, 160, 50)

    # 11 Handlebar on a stem bolted to the bulkhead (steers with the bed)
    parts[11] = (rod((1062, 0, 600), (1010, 0, 830), 14) + rod((1010, 0, 830), (930, 0, 850), 14)
                 + rod((930, -290, 850), (930, 290, 850), 11)
                 + rod((930, 290, 850), (885, 320, 850), 13) + rod((930, -290, 850), (885, -320, 850), 13))

    # 12 Brake levers, cables and parking latch
    parts[12] = (Pos(920, 250, 862) * Box(40, 30, 22) + Pos(920, -250, 862) * Box(40, 30, 22)
                 + Pos(920, 200, 862) * Box(30, 22, 30)
                 + rod((920, 250, 850), (kp, 20, 620), 3) + rod((kp, 20, 620), (880, 40, 560), 3)
                 + rod((880, 40, 560), (60, 64, 340), 3)
                 + rod((920, -250, 850), (1070, -310, 600), 3) + rod((1070, -310, 600), (P["WB"], -330, 330), 3)
                 + rod((P["WB"], -330, 330), (P["WB"], 330, 330), 3))
    return parts


NAMES = {1: "Spine plates and covers", 2: "Rear stay plates (pair)", 3: "Front bed plates",
         4: "Ribs, spacers and M8 bolts", 5: "Kingpin, headset and collars", 6: "Front wheels, drum brakes (2)",
         7: "Rear wheel, 3-speed drum hub", 8: "Drivetrain", 9: "Cargo box and lid, plywood",
         10: "Seat and seatpost", 11: "Handlebar and stem", 12: "Brake levers, cables, parking latch"}


def plate_schedule():
    """Group PLATES by name: qty, area each (m2), bounding size (mm). Call after build_parts()."""
    out = {}
    for p in PLATES:
        k = p["name"]
        if k not in out:
            out[k] = {"bom": p["bom"], "qty": 0, "area_m2": p["area_mm2"] / 1e6, "size": p["size"]}
        out[k]["qty"] += 1
    return out


if __name__ == "__main__":
    parts = build_parts()
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    frame = Compound(children=[parts[1], parts[2], parts[4], parts[5]])
    front = Compound(children=[parts[3]])
    asm = Compound(children=[parts[k] for k in sorted(parts)])
    for name, shp in (("flattrike-frame", frame), ("flattrike-front-bed", front), ("flattrike-assembly", asm)):
        export_step(shp, str(root / "step" / f"{name}.step"))
        export_stl(shp, str(root / "stl" / f"{name}.stl"))
    bb = asm.bounding_box()
    print(f"assembly bounding box: L {bb.size.X:.0f} x W {bb.size.Y:.0f} x H {bb.size.Z:.0f} mm")
    tot = 0.0
    for k, v in plate_schedule().items():
        tot += v["qty"] * v["area_m2"]
        print(f"  {k:26s} item {v['bom']}  x{v['qty']}  {v['area_m2']:.4f} m2 each  {v['size'][0]:.0f} x {v['size'][1]:.0f} mm")
    print(f"total plate area {tot:.3f} m2, mass {tot * T * 7.85:.1f} kg at 3 mm")
    print("wrote cad/step/*.step and cad/stl/*.stl")
