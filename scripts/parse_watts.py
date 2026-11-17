#!/usr/bin/env python3
"""
Parse the digitized Watts (1963) limb charts, VizieR catalogue VI/122
(USNO grid version of the HMNAO digitisation), into a numpy array.

Source file : data/watts.dat.gz  (CDS file watts.dat, no CR/LF)
Layout      : per VI/122 ReadMe + doc.txt (Herald 2006):
              6-byte fields: bytes 1-4 = signed height in 0.01 arcsec
              (sign in byte 1), byte 5 = accuracy code a, byte 6 = code b.
              Blocks: 91 longitude librations L = +9.0 .. -9.0 (0.2 deg steps),
                      81 latitude  librations B = +8.0 .. -8.0 (0.2 deg steps),
                      1800 Watts angles WA = 0.0 .. 359.8 (0.2 deg steps).
              Total valid records 13,267,800, plus one trailing block of
              1800 zero-height records (doc.txt section 2).
Output      : data/watts_grid.npz with
                h      float32 [91, 81, 1800] heights in arcsec (mean distance)
                code_a uint8   [91, 81, 1800]
                code_b uint8   [91, 81, 1800]
                L_vals, B_vals, WA_vals (degrees)
Heights are as tabulated: angular height above the Watts datum at the
Moon's mean distance (doc.txt section 6a; mean distance 384,400 km).
"""
import gzip
import numpy as np
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

NL, NB, NWA = 91, 81, 1800
NVALID = NL * NB * NWA          # 13,267,800
NTOTAL = NVALID + 1800          # + trailing zero block


def main():
    path = os.path.join(DATA, "watts.dat.gz")
    with gzip.open(path, "rb") as f:
        raw = f.read()
    print(f"decompressed bytes: {len(raw)}  expected: {NTOTAL * 6}")
    assert len(raw) == NTOTAL * 6, "unexpected file size"

    arr = np.frombuffer(raw, dtype=np.uint8).reshape(NTOTAL, 6)
    # bytes 1-4: Fortran I4 signed height in 0.01 arcsec, right-justified
    # and SPACE-padded (e.g. '- 70' = -0.70 arcsec); sign in byte 1.
    sign = np.where(arr[:, 0] == ord('-'), -1, 1)
    d = arr[:, 1:4].astype(np.int32)
    d = np.where(d == 32, 48, d)  # leading spaces -> '0'
    digits = (d[:, 0] - 48) * 100 + (d[:, 1] - 48) * 10 + (d[:, 2] - 48)
    h = (sign * digits).astype(np.float32) * 0.01
    code_a = arr[:, 4] - 48
    code_b = arr[:, 5] - 48
    assert digits.min() >= 0 and digits.max() <= 999, "digit parse failure"
    assert code_a.min() >= 0 and code_a.max() <= 7
    assert code_b.min() >= 0 and code_b.max() <= 7

    # trailing block must be all-zero heights (doc.txt)
    tail = h[NVALID:]
    print(f"trailing block: n={tail.size}, all zero: {bool(np.all(tail == 0))}")

    h = h[:NVALID].reshape(NL, NB, NWA)
    code_a = code_a[:NVALID].reshape(NL, NB, NWA)
    code_b = code_b[:NVALID].reshape(NL, NB, NWA)

    L_vals = 9.0 - 0.2 * np.arange(NL)
    B_vals = 8.0 - 0.2 * np.arange(NB)
    WA_vals = 0.2 * np.arange(NWA)

    print(f"height range: {h.min():.2f} .. {h.max():.2f} arcsec")
    print(f"height mean : {h.mean():+.4f} arcsec   std: {h.std():.4f}")
    # spot check: profile at L=0, B=0 (nearest grid point: L index 45, B index 40)
    prof = h[45, 40]
    print(f"L=0,B=0 profile: mean {prof.mean():+.3f}, "
          f"h(WA=0)={prof[0]:+.2f}, h(WA=90)={prof[450]:+.2f}, "
          f"h(WA=180)={prof[900]:+.2f}, h(WA=270)={prof[1350]:+.2f}")

    out = os.path.join(DATA, "watts_grid.npz")
    np.savez_compressed(out, h=h, code_a=code_a, code_b=code_b,
                        L_vals=L_vals, B_vals=B_vals, WA_vals=WA_vals)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
