"""FlatTrike sizing calculations, FTK-CAL-001 v0.6 (TRL 3, constructable design, FTK-DDR-003, with the
decisions of 2026-10-02: cargo rated at 148 kg with an 80 kg rider and 138 kg with a 90 kg rider, R8 72 kg,
R14 60 min for a knuckle post plate, steering lock stops at the knuckle posts).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
Geometry, plate areas and part centroids come from the parametric model (cad/src/model.py),
so the note, the model and the drawing stay in step. First-principles estimates only;
nothing here is measured.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
import model as M  # noqa: E402

G = 9.81
OUT = []   # (key, value, unit, note)


def rec(key, value, unit="", note=""):
    OUT.append((key, value, unit, note))
    v = f"{value:,.3g}" if isinstance(value, float) and abs(value) < 100 else (
        f"{value:,.1f}" if isinstance(value, float) else str(value))
    print(f"  {key:52s} {v:>12s} {unit}")
    return value


def head(t):
    print(f"\n== {t}")


# ---------------------------------------------------------------- assumptions
P = M.PARAMS
RIDER, RIDER_MAX, CARGO, CARGO_MAX = 80.0, 90.0, 148.0, 138.0    # rating restated 2026-10-02 (FTK-DDR-003 A1)
R8_KG = 72.0                   # R8 empty mass target, relaxed 2026-10-02
R14_KN_MIN = 60.0              # R14 target for a knuckle post plate, 2026-10-02
FORK_BUY = (30.0, 40.0)        # mm, fork offset range to buy; the fork is fitted turned round so the offset trails
                               # (decided by Amish 2026-10-03); the model uses P["FORK_OFFSET"]
RHO_STEEL, RHO_PLY = 7850.0, 700.0
CRR, CDA, RHO_AIR, ETA = 0.015, 0.9, 1.2, 0.89
P_RIDER, P_ASSIST = 110.0, 250.0
DYN = 2.5                      # dynamic factor on static loads for potholes and curbs
E, FY = 210e3, 235.0           # MPa
FAT_CAFL = 0.737 * 90          # MPa, constant-amplitude fatigue limit for a 90 MPa detail (plate with holes)
MU_SLIP, BOLT_PRELOAD = 0.20, 15.6e3   # painted faying faces; M8 8.8 at 25 N m with K = 0.2
HUB_RATIOS = (0.75, 1.00, 1.333)       # typical 3-speed hub gear
BOUGHT = {   # kg, assumed masses of bought parts (BOM items 5 to 8 and 10 to 14)
    "Front wheels with drum hubs (2)": (6, 5.8), "Rear wheel with 3-speed drum hub": (7, 3.8),
    "Drivetrain (BB, cranks, ring, chain, pedals, guard)": (8, 3.0),
    "Steering: 3 headsets, head tubes, column, two 20 in forks, drag link, tie rod": (5, 4.7), "Seat and seatpost": (10, 1.4), "Handlebar and stem": (11, 1.2),
    "Brake levers, cables, latch": (12, 0.7), "Box hinges, hasp, lock, screws, battens": (9, 1.0),
    "Paint": (13, 0.6), "Accessories (mudguards, reflectors, bell, bumpers)": (14, 1.5),
    "Seat tube (31.8 x 2.3 mm) and two shaft collars (FTK-DDR-003)": (10, 0.45),
    "Spacer tubes (4) and U-bolts (4) (FTK-DDR-003)": (4, 0.30),
}
BOLTS = {}  # M8 class 8.8 bolt sets (bolt, washer, all-metal locknut) per joint group: counted from the model in main()
BOLT_KG = 0.028


def true_shape_nest(plates, SW, SL, EDGE, cell=5.0):
    """Greedy bottom-left nest of the true plate shapes (outline minus windows) on a raster.
    Parts are placed largest first in 4 orientations; a part may sit inside another part's window.
    Each rasterized part is grown by one cell for raster error and by 2 more cells (10 mm) for the gap
    between parts. Returns (length used, count)."""
    import numpy as np
    from matplotlib.path import Path as MPath
    nx, ny = int((SW - 2 * EDGE) // cell), int((SL - 2 * EDGE) // cell)

    def raster(pl):
        us = [u for u, _ in pl["poly"]]; vs = [v for _, v in pl["poly"]]
        u0, v0 = min(us), min(vs)
        w, h = int(math.ceil((max(us) - u0) / cell)) + 1, int(math.ceil((max(vs) - v0) / cell)) + 1
        gu, gv = np.meshgrid(u0 + (np.arange(w) + 0.5) * cell, v0 + (np.arange(h) + 0.5) * cell)
        pts = np.column_stack([gu.ravel(), gv.ravel()])
        m = MPath(pl["poly"]).contains_points(pts)
        for hole in pl["holes"]:
            m &= ~MPath(hole).contains_points(pts)
        return grow(m.reshape(h, w), 1)     # one extra cell all round, so thin edges and window rims are kept

    def grow(m, k):
        out = np.pad(m, k)
        base = out.copy()
        for dy in range(-k, k + 1):
            for dx in range(-k, k + 1):
                out |= np.roll(np.roll(base, dy, 0), dx, 1)
        return out

    occ = np.zeros((ny, nx), bool)
    order = sorted(plates, key=lambda p: -p["area_mm2"])
    used, placed = 0, 0
    for pl in order:
        m0 = raster(pl)
        best = None
        for r in range(4):
            mat = np.rot90(m0, r)
            big = grow(mat, 2)
            h, w = big.shape
            if h > ny or w > nx:
                continue
            H, W = ny + h, nx + w
            F = np.fft.rfft2(occ.astype(float), (H, W)) * np.conj(np.fft.rfft2(big.astype(float), (H, W)))
            corr = np.fft.irfft2(F, (H, W))[: ny - h + 1, : nx - w + 1]
            ok = np.argwhere(corr < 0.5)
            if len(ok) == 0:
                continue
            key = ok[:, 0] + h
            i = np.lexsort((ok[:, 1], key))[0]
            cand = (key[i], ok[i, 1], r, ok[i, 0], mat)
            if best is None or cand[:2] < best[:2]:
                best = cand
        if best is None:
            continue
        _, x, r, y, mat = best
        h, w = mat.shape
        occ[y + 2: y + 2 + h, x + 2: x + 2 + w] |= mat
        placed += 1
    rows = np.where(occ.any(axis=1))[0]
    used = (rows.max() + 1) * cell + 2 * EDGE if len(rows) else 0.0
    return float(used), placed


def V_j_static(items, rider, mt, front):
    """Vertical shear at the bed-to-spine joint, static, N (as section 5.3)."""
    rear_lst = [i for i in items if not i[5]] + [rider]
    return sum(i[1] for i in rear_lst) * G - (mt - front) * G


def M_j_static(items, rider, mt, front, kp):
    """Pitch moment at the bed-to-spine joint, static, N m (as section 5.3)."""
    rear_lst = [i for i in items if not i[5]] + [rider]
    return ((mt - front) * G * kp - sum(i[1] * G * (kp - i[2]) for i in rear_lst)) / 1000


def main():
    parts = M.build_parts()
    sched = M.plate_schedule()
    BOLTS.update(M.bolt_count())
    kgm2 = P["T"] / 1000 * RHO_STEEL

    # ------------------------------------------------------------ 1 geometry and plates
    head("1. Geometry, plates and nesting (R3, R4, R6, R9, R17)")
    from build123d import Compound
    asm = Compound(children=[parts[k] for k in sorted(parts)])
    bb = asm.bounding_box()
    rec("Overall length", bb.size.X / 1000, "m")
    rec("Overall width", bb.size.Y / 1000, "m")
    rec("Overall height (saddle top)", bb.size.Z / 1000, "m")
    rec("Wheelbase", M.axle_x() / 1000, "m", "front axles trail the knuckle steering axes (1.45 m) by the fork offset")
    rec("Front track", P["TRACK"] / 1000, "m")
    n_plates = sum(v["qty"] for v in sched.values())
    area = sum(v["qty"] * v["area_m2"] for v in sched.values())
    rec("Cut plates (count)", n_plates)
    rec("Plate area, net of windows", area, "m2")
    plate_kg = rec("Plate mass (3 mm, 23.6 kg/m2)", area * kgm2, "kg")
    washers = 8 * 9 + 2 * 3
    rec("Spacer washers cut from offcuts (8 stacks of 9 at the stay nodes, 2 of 3 behind the box)", washers)

    # shelf nesting of bounding rectangles on one 1250 x 2500 sheet, 8 mm gap, 10 mm edge margin
    SW, SL, GAP, EDGE = 1250.0, 2500.0, 8.0, 10.0
    pieces = []
    for k, v in sched.items():
        pieces += [v["size"]] * v["qty"]

    def ffdh(pcs):
        """First-fit decreasing height: shelves stacked along the 2500 mm length, pieces side by side
        across the 1250 mm width. pcs: list of (across, along)."""
        pcs = sorted(pcs, key=lambda r: -r[1])
        shelves = []
        for across, along in pcs:
            for sh in shelves:
                if sh["used"] + across <= SW - 2 * EDGE and along <= sh["depth"]:
                    sh["used"] += across + GAP; break
            else:
                shelves.append({"used": across + GAP, "depth": along})
        return sum(sh["depth"] for sh in shelves) + GAP * (len(shelves) - 1) + 2 * EDGE, len(shelves)

    import random
    rng = random.Random(1)      # fixed seed: the note quotes this result
    best = (1e9, 0)
    for it in range(3000):      # random orientation of each piece, keep the shortest layout
        pcs = [(w, h) if (it == 0 or rng.random() < 0.5) else (h, w) for w, h in pieces]
        pcs = [(a, b) if a <= SW - 2 * EDGE else (b, a) for a, b in pcs]
        best = min(best, ffdh(pcs))
    used, n_sh = best
    rec("Shelf-nest of bounding rectangles: sheet length used (of 2500 mm)", used, "mm",
        f"{n_sh} shelves; conservative, ignores the plates' shapes and windows")
    rec("Sheet utilisation by net area", area / (SW * SL / 1e6) * 100, "%")
    used_ts, placed = true_shape_nest(M.PLATES, SW, SL, EDGE)
    rec("True-shape raster nest: sheet length used (of 2500 mm)", used_ts, "mm",
        f"{placed} of {len(M.PLATES)} plates placed; 5 mm raster, 10 mm or more between parts, small parts in windows")
    r4_ok = used_ts <= SL

    # box and flat pack
    x0 = P["BOX_X0"]; L_in = P["BOX_L"] - 2 * P["PLY_WALL"]; W_in = P["BOX_W"] - 2 * P["PLY_WALL"]
    H_in = P["BOX_H"] - P["PLY_FLOOR"]
    rec("Box inside volume", L_in * W_in * H_in / 1e6, "L")
    lid_top = P["BOX_Z0"] + P["BOX_H"] + P["PLY_WALL"]
    rec("Lid (counter) height", lid_top / 1000, "m")
    box_kg = rec("Box mass (12 mm floor, 9 mm walls and lid, 700 kg/m3)", parts[9].volume / 1e9 * RHO_PLY, "kg")
    stack = (n_plates + 6) * 3.0 * 1.1 + (P["PLY_FLOOR"] + 5 * P["PLY_WALL"]) * 1.1
    rec("Flat stack of plates and box panels", stack, "mm")
    foot_l = max(max(v["size"]) for v in sched.values()) / 1000 + 0.005
    foot_w = max(max(min(v["size"]) for v in sched.values()) / 1000, P["BOX_W"] / 1000) + 0.04
    crate = (round(foot_l + 0.52, 2), round(max(foot_w, 0.52), 2), 0.36)
    rec(f"Crate: plates and panels {foot_l:.2f} x {foot_w:.2f}, three wheels and forks stacked beside",
        crate[0] * crate[1] * crate[2], "m3", f"{crate[0]:.2f} x {crate[1]:.2f} x {crate[2]:.2f} m")
    longest = max(max(v["size"]) for v in sched.values())
    rec("Longest cut plate", longest, "mm")
    rec("Longest single piece (box floor panel)", float(P["BOX_L"]), "mm")

    # ------------------------------------------------------------ 2 mass and centre of mass
    head("2. Mass budget and centre of mass (R1, R8)")
    items = []   # (label, kg, x, y, z, on_bed)
    bed_items = {3, 6, 9, 11}
    by_bom = {}
    for k, v in sched.items():
        by_bom[v["bom"]] = by_bom.get(v["bom"], 0.0) + v["qty"] * v["area_m2"] * kgm2
    for b, kg in by_bom.items():
        c = parts[b].center()
        items.append((f"Plates, item {b}", kg, c.X, c.Y, c.Z, b in bed_items))
    washer_kg = washers * (math.pi * (13 ** 2 - 4.25 ** 2) * 3 / 1e9 * RHO_STEEL)
    c = parts[4].center(); items.append(("Spacer washers", washer_kg, c.X, 0, c.Z, False))
    n_bolts = sum(BOLTS.values())
    bolts_kg = n_bolts * BOLT_KG
    items.append(("M8 bolt sets", bolts_kg, 800, 0, 450, False))
    items.append(("Cargo box", box_kg, *(lambda c: (c.X, c.Y, c.Z))(parts[9].center()), True))
    for name, (b, kg) in BOUGHT.items():
        c = parts[b].center() if b in parts else parts[1].center()
        items.append((name, kg, c.X, c.Y, c.Z, b in bed_items))
    empty = sum(i[1] for i in items)
    for i in items:
        print(f"    {i[0]:52s} {i[1]:6.1f} kg")
    rec("Bolt sets (count)", n_bolts)
    rec("Bolts and spacer washers", bolts_kg + washer_kg, "kg")
    rec("Empty mass", empty, "kg", f"R8 target {R8_KG:.0f} kg (relaxed 2026-10-02; 70 kg before)")
    rec("Margin under R8", R8_KG - empty, "kg")
    rec("Plate share of empty mass", plate_kg / empty * 100, "%")
    rec("Box share of empty mass", box_kg / empty * 100, "%")
    gross = rec(f"Gross mass, 80 kg rider and {CARGO:.0f} kg cargo", empty + RIDER + CARGO, "kg", "R1 limit 300 kg")
    rec(f"Gross mass, 90 kg rider and {CARGO_MAX:.0f} kg cargo", empty + RIDER_MAX + CARGO_MAX, "kg", "R1 limit 300 kg")
    rec("Cargo allowed with an 80 kg rider inside 300 kg", 300 - empty - RIDER, "kg", f"R1 rated cargo {CARGO:.0f} kg")
    rec("Cargo allowed with a 90 kg rider inside 300 kg", 300 - empty - RIDER_MAX, "kg", f"R1 rated cargo {CARGO_MAX:.0f} kg")

    saddle_x = M.seat_xy(P["SADDLE_TOP"] - 25)
    rider = ("Rider", RIDER, saddle_x + 20, 0.0, P["SADDLE_TOP"] + 160, False)
    cargo = ("Cargo", CARGO, x0 + P["BOX_L"] / 2, 0.0, P["BOX_Z0"] + P["PLY_FLOOR"] + H_in / 2, True)
    rec("Rider centre of mass ahead of rear axle", rider[2] / 1000, "m")
    rec("Rider centre of mass height", rider[4] / 1000, "m")

    def com(lst):
        m = sum(i[1] for i in lst)
        return m, sum(i[1] * i[2] for i in lst) / m, sum(i[1] * i[3] for i in lst) / m, sum(i[1] * i[4] for i in lst) / m

    m0, xe, _, ze = com(items)
    rec("Empty trike CoM ahead of rear axle", xe / 1000, "m"); rec("Empty trike CoM height", ze / 1000, "m")

    # axle loads, loaded
    mt, xt, _, zt = com(items + [rider, cargo])
    front = mt * xt / M.axle_x()
    rec("Front axle load, loaded (static)", front * G / 1000, "kN")
    rec("Rear axle load, loaded (static)", (mt - front) * G / 1000, "kN")
    mr, xr, _, _ = com(items + [rider])
    rec("Rear axle load, rider only (static)", (mr - mr * xr / M.axle_x()) * G / 1000, "kN")

    # ------------------------------------------------------------ 3 riding power
    head("3. Riding power, gearing and assist (R12, R13)")
    f_roll = CRR * gross * G
    rec("Rolling resistance at gross mass", f_roll, "N")
    p_wheel = P_RIDER * ETA
    k_air = 0.5 * RHO_AIR * CDA
    v = 1.0
    for _ in range(60):
        v = v - (f_roll * v + k_air * v ** 3 - p_wheel) / (f_roll + 3 * k_air * v ** 2)
    rec("Power at the rear wheel from 110 W", p_wheel, "W")
    rec("Cruise speed, flat", v * 3.6, "km/h", "R12 target 7 km/h")
    rec("  of which rolling", f_roll * v, "W"); rec("  of which drag", k_air * v ** 3, "W")
    f5 = gross * G * (0.05 + CRR)
    v4 = 4 / 3.6
    p5 = f5 * v4 + k_air * v4 ** 3
    rec("Force on a 5 % grade", f5, "N")
    rec("Wheel power at 4 km/h on 5 %", p5, "W")
    rec("Pedal power at 4 km/h on 5 %", p5 / ETA, "W", "R13; rider sustains 110 W")
    v5 = 1.0
    for _ in range(60):
        v5 = v5 - (f5 * v5 + k_air * v5 ** 3 - p_wheel) / (f5 + 3 * k_air * v5 ** 2)
    rec("Unassisted speed on 5 % at 110 W", v5 * 3.6, "km/h")
    rear_n = (mt - front) * G
    rec("Rear tyre grip needed on 5 %, loaded (rear-wheel drive)", f5 / rear_n, "", "friction coefficient")
    R = P["WHEEL_R"] / 1000
    rec("Wheel torque on 5 %", f5 * R, "N m")
    ring, spr = P["RING_T"], P["SPROCKET_T"]
    circ = 2 * math.pi * R
    for g_, rt in zip(("low", "middle", "high"), HUB_RATIOS):
        dev = circ * ring / spr * rt
        rec(f"Development, {g_} gear", dev, "m per crank rev")
    rec("Cadence at 4 km/h in low gear", v4 / (circ * ring / spr * HUB_RATIOS[0]) * 60, "rpm")
    rec("Speed at 70 rpm in high gear", 70 / 60 * circ * ring / spr * HUB_RATIOS[2] * 3.6, "km/h")
    crank_t = f5 * R / (ring / spr * HUB_RATIOS[0]) / ETA
    rec("Mean crank torque on 5 % in low gear", crank_t, "N m")
    rec("Mean pedal force at 170 mm", crank_t / (P["CRANK"] / 1000), "N")
    pa = (P_ASSIST + P_RIDER) * ETA
    va = 1.0
    for _ in range(60):
        va = va - (f5 * va + k_air * va ** 3 - pa) / (f5 + 3 * k_air * va ** 2)
    rec("Speed on 5 % with 250 W mid-drive plus rider", va * 3.6, "km/h", "assist route C")
    # SwapCell energy use, assist route C
    e_pack = 457.0   # Wh at the terminals per cycle, SWC-CAL-001
    eta_motor = 0.80
    v12 = 12 / 3.6
    p12 = f_roll * v12 + k_air * v12 ** 3
    motor_w = max(p12 - p_wheel, 0) / ETA
    wh_km_flat = motor_w / eta_motor / (v12 * 3.6)
    rec("Assist battery use, flat at 12 km/h", wh_km_flat, "Wh/km")
    rec("SwapCell range, flat at 12 km/h", e_pack / wh_km_flat, "km")
    motor5 = (P_ASSIST) / eta_motor
    wh_km_5 = motor5 / (va * 3.6)
    rec("Assist battery use, 5 % climb", wh_km_5, "Wh/km")

    # ------------------------------------------------------------ 4 steering and stability
    head("4. Steering, turning circle and stability (R9, R10)")
    kp, wk, tr = P["KP_X"], P["WB"], P["TRACK"] / 2
    e = P["FORK_OFFSET"]                      # trail: each contact patch is e behind its kingpin axis
    wb = M.axle_x()                           # wheelbase, straight ahead
    lock = math.radians(P["STEER_LOCK"])

    def contact(side_y, d):
        """Contact patch of the front wheel whose kingpin is at (wk, side_y), steered d (rad, + anticlockwise)."""
        return wk - e * math.cos(d), side_y - e * math.sin(d)

    def axle_line_y(side_y, d):
        """Where the wheel's axle line (through its contact patch) meets the rear axle line (x = 0)."""
        cx, cy = contact(side_y, d)
        return cy + cx / math.tan(d)

    def threshold(lst, d_out=0.0):
        """Lateral acceleration (g) at tip-up in a left turn, outer (right) wheel steered d_out. With trail the
        outer contact patch moves out and forward as the wheels turn, so straight ahead is the lowest case."""
        m = sum(i[1] for i in lst)
        cx = sum(i[1] * i[2] for i in lst) / m; cy = sum(i[1] * i[3] for i in lst) / m
        cz = sum(i[1] * i[4] for i in lst) / m
        ox, oy = contact(-tr, d_out)            # outer (right) front contact
        L = math.hypot(ox, oy)
        dist = (cx * (-oy) + cy * ox) / L       # distance of CoM from the rear-to-outer-front axis
        return dist / cz, cx, cz

    # inner wheel at full lock: its axle line through its trailing contact patch sets the turn centre
    y_ic = axle_line_y(tr, lock)
    lo_, hi_ = math.radians(1), lock          # ideal Ackermann outer angle: outer axle line through the same centre
    for _ in range(60):
        mid = (lo_ + hi_) / 2
        if axle_line_y(-tr, mid) > y_ic:
            lo_ = mid
        else:
            hi_ = mid
    d_outer = math.degrees((lo_ + hi_) / 2)
    r_box = math.hypot(x0 + P["BOX_L"], y_ic + P["BOX_W"] / 2)
    rec("Inner wheel lock (box clearance limit)", P["STEER_LOCK"], "deg")
    rec("Outer wheel lock (ideal Ackermann, for comparison)", d_outer, "deg")
    d_built = abs(math.degrees(M._right_angle(lock)))
    rec("Outer wheel lock through the built linkage at 40 deg inner lock", d_built, "deg",
        "the trapezoid only approximates Ackermann; the turning circle below uses the built linkage")
    rec("Column (handlebar) turn at full inner lock, left wheel through the drag link", math.degrees(M._column_angle(lock)), "deg",
        "drop arm parallel to the left steering arm (FTK-DDR-003); was about 1.7 times the wheel angle")
    # built linkage: the outer wheel's axle line meets the rear axle line closer in than the inner wheel's; the tyres
    # scrub between the two. The outer wheel's own line sets the outer tyre's path (the smaller, built figure);
    # the inner wheel's line gives the larger figure (upper bound).
    db = math.radians(d_built)
    y_ic_out = axle_line_y(-tr, db)
    ocx, ocy = contact(-tr, db)
    rec("Turn centre from the centre line, outer wheel's axle line (built linkage)", y_ic_out / 1000, "m")
    rec("Turn centre from the centre line, inner wheel's axle line", y_ic / 1000, "m")
    rec("Turn centre mismatch between the front wheels (tyre scrub at full lock)", y_ic - y_ic_out, "mm")
    r_out_b = math.hypot(ocx, y_ic_out - ocy) + P["TYRE_W"] / 2
    r_outer = math.hypot(ocx, y_ic - ocy) + P["TYRE_W"] / 2
    rec("Turning circle, outer tyre, built linkage", 2 * r_out_b / 1000, "m", "R9 target 6 m")
    rec("Turning circle, outer tyre, if the turn centre stayed on the inner wheel's axle line (upper bound)",
        2 * r_outer / 1000, "m", "the inner wheel's turn centre")
    rec("Swept circle, box front corner (inner wheel's turn centre, upper bound)", 2 * r_box / 1000, "m")
    # steering lock stops (2026-10-02): the clamp plate's front inboard corner meets a stop fin at the inner lock
    xc_s, yc_s = M.stop_corner(1)
    arm_y = abs(yc_s - tr)                     # lever of a fore-and-aft contact force about the kingpin axis
    rec("Steering lock stop: met by each clamp plate at (inner wheel)", P["STEER_LOCK"], "deg",
        "constructability check in model.py --check")
    rec("Steering lock stop: lever of the contact force about the kingpin axis", arm_y, "mm")
    m_stop = 300.0 * 0.30          # N m: 300 N at one bar grip on a 300 mm half-bar, rider forcing the lock
    f_stop = m_stop / (arm_y / 1000)
    rec("Stop force, rider forcing the bar into the lock (300 N at one grip, 300 mm)", f_stop, "N",
        "one stop takes the whole bar torque; the force lies in the fin's plane")
    z0s, z1s, z2s = P["STOP_Z"]
    z_c = sum(P["CLAMP_Z"]) / 2
    rec("Stop fin lower leg, in-plane bending stress", f_stop * (z1s - z_c) / (P["T"] * P["STOP_LEG"] ** 2 / 6), "MPa",
        f"{P['STOP_LEG']:.0f} mm wide leg; yield 235 MPa")
    rec("Stop fin lower leg, out-of-plane stress from contact friction (mu 0.2)",
        0.2 * f_stop * (z1s - z_c) / (P["STOP_LEG"] * P["T"] ** 2 / 6), "MPa")
    t_bolt = f_stop * (z2s - z_c) / (z2s - (P["AB_Z0"] + 14))
    rec("Stop fin T-slot bolt tension (fin pivots on its top corner)", t_bolt, "N", "M8 8.8 preload 15.6 kN")
    # steering geometry (study decided 2026-10-02; fork direction decided by Amish 2026-10-03: forks turned to trail)
    head("4a. Steering geometry: forks turned to trail (decided 2026-10-03)")
    geo = M.steering_geometry(M.C)["left"]
    rec("Caster angle, measured on the model (knuckle head tubes vertical)", round(geo["caster"], 2) + 0.0, "deg")
    rec("Kingpin inclination, measured on the model", round(geo["kpi"], 2) + 0.0, "deg")
    rec("Scrub radius, measured on the model", round(geo["scrub"], 2) + 0.0, "mm", "steering axis in the wheel's centre plane")
    rec("Fork offset, fitted turned round (model)", e, "mm", f"buy {FORK_BUY[0]:.0f} to {FORK_BUY[1]:.0f} mm, legs parallel to the steerer")
    rec("Mechanical trail, measured on the model", geo["trail"], "mm",
        f"target {P['TRAIL_RANGE'][0]:.0f} to {P['TRAIL_RANGE'][1]:.0f} mm; checked by model.py --check")
    front_w = front * G / 2
    for lab, tr_ in (("model", geo["trail"]), (f"{FORK_BUY[0]:.0f} mm fork", FORK_BUY[0]), (f"{FORK_BUY[1]:.0f} mm fork", FORK_BUY[1])):
        rec(f"Aligning moment per wheel at 0.2 g, loaded, {lab}", front_w * 0.2 * tr_ / 1000, "N m", "centres the steering")
    t_col = 2 * front_w * 0.2 * geo["trail"] / 1000
    rec("Self-centring torque at the column, both wheels, 0.2 g, loaded", t_col, "N m", "1:1 linkage")
    rec("  as a force at each grip (300 mm half-bar, two hands)", t_col / (2 * 0.30), "N")
    front_r = (mr * xr / M.axle_x()) * G / 2
    rec("Self-centring torque at the column, rider only, 0.2 g", 2 * front_r * 0.2 * geo["trail"] / 1000, "N m")
    rec("Reference: same fork fitted as sold (crown forward), trail", -e, "mm", "pulls into the turn; not allowed")
    rec("Front wheel drop (flop) when steered, vertical axis", 0.0, "mm", "no lift or fall of the front with steering")
    rec("Gravity self-centring (needs caster or kingpin inclination)", 0.0, "N m")
    rec("Contact patch swing across at full lock (inner wheel)", e * math.sin(lock), "mm", "the rear of the inner tyre swings in")
    # tyre notch in the bed rails (2026-10-03): the rail's least section at the notch, between the bulkhead and beams
    nx0, nx1, nz = P["RAIL_NOTCH"]
    x_n = (nx0 + nx1) / 2
    h_n = P["BOX_Z0"] - nz
    bed_behind = [i for i in items if i[5] and kp < i[2] < x_n]
    m_static = abs(M_j_static(items, rider, mt, front, kp) - V_j_static(items, rider, mt, front) * (x_n - kp) / 1000
                   - sum(i[1] * G * (x_n - i[2]) for i in bed_behind) / 1000)
    box_part = (x_n - P["BOX_X0"]) / P["BOX_L"] * (CARGO + 0.0) * G       # cargo standing on the box floor behind the notch
    m_n = (m_static + box_part * (x_n - P["BOX_X0"]) / 2 / 1000) * DYN / 2  # per rail, dynamic, cargo added unfavourably
    rec("Bed rail at the tyre notch: depth of plate left", h_n, "mm", f"notch {nx0:.0f} to {nx1:.0f} mm from the rear axle")
    rec("Bed rail at the tyre notch: bending moment per rail, dynamic", m_n, "N m")
    rec("Bed rail at the tyre notch: bending stress", m_n * 1e3 / (P["T"] * h_n ** 2 / 6), "MPa", "yield 235 MPa")

    cases = {}
    for label, lst in (("loaded", items + [rider, cargo]), ("rider only", items + [rider]),
                       ("rider only, 90 kg", items + [rider[:1] + (RIDER_MAX,) + rider[2:]]),
                       (f"90 kg rider and {CARGO_MAX:.0f} kg cargo", items + [rider[:1] + (RIDER_MAX,) + rider[2:],
                                                                         cargo[:1] + (CARGO_MAX,) + cargo[2:]])):
        a0, cx, cz = threshold(lst)
        cases[label] = (a0, cx)
        rec(f"Tipping threshold, {label}, any lock", a0, "g", f"CoM {cx/1000:.2f} m ahead, {cz/1000:.2f} m high")
        rec(f"  speed at threshold on a 5 m radius, {label}", math.sqrt(a0 * G * 5) * 3.6, "km/h")
    for label in ("loaded", "rider only"):
        a0, cx = cases[label]
        rc = math.hypot(cx, y_ic)
        rec(f"  tip-up speed at full lock, {label}", math.sqrt(a0 * G * rc / 1000) * 3.6, "km/h",
            f"CoM path radius {rc/1000:.2f} m")
    a_r, cx_r = cases["rider only"]
    rc = math.hypot(cx_r, y_ic)
    label_kmh = math.floor(math.sqrt(0.7 * a_r * G * rc / 1000) * 3.6)
    rec("Cornering-speed label, empty, full-lock turns (70 % of tip-up lateral acceleration, rounded down)",
        float(label_kmh), "km/h")
    rec("Cornering-speed label, empty, 10 m radius turns (same rule)",
        float(math.floor(math.sqrt(0.7 * a_r * G * 10) * 3.6)), "km/h")
    ballast = None
    for kg in range(0, 200, 5):
        lst = items + [rider, ("Ballast", float(kg), x0 + P["BOX_L"] / 2, 0.0, P["BOX_Z0"] + 30, True)]
        if threshold(lst)[0] >= 0.30:
            ballast = kg; break
    rec("Ballast low in the box for 0.30 g rider only (sensitivity)", float(ballast), "kg")

    # ------------------------------------------------------------ 5 structure
    head("5. Structure (R2)")
    t = P["T"]
    # 5.1 rear stays as a two-member truss from the rear axle to the seat node and the front node
    R_rear = (mt - front) * G
    ax_, az_ = 0.0, P["WHEEL_R"]
    seat_node = tuple(sum(c) / 2 for c in zip(*M.NODES[:2]))      # the two rear stay-to-spine bolts
    front_node = tuple(sum(c) / 2 for c in zip(*M.NODES[2:]))     # the two front ones
    ut = ((seat_node[0] - ax_), (seat_node[1] - az_)); lt = math.hypot(*ut); ut = (ut[0] / lt, ut[1] / lt)
    ub = ((front_node[0] - ax_), (front_node[1] - az_)); lb = math.hypot(*ub); ub = (ub[0] / lb, ub[1] / lb)
    import numpy as np
    A = np.array([[ut[0], ub[0]], [ut[1], ub[1]]]); F = np.linalg.solve(A, np.array([0.0, -R_rear]))
    Ft, Fb = float(F[0]), float(F[1])
    rec("Rear axle load, loaded (static)", R_rear, "N")
    rec("Upper stay strip force (both plates, static)", Ft, "N", "negative = compression")
    rec("Lower stay strip force (both plates, static)", Fb, "N")
    comp = abs(Ft) / 2 * DYN
    rec("Compression per plate, dynamic x2.5", comp, "N")
    (ex0, ez0), (ex1, ez1) = M.STAY[-1], M.STAY[-2]          # upper edge of the stay plate
    le = math.hypot(ex1 - ex0, ez1 - ez0); nx_, nz_ = -(ez1 - ez0) / le, (ex1 - ex0) / le
    b_strip = min(abs((wx - ex0) * nx_ + (wz - ez0) * nz_) for wx, wz in M.STAY_WIN)
    rec("Narrowest upper stay strip (edge to window)", b_strip, "mm")
    I_s = b_strip * t ** 3 / 12
    for L_u, lab in ((lt, "if unbraced from axle to seat node"), (300.0, "braced by the stay bridge (300 mm)")):
        pcr = math.pi ** 2 * E * I_s / L_u ** 2
        rec(f"Strip buckling load, {lab}", pcr, "N", f"L = {L_u:.0f} mm, pinned ends")
        rec(f"  safety factor on dynamic compression, {lab}", pcr / comp, "")
    b55 = 55.0
    rec("Safety factor with the TRL 2 style 55 mm strip, braced", math.pi ** 2 * E * b55 * t ** 3 / 12 / 300 ** 2 / comp, "")
    sig_strip = abs(Ft) / 2 / ((b_strip - 8.5) * t)
    rec("Static net stress in upper strip at an M8 hole", sig_strip, "MPa")
    rec("Dynamic net stress in upper strip", sig_strip * DYN, "MPa")

    # 5.2 spine torsion from roll of the rear frame (rider and rear frame at 0.5 g lateral)
    rear_frame = [i for i in items if not i[5]] + [rider]
    mrf, _, _, zrf = com(rear_frame)
    Troll = mrf * 0.5 * G * zrf / 1000
    rec("Rear frame and rider mass", mrf, "kg")
    rec("Roll moment at the kingpin, 0.5 g lateral", Troll, "N m")
    h_sp = 150.0; w_sp = 2 * P["SPINE_IN"] + t
    J_open = 2 * (1 / 3) * h_sp * t ** 3
    tau_open = Troll * 1e3 * t / J_open
    A_cell = (w_sp) * (h_sp - t)
    tau_closed = Troll * 1e3 / (2 * A_cell * t)
    rec("Spine shear stress, open twin plates (TRL 2)", tau_open, "MPa", "yield in shear about 136 MPa")
    rec("Spine shear stress, closed box with covers (TRL 3)", tau_closed, "MPa")
    q = Troll * 1e3 / (2 * A_cell)
    s_closed = (720.0 - M.SPINE[0][0]) / ((M.SPINE[1][0] - M.SPINE[0][0]) / math.dist(M.SPINE[0], M.SPINE[1]))
    L_closed = math.dist(M.SPINE[0], M.SPINE[1]) - s_closed
    n_tabs = sum(1 for k, s_ in M.ST_TOP if k == "tab" and s_ >= s_closed)
    rec("Shear flow on each cover edge", q, "N/mm")
    rec(f"Tab bearing stress, {n_tabs} tabs per edge over {L_closed:.0f} mm of closed box (3 x 3 mm bearing face)",
        q * L_closed / n_tabs / (t * t), "MPa")
    Gs = 81e3
    k_open = Gs * J_open / 1e6; k_closed = Gs * 4 * A_cell ** 2 * t / (2 * (w_sp + h_sp)) / 1e6
    rec("Spine torsional stiffness GJ, open", k_open, "N m2")
    rec("Spine torsional stiffness GJ, closed", k_closed, "N m2")

    # 5.3 bed-to-spine joint (fixed bed, FTK-DDR-002 item 13) and spine bending
    rear_lst = [i for i in items if not i[5]] + [rider]
    W_rf = sum(i[1] for i in rear_lst) * G
    R_r = (mt - front) * G
    V_j = W_rf - R_r
    M_j = R_r * kp - sum(i[1] * G * (kp - i[2]) for i in rear_lst)
    rec("Vertical shear at the bed-to-spine joint, loaded (static)", V_j, "N", "negative = bed lifts the rear frame")
    rec("Pitch moment at the bed-to-spine joint, loaded (static)", M_j / 1000, "N m")
    brake_h = 0.5 * G * mrf
    M_sp = ((abs(M_j) + abs(V_j) * (kp - front_node[0])) * DYN + brake_h * 0.25 * 1000) / 1000
    Z_box = 2 * t * h_sp ** 2 / 6 + 2 * w_sp * t * (h_sp / 2) / 1  # webs plus covers, mm3 (approx.)
    rec("Spine bending moment at the front node (dynamic plus 0.5 g braking)", M_sp, "N m")
    rec("Spine bending stress", M_sp * 1e3 / Z_box, "MPa")

    # 5.4 front axle beam and knuckle posts
    w_front = front * G * DYN
    span = 2 * P["POST_Y0"]
    M_ab = w_front * (span / 1000) / 8
    hab = P["BOX_Z0"] - P["AB_Z0"]
    hw_ = hab - 44.0                                      # lightening windows, 22 mm of plate above and below
    Z_ab = 2 * t * (hab ** 3 - hw_ ** 3) / (6 * hab)      # twin plates with lightening windows
    rec("Front load, dynamic", w_front, "N")
    rec(f"Axle beam bending stress (twin 3 x {hab:.0f} mm, UDL over {span:.0f} mm)", M_ab * 1e6 / Z_ab / 1000, "MPa")
    p_w = w_front / 2
    py1 = P["POST_Y0"] + P["POST_W"]
    rec("Knuckle load per wheel, dynamic", p_w, "N")
    d_top = P["KN_LEN"]                                   # the knuckle head tube's own length of plate, solid
    I_cant = 2 * t * d_top ** 3 / 12
    rec("Knuckle post cantilever stress at its root (two plates, 120 mm deep)",
        p_w * (tr - py1 - 10) / (I_cant / (d_top / 2)), "MPa")
    lo_ring = 22.5; span_c = 2 * P["POST_X"]
    rec("Lower knuckle collar plate: cup flange radius against the plate supports (half span)", span_c / 2 - lo_ring, "mm",
        "the flange bears on the plate within 2.5 mm of the transverse plates' edges, so the plate is not bent")
    bw = P["POST_W"]
    I_col = 2 * t * bw ** 3 / 12 + 2 * (2 * P["POST_X"]) * t * (bw / 2 - t / 2) ** 2
    m_col = p_w * (tr - (P["POST_Y0"] + bw / 2))
    rec("Knuckle post column bending moment", m_col / 1000, "N m")
    rec(f"Knuckle post column stress (closed {bw:.0f} x {2 * P['POST_X']:.0f} mm box of 3 mm plate)", m_col / (I_col / (bw / 2)), "MPa")
    rec("Column stress if the cheeks were left out (two plates only)", m_col / (2 * t * bw ** 2 / 6), "MPa")
    rec("Knuckle headset axial load, dynamic", p_w, "N")

    # 5.5 head tube joint under the roll moment (item 19: longer head tube)
    rec("Joint couple at the head tube, 0.5 g roll, 150 mm head tube (TRL 3, v0.1)", Troll / 0.150, "N")
    couple = Troll / (P["HT_LEN"] / 1000)
    rec(f"Joint couple at the head tube, 0.5 g roll, {P['HT_LEN']:.0f} mm head tube", couple, "N",
        "carried by the cups into the yokes and by the yokes' tabs into the spine side plates")
    rec("Bearing stress, roll couple on one yoke's two tabs (16 x 3 mm side faces)", couple / (2 * 16 * t), "MPa")

    # 5.6 bolted joints
    slip = MU_SLIP * BOLT_PRELOAD
    rec("M8 8.8 preload at 25 N m", BOLT_PRELOAD, "N")
    rec("Slip load per bolt per faying face (mu 0.20)", slip, "N")
    node_force = max(abs(Ft), abs(Fb)) / 2 * DYN
    rec("Stay node force per plate, dynamic", node_force, "N")
    rec("Bolts per plate per node for no slip (1 face; spacer stack in series)", math.ceil(node_force / slip), "")
    bearing = 2.5 * 360 * 8 * t / 1.25
    rec("Bearing resistance of 3 mm plate at one M8 bolt", bearing, "N")
    rec("Bearing utilisation if the node slips onto 2 bolts", node_force / (2 * bearing) * 100, "%")

    # 5.7 fatigue screening
    rng_road = sig_strip * 1.0
    rng_big = sig_strip * (DYN - 1) * 2
    rec("Stress range, routine road cycle (+/- 0.5 g)", rng_road, "MPa")
    rec("Stress range, pothole cycle (to 2.5 g and back)", rng_big, "MPa")
    rec("Constant-amplitude fatigue limit, 90 MPa detail", FAT_CAFL, "MPa")
    rec("Cycles in 5 years (300 days, 20 km, 1 per 10 m)", 5 * 300 * 20 * 100.0, "")
    # proof load
    proof = (2 * CARGO) * G
    rec(f"Proof load, twice rated cargo ({CARGO:.0f} kg) (R2)", proof, "N")
    rec("Axle beam stress under proof load", proof / 2 * (span / 1000) / 8 * 2 * 1e6 / Z_ab / 1000, "MPa")

    # ------------------------------------------------------------ 6 braking and parking
    head("6. Braking and parking (R11)")
    v15 = 15 / 3.6
    decel = v15 ** 2 / (2 * 6.0)
    rec("Kinetic energy at 15 km/h, gross", 0.5 * gross * v15 ** 2 / 1000, "kJ")
    rec("Deceleration to stop in 6 m (no reaction time)", decel, "m/s2")
    rec("Deceleration to stop in 6 m with 0.5 s reaction", v15 ** 2 / (2 * (6.0 - v15 * 0.5)), "m/s2")
    rec("Drum torque needed per wheel, equal share", gross * decel * R / 3, "N m")
    rec("Tyre grip needed at the front pair alone", gross * decel / (front * G), "", "friction coefficient")
    f_hold = gross * G * math.sin(math.atan(0.10))
    rec("Parking force on a 10 % grade", f_hold, "N")
    rec("Drum torque per front wheel to park (latch on the front pair)", f_hold * R / 2, "N m")
    p_desc = gross * G * 0.05 * (10 / 3.6) - f_roll * (10 / 3.6) - k_air * (10 / 3.6) ** 3
    rec("Brake power, 10 km/h down a 5 % grade", p_desc, "W")
    C_drum = 0.35 * 460 + 0.30 * 900
    hA = 0.5
    dT_ss = p_desc / 3 / hA
    tau = C_drum / hA
    t100 = -tau * math.log(1 - 100 / dT_ss) if dT_ss > 100 else float("inf")
    rec("Drum heat capacity per wheel (0.35 kg iron, 0.30 kg aluminium)", C_drum, "J/K")
    rec("Steady drum temperature rise (hA 0.5 W/K)", dT_ss, "K")
    rec("Time to a 100 K rise", t100 / 60, "min")
    rec("Descent length to a 100 K rise at 10 km/h", t100 * 10 / 3.6 / 1000, "km")

    # ------------------------------------------------------------ 7 assembly, repair, life
    head("7. Assembly, repair and service life (R7, R14, R16)")
    t_bolt = 1.5
    t_other = {"wheels (3)": 30, "steering column, two knuckle headsets and forks, tie rod, drag link": 50,
               "headset and bottom bracket cups pressed and screwed in": 20, "seat tube, spacer tubes, U-bolts": 15,
               "drivetrain and chain": 25, "brakes and cables": 30,
               "seat and bars": 10, "box to bed": 20, "deburr check and final torque": 30}
    t_total = n_bolts * t_bolt + sum(t_other.values())
    rec("Assembly work content", t_total / 60, "person-h")
    rec("Elapsed time, two people (70 % parallel)", t_total / 60 * (1 - 0.7 / 2), "h", "R7 target 4 h")
    J = M.JOINTS
    side = "Spine side plate, left"

    def jb(cond):
        return sum(j["bolts"] for j in J if cond(j))
    # a side plate's edge tabs sit in the covers and the lower yoke, so those come off; ribs, saddles and the upper
    # yoke stay on the other plate; the steering column and the bottom bracket come out
    spine_bolts = (jb(lambda j: j["group"] in ("Spine top cover", "Spine bottom cover", "Lower yoke to spine"))
                   + jb(lambda j: j["group"] == "Yokes to bulkhead" and j["edge"] == "Lower yoke")
                   + jb(lambda j: j["group"] in ("Upper yoke to spine", "Spine ribs", "Seat tube saddles") and j["face"] == side)
                   + len(M.NODES))
    rec("Bolts disturbed to replace one spine side plate", spine_bolts, "")
    rec("Time to replace one spine side plate (0.75 min per bolt each way, 15 min, 20 min for the column and bottom bracket)",
        spine_bolts * 0.75 * 2 + 35, "min", "R14 target 90 min for the spine side plates only")
    kp_plate = "Knuckle post plate, left rear"
    kn_bolts = jb(lambda j: j["group"] == "Knuckle collar plates" and j["face"].startswith("Knuckle collar plate, left")) \
        + jb(lambda j: j["group"] == "Knuckle post corners" and kp_plate in (j["face"], j["edge"]))
    rec("Bolts disturbed to replace one knuckle post plate (both collar plates come off)", kn_bolts, "")
    rec("Time to replace one knuckle post plate (0.75 min per bolt each way, 15 min, 20 min for wheel, fork and cups)",
        kn_bolts * 0.75 * 2 + 35, "min", f"R14 target {R14_KN_MIN:.0f} min for a knuckle post plate (2026-10-02)")
    rec("Margin under R14 for a knuckle post plate", R14_KN_MIN - (kn_bolts * 0.75 * 2 + 35), "min")
    for cat, rate in (("C3", 50.0), ("C4", 80.0)):
        rec(f"Unprotected loss, 5 years at the {cat} first-year upper rate (both faces)",
            rate * 5 ** 0.6 * 2 / 1000, "mm", "bilogarithmic law, exponent 0.6 assumed")

    # ------------------------------------------------------------ 8 cost
    head("8. Cost (R15, R18)")
    rows = list(csv.DictReader(open(ROOT / "bom/bom.csv")))
    base = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if "Optional" not in r["item"])
    opt = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if "Optional" in r["item"])
    rec("BOM lines", len(rows))
    rec("Base prototype, pedal only (bom.csv)", base, "USD", "budget 800")
    rec("Budget margin", 800 - base, "USD")
    rec("Optional assist kit, route C, excluding the SwapCell pack", opt, "USD")
    # production at 100 units
    cut_len = 0.0
    for p_ in M.PLATES:
        w, h = p_["size"]
        cut_len += 2 * (w + h) * 1.6   # perimeter plus windows and holes, factor from the profiles
    sheet_kg = 1.25 * 2.5 * t / 1000 * RHO_STEEL
    rec("Cut length per frame (estimate)", cut_len / 1000, "m")
    steel_usd = sheet_kg * 1.0
    cut_usd = cut_len / 1000 * 0.30
    rec("Steel, one full sheet at 1.0 USD/kg", steel_usd, "USD")
    rec("Laser cutting at 0.30 USD/m (volume rate, assumed)", cut_usd, "USD")
    bought = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows
                 if r["make_buy"] == "buy" and "Optional" not in r["item"])
    carp = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].startswith("9 "))
    prod = steel_usd + cut_usd + 0.65 * bought + 0.6 * carp + 15
    rec("Bought parts at 65 % of prototype retail", 0.65 * bought, "USD")
    rec("Production cost at 100 units (parts, cutting, 15 USD assembly labour)", prod, "USD", "R18 target 300")

    with open(ROOT / "docs/04-calcs/results.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["quantity", "value", "unit", "note"])
        for k, v_, u, n in OUT:
            w.writerow([k, f"{v_:.4g}" if isinstance(v_, float) else v_, u, n])
    print("\nwrote docs/04-calcs/results.csv")


if __name__ == "__main__":
    main()
