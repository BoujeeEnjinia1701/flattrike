"""FlatTrike parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the plate schedule
(flat area and bounding size of every cut plate) used by FTK-CAL-001.

Massing-plus level of detail: correct interfaces and main dimensions, not
fabrication detail. PRELIMINARY, NOT FOR FABRICATION.

Coordinates in mm. X forward, Y to the left, Z up, ground at Z = 0, rear axle at X = 0.
Layout (decided by Amish, 2026-09-25, FTK-DDR-001): tadpole front loader. Steering
(decided by Amish, 2026-09-25, FTK-DDR-002 item 13): Ackermann steering with a fixed
box. Each front wheel turns in a standard 20 in fork on its own headset (knuckle),
linked by a tie rod; the handlebar turns a central steering column whose drop arm
drives the left knuckle through a drag link. The bed is bolted rigidly to the spine.
Every steel part is flat 3 mm plate cut from DXF; nothing is welded or bent. TRL 3
changes from the TRL 2 massing model: closed-box spine, seat moved forward to a 73
degree seat angle, track 0.84 m; after DDR-002: fixed bed with knuckle posts, 200 mm
central head tube (item 19), box 820 x 560 x 360 mm with its floor at 470 mm so the
steered wheels pass under it.
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
    "HT_Z0": 310.0,           # central head tube bottom
    "HT_LEN": 200.0,          # central head tube length (150 mm before FTK-DDR-002 item 19)
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
    "FORK_OLD": 100.0,        # bought 20 in fork, front hub over locknuts
    "POST_Y0": 283.0,         # knuckle post inner face from the centre plane
    "POST_W": 45.0,           # knuckle post box width (inner to outer cheek)
    "POST_X": 45.0,           # knuckle post transverse plates at WB +/- this
    "KN_Z0": 555.0,           # knuckle head tube bottom (above the fork crown)
    "KN_LEN": 120.0,          # knuckle head tube length
    "ARM_L": 120.0,           # Ackermann steering arm, kingpin axis to tie rod joint
    "ARM_Z": 400.0,           # steering arm and tie rod height
    "DROP_Z": 255.0,          # drop arm under the lower yoke
    "BOX_X0": 1065.0,         # cargo box rear face
    "BOX_L": 820.0,
    "BOX_W": 560.0,
    "BOX_Z0": 470.0,          # box floor underside (top of bed rails), above the steered tyres
    "BOX_H": 360.0,
    "PLY_FLOOR": 12.0,
    "PLY_WALL": 9.0,
    "RAIL_Y": 240.0,          # bed rail outer face offset
    "STEER_LOCK": 40.0,       # Ackermann inner-wheel lock, degrees (box clearance limit)
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
                       "size": (max(us) - min(us), max(vs) - min(vs)),
                       "poly": [tuple(q) for q in poly], "holes": [[tuple(q) for q in h] for h in holes]})
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
    top0, top1 = (360.0, 800.0), (P["KP_X"] - 25, 520.0)
    return [top0, top1, (P["KP_X"] - 25, 305.0), (720.0, 457.0), (665.0, 215.0), (540.0, 215.0),
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

    # 3 Front bed, fixed to the spine: yokes, bulkhead, rails, twin axle beam and two knuckle posts
    tr = P["TRACK"] / 2
    ly_z = P["HT_Z0"] - 18; uy_z = P["HT_Z0"] + P["HT_LEN"] + 25
    steer_hole = circle_pts(kp, 0, 14)
    ry = P["RAIL_Y"]
    f, n = xy(ly_z)
    bed = plate("Lower yoke", 3, [(kp - 45, -45), (kp - 45, 45), (1060, ry), (1060, -ry)], f, n, [steer_hole])
    f, n = xy(uy_z)
    bed = bed + plate("Upper yoke", 3, [(kp - 45, -45), (kp - 45, 45), (1060, 200), (1060, -200)], f, n, [steer_hole])
    f, n = yz(1060)
    bed = bed + plate("Bulkhead", 3, [(-ry, ly_z), (ry, ly_z), (ry, 600), (-ry, 600)], f, n,
                      [[(-ry + 40, ly_z + 40), (ry - 40, ly_z + 40), (ry - 40, 560), (-ry + 40, 560)]])
    x_end = P["BOX_X0"] + P["BOX_L"]
    rz0 = P["BOX_Z0"] - 110
    rail = [(1060, ly_z), (1180, ly_z), (1240, rz0), (x_end, rz0), (x_end, P["BOX_Z0"]), (1060, P["BOX_Z0"])]
    rail_holes = [[(1100, ly_z + 22), (1175, ly_z + 22), (1215, rz0 + 15), (1215, P["BOX_Z0"] - 18), (1100, P["BOX_Z0"] - 18)]]
    rail_holes += [[(xh, rz0 + 18), (xh + w, rz0 + 18), (xh + w, P["BOX_Z0"] - 18), (xh, P["BOX_Z0"] - 18)]
                   for xh, w in ((1265, 115), (1520, 150), (1690, 165))]
    bed = bed + pair_xz("Bed rail", 3, rail, ry - T, holes=rail_holes)
    py0 = P["POST_Y0"]; py1 = py0 + P["POST_W"]; ab_top = P["BOX_Z0"]
    for xb in (P["WB"] - 33, P["WB"] + 30):
        f, n = yz(xb)
        ab_holes = [[(yh, 318), (yh + 115, 318), (yh + 115, 442), (yh, 442)] for yh in (-250, -122, 7, 135)]
        bed = bed + plate("Axle beam plate", 3, [(-py0, 290), (py0, 290), (py0, ab_top), (-py0, ab_top)], f, n,
                          ab_holes)
    # knuckle posts: per side a closed box column (two transverse plates, two cheek plates) that
    # carries a knuckle head tube above the tyre between two collar plates
    kz0, kz1 = P["KN_Z0"], P["KN_Z0"] + P["KN_LEN"]
    top = kz1 + 35; ymax = tr + 45
    post = [(py0, 290), (py1, 290), (py1, 530), (ymax, 530), (ymax, top), (py0, top)]
    post_win = [(py1 + 20, 548), (ymax - 30, 548), (ymax - 30, top - 18), (py1 + 20, top - 18)]
    for s in (1, -1):
        for xc in (P["WB"] - P["POST_X"] - T, P["WB"] + P["POST_X"]):
            pr = [(s * u, v) for u, v in post] if s > 0 else [(-u, v) for u, v in reversed(post)]
            pw = [(s * u, v) for u, v in post_win] if s > 0 else [(-u, v) for u, v in reversed(post_win)]
            f, n = yz(xc)
            bed = bed + plate("Knuckle post plate", 3, pr, f, n, [pw])
        for yc, ztop, nm in ((py0, top, "Knuckle post inner cheek"), (py1 - T, 530, "Knuckle post outer cheek")):
            y0 = yc if s > 0 else -yc - T
            f, n = xz(y0)
            bed = bed + plate(nm, 3, [(P["WB"] - P["POST_X"], 290), (P["WB"] + P["POST_X"], 290),
                                                        (P["WB"] + P["POST_X"], ztop), (P["WB"] - P["POST_X"], ztop)],
                              f, n, [[(P["WB"] - 25, 320), (P["WB"] + 25, 320), (P["WB"] + 25, ztop - 40),
                                      (P["WB"] - 25, ztop - 40)]])
        for zc in (kz0 + 12, kz1 - 12 - T):
            f, n = xy(zc)
            cp = [(P["WB"] - P["POST_X"], s * py1), (P["WB"] + P["POST_X"], s * py1),
                  (P["WB"] + P["POST_X"], s * ymax), (P["WB"] - P["POST_X"], s * ymax)]
            bed = bed + plate("Knuckle collar plate", 3, cp, f, n, [circle_pts(P["WB"], s * tr, P["HT_OD"] / 2 + 0.5)])
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

    # 5 Steering: central head tube and steering column (clamped by two collar plates; the yokes bolt to
    # the collars, so the bed is fixed), drop arm, drag link, two knuckle head tubes with bought 20 in forks,
    # Ackermann steering arms and tie rod
    hz = P["HT_Z0"]; hl = P["HT_LEN"]
    king = Pos(kp, 0, hz + hl / 2) * (Cylinder(P["HT_OD"] / 2, hl) - Cylinder(17, hl + 2))
    king = king + rod((kp, 0, P["DROP_Z"] - 5), (kp, 0, 830), 12)
    for zc in (hz + 20, hz + hl - 23):
        f, n = xy(zc)
        king = king + plate("Head tube collar plate", 5, [(kp - 75, -si - T - 6), (kp + 30, -si - T - 6),
                                                          (kp + 30, si + T + 6), (kp - 75, si + T + 6)],
                            f, n, [circle_pts(kp, 0, P["HT_OD"] / 2 + 0.5)])
    f, n = xy(P["DROP_Z"])
    king = king + plate("Drop arm", 5, [(kp - 22, -22), (kp + 22, -22), (kp + 15, 85), (kp - 15, 85)], f, n,
                        [circle_pts(kp, 0, 12.5)])
    # Ackermann arms point from each kingpin axis at the rear axle centre
    d = math.hypot(P["WB"], tr)
    tip = lambda s: (P["WB"] - P["ARM_L"] * P["WB"] / d, s * (tr - P["ARM_L"] * tr / d))
    king = king + rod((kp, 70, P["DROP_Z"] + 1.5), (*tip(1), P["ARM_Z"]), 5)
    king = king + rod((tip(1)[0], tip(1)[1], P["ARM_Z"]), (tip(-1)[0], tip(-1)[1], P["ARM_Z"]), 6)
    ho = P["FORK_OLD"] / 2
    for s in (1, -1):
        cy = s * tr
        king = king + Pos(P["WB"], cy, (kz0 + kz1) / 2) * (Cylinder(P["HT_OD"] / 2, P["KN_LEN"]) - Cylinder(17, P["KN_LEN"] + 2))
        king = king + rod((P["WB"], cy, 520), (P["WB"], cy, kz1 + 30), 12)
        king = king + Pos(P["WB"], cy, 530) * Box(40, P["FORK_OLD"] + 30, 26)
        for sy in (1, -1):
            king = king + rod((P["WB"], cy + sy * (ho + 5), 520), (P["WB"], cy + sy * (ho + 5), P["WHEEL_R"]), 9)
        tx, ty = tip(s)
        leg_y = cy - s * (ho + 5)
        f, n = xy(P["ARM_Z"] - T / 2)
        arm = [(P["WB"] + 10, leg_y - 11), (P["WB"] + 10, leg_y + 11), (tx - 10, ty + 11), (tx - 10, ty - 11)]
        arm = arm if s > 0 else list(reversed(arm))
        king = king + plate("Steering arm", 5, arm, f, n)
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

    # 11 Handlebar and stem on the central steering column
    parts[11] = (rod((kp, 0, 830), (930, 0, 850), 14)
                 + rod((930, -290, 850), (930, 290, 850), 11)
                 + rod((930, 290, 850), (885, 320, 850), 13) + rod((930, -290, 850), (885, -320, 850), 13))

    # 12 Brake levers, cables and parking latch
    parts[12] = (Pos(920, 250, 862) * Box(40, 30, 22) + Pos(920, -250, 862) * Box(40, 30, 22)
                 + Pos(920, 200, 862) * Box(30, 22, 30)
                 + rod((920, 250, 850), (900, 60, 640), 3) + rod((900, 60, 640), (880, 40, 560), 3)
                 + rod((880, 40, 560), (60, 64, 340), 3)
                 + rod((920, -250, 850), (1040, -180, 600), 3) + rod((1040, -180, 600), (1040, -180, 270), 3)
                 + rod((1040, -180, 270), (P["WB"] - 60, -180, 270), 3)
                 + rod((P["WB"] - 60, -tr + 50, 270), (P["WB"] - 60, tr - 50, 270), 3))
    return parts


NAMES = {1: "Spine plates and covers", 2: "Rear stay plates (pair)", 3: "Front bed plates",
         4: "Ribs, spacers and M8 bolts", 5: "Steering column, knuckles and linkage", 6: "Front wheels, drum brakes (2)",
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
