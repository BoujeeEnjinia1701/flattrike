"""FlatTrike product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: powder-coated flat 3 mm plates with their tabs, slots
and T-slots as cut, zinc M8 bolt heads, washers and locknuts at every node, cut
spacer-washer stacks, a filleted spine box with a white part-number decal, tyres with tread, 36-spoke
wheels with drum brake hubs, a 3-speed rear hub, toothed chainring and sprocket with a roller chain
and a flat-cut chain guard ring, platform pedals, a sprung saddle, rubber grips, brake levers with a
parking latch, the Ackermann steering linkage with rod ends, a plywood cargo box with corner bumpers,
hinges, hasp and padlock, mudguards, reflectors, a bell and the cornering-speed label on the bar.
Context: a produce crate strapped to the counter lid, and the shared clay mannequin riding (pose
"ride", placed from its landmarks so it sits on the saddle, its feet meet the pedals and its hands
meet the grips).
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every plate, tube, bought steering part and bolt set of the frame is the constructable part from
model.build_components() (FTK-DDR-003 and the decisions of 2026-10-02, steering lock stops included),
so the renders show the design for construction. Wheels, drivetrain detail, seat, bars, box hardware
and accessories are drawn here in appearance detail from PARAMS. Axes as model.py: X forward, Y to the left, Z up,
ground at Z = 0, rear axle at X = 0. Group "internal" holds the core module that the detail view
frames: spine box, rear stays, ribs and spacers, drivetrain and rear wheel.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Compound, Cylinder, Face, Plane, Pos, RegularPolygon, Rot, Solid,  # noqa: E402
                       Sphere, Torus, Vector, Wire, extrude, fillet)
from model import (PARAMS, SPINE, SPINE_HOLES, SPINE_WIN, STAY, STAY_WIN, circle_pts, edge_strip,  # noqa: E402
                   plate, seat_xy, xy, xz, yz)

TITLE = "FlatTrike: bolt-together cargo tricycle cut from flat steel plate"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 22, "az": -52,
     "note": "Product render from the front right and above (about 22 deg elevation); rider on the saddle, "
             "crate on the counter lid, flat-cut teal frame plates bolted together"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): spine side plates and "
             "covers, ribs, rear stays, front bed and knuckle posts, steering, wheels, drivetrain, seat, "
             "handlebar and cargo box"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 16, "az": 38,
     "note": "Detail from the front left, slightly above (about 16 deg elevation): bolted spine box and rear "
             "stays, spacer stacks, chainring, chain guard, chain and 3-speed rear hub"},
]

P = PARAMS
T = P["T"]

# Colours (restrained product palette; kit accent for the powder-coated plates)
C_TEAL = "#0F766E"
C_GRAPH = "#334155"
C_FORK = "#23272D"
C_ZINC = "#C5CAD0"
C_STEEL = "#9AA1A9"
C_RIM = "#B9BFC6"
C_SPOKE = "#D3D7DB"
C_TYRE = "#1B1E22"
C_RUBBER = "#26292E"
C_CHAIN = "#4A4F56"
C_WOOD = "#C8A277"
C_WOOD2 = "#D6B68D"
C_LABEL = "#F2F2EF"
C_INK = "#1F2937"
C_BRASS = "#B8962E"
C_RED = "#B91C1C"
C_REFL = "#E6E7E9"
C_CRATE = "#44627F"
C_STRAP = "#1F2937"
C_CLAY = "#9CA3AF"


# ---------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _rod(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _on(origin, zdir, shape):
    """Place a shape built along +Z at `origin`, its +Z along `zdir`."""
    return Plane(origin=Vector(*origin), z_dir=Vector(*zdir)).location * shape


def _comp(shapes):
    shapes = [s for s in shapes if s is not None]
    return Compound(children=shapes)


def _rplate(poly, to3d, normal, holes=(), radii=(8.0, 5.0, 3.0, 1.5)):
    """Flat plate from model.plate() with laser-cut corner radii on its profile and window corners."""
    s = plate("appearance", None, poly, to3d, normal, holes, record=False)
    return _fillet_try(s, s.edges().filter_by(Axis((0, 0, 0), normal)), radii)


def _hex_head(origin, zdir, af=13.0, h=5.3, washer=True):
    """M8 hex head (or nut) with a washer, seated on a face at `origin`, standing along `zdir`."""
    parts = []
    z = 0.0
    if washer:
        parts.append(Pos(0, 0, 0.8) * Cylinder(8.0, 1.6))
        z = 1.6
    hx = Pos(0, 0, z) * extrude(RegularPolygon(af / 1.732, 6), amount=h)
    hx = _fillet_try(hx, hx.faces().sort_by(Axis.Z)[-1].edges(), [0.8, 0.4])
    parts.append(hx)
    return [_on(origin, zdir, p) for p in parts]


def _bolt(origin, zdir, grip, af=13.0):
    """Head on one face, locknut and a short thread stub on the far face `grip` mm away."""
    o = Vector(*origin); n = Vector(*zdir).normalized()
    out = _hex_head(o, n, af)
    far = o - n * grip
    out += _hex_head(far, -n, af, h=6.5)
    out.append(_on(far - n * 8.1, -n, Pos(0, 0, 2.5) * Cylinder(4.0, 5.0)))
    return out


def _teeth(r_pitch, n, depth=4.5, y=0.0, t=3.0):
    """Toothed ring (chainring or sprocket) in the XZ plane, thickness t along Y centred at y."""
    pts = []
    for k in range(n):
        a0 = 2 * math.pi * k / n
        for frac, rr in ((0.0, r_pitch - depth), (0.22, r_pitch + depth * 0.9), (0.5, r_pitch + depth * 0.9),
                         (0.72, r_pitch - depth)):
            a = a0 + frac * 2 * math.pi / n
            pts.append((rr * math.cos(a), rr * math.sin(a)))
    f = Face(Wire.make_polygon([Vector(u, y - t / 2, v) for u, v in pts], close=True))
    return extrude(f, amount=t, dir=(0, 1, 0))


def _arc_band(cx, cy, cz, r0, r1, w, a0, a1):
    """Annular band in the XZ plane (mudguard), from angle a0 to a1 (degrees from +X toward +Z)."""
    ring = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(r1, w) - Cylinder(r0, w + 2))
    pts = [(cx, cz)]
    for k in range(13):
        a = math.radians(a0 + (a1 - a0) * k / 12)
        pts.append((cx + 2 * r1 * math.cos(a), cz + 2 * r1 * math.sin(a)))
    f = Face(Wire.make_polygon([Vector(u, cy - w, v) for u, v in pts], close=True))
    return ring & extrude(f, amount=2 * w, dir=(0, 1, 0))


# ---------------------------------------------------------------- wheels
def _wheel(cx, cy, cz, hub_r, hub_len, rear=False):
    """Returns dict of tyre, tread, rim, spokes and hub pieces for a 20 in wheel (axis along Y)."""
    R = P["WHEEL_R"]; tw = P["TYRE_W"]
    tyre = Pos(cx, cy, cz) * Rot(90, 0, 0) * Torus(R - tw / 2, tw / 2)
    tread = []
    n = 64
    for k in range(n):
        a = 2 * math.pi * (k + 0.5 * (k % 2)) / n
        for sy in (-1, 1):
            if (k + (sy > 0)) % 2:
                continue
            blk = Pos(0, sy * 9.5, R - 1.5) * Box(9.0, 11.0, 6.5)
            tread.append(Pos(cx, cy, cz) * Rot(0, -math.degrees(a), 0) * blk)
        tread.append(Pos(cx, cy, cz) * Rot(0, -math.degrees(a), 0) * (Pos(0, 0, R - 0.5) * Box(5.0, 6.0, 5.0)))
    rim = Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(R - 45, 22) - Cylinder(R - 57, 24))
    rim += Pos(cx, cy, cz) * Rot(90, 0, 0) * (Cylinder(R - 40, 3) - Cylinder(R - 50, 4))
    fl = hub_len / 2 - 8
    hub = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(hub_r * 0.62, hub_len - 6)
    for sy in (-1, 1):
        hub += Pos(cx, cy + sy * fl, cz) * Rot(90, 0, 0) * Cylinder(hub_r + 10, 3.0)
    drum = Pos(cx, cy - fl + 12, cz) * Rot(90, 0, 0) * Cylinder(hub_r + 6, 20)
    for k in range(4):
        drum -= Pos(cx, cy - fl + 5 + 4.5 * k, cz) * Rot(90, 0, 0) * (Cylinder(hub_r + 8, 1.4) - Cylinder(hub_r + 4.5, 2))
    brake_plate = Pos(cx, cy - fl + 1.5, cz) * Rot(90, 0, 0) * Cylinder(hub_r + 8, 3.0)
    arm = _rod((cx, cy - fl, cz), (cx - 110, cy - fl, cz - 25), 6.0)
    spokes = []
    for k in range(36):
        side = 1 if k % 2 else -1
        a = 2 * math.pi * k / 36
        b = a + side * 2 * math.pi * 3 / 36 * (1 if (k // 2) % 2 else -1)
        hp = (cx + (hub_r + 6) * math.cos(a), cy + side * fl, cz + (hub_r + 6) * math.sin(a))
        rp = (cx + (R - 56) * math.cos(b), cy + side * 3.0, cz + (R - 56) * math.sin(b))
        spokes.append(_rod(hp, rp, 1.0))
    ax_len = hub_len + 30
    axle = Pos(cx, cy, cz) * Rot(90, 0, 0) * Cylinder(5.0, ax_len)
    nuts = []
    for sy in (-1, 1):
        nuts += _hex_head((cx, cy + sy * (hub_len / 2 + 3), cz), (0, sy, 0), af=15.0, h=7.0)
    out = dict(tyre=tyre, tread=_comp(tread), rim=rim, spokes=_comp(spokes), hub=hub, drum=drum,
               brake=brake_plate + arm, axle=_comp([axle] + nuts))
    if rear:
        # 3-speed hub gear: shifter click box on the drive side
        out["clickbox"] = _box(cx, cy + hub_len / 2 + 22, cz, 22, 14, 28)
    return out


# ---------------------------------------------------------------- rider fit
def _fit_rider(height, seat_w, grips_w, pedals_w):
    """Joint overrides and translation so mannequin(height, 'ride') meets the trike's seat, pedals and grips.

    World targets are in model.py axes; the figure is turned Rot(0, 0, 90) so it faces +X. Returns
    (joints, (tx, ty, tz))."""
    from scipy.optimize import least_squares
    from context_parts import mannequin_landmarks
    lm0 = mannequin_landmarks(height, "ride", torso_lean=36.0)
    j0 = lm0["joints"]
    sx, sy, sz = lm0["seat"]
    # local (x, y, z) -> world (tx - y, ty + x, tz + z)
    tx, ty, tz = seat_w[0] + sy, seat_w[1] - sx, seat_w[2] - sz
    to_local = lambda w: (w[1] - ty, tx - w[0], w[2] - tz)
    joints = {"torso_lean": 36.0}

    def solve(names, key, idx, target, pitch_target=None):
        x0 = [j0[n] + (12.0 if "abd" in n else 0.0) for n in names]

        def res(x):
            kw = dict(joints); kw.update(dict(zip(names, x)))
            lm = mannequin_landmarks(height, "ride", **kw)
            p = lm[key][idx]
            r = [p[0] - target[0], p[1] - target[1], p[2] - target[2]]
            if pitch_target is not None:
                jj = lm["joints"]
                s = "l" if idx == 0 else "r"
                pitch = jj[f"hip_flex_{s}"] - jj[f"knee_flex_{s}"] + jj[f"ankle_flex_{s}"]
                r.append(0.5 * (pitch - pitch_target))
            return r
        sol = least_squares(res, x0, diff_step=0.05)
        joints.update(dict(zip(names, sol.x)))

    for idx, s in ((0, "l"), (1, "r")):
        solve([f"hip_flex_{s}", f"knee_flex_{s}", f"ankle_flex_{s}"], "feet", idx, to_local(pedals_w[idx]), 0.0)
        solve([f"shoulder_flex_{s}", f"elbow_flex_{s}", f"shoulder_abd_{s}"], "hands", idx, to_local(grips_w[idx]))
    return joints, (tx, ty, tz)


# ---------------------------------------------------------------- constructable parts from model.py
_SKIP = ("Rear wheel", "Front wheel", "Drivetrain", "Cargo box", "Seatpost and saddle", "Handlebar", "Brake levers",
         "Seat tube")      # drawn here in appearance detail instead (or added with the seat)
_REAR_X = 960.0           # parts centred behind this belong to the core module (group "internal")


def _model_components():
    import model as M
    return dict(M.build_components())


def _style(name, c):
    """(colour, material, group, explode) for a model.py component, or None to skip it."""
    if name.startswith(_SKIP):
        return None
    cx = c.shape.center().X
    grp = "internal" if cx < _REAR_X and not name.startswith(("Upper yoke", "Lower yoke", "Central head", "Central headset",
                                                              "Steering column", "Drop arm", "Bolt: drop arm",
                                                              "Bolt: lower yoke", "Bolt: upper yoke", "Drag link")) else "shell"
    if name.startswith("Spine side plate, left"):
        return C_TEAL, "painted", grp, (0, 260, 0)
    if name.startswith("Spine side plate, right"):
        return C_TEAL, "painted", grp, (0, -260, 0)
    if name.startswith("Spine top cover"):
        return C_GRAPH, "painted", grp, (0, 0, 220)
    if name.startswith("Spine bottom cover"):
        return C_GRAPH, "painted", grp, (0, 0, -220)
    if name.startswith("Rear stay plate"):
        s = 1 if "left" in name else -1
        return C_TEAL, "painted", grp, (-120, s * 520, 0)
    if name.startswith(("Spine rib", "Stay bridge", "Seat tube saddle")):
        return C_GRAPH, "painted", grp, (0, 0, 0)
    if name.startswith(("Spacer washer stacks", "Spacer tube")):
        s = 1 if c.shape.center().Y >= 0 else -1
        return C_GRAPH, "painted", grp, (0, 0, 0)
    if name.startswith("Bottom bracket shell"):
        return C_STEEL, "metal", grp, (0, 0, 0)
    if name.startswith(("Bed rail",)):
        s = 1 if "left" in name else -1
        return C_TEAL, "painted", grp, (620, s * 170, 0)
    if name.startswith(("Knuckle post plate", "Knuckle post inner", "Knuckle post outer")):
        s = 1 if "left" in name else -1
        return C_TEAL, "painted", grp, (620, s * 330, 0)
    if name.startswith(("Knuckle collar plate", "Steering lock stop")):
        s = 1 if "left" in name else -1
        return C_GRAPH, "painted", grp, (620, s * 330, 0)
    if name.startswith(("Knuckle head tube",)):
        s = 1 if "left" in name else -1
        return C_GRAPH, "painted", grp, (620, s * 330, 0)
    if name.startswith(("Knuckle headset",)):
        s = 1 if "left" in name else -1
        return C_STEEL, "metal", grp, (620, s * 700, 0)
    if name.startswith(("Front fork", "U-bolts", "Steering arm")):
        s = 1 if "left" in name else -1
        col = C_FORK if name.startswith("Front fork") else (C_ZINC if name.startswith("U-bolts") else C_GRAPH)
        return col, "metal" if name.startswith("U-bolts") else "painted", grp, (620, s * 700, 0)
    if name.startswith(("Lower yoke",)):
        return C_GRAPH, "painted", grp, (620, 0, -60)
    if name.startswith(("Upper yoke",)):
        return C_GRAPH, "painted", grp, (620, 0, 80)
    if name.startswith(("Bulkhead", "Axle beam plate")):
        return C_GRAPH, "painted", grp, (620, 0, 0)
    if name.startswith("Central head tube"):
        return C_GRAPH, "painted", grp, (260, 0, 160)
    if name.startswith("Central headset"):
        return C_STEEL, "metal", grp, (260, 0, 160)
    if name.startswith("Steering column"):
        return C_STEEL, "metal", grp, (260, 0, 320)
    if name.startswith("Drop arm"):
        return C_GRAPH, "painted", grp, (620, 0, -300)
    if name.startswith(("Tie rod", "Drag link", "Rod end bolts")):
        return C_ZINC, "metal", grp, (620, 0, -300)
    if name.startswith("Spacer washers, box"):
        return C_GRAPH, "painted", grp, (620, 0, 0)
    if name.startswith("Bolt:"):
        e = (0, 0, 0) if grp == "internal" else (620, 0, 0)
        return C_ZINC, "metal", grp, e
    return C_GRAPH, "painted", grp, (0, 0, 0)


# ---------------------------------------------------------------- parts
def product_parts(P=PARAMS, with_rider=True):
    si = P["SPINE_IN"]; st = P["STAY_IN"]; kp = P["KP_X"]; WB = P["WB"]; tr = P["TRACK"] / 2
    R = P["WHEEL_R"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ============================================================ 1, 2, 4 rear frame (core module)
    # Every plate, spacer, tube and bolt set is the constructable part from model.build_components()
    # (FTK-DDR-003), so the renders show the design as it will be cut and bolted.
    MC = _model_components()
    for name, c in MC.items():
        sty = _style(name, c)
        if sty is not None and sty[2] == "internal":
            add(name, c.shape, sty[0], sty[1], c.bom, "internal", sty[3])
    # part-number decal on each side plate (thin raised parts)
    dec = []
    ink = []
    for s in (1, -1):
        yo = s * (si + T + 0.2)
        dec.append(_box(887, yo, 505, 90, 0.4, 30))
        ink += [_box(864, yo + s * 0.25, 510, 34, 0.3, 9), _box(904, yo + s * 0.25, 512, 36, 0.3, 4),
                _box(887, yo + s * 0.25, 497, 76, 0.3, 3)]
    add("Spine decal", _comp(dec), C_LABEL, "paper", 1, "internal", (0, 0, 0))
    add("Spine decal print", _comp(ink), C_INK, "paper", 1, "internal", (0, 0, 0))

    # ============================================================ 7 rear wheel (core)
    rw = _wheel(0, 0, R, 50, 2 * st, rear=True)
    ER = (-620, 0, 0)
    add("Rear tyre, 20 x 2.125 in", rw["tyre"], C_TYRE, "rubber", 7, "internal", ER)
    add("Rear tyre tread", rw["tread"], C_TYRE, "rubber", 7, "internal", ER)
    add("Rear rim", rw["rim"], C_RIM, "metal", 7, "internal", ER)
    add("Rear spokes", rw["spokes"], C_SPOKE, "metal", 7, "internal", ER)
    add("Rear 3-speed hub shell", rw["hub"], C_STEEL, "metal", 7, "internal", ER)
    add("Rear drum brake", rw["drum"], C_STEEL, "metal", 7, "internal", ER)
    add("Rear brake plate and arm", rw["brake"], C_FORK, "painted", 7, "internal", ER)
    add("Rear axle nuts", rw["axle"], C_ZINC, "metal", 7, "internal", ER)
    add("Hub gear click box", rw["clickbox"], C_FORK, "plastic", 7, "internal", ER)

    # ============================================================ 8 drivetrain (core)
    bx, bz = P["BB_X"], P["BB_Z"]; cy = P["CHAINLINE"]
    r_ring = P["RING_T"] * 12.7 / (2 * math.pi); r_spr = P["SPROCKET_T"] * 12.7 / (2 * math.pi)
    ED = (0, 0, -520)
    add("Bottom bracket spindle", _ycyl(bx, 0, bz, 8.0, 124), C_STEEL, "metal", 8, "internal", ED)
    ring = Pos(bx, 0, bz) * _teeth(r_ring, P["RING_T"], y=cy)
    ring -= _ycyl(bx, cy, bz, r_ring - 14, 6)
    so_ = math.copysign(1.0, cy)          # outboard of the chain line
    spider = _ycyl(bx, cy + so_ * 3, bz, 20, 6)
    for k in range(5):
        a = math.radians(90 + 72 * k)
        spider += _rod((bx, cy + so_ * 3, bz), (bx + (r_ring - 10) * math.cos(a), cy + so_ * 3, bz + (r_ring - 10) * math.sin(a)), 6.0)
        spider += _ycyl(bx + (r_ring - 10) * math.cos(a), cy + so_ * 2, bz + (r_ring - 10) * math.sin(a), 5.0, 6)
    add("Chainring, 32T", ring, C_STEEL, "metal", 8, "internal", ED)
    add("Crank spider", spider, "#2A2E34", "metal", 8, "internal", ED)
    guard = _ycyl(bx, cy + so_ * 9, bz, r_ring + 16, 2.5) - _ycyl(bx, cy + so_ * 9, bz, r_ring + 7, 4)
    add("Chain guard ring, flat-cut", guard, C_TEAL, "painted", 8, "internal", (0, so_ * 60, -520))
    spr = Pos(0, 0, R) * _teeth(r_spr, P["SPROCKET_T"], depth=3.8, y=cy)
    spr -= _ycyl(0, cy, R, 16, 6)
    add("Rear sprocket, 24T", spr, C_STEEL, "metal", 8, "internal", ER)
    # roller chain: straight runs of rollers and side plates, plus wraps round the ring and sprocket
    rollers, plates_ = [], []

    def run(p0, p1):
        (x0, z0), (x1, z1) = p0, p1
        L = math.hypot(x1 - x0, z1 - z0)
        nlink = int(L / 12.7)
        for k in range(nlink + 1):
            t = k / max(nlink, 1)
            rollers.append(_ycyl(x0 + (x1 - x0) * t, cy, z0 + (z1 - z0) * t, 3.8, 8.0))
        for sy in (-1, 1):
            plates_.append(_rod((x0, cy + sy * 4.8, z0), (x1, cy + sy * 4.8, z1), 3.6))

    def wrap(xc, zc, r, a0, a1):
        m = int(abs(a1 - a0) / 360 * 2 * math.pi * r / 12.7)
        for k in range(m + 1):
            a = math.radians(a0 + (a1 - a0) * k / max(m, 1))
            rollers.append(_ycyl(xc + r * math.cos(a), cy, zc + r * math.sin(a), 3.8, 8.0))
        for sy in (-1, 1):
            plates_.append(_arc_band(xc, cy + sy * 4.8, zc, r - 3.6, r + 3.6, 1.4, a0, a1))

    run((0, R + r_spr), (bx, bz + r_ring))
    run((0, R - r_spr), (bx, bz - r_ring))
    wrap(bx, bz, r_ring, -89, 89)
    wrap(0, R, r_spr, 91, 269)
    add("Roller chain", _comp(rollers + plates_), C_CHAIN, "metal", 8, "internal", (0, 0, -260))
    # cranks and pedals at the model.py crank angle (55 deg)
    ca = math.radians(55)
    cranks, pedals, pins = [], [], []
    for s in (1, -1):
        tip = (bx + s * P["CRANK"] * math.cos(ca), s * 72, bz - s * P["CRANK"] * math.sin(ca))
        d = (tip[0] - bx, tip[2] - bz)
        L = math.hypot(*d); ux, uz = d[0] / L, d[1] / L; nx, nz = -uz, ux
        prof = [(bx + nx * 17, bz + nz * 17), (tip[0] + nx * 11, tip[2] + nz * 11),
                (tip[0] - nx * 11, tip[2] - nz * 11), (bx - nx * 17, bz - nz * 17)]
        fc = Face(Wire.make_polygon([Vector(u, s * 72 - 7, v) for u, v in prof], close=True))
        arm = extrude(fc, amount=14, dir=(0, 1, 0))
        arm = _fillet_try(arm, arm.edges().filter_by(Axis.Y), [6.0, 4.0])
        arm += _ycyl(bx, s * 72, bz, 17, 14) + _ycyl(tip[0], s * 72, tip[2], 11, 14)
        cranks.append(arm)
        body = _box(tip[0], s * 110, tip[2], 100, 90, 18)
        body = _fillet_try(body, body.edges().filter_by(Axis.Y), [5.0, 3.0])
        body -= _box(tip[0], s * 110, tip[2], 70, 96, 10)
        body += _ycyl(tip[0], s * 110, tip[2], 7, 92)
        pedals.append(body)
        for px in (-40, -14, 14, 40):
            for py in (-30, 0, 30):
                pins.append(_zcyl(tip[0] + px, s * 110 + py, tip[2] + 10.5, 1.6, 3.0))
    add("Cranks, 170 mm", _comp(cranks), "#C0C5CB", "metal", 8, "internal", ED)
    add("Platform pedals", _comp(pedals), C_FORK, "plastic", 8, "internal", (0, 0, -560))
    add("Pedal pins", _comp(pins), C_ZINC, "metal", 8, "internal", (0, 0, -560))

    # ============================================================ 3, 5 front bed, knuckle posts and steering (shell)
    # From model.build_components(): yokes clamping the head tube, bulkhead, rails, axle beams, knuckle posts
    # with their collar plates and steering lock stops, head tubes and headsets, steering column, drop arm,
    # drag link, tie rod, forks, U-bolts, clamp plates and steering arms, and every bolt set.
    for name, c in MC.items():
        sty = _style(name, c)
        if sty is not None and sty[2] == "shell":
            add(name, c.shape, sty[0], sty[1], c.bom, "shell", sty[3])
    for s, side in ((1, "left"), (-1, "right")):
        cyw = s * tr
        EW = (620, s * 700, 0)
        fw = _wheel(WB, cyw, R, 45, P["FORK_OLD"])
        # drums on the outboard side of each front wheel
        add(f"Front tyre, {side}", fw["tyre"], C_TYRE, "rubber", 6, "shell", EW)
        add(f"Front tyre tread, {side}", fw["tread"], C_TYRE, "rubber", 6, "shell", EW)
        add(f"Front rim, {side}", fw["rim"], C_RIM, "metal", 6, "shell", EW)
        add(f"Front spokes, {side}", fw["spokes"], C_SPOKE, "metal", 6, "shell", EW)
        add(f"Front hub, {side}", fw["hub"], C_STEEL, "metal", 6, "shell", EW)
        add(f"Front drum brake, {side}", fw["drum"], C_STEEL, "metal", 6, "shell", EW)
        add(f"Front brake plate and arm, {side}", fw["brake"], C_FORK, "painted", 6, "shell", EW)
        add(f"Front axle nuts, {side}", fw["axle"], C_ZINC, "metal", 6, "shell", EW)
        mg = _arc_band(WB, cyw, R, R + 8, R + 10.5, 62, 20, 160)
        add(f"Front mudguard, {side}", mg, C_FORK, "plastic", 14, "accessory", (620, s * 700, 120))

    # ============================================================ 9 cargo box (shell)
    x0 = P["BOX_X0"]; x1 = x0 + P["BOX_L"]; yb_ = P["BOX_W"] / 2; z0 = P["BOX_Z0"]; z1 = z0 + P["BOX_H"]
    w = P["PLY_WALL"]
    EX = (620, 0, 760)
    cb = _box((x0 + x1) / 2, 0, (z0 + z1) / 2, x1 - x0, 2 * yb_, z1 - z0)
    cb = _fillet_try(cb, cb.edges().filter_by(Axis.Z), [8.0, 5.0, 3.0])
    cb -= _box((x0 + x1) / 2, 0, (z0 + z1) / 2 + P["PLY_FLOOR"] / 2 + 0.5, x1 - x0 - 2 * w, 2 * yb_ - 2 * w,
               z1 - z0 - P["PLY_FLOOR"] + 1)
    # panel joint grooves (plywood panels meeting at the floor line)
    cb -= _box((x0 + x1) / 2, 0, z0 + P["PLY_FLOOR"], x1 - x0 + 2, 2 * yb_ + 2, 1.2) - \
        _box((x0 + x1) / 2, 0, z0 + P["PLY_FLOOR"], x1 - x0 - 2, 2 * yb_ - 2, 2)
    add("Cargo box, plywood", cb, C_WOOD, "wood", 9, "shell", EX)
    lid = _box((x0 + x1) / 2, 0, z1 + w / 2, x1 - x0, 2 * yb_, w)
    lid = _fillet_try(lid, lid.edges().filter_by(Axis.Z), [8.0, 5.0])
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Z)[-1].edges(), [2.5, 1.5])
    add("Counter lid, plywood", lid, C_WOOD2, "wood", 9, "shell", (620, 0, 1020))
    hw = []
    for yh in (-170, 170):
        hw.append(_box(x0 - 1.2, yh, z1 - 4, 2.4, 70, 40))
        hw.append(Pos(x0 - 4, yh, z1 + 1) * Rot(90, 0, 0) * Cylinder(4, 70))
    add("Lid hinges", _comp(hw), C_ZINC, "metal", 9, "shell", EX)
    hasp = [_box(x1 + 1.2, 0, z1 - 20, 2.4, 34, 60), _box(x1 + 1.2, 0, z1 + 6, 2.4, 40, 12)]
    add("Hasp", _comp(hasp), C_ZINC, "metal", 9, "shell", EX)
    lock = _box(x1 + 14, 0, z1 - 52, 20, 40, 34)
    lock = _fillet_try(lock, lock.edges().filter_by(Axis.X), [5.0, 3.0])
    shackle = (Pos(x1 + 14, 0, z1 - 35) * Rot(90, 0, 0) * (Cylinder(14, 5) - Cylinder(10, 6))) & \
        _box(x1 + 14, 0, z1 - 20, 40, 10, 30)
    add("Padlock body", lock, C_BRASS, "metal", 9, "shell", EX)
    add("Padlock shackle", shackle, C_STEEL, "metal", 9, "shell", EX)
    bumpers = []
    for (xc, sx) in ((x0, -1), (x1, 1)):
        for sy in (-1, 1):
            b = _box(xc + sx * 3, sy * (yb_ + 3), (z0 + z1) / 2, 40, 40, z1 - z0 - 20) & \
                _box(xc + sx * 3 - sx * 16, sy * (yb_ + 3 - 16), (z0 + z1) / 2, 46, 46, z1 - z0)
            b = b - _box(xc - sx * 30, sy * (yb_ - 30), (z0 + z1) / 2, 60, 60, z1 - z0 + 2)
            b = _fillet_try(b, b.edges().filter_by(Axis.Z), [4.0, 2.0, 1.0])
            bumpers.append(b)
    add("Rubber corner bumpers", _comp(bumpers), C_RUBBER, "rubber", 14, "accessory", EX)
    plate_ = _box(x1 + 0.3, -yb_ / 2 - 20, z0 + 250, 0.6, 150, 40)
    add("Box name plate", plate_, C_TEAL, "painted", 14, "accessory", EX)
    pr = [_box(x1 + 0.7, -yb_ / 2 - 50, z0 + 255, 0.4, 70, 12), _box(x1 + 0.7, -yb_ / 2 + 25, z0 + 255, 0.4, 40, 12),
          _box(x1 + 0.7, -yb_ / 2 - 20, z0 + 238, 0.4, 120, 4)]
    add("Box name plate print", _comp(pr), C_LABEL, "paper", 14, "accessory", EX)
    refl = [_on((x1, sy * (yb_ - 40), z0 + 60), (1, 0, 0), Pos(0, 0, 1.5) * Cylinder(22, 3)) for sy in (-1, 1)]
    add("Front reflectors", _comp(refl), C_REFL, "plastic", 14, "accessory", EX)

    # ============================================================ 10 seat (shell)
    zs = P["SADDLE_TOP"]; xs = seat_xy(zs - 25)
    ESt = (0, 0, 460)
    post = _rod((seat_xy(700), 0, 700), (seat_xy(zs - 60), 0, zs - 60), 13.6)
    add("Seatpost, 27.2 mm", post, C_STEEL, "metal", 10, "shell", ESt)
    for name in ("Seat tube", "Seat tube shaft collars"):
        add(name, MC[name].shape, C_GRAPH if name == "Seat tube" else C_ZINC, "painted" if name == "Seat tube" else "metal",
            10, "shell", ESt)
    clamp = _box(seat_xy(zs - 60), 0, zs - 60, 40, 30, 22)
    clamp = _fillet_try(clamp, clamp.edges().filter_by(Axis.Y), [4.0, 2.0])
    rails = [_rod((xs - 90, sy * 35, zs - 48), (xs + 70, sy * 22, zs - 42), 3.5) for sy in (-1, 1)]
    springs = []
    for sy in (-1, 1):
        for k in range(5):
            springs.append(Pos(xs - 80, sy * 42, zs - 76 + 7 * k) * Torus(9, 2.2))
        springs.append(_rod((xs - 80, sy * 42, zs - 80), (seat_xy(zs - 60) - 10, sy * 20, zs - 62), 3.0))
    add("Saddle clamp, rails and springs", _comp([clamp] + rails + springs), C_FORK, "metal", 10, "shell",
        (0, 0, 520))
    so = [(xs - 130, -80), (xs - 30, -82), (xs + 60, -40), (xs + 130, -24), (xs + 130, 24), (xs + 60, 40),
          (xs - 30, 82), (xs - 130, 80)]
    fc = Face(Wire.make_polygon([Vector(u, v, zs - 50) for u, v in so], close=True))
    saddle = extrude(fc, amount=50, dir=(0, 0, 1))
    saddle = _fillet_try(saddle, saddle.edges().filter_by(Axis.Z), [20.0, 12.0, 8.0])
    saddle = _fillet_try(saddle, saddle.faces().sort_by(Axis.Z)[-1].edges(), [16.0, 12.0, 8.0, 4.0])
    add("Sprung saddle", saddle, C_RUBBER, "rubber", 10, "shell", (0, 0, 580))
    seam = extrude(Face(Wire.make_polygon([Vector(u, v * 1.01, zs - 51) for u, v in so], close=True)),
                   amount=3, dir=(0, 0, 1))
    seam = _fillet_try(seam, seam.edges().filter_by(Axis.Z), [20.0, 12.0, 8.0])
    add("Saddle base seam", seam, "#3A3F46", "plastic", 10, "shell", (0, 0, 580))

    # ============================================================ 11 handlebar and 12 brakes (shell)
    EH = (200, 0, 560)
    stem = _rod((kp, 0, 830), (930, 0, 850), 14)
    sc = _box(930, 0, 850, 34, 50, 34)
    sc = _fillet_try(sc, sc.edges().filter_by(Axis.Y), [8.0, 5.0])
    stem += sc + _zcyl(kp, 0, 830, 17, 34)
    add("Stem", stem, C_FORK, "painted", 11, "shell", EH)
    bar = _rod((930, -290, 850), (930, 290, 850), 11) + Pos(930, 290, 850) * Sphere(11) + \
        Pos(930, -290, 850) * Sphere(11)
    bar += _rod((930, 290, 850), (885, 320, 850), 11) + _rod((930, -290, 850), (885, -320, 850), 11)
    add("Riser handlebar", bar, "#C0C5CB", "metal", 11, "shell", EH)
    grips = []
    for s in (1, -1):
        a = Vector(924, s * 294, 850); b = Vector(885, s * 320, 850)
        dvec = b - a; L = dvec.length
        g = Solid.make_cylinder(16, L + 20, Plane(origin=a - dvec.normalized() * 8, z_dir=dvec.normalized()))
        for k in range(1, 9):
            ctr = a - dvec.normalized() * 8 + dvec.normalized() * ((L + 20) * k / 9)
            g -= _on(ctr, dvec.normalized(), Torus(16.4, 1.1))
        grips.append(g)
    add("Rubber grips", _comp(grips), C_RUBBER, "rubber", 11, "shell", EH)
    levers = []
    for s in (1, -1):
        clampb = Pos(918, s * 250, 850) * Rot(0, 90, 90) * (Cylinder(15, 18))
        body = _box(918, s * 262, 866, 38, 28, 22)
        body = _fillet_try(body, body.edges(), [5.0, 3.0])
        blade = _rod((925, s * 262, 862), (880, s * 330, 842), 5.5)
        levers += [clampb, body, blade]
    latch = _box(918, 208, 870, 26, 18, 26)
    latch = _fillet_try(latch, latch.edges(), [4.0, 2.0])
    add("Brake levers", _comp(levers), C_FORK, "plastic", 12, "shell", EH)
    add("Parking latch", latch, C_TEAL, "plastic", 12, "shell", EH)
    bell = _zcyl(930, 70, 872, 26, 3) + Pos(930, 70, 872) * Sphere(26) & _box(930, 70, 890, 60, 60, 36)
    add("Bell", bell, "#C0C5CB", "metal", 14, "accessory", EH)
    lab = (Pos(930, -60, 850) * Rot(90, 0, 0) * (Cylinder(11.4, 70) - Cylinder(10.5, 72)))
    add("Cornering-speed label (6 km/h)", lab, "#F59E0B", "paper", 14, "accessory", EH)
    cables = [
        _rod((918, 262, 862), (900, 60, 640), 3), _rod((900, 60, 640), (880, 40, 560), 3),
        _rod((880, 40, 560), (60, 64, 340), 3),
        _rod((918, -262, 862), (1040, -180, 600), 3), _rod((1040, -180, 600), (1040, -180, 270), 3),
        _rod((1040, -180, 270), (WB - 60, -180, 270), 3),
        _rod((WB - 60, -tr + 50, 270), (WB - 60, tr - 50, 270), 3),
    ]
    # long cable runs sit in "context" so they show in the assembled hero but do not cross the exploded view
    add("Brake cable runs and housing", _comp(cables), C_FORK, "plastic", 12, "context", (0, 0, 0))

    rmg = _arc_band(0, 0, R, R + 8, R + 10.5, 64, 70, 200)
    add("Rear mudguard", rmg, C_FORK, "plastic", 14, "accessory", (-620, 0, 160))
    rr = _box(-252, 0, R + 90, 6, 40, 70)
    rr = _fillet_try(rr, rr.edges().filter_by(Axis.X), [4.0, 2.0])
    add("Rear reflector", rr, C_RED, "plastic", 14, "accessory", (-620, 0, 160))

    # ============================================================ context: crate and rider
    cx0 = x0 + 470; cw_, cd_, ch_ = 520, 360, 250
    cz0 = z1 + w
    crate = _box(cx0, 0, cz0 + ch_ / 2, cw_, cd_, ch_)
    crate = _fillet_try(crate, crate.edges().filter_by(Axis.Z), [18.0, 12.0])
    crate -= _box(cx0, 0, cz0 + ch_ / 2 + 8, cw_ - 14, cd_ - 14, ch_)
    for k in range(6):
        for zz in (cz0 + 60, cz0 + 150):
            crate -= _box(cx0 - 200 + 80 * k, 0, zz, 44, cd_ + 10, 56)
    for k in range(4):
        for zz in (cz0 + 60, cz0 + 150):
            crate -= _box(cx0, -120 + 80 * k, zz, cw_ + 10, 44, 56)
    crate -= _box(cx0, 0, cz0 + ch_ - 30, 140, cd_ + 10, 30)
    add("Produce crate (cargo)", crate, C_CRATE, "plastic", None, "context", (0, 0, 0))
    strap = [_box(cx0 + 120, 0, cz0 + ch_ + 1.5, 38, cd_ + 6, 3)]
    for sy in (-1, 1):
        strap.append(_box(cx0 + 120, sy * (cd_ / 2 + 1.5), cz0 + ch_ / 2, 38, 3, ch_))
        strap.append(_box(cx0 + 120, sy * (cd_ / 2 + 22), z1 + w + 1.5, 38, 40, 3))
    add("Cargo strap", _comp(strap), C_STRAP, "fabric", None, "context", (0, 0, 0))
    buckle = _box(cx0 + 120, -(cd_ / 2 + 4), cz0 + 120, 46, 4, 30) - _box(cx0 + 120, -(cd_ / 2 + 4), cz0 + 120, 30, 6, 16)
    add("Strap buckle", buckle, C_ZINC, "metal", None, "context", (0, 0, 0))

    if with_rider:
        from context_parts import mannequin
        H = 1760.0
        seat_w = (xs - 55, 0.0, zs)
        grips_w = [(904, 307, 850), (904, -307, 850)]
        ped = []
        for s in (1, -1):
            tip_ = (bx + s * P["CRANK"] * math.cos(ca), bz - s * P["CRANK"] * math.sin(ca))
            ped.append((tip_[0] + 10, s * 88.0, tip_[1] + 10))
        joints, (tx, ty, tz) = _fit_rider(H, seat_w, grips_w, ped)
        rider = Pos(tx, ty, tz) * Rot(0, 0, 90) * mannequin(H, "ride", head_tilt=-22, **joints)
        add("Rider, 1.76 m (clay mannequin)", rider, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    ps = product_parts()
    for p in ps:
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid}")
    print(len(ps), "parts", round(time.time() - t0, 1), "s")
