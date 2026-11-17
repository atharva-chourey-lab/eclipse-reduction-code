# PREDICTION.md — Pre-registration for the Eclipse-Radius Audit

**Registered:** 2026-11-17 (git-committed before any archive data was downloaded or inspected).
**Project:** Does the eclipse-based solar-diameter record survive removal of the Watts (1963) lunar-limb datum?
**Status rule:** Nothing in this file may be edited after data acquisition begins. Corrections, if forced by the data, go in RESULTS.md labelled POST-HOC, never here.

---

## 1. The claim under audit

Since 1970, IOTA observers have timed Baily's beads at eclipse path limits to derive per-eclipse
corrections ΔR to the standard solar radius (Auwers 1891, S⊙ = 959.63″ at 1 au — the value still
used in all published eclipse predictions). The published compilation (Dunham, Sofia, Guhl &
Herald, "Solar diameter measurements from eclipses as a solar variability proxy", IAU Symp. 320,
2016) presents ΔR fluctuations of order 0.1–0.3″ and discusses them as a solar-variability (cycle)
proxy. By the authors' own statement, that table was *"analyzed with lunar limb data from 'The
Marginal Zone of the Moon' Watts (1963)"* — a 1950s photographic limb survey whose datum is known
to be slightly elliptical and offset from the Moon's centre of mass (Van Flandern 1970; Morrison
1979), with known deficiencies in the polar zones — exactly where path-limit beads occur. Modern
reductions use Kaguya/LOLA altimetry, but no published wholesale re-reduction of the 1970–2015
ΔR archive against a modern limb was found in the 2026-11-17 scouting
(`~/workspace/astro-scouting/FEASIBILITY.md`, Seam 1b).

**This project applies a differential correction:** for each eclipse event in the published
archive, compute the limb-profile difference (modern − Watts) at that event's bead position
angles and libration state, and apply it to the published ΔR. The raw timings are not re-reduced;
the published ΔR values are the quantities under audit.

## 2. Fixed choices (registered in advance)

**(a) Solar-edge definition.** The inflection point of the limb-darkening function — the modern
standard definition of the photospheric radius. Note, declared in advance: Baily's-bead timings
sense the extinction edge, and the published ΔR were derived under the original reduction's
conventions. Our correction is a *differential* applied to the published ΔR at fixed timings, so
it is definition-preserving: it changes only the limb model, not the edge definition. In Q2,
each modern comparator is quoted with its own stated definition and no cross-definition
averaging is performed.

**(b) Limb models.**
- *Old (the datum under audit):* Watts (1963), "The Marginal Zone of the Moon", limb profiles
  as tabulated — machine-readable form to be sourced openly (Occult-ecosystem distribution or
  digitization of the printed tables for the needed ranges; the route actually used will be
  documented in data/PROVENANCE.md).
- *New (the modern comparator):* Kaguya (SELENE) LALT altimetry reduced to Watts-format limb
  profiles by D. Herald — the same profiles distributed with Occult 4 and used by modern
  reductions (this is the limb model Quaglia et al. 2021's class of reductions relies on via
  SLDEM; Kaguya LALT and LOLA SLDEM2015 are independent spacecraft altimetry of the same limb).
  Spot-checks against LOLA SLDEM2015 (Barker et al. 2016; NASA PDS LRO LOLA GDR) will be run
  if a subset download is practical, and reported either way.

**(c) Ephemeris.** JPL DE440 for all event geometry: eclipse dates/times, and the lunar
libration (l, b) at each event. Operational source: skyfield/jplephem with the DE440 kernel
(de440.bsp). If the kernel cannot be obtained, NASA eclipse-bulletin librations (Espenak,
computed from JPL ephemerides) are the registered fallback and every affected event is flagged.

**(d) Correction method.** For event *e* with published ΔR_pub:
  ΔR_corr(e) = ΔR_pub(e) − δ̄(e),
  δ(θ, lib) = h_new(θ, lib) − h_Watts(θ, lib)   [arcsec, radial limb height],
  δ̄(e) = mean of δ over the event's bead position-angle window at the event's libration.
Sign derivation (tangent-point approximation): a bead event at time t fixes the centre distance
d(t); the reduction solves R = d − ρ − h_assumed(θ). Replacing h_Watts by h_new therefore
changes the inferred radius by −(h_new − h_Watts) = −δ. A limb that is *higher* in the modern
profile than in Watts means the Watts-based reduction *overstated* the solar radius, and the
correction subtracts δ. ✓ consistent with the formula above.
- *Bead position-angle window:* per-bead Watts angles are not published with the ΔR table, so
  the registered approximation is a polar window: north-limit results use Watts angles within
  ±15° of the lunar north point (0°), south-limit results within ±15° of the south point (180°);
  results published as a single merged value use the mean of the two windows. Sensitivity to
  window half-width (±7.5°, ±15°, ±30°) is reported for every headline number.
- *Libration:* the event's (l, b) at greatest eclipse; each profile set is interpolated to
  that libration in its own native grid/interpolation scheme, documented in the scripts.
- Events for which a correction cannot be computed (missing libration, profile coverage gap,
  ambiguous limit attribution) are **excluded and listed**, never silently dropped or zero-filled.

**(e) Cycle proxy for Q1.** Annual mean sunspot number, SILSO v2.0 (sidc.be), value for each
event's calendar year. No lag is applied in the primary test; a ±1-year lag check is a
registered secondary diagnostic, not a headline.

## 3. Registered decision rules

### Q1 — Does the claimed cycle-linked ΔR variation survive the Watts→modern correction?

Primary metrics, computed identically on the published and on the corrected series:
(i) robust scatter = 1.4826 × MAD of ΔR; (ii) Spearman ρ between ΔR and the annual sunspot
number at event epochs, with its p-value; (iii) for reference, Pearson r and the OLS slope
ΔR ~ SSN.

- **SURVIVES** — corrected series: Spearman ρ significant (p < 0.05) with |ρ| ≥ 0.45, **and**
  robust scatter ≥ 0.08″.
- **COLLAPSES (limb artefact)** — corrected series: correlation not significant (p ≥ 0.05),
  **and** robust scatter shrinks by ≥ 25% relative to the published series.
- **PARTIAL / MIXED** — anything else. Reported as such, with both metrics printed; no
  rounding of a mixed outcome into either headline.

Either outcome — survival or collapse — counts as a result. A vindication of the archive is a
publishable outcome of this audit, not a failure of it.

### Q2 — Where does the corrected archive's mean radius sit?

R̄ = 959.63″ + mean(ΔR_corr), standard error = SD/√n; the median-based value is reported
alongside. Comparators (all at 1 au): Auwers standard **959.63**; IAU 2015 nominal **959.22**;
Lamy et al. 2015 **959.99 ± 0.06**; Quaglia et al. 2021 **959.95 ± 0.05**; Kubo et al.
**959.74–959.88** (range).

- |R̄ − 959.63| ≤ 0.06″ → **consistent with the Auwers standard** the almanacs print.
- |R̄ − 959.97| ≤ 0.06″ → **consistent with the modern eclipse cluster** (Lamy/Quaglia).
- |R̄ − 959.22| ≤ 0.06″ → **consistent with the IAU helioseismic nominal**.
- Otherwise → **inconsistent with all three**; R̄ ± SE is reported as the archive's own number.
If the mean and median land in different bands, both are reported and the discrepancy is
discussed, not resolved by preference.

## 4. Data-acquisition plan (registered fallbacks)

1. **Published ΔR table** — Dunham, Sofia, Guhl & Herald 2016 (IAU Symp. 320, Cambridge,
   open PDF per scouting). Transcribe the table exactly; photograph-equivalent provenance
   (page/figure numbers) recorded per value. If the proceedings table proves inaccessible,
   fall back to any openly posted IOTA ΔR compilation by the same authors, flagged as such.
2. **Event-level bead timings** — attempt IOTA / Occult-ecosystem open downloads. If raw
   timings are not openly obtainable, that limit is declared and the audit proceeds at the
   published-ΔR level (the registered design already assumes this level).
3. **Watts profiles** — machine-readable via the Occult ecosystem or equivalent open source;
   fallback: digitize the printed 1963 tables for the polar windows and libration ranges the
   archive actually needs, and say so.
4. **Modern profiles** — Herald's Kaguya Watts-format profiles (Occult 4 distribution);
   LOLA SLDEM2015 subset via PDS as cross-check if practical.

## 5. Standing honesty rules

- Missing = missing: uncorrectable events are listed with reasons, never imputed.
- Every number in RESULTS.md must be reproducible by re-running scripts/ on data/ as archived.
- Pre-GPS-era timing/position errors in the original observations are *not* modelled by this
  differential design and are declared as a limitation, not absorbed into the correction.
- The audit is of a *method era* (a superseded limb datum), not of the named observers; the
  write-up will be framed accordingly.
