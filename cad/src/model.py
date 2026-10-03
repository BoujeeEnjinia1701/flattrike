"""FlatTrike parametric model (build123d), TRL 3, constructable design (FTK-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL into cad/step and cad/stl and prints the plate schedule
    python cad/src/model.py --check    runs the constructability checks (joints, overlaps, contacts, steering sweep)

Every physical piece is its own solid in build_components(): each cut plate (left and right
separately), each bought part and each bolt set. build_parts() fuses them by BOM line for the
calculations, the concept media and the general arrangement. The build plan pictures
(cad/src/build_plan_media.py) draw from build_components(), so pictures and model agree.

Coordinates in mm. X forward, Y to the left (as the rider sits), Z up, ground at Z = 0, rear axle at X = 0.
Layout (decided by Amish, 2026-09-25, FTK-DDR-001): tadpole front loader. Steering (FTK-DDR-002 item 13):
Ackermann steering with a fixed box. Every steel frame part is a flat 3 mm plate cut from DXF; nothing
is welded or bent.

How the pieces join (FTK-DDR-003, design for construction):
  * Tee joints: tabs on the edge of one plate sit in slots cut in the other and carry the load; between
    tabs an M8 bolt passes through the face plate into a T-slot in the edge plate, where an all-metal
    locknut sits in a window and cannot turn. Where the edge plate meets the face plate at its edge (the
    spine covers, the knuckle post corners) the slot is an open notch: a finger joint.
  * Parallel plates (stays outside the spine): through-bolts with stacks of cut spacer washers outside
    the spine and a cut steel spacer tube inside it.
  * Rails and axle beams cross in halving joints (slot from below in the rail, from above in the beam).
  * Head tubes and the bottom bracket shell are clamped between two plates by their own pressed or
    threaded cups: each cup's spigot passes through a hole in the plate and its flange holds the plate
    against the end of the tube or shell.
  * Steering arms clamp to the inboard fork leg with two U-bolts through a clamp plate; the drop arm
    is a plate slid over the two leg stubs of a cut-down steering fork, held by shaft collars.
PRELIMINARY, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
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
    "KP_X": 1000.0,           # central steering axis, ahead of the rear axle
    "HT_Z0": 310.0,           # central head tube bottom (top face of the lower yoke)
    "HT_LEN": 200.0,          # central head tube length = gap between the yokes (FTK-DDR-002 item 19)
    "HT_OD": 40.0,            # head tube outside diameter, 1 1/8 in threaded headset
    "CUP_HOLE_R": 17.25,      # plate hole for a headset cup spigot (34 mm press fit)
    "SPINE_IN": 30.0,         # inner face of each spine side plate from the centre plane
    "STAY_IN": 60.0,          # inner face of each rear stay plate (120 mm hub OLD)
    "BB_X": 600.0,            # bottom bracket centre
    "BB_Z": 265.0,
    "BB_HOLE_R": 17.75,       # spine hole for the bottom bracket cup spigots (BSA 1.37 in thread)
    "SEAT_ANGLE": 73.0,       # seat tube angle, degrees from horizontal
    "SADDLE_TOP": 930.0,      # saddle top height
    "SEAT_TUBE_R": 15.9,      # bought seat tube, 31.8 x 2.3 mm (27.2 mm seatpost)
    "SADDLE_Z": (600.0, 700.0),   # seat line heights of the lower and upper seat tube saddles
    "CHAINLINE": -44.0,       # chain plane, right-hand drive (negative Y is the rider's right)
    "RING_T": 32,             # chainring teeth
    "SPROCKET_T": 24,         # rear sprocket teeth
    "CRANK": 170.0,
    "FORK_OLD": 100.0,        # bought 20 in fork, front hub over locknuts
    "LEG_R": 11.0,            # fork leg radius
    "LEG_Y": 61.0,            # fork leg centre from the wheel centre plane
    "POST_Y0": 283.0,         # knuckle post inner face from the centre plane
    "POST_W": 45.0,           # knuckle post box width (inner to outer cheek)
    "POST_X": 25.0,           # knuckle post transverse plates' inner faces at WB +/- this
    "KN_Z0": 555.0,           # knuckle head tube bottom (top face of the lower collar plate)
    "KN_LEN": 120.0,          # knuckle head tube length = gap between the collar plates
    "ARM_L": 120.0,           # Ackermann steering arm, kingpin axis to tie rod joint
    "ARM_Z": 321.0,           # steering arm plate underside, below the knuckle post column
    "CLAMP_Z": (303.0, 343.0),    # steering arm clamp plate, bottom and top
    "UBOLT_Z": (310.0, 336.0),    # U-bolts round the inboard fork leg
    "AB_Z0": 350.0,           # bottom of the axle beams and knuckle post columns (steering arms pass beneath)
    "COVER_HW": 45.0,         # half width of the spine covers and the lower yoke tongue (12 mm past the side plates)
    "DROP_Z": 264.0,          # drop arm plate underside (it is bolted under the steering fork crown)
    "CROWN_BOLT_R": 32.0,     # drop arm bolts through the crown, either side of the steering axis
    # drop arm: same length and direction as the left steering arm, so the column, drop arm, drag link and
    # left steering arm form a parallelogram and the left wheel turns with the handlebar (FTK-DDR-003)
    "BOX_X0": 1072.0,         # cargo box rear face, 9 mm (three spacer washers) in front of the bulkhead
    "BOX_L": 820.0,
    "BOX_W": 560.0,
    "BOX_Z0": 470.0,          # box floor underside (top of bed rails), above the steered tyres
    "BOX_H": 360.0,
    "PLY_FLOOR": 12.0,
    "PLY_WALL": 9.0,
    "RAIL_Y": 240.0,          # bed rail outer face offset
    "RAIL_X0": 1040.0,        # bed rail rear end
    "BULK_X": 1060.0,         # bulkhead rear face
    "BULK_Z0": 298.0,         # bulkhead bottom edge
    "AB_X": (1436.0, 1461.0), # axle beam plates (rear faces)
    "STEER_LOCK": 40.0,       # Ackermann inner-wheel lock, degrees (box clearance limit)
    # steering lock stops (decided by Amish 2026-10-02, FTK-DEC-001): a stop under each knuckle post that the
    # steering arm clamp plate meets at the inner-wheel lock
    "CLAMP_IN": 130.0,        # clamp plate inboard end from the kingpin axis (was 85 mm); its front corner meets the stop
    "STOP_Z": (300.0, 348.0, 430.0),   # stop fin: bottom, underside of its upper part, top
    "STOP_LEG": 30.0,         # width of the stop fin's lower leg, ahead of the contact face
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


def tube(a, b, r, ri):
    return rod(a, b, r) - rod(a, b, ri)


def obox(c, u, n, lu, lv, ln):
    """Box centred at c with edges along u (lu), n (ln) and n x u (lv)."""
    return Plane(origin=Vector(*c), x_dir=Vector(*u), z_dir=Vector(*n)) * Box(lu, lv, ln)


def circle_pts(cx, cy, r, n=24):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def poly_area(pts):
    a = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


def v_add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def v_mul(v, k):
    return tuple(c * k for c in v)


PLATES = []   # plate schedule: dicts with name, bom, area_mm2, size (w, h), poly, holes


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


def mirror_poly(poly):
    """Mirror a (u, v) profile in u (left to right side) and keep it counter-clockwise."""
    return [(-u, v) for u, v in reversed(poly)]


def edge_strip(name, bom, p0, p1, half_w, outward, t=T, record=True):
    """Cover plate lying on a straight edge p0 -> p1 of the side profile (XZ), spanning +/- half_w in Y."""
    (x0, z0), (x1, z1) = p0, p1
    L = math.hypot(x1 - x0, z1 - z0); ex, ez = (x1 - x0) / L, (z1 - z0) / L
    nx, nz = (-ez, ex) if outward == "left" else (ez, -ex)
    to3d = lambda u, v: (x0 + ex * u, v, z0 + ez * u)  # noqa: E731
    return plate(name, bom, [(0, -half_w), (L, -half_w), (L, half_w), (0, half_w)], to3d, (nx, 0, nz), t=t,
                 record=record)


def wheel(cx, cy, cz, hub_r, hub_len, tyre_only=False):
    R = P["WHEEL_R"]; tw = P["TYRE_W"]
    tyre = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(R, tw) - Cylinder(R - 42, tw + 2))
    if tyre_only:
        return tyre
    rim = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(R - 45, 20) - Cylinder(R - 57, 22))
    hub = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(hub_r, hub_len)
    axle = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(4.75, hub_len + 40)
    s = tyre + rim + hub + axle
    for k in range(12):
        a = math.radians(k * 30 + 15)
        s = s + rod((cx, cy, cz), (cx + (R - 55) * math.cos(a), cy, cz + (R - 55) * math.sin(a)), 2.0)
    return s


# ---------------- profiles ----------------
def spine_profile():
    """Side profile of the spine box beam: seat node to head tube, with a drop lobe to the bottom bracket.
    The short level edge at 310 mm under the head tube carries the lower yoke."""
    return [(360.0, 800.0), (P["KP_X"] - 25, 520.0), (P["KP_X"] - 25, P["HT_Z0"]), (900.0, P["HT_Z0"]),
            (720.0, 457.0), (665.0, 215.0), (540.0, 215.0), (520.0, 555.0), (294.0, 665.0)]


SPINE = spine_profile()
SPINE_WIN = [(565, 320), (660, 320), (690, 440), (565, 500)]
SPINE_HOLES = [[(355, 703), (425, 670), (425, 720), (380, 742)]]   # rear lightening window, clear of the seat tube
STAY = [(-45, 215), (45, 205), (700, 520), (690, 610), (440, 760), (350, 745), (-45, 300)]
STAY_WIN = [(140, 320), (540, 495), (430, 640), (320, 560)]
STAY_SLOT = [(-45, 249.0), (8.0, 249.0), (8.0, 259.0), (-45, 259.0)]   # open dropout slot, 10 mm, axle at x = 0
# spine cover joints, along the edge from its rear end (mm): in the closed box (the top cover from 395 mm,
# the whole bottom cover) the tabs are close together because they carry the torsion shear flow
ST_TOP = [("tab", 25), ("bolt", 48), ("tab", 150), ("bolt", 200), ("tab", 270), ("bolt", 330), ("tab", 378),
          ("tab", 400), ("tab", 422), ("tab", 444), ("bolt", 472), ("tab", 500), ("tab", 522), ("tab", 544),
          ("bolt", 572), ("tab", 600), ("tab", 622), ("tab", 644), ("tab", 664)]
ST_BOT = [("tab", 12), ("tab", 34), ("bolt", 70), ("tab", 100), ("tab", 122), ("tab", 144), ("bolt", 172),
          ("tab", 198)]
NODES = [(335.0, 697.0), (545.0, 650.0), (620.0, 560.0), (680.0, 540.0)]   # stay-to-spine through-bolts


def stay_profile():
    """STAY with the open dropout slot let into its rear edge."""
    pts = list(STAY)
    i = pts.index((-45, 300)) + 1
    return pts[:i] + [(-45, 259.0), (8.0, 259.0), (8.0, 249.0), (-45, 249.0)] + pts[i:]


def seat_xy(z):
    """Point on the seat tube line through the bottom bracket at height z."""
    return P["BB_X"] - (z - P["BB_Z"]) / math.tan(math.radians(P["SEAT_ANGLE"]))


def seat_axes():
    a = math.radians(P["SEAT_ANGLE"])
    t = (-math.cos(a), 0.0, math.sin(a))      # up the seat tube
    w = (math.sin(a), 0.0, math.cos(a))       # across it, in the side view
    return t, w


def drop_pin():
    """Drag link joint on the drop arm: the left steering arm's vector placed on the column axis."""
    tx, ty = ackermann_tip(1)
    return (P["KP_X"] + tx - P["WB"], ty - P["TRACK"] / 2)


def stop_corner(s):
    """Where the clamp plate's front inboard corner is (x, y) when wheel s (+1 left, -1 right) is at the
    inner-wheel lock (left +STEER_LOCK, right -STEER_LOCK). The stop fin's rear face is placed there."""
    wb, tr = P["WB"], P["TRACK"] / 2
    a = s * math.radians(P["STEER_LOCK"])
    qx, qy = -P["LEG_R"], -s * P["CLAMP_IN"]          # clamp plate front face is LEG_R behind the kingpin axis
    return (wb + qx * math.cos(a) - qy * math.sin(a), s * tr + qx * math.sin(a) + qy * math.cos(a))


def ackermann_tip(s):
    """Steering arm joint for side s (+1 left, -1 right), on the line from the kingpin to the rear axle centre."""
    wb, tr = P["WB"], P["TRACK"] / 2
    d = math.hypot(wb, tr)
    return (wb - P["ARM_L"] * wb / d, s * (tr - P["ARM_L"] * tr / d))


# ---------------- components ----------------
@dataclass
class Comp:
    shape: object
    bom: int
    kind: str            # plate, bought, hardware, wood
    group: str           # pieces in one group may overlap (a bought assembly); others must not
    note: str = ""
    moving: str = ""     # "L" or "R" for the steered front wheel groups, "C" for the steering column


C = {}
JOINTS = []              # one dict per joint: group, kind, face, edge, tabs, bolts
ISSUES = []              # problems found while building (tab or slot not on solid plate)
BOLT_GROUPS = {}         # bolt sets by joint group, for the calculations


def add(name, shape, bom, kind, group=None, note="", moving=""):
    C[name] = Comp(shape, bom, kind, group or name, note, moving)
    return C[name]


def _cut(name, tool):
    C[name].shape = C[name].shape - tool


def _fuse(name, tool):
    C[name].shape = C[name].shape + tool


def _fill(name, region, label):
    """Fraction of a check region (exactly one plate thick) that is solid plate. Logs an issue if < 0.98."""
    try:
        got = (C[name].shape & region).volume
    except Exception:
        got = 0.0
    frac = got / region.volume
    if frac < 0.98:
        ISSUES.append(f"{label}: only {frac * 100:.0f} % solid plate around it on {name}")
    return frac


_bolt_n = [0]


def bolt_set(group, head_at, axis, grip, length=None, nut_depth=None, washer=True, bom=4, moving=""):
    """M8 bolt, washer and all-metal locknut. head_at: point on the face the head bears on; axis: unit vector
    into the joint. grip: distance from that face to the nut's near face (a T-slot nut) or to the far face of
    the joint (a through-bolt). Returns the bolt set solid."""
    ax = Vector(*axis).normalized(); h = Vector(*head_at)
    L = length or (grip + 11)
    s = Solid.make_cylinder(4.0, L, Plane(origin=h, z_dir=ax))
    wsh = 1.6 if washer else 0.0
    if washer:
        s = s + Solid.make_cylinder(8.0, 1.6, Plane(origin=h - ax * 1.6, z_dir=ax))
    s = s + Solid.make_cylinder(6.5, 5.3, Plane(origin=h - ax * (wsh + 5.3), z_dir=ax))
    nd = grip if nut_depth is None else nut_depth
    if nut_depth is None:     # through-bolt: washer and nut beyond the far face
        s = s + Solid.make_cylinder(8.0, 1.6, Plane(origin=h + ax * grip, z_dir=ax))
        s = s + Solid.make_cylinder(7.3, 8.0, Plane(origin=h + ax * (grip + 1.6), z_dir=ax))
    _bolt_n[0] += 1
    BOLT_GROUPS[group] = BOLT_GROUPS.get(group, 0) + 1
    return s


def tee(group, face, edge, p0, u, nf, te, stations, tf=T, te_t=T, finger=False, tab_len=16.0, depth=23.0,
        bom=4, head_group=None):
    """Tee joint between a face plate and an edge plate meeting it.
    p0: point on the face plate's contact surface, at the mid-thickness of the edge plate.
    u: unit vector along the joint line; nf: unit vector from the face plate into the edge plate;
    te: the edge plate's thickness direction. stations: list of ("tab" | "bolt", s), s along u from p0.
    Tabs on the edge plate sit in slots in the face plate (an open notch when finger=True). Each bolt passes
    through the face plate into a T-slot in the edge plate, where its locknut sits in a window."""
    u = Vector(*u).normalized(); nf = Vector(*nf).normalized(); te = Vector(*te).normalized()
    p0 = Vector(*p0)
    nb = 0; ntab = 0
    hw = []
    for kind, s in stations:
        p = p0 + u * s
        if kind == "tab":
            c = p - nf * (tf / 2)
            tab = obox(c, u, nf, tab_len, te_t, tf)
            slot = obox(c, u, nf, tab_len + 0.4, te_t + 0.4, tf + 2)
            # checks: the tab root is on solid edge plate; the slot is in solid face plate
            _fill(edge, obox(p + nf * 4, u, nf, tab_len, te_t, 6), f"{group}: tab root at s={s:.0f}")
            if not finger:
                _fill(face, obox(c, u, nf, tab_len + 10, te_t + 10, tf), f"{group}: slot at s={s:.0f}")
            _cut(face, slot)
            _fuse(edge, tab)
            ntab += 1
        else:
            _fill(face, obox(p - nf * (tf / 2), u, nf, 19, 19, tf), f"{group}: bolt hole at s={s:.0f}")
            _fill(edge, obox(p + nf * (depth + 4) / 2, u, nf, 23.6, te_t, depth + 4), f"{group}: T-slot at s={s:.0f}")
            _cut(face, Solid.make_cylinder(4.5, tf + 2, Plane(origin=p - nf * (tf + 1), z_dir=nf)))
            _cut(edge, obox(p + nf * (depth / 2), u, nf, 9.0, te_t + 2, depth))
            _cut(edge, obox(p + nf * 14.2, u, nf, 13.6, te_t + 2, 8.4))
            b = bolt_set(group, p - nf * tf, nf, tf + 10, length=tf + depth - 1, nut_depth=tf + 10, bom=bom)
            nut = obox(p + nf * 14.2, u, nf, 13.0, 13.0, 8.0)
            hw.append(b + nut)
            nb += 1
    JOINTS.append({"group": group, "kind": "finger" if finger else "tee", "face": face, "edge": edge,
                   "tabs": ntab, "bolts": nb})
    for k, h in enumerate(hw):
        nb_ = sum(1 for n in C if n.startswith(f"Bolt: {group} ")) + 1
        add(f"Bolt: {group} {nb_}", h, bom, "hardware", group=head_group or f"bolt-{group}-{nb_}")
    return nb


def through_bolt(group, name, a, axis, grip, cut=(), bom=4):
    """Bolt from a (head side face) along axis through grip mm of parts; holes cut in the named parts."""
    ax = Vector(*axis).normalized(); av = Vector(*a)
    for n in cut:
        _fill(n, _hole_region(n, av, ax, grip), f"{group}: bolt hole")
        _cut(n, Solid.make_cylinder(4.5, grip + 2, Plane(origin=av - ax * 1, z_dir=ax)))
    b = bolt_set(group, a, axis, grip, length=grip + 12, bom=bom)
    add(name, b, bom, "hardware")
    JOINTS.append({"group": group, "kind": "through", "face": ",".join(cut), "edge": "", "tabs": 0, "bolts": 1})


def _hole_region(name, av, ax, grip):
    """A 19 mm square, one plate thick, around where a bolt crosses a plate (for the solid-plate check)."""
    bb = C[name].shape.bounding_box()
    # find where the axis enters the plate: sample along the axis
    best = None
    for k in range(int(grip) + 1):
        q = av + ax * (k + 0.5)
        if bb.min.X - 1 <= q.X <= bb.max.X + 1 and bb.min.Y - 1 <= q.Y <= bb.max.Y + 1 and bb.min.Z - 1 <= q.Z <= bb.max.Z + 1:
            best = q; break
    best = best or av
    return obox(best, _perp(ax), ax, 19, 19, 2.0)


def _perp(v):
    a = Vector(1, 0, 0) if abs(v.X) < 0.9 else Vector(0, 1, 0)
    return v.cross(a).normalized()


def build_components():
    """Every physical piece of the prototype as its own solid, named; see the module docstring."""
    C.clear(); JOINTS.clear(); ISSUES.clear(); BOLT_GROUPS.clear(); PLATES.clear(); _bolt_n[0] = 0
    si = P["SPINE_IN"]; st = P["STAY_IN"]; kp = P["KP_X"]; wb = P["WB"]; tr = P["TRACK"] / 2
    hz0, hl = P["HT_Z0"], P["HT_LEN"]
    sides = (("left", 1), ("right", -1))

    # ---------------------------------------------------------------- 1 spine
    bb_hole = circle_pts(P["BB_X"], P["BB_Z"], P["BB_HOLE_R"])
    for nm, s in sides:
        y0 = si if s > 0 else -si - T
        f, n = xz(y0)
        add(f"Spine side plate, {nm}", plate("Spine side plate", 1, SPINE, f, n, holes=[SPINE_WIN, bb_hole] + SPINE_HOLES),
            1, "plate")
    chw = P["COVER_HW"]
    add("Spine top cover", edge_strip("Spine top cover", 1, SPINE[0], SPINE[1], chw, "left"), 1, "plate")
    (ax0, az0), (ax1, az1) = SPINE[4], SPINE[3]
    Lb = math.hypot(ax1 - ax0, az1 - az0); db = ((ax1 - ax0) / Lb, (az1 - az0) / Lb)
    bc0 = (ax0 + db[0] * 6, az0 + db[1] * 6); bc1 = (ax1 - db[0] * 6, az1 - db[1] * 6)
    add("Spine bottom cover", edge_strip("Spine bottom cover", 1, bc0, bc1, chw, "right"), 1, "plate")

    # ---------------------------------------------------------------- 3 bed: yokes (in the spine), bulkhead, rails
    cr = P["CUP_HOLE_R"]
    f, n = xy(hz0 - T)
    ly = [(900, -chw), (985, -chw), (1010, -60), (1040, -237), (P["BULK_X"], -237), (P["BULK_X"], 237), (1040, 237), (1010, 60),
          (985, chw), (900, chw)]
    add("Lower yoke", plate("Lower yoke", 3, ly, f, n, [circle_pts(kp, 0, cr)]), 3, "plate")
    f, n = xy(hz0 + hl)
    uy = [(910, -si), (kp - 25, -si), (985, -60), (P["BULK_X"], -200), (P["BULK_X"], 200), (985, 60),
          (kp - 25, si), (910, si)]
    add("Upper yoke", plate("Upper yoke", 3, uy, f, n, [circle_pts(kp, 0, cr)]), 3, "plate")
    bz0 = P["BULK_Z0"]; ry = P["RAIL_Y"]; ri = ry - T
    f, n = yz(P["BULK_X"])
    add("Bulkhead", plate("Bulkhead", 3, [(-ri, bz0), (ri, bz0), (ri, 600), (-ri, 600)], f, n,
                          [[(-200, 338), (200, 338), (200, 490), (-200, 490)],
                           [(-200, 533), (200, 533), (200, 575), (-200, 575)]]), 3, "plate")
    x_end = P["BOX_X0"] + P["BOX_L"]
    rz0 = P["BOX_Z0"] - 110; bz = P["BOX_Z0"]; rx0 = P["RAIL_X0"]
    rail = [(rx0, 310), (1110, 310), (1150, rz0), (x_end, rz0), (x_end, bz), (rx0, bz)]
    rail_holes = [[(1125, rz0 + 18), (1215, rz0 + 18), (1215, bz - 18), (1125, bz - 18)]]
    rail_holes += [[(xh, rz0 + 18), (xh + w, rz0 + 18), (xh + w, bz - 18), (xh, bz - 18)]
                   for xh, w in ((1265, 115), (1520, 150), (1690, 145))]
    for nm, s in sides:
        y0 = ri if s > 0 else -ry
        f, n = xz(y0)
        add(f"Bed rail, {nm}", plate("Bed rail", 3, rail, f, n, rail_holes), 3, "plate")

    # axle beams: twin plates, windows clear of the rail crossings
    ab_holes = []
    az0 = P["AB_Z0"]
    for a, b in ((6, 106), (118, 213)):
        ab_holes += [[(a, az0 + 22), (b, az0 + 22), (b, bz - 22), (a, bz - 22)],
                     [(-b, az0 + 22), (-a, az0 + 22), (-a, bz - 22), (-b, bz - 22)]]
    py0 = P["POST_Y0"]; py1 = py0 + P["POST_W"]
    for k, xb in enumerate(P["AB_X"]):
        f, n = yz(xb)
        add(f"Axle beam plate, {'rear' if k == 0 else 'front'}",
            plate("Axle beam plate", 3, [(-py0, az0), (py0, az0), (py0, bz), (-py0, bz)], f, n, ab_holes), 3, "plate")

    # knuckle posts: two transverse plates between an inner cheek (which they tab into) and an outer
    # cheek (which tabs into them), and two collar plates that clamp the knuckle head tube
    px = P["POST_X"]; kz0, kz1 = P["KN_Z0"], P["KN_Z0"] + P["KN_LEN"]
    step_y = py1 + 10; ymax = 470.0
    tprof = [(py0 + T, az0), (step_y, az0), (step_y, kz0), (ymax, kz0), (ymax, kz1), (py0 + T, kz1)]
    for nm, s in sides:
        pr = tprof if s > 0 else mirror_poly(tprof)
        for xc, lab in ((wb - px - T, "rear"), (wb + px, "front")):
            f, n = yz(xc)
            add(f"Knuckle post plate, {nm} {lab}", plate("Knuckle post plate", 3, pr, f, n), 3, "plate")
        for yc, x_a, x_b, ztop, lab in ((py0, wb - px - 13, wb + px + 13, kz1, "inner"), (py1 - T, wb - px, wb + px, kz0 - 10, "outer")):
            y0 = yc if s > 0 else -yc - T
            f, n = xz(y0)
            add(f"Knuckle post {lab} cheek, {nm}",
                plate(f"Knuckle post {lab} cheek", 3, [(x_a, az0), (x_b, az0), (x_b, ztop), (x_a, ztop)], f, n),
                3, "plate")
        cp = [(wb - px - 13, step_y), (wb + px + 13, step_y), (wb + px + 13, ymax + 10), (wb - px - 13, ymax + 10)]
        cp = cp if s > 0 else [(u, -v) for u, v in reversed(cp)]
        for zc, lab in ((kz0 - T, "lower"), (kz1, "upper")):
            f, n = xy(zc)
            add(f"Knuckle collar plate, {nm} {lab}", plate("Knuckle collar plate", 3, cp, f, n,
                                                          [circle_pts(wb, s * tr, cr)]), 3, "plate")

    # ---------------------------------------------------------------- 4 ribs, stay bridge, seat saddles
    def edge_z(x, top):
        if top:
            (x0, z0), (x1, z1) = SPINE[0], SPINE[1]
        elif x >= SPINE[3][0]:
            return P["HT_Z0"]
        else:
            (x0, z0), (x1, z1) = SPINE[4], SPINE[3]
        return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    RIBS = {}
    for xr in (800.0, 900.0):
        zb = max(edge_z(xr, False), edge_z(xr + T, False)) + 5
        zt = min(edge_z(xr, True), edge_z(xr + T, True)) - 5
        f, n = yz(xr)
        add(f"Spine rib at {xr:.0f}", plate("Spine rib", 4, [(-si, zb), (si, zb), (si, zt), (-si, zt)], f, n), 4, "plate")
        RIBS[xr] = (zb, zt)
    f, n = yz(200)
    add("Stay bridge", plate("Stay bridge", 4, [(-st, 480), (st, 480), (st, 560), (-st, 560)], f, n), 4, "plate")
    tdir, wdir = seat_axes()
    SADDLES = {}
    for zc, lab in zip(P["SADDLE_Z"], ("lower", "upper")):
        c0 = (seat_xy(zc), 0.0, zc)
        to3d = (lambda c: (lambda uu, vv: v_add(c, v_mul(wdir, uu), (0, vv, 0))))(c0)
        add(f"Seat tube saddle, {lab}", plate("Seat tube saddle", 4, [(-46, -si), (46, -si), (46, si), (-46, si)], to3d, tdir,
                                              [circle_pts(0, 0, P["SEAT_TUBE_R"] + 0.5)]), 4, "plate")
        SADDLES[lab] = c0

    # ---------------------------------------------------------------- 2 stays
    for nm, s in sides:
        y0 = st if s > 0 else -st - T
        f, n = xz(y0)
        add(f"Rear stay plate, {nm}", plate("Rear stay plate", 2, stay_profile(), f, n, holes=[STAY_WIN]), 2, "plate")

    # ---------------------------------------------------------------- 5 steering: plates
    tipL = ackermann_tip(1)
    lr, ly_ = P["LEG_R"], P["LEG_Y"]
    for nm, s in sides:
        leg_y = s * (tr - ly_)
        xc = wb - lr - T          # clamp plate rear face; its front face touches the leg
        cz0, cz1 = P["CLAMP_Z"]
        y_in, y_out = s * (tr - P["CLAMP_IN"]), leg_y + s * 24      # inboard end reaches the lock stop
        cpl = [(min(y_in, y_out), cz0), (max(y_in, y_out), cz0), (max(y_in, y_out), cz1), (min(y_in, y_out), cz1)]
        f, n = yz(xc)
        add(f"Steering arm clamp plate, {nm}", plate("Steering arm clamp plate", 5, cpl, f, n), 5, "plate",
            group=f"wheel-{nm}", moving=nm[0].upper())
        tx, ty = ackermann_tip(s)
        a1, a2 = leg_y - s * 22, leg_y + s * 22
        arm = [(xc, a1), (xc, a2), (tx - 10, ty + s * 12), (tx - 10, ty - s * 12)]
        arm = arm if s < 0 else list(reversed(arm))
        f, n = xy(P["ARM_Z"])
        add(f"Steering arm, {nm}", plate("Steering arm", 5, arm, f, n, [circle_pts(tx, ty, 4.1, 24)]), 5, "plate",
            group=f"wheel-{nm}", moving=nm[0].upper())
    f, n = xy(P["DROP_Z"])
    dz = P["DROP_Z"]
    pxd, pyd = drop_pin()
    ua = ((pxd - kp) / P["ARM_L"], pyd / P["ARM_L"]); va = (-ua[1], ua[0])
    loc = lambda a, b: (kp + ua[0] * a + va[0] * b, ua[1] * a + va[1] * b)  # noqa: E731
    drop = [loc(-50, -20), loc(50, -20), loc(P["ARM_L"] + 13, -13), loc(P["ARM_L"] + 13, 13), loc(50, 20), loc(-50, 20)]
    cb = P["CROWN_BOLT_R"]
    add("Drop arm", plate("Drop arm", 5, drop, f, n, [circle_pts(*loc(cb, 0), 4.5, 12), circle_pts(*loc(-cb, 0), 4.5, 12),
                                                       circle_pts(pxd, pyd, 4.1, 24)]), 5, "plate",
        group="column", moving="C")

    # ---------------------------------------------------------------- joints in the frame
    # spine covers (finger joints: the side plates' top and bottom edges fill notches in the cover edges)
    d_top = (SPINE[1][0] - SPINE[0][0], SPINE[1][1] - SPINE[0][1]); Lt = math.hypot(*d_top)
    ut = (d_top[0] / Lt, 0, d_top[1] / Lt)
    n_out = (-ut[2], 0, ut[0]); nft = (-n_out[0], 0, -n_out[2])      # from the cover into the side plate
    for nm, s in sides:
        tee("Spine top cover", "Spine top cover", f"Spine side plate, {nm}", (SPINE[0][0], s * (si + T / 2), SPINE[0][1]),
            ut, nft, (0, 1, 0), ST_TOP, tab_len=12.0)
    ub = (db[0], 0, db[1]); n_outb = (ub[2], 0, -ub[0]); nfb = (-n_outb[0], 0, -n_outb[2])
    for nm, s in sides:
        tee("Spine bottom cover", "Spine bottom cover", f"Spine side plate, {nm}", (bc0[0], s * (si + T / 2), bc0[1]),
            ub, nfb, (0, 1, 0), ST_BOT, tab_len=12.0)
    # lower yoke under the level edge; upper yoke between the side plates
    for nm, s in sides:
        tee("Lower yoke to spine", "Lower yoke", f"Spine side plate, {nm}", (900, s * (si + T / 2), hz0), (1, 0, 0), (0, 0, 1),
            (0, 1, 0), [("tab", 20), ("bolt", 50)], bom=3)
        tee("Upper yoke to spine", f"Spine side plate, {nm}", "Upper yoke", (910, s * si, hz0 + hl + T / 2), (1, 0, 0),
            (0, -s, 0), (0, 0, 1), [("tab", 15), ("bolt", 45)], bom=3)
    # ribs and seat tube saddles between the side plates
    for xr, (zb, zt) in RIBS.items():
        for nm, s in sides:
            tee("Spine ribs", f"Spine side plate, {nm}", f"Spine rib at {xr:.0f}", (xr + T / 2, s * si, zb), (0, 0, 1),
                (0, -s, 0), (1, 0, 0), [("tab", 22), ("bolt", (zt - zb) / 2), ("tab", zt - zb - 22)])
    for lab, c0 in SADDLES.items():
        for nm, s in sides:
            p0 = v_add(c0, v_mul(tdir, T / 2), v_mul(wdir, -46), (0, s * si, 0))
            tee("Seat tube saddles", f"Spine side plate, {nm}", f"Seat tube saddle, {lab}", p0, wdir, (0, -s, 0), tdir,
                [("bolt", 16), ("tab", 46), ("bolt", 76)])
    # stay bridge
    for nm, s in sides:
        tee("Stay bridge", f"Rear stay plate, {nm}", "Stay bridge", (200 + T / 2, s * st, 480), (0, 0, 1), (0, -s, 0),
            (1, 0, 0), [("tab", 15), ("bolt", 40), ("tab", 65)])
    # stays to spine: through-bolts with washer stacks outside the spine and a spacer tube inside it
    for k, (xn, zn) in enumerate(NODES):
        a = (xn, -(st + T), zn)
        for nm, yc in (("Rear stay plate, right", -st - T / 2), ("Spine side plate, right", -si - T / 2),
                       ("Spine side plate, left", si + T / 2), ("Rear stay plate, left", st + T / 2)):
            _fill(nm, obox((xn, yc, zn), (1, 0, 0), (0, 1, 0), 19, 19, T), f"Stay node {k + 1}: bolt hole")
            _cut(nm, Solid.make_cylinder(4.5, T + 2, Plane(origin=(xn, yc - T / 2 - 1, zn), z_dir=(0, 1, 0))))
        stacks = None
        for y_a, y_b in ((si + T, st), (-st, -si - T)):
            w_ = tube((xn, y_a, zn), (xn, y_b, zn), 8.0, 4.25)
            stacks = w_ if stacks is None else stacks + w_
        add(f"Spacer washer stacks, node {k + 1}", stacks, 4, "plate")
        add(f"Spacer tube, node {k + 1}", tube((xn, -si, zn), (xn, si, zn), 8.0, 6.0), 4, "bought")
        add(f"Bolt: stay node {k + 1}", bolt_set("Stay to spine nodes", a, (0, 1, 0), 2 * (st + T), length=2 * (st + T) + 12), 4,
            "hardware")
        JOINTS.append({"group": "Stay to spine nodes", "kind": "through", "face": "stays and spine", "edge": "",
                       "tabs": 0, "bolts": 1})

    # bed: yokes to bulkhead, bulkhead to rails, rails and axle beams, beams to knuckle posts
    bx = P["BULK_X"]
    tee("Yokes to bulkhead", "Bulkhead", "Lower yoke", (bx, -237, hz0 - T / 2), (0, 1, 0), (-1, 0, 0), (0, 0, 1),
        [("tab", 22), ("bolt", 90), ("tab", 160), ("bolt", 237), ("tab", 314), ("bolt", 384), ("tab", 452)], bom=3)
    tee("Yokes to bulkhead", "Bulkhead", "Upper yoke", (bx, -200, hz0 + hl + T / 2), (0, 1, 0), (-1, 0, 0), (0, 0, 1),
        [("tab", 20), ("bolt", 80), ("tab", 140), ("bolt", 200), ("tab", 260), ("bolt", 320), ("tab", 380)], bom=3)
    for nm, s in sides:
        tee("Bulkhead to rails", f"Bed rail, {nm}", "Bulkhead", (bx + T / 2, s * ri, bz0), (0, 0, 1), (0, -s, 0), (1, 0, 0),
            [("tab", 32), ("bolt", 90), ("tab", 150)], bom=3)
    for nm, s in sides:
        rn = f"Bed rail, {nm}"
        for k, xb in enumerate(P["AB_X"]):
            bn = f"Axle beam plate, {'rear' if k == 0 else 'front'}"
            yc = s * (ry - T / 2)
            _cut(rn, box(xb - 0.2, xb + T + 0.2, yc - 3, yc + 3, rz0 - 1, 415))
            _cut(bn, box(xb - 1, xb + T + 1, yc - T / 2 - 0.2, yc + T / 2 + 0.2, 415, bz + 1))
            JOINTS.append({"group": "Rails and axle beams (halving)", "kind": "halving", "face": rn, "edge": bn,
                           "tabs": 0, "bolts": 0})
    for nm, s in sides:
        for k, xb in enumerate(P["AB_X"]):
            bn = f"Axle beam plate, {'rear' if k == 0 else 'front'}"
            tee("Axle beams to knuckle posts", f"Knuckle post inner cheek, {nm}", bn, (xb + T / 2, s * py0, az0), (0, 0, 1),
                (0, -s, 0), (1, 0, 0), [("tab", 20), ("bolt", 60), ("tab", 100)], bom=3)
    # knuckle post corners and collar plates
    for nm, s in sides:
        for lab, xf, sx in (("rear", wb - px, 1), ("front", wb + px, -1)):
            tpl = f"Knuckle post plate, {nm} {lab}"
            tee("Knuckle post corners", f"Knuckle post inner cheek, {nm}", tpl, (xf - sx * T / 2, s * (py0 + T), az0), (0, 0, 1),
                (0, s, 0), (1, 0, 0), [("tab", 20), ("bolt", 70), ("tab", 120), ("tab", 175), ("bolt", 245), ("tab", 300)],
                bom=3)
            tee("Knuckle post corners", tpl, f"Knuckle post outer cheek, {nm}", (xf, s * (py1 - T / 2), az0), (0, 0, 1),
                (sx, 0, 0), (0, 1, 0), [("tab", 18), ("bolt", 60), ("tab", 100), ("bolt", 145), ("tab", 177)], bom=3)
            for zc, nz, clab in ((kz0, 1, "lower"), (kz1, -1, "upper")):
                tee("Knuckle collar plates", f"Knuckle collar plate, {nm} {clab}", tpl,
                    (xf - sx * T / 2, s * step_y, zc), (0, s, 0), (0, 0, nz), (1, 0, 0),
                    [("tab", 18), ("bolt", 44), ("tab", 74), ("bolt", 117)], bom=3)
    # steering lock stops: a vertical fin plate tabbed and bolted to the front knuckle post plate's front face.
    # Its lower leg hangs beside the clamp plates; at the inner-wheel lock the clamp plate's front inboard corner
    # meets the fin's rear face, so the stop load is along the fin, in its own plane.
    z0s, z1s, z2s = P["STOP_Z"]
    for nm, s in sides:
        xc_, yc_ = stop_corner(s)
        y0 = abs(yc_) - T / 2 if s > 0 else -abs(yc_) - T / 2
        f, n = xz(y0)
        x_r = wb + px + T
        fin = [(x_r, z1s), (xc_, z1s), (xc_, z0s), (xc_ + P["STOP_LEG"], z0s), (xc_ + P["STOP_LEG"], z2s), (x_r, z2s)]
        add(f"Steering lock stop, {nm}", plate("Steering lock stop", 3, fin, f, n), 3, "plate")
        tee("Steering lock stops", f"Knuckle post plate, {nm} front", f"Steering lock stop, {nm}", (x_r, s * abs(yc_), az0),
            (0, 0, 1), (1, 0, 0), (0, 1, 0), [("bolt", 14), ("tab", 34), ("tab", 52)], tab_len=12.0, bom=3)
    # steering arm to clamp plate
    for nm, s in sides:
        leg_y = s * (tr - ly_)
        tee("Steering arm clamps", f"Steering arm clamp plate, {nm}", f"Steering arm, {nm}",
            (wb - lr - T, leg_y - s * 22, P["ARM_Z"] + T / 2), (0, s, 0), (-1, 0, 0), (0, 0, 1),
            [("tab", 14), ("bolt", 34)], bom=5, head_group=f"wheel-{nm}")
    for k in list(C):
        if k.startswith("Bolt: Steering arm clamps"):
            C[k].group = "wheel-left" if C[k].shape.center().Y > 0 else "wheel-right"
            C[k].moving = "L" if C[k].shape.center().Y > 0 else "R"

    # ---------------------------------------------------------------- bought: head tubes, cups, forks, BB
    def cups(cx, cy, zb_, zt_, name, group, moving=""):
        """Head tube between two plates: tube zb_..zt_, plates under zb_ and over zt_, cups through them."""
        tb = Pos(cx, cy, (zb_ + zt_) / 2) * (Cylinder(P["HT_OD"] / 2, zt_ - zb_) - Cylinder(17, zt_ - zb_ + 2))
        cu = (tube((cx, cy, zb_ - T - 5), (cx, cy, zb_ - T), 22.5, 14.3) + tube((cx, cy, zb_ - T), (cx, cy, zb_ + 12), 16.9, 14.3)
              + tube((cx, cy, zt_ + T), (cx, cy, zt_ + T + 5), 22.5, 14.3) + tube((cx, cy, zt_ - 12), (cx, cy, zt_ + T), 16.9, 14.3))
        add(name, tb, 5, "bought", group=group)
        add(name.replace("head tube", "headset cups"), cu, 5, "bought", group=group)
    cups(kp, 0, hz0, hz0 + hl, "Central head tube", "headtube")
    for nm, s in sides:
        cups(wb, s * tr, kz0, kz1, f"Knuckle head tube, {nm}", f"knuckle-{nm}")
    # steering column: a bought threaded fork with a forged crown, legs cut off at the crown, and a tall
    # quill stem; the drop arm bolts under the crown through two holes drilled in it
    crown_t = hz0 - T - 5 - 8
    col = rod((kp, 0, crown_t), (kp, 0, hz0 + hl + T + 30), 14.3)
    crown = Pos(kp, 0, crown_t - 13.5) * Rot(0, 0, math.degrees(math.atan2(ua[1], ua[0]))) * Box(2 * (ly_ + lr), 40, 27)
    for sgn in (1, -1):
        crown = crown - rod((*loc(sgn * cb, 0), crown_t - 30), (*loc(sgn * cb, 0), crown_t + 1), 4.5)
    col = col + crown
    col = col + rod((kp, 0, hz0 + hl + T + 20), (kp, 0, 830), 11.1)
    add("Steering column (cut-down fork and quill stem)", col, 5, "bought", group="column", moving="C")
    for sgn, lab in ((1, "1"), (-1, "2")):
        bx_, by_ = loc(sgn * cb, 0)
        add(f"Bolt: drop arm to crown {lab}", bolt_set("Drop arm to crown", (bx_, by_, crown_t), (0, 0, -1), 27 + T,
                                                        length=27 + T + 12, bom=5), 5, "hardware", group="column", moving="C")
    # knuckle forks with wheels; U-bolts around the inboard leg
    for nm, s in sides:
        cy = s * tr
        fk = rod((wb, cy, kz0 - T - 9), (wb, cy, kz1 + T + 22), 14.3)
        fk = fk + box(wb - 20, wb + 20, cy - ly_ - lr, cy + ly_ + lr, kz0 - T - 9 - 26 - 8, kz0 - T - 9 - 8)
        for sy in (1, -1):
            fk = fk + rod((wb, cy + sy * ly_, kz0 - T - 43), (wb, cy + sy * ly_, P["WHEEL_R"]), lr)
        add(f"Front fork, {nm}", fk, 5, "bought", group=f"wheel-{nm}", moving=nm[0].upper())
        add(f"Front wheel, {nm}", wheel(wb, cy, P["WHEEL_R"], 45, P["FORK_OLD"]), 6, "bought", group=f"wheel-{nm}",
            moving=nm[0].upper())
        leg_y = s * (tr - ly_)
        ub_ = None
        for zc in P["UBOLT_Z"]:
            ring = Pos(wb, leg_y, zc) * (Cylinder(lr + 6.5, 6) - Cylinder(lr + 0.5, 8))
            ring = ring & box(wb, wb + 30, leg_y - 30, leg_y + 30, zc - 5, zc + 5)
            for sy in (-1, 1):
                yl = leg_y + sy * (lr + 3.5)
                ring = ring + rod((wb, yl, zc), (wb - lr - T - 14, yl, zc), 3.0)
                ring = ring + rod((wb - lr - T - 0.5, yl, zc), (wb - lr - T - 5.5, yl, zc), 5.5)
                _cut(f"Steering arm clamp plate, {nm}", rod((wb - lr - T - 1, yl, zc), (wb - lr + 1, yl, zc), 3.5))
            ub_ = ring if ub_ is None else ub_ + ring
        add(f"U-bolts, {nm}", ub_, 5, "bought", group=f"wheel-{nm}", moving=nm[0].upper())
    # bottom bracket: shell between the side plates, cups through them
    bxx, bzz = P["BB_X"], P["BB_Z"]
    bbs = tube((bxx, -si, bzz), (bxx, si, bzz), 19.0, 17.0)
    for s in (1, -1):
        bbs = bbs + tube((bxx, s * si, bzz), (bxx, s * (si + T), bzz), 17.4, 15.0)
        bbs = bbs + tube((bxx, s * (si + T), bzz), (bxx, s * (si + T + 4), bzz), 22.5, 15.0)
    bbs = bbs + rod((bxx, -62, bzz), (bxx, 62, bzz), 8)
    add("Bottom bracket shell and cups", bbs, 8, "bought", group="drive")

    # ---------------------------------------------------------------- bought: rear wheel, drivetrain
    add("Rear wheel", wheel(0, 0, P["WHEEL_R"], 50, 2 * st), 7, "bought", group="drive")
    cyl = P["CHAINLINE"]
    r_ring = P["RING_T"] * 12.7 / (2 * math.pi); r_spr = P["SPROCKET_T"] * 12.7 / (2 * math.pi)
    dt = (rod((bxx, cyl - 1.5, bzz), (bxx, cyl + 1.5, bzz), r_ring + 4)
          + rod((0, cyl - 1.5, P["WHEEL_R"]), (0, cyl + 1.5, P["WHEEL_R"]), r_spr + 4)
          + rod((0, cyl, P["WHEEL_R"] + r_spr), (bxx, cyl, bzz + r_ring), 4)
          + rod((0, cyl, P["WHEEL_R"] - r_spr), (bxx, cyl, bzz - r_ring), 4))
    ca = math.radians(55)
    for s in (1, -1):
        tip = (bxx + s * P["CRANK"] * math.cos(ca), s * 72, bzz - s * P["CRANK"] * math.sin(ca))
        dt = dt + rod((bxx, s * 64, bzz), (bxx, s * 80, bzz), 12) + rod((bxx, s * 72, bzz), tip, 8) \
            + Pos(tip[0], s * 110, tip[2]) * Box(90, 60, 20)
    add("Drivetrain (chainring, cranks, pedals, chain, sprocket)", dt, 8, "bought", group="drive")

    # ---------------------------------------------------------------- 9 box
    x0 = P["BOX_X0"]; x1 = x0 + P["BOX_L"]; yb = P["BOX_W"] / 2; z0 = P["BOX_Z0"]; z1 = z0 + P["BOX_H"]
    w = P["PLY_WALL"]
    cb = box(x0, x1, -yb, yb, z0, z1) - box(x0 + w, x1 - w, -yb + w, yb - w, z0 + P["PLY_FLOOR"], z1 + 1)
    add("Cargo box", cb, 9, "wood")
    for s in (1, -1):        # counterbores in the box sides for the knuckle post bolt heads
        for xh in (wb - px - T / 2, wb + px + T / 2):
            _cut("Cargo box", rod((xh, s * (yb + 1), 595.0), (xh, s * (yb - 5), 595.0), 10.0))
    add("Cargo box lid", box(x0, x1, -yb, yb, z1, z1 + w), 9, "wood")
    for nm, s in sides:
        tee("Box to rails", "Cargo box", f"Bed rail, {nm}", (1240, s * (ry - T / 2), bz), (1, 0, 0), (0, 0, -1), (0, 1, 0),
            [("bolt", 0), ("bolt", 210), ("bolt", 615)], tf=P["PLY_FLOOR"], bom=9)
    for s in (1, -1):
        yb_, zb_ = s * 220, hz0 + hl + T / 2
        _fill("Bulkhead", obox((bx + T / 2, yb_, zb_), (0, 1, 0), (1, 0, 0), 19, 19, T), "Box to bulkhead: bolt hole")
        _cut("Bulkhead", rod((bx - 1, yb_, zb_), (x0 + w + 1, yb_, zb_), 4.5))
        _cut("Cargo box", rod((bx - 1, yb_, zb_), (x0 + w + 1, yb_, zb_), 4.5))
        add(f"Spacer washers, box to bulkhead {'left' if s > 0 else 'right'}", tube((bx + T, yb_, zb_), (x0, yb_, zb_), 8.0, 4.25),
            4, "plate")
        add(f"Bolt: box to bulkhead {'left' if s > 0 else 'right'}",
            bolt_set("Box to bulkhead", (x0 + w, yb_, zb_), (-1, 0, 0), x0 + w - bx, length=x0 + w - bx + 12, bom=9), 9, "hardware")
        JOINTS.append({"group": "Box to bulkhead", "kind": "through", "face": "Cargo box,Bulkhead", "edge": "",
                       "tabs": 0, "bolts": 1})

    # ---------------------------------------------------------------- 10 seat: bought seat tube, collars, seatpost, saddle
    tdv = Vector(*tdir)
    lo, up = SADDLES["lower"], SADDLES["upper"]
    a_ = Vector(*lo) - tdv * 25; b_ = Vector(*up) + tdv * 95
    add("Seat tube", tube(tuple(a_), tuple(b_), P["SEAT_TUBE_R"], 13.7), 10, "bought", group="seat")
    sc = tube(tuple(Vector(*up) + tdv * T), tuple(Vector(*up) + tdv * (T + 14)), 25, P["SEAT_TUBE_R"]) + \
        tube(tuple(Vector(*lo) - tdv * 14), tuple(Vector(*lo)), 25, P["SEAT_TUBE_R"])
    add("Seat tube shaft collars", sc, 10, "bought", group="seat")
    cut_seat = rod(tuple(a_ - tdv * 50), tuple(b_ + tdv * 50), P["SEAT_TUBE_R"] + 1.0)
    _cut("Spine top cover", cut_seat)
    zs = P["SADDLE_TOP"]
    sp = rod((seat_xy(690), 0, 690), (seat_xy(zs - 40), 0, zs - 40), 13.6) + \
        Pos(seat_xy(zs - 25), 0, zs - 25) * Box(260, 160, 50)
    add("Seatpost and saddle", sp, 10, "bought", group="seat")

    # ---------------------------------------------------------------- 11, 12 bars, brakes
    add("Handlebar and stem", rod((kp, 0, 830), (930, 0, 850), 14) + rod((930, -290, 850), (930, 290, 850), 11)
        + rod((930, 290, 850), (885, 320, 850), 13) + rod((930, -290, 850), (885, -320, 850), 13), 11, "bought", group="column",
        moving="C")
    add("Brake levers, cables and parking latch",
        Pos(920, 250, 862) * Box(40, 30, 22) + Pos(920, -250, 862) * Box(40, 30, 22) + Pos(920, 200, 862) * Box(30, 22, 30)
        + rod((920, 250, 850), (900, 80, 640), 3) + rod((900, 80, 640), (880, 80, 560), 3)
        + rod((880, 80, 560), (60, 75, 340), 3)
        + rod((920, -250, 850), (1040, -180, 640), 3) + rod((1040, -180, 640), (1040, -180, 480), 3),
        12, "bought", group="cables")

    # ---------------------------------------------------------------- 5 linkage: drag link and tie rod with rod ends
    linkage(0.0, 0.0, 0.0, add_to_model=True)
    return C


def _rot_z(pt, centre, ang):
    c, s = math.cos(ang), math.sin(ang)
    dx, dy = pt[0] - centre[0], pt[1] - centre[1]
    return (centre[0] + c * dx - s * dy, centre[1] + s * dx + c * dy) + tuple(pt[2:])


DRAG_Z = (P["DROP_Z"] - 9.0, P["ARM_Z"] - 7.0)     # drag link rod-end heights: under the drop arm, under the left arm
TIE_Z = P["ARM_Z"] + T + 7.0                            # tie rod rod-end height, on top of both arms


def linkage(dL, dR, phi, add_to_model=False):
    """Drag link and tie rod for wheel angles dL, dR and column angle phi (radians, + is anticlockwise
    seen from above). Returns {name: solid}."""
    wb, tr, kp = P["WB"], P["TRACK"] / 2, P["KP_X"]
    tL = _rot_z(ackermann_tip(1), (wb, tr), dL); tR = _rot_z(ackermann_tip(-1), (wb, -tr), dR)
    pin = _rot_z(drop_pin(), (kp, 0), phi)
    out = {}
    tie = rod((tL[0], tL[1], TIE_Z), (tR[0], tR[1], TIE_Z), 6) + _eyes([tL, tR], TIE_Z)
    drag = rod((pin[0], pin[1], DRAG_Z[0]), (tL[0], tL[1], DRAG_Z[1]), 5) + _eyes([pin], DRAG_Z[0]) + _eyes([tL], DRAG_Z[1])
    pins = None
    for (x, y), z0, z1 in ((tL, DRAG_Z[1] - 8, TIE_Z + 5.5), (tR, P["ARM_Z"] - 6, TIE_Z + 5.5), (pin, DRAG_Z[0] - 8, P["DROP_Z"] + T)):
        b = rod((x, y, z0), (x, y, z1), 4.0) + rod((x, y, z1), (x, y, z1 + 5.3), 6.5)
        pins = b if pins is None else pins + b
    out["Tie rod with rod ends"] = tie
    out["Drag link with rod ends"] = drag
    out["Rod end bolts"] = pins
    if add_to_model:
        add("Tie rod with rod ends", tie, 5, "bought", group="linkage")
        add("Drag link with rod ends", drag, 5, "bought", group="linkage")
        add("Rod end bolts", pins, 5, "hardware", group="linkage")
        BOLT_GROUPS["Rod end bolts"] = 3
    return out


def _eyes(pts, z):
    e = None
    for x, y in pts:
        r = Pos(x, y, z) * (Cylinder(9.5, 11) - Cylinder(4.0, 13))
        e = r if e is None else e + r
    return e


# ---------------------------------------------------------------- grouping by BOM line
NAMES = {1: "Spine plates and covers", 2: "Rear stay plates (pair)", 3: "Front bed and knuckle post plates",
         4: "Ribs, saddles, spacers and M8 bolts", 5: "Steering column, knuckles and linkage", 6: "Front wheels, drum brakes (2)",
         7: "Rear wheel, 3-speed drum hub", 8: "Drivetrain", 9: "Cargo box and lid, plywood",
         10: "Seat tube, seatpost and saddle", 11: "Handlebar and stem", 12: "Brake levers, cables, parking latch"}


def build_parts(comps=None):
    """Components fused by BOM line (1 to 12), for the calculations, concept media and general arrangement."""
    comps = comps or build_components()
    out = {}
    for name, c in comps.items():
        out.setdefault(c.bom, []).append(c.shape)
    return {k: Compound(children=v) for k, v in sorted(out.items())}


def plate_schedule():
    """Group PLATES by name: qty, area each (m2), bounding size (mm). Call after build_components()."""
    out = {}
    for p in PLATES:
        k = p["name"]
        if k not in out:
            out[k] = {"bom": p["bom"], "qty": 0, "area_m2": p["area_mm2"] / 1e6, "size": p["size"]}
        out[k]["qty"] += 1
    return out


def bolt_count():
    return dict(BOLT_GROUPS)


# ---------------------------------------------------------------- constructability checks
def check(verbose=True):
    """Constructability checks. Returns a list of failures (empty when the design is constructable)."""
    import itertools
    comps = build_components()
    fails = list(ISSUES)
    names = [n for n, c in comps.items() if c.group != "cables"]
    bbs = {n: comps[n].shape.bounding_box() for n in names}

    def bb_gap(a, b):
        A, B = bbs[a], bbs[b]
        return max(A.min.X - B.max.X, B.min.X - A.max.X, A.min.Y - B.max.Y, B.min.Y - A.max.Y,
                   A.min.Z - B.max.Z, B.min.Z - A.max.Z)
    # 1. no two pieces overlap (pieces of one bought assembly excepted)
    n_pairs = 0; overlaps = []
    for a, b in itertools.combinations(names, 2):
        if comps[a].group == comps[b].group or bb_gap(a, b) > 0.01:
            continue
        n_pairs += 1
        try:
            v = (comps[a].shape & comps[b].shape).volume
        except Exception:
            v = 0.0
        if v > 1.0:
            overlaps.append((a, b, v))
    for a, b, v in overlaps:
        fails.append(f"overlap {v:.0f} mm3: {a} / {b}")
    # 2. every piece touches the assembly (no floating parts): connectivity within 0.05 mm
    adj = {n: set() for n in names}
    for a, b in itertools.combinations(names, 2):
        if bb_gap(a, b) > 0.06:
            continue
        if comps[a].group == comps[b].group and comps[a].kind == "bought":
            adj[a].add(b); adj[b].add(a); continue
        try:
            d = comps[a].shape.distance_to(comps[b].shape)
        except Exception:
            d = 99
        if d < 0.06:
            adj[a].add(b); adj[b].add(a)
    seen = set(); stack = ["Spine side plate, left"]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n); stack += list(adj[n] - seen)
    for n in names:
        if n not in seen:
            fails.append(f"floating: {n} does not touch the rest of the assembly")
    # 3. steering sweep: wheels, forks, arms, linkage and column against the fixed structure
    sweep = steering_sweep(comps)
    fails += sweep
    # 4. lock stops: each clamp plate meets its stop fin at the inner-wheel lock, and not before
    stops = lock_stop_check(comps)
    fails += stops
    if verbose:
        print(f"components {len(comps)}, plates {len(PLATES)}, joints {len(JOINTS)}, bolt sets {sum(BOLT_GROUPS.values())}")
        print(f"overlap pairs tested {n_pairs}; overlaps {len(overlaps)}; floating {len(names) - len(seen)}; "
              f"joint issues {len(ISSUES)}; steering sweep issues {len(sweep)}; lock stop issues {len(stops)}")
        for f_ in fails:
            print("  FAIL", f_)
        print("PASS" if not fails else f"{len(fails)} failures")
    return fails


def _steer_angles(d_in):
    """Ackermann: inner angle d_in (deg, + = left turn) -> (left wheel, right wheel) angles, radians."""
    if abs(d_in) < 1e-9:
        return 0.0, 0.0
    wb, tr = P["WB"], P["TRACK"] / 2
    a = math.radians(abs(d_in))
    y_ic = tr + wb / math.tan(a)
    d_out = math.atan(wb / (y_ic + tr))
    return (a, d_out) if d_in > 0 else (-d_out, -a)


def _left_for_right(dR):
    """Left wheel angle that puts the right wheel at dR (radians) through the tie rod."""
    a, b = 0.0, 0.0
    while _right_angle(b) > dR:          # step the left wheel into the right turn until the right wheel passes dR
        a, b = b, b - 0.005
    for _ in range(60):
        m = (a + b) / 2
        if _right_angle(m) > dR:
            a = m
        else:
            b = m
    return (a + b) / 2


def _right_angle(dL):
    """Right wheel angle that keeps the tie rod at its straight-ahead length (true trapezoid kinematics);
    the root nearest the ideal Ackermann angle."""
    wb, tr = P["WB"], P["TRACK"] / 2
    tL0, tR0 = ackermann_tip(1), ackermann_tip(-1)
    L0 = math.dist(tL0, tR0)
    tL = _rot_z(tL0, (wb, tr), dL)

    def f(d):
        return math.dist(tL, _rot_z(tR0, (wb, -tr), d)) - L0
    if abs(dL) < 1e-12:
        return 0.0
    y_ic = tr + wb / math.tan(abs(dL)) if dL > 0 else None
    guess = math.atan(wb / (y_ic + tr)) if dL > 0 else -math.atan(wb / (wb / math.tan(-dL) - 2 * tr)) \
        if wb / math.tan(-dL) > 2 * tr else dL
    best = None
    for k in range(0, 400):
        for x0, x1 in ((guess + k * 0.002, guess + (k + 1) * 0.002), (guess - (k + 1) * 0.002, guess - k * 0.002)):
            if f(x0) * f(x1) <= 0:
                best = (x0, x1); break
        if best:
            break
    lo, hi = best
    for _ in range(60):
        m = (lo + hi) / 2
        if f(lo) * f(m) <= 0:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2


def _column_angle(dL):
    """Column angle that keeps the drag link at its straight-ahead length for left wheel angle dL."""
    wb, tr, kp = P["WB"], P["TRACK"] / 2, P["KP_X"]
    t0 = ackermann_tip(1); p0 = drop_pin()
    L0 = math.dist((p0[0], p0[1], DRAG_Z[0]), (t0[0], t0[1], DRAG_Z[1]))
    tL = _rot_z(t0, (wb, tr), dL)

    def f(phi):
        pin = _rot_z(p0, (kp, 0), phi)
        return math.dist((pin[0], pin[1], DRAG_Z[0]), (tL[0], tL[1], DRAG_Z[1])) - L0
    best = None
    for k in range(0, 300):          # search outward from the parallelogram answer phi = dL
        for x0, x1 in ((dL + k * 0.002, dL + (k + 1) * 0.002), (dL - (k + 1) * 0.002, dL - k * 0.002)):
            if f(x0) * f(x1) <= 0:
                best = (x0, x1); break
        if best:
            break
    if best is None:
        raise ValueError(f"steering linkage cannot reach a left wheel angle of {math.degrees(dL):.1f} deg")
    lo, hi = best
    for _ in range(60):
        m = (lo + hi) / 2
        if f(lo) * f(m) <= 0:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2


LOCK_STOP = {}      # side -> (gap at the lock, gap 1 deg before it, overlap at the lock); filled by lock_stop_check


def lock_stop_check(comps, verbose=False):
    """Each steering arm clamp plate meets its knuckle post's stop fin at the inner-wheel lock (left wheel at
    +STEER_LOCK, right wheel at -STEER_LOCK): gap under 0.2 mm and no overlap at the lock, clear 1 deg before it."""
    wb, tr = P["WB"], P["TRACK"] / 2
    fails = []
    for nm, s in (("left", 1), ("right", -1)):
        plate_ = comps[f"Steering arm clamp plate, {nm}"].shape
        pin = comps[f"Steering lock stop, {nm}"].shape
        res = []
        for d in (P["STEER_LOCK"], P["STEER_LOCK"] - 1.0):
            rot = Pos(wb, s * tr, 0) * Rot(0, 0, s * d) * Pos(-wb, -s * tr, 0)
            moved = rot * plate_
            gap = moved.distance_to(pin)
            try:
                ov = (moved & pin).volume
            except Exception:
                ov = 0.0
            res.append((gap, ov))
        LOCK_STOP[nm] = (res[0][0], res[1][0], res[0][1])
        if res[0][0] > 0.2 or res[0][1] > 0.5:
            fails.append(f"lock stop, {nm}: clamp plate is {res[0][0]:.2f} mm from its stop at {P['STEER_LOCK']:.0f} deg "
                         f"(overlap {res[0][1]:.1f} mm3)")
        if res[1][0] < 0.3:
            fails.append(f"lock stop, {nm}: clamp plate already meets its stop 1 deg before the lock")
    return fails


def steering_sweep(comps, angles=(-40, -30, -20, -10, 0, 10, 20, 30, 40), report=None):
    wb, tr, kp = P["WB"], P["TRACK"] / 2, P["KP_X"]
    fixed = [n for n, c in comps.items() if not c.moving and c.group not in ("linkage", "cables")]
    fails = []
    mov = {"L": [n for n, c in comps.items() if c.moving == "L" and not n.startswith("Front wheel")],
           "R": [n for n, c in comps.items() if c.moving == "R" and not n.startswith("Front wheel")],
           "C": [n for n, c in comps.items() if c.moving == "C" and not n.startswith("Handlebar")]}
    tyres = {"L": wheel(wb, tr, P["WHEEL_R"], 45, P["FORK_OLD"], tyre_only=True),
             "R": wheel(wb, -tr, P["WHEEL_R"], 45, P["FORK_OLD"], tyre_only=True)}
    fb = {n: comps[n].shape.bounding_box() for n in fixed}
    min_gap = {}; straight = {}
    for d in sorted(angles, key=abs):
        # d is the inner wheel's angle: the left wheel in a left turn (+), the right wheel in a right turn (-)
        dL = math.radians(d) if d >= 0 else _left_for_right(math.radians(d))
        dR = _right_angle(dL)
        phi = _column_angle(dL)
        movers = []
        for side, ang, cx, cy in (("L", dL, wb, tr), ("R", dR, wb, -tr), ("C", phi, kp, 0)):
            rot = Pos(cx, cy, 0) * Rot(0, 0, math.degrees(ang)) * Pos(-cx, -cy, 0)
            for n in mov[side]:
                movers.append((n, rot * comps[n].shape))
            if side in tyres:
                movers.append((f"Front tyre, {'left' if side == 'L' else 'right'}", rot * tyres[side]))
        for n, s in linkage(dL, dR, phi).items():
            movers.append((n, s))
        for n, s in movers:
            b = s.bounding_box()
            for fn in fixed:
                B = fb[fn]
                gap = max(b.min.X - B.max.X, B.min.X - b.max.X, b.min.Y - B.max.Y, B.min.Y - b.max.Y,
                          b.min.Z - B.max.Z, B.min.Z - b.max.Z)
                if gap > 6:
                    continue
                if fn.startswith("Bolt: Steering arm") or (n.startswith("Rod end") and fn.startswith("Steering arm")):
                    continue
                if n.startswith("Steering arm clamp plate") and fn.startswith("Steering lock stop"):
                    continue          # the stop contact itself; checked by lock_stop_check()
                try:
                    dist = s.distance_to(comps[fn].shape)
                except Exception:
                    dist = 99
                key = (n, fn)
                if d == 0:
                    straight[key] = dist
                if dist < min_gap.get(key, (99, 0))[0]:
                    min_gap[key] = (dist, d)
    for (n, fn), (dist, d) in sorted(min_gap.items(), key=lambda kv: kv[1][0]):
        d0 = straight.get((n, fn), 99)
        if dist < 3.0 and dist < d0 - 0.3:      # a clearance that closes up as the wheels turn
            fails.append(f"steering at {d:+d} deg: {n} comes within {dist:.1f} mm of {fn}")
    if report is not None:
        report.update(min_gap)
    return fails


if __name__ == "__main__":
    if "--check" in sys.argv:
        f = check()
        sys.exit(1 if f else 0)
    comps = build_components()
    parts = build_parts(comps)
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    frame = Compound(children=[parts[1], parts[2], parts[4], parts[5]])
    front = Compound(children=[parts[3]])
    asm = Compound(children=[parts[k] for k in sorted(parts)])
    for name, shp in (("flattrike-frame", frame), ("flattrike-front-bed", front), ("flattrike-assembly", asm)):
        export_step(shp, str(root / "step" / f"{name}.step"))
        export_stl(shp, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
    bb = asm.bounding_box()
    print(f"assembly bounding box: L {bb.size.X:.0f} x W {bb.size.Y:.0f} x H {bb.size.Z:.0f} mm")
    tot = 0.0
    for k, v in plate_schedule().items():
        tot += v["qty"] * v["area_m2"]
        print(f"  {k:28s} item {v['bom']}  x{v['qty']}  {v['area_m2']:.4f} m2 each  {v['size'][0]:.0f} x {v['size'][1]:.0f} mm")
    print(f"total plate area {tot:.3f} m2, mass {tot * T * 7.85:.1f} kg at 3 mm; {len(PLATES)} plates")
    print(f"bolt sets {sum(BOLT_GROUPS.values())}: {BOLT_GROUPS}")
    print("wrote cad/step/*.step and cad/stl/*.stl")
