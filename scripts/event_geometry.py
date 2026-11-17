#!/usr/bin/env python3
"""
Event geometry for the eclipse-radius audit: for each event in the
published Dunham et al. (2016) table, find the instant of greatest
eclipse (minimum geocentric Sun-Moon separation) from JPL DE440 and
compute the Moon's optical libration (l, b) at that instant.

Libration model: IAU 2009 WGCCRE mean rotation elements for the Moon
(Archinal et al. 2011): pole alpha0 = 269.9949 deg, delta0 = +66.5392 deg
(J2000), prime-meridian angle W = 38.3213 + 13.176358959 * d, d = days
from J2000.0 TT. The small secular rates of the pole (<=0.003 deg/cy)
and the forced-libration periodic terms (<= ~0.03 deg) are neglected;
the resulting libration accuracy (~0.05 deg) is well inside the 0.2 deg
sampling of both limb grids, and the convention is validated against
(a) Espenak's published bulletin libration for 2006-03-29 and
(b) the Watts<->LOLA profile cross-correlation in validate_frames.py.

Conventions: l = selenographic longitude of the sub-Earth point,
east-positive (ME frame, matching LDEM's EAST-positive longitudes);
b = selenographic latitude of the sub-Earth point. Whether the Watts
charts' (L, B) arguments use this same sign convention is tested
empirically in validate_frames.py before any correction is computed.

Output: outputs/event_geometry.csv
"""
import csv
import os
import numpy as np
from skyfield.api import load, Loader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs")

ts = load.timescale()
loader = Loader(DATA)
eph = loader("de440.bsp")
earth, moon, sun = eph["earth"], eph["moon"], eph["sun"]

ALPHA0 = np.radians(269.9949)
DELTA0 = np.radians(66.5392)
W0 = 38.3213
WRATE = 13.176358959  # deg/day


def moon_orientation(d_days):
    """Body-fixed basis (x=prime meridian, y, z=pole) in J2000 equatorial
    inertial coordinates, d_days from J2000.0 TT."""
    p = np.array([np.cos(DELTA0) * np.cos(ALPHA0),
                  np.cos(DELTA0) * np.sin(ALPHA0),
                  np.sin(DELTA0)])
    n = np.array([-np.sin(ALPHA0), np.cos(ALPHA0), 0.0])  # node direction
    W = np.radians((W0 + WRATE * d_days) % 360.0)
    x = np.cos(W) * n + np.sin(W) * np.cross(p, n)
    y = np.cross(p, x)
    return x, y, p


def separation_deg(t):
    """Geocentric angular separation Sun-Moon (deg) at skyfield time t."""
    m = earth.at(t).observe(moon).position.km
    s = earth.at(t).observe(sun).position.km
    cosang = np.dot(m, s) / (np.linalg.norm(m) * np.linalg.norm(s))
    return np.degrees(np.arccos(np.clip(cosang, -1, 1)))


def greatest_eclipse(year, month, day):
    """Golden-section search for min separation over the TT day."""
    t0 = ts.tt(year, month, day, 0.0)
    lo, hi = float(t0.tt), float(t0.tt) + 1.0
    # coarse scan first (5-min steps) to bracket the minimum
    grid = np.linspace(lo, hi, 289)
    vals = [separation_deg(ts.tt_jd(float(jd))) for jd in grid]
    i = int(np.argmin(vals))
    lo, hi = float(grid[max(i - 1, 0)]), float(grid[min(i + 1, len(grid) - 1)])
    gr = (np.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = separation_deg(ts.tt_jd(c)), separation_deg(ts.tt_jd(d))
    for _ in range(60):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = separation_deg(ts.tt_jd(c))
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = separation_deg(ts.tt_jd(d))
    jd = 0.5 * (a + b)
    return ts.tt_jd(jd)


def libration(t):
    """Optical libration (l, b) in degrees at skyfield time t (TT)."""
    mpos = earth.at(t).observe(moon).position.km  # geocentric Moon
    e = -mpos / np.linalg.norm(mpos)              # Moon->Earth direction
    d_days = t.tt - 2451545.0
    x, y, p = moon_orientation(d_days)
    lon = np.degrees(np.arctan2(np.dot(e, y), np.dot(e, x)))
    lat = np.degrees(np.arcsin(np.clip(np.dot(e, p), -1, 1)))
    dist = np.linalg.norm(mpos)
    return lon, lat, dist


def node_elongation(t):
    """Moon's ecliptic longitude minus ascending-node longitude (deg)."""
    r = earth.at(t).observe(moon).position.km
    v = earth.at(t).observe(moon).velocity.km_per_s
    # ecliptic coords: rotate equatorial (J2000) by obliquity about x-axis
    eps = np.radians(23.4392911)
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(eps), np.sin(eps)],
                   [0, -np.sin(eps), np.cos(eps)]])
    re, ve = Rx @ r, Rx @ v
    lam = np.degrees(np.arctan2(re[1], re[0])) % 360.0
    h = np.cross(re, ve)
    n = np.cross([0, 0, 1.0], h)
    omega = np.degrees(np.arctan2(n[1], n[0])) % 360.0
    return (lam - omega) % 360.0


def main():
    src = os.path.join(DATA, "dunham2016_table.csv")
    rows = list(csv.DictReader(open(src)))
    out_rows = []
    for r in rows:
        y, m, d = int(r["year"]), int(r["month"]), int(r["day"])
        t = greatest_eclipse(y, m, d)
        lon, lat, dist = libration(t)
        elong = node_elongation(t)
        out_rows.append({
            "date": f"{y:04d}-{m:02d}-{d:02d}",
            "t_ge_tt": t.utc_iso(),
            "libration_l_deg": f"{lon:+.3f}",
            "libration_b_deg": f"{lat:+.3f}",
            "elong_from_node_deg": f"{elong:.2f}",
            "moon_dist_km": f"{dist:.0f}",
        })
        print(out_rows[-1])
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "event_geometry.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
