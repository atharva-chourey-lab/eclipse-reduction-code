#!/usr/bin/env python3
"""
Main analysis for the eclipse-radius audit, implementing PREDICTION.md
exactly as registered:

  delta(theta, lib) = h_new(theta, lib) - h_Watts(theta, lib)   [arcsec]
  deltaR_corr(e)    = deltaR_pub(e) - delta_bar(e)

where delta_bar(e) is the mean of delta over the event's bead
position-angle window at the event's libration. The published table is
a single merged value per event, so the registered merged window is
used: mean of the north window (Axis Angle within +/-W of 0 deg) and
the south window (within +/-W of 180 deg), primary W = 15 deg, with
W = 7.5 and 30 deg reported as the registered sensitivity.

Watts sampling: bilinear in (L, B) on the native VI/122 grid, then
periodic linear interpolation in Watts Angle, with the documented
frame conversion (VI/122 doc.txt sec. 6b):
  WA = AA + 0.21 - 0.022 * cos(elongation of Moon from ascending node)
The (L, B) sign convention for entering the Watts grid is the one
established empirically by scripts/validate_frames.py (WATTS_L_SIGN,
WATTS_B_SIGN below; see RESULTS.md).

Modern profiles: LOLA LDEM_128 silhouettes from
scripts/extract_lola_profiles.py (see PREDICTION-deviation note in
RESULTS.md: Herald's Kaguya reduction, the registered first choice,
ceased distribution when Occult 4.12.3 removed Kaguya support in 2021
in favour of LOLA; the audit therefore uses LOLA directly, the same
successor dataset).

Outputs: outputs/corrected_series.csv, outputs/q1_q2_results.json
"""
import csv
import json
import os
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs")

# Frame convention established by validate_frames.py (filled from its output)
WATTS_L_SIGN = +1   # Watts L argument = WATTS_L_SIGN * l
WATTS_B_SIGN = -1   # Watts B argument = WATTS_B_SIGN * b  (r=0.87-0.89, all 3 test events)
WA_SHIFT = 0.21     # deg, doc.txt sec. 6b (Scott 1988: 0.214 deg)

WINDOWS = [7.5, 15.0, 30.0]
PRIMARY_W = 15.0
AUWERS = 959.63

# Reference-frame term (arcsec). The published reductions (WinOccult /
# Occult, Solrad) solve for deltaR against the reduction framework's
# adopted mean limb, defined by the classical eclipse constant
# k = 0.2725076 lunar radii per Earth radius (Explanatory Supplement;
# the same constants Herald printed in the Kaguya Watts-format ReadMe:
# k = 0.2725076, Earth radius 6378.137 km, mean distance 384398.55 km),
# i.e. a mean-limb radius of 1738.091 km. The archived LOLA profiles
# (data/lola_profiles.npz) are instead referenced to the LDEM
# 1737.4 km sphere. Limb heights must be compared on a common datum:
# delta_framework = delta_raw - REFERENCE_TERM. External check: for
# the 1715 eclipse, Hayakawa et al. (2026)'s modern re-derivation
# (959.98) vs Fiala et al. (1994)'s Watts-era value (+0.48) implies a
# limb correction of +0.13 arcsec; this referencing gives +0.165 arcsec,
# while the unshifted raw referencing would give +0.54 arcsec.
REFERENCE_TERM = (0.2725076 * 6378.137 - 1737.4) * (206264.806 / 384398.55)


def watts_profile(w, L, B, wa_query):
    h, Lv, Bv = w["h"], w["L_vals"], w["B_vals"]
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


def window_mean(delta, AA, centre, halfwidth):
    d = np.abs((AA - centre + 180.0) % 360.0 - 180.0)
    return float(delta[d <= halfwidth].mean())


def q1_metrics(dr, ssn):
    dr = np.asarray(dr, float)
    ssn = np.asarray(ssn, float)
    mad = np.median(np.abs(dr - np.median(dr)))
    rho, p_rho = stats.spearmanr(dr, ssn)
    r, _ = stats.pearsonr(dr, ssn)
    slope, intercept, *_ = stats.linregress(ssn, dr)
    return {
        "n": int(len(dr)),
        "robust_scatter_arcsec": float(1.4826 * mad),
        "spearman_rho": float(rho),
        "spearman_p": float(p_rho),
        "pearson_r": float(r),
        "ols_slope_arcsec_per_ssn": float(slope),
        "ols_intercept_arcsec": float(intercept),
        "mean": float(dr.mean()),
        "sd": float(dr.std(ddof=1)),
        "median": float(np.median(dr)),
    }


def main():
    pub = list(csv.DictReader(open(os.path.join(DATA, "dunham2016_table.csv"))))
    geom = {r["date"]: r for r in
            csv.DictReader(open(os.path.join(OUT, "event_geometry.csv")))}
    ssn = {}
    for line in open(os.path.join(DATA, "silso_yearly.csv")):
        parts = line.split(";")
        if len(parts) >= 2:
            try:
                ssn[int(float(parts[0]))] = float(parts[1])
            except ValueError:
                pass
    w = np.load(os.path.join(DATA, "watts_grid.npz"))
    lp = np.load(os.path.join(DATA, "lola_profiles.npz"))
    AA = lp["AA_vals"].astype(np.float64)
    lola_by_date = {d: lp["h"][i].astype(np.float64)
                    for i, d in enumerate(lp["dates"])}

    rows = []
    for r in pub:
        date = f"{int(r['year']):04d}-{int(r['month']):02d}-{int(r['day']):02d}"
        g = geom[date]
        l, b = float(g["libration_l_deg"]), float(g["libration_b_deg"])
        elong = np.radians(float(g["elong_from_node_deg"]))
        wa = AA + WA_SHIFT - 0.022 * np.cos(elong)
        wp = watts_profile(w, WATTS_L_SIGN * l, WATTS_B_SIGN * b, wa)
        delta = lola_by_date[date] - wp - REFERENCE_TERM
        row = {
            "date": date,
            "type": r["type"],
            "n_obs": int(r["n_obs"]),
            "method": r["method"],
            "deltaR_pub": float(r["deltaR_arcsec"]),
            "sigma_pub": float(r["sigma_arcsec"]),
            "ssn_year": ssn[int(r["year"])],
            "libration_l_deg": l,
            "libration_b_deg": b,
        }
        for W in WINDOWS:
            dn = window_mean(delta, AA, 0.0, W)
            ds = window_mean(delta, AA, 180.0, W)
            dm = 0.5 * (dn + ds)
            tag = f"{W:g}".replace(".", "p")
            row[f"delta_bar_N_w{tag}"] = dn
            row[f"delta_bar_S_w{tag}"] = ds
            row[f"delta_bar_w{tag}"] = dm
            row[f"deltaR_corr_w{tag}"] = row["deltaR_pub"] - dm
        rows.append(row)
        print(f"{date}  dR_pub {row['deltaR_pub']:+.2f}  "
              f"delta_bar(15) {row['delta_bar_w15']:+.3f}  "
              f"dR_corr {row['deltaR_corr_w15']:+.3f}")

    with open(os.path.join(OUT, "corrected_series.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)

    dr_pub = np.array([r["deltaR_pub"] for r in rows])
    ssn_v = np.array([r["ssn_year"] for r in rows])
    years = np.array([int(r["date"][:4]) for r in rows])
    res = {"published": q1_metrics(dr_pub, ssn_v)}
    for W in WINDOWS:
        tag = f"{W:g}".replace(".", "p")
        dr_c = np.array([r[f"deltaR_corr_w{tag}"] for r in rows])
        res[f"corrected_w{tag}"] = q1_metrics(dr_c, ssn_v)
    # registered secondary diagnostic: +/-1 yr lag on the primary series
    ssn_by_year = ssn
    for lag in (-1, +1):
        lagged = np.array([ssn_by_year[int(r["date"][:4]) + lag] for r in rows])
        m = q1_metrics(np.array([r["deltaR_corr_w15"] for r in rows]), lagged)
        res[f"corrected_w15_lag{lag:+d}"] = {
            "spearman_rho": m["spearman_rho"], "spearman_p": m["spearman_p"]}
    # POST-HOC diagnostic (labelled): IOTA-era subset 1970+
    keep = years >= 1970
    res["diagnostic_1970plus_published"] = q1_metrics(dr_pub[keep], ssn_v[keep])
    res["diagnostic_1970plus_corrected_w15"] = q1_metrics(
        np.array([r["deltaR_corr_w15"] for r in rows])[keep], ssn_v[keep])

    # POST-HOC robustness (steer-mandated transcription cross-check):
    # substitute Fiala et al. (1994) values (via Sigismondi 2008, AIP 966,
    # Table 1) for the 9 events present in both tables, keeping the same
    # limb corrections; recompute Q1 metrics and the Q2 location.
    FIALA = {"1715-05-03": 0.48, "1925-01-24": 0.51, "1976-10-23": 0.04,
             "1979-02-26": -0.11, "1980-02-16": -0.03, "1981-02-04": -0.02,
             "1983-06-11": 0.09, "1984-05-30": 0.09, "1987-09-23": -0.11}
    dr_fiala_pub = np.array([FIALA.get(r["date"], r["deltaR_pub"]) for r in rows])
    dr_fiala_cor = dr_fiala_pub - np.array([r["delta_bar_w15"] for r in rows])
    res["fiala_substituted_published"] = q1_metrics(dr_fiala_pub, ssn_v)
    res["fiala_substituted_corrected_w15"] = q1_metrics(dr_fiala_cor, ssn_v)
    res["fiala_substituted_q2"] = {
        "R_mean_arcsec": AUWERS + float(dr_fiala_cor.mean()),
        "R_median_arcsec": AUWERS + float(np.median(dr_fiala_cor)),
    }

    # POST-HOC robustness: Watts B-sign sensitivity of delta_bar.
    # Recompute delta_bar(15) entering the Watts grid at B = +b instead of
    # the validated B = -b, and summarise the shift.
    alt = []
    for r in rows:
        g = geom[r["date"]]
        l, b = float(g["libration_l_deg"]), float(g["libration_b_deg"])
        elong = np.radians(float(g["elong_from_node_deg"]))
        wa = AA + WA_SHIFT - 0.022 * np.cos(elong)
        wp_alt = watts_profile(w, WATTS_L_SIGN * l, -WATTS_B_SIGN * b, wa)
        d_alt = lola_by_date[r["date"]] - wp_alt - REFERENCE_TERM
        dm_alt = 0.5 * (window_mean(d_alt, AA, 0.0, PRIMARY_W)
                        + window_mean(d_alt, AA, 180.0, PRIMARY_W))
        alt.append(abs(dm_alt - r["delta_bar_w15"]))
    res["bsign_sensitivity"] = {
        "mean_abs_delta_bar_shift_arcsec": float(np.mean(alt)),
        "max_abs_delta_bar_shift_arcsec": float(np.max(alt)),
    }

    # ---- Q1 verdict under the registered rules (primary window) ----
    pub_m, cor_m = res["published"], res["corrected_w15"]
    shrink = 1.0 - cor_m["robust_scatter_arcsec"] / pub_m["robust_scatter_arcsec"]
    if (cor_m["spearman_p"] < 0.05 and abs(cor_m["spearman_rho"]) >= 0.45
            and cor_m["robust_scatter_arcsec"] >= 0.08):
        q1 = "SURVIVES"
    elif cor_m["spearman_p"] >= 0.05 and shrink >= 0.25:
        q1 = "COLLAPSES (limb artefact)"
    else:
        q1 = "PARTIAL / MIXED"
    res["q1_verdict"] = q1
    res["q1_scatter_shrink_fraction"] = float(shrink)

    # ---- Q2 under the registered rules ----
    dr_c = np.array([r["deltaR_corr_w15"] for r in rows])
    R_mean = AUWERS + float(dr_c.mean())
    R_se = float(dr_c.std(ddof=1) / np.sqrt(len(dr_c)))
    R_med = AUWERS + float(np.median(dr_c))
    def band(R):
        if abs(R - 959.63) <= 0.06:
            return "consistent with Auwers 959.63"
        if abs(R - 959.97) <= 0.06:
            return "consistent with modern eclipse cluster 959.97"
        if abs(R - 959.22) <= 0.06:
            return "consistent with IAU nominal 959.22"
        return "inconsistent with all three"
    res["q2"] = {
        "R_mean_arcsec": R_mean, "R_se_arcsec": R_se,
        "R_median_arcsec": R_med,
        "band_mean": band(R_mean), "band_median": band(R_med),
        "mean_deltaR_corr": float(dr_c.mean()),
    }
    res["q2_verdict"] = (f"mean: {band(R_mean)}; median: {band(R_med)}")

    res["reference_term_arcsec"] = float(REFERENCE_TERM)
    res["watts_frame_convention"] = {
        "L_sign": WATTS_L_SIGN, "B_sign": WATTS_B_SIGN, "WA_shift_deg": WA_SHIFT}

    with open(os.path.join(OUT, "q1_q2_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("\nQ1 verdict:", q1)
    print("Q2:", res["q2"])
    print("wrote outputs/corrected_series.csv, outputs/q1_q2_results.json")


if __name__ == "__main__":
    main()
