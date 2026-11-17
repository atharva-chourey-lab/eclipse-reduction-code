# RESULTS.md — Does the eclipse ΔR archive survive removal of the Watts datum?

**Project:** Eclipse-radius audit, pre-registered in `PREDICTION.md`
(git commit `a42d76a`, before any archive data was touched).
**Date:** 2026-11-17. **Status:** local only; nothing released publicly.

## The claim, in its tightest defensible form

> Dunham, Sofia, Guhl & Herald (2016) published the IOTA Baily's-bead
> ΔR series (1970–2015, with historical extensions to 1715) reduced
> against Watts (1963), and stated that a consistent re-analysis with
> Kaguya/LRO limb profiles was needed. That re-analysis was never
> published. This work is the first to apply a uniform
> Watts→modern-limb differential correction to the full published ΔR
> series and to test, under pre-registered rules, whether its claimed
> solar-cycle correlation and its mean level survive the removal of
> the Watts datum.

Anything stronger is contradicted by the record (see §7): modern-limb
single-eclipse radii exist since 2011; reduction practice migrated to
Kaguya by ~2010 and to LOLA-only in Feb 2021; the archive was publicly
questioned by Hayakawa et al. (2026). This audit executes the original
authors' own stated future-work programme (Dunham et al. 2016, §4);
it does not ambush it.

## Headline results

- **The Watts→LOLA correction is small, positive, and lopsided.**
  Averaged over the registered ±15° polar bead windows, the modern
  limb sits **δ̄ = +0.100″** above the Watts limb (per-event range
  −0.003…+0.194″), so Watts-based reductions *overstated* ΔR by
  ~0.1″ on average. The correction is strongly hemispheric:
  south-window mean **+0.271″**, north-window mean **−0.071″**
  (S−N asymmetry +0.34″) — the Watts datum's southern polar zone is
  its weak side, a structure a single merged ΔR per event conceals.
- **Q1 — PARTIAL / MIXED** (registered verdict). The published series
  shows no significant sunspot correlation to begin with (Spearman
  ρ = −0.19, p = 0.34); after correction ρ = −0.24 (p = 0.22) and the
  robust scatter shrinks 0.237″ → 0.196″ (−17.4%), short of the
  registered −25% collapse criterion. The limb correction neither
  manufactures nor destroys a cycle signal at the registered
  thresholds. In the IOTA-era subset (1970+, labelled diagnostic) the
  scatter shrinks by 32% (0.208″ → 0.141″) — the Watts datum was
  contributing about a third of that subset's scatter — but the
  correlation remains non-significant there too.
- **Q2 — the corrected archive's mean radius is 959.494 ± 0.044″**
  (SE; median-based 959.481″), which under the registered ±0.06″
  bands is **inconsistent with all three** comparators: 0.136″ below
  Auwers' 959.63, 0.48″ below the modern eclipse cluster (~959.97),
  0.27″ above the IAU nominal 959.22. Removing the Watts datum moves
  the archive *down*, away from the modern single-eclipse cluster —
  because the published mean already sat at Auwers and the net limb
  correction is positive. The result is stable across the registered
  window sensitivity (959.488 / 959.494 / 959.508 for ±7.5°/±15°/±30°).
- **The input table matters as much as the limb.** Dunham et al.
  (2016)'s Figure 1 disagrees with its own probable source, Fiala et
  al. (1994), on 7 of 9 overlapping events — five of them sign flips,
  including 1715 (−0.50 vs +0.48) and 1925 (−0.21 vs +0.51). This is
  the discrepancy Hayakawa et al. (2026) cited when excluding the
  table; here it is itemised (§5). Substituting Fiala's values leaves
  Q1's verdict unchanged but moves Q2 to 959.581″ — consistent with
  Auwers by the mean. **Which published table one audits changes the
  Q2 answer at the ~0.09″ level; the limb correction does not.**

## 1. Method as executed

Registered design (PREDICTION.md §2): for each of the 27 events in
Dunham et al. (2016) Figure 1, ΔR_corr = ΔR_pub − δ̄, with
δ(θ, lib) = h_LOLA(θ, lib) − h_Watts(θ, lib) and δ̄ the mean of δ over
the bead position-angle window (merged north+south polar windows,
primary half-width ±15°, sensitivities ±7.5°/±30°) at the event's
libration (l, b) at greatest eclipse from JPL DE440. Cycle proxy:
SILSO v2.0 annual mean sunspot number for the event's year. Decision
rules exactly as registered (PREDICTION.md §3). All 27 events were
correctable; none was excluded or imputed.

Pipeline (all in `scripts/`, re-runnable on `data/` as archived):
`parse_watts.py` (VI/122 → grid) → `event_geometry.py` (DE440
greatest-eclipse instants + librations; 2006-03-29 greatest eclipse
reproduced to 0.4 s against Espenak's published 10:11:17.6 UT) →
`extract_lola_profiles.py` (LDEM_128 silhouettes at each event's
libration) → `validate_frames.py` (frame conventions) →
`correct_and_test.py` (correction + registered tests).

## 2. Deviations and determinations forced by the data

Labelled here, per the project's discipline; PREDICTION.md is
unchanged.

**(a) Modern limb: Kaguya → LOLA (forced substitution).**
PREDICTION.md §2(b) named Herald's Kaguya reduction to Watts-format
profiles (Occult 4 distribution). That distribution no longer exists:
Occult 4.12.2 (14 Feb 2021) disabled the Kaguya download as "fully
superseded by the LOLA dataset", and 4.12.3 removed Kaguya support
entirely; the standalone "Kaguya For Eclipses" file survives only as
a ReadMe in the Occult help files. The audit therefore derives its
modern profiles from **LOLA LDEM_128** (NASA PDS) — the successor
dataset the ecosystem itself adopted, and an independent spacecraft
altimetry of the same limb. Registered SLDEM2015 spot-checks were
not run: SLDEM2015 covers only ±60° latitude and cannot see the
polar windows this audit is about; LDEM_128's polar coverage is used
instead, with its GMT-interpolation caveat declared (§8).

**(b) Datum referencing (determination, externally validated).**
ΔR is defined relative to the reduction framework's adopted mean
limb. Herald's Watts-format convention (printed in the Kaguya
ReadMe) uses the classical eclipse constant k = 0.2725076 with Earth
radius 6378.137 km at mean distance 384,398.55 km — a mean-limb
radius of 1738.091 km. The LDEM grid is referenced to a 1737.4 km
sphere. Comparing heights across the two datums without aligning
them would inject a spurious +0.371″ into every δ̄; the correction
therefore applies this constant datum term (REFERENCE_TERM in
`correct_and_test.py`) before differencing. External validation:
for the 1715 eclipse, Fiala et al. (1994)'s Watts-era value
(ΔR = +0.48) and Hayakawa et al. (2026)'s modern-topography
re-derivation (959.98 ± 0.23″, i.e. ΔR = +0.35) imply a true limb
correction of +0.13″; this pipeline's δ̄(1715) = **+0.166″** — within
0.04″ of the implied value, well inside Hayakawa's ±0.23″. Without
the datum term the pipeline would have reported +0.54″, a 0.4″ miss.
The term is a constant, so it affects Q2's location only; Q1's
scatter and correlation are invariant to it.

**(c) Watts frame convention (determined empirically).**
The Watts grid's (L, B, WA) arguments were mapped to the modern
(l, b, axis angle) frame by cross-correlating the Watts and LOLA
profiles for three events over all sign/shift combinations
(`validate_frames.py`). The winner is unambiguous and matches the
dataset's own documentation where it speaks: L entered at +l,
**B entered at −b**, WA = AA + 0.21° (Scott 1988's offset, doc.txt
§6b), with Pearson r = 0.87–0.89 (reversed-axis mappings give
r < 0; wrong-L mappings ≤ 0.80). The B-sign choice is the weakest
link: entering B at +b instead shifts δ̄ by 0.061″ on average
(max 0.148″) — declared as a systematic in §8.

**(d) Raw bead timings.** Not openly obtainable (PREDICTION.md §4.2
anticipated this); the audit proceeds at the published-ΔR level, as
registered. Dunham's own reduction used bead events within 30° of
the poles (IAU GA 2015 talk), consistent with the registered window
design and its ±30° sensitivity.

## 3. The correction, event by event

δ̄ at the primary ±15° window (merged N/S), framework datum.
Full table with N/S splits, all three window widths, librations and
sunspot numbers: `outputs/corrected_series.csv`.

| Date | ΔR_pub (″) | δ̄ (″) | ΔR_corr (″) | | Date | ΔR_pub (″) | δ̄ (″) | ΔR_corr (″) |
|---|---|---|---|---|---|---|---|---|
| 1715-05-03 | −0.50 | +0.166 | −0.666 | | 1983-06-11 | −0.10 | +0.030 | −0.130 |
| 1878-07-29 | +0.55 | +0.149 | +0.401 | | 1984-05-30 | +0.13 | +0.120 | +0.010 |
| 1900-05-28 | +0.12 | +0.092 | +0.028 | | 1987-03-29 | −0.19 | +0.011 | −0.201 |
| 1912-04-17 | −0.29 | +0.146 | −0.436 | | 1987-09-23 | +0.10 | +0.117 | −0.017 |
| 1922-09-21 | +0.20 | +0.043 | +0.157 | | 1988-03-18 | −0.13 | +0.107 | −0.237 |
| 1925-01-24 | −0.21 | +0.184 | −0.394 | | 1991-07-11 | 0.00 | +0.065 | −0.065 |
| 1966-05-20 | +0.03 | +0.127 | −0.097 | | 1994-05-10 | −0.25 | +0.114 | −0.364 |
| 1970-03-07 | −0.05 | +0.107 | −0.157 | | 1995-10-24 | +0.11 | +0.126 | −0.016 |
| 1972-07-10 | −0.02 | +0.129 | −0.149 | | 1998-02-26 | +0.16 | +0.107 | +0.053 |
| 1973-06-30 | +0.40 | +0.050 | +0.350 | | 1999-08-11 | −0.03 | +0.108 | −0.138 |
| 1976-10-23 | −0.38 | +0.033 | −0.413 | | 2002-12-04 | −0.22 | −0.003 | −0.217 |
| 1979-02-26 | −0.05 | +0.194 | −0.244 | | 2005-10-03 | −0.06 | +0.121 | −0.181 |
| 1980-02-16 | −0.18 | +0.101 | −0.281 | | 2006-03-29 | +0.09 | +0.104 | −0.014 |
| 1981-02-04 | −0.21 | +0.043 | −0.253 | | | | | |

Reading of the pattern: the south polar window carries the
correction (mean δ̄_S = +0.271″, every event positive, range
+0.136…+0.353″); the north window is near zero on average
(δ̄_N = −0.071″, range −0.179…+0.072″). This is the signature
Morrison & Appleby (1981) documented from 66,000 occultations —
Watts datum errors attaining 0.4″ at some position angles, with the
datum radius varying with libration — localised here to the
southern polar zone at eclipse librations. (The VI/122 documentation
independently flags the polar Cassini regions as the charts' weak
zone.) A merged per-event ΔR, and Dunham's 2-parameter fits (whose
second parameter is a lunar-centre offset, partially degenerate
with a N–S limb asymmetry), both dilute this structure; it is
reported here because any future bead-level re-reduction should
expect it.

## 4. Q1 — does the cycle-linked variation survive? **PARTIAL / MIXED**

Registered metrics, computed identically on both series (n = 27):

| Series | Robust scatter (″) | Spearman ρ vs SSN | p | Pearson r | OLS slope (″/SSN) |
|---|---|---|---|---|---|
| Published | 0.237 | −0.193 | 0.336 | −0.217 | −0.00072 |
| Corrected (±7.5°) | 0.205 | −0.273 | 0.169 | −0.202 | −0.00070 |
| Corrected (±15°) | 0.196 | −0.245 | 0.218 | −0.198 | −0.00067 |
| Corrected (±30°) | 0.194 | −0.226 | 0.257 | −0.218 | −0.00074 |

Registered secondary diagnostics (±1-yr lag, corrected ±15°):
lag −1: ρ = −0.005 (p = 0.98); lag +1: ρ = −0.299 (p = 0.13).

Application of the registered rules: SURVIVES requires a significant
corrected correlation with |ρ| ≥ 0.45 and scatter ≥ 0.08″ — the
correlation is not significant at any window (p ≥ 0.17), so it does
not survive. COLLAPSES requires non-significance **and** a scatter
shrink ≥ 25% — the shrink is 17.4% at the primary window (13–18%
across windows), so it does not collapse either. **Verdict:
PARTIAL / MIXED**, at every window width.

What this means, stated plainly: in the published table as a whole
there is no statistically significant sunspot-cycle correlation for
the limb correction to kill — Dunham et al.'s variability claim
rests on the 0.1–0.3″ fluctuation level itself and on the Sofia–Li
W-parameter argument, not on a raw correlation of this table with
sunspot number. The Watts correction removes about a sixth of the
series' robust scatter (and, in the 1970+ diagnostic subset, about
a third: 0.208″ → 0.141″, ρ = −0.13 → −0.26, still non-significant).
The residual scatter (~0.20″) is an order of magnitude above the
space-based cap on true cycle-synchronous radius variation
(< 23 mas peak-to-peak, Bush, Emilio & Kuhn 2010, *ApJ* 716:1381;
< 7 mas after correction in Kuhn et al. 2004). Two consequences:
(i) the residual fluctuations in the corrected series cannot be
promoted to a physical solar-radius variation without confronting
that cap; (ii) the comparison is not apples-to-apples in edge
definition — bead timings sense an extinction edge, the space
results an inflection-point radius (PREDICTION.md §2a) — so the cap
constrains, but does not by itself falsify, a ground-based
extinction-edge record. What this audit establishes is narrower and
firmer: the Watts datum is responsible for a real, quantified slice
of the archive's scatter and level, and it is not responsible for
the rest.

## 5. Q2 — where does the corrected mean radius sit? **Inconsistent with all three**

R̄ = 959.63 + mean(ΔR_corr) = **959.494″**, SE = 0.044″; median-based
value **959.481″**. Mean and median fall in the same registered
category, so the registered mean/median clause is not triggered.

| Comparator | Value (″) | Definition / basis | R̄ − value (″) | In ±0.06 band? |
|---|---|---|---|---|
| Auwers 1891 standard | 959.63 | eclipse-prediction standard (still the almanac value; Quaglia et al. 2021; Wright & Young 2024 §6.4) | −0.136 | no |
| Modern eclipse cluster | 959.97 (centre) | Lamy et al. 2015: 959.99 ± 0.06; Quaglia et al. 2021: 959.95 ± 0.05; Guhl 2023: 960.01 ± 0.12 — modern-limb single-eclipse determinations | −0.476 | no |
| IAU 2015 nominal | 959.22 | helioseismic (Prša et al. 2016); the seismic radius is the field's current best determination per Rozelot & Kosovichev 2026 §2.5 | +0.274 | no |
| Kubo et al. (context) | 959.74–959.88 | Watts-era pooled eclipses 1970–1991 | −0.25…−0.39 | — |
| Kilcik et al. 2009 (context) | 959.22 ± 0.04 | 2006 eclipse, Watts/occultation-refined limb era | +0.27 | — |

Registered verdict: **inconsistent with all three**; the corrected
archive's own number is 959.494 ± 0.044″ (statistical SE; declared
systematics in §8 are of comparable size and are not folded into the
band test, per the registered rule).

Interpretation, with the concessions of §7 kept in view: this is a
test of the *corrected archive*, not a new radius measurement. The
modern cluster (959.92–960.02″) was already established by
single-eclipse modern-limb work; the corrected archive does not join
it — it sits ~0.48″ below it, and ~0.14″ below the Auwers value its
own reductions used as zero-point. Two readings are available and
the data here do not separate them: (i) the bead archive carries
further negative systematics beyond the limb datum (extinction-edge
vs inflection-point definitions; filter/detector edge losses of
−0.02…−0.17″ quantified by Sigismondi 2008; pre-GPS position/timing
errors — none modelled by this differential design, §8); (ii) the
archive's merged, polar-bead, 2-parameter reductions are not the
same measurement as the modern full-light-curve or flash-spectrum
determinations. Either way, the Watts datum is *not* the reason the
archive's mean disagrees with the modern cluster: removing it moves
the mean the other way.

Confrontation with the archive-era outlier: Kilcik et al. (2009)
derived 959.22 ± 0.04″ for the 2006-03-29 eclipse (ΔR = −0.41). The
corrected archive value for that eclipse is ΔR_corr = −0.014″
(R = 959.616″), 0.40″ above Kilcik's, and the corrected archive mean
sits 0.27″ above their value. The corrected series does not support
the Kilcik et al. outlier or its 19-eclipse "nonhomologous"
compilation claim.

## 6. Transcription cross-check (the Hayakawa hazard)

Hayakawa, Sôma, Rozelot et al. (2026, *ApJL*) excluded Dunham et
al. (2016)'s data from their compilation figure "as they have
considerable data offsets with their probable source articles."
Following the novelty audit's steer, the digitized table was
cross-checked against Fiala, Dunham & Sofia (1994, *Solar Phys.*
152:97–104) — the archive's foundational table — as reproduced in
Sigismondi (2008, AIP Conf. Proc. 966, Table 1; cross-verified
against the same author's companion reproduction), and against
per-eclipse source articles where they exist. The digitization
itself was first re-verified digit-for-digit against the rendered
Figure 1: **the transcription is exact as published**, so every
disagreement below is a genuine difference between publications.

**Fiala et al. (1994) vs Dunham et al. (2016)** — 9 overlapping
events; full log in `outputs/crosscheck_sources.csv`:

| Date | Fiala 1994 ΔR (″) | Dunham 2016 ΔR (″) | Difference |
|---|---|---|---|
| 1715-05-03 | +0.48 ± 0.20 (3 obs) | −0.50 ± 0.20 (3 obs) | **−0.98, sign flip** |
| 1925-01-24 | +0.51 ± 0.08 (8 obs) | −0.21 ± 0.17 (11 obs) | **−0.72, sign flip** |
| 1976-10-23 | +0.04 ± 0.07 | −0.38 ± 0.09 | **−0.42, sign flip** |
| 1987-09-23 | −0.11 ± 0.03 | +0.10 ± 0.05 | **+0.21, sign flip** |
| 1981-02-04 | −0.02 ± 0.03 | −0.21 ± 0.05 | −0.19 |
| 1983-06-11 | +0.09 ± 0.02 | −0.10 ± 0.08 | **−0.19, sign flip** |
| 1980-02-16 | −0.03 ± 0.03 | −0.18 ± 0.05 | −0.15 |
| 1979-02-26 | −0.11 ± 0.05 (47 obs) | −0.05 ± 0.08 (21 obs) | +0.06 |
| 1984-05-30 | +0.09 ± 0.04 | +0.13 ± 0.07 | +0.04 |

Dunham et al. (2016) is a re-reduction (WinOccult/Solrad 2-parameter
solutions, beads within 30° of the poles), not a reprint of Fiala —
different bead subsets explain the differing observation counts
(e.g. 1979: 47 bead events vs 21). They do not comfortably explain
five sign flips, two of them (1715, 1925) on the programme's most
cited historical anchors, at unchanged n and σ for 1715. Hayakawa
et al.'s compiled values side with Fiala where both exist
(1925: 960.14 ± 0.08″ = ΔR +0.51; 1715: ≥ 959.91″, i.e. ΔR ≥ +0.28).

**Per-eclipse sources, post-1991 events:** 1994-05-10: Thompson/IOTA
−0.27 ± 0.02 vs Dunham −0.25 (agreement); 1999-08-11: Thompson/IOTA
+0.06 ± 0.06 vs −0.03; 2005-10-03: Sigismondi 0.00 ± 0.17 (southern
limit) vs −0.06; 2006-03-29: Kilcik et al. −0.41 (see §5) and
Sigismondi ≈ 0.00…−0.01 ± 0.17 vs Dunham +0.09.

**Which source the correction used, per event:** the primary
correction uses **Dunham et al. (2016) Figure 1 for all 27 events** —
that table, as published, is the registered audit object
(PREDICTION.md §4.1). No event's primary value comes from any other
source.

**Sensitivity to the input table (labelled, post-registration):**
substituting Fiala's 9 values (same limb corrections) gives:
published-series scatter 0.163″, ρ = −0.285 (p = 0.150); corrected
scatter 0.175″, ρ = −0.277 (p = 0.163) — **Q1 verdict unchanged**
(PARTIAL / MIXED under the same rules). Q2 moves to
R̄ = **959.581″** (median 959.565″): consistent with Auwers by the
registered mean band (|Δ| = 0.049 ≤ 0.06), with the median 0.005″
outside its band — reported as-is under the registered mean/median
clause. The Q2 location therefore depends on which published table
is audited, at the ~0.09″ level; the limb correction (δ̄ ≈ +0.10″)
is smaller than the tables' mutual disagreement (up to 0.98″).

**The 1715 anchor, three ways:** Fiala +0.48 → this pipeline
959.944″; Hayakawa et al. (2026) modern re-derivation 959.98 ± 0.23″
(agreement within 0.04″). Dunham 2016 −0.50 → this pipeline
958.964″, irreconcilable with the modern re-derivation by ~1″: no
limb correction of the size documented anywhere (≤ 0.4″, Morrison &
Appleby 1981) can bridge it. The 1715 point in Dunham et al. (2016)
should be treated as an error in that table — most plausibly a sign
error, given identical n = 3 and σ = 0.20 to Fiala's — until the
custodians say otherwise. The famous 1715-vs-1979 "0.4″ shrinkage"
(Dunham et al. 1980, *Science* 210:1243) is not supported by the
2016 table's own 1715 value; on Fiala's values the pair reads
+0.48 (1715) vs −0.11 (1979), a 0.59″ difference in the claimed
direction, while on Dunham 2016's values it reads −0.50 vs −0.05 —
the shrinkage inverts. This audit takes no position on the 1980
claim itself, which used the era's own reductions; it reports that
the 2016 table cannot be used to support it.

## 7. Concessions and prior art (per NOVELTY_AUDIT.md)

1. Dunham et al. 2016 §4 stated this re-analysis as their own future
   work (also their 2014/2015 talks; Sôma 2012 announced the same
   intent). We execute their programme.
2. Hayakawa et al. 2026 (ApJL) already flagged and excluded the
   D+16 table (§6) — first to doubt the archive *in print* is theirs.
3. Hayakawa et al. 2026 (1715; arXiv:2604.24503): 959.98 ± 0.23″ —
   prior single-event modern re-derivation of the archive's most
   famous anchor; used here as an external check (§2b, §6).
4. Rozelot & Kosovichev 2026 §2.5: the "eclipse astrometry revival"
   framing; the seismic radius is the field's current best
   determination. Q2's comparators are positioned accordingly.
5. Bush, Emilio & Kuhn 2010: the < 23 mas peak-to-peak space cap —
   confronted in §4; no physical cycle variation is claimed here.
6. Lamy et al. 2015 (959.99 ± 0.06), Quaglia et al. 2021
   (959.95 ± 0.05), Guhl 2023 (960.01 ± 0.12), Quaglia 2024,
   Guhl & Tegtmeier 2018: the modern-limb single-eclipse cluster
   pre-exists; Q2 tests the corrected archive against it.
7. Kilcik et al. 2009: the Watts-era 959.22 ± 0.04 outlier —
   confronted explicitly in §5.
8. Morrison & Appleby 1981: Watts datum systematics up to 0.4″ were
   published 45 years ago; the correction's plausibility is not
   novel — only its application to this series is.
9. Occult 4.12.2/4.12.3 release notes (Feb 2021) and IOTA's current
   guidance: prediction/reduction practice migrated (Kaguya ~2010,
   LOLA-only 2021). The "959.63″ remains the prediction standard"
   clause is an almanac/de-facto statement (Quaglia et al. 2021;
   Wright & Young 2024 §6.4), with Irwin's 2024 map (959.95″) the
   first prominent break.
10. Dunham's IOTA pages (2023, updated 2025): the custodian
    community has itself de-emphasized bead-derived diameters
    ("we came to realize the difficulty in deriving such information
    from such recordings"). This audit closes out a programme its
    owners have wound down; that cuts both ways and is said plainly.

## 8. Limitations and declared gaps

- **Raw bead timings are not openly obtainable**; the audit works
  at the published-ΔR level (registered design). A bead-level
  re-reduction could distribute the N/S asymmetry of §3 differently
  (per-limit values are not published), and could supersede the
  window approximation.
- **Window approximation:** per-bead position angles are
  unpublished; polar windows (±15° primary) stand in for them.
  Dunham's own bead selection (within 30° of the poles) supports the
  geometry; verdicts are stable across ±7.5°/±15°/±30°.
- **Libration:** geocentric (l, b) at greatest eclipse (DE440 + IAU
  mean rotation elements, forced-libration terms ≤ ~0.03°
  neglected). The original reductions used per-observer topocentric
  librations; the merged published values mix sites, and profile
  variation over the difference is second-order at window-mean
  level. The Watts B-sign determination (§2c) contributes a
  declared systematic of ~0.06″ (mean |Δδ̄|; max 0.15″) — comparable
  to Q2's statistical SE (0.044″) and not folded into it.
- **LDEM polar caveat:** LDEM_128's highest-latitude cells are
  GMT-`surface` interpolations where LOLA tracks are sparse (label
  DESCRIPTION); the polar windows inherit that smoothing. The
  DE421-ME frame of LDEM vs DE440 geometry differs at arcsec level,
  negligible at 0.2° sampling.
- **Not modelled** (registered): pre-GPS-era timing/position errors
  in the original observations; filter/detector extinction-edge
  losses; personal equation. The authors' own assessed real errors
  (±0.2″ video era, ±0.4″ visual era) exceed most of the corrections
  applied here — the correction is a datum audit, not a claim that
  the corrected values are accurate to their formal σ.
- **1715's sunspot number** (45.0) rests on sparse early
  observations (SILSO v2.0 yearly file, pre-1749 caveat); it enters
  Q1 as registered. Excluding 1715 changes no verdict (its leverage
  is on the Q2 mean via ΔR, addressed in §6, not via SSN).
- The published σ's are not used by the registered metrics (the
  registered tests are unweighted); the paper itself assesses the
  formal σ's as ~4× too small.

## 9. Reproducibility

Every number above is regenerated by, in order:
`.venv/bin/python scripts/parse_watts.py`,
`scripts/event_geometry.py`, `scripts/extract_lola_profiles.py`,
`scripts/validate_frames.py`, `scripts/correct_and_test.py`
on the datasets archived in `data/` with provenance in
`data/PROVENANCE.md`. Deliverables: `outputs/corrected_series.csv`
(per-event ΔR_pub, δ̄ N/S/merged and ΔR_corr at all three window
widths, librations, SSN), `outputs/q1_q2_results.json` (all metrics
and verdicts, including the labelled diagnostics),
`outputs/crosscheck_sources.csv` (the §6 log), `outputs/event_geometry.csv`.

**Per-event source statement (summary):** primary ΔR for all 27
events = Dunham, Sofia, Guhl & Herald (2016), Figure 1, as published
and digit-verified. Cross-check sources exist for 13 events (9 Fiala
1994; 1994/1999 Thompson-IOTA; 2005 Sigismondi; 2006 Kilcik and
Sigismondi) and are logged in `outputs/crosscheck_sources.csv`; none
replaces a primary value. The Fiala-substitution sensitivity (§6) is
the only computation that uses non-Dunham inputs, and it is labelled
wherever it appears.
