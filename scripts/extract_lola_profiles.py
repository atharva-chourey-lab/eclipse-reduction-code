#!/usr/bin/env python3
"""
Extract modern limb profiles from the LOLA LDEM_128 global grid
(NASA PDS, LRO-L-LOLA-4-GDR-V1.0 V3.0) at each archive event's
libration, in the same format as the Watts profiles: angular height
(arcsec) above the reference limb vs Axis Angle (0.2 deg steps).

Method (silhouette / max-projected-radius construction, cf. Wright &
Young 2024, AJ 168:163, sec. 4): for sub-Earth point (l, b) (ME frame,
east-positive longitude), every DEM pixel gets Moon-fixed unit vector u
and radius r. Pixels within +/-14 deg of the limb plane (u . e ~ 0) are
projected onto the sky plane perpendicular to the Earth direction e;
in each 0.2 deg Axis Angle bin the limb radius is the maximum projected
radius. Axis Angle is measured from the projected lunar north pole,
eastward (toward the selenographic-east limb point), matching the
definition used by Occult / Herald ("measured eastward from the Moon's
north pole", Sigismondi et al. 2011).

Heights are expressed as in the Kaguya/Watts convention: angular height
above a mean limb of radius 1737.4 km centred on the centre of mass,
with the Moon at its mean distance 384,398.55 km
(1 km = 0.536605 arcsec). LDEM radii are relative to the same 1737.4 km
sphere (label OFFSET), in the DE421 Mean-Earth frame; the DE421->DE440
frame difference is arcsec-level and negligible at 0.2 deg sampling.

Grid geometry (from ldem_128.lbl): 23040 lines x 46080 samples,
simple cylindrical, pixel-registered; lat = (11519.5 - row)/128,
lon_east = (col - 23039.5)/128; radius_m = DN*0.5 + 1737400.

Output: data/lola_profiles.npz with h [27, 1800] float32 arcsec,
AA_vals, and the event dates.
"""
import csv
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs")

NLINES, NSAMP, PPD = 23040, 46080, 128
R_REF_KM = 1737.4
MEAN_DIST_KM = 384398.55
ARCSEC_PER_KM = 206264.806 / MEAN_DIST_KM
BAND = np.sin(np.radians(14.0))
NBIN = 1800


def extract_profile(dem, l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    e = np.array([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)])
    pole = np.array([0.0, 0.0, 1.0])
    yhat = pole - np.dot(pole, e) * e
    yhat /= np.linalg.norm(yhat)
    # east reference: surface point at lon l+90, lat b
    ue = np.array([np.cos(b) * np.cos(l + np.pi / 2),
                   np.cos(b) * np.sin(l + np.pi / 2), np.sin(b)])
    xhat = np.cross(yhat, e)
    if np.dot(xhat, ue) < 0:
        xhat = -xhat
    xhat /= np.linalg.norm(xhat)

    lats = np.radians((11519.5 - np.arange(NLINES)) / PPD)
    lons = np.radians((np.arange(NSAMP) - 23039.5) / PPD)
    coslat, sinlat = np.cos(lats), np.sin(lats)
    coslon, sinlon = np.cos(lons), np.sin(lons)
    # per-column part of u.e and of the sky-plane coords
    ue_col = e[0] * coslon + e[1] * sinlon          # times coslat
    ux_col = xhat[0] * coslon + xhat[1] * sinlon    # times coslat
    uy_col = yhat[0] * coslon + yhat[1] * sinlon    # times coslat

    best = np.full(NBIN, -np.inf, dtype=np.float64)
    rows_per_block = 720
    for r0 in range(0, NLINES, rows_per_block):
        r1 = min(r0 + rows_per_block, NLINES)
        dn = dem[r0:r1].astype(np.float32)
        r_km = (dn * 0.5 + 1737400.0) / 1000.0
        cl = coslat[r0:r1][:, None]
        sl = sinlat[r0:r1][:, None]
        ue = cl * ue_col[None, :] + e[2] * sl
        mask = np.abs(ue) <= BAND
        if not mask.any():
            continue
        ri, ci = np.nonzero(mask)
        ue_b = ue[ri, ci]
        ux = cl[ri, 0] * ux_col[ci] + xhat[2] * sl[ri, 0]
        uy = cl[ri, 0] * uy_col[ci] + yhat[2] * sl[ri, 0]
        rho = r_km[ri, ci] * np.sqrt(np.clip(1.0 - ue_b * ue_b, 0.0, None))
        aa = np.degrees(np.arctan2(ux, uy)) % 360.0
        bins = (aa / 0.2).astype(np.int32)
        np.maximum.at(best, bins, rho)
    empty = int(np.sum(~np.isfinite(best)))
    if empty:
        idx = np.arange(NBIN)
        good = np.isfinite(best)
        best = np.interp(idx, idx[good], best[good], period=NBIN)
    h = (best - R_REF_KM) * ARCSEC_PER_KM
    return h.astype(np.float32), empty


def main():
    dem = np.memmap(os.path.join(DATA, "LDEM_128.IMG"), dtype="<i2",
                    mode="r", shape=(NLINES, NSAMP))
    rows = list(csv.DictReader(open(os.path.join(OUT, "event_geometry.csv"))))
    profiles = np.zeros((len(rows), NBIN), dtype=np.float32)
    dates = []
    for i, r in enumerate(rows):
        l, b = float(r["libration_l_deg"]), float(r["libration_b_deg"])
        h, empty = extract_profile(dem, l, b)
        profiles[i] = h
        dates.append(r["date"])
        print(f"{r['date']}  l={l:+.2f} b={b:+.2f}  "
              f"profile mean {h.mean():+.3f}  min {h.min():+.2f}  "
              f"max {h.max():+.2f}  empty bins {empty}", flush=True)
    np.savez_compressed(os.path.join(DATA, "lola_profiles.npz"),
                        h=profiles, AA_vals=0.2 * np.arange(NBIN),
                        dates=np.array(dates))
    print("wrote data/lola_profiles.npz")


if __name__ == "__main__":
    main()
