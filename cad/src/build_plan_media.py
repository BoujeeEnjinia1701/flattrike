"""FlatTrike prototype build plan pictures (FTK-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...] [only=N,N]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/FTK-DWG-101 to 124        making sketches for the made, cut and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as M  # noqa: E402

import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402

# ------------------------------------------------- leader lines that end on a part you can see
# The kit puts a leader on a vertex of the part, which can be hidden behind a nearer part. This
# script wraps the kit's rasterizer to draw a second, flat "which part is here" image, then ends
# each leader on a visible pixel of its own part, as near as possible to the kit's choice and
# well inside the part's visible area.
_raster_kit = bv._raster
_VIS = {}
_BADGE_BESIDE_SMALL = False


class _Px(np.ndarray):
    pass


def _raster_visible(items, elev, azim, W, H, ss=2):
    img, proj, verts = _raster_kit(items, elev, azim, W, H, ss)
    tris, cols, ids = [], [], []
    for k, (p, color, alpha, off) in enumerate(items):
        v, t = bv._tris(p.shape)
        tri = (v + np.asarray(off, float))[t]
        tris.append(tri); cols.append(np.zeros((len(tri), 4))); ids.append(np.full(len(tri), k))
    _, _, _, idb = bv._zbuffer(np.vstack(tris), np.vstack(cols), elev, azim, W, H, ids=np.concatenate(ids))
    _VIS.clear()
    free = None
    for k, v in enumerate(verts):
        m = idb == k
        if not m.any():
            continue
        x0, y0 = proj(bv._anchor_kit(v))
        inner = ndimage.distance_transform_edt(m)
        best = inner >= min(4.0, inner.max())             # at least 4 px inside the part where it can be
        ys, xs = np.nonzero(best)
        j = np.argmin((xs - x0) ** 2 + (ys - y0) ** 2)
        px_, py_ = xs[j] + 0.5, ys[j] + 0.5
        if _BADGE_BESIDE_SMALL and m.sum() < 1500:      # overview key: a numbered badge would hide a small part,
            if free is None:                              # so it sits in clear space right beside the part instead
                free = ndimage.distance_transform_edt(idb < 0) >= 14
            fy, fx = np.nonzero(free)
            jj = np.argmin((fx - px_) ** 2 + (fy - py_) ** 2)
            px_, py_ = fx[jj] + 0.5, fy[jj] + 0.5
        _VIS[id(v)] = (px_, py_)

    def proj_visible(pts):
        if isinstance(pts, _Px):
            return np.asarray(pts)
        return proj(pts)
    return img, proj_visible, verts


def _anchor_visible(v):
    if id(v) in _VIS:
        return np.asarray(_VIS[id(v)], float).view(_Px)
    return bv._anchor_kit(v)


bv._anchor_kit = bv._anchor
bv._anchor = _anchor_visible
bv._raster = _raster_visible

P = M.P
OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
C = M.build_components()

COL = {"spine": "#64748B", "cover": "#475569", "rib": "#D4A017", "saddle": "#B45309", "uyoke": "#0F766E",
       "lyoke": "#115E59", "ht": "#1F2937", "bb": "#7C3AED", "seat": "#9333EA", "stay": "#94A3B8", "bridge": "#CA8A04",
       "spacer": "#A16207", "bulk": "#334155", "rail": "#1D4ED8", "beam": "#2563EB", "post": "#0E7490",
       "cheek": "#155E75", "collar": "#0891B2", "column": "#374151", "drop": "#C2410C", "fork": "#27272A",
       "wheel": "#3F3F46", "arm": "#EA580C", "clamp": "#9A3412", "link": "#DC2626", "drive": "#6D28D9",
       "box": "#C08A4A", "bars": "#2563EB", "bolt": "#111827", "ghost": "#D1D5DB", "stop": "#B91C1C"}
REV2 = ("P2", "Steering lock stop added (decided 2026-10-02, FTK-DEC-001)", "2026-10-02", "AC")
REV_TRAIL = "forks turned to trail (FTK-DEC-001)"
P1 = ("P1", "Making sketch for the prototype build plan", "2026-10-01", "AC")


def S(*names):
    out = None
    for n in names:
        sh = C[n].shape
        out = sh if out is None else out + sh
    return out


def starts(*prefixes):
    return [n for n in C if any(n.startswith(p) for p in prefixes)]


def bolts(*groups):
    return [n for n in C if n.startswith("Bolt:") and any(n.startswith(f"Bolt: {g}") for g in groups)]


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


SIDE = ("left", "right")


# ----------------------------------------------------------------- named groups, in build order
def groups():
    g = {}
    g["spine"] = part("Spine side plates (2)", S("Spine side plate, left", "Spine side plate, right"), COL["spine"])
    g["ribs"] = part("Spine ribs (2)", S("Spine rib at 800", "Spine rib at 900"), COL["rib"])
    g["saddles"] = part("Seat tube saddles (2)", S("Seat tube saddle, lower", "Seat tube saddle, upper"), COL["saddle"])
    g["uyoke"] = part("Upper yoke", C["Upper yoke"].shape, COL["uyoke"])
    g["topc"] = part("Spine top cover", C["Spine top cover"].shape, COL["cover"])
    g["botc"] = part("Spine bottom cover", C["Spine bottom cover"].shape, COL["cover"])
    g["lyoke"] = part("Lower yoke", C["Lower yoke"].shape, COL["lyoke"])
    g["ht"] = part("Central head tube and headset cups", S("Central head tube", "Central headset cups"), COL["ht"])
    g["bb"] = part("Bottom bracket shell and cups", C["Bottom bracket shell and cups"].shape, COL["bb"])
    g["seat"] = part("Seat tube and shaft collars", S("Seat tube", "Seat tube shaft collars"), COL["seat"])
    g["stays"] = part("Rear stay plates (2)", S("Rear stay plate, left", "Rear stay plate, right"), COL["stay"])
    g["bridge"] = part("Stay bridge", C["Stay bridge"].shape, COL["bridge"])
    g["nodes"] = part("Spacer washers, spacer tubes, node bolts", S(*starts("Spacer washer stacks", "Spacer tube", "Bolt: stay node")),
                      COL["spacer"])
    g["bulk"] = part("Bulkhead", C["Bulkhead"].shape, COL["bulk"])
    g["rails"] = part("Bed rails (2)", S("Bed rail, left", "Bed rail, right"), COL["rail"])
    g["beams"] = part("Axle beam plates (2)", S("Axle beam plate, rear", "Axle beam plate, front"), COL["beam"])
    g["posts"] = part("Knuckle posts: plates and cheeks (2 sets)", S(*starts("Knuckle post plate", "Knuckle post inner", "Knuckle post outer")),
                      COL["post"])
    g["stops"] = part("Steering lock stops (2)", S(*starts("Steering lock stop"), *bolts("Steering lock stop")), COL["stop"])
    g["collars"] = part("Knuckle collar plates, head tubes, cups", S(*starts("Knuckle collar plate", "Knuckle head tube", "Knuckle headset")),
                        COL["collar"])
    g["column"] = part("Steering column and drop arm", S("Steering column (cut-down fork and quill stem)", "Drop arm",
                                                          *bolts("drop arm")), COL["drop"])
    g["forks"] = part("Front forks and wheels (2)", S("Front fork, left", "Front fork, right", "Front wheel, left", "Front wheel, right"),
                      COL["fork"])
    g["arms"] = part("Steering arms, clamp plates, U-bolts (2)", S(*starts("Steering arm", "U-bolts", "Bolt: Steering arm")), COL["arm"])
    g["link"] = part("Tie rod and drag link", S("Tie rod with rod ends", "Drag link with rod ends", "Rod end bolts"), COL["link"])
    g["drive"] = part("Rear wheel and drivetrain", S("Rear wheel", "Drivetrain (chainring, cranks, pedals, chain, sprocket)"),
                      COL["drive"])
    g["box"] = part("Cargo box and lid", S("Cargo box", "Cargo box lid", *starts("Spacer washers, box"), *bolts("box", "Box")),
                    COL["box"])
    g["ride"] = part("Seatpost, saddle, handlebar (brakes not shown)", S("Seatpost and saddle", "Handlebar and stem"), COL["bars"])
    return g


ORDER = ["spine", "ribs", "saddles", "uyoke", "topc", "botc", "lyoke", "ht", "bb", "seat", "stays", "bridge", "nodes",
         "bulk", "rails", "beams", "posts", "stops", "collars", "column", "forks", "arms", "link", "drive", "box", "ride"]


# ----------------------------------------------------------------- overview
def overview():
    G = groups()
    off = {"spine": (0, 0, 0), "ribs": (0, 0, 330), "saddles": (-60, 0, 420), "uyoke": (100, 0, 420),
           "topc": (-40, 0, 620), "botc": (0, 0, -300), "lyoke": (100, 0, -420), "ht": (260, 0, -120),
           "bb": (-60, 0, -560), "seat": (-200, 0, 760), "stays": (-520, 0, 0), "bridge": (-700, 0, 420),
           "nodes": (-220, 0, -480), "bulk": (500, 0, 120), "rails": (700, 0, -60), "beams": (900, 0, -380),
           "posts": (950, 0, 230), "stops": (1300, 0, 120), "collars": (1050, 0, 560), "column": (300, 380, -520), "forks": (1350, 0, -520),
           "arms": (1250, 0, -950), "link": (750, 0, -820), "drive": (-850, 0, -520), "box": (800, 0, 900),
           "ride": (150, 0, 1150)}
    parts = []
    for k in ORDER:
        p = G[k]; p.explode = off[k]; parts.append(p)
    global _BADGE_BESIDE_SMALL
    _BADGE_BESIDE_SMALL = True
    return bv.overview(parts, OUT / "overview.png", "FlatTrike prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above. The bolts that join the plates are not shown",
                       elev=16, azim=-62, size=(13, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


def turn(shape):
    """A transverse (YZ) plate turned so its face shows in the front view."""
    import build123d as b
    return b.Rot(0, 0, -90) * shape


def joint_text(name):
    """Count the tabs, slots, bolt holes and T-slots on a plate from the model's joint list."""
    tabs = sum(j["tabs"] for j in M.JOINTS if j["edge"] == name)
    tslots = sum(j["bolts"] for j in M.JOINTS if j["edge"] == name and j["kind"] != "through")
    slots = sum(j["tabs"] for j in M.JOINTS if j["face"] == name)
    holes = sum(j["bolts"] for j in M.JOINTS if j["face"] == name and j["kind"] != "through")
    return tabs, tslots, slots, holes


def cutnote(name):
    tabs, tslots, slots, holes = joint_text(name)
    bits = []
    if tabs:
        bits.append(f"{tabs} tabs")
    if tslots:
        bits.append(f"{tslots} T-slots")
    if slots:
        bits.append(f"{slots} slots")
    if holes:
        bits.append(f"{holes} bolt holes 9 mm")
    return ", ".join(bits)


TSLOT = "T-slot: 9 mm wide, 23 deep, with a 13.6 x 8.4 mm window 10 mm in for the nut."
CUT = "Laser or waterjet cut from 3 mm S235JR or A36 steel, from the model's outline."
MAT = "3 mm S235JR or A36 steel plate, laser or waterjet cut"


def sheets(only=None):
    import build123d as b
    G = groups()
    base = dict(project="FlatTrike", date=DATE)
    out = []
    ghost = lambda *ks: [G[k] for k in ks]  # noqa: E731

    def others(exclude, *prefixes):
        """Grey neighbours: every component starting with a prefix, except the part itself."""
        return [Part(n, C[n].shape, COL["ghost"]) for n in C if n != exclude and any(n.startswith(p) for p in prefixes)]
    tdir, wdir = M.seat_axes()

    def sheet(no, *a, **k):
        if only and no not in only:
            return
        out.append(bv.component_sheet(*a, dwg_no=f"FTK-DWG-{no}", **{**base, **k}))

    sp = C["Spine side plate, left"].shape
    sheet(101, Part("Spine side plate", sp, COL["spine"]), ghost("ribs", "saddles", "uyoke", "topc", "botc", "lyoke", "stays"),
          title="FlatTrike spine side plate (make 2, left and right): making sketch", material=MAT,
          inset_view=(15, 70),
          notes=["Make 2. The right plate is the left plate turned over: cut both from one file.",
                 f"Outline about {M.PLATES[0]['size'][0]:.0f} x {M.PLATES[0]['size'][1]:.0f} mm; front edge vertical, 210 mm deep at the head tube.",
                 "Holes: bottom bracket 35.5 mm; four 9 mm stay bolt holes; 9 mm bolt holes",
                 "  for the ribs, saddles and upper yoke.",
                 "Two lightening windows (rear and in the bottom bracket lobe).",
                 f"Top edge: {sum(1 for k, _ in M.ST_TOP if k == 'tab')} tabs into the top cover, {sum(1 for k, _ in M.ST_TOP if k == 'bolt')} T-slots between.",
                 f"Bottom edges: {sum(1 for k, _ in M.ST_BOT if k == 'tab') + 1} tabs into the bottom cover and lower yoke, {sum(1 for k, _ in M.ST_BOT if k == 'bolt') + 1} T-slots.",
                 "Inside face: slots for the two ribs, two seat tube saddles, upper yoke.",
                 TSLOT,
                 "Deburr every edge, slot and window. Keep the tabs square.",
                 "Fit: the plates stand 60 mm apart (inside faces), joined by the ribs,",
                 "  saddles and yokes; the covers close the box top and bottom.",
                 "Check: a scrap of 3 mm plate slides into every slot by hand."])
    tc = C["Spine top cover"].shape
    (x0, z0), (x1, z1) = M.SPINE[0], M.SPINE[1]
    L = math.hypot(x1 - x0, z1 - z0); d = ((x1 - x0) / L, 0, (z1 - z0) / L)
    sheet(102, Part("Spine top cover", tc, COL["cover"]), ghost("spine", "seat"),
          title="FlatTrike spine top cover: making sketch", material=MAT,
          view_shape=flat(tc, (x0, 0, z0), d, (-d[2], 0, d[0])), inset_view=(30, -60),
          notes=[f"Strip {L:.0f} x 90 mm. It lies on the side plates' top edges and overhangs",
                 "  each plate by 12 mm.",
                 "Two rows of slots 33 mm each side of the centre line: the side plates'",
                 "  tabs come up through them. In the front 280 mm (the closed box)",
                 "  the slots are 22 mm apart: they carry the twisting load.",
                 f"Bolt holes 9 mm between slots ({cutnote('Spine top cover')}).",
                 "Oval hole for the seat tube, 34 x 45 mm, about 100 mm from the rear end.",
                 "Fit: drop it onto the tabs, then M8 x 25 bolts down into the side plates'",
                 "  T-slots with a locknut in each window.",
                 "Check: every tab shows through its slot and sits flush or just proud."])
    bc = C["Spine bottom cover"].shape
    sheet(103, Part("Spine bottom cover", bc, COL["cover"]), ghost("spine", "lyoke"),
          title="FlatTrike spine bottom cover: making sketch", material=MAT,
          view_shape=flat(bc, (720, 0, 457), (0.7746, 0, -0.6325), (-0.6325, 0, -0.7746)), inset_view=(-40, -95),
          notes=["Strip 220 x 90 mm under the sloping bottom edges of the side plates,",
                 "  between the bottom bracket lobe and the lower yoke.",
                 f"Two rows of slots 33 mm each side of the centre line; {cutnote('Spine bottom cover')}.",
                 "Fit: hold it up onto the tabs; M8 x 25 bolts up into the side plates'",
                 "  T-slots, locknuts in the windows.",
                 "With the top cover it closes the spine into a box (torsion: FTK-CAL-001).",
                 "Check: no gap between the cover and the plate edges."])
    r8, r9 = C["Spine rib at 800"].shape, C["Spine rib at 900"].shape
    rside = [Part("Right spine side plate", C["Spine side plate, right"].shape, COL["ghost"])]
    sheet(104, Part("Spine ribs", r8 + r9, COL["rib"]), rside,
          title="FlatTrike spine ribs (make 1 of each): making sketch", material=MAT,
          view_shape=turn(r8 + b.Pos(-100, 90, 0) * r9),
          inset_view=(15, 70),
          notes=["Two ribs, both 60 mm wide plus a tab each side: rib A (at 800 mm from",
                 "  the rear axle, left in the sketch) 197 mm tall, rib B (at 900 mm) 233 mm tall.",
                 "Each long edge: two tabs into the side plate slots and one T-slot",
                 "  between them for an M8 bolt from outside the spine.",
                 TSLOT,
                 "Fit: the ribs stand square across the spine, 5 mm clear of both covers.",
                 "Mark each rib A or B with a paint pen; they are not interchangeable.",
                 "Check: the rib sits square in the side plate slots."])
    sd = C["Seat tube saddle, lower"].shape
    c0 = (M.seat_xy(P["SADDLE_Z"][0]), 0.0, P["SADDLE_Z"][0])
    sheet(105, Part("Seat tube saddle", sd, COL["saddle"]), rside + [Part("Seat tube", C["Seat tube"].shape, COL["ghost"])],
          title="FlatTrike seat tube saddle (make 2): making sketch", material=MAT,
          view_shape=flat(sd, c0, wdir, tdir), inset_view=(15, 70),
          notes=["Make 2, identical. Plate 92 x 60 mm with a 32.8 mm hole in the middle",
                 "  for the 31.8 mm seat tube.",
                 "Each 92 mm edge: a tab in the middle and a T-slot 30 mm either side.",
                 TSLOT,
                 "Fit: the saddles sit across the spine at right angles to the 73 degree",
                 "  seat line, 100 mm apart along it; the seat tube passes through both",
                 "  and a shaft collar bears on the outside face of each.",
                 "Check: the seat tube slides through both saddles without binding."])
    uy = C["Upper yoke"].shape
    sheet(106, Part("Upper yoke", uy, COL["uyoke"]), rside + ghost("ht", "bulk"),
          title="FlatTrike upper yoke: making sketch", material=MAT, inset_view=(30, -55),
          notes=["Flat plate 150 mm long, 60 mm wide at the back (it fits between the",
                 "  side plates), 400 mm wide at the front where it meets the bulkhead.",
                 "Hole 34.5 mm, 90 mm from the back edge: the headset cup spigot.",
                 f"Back edges: one tab and one T-slot each side. Front edge: {joint_text('Upper yoke')[0] - 2} tabs",
                 f"  and {joint_text('Upper yoke')[1] - 2} T-slots into the bulkhead.",
                 TSLOT,
                 "Fit: it lies flat on top of the head tube; the upper headset cup's flange",
                 "  holds it down on the tube end.",
                 "Check: the hole is 90.0 mm from the back edge, give or take 0.5 mm."])
    ly = C["Lower yoke"].shape
    sheet(107, Part("Lower yoke", ly, COL["lyoke"]), ghost("spine", "ht", "bulk", "rails"),
          title="FlatTrike lower yoke: making sketch", material=MAT, inset_view=(-30, -55),
          notes=["Flat plate 160 mm long, 90 mm wide at the back, 474 mm wide at the",
                 "  front where it meets the bulkhead and the two rails.",
                 "Hole 34.5 mm, 100 mm from the back edge: the lower headset cup spigot.",
                 "Back part: a slot (a side plate's tab) and a 9 mm bolt hole each side,",
                 "  33 mm from the centre line. Front edge: 4 tabs and 3 T-slots into the bulkhead.",
                 TSLOT,
                 "Fit: it lies flat under the side plates' level bottom edges and under",
                 "  the head tube; the lower cup's flange holds it up against the tube.",
                 "Check: the hole lines up with the upper yoke's hole (plumb line)."])
    st = C["Rear stay plate, left"].shape
    sheet(108, Part("Rear stay plate", st, COL["stay"]), ghost("spine", "bridge", "drive"),
          title="FlatTrike rear stay plate (make 2, left and right): making sketch", material=MAT,
          inset_view=(20, -60),
          notes=["Make 2. The right plate is the left plate turned over.",
                 "Outline about 745 x 555 mm with one window.",
                 "Rear dropout: an open slot 10 mm wide and 53 mm long cut into the",
                 "  rear edge, 254 mm up; the hub axle slides in from behind.",
                 "Four 9 mm holes for the stay-to-spine bolts; a slot pair and a 9 mm",
                 "  hole for the stay bridge (inside face).",
                 "Fit: the plates stand 120 mm apart (the hub's width over locknuts),",
                 "  27 mm outside the spine, held by four through-bolts.",
                 "Check: a 10 mm bar slides the full length of the dropout slot."])
    sb = C["Stay bridge"].shape
    sheet(109, Part("Stay bridge", sb, COL["bridge"]), [Part("Right stay", C["Rear stay plate, right"].shape, COL["ghost"]),
                                                       Part("Rear wheel", C["Rear wheel"].shape, COL["ghost"])],
          title="FlatTrike stay bridge: making sketch", material=MAT, view_shape=turn(sb),
          inset_view=(15, 70),
          notes=["Plate 120 x 80 mm plus a tab each side.",
                 "Each 80 mm edge: two tabs and a T-slot between them.",
                 TSLOT,
                 "Fit: across the stays 200 mm ahead of the rear axle, 480 to 560 mm up;",
                 "  it braces the stays' upper strips against buckling (FTK-CAL-001).",
                 "Check: the stays stand parallel, 120 mm apart, with the bridge fitted."])
    ws = b.Pos(0, 0, 0) * M.tube((0, 0, 0), (0, 3, 0), 8.0, 4.25) + M.tube((40, 0, 0), (40, 60, 0), 8.0, 6.0)
    sheet(110, Part("Spacer washers and tubes", S(*starts("Spacer washer stacks", "Spacer tube")), COL["spacer"]),
          [Part("Right spine side plate", C["Spine side plate, right"].shape, COL["ghost"]),
           Part("Right stay", C["Rear stay plate, right"].shape, COL["ghost"])], view_shape=ws,
          title="FlatTrike spacer washers (78) and spacer tubes (4): making sketch",
          material="Washers: 3 mm steel offcuts. Tubes: 16 x 2 mm steel tube", inset_view=(15, 70),
          notes=["Sketch: one washer (left) and one tube (right).",
                 "Washers: 16 mm outside, 8.5 mm hole, 3 mm thick; cut 78 from the",
                 "  sheet's offcuts in the same laser run.",
                 "Stacks of 9 go between the spine and each stay at the four stay bolts",
                 "  (27 mm); stacks of 3 go between the bulkhead and the box (9 mm).",
                 "Tubes: saw 16 x 2 mm steel tube into four 60.0 mm lengths, square the",
                 "  ends with a file. One goes inside the spine at each stay bolt so the",
                 "  bolt cannot squeeze the side plates together.",
                 "Check: each tube is 60.0 mm long, give or take 0.2 mm."])
    bk = C["Bulkhead"].shape
    sheet(111, Part("Bulkhead", bk, COL["bulk"]), ghost("rails", "uyoke", "lyoke", "beams"),
          title="FlatTrike bulkhead: making sketch", material=MAT, view_shape=turn(bk),
          inset_view=(25, -40),
          notes=["Plate 474 x 302 mm with two windows (400 x 152 and 400 x 42 mm).",
                 "Two rows of slots: the lower yoke's tabs 9 mm up from the bottom",
                 "  edge and the upper yoke's tabs 212 mm up, with bolt holes between.",
                 "Each side edge: two tabs and a T-slot into the bed rail.",
                 "Two 9 mm holes 220 mm each side of the centre, 214 mm up: the box bolts.",
                 TSLOT,
                 "Fit: square across the bed between the rails; the yokes come in from",
                 "  behind, the box sits 9 mm in front on spacer washers.",
                 "Check: the plate is flat within 1 mm after deburring."])
    rl = C["Bed rail, left"].shape
    sheet(112, Part("Bed rail", rl, COL["rail"]), ghost("bulk", "beams", "posts"),
          title="FlatTrike bed rail (make 2, left and right): making sketch", material=MAT,
          inset_view=(25, -60), rev="P2", date="2026-10-03",
          revisions=[P1, ("P2", "Tyre notch in the lower edge; " + REV_TRAIL, "2026-10-03", "AC")],
          notes=["Make 2; the right rail is the left rail turned over.",
                 "Strip 852 mm long, 160 mm deep at the back, 110 mm deep from 1150 mm",
                 "  ahead of the rear axle; four lightening windows.",
                 f"Tyre notch {P['RAIL_NOTCH'][2] - P['BOX_Z0'] + 110:.0f} mm up into the lower edge, {P['RAIL_NOTCH'][0]:.0f} to"
                 f" {P['RAIL_NOTCH'][1]:.0f} mm ahead",
                 f"  of the rear axle ({P['BOX_Z0'] - P['RAIL_NOTCH'][2]:.0f} mm of plate left): the trailing tyre passes"
                 " under it.",
                 "Two halving slots 3.4 mm wide from the bottom edge up to 55 mm deep,",
                 "  25 mm apart, for the axle beam plates.",
                 "Three T-slots in the top edge for the box bolts; a pair of slots and",
                 "  a 9 mm hole near the back for the bulkhead.",
                 TSLOT,
                 "Fit: the rails run along the bed 474 mm apart (inside faces).",
                 "Check: the halving slots are square to the top edge."])
    ab = C["Axle beam plate, rear"].shape
    sheet(113, Part("Axle beam plate", ab, COL["beam"]), ghost("rails", "posts"),
          title="FlatTrike axle beam plate (make 2): making sketch", material=MAT,
          view_shape=turn(ab), inset_view=(20, -40),
          notes=["Make 2, identical. Plate 566 x 120 mm with four windows.",
                 "Two halving slots 3.4 mm wide down from the top edge, 55 mm deep,",
                 "  238.5 mm each side of the centre line: the rails drop into them.",
                 "Each end: two tabs and a T-slot into the knuckle post's inner cheek.",
                 TSLOT,
                 "Fit: the two plates cross the bed 25 mm apart under the box floor and",
                 "  carry the front wheels' load from one knuckle post to the other.",
                 "Check: with both rails in the slots the top edges are level."])
    kp = C["Knuckle post plate, left front"].shape
    sheet(114, Part("Knuckle post plate", kp, COL["post"]),
          others("Knuckle post plate, left front", "Knuckle post", "Knuckle collar", "Axle beam", "Bed rail")
          + [Part("Lock stop", C["Steering lock stop, left"].shape, COL["stop"])],
          title="FlatTrike knuckle post plate (make 4): making sketch", material=MAT,
          view_shape=turn(kp), inset_view=(20, -150), rev="P3", date="2026-10-03",
          revisions=[P1, REV2, ("P3", "Lower lip trimmed to 8 mm; " + REV_TRAIL, "2026-10-03", "AC")],
          notes=["Make 4 from one file; turn two over for the right-hand post.",
                 "Front plates (one per post): also cut the lock stop's two slots and",
                 "  9 mm hole low on the column (shown); harmless on the rear plates.",
                 f"L-shaped plate: a {P['POST_W'] - P['T'] + P['POST_LIP']:.0f} mm wide column 325 mm tall, and an arm "
                 f"{470 - P['POST_Y0'] - P['POST_W'] - P['POST_LIP']:.0f} mm",
                 "  wide and 120 mm deep at the top that reaches out over the wheel.",
                 "Inner edge: 4 tabs and 2 T-slots into the inner cheek.",
                 "Arm: 2 tabs and 2 T-slots on its bottom edge and on its top edge,",
                 "  into the knuckle collar plates.",
                 f"Three slots and two 9 mm holes {P['POST_LIP'] + P['T'] / 2:.1f} mm in from the column's outer",
                 "  edge: the outer cheek's tabs and bolts.",
                 TSLOT,
                 "Fit: two plates stand 50 mm apart either side of the knuckle head tube;",
                 "  the lock stop (FTK-DWG-124) tabs into the front plate.",
                 "Check: all four plates match when stacked."])
    ic = C["Knuckle post inner cheek, left"].shape
    sheet(115, Part("Knuckle post inner cheek", ic, COL["cheek"]), others("Knuckle post inner cheek, left", "Knuckle post", "Axle beam", "Bed rail"),
          title="FlatTrike knuckle post inner cheek (make 2): making sketch", material=MAT,
          inset_view=(20, -120),
          notes=["Make 2; turn one over for the right-hand post. Plate 76 x 325 mm.",
                 "Two rows of slots 53 mm apart: the knuckle post plates' tabs.",
                 "Two rows of slots 25 mm apart near the bottom: the axle beam tabs.",
                 f"Bolt holes 9 mm between the slots ({cutnote('Knuckle post inner cheek, left')}).",
                 "Fit: the cheek faces the box, 3 mm from its side; the bolt heads above",
                 "  the box floor sit in counterbores in the box sides.",
                 "Check: the slots for the beams line up with the beams' end tabs."])
    oc = C["Knuckle post outer cheek, left"].shape
    sheet(116, Part("Knuckle post outer cheek", oc, COL["cheek"]), others("Knuckle post outer cheek, left", "Knuckle post", "Axle beam"),
          title="FlatTrike knuckle post outer cheek (make 2): making sketch", material=MAT,
          inset_view=(15, 60), rev="P2", date="2026-10-03",
          revisions=[P1, ("P2", "Note on the 8 mm lip; " + REV_TRAIL, "2026-10-03", "AC")],
          notes=["Make 2, identical. Plate 50 x 195 mm.",
                 "Each 195 mm edge: three tabs and two T-slots into the knuckle post plates.",
                 TSLOT,
                 "Fit: it closes the post's column on the wheel side, between the two",
                 f"  plates, {P['POST_LIP']:.0f} mm in from their outer edges.",
                 "Check: the cheek fits between two plates held 50 mm apart."])
    cl = C["Knuckle collar plate, left upper"].shape
    sheet(117, Part("Knuckle collar plate", cl, COL["collar"]), others("Knuckle collar plate, left upper", "Knuckle post", "Knuckle collar", "Knuckle head", "Axle beam"),
          title="FlatTrike knuckle collar plate (make 4): making sketch", material=MAT,
          inset_view=(50, -140),
          notes=["Make 4, identical. Plate 76 x 142 mm with a 34.5 mm hole 82 mm from",
                 "  one end, centred across the width: the headset cup spigot.",
                 "Two rows of slots 53 mm apart (the post plates' tabs), two 9 mm holes",
                 "  in each row.",
                 "Fit: one under the knuckle head tube and one on top; each cup's flange",
                 "  holds its plate against the tube end. The flange bears 2.5 mm inside",
                 "  the post plates, so the wheel load goes straight into them.",
                 "Check: the hole is square to the plate and burr free."])
    sa = C["Steering arm, left"].shape
    tx_, ty_ = M.ackermann_tip(1)
    arm_len = math.hypot(M.axle_x() - P["LEG_R"] - P["T"] - (tx_ - 10), (P["TRACK"] / 2 - P["LEG_Y"]) - ty_) + 12
    sheet(118, Part("Steering arm", sa, COL["arm"]), ghost("forks", "posts", "link"),
          title="FlatTrike steering arm (make 2, left and right): making sketch", material=MAT,
          inset_view=(30, -150), rev="P2", date="2026-10-03",
          revisions=[P1, ("P2", "Shorter arm; " + REV_TRAIL, "2026-10-03", "AC")],
          notes=["Make 2; the right arm is the left arm turned over.",
                 f"Tapered plate about {arm_len:.0f} mm long, 44 mm wide at the clamp end.",
                 "Clamp end: one tab and one T-slot into the clamp plate.",
                 "Tip: 8.2 mm hole for the rod end bolt, 120 mm from the kingpin axis,",
                 "  on the line from the kingpin to the middle of the rear axle",
                 "  (this is what gives the Ackermann steering).",
                 TSLOT,
                 "Fit: the arm points back and slightly in from the inboard fork leg,",
                 "  below the knuckle post; it turns with the wheel.",
                 "Check: on the fork, the hole is 120 mm from the steering axis (the",
                 "  wheel's centre line), give or take 1 mm."])
    cp = C["Steering arm clamp plate, left"].shape
    sheet(119, Part("Steering arm clamp plate", cp, COL["clamp"]), [Part("Fork", C["Front fork, left"].shape, COL["ghost"]),
                                                                   Part("Arm", C["Steering arm, left"].shape, COL["ghost"]),
                                                                   Part("U-bolts", C["U-bolts, left"].shape, COL["ghost"])],
          title="FlatTrike steering arm clamp plate (make 2): making sketch", material=MAT,
          view_shape=turn(cp), inset_view=(15, -160), rev="P3", date="2026-10-03",
          revisions=[P1, ("P2", "Lengthened inboard to meet the steering lock stop (2026-10-02)", "2026-10-02", "AC"),
                     ("P3", "Shortened inboard to 104 mm; " + REV_TRAIL, "2026-10-03", "AC")],
          notes=[f"Make 2; turn one over for the right. Plate {P['CLAMP_IN'] - P['LEG_Y'] + 24:.0f} x 40 mm.",
                 "Four 7 mm holes for two M6 U-bolts, 29 mm apart across and 26 mm",
                 "  apart up and down; one slot and one 9 mm hole for the arm.",
                 f"The plate runs {P['CLAMP_IN'] - P['LEG_Y']:.0f} mm in from the leg's centre: at full lock",
                 "  its front inboard corner meets the lock stop (FTK-DWG-124).",
                 "Fit: the plate sits behind the inboard fork leg, which trails the",
                 f"  steering axis by {P['FORK_OFFSET']:.0f} mm; the U-bolts go round the leg from the",
                 "  front and pull the plate against it; the long end points in.",
                 "Check: the U-bolts' legs pass through without forcing."])
    stp = C["Steering lock stop, left"].shape
    rot40 = lambda sh: M.Pos(P["WB"], P["TRACK"] / 2, 0) * M.Rot(0, 0, P["STEER_LOCK"]) * M.Pos(-P["WB"], -P["TRACK"] / 2, 0) * sh  # noqa: E731
    z0s, z1s, z2s = P["STOP_Z"]
    xc_, _ = M.stop_corner(1)
    sheet(124, Part("Steering lock stop", stp, COL["stop"]),
          [Part("Front knuckle post plate", C["Knuckle post plate, left front"].shape, COL["ghost"]),
           Part("Clamp plate (at full lock)", rot40(C["Steering arm clamp plate, left"].shape), COL["ghost"]),
           Part("Steering arm (at full lock)", rot40(C["Steering arm, left"].shape), COL["ghost"])],
          title="FlatTrike steering lock stop (make 2): making sketch", material=MAT, inset_view=(20, -125),
          rev="P2", date="2026-10-03",
          revisions=[("P1", "Making sketch for the steering lock stop (decided 2026-10-02)", "2026-10-02", "AC"),
                     ("P2", "Smaller fin; " + REV_TRAIL, "2026-10-03", "AC")],
          notes=[f"Make 2, identical; turn one over for the right. Plate {xc_ + P['STOP_LEG'] - P['WB'] - P['POST_X'] - P['T']:.0f}"
                 f" x {z2s - z0s:.0f} mm, 80 mm over the tabs.",
                 f"An upper part and a {P['STOP_LEG']:.0f} mm wide leg that hangs {z1s - z0s:.0f} mm below it at the front.",
                 "Back edge: two tabs and one T-slot into the front knuckle post plate.",
                 TSLOT,
                 "Fit: the fin stands upright, fore and aft, under the front of the",
                 f"  knuckle post; its leg's back edge is {xc_ - P['WB']:.0f} mm ahead of the kingpin axis.",
                 f"At full lock ({P['STEER_LOCK']:.0f} deg at the inner wheel) the steering arm clamp",
                 "  plate's front inboard corner meets the leg's back edge. The load",
                 "  then runs along the fin, in its own plane.",
                 "Check before the first ride: turn to full lock each way; each clamp",
                 "  plate meets its stop, and the tyres clear the box and the posts."])
    da = C["Drop arm"].shape
    pxd, pyd = M.drop_pin()
    ang = math.degrees(math.atan2(pyd, pxd - P["KP_X"]))
    sheet(120, Part("Drop arm", da, COL["drop"]), [Part("Steering column", C["Steering column (cut-down fork and quill stem)"].shape, COL["ghost"]),
                                                   Part("Drag link", C["Drag link with rod ends"].shape, COL["ghost"])],
          title="FlatTrike drop arm: making sketch", material=MAT, inset_view=(-30, -60),
          view_shape=b.Rot(0, 0, -ang) * b.Pos(-P["KP_X"], 0, 0) * da,
          notes=["Plate 183 mm long, 40 mm wide at the column end, 26 mm at the tip.",
                 "Two 9 mm holes 64 mm apart on its centre line: the crown bolts.",
                 "Tip: 8.2 mm hole for the drag link's rod end, 120 mm from the",
                 "  steering axis.",
                 "Fit: bolted flat under the steering fork's crown, pointing back and",
                 "  to the right, parallel to the left steering arm; the drag link,",
                 "  drop arm and left arm then form a parallelogram, so the left wheel",
                 "  turns as far as the handlebar.",
                 "Check: drop arm and left steering arm hole centres are 120 mm out."])
    cf = C["Steering column (cut-down fork and quill stem)"].shape
    sheet(121, Part("Steering column fork", cf, COL["column"]), ghost("ht", "lyoke", "uyoke") + [Part("Drop arm", C["Drop arm"].shape, COL["ghost"])],
          title="FlatTrike steering column: cutting and drilling a bought fork",
          material="Bought 1 1/8 in threaded steel fork with a forged crown; tall quill stem", inset_view=(15, -60),
          notes=["Buy a threaded 1 1/8 in steel fork with a separate forged crown (the",
                 "  roadster type), steerer at least 250 mm long.",
                 "Saw both legs off flush with the underside of the crown; file flat.",
                 "Drill two 9 mm holes up through the crown, 32 mm either side of the",
                 "  steerer, on the line of the legs. Use the drop arm as the template.",
                 "Cut the steerer to suit the headset stack (about 245 mm above the",
                 "  crown race seat) and fit a tall quill stem (about 350 mm).",
                 "Fit: the crown sits under the lower yoke; the drop arm bolts under it.",
                 "Check: the steerer turns freely in the head tube once the headset is",
                 "  adjusted, with no play."])
    tb = (M.tube((0, 0, 0), (0, 0, 200), 20, 17) + M.tube((70, 0, 0), (70, 0, 120), 20, 17)
          + M.tube((130, 0, 0), (130, 0, 120), 20, 17) + M.tube((190, 0, 0), (190, 0, 225), 15.9, 13.7))
    sheet(122, Part("Head tubes and seat tube", S("Central head tube", "Knuckle head tube, left", "Knuckle head tube, right", "Seat tube"),
                    COL["ht"]), ghost("spine", "uyoke", "lyoke", "posts"), view_shape=tb,
          title="FlatTrike head tubes and seat tube: cutting to length",
          material="Bought steel tube: 40 mm head tube section; 31.8 x 2.3 mm seat tube", inset_view=(20, -60),
          notes=["Central head tube: one 200.0 mm length (left in the sketch).",
                 "Knuckle head tubes: two 120.0 mm lengths (middle).",
                 "Seat tube: one 225 mm length of 31.8 x 2.3 mm tube (right); a 27.2 mm",
                 "  seatpost must slide in it.",
                 "Saw square, then face both ends of each head tube square to the tube",
                 "  axis (a head tube facing tool, or a lathe): the cups' flanges clamp",
                 "  the yokes and collar plates against these ends.",
                 "Head tube bore 34.0 mm for press-in 1 1/8 in threaded headset cups.",
                 "Check: lengths 200.0 and 120.0 mm, give or take 0.2 mm."])
    bx = C["Cargo box"].shape
    sheet(123, Part("Cargo box", bx, COL["box"]), ghost("rails", "bulk", "posts"),
          title="FlatTrike cargo box: drilling for the bed bolts",
          material="Exterior plywood, 12 mm floor, 9 mm walls and lid (by a carpenter)", inset_view=(25, -55),
          notes=["Box 820 x 560 x 360 mm outside; floor 12 mm, walls and lid 9 mm.",
                 "Floor: six 9 mm holes, 238.5 mm each side of the centre line, at",
                 "  168, 378 and 783 mm from the back face: bolts down into the rails.",
                 "Back: two 9 mm holes 220 mm each side of the centre line, 42 mm above",
                 "  the floor's underside: bolts to the bulkhead.",
                 "Each side: two 20 mm counterbores 5 mm deep, 125 mm above the floor's",
                 "  underside, 352 and 405 mm from the back face: room for the knuckle",
                 "  post bolt heads.",
                 "Seal every hole and edge before painting.",
                 "Check: drill the floor holes through the rails' T-slots with the box",
                 "  in place, so they line up."])
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    import build123d as b
    out = []
    box = lambda x0, x1, y0, y1, z0, z1: b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)  # noqa: E731

    def win(names, bx_):
        sh = S(*names) if isinstance(names, (list, tuple)) else C[names].shape
        return sh & bx_

    def J(n, items, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.joint([part(nm, sh, col) for nm, sh, col in items], OUT / f"joint-{n:02d}.png",
                            f"Joint {n}: {title}", subtitle=sub, **kw))

    # 01 top cover on a side plate (left), around the bolt at 472 mm along the edge
    (x0, z0), (x1, z1) = M.SPINE[0], M.SPINE[1]
    L = math.hypot(x1 - x0, z1 - z0); ux, uz = (x1 - x0) / L, (z1 - z0) / L
    cx, cz = x0 + ux * 472, z0 + uz * 472
    bw = box(cx - 45, cx + 45, 0, 60, cz - 45, cz + 30)
    J(1, [("Spine top cover", win("Spine top cover", bw), COL["cover"]),
          ("Spine side plate (left)", win("Spine side plate, left", bw), COL["spine"]),
          ("M8 bolt and locknut in the T-slot", win(bolts("Spine top cover"), bw), COL["bolt"])],
      "spine top cover on a side plate (cut away at the centre line)",
      "Tabs on the plate's edge sit in slots in the cover; the bolt pulls the cover down onto a locknut held in the plate",
      elev=20, azim=-120, size=(8, 6))
    # 02 ribs and upper yoke inside the spine: seen from below with the bottom cover and lower yoke left off
    bw = box(760, 980, -40, 40, 300, 610)
    J(2, [("Spine side plate (right)", win("Spine side plate, right", box(760, 1010, -40, 40, 300, 610)), COL["spine"]),
          ("Spine ribs", win(["Spine rib at 800", "Spine rib at 900"], bw), COL["rib"]),
          ("Upper yoke", win("Upper yoke", bw), COL["uyoke"]),
          ("Bolts from outside the spine", win(bolts("Spine ribs", "Upper yoke"), bw), COL["bolt"])],
      "ribs and upper yoke inside the spine (left plate and covers left off)",
      "Their tabs go through slots in both side plates; one M8 bolt each side into a T-slot", elev=30, azim=105, size=(8, 6))
    # 03 seat tube in its saddles
    bw = box(380, 560, -40, 40, 560, 810)
    J(3, [("Spine side plate (right)", win("Spine side plate, right", bw), COL["spine"]),
          ("Seat tube saddles", win(["Seat tube saddle, lower", "Seat tube saddle, upper"], bw), COL["saddle"]),
          ("Seat tube", win("Seat tube", bw), COL["seat"]),
          ("Shaft collars", win("Seat tube shaft collars", bw), "#C026D3"),
          ("Spine top cover (oval hole)", win("Spine top cover", bw), COL["cover"])],
      "seat tube in its two saddles (left side plate left off)",
      "A collar above the upper saddle carries the rider; a collar below the lower saddle stops the tube lifting",
      elev=10, azim=70, size=(8, 6))
    # 04 a stay node, cut through the bolt
    xn, zn = M.NODES[1]
    bw = box(xn - 25, xn + 25, -80, 80, zn - 25, zn)
    J(4, [("Rear stay plates", win(["Rear stay plate, left", "Rear stay plate, right"], bw), COL["stay"]),
          ("Spine side plates", win(["Spine side plate, left", "Spine side plate, right"], bw), COL["spine"]),
          ("Spacer washers (9 each side)", win("Spacer washer stacks, node 2", bw), COL["spacer"]),
          ("Spacer tube inside the spine", win("Spacer tube, node 2", bw), "#EAB308"),
          ("M8 through-bolt", win("Bolt: stay node 2", bw), COL["bolt"])],
      "a stay-to-spine bolt (cut through the bolt)", "Washer stacks fill the 27 mm gaps; the tube stops the bolt squeezing the spine",
      elev=55, azim=-50, size=(8, 6))
    # 05 bottom bracket
    bw = box(570, 630, -60, 60, 235, 265)
    J(5, [("Spine side plates", win(["Spine side plate, left", "Spine side plate, right"], bw), COL["spine"]),
          ("Bottom bracket shell and cups", win("Bottom bracket shell and cups", bw), COL["bb"])],
      "bottom bracket (cut through its axis)",
      "The shell sits between the plates; each cup's spigot passes through a plate and its flange clamps the plate to the shell",
      elev=35, azim=-30, size=(8, 6))
    # 06 head tube between the yokes
    bw = box(940, 1060, -60, 0, 290, 530)
    J(6, [("Upper yoke", win("Upper yoke", bw), COL["uyoke"]), ("Lower yoke", win("Lower yoke", bw), COL["lyoke"]),
          ("Central head tube", win("Central head tube", bw), COL["ht"]),
          ("Headset cups", win("Central headset cups", bw), "#6B7280"),
          ("Spine side plate (right)", win("Spine side plate, right", bw), COL["spine"])],
      "central head tube between the yokes (cut through its axis)",
      "The tube is the gap between the yokes; each pressed cup passes through a yoke and its flange clamps the yoke to the tube end",
      elev=15, azim=70, size=(8, 6))
    # 07 bulkhead: yokes and rail
    bw = box(1000, 1100, 150, 245, 295, 530)
    J(7, [("Bulkhead", win("Bulkhead", bw), COL["bulk"]), ("Bed rail (left)", win("Bed rail, left", bw), COL["rail"]),
          ("Upper yoke", win("Upper yoke", bw), COL["uyoke"]), ("Lower yoke", win("Lower yoke", bw), COL["lyoke"]),
          ("Bolts", win(bolts("Yokes to bulkhead", "Bulkhead to rails"), bw), COL["bolt"])],
      "bulkhead, yokes and left rail (seen from behind and inside)",
      "The yokes' tabs go into the bulkhead from behind; the bulkhead's tabs go into the rail; bolts into T-slots",
      elev=20, azim=-150, size=(8, 6))
    # 08 halving joint
    bw = box(1410, 1490, 215, 265, 340, 480)
    J(8, [("Bed rail (left), lifted to show its slots", b.Pos(0, 0, 110) * win("Bed rail, left", bw), COL["rail"]),
          ("Axle beam plates", win(["Axle beam plate, rear", "Axle beam plate, front"], box(1410, 1490, 160, 320, 340, 480)), "#F59E0B")],
      "rail and axle beams: halving joints (rail lifted off)",
      "Slots from below in the rail, from above in each beam plate; the rail drops over the beams and the box floor holds them together",
      elev=20, azim=-130, size=(8, 6))
    # 09 knuckle post corner with the beam ends (left post, seen from inside and below)
    bw = box(1400, 1500, 255, 345, 345, 480)
    J(9, [("Knuckle post plates", win(["Knuckle post plate, left rear", "Knuckle post plate, left front"], bw), COL["post"]),
          ("Inner cheek", win("Knuckle post inner cheek, left", bw), "#F59E0B"),
          ("Axle beam plates", win(["Axle beam plate, rear", "Axle beam plate, front"], bw), COL["beam"]),
          ("Bolts", win(bolts("Knuckle post corners", "Axle beams to knuckle"), bw), COL["bolt"])],
      "bottom of the left knuckle post, with the axle beam ends (outer cheek left off)", "Every corner is a row of tabs in slots, with M8 bolts into T-slots between them",
      elev=25, azim=-145, size=(8, 6))
    # 10 knuckle head tube between the collar plates
    bw = box(1390, 1450, 370, 470, 535, 695)
    J(10, [("Knuckle collar plates", win(["Knuckle collar plate, left lower", "Knuckle collar plate, left upper"], bw), "#F59E0B"),
           ("Knuckle post plates", win(["Knuckle post plate, left rear", "Knuckle post plate, left front"], bw), COL["post"]),
           ("Knuckle head tube", win("Knuckle head tube, left", bw), COL["ht"]),
           ("Headset cups", win("Knuckle headset cups, left", bw), "#6B7280"),
           ("Fork steerer and crown", win("Front fork, left", bw), COL["fork"])],
       "left knuckle: head tube between the collar plates (cut through its axis)",
       "The cup flanges bear on the collar plates right beside the post plates, so the wheel load goes straight into the plates",
       elev=12, azim=30, size=(8, 6))
    # 11 steering arm clamp
    leg_y = P["TRACK"] / 2 - P["LEG_Y"]
    bw = box(1310, 1560, leg_y - 80, leg_y + 50, 290, 360)
    J(11, [("Fork leg (inboard)", win("Front fork, left", bw), COL["fork"]),
           ("Lock stop", win("Steering lock stop, left", bw), COL["stop"]),
           ("Clamp plate", win("Steering arm clamp plate, left", bw), COL["clamp"]),
           ("Steering arm", win("Steering arm, left", bw), COL["arm"]),
           ("Two M6 U-bolts", win("U-bolts, left", bw), "#78716C"),
           ("Rod ends", win(["Tie rod with rod ends", "Drag link with rod ends", "Rod end bolts"], bw), COL["link"])],
       "left steering arm on the inboard fork leg",
       "Two U-bolts pull the clamp plate against the leg; the arm tabs into it. At full lock the plate's inner corner meets the lock stop",
       elev=25, azim=-140, size=(8, 6))
    # 12 drop arm under the crown
    bw = box(840, 1080, -90, 60, 240, 300)
    J(12, [("Steering fork crown (legs cut off)", win("Steering column (cut-down fork and quill stem)", bw), COL["column"]),
           ("Drop arm", win("Drop arm", bw), COL["drop"]),
           ("Two M8 bolts through the crown", win(bolts("drop arm"), bw), COL["bolt"]),
           ("Drag link rod end", win(["Drag link with rod ends", "Rod end bolts"], bw), COL["link"])],
       "drop arm under the steering fork crown", "Seen from below. The drop arm points back and right, parallel to the left steering arm",
       elev=-35, azim=-60, size=(8, 6))
    # 13 box to bed
    bw = box(1050, 1110, 180, 260, 450, 540)
    J(13, [("Bulkhead", win("Bulkhead", bw), COL["bulk"]), ("Cargo box (back and floor)", win("Cargo box", bw), COL["box"]),
           ("Spacer washers (3)", win("Spacer washers, box to bulkhead left", bw), COL["spacer"]),
           ("Bed rail (left)", win("Bed rail, left", bw), COL["rail"]),
           ("Bolts", win(bolts("box to bulkhead left", "Box to rails"), bw), COL["bolt"])],
       "box to bulkhead and rail (cut away, seen from the left)", "Three spacer washers keep the box clear of the yoke bolt heads on the bulkhead",
       elev=15, azim=75, size=(8, 6))
    # 14 rear dropout
    bw = box(-60, 40, 0, 90, 215, 300)
    J(14, [("Rear stay plate (left)", win("Rear stay plate, left", bw), COL["stay"]),
           ("Rear hub axle (hub body left off)", win("Rear wheel", box(-60, 40, 61, 90, 215, 300)), COL["drive"])],
       "rear dropout: open slot in the stay plate (seen from outside)", "The axle slides in from behind; pull it back to tension the chain, then tighten the axle nuts",
       elev=15, azim=70, size=(8, 6))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    G = groups()
    out = []
    g = lambda nm, col=None, *ks: part(nm, S(*ks), col or COL["ghost"])  # noqa: E731

    def st(n, done, new, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    spL = part("Left spine side plate", C["Spine side plate, left"].shape, COL["spine"])
    spR = part("Right spine side plate", C["Spine side plate, right"].shape, COL["spine"])
    st(1, [spL], [mv(part("Spine ribs (2)", S("Spine rib at 800", "Spine rib at 900"), COL["rib"]), (0, -150, 0)),
                  mv(part("Seat tube saddles (2)", S("Seat tube saddle, lower", "Seat tube saddle, upper"), COL["saddle"]), (0, -150, 0)),
                  mv(part("Upper yoke", C["Upper yoke"].shape, COL["uyoke"]), (0, -150, 0))],
       "ribs, saddles and upper yoke into the left side plate",
       "Lay the left plate on blocks, inside face up; push each part's tabs into its slots. No bolts yet", elev=30, azim=-70)
    inner = [spL, part("Ribs, saddles, upper yoke", S("Spine rib at 800", "Spine rib at 900", "Seat tube saddle, lower",
                                                      "Seat tube saddle, upper", "Upper yoke"), COL["ghost"])]
    st(2, inner, [mv(spR, (0, -160, 0))], "right side plate onto the tabs",
       "Lower it on so every tab enters its slot; then fit the M8 bolts and locknuts, finger tight", elev=25, azim=-70)
    box_ = inner + [spR]
    st(3, box_, [mv(G["topc"], (0, 0, 120))], "top cover",
       "Onto the plates' top-edge tabs; M8 x 25 bolts down into the T-slots, locknuts in the windows", elev=25, azim=-60, label_done=False)
    box2 = box_ + [G["topc"]]
    st(4, box2, [mv(G["botc"], (0, 0, -120)), mv(G["lyoke"], (0, 0, -150))], "bottom cover and lower yoke",
       "Up onto the bottom-edge tabs; bolts up into the T-slots. Now square the spine and tighten all its bolts", elev=-25, azim=-60,
       label_done=False)
    spine = box2 + [G["botc"], G["lyoke"]]
    st(5, spine, [mv(part("Central head tube", C["Central head tube"].shape, COL["ht"]), (150, 0, 0)),
                  mv(part("Headset cups (pressed in)", C["Central headset cups"].shape, "#6B7280"), (150, 0, 0))],
       "head tube between the yokes", "Slide the tube in between the yokes, line it up with the holes, then press a cup in from above and below",
       elev=18, azim=-55, label_done=False)
    spine2 = spine + [G["ht"]]
    st(6, spine2, [mv(G["bb"], (0, -200, 0))], "bottom bracket",
       "Shell between the plates; screw the cups in from each side so their flanges clamp the plates", elev=10, azim=-60, label_done=False)
    spine3 = spine2 + [G["bb"]]
    st(7, spine3, [mv(G["seat"], (-70, 0, 230))], "seat tube",
       "Down through the top cover and both saddles; fit the collars against the saddles and tighten them", elev=20, azim=-60,
       label_done=False)
    spine4 = spine3 + [G["seat"]]
    st(8, [G["stays"]], [mv(G["bridge"], (0, 0, 150))], "stay bridge between the stays",
       "Stand the stays 120 mm apart; bridge tabs into the stays' slots; one M8 bolt each side", elev=25, azim=-50)
    st(9, spine4, [mv(part("Stays with their bridge", S("Rear stay plate, left", "Rear stay plate, right", "Stay bridge"), COL["stay"]), (-250, 0, 0)),
                   mv(G["nodes"], (0, -250, 0))],
       "stays onto the spine", "Four M8 x 140 bolts: 9 washers each side between spine and stay, a spacer tube inside the spine",
       elev=20, azim=-60, label_done=False)
    frame = spine4 + [G["stays"], G["bridge"], G["nodes"]]
    st(10, frame, [mv(G["bulk"], (150, 0, 0))], "bulkhead onto the yokes",
       "Onto both yokes' front tabs; M8 bolts through the bulkhead into the yokes' T-slots", elev=20, azim=-55, label_done=False)
    frame2 = frame + [G["bulk"]]
    st(11, frame2, [mv(G["rails"], (0, 0, 0)), ], "bed rails onto the bulkhead",
       "Each rail onto the bulkhead's side tabs; one bolt each into the bulkhead's T-slot", elev=22, azim=-55, label_done=False)
    G["rails"].explode = (0, 0, 0)
    frame3 = frame2 + [G["rails"]]
    st(12, frame3, [mv(G["beams"], (0, 0, -120))], "axle beams up into the rails",
       "Push each beam plate up so its slots straddle both rails and the rails sit in the beam slots", elev=-15, azim=-55,
       label_done=False)
    post = part("Knuckle post plates and cheeks", S("Knuckle post plate, left rear", "Knuckle post plate, left front",
                                                    "Knuckle post inner cheek, left", "Knuckle post outer cheek, left"), COL["post"])
    st(13, [post], [mv(part("Lower collar plate", C["Knuckle collar plate, left lower"].shape, COL["collar"]), (0, 0, -90)),
                    mv(part("Head tube", C["Knuckle head tube, left"].shape, COL["ht"]), (0, 90, 0)),
                    mv(part("Upper collar plate", C["Knuckle collar plate, left upper"].shape, COL["collar"]), (0, 0, 90)),
                    mv(part("Headset cups (pressed in)", C["Knuckle headset cups, left"].shape, "#6B7280"), (0, 90, 0)),
                    mv(part("Lock stop", S("Steering lock stop, left", *[n for n in bolts("Steering lock stops") if C[n].shape.center().Y > 0]),
                            COL["stop"]), (120, 0, -60))],
       "build each knuckle post (left shown)",
       "Plates and cheeks, tabs in slots; collar plates on; head tube between them; cups in; lock stop onto the front plate",
       elev=20, azim=-30, label_done=False)
    frame4 = frame3 + [G["beams"]]
    st(14, frame4, [mv(part("Knuckle post, left", S(*starts("Knuckle post plate, left", "Knuckle post inner cheek, left",
                                                            "Knuckle post outer cheek, left", "Knuckle collar plate, left",
                                                            "Knuckle head tube, left", "Knuckle headset cups, left")), COL["post"]), (0, 150, 0)),
                    mv(part("Lock stop, left", C["Steering lock stop, left"].shape, COL["stop"]), (0, 150, 0)),
                    mv(part("Lock stop, right", C["Steering lock stop, right"].shape, COL["stop"]), (0, -150, 0)),
                    mv(part("Knuckle post, right", S(*starts("Knuckle post plate, right", "Knuckle post inner cheek, right",
                                                             "Knuckle post outer cheek, right", "Knuckle collar plate, right",
                                                             "Knuckle head tube, right", "Knuckle headset cups, right")), COL["post"]), (0, -150, 0))],
       "knuckle posts onto the axle beams",
       "Each post, with its lock stop on the front plate, onto the beams' end tabs; bolts through the cheek into the beams",
       elev=20, azim=-55, label_done=False)
    frame5 = frame4 + [G["posts"], G["collars"], G["stops"]]
    st(15, frame5, [mv(part("Steering column (cut-down fork)", C["Steering column (cut-down fork and quill stem)"].shape, COL["column"]), (0, 0, -250)),
                    mv(part("Drop arm and crown bolts", S("Drop arm", *bolts("drop arm")), COL["drop"]), (0, 0, -330))],
       "steering column and drop arm", "Steerer up through the head tube; adjust the headset; bolt the drop arm under the crown",
       elev=-12, azim=-55, label_done=False)
    frame6 = frame5 + [G["column"]]
    st(16, frame6, [mv(part("Front forks and wheels", S("Front fork, left", "Front fork, right", "Front wheel, left", "Front wheel, right"), COL["fork"]), (0, 0, -260))],
       "front forks and wheels", "Each fork turned round so its legs trail the steerer; steerer up through its knuckle head tube; adjust the headset; wheel in",
       elev=15, azim=-55, label_done=False)
    frame7 = frame6 + [G["forks"]]
    stops17 = part("Lock stop, right (fitted in step 14)", C["Steering lock stop, right"].shape, COL["stop"])
    side_ = lambda sd: [n for n in starts("Steering arm", "U-bolts", "Bolt: Steering arm")  # noqa: E731
                        if (C[n].shape.center().Y > 0) == (sd > 0)]
    armR = part("Right steering arm, clamp plate, U-bolts", S(*side_(-1)), COL["arm"])
    armL = part("Left arm, the same", S(*side_(1)), COL["arm"])
    stopL = part("Lock stop, left", C["Steering lock stop, left"].shape, COL["ghost"])
    st(17, [p for p in frame7 if p is not G["stops"]] + [stopL], [mv(armR, (-120, 0, 0)), mv(armL, (-120, 0, 0)), stops17],
       "steering arms onto the fork legs",
       "Clamp plate behind each inboard leg, long end in; two U-bolts; arm tabs in, one bolt. Turn to full lock: each clamp plate meets its stop",
       elev=-20, azim=-40, label_done=False)
    frame8 = frame7 + [G["arms"]]
    st(18, frame8, [mv(G["link"], (0, 0, -120))], "tie rod and drag link",
       "Rod ends with locknuts on all three bolts. Set the tie rod so both wheels point straight ahead", elev=-25, azim=-50,
       label_done=False)
    frame9 = frame8 + [G["link"]]
    st(19, frame9, [mv(G["drive"], (-200, -150, 0))], "rear wheel and drivetrain",
       "Axle into the open dropouts, chain on, pull the wheel back to tension the chain; cranks and pedals on", elev=15, azim=-60,
       label_done=False)
    frame10 = frame9 + [G["drive"]]
    st(20, frame10, [mv(G["box"], (0, 0, 220))], "cargo box onto the bed",
       "Six bolts down through the floor into the rails' T-slots, two through the back into the bulkhead", elev=20, azim=-55,
       label_done=False)
    st(21, frame10 + [G["box"]], [mv(G["ride"], (0, 0, 200))], "seatpost, saddle, handlebar and brakes",
       "Seatpost in the seat tube; quill stem and bar in the steerer; brake levers, cables and the parking latch",
       elev=20, azim=-55, label_done=False)
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("only=")]
    only = None
    for a in sys.argv[1:]:
        if a.startswith("only="):
            only = {int(x) for x in a[5:].split(",")}
    what = args or ["overview", "sheets", "joints", "steps"]
    for w in what:
        if w == "overview":
            print(w, "->", overview())
        else:
            print(w, "->", {"sheets": sheets, "joints": joints, "steps": steps}[w](only))
