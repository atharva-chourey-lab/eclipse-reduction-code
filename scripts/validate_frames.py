#!/usr/bin/env python3
"""
Frame-convention validation: pin down how the Watts grid's (L, B, WA)
arguments map onto the modern (l, b, Axis Angle) frame, empirically.

The two datasets depict the same physical limb, so under the correct
convention the Watts profile and the LOLA profile for the same event
must correlate strongly (they differ by the datum systematic under
audit, ~0.1-0.4 arcsec, on top of ~1 arcsec of common topography).
Wrong sign conventions decorrelate them. We scan: Watts lookup at
(L, B) in {(l,b), (-l,b), (l,-b), (-l,-b)} x angle map WA = AA + shift
for shift in {+0.21, 0.0, -0.21} deg, plus the reversed-axis map
WA = -AA + 0.21. Pearson r over all 1800 bins decides.

Watts sampling at arbitrary (L, B): bilinear in (L, B) on the native
0.2 deg grid, then periodic linear interpolation in WA.
"""
import csv
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs")


def watts_profile(w, L, B, wa_query):
    """Bilinear-in-(L,B) Watts profile sampled at wa_query (deg, any range)."""
    h, Lv, Bv = w["h"], w["L_vals"], w["B_vals"]
    # grid is descending in L and B; convert query to fractional indices
    fi = (Lv[0] - L) / 0.2
    fj = (Bv[0] - B) / 0.2
    i0, j0 = int(np.floor(fi)), int(np.floor(fj))
    ti, tj = fi - i0, fj - j0
    i0 = min(max(i0, 0), len(Lv) - 2)
    j0 = min(max(j0, 0), len(Bv) - 2)
    prof = ((1 - ti) * (1 - tj) * h[i0, j0] + ti * (1 - tj) * h[i0 + 1, j0]
            + (1 - ti) * tj * h[i0, j0 + 1] + ti * tj * h[i0 + 1, j0 + 1])
    wa = np.mod(wa_query, 360.0)
    x = wa / 0.2
    k0 = np.floor(x).astype(int) % 1800
    k1 = (k0 + 1) % 1800
    tk = x - np.floor(x)
    return (1 - tk) * prof[k0] + tk * prof[k1]


def main():
    w = np.load(os.path.join(DATA, "watts_grid.npz"))
    lp = np.load(os.path.join(DATA, "lola_profiles.npz"))
    geom = {r["date"]: r for r in
            csv.DictReader(open(os.path.join(OUT, "event_geometry.csv")))}
    dates = list(lp["dates"])
    AA = lp["AA_vals"]
    for date in ["2006-03-29", "1999-08-11", "1973-06-30"]:
        i = dates.index(date)
        lola = lp["h"][i].astype(np.float64)
        l, b = float(geom[date]["libration_l_deg"]), float(geom[date]["libration_b_deg"])
        print(f"\n=== {date}  l={l:+.2f} b={b:+.2f} ===")
        results = []
        for sL, sB in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            for shift in [0.21, 0.0, -0.21]:
                wp = watts_profile(w, sL * l, sB * b, AA + shift)
                r = np.corrcoef(wp, lola)[0, 1]
                results.append((r, f"L*{sL:+d} B*{sB:+d} WA=AA{shift:+.2f}"))
            wp = watts_profile(w, sL * l, sB * b, -AA + 0.21)
            r = np.corrcoef(wp, lola)[0, 1]
            results.append((r, f"L*{sL:+d} B*{sB:+d} WA=-AA+0.21"))
        for r, label in sorted(results, reverse=True):
            print(f"  r = {r:+.3f}   {label}")


if __name__ == "__main__":
    main()
