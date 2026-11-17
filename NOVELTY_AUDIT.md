# NOVELTY_AUDIT.md — Is the eclipse ΔR archive re-reduction seam still open?

**Audit date:** 2026-11-17 · **Auditor's role:** literature/novelty audit only; the build continues in parallel.
**Claim under audit:** "The IOTA Baily's-bead ΔR archive (1970–2015) — basis for claims that the solar
diameter varies with the solar cycle — was reduced against Watts' 1963 lunar limb profiles and has
never been re-reduced against LOLA/Kaguya laser-altimetry limbs; Auwers' 1891 radius 959.63″ is still
the eclipse-prediction standard."

**Method / searched sources:** NASA ADS–indexed journals (ApJ, ApJS, AJ, Solar Phys., PASJ, MNRAS)
via publisher and ADS pages; arXiv; Cambridge UP proceedings (IAU Symp. 264, 320); Springer;
IOPscience; the *Journal for Occultation Astronomy* (IOTA/ES, iota-es.de); IOTA web publications
(occultations.org, incl. Dunham's graze/eclipse pages); Occult 4 release notes (IOTAoccultations
groups.io); Korea Science (Bull. Korean Astron. Soc., Publ. Korean Astron. Soc.); NASA eclipse office
pages; Sigismondi's ICRA pages; and the independent eclipse-computation bibliography at sankara.net
(updated Oct 2026). Every instance below was verified from the source itself (full text, abstract of
record, release notes, or the paper's own indexed full text), not from a bare search snippet.
**One access caveat:** the publisher PDF of Hayakawa et al. 2026 (ApJL) timed out on fetch; its
details below come from the IOPscience abstract page and the paper's indexed full text — flagged
where that matters.

---

## (a) RE-REDUCTION OF THE ARCHIVE — none found. This is the claim-killer category, and it is empty.

No publication was found, in any searched source, that re-processes the historical bead ΔR series
(or a substantial multi-eclipse subset of the 1970–2015 IOTA archive) with LOLA/Kaguya limbs, or
that publishes Watts→modern corrections applied to the published ΔR values of Dunham et al. (2016).

What exists instead is the archive authors' own repeated statement that this is *future work*:

- **Dunham, Sofia, Guhl & Herald 2016**, IAU Symp. 320, §4 "Future Work" (verified in the Cambridge
  PDF): "The results can be improved with a consistent reanalysis of the observations using the much
  more accurate lunar profile data that are now available from the Japanese Kaguya and NASA's LRO
  lunar orbiter observations." The same paper's results table is, by its own statement, "analyzed
  with lunar limb data from 'The Marginal Zone of the Moon' Watts (1963)."
- **Dunham et al., IAU GA 2015 talk (FM13p.21) and Solar Eclipse Conference 2014 talk:** the
  programme overview lists "Re-analyze all obs. with accurate profile data — eg, LRO" as a plan;
  the 2014 talk records that Dunham "worked with student interns to analyze most of these published
  past observations, as well as a backlog of video observations" — and the resulting table is the
  Watts-reduced one published in 2016. The re-analysis with modern profiles is announced in 2014,
  2015 and 2016 and never appears in print through Nov 2026.
- **Sôma 2012** (see (d)) likewise announces the intent — "By analyzing Baily's beads timing
  observations of past total and annular solar eclipses using the accurate lunar limb profiles we
  will be able to detect solar diameter variations" — and no resulting re-derived series by Sôma
  was found (his subsequent eclipse output is ΔT/historical-eclipse work and the 2012 Japanese
  public annular-eclipse campaign, Publ. Korean Astron. Soc. 30, 2015).

**Partial exception at the historical (pre-1970) end — see the Hayakawa entries in (e)/(f):** the
1715 anchor eclipse has been re-derived with modern topography in 2026, and the 1560/1567 Clavius
eclipses re-analysed. Those are individual historical events, not the 1970–2015 bead archive, and
the 1715 value enters the archive only through Fiala et al. (1994), not through the IOTA bead
programme. They narrow the seam's historical flank; they do not touch its core.

## (b) SINGLE-ECLIPSE re-measurements with Kaguya/LOLA profiles — the edges are populated

Each of these is one eclipse (or one team's homogeneous multi-eclipse photometry set), reduced with
spacecraft-altimetry limbs. None re-touches the IOTA archive's eclipses as a series.

| Eclipse | Authors / venue | Limb data | Radius derived (at 1 au) |
|---|---|---|---|
| 15 Jan 2010 (annular) | Adassuriya, Gunasekera & Samarasinha, *Sun and Geosphere* 6(1):17–22 (2011; cited 2012) | Kaguya, via Occult 4.0.8.6 | ΔR = +0.26 ± 0.18″ → **959.89″** |
| 15 Jan 2010 (annular) | Sigismondi et al., *Nuovo Cimento* / Raponi et al., IJMPD (2011–2012), LDF method | Kaguya LALT via Occult 4 | inflection point bracketed at ΔR ∈ [−0.19, +0.05]″ (no single value) |
| 11 Jul 2010, 13 Nov 2012, 3 Nov 2013, 20 Mar 2015 (total) | Lamy et al., *Solar Phys.* 290:2617–2648 (2015) | Kaguya topographic model, synthetic light-curve matching | per-eclipse 959.94 ± 0.02 / 960.02 ± 0.04 / 959.99 ± 0.09 / 960.01 ± 0.09; **mean 959.99 ± 0.06″** (17 determinations, 540 nm) |
| 21 Aug 2017 (total) | Quaglia, Irwin, Emmanouilidis & Pessi, *ApJS* 256:36 (2021) | LOLA SLDEM-256 + LDEM-128 (ME frame), DE430 | **959.95 ± 0.05″** (flash-spectrum video, southern limit) |
| 21 Aug 2017 (total) | Guhl & Tegtmeier, *J. Occultation Astronomy* 2018-3, pp. 19–21 | Occult with LOLA and Kaguya | northern limit **959.66″** (southern video overexposed/unreliable) |
| 21 Aug 2017 (total) | Jubier et al. (2021), as compiled in Wright & Young 2024, *AJ* 168:163 §6.4 | modern DEM (Solar Eclipse Maestro) | **959.98″** |
| 20 Apr 2023 (hybrid) | Guhl, *J. Occultation Astronomy* 2023-4, pp. 12–15 | Occult with LOLA and Kaguya | mean bead correction +0.38″ → **960.01 ± 0.12″** |
| 14 Oct 2023 (annular) | Quaglia, *J. Occultation Astronomy* 14(2), 2024-2 | LOLA-based bead matching | **960.00″**; from the same eclipse, the Dunhams' southern-limit annularity duration gives **959.92″** |

Pre-altimetry context (Watts-era, listed so RESULTS.md does not mistake them for modern-limb work):

- **Kubo 1993**, *PASJ* 45:819–829: eclipses of 1970, 1973, 1980, 1991 pooled; Moon's position/figure
  rectified by lunar-occultation data (Watts-profile era). Semidiameters 959.74 ± 0.008 (1970),
  959.84 (1973), … range **959.74–959.88″**.
- **Kilcik, Sigismondi, Rozelot & Guhl 2009**, *Solar Phys.* 257:237–250: 29 Mar 2006 eclipse →
  **959.22 ± 0.04″** — a full 0.7″ below the Lamy/Quaglia cluster, from the Watts/occultation-refined
  limb era (their paper's "real lunar limb vs Watts profile" comparison notwithstanding; Kaguya data
  were not public until Nov 2009). The same paper compiles 19 modern eclipses and claims the radius
  changes are "nonhomologous" (leptocline). This is the archive-era literature's own internal outlier
  and must be confronted, not ignored.

## (c) SOFTWARE / PREDICTION migration — happened, in two steps; it is NOT an archive re-reduction

- **2009:** David Herald reduced the newly released Kaguya (SELENE) LALT altimetry into Watts-format
  limb profiles so existing software could ingest them (corroborated by Sigismondi's 2013 review,
  *Mem. S.A.It.* 86:100 — arXiv:1211.4394 — and by the project's own PREDICTION.md).
- **By 2010–2011:** Occult 4 distributed the Kaguya profiles — Adassuriya et al. used Occult
  **4.0.8.6** "updated with the currently available most accurate lunar limb profile, the Kaguya Lunar
  Explorer data" for the Jan 2010 eclipse.
- **14 Feb 2021, Occult 4.12.2.0 release notes (Herald):** "Disabled the downloads of the Kaguya lunar
  limb profile in anticipation of removing all support for using this dataset. [It is fully superseded
  by the LOLA dataset.]"
- **27 Feb 2021, Occult 4.12.3.0 release notes (Herald):** "Removed all support for the Kaguya lunar
  limb data in Lunar occultations and Baily Beads… The files Kaguya.bin, KaguyaHiRes.bin and
  KaguyaHiRes.inx can be deleted."
- **Current practice:** IOTA's 2026 occultation-prediction guidance (occultations.org) instructs users
  to select **LOLA** under "Kaguya/LOLA profile data" in Occult 4; NASA's eclipse office states
  Kaguya/LRO profiles bring contact-time accuracy to ~0.2 s (vs ~0.5 s with corrected Watts); NASA SVS
  eclipse maps (Wright & Young 2024) are built from an 18,000-element LRO+Kaguya DEM limb.
- **The radius standard, separately, has NOT migrated in the almanacs:** Quaglia et al. (2021):
  Auwers' 959.63″ "is used in all published eclipse predictions — for example, in The Astronomical
  Almanac." Wright & Young (2024) §6.4: "Nearly all eclipse calculations use a de facto standard value
  of the solar radius first published more than a century ago" — while noting Irwin's 2024 April 8 map
  used 959.95″ (Irwin & Quaglia 2024) and shifted the northern limit by city blocks. So: limb data
  migrated (Watts → Kaguya ~2010 → LOLA-only 2021); the printed prediction radius remains Auwers.

## (d) WATTS-vs-MODERN comparison studies — the difference profile is old, documented knowledge

- **Morrison & Appleby 1981**, *MNRAS* 196:1013–1020: from 66,000 lunar occultations, systematic
  corrections to Watts' limb profiles; the Watts datum's radius varies with libration, producing
  systematic profile errors attaining **0.4″** at some position angles (also Van Flandern 1970;
  Morrison 1979 — datum elliptical, offset from centre of mass). The physical basis for expecting a
  Watts→modern correction of the same order as the claimed ΔR fluctuations has been in print for
  45 years.
- **Sôma 1999**, *Publ. Natl. Astron. Obs. Japan* 5:99–119: limb profiles refined from grazing
  occultations (the pre-spacecraft "real limb").
- **Kilcik et al. 2009** (above): published comparison figure "Real lunar limb vs Watts profile"
  (as presented in Sigismondi's 2010 IAP talk) in the course of the 2006-eclipse analysis.
- **Sôma 2012**, *Bull. Korean Astron. Soc.* 37(1): limb profiles generated for arbitrary libration
  from Kaguya **and** LRO topography; abstract states Watts' data contain "many kinds of errors…
  which seriously affected the results obtained from the analyses of the observations," and shows
  the new profiles fitting observed graze limbs. This is a profiles paper, not a ΔR re-reduction.
- **NASA eclipse office** (Espenak, "The Lunar Limb Profile and Eclipse Predictions"): Watts-based
  corrected predictions agree to <0.5 s; Kaguya/LRO improve this to ~0.2 s.

## (e) Post-2016 work by the archive's own authors — no archive revisit; the programme has wound down

- **Dunham:** no post-2016 paper re-reducing or revisiting the ΔR archive was found. Post-2016
  Dunham eclipse output is observational/web: the Dunhams observed the 14 Oct 2023 annular eclipse
  at its southern limit (their ~21 s annularity → S⊙ = 959.92″, reported inside Quaglia 2024, JOA —
  a modern single-eclipse estimate, not an archive correction). Dunham's own IOTA graze pages
  (2023, updated 2025) state, of bead-based diameter work: "IOTA used to strongly encourage
  accurately timed video observations of solar eclipses from near the edges of the paths… for
  measuring the solar diameter, but we came to realize the difficulty in deriving such information
  from such recordings." The custodian community has de-emphasized the programme; it has not
  re-reduced it.
- **Guhl** (Dunham et al. 2016 co-author): the 2018 and 2023 JOA single-eclipse analyses in (b) —
  modern-limb, per-bead residual tables, new eclipses only.
- **Herald:** the Occult migration in (c); no ΔR-archive paper.
- **Sofia:** no post-2016 eclipse-archive publication found; the Sofia radius line's last major
  statement is the SDS balloon work (Sofia et al. 2013, *MNRAS* 436:2151).
- **The sharpest post-2016 development comes from outside the author list — Hayakawa et al. 2026**
  (see (f)): a refereed paper that *excludes Dunham et al. (2016)'s data from its compilation figure*
  "as they have considerable data offsets with their probable source articles." The archive is now
  publicly flagged as internally inconsistent with its own sources — by name — but the flag is a
  compilation decision, not a re-reduction: nobody has yet published what the corrected values are.

## (f) The solar-cycle diameter-variation claims — contested state of the literature

**Still asserting variation (the claim side):**
- The Dunham/Sofia programme itself: ΔR fluctuations of 0.1–0.3″ presented as a solar-variability
  proxy via the Sofia–Li W-parameter relation (Dunham et al. 2016; Fiala, Dunham & Sofia 1994,
  *Solar Phys.* 152:97–104, "Variation of the solar diameter from solar eclipse observations,
  1715–1991" — the archive's foundational table, Watts-dependent by its own method description).
- Kilcik et al. 2009: compiled-19-eclipse claim of nonhomologous radius changes (leptocline).
- Sigismondi school, most recently **Sigismondi et al. 2024**, *Universe* 10(2):90 (review):
  "The variability of the solar diameter is sustained by several accurate measures in the last 130
  years as well as from historical eclipses since 1567"; notes the last decade's eclipse values
  cluster near 960.0″.

**Challenging on other grounds (the sceptical side — none of these uses the Watts mechanism):**
- **Kuhn, Bush, Emilio & Scherrer 2004**, *ApJ* 613:1241 (MDI/SOHO): cycle radius variability
  < **7 mas** after statistical correction.
- **Bush, Emilio & Kuhn 2010**, *ApJ* 716:1381 ("On the Constancy of the Solar Radius. III"): any
  cycle-synchronous intrinsic variation < **23 mas peak-to-peak**; secular drift < 1.2 mas/yr; if
  ground and space are both right, ground-based apparent variability must be terrestrial-atmosphere
  change. Emilio, Kuhn & Bush 2010 (IAU Symp. 264): MDI absolute radius 959.28 ± 0.15″, cycle
  upper limit 22 mas p2p. PICARD/SODISM: variations < ±20 mas in 2010–2011, uncorrelated with the
  cycle (Meftah et al. 2015).
- **Lefebvre et al. 2006**, *ApJ* 649:444 (Mount Wilson, 30+ yr): radius variations "not
  significantly correlated with the solar cycle."
- **Rozelot & Damiani 2012** (critical quality assessment of the historical corpus) and **Rozelot,
  Kosovichev & Kilcik 2018**; and **Rozelot & Kosovichev 2026**, "Do Modern Observations Pin Down
  the Solar Radius to Converge on New Standards?" (arXiv:2605.23794): §2.5 hails an "eclipse
  astrometry revival (2024)" due to Kaguya/LOLA profiles, quotes Lamy et al.'s 959.97 ± 0.06″, and
  concludes the **seismic** radius is the best determination — the 2026 review does not cite Dunham
  et al. (2016) at all.
- **Hayakawa, Sôma, Rozelot, Murata, Pevtsov, Gunár & Green 2026**, *ApJ Letters* (arXiv:2607.02347;
  DOI 10.3847/2041-8213/ae84b7): re-analysis of Clavius' 1560/1567 reports using modern lunar
  topography and ephemerides → 1567 upper limit R⊙ ≤ 959.92″; "no linear secular R⊙ shrinkage but
  possible R⊙ modulations on a centennial timescale"; compiles eclipse constraints (1567 ≤ 959.92″;
  1715 ≥ 959.91″; 1925: 960.14 ± 0.08″) and **excludes D+16's data from Fig. 5 over "considerable
  data offsets with their probable source articles."**
- **Hayakawa et al. 2026** (second paper; arXiv:2604.24503, cited in Rozelot & Kosovichev 2026
  §2.5): a modern-topography determination for **Halley's 1715 eclipse: 959.98 ± 0.23″** — i.e., the
  archive's most famous historical anchor (the 1715-vs-1979 "0.4″ shrinkage" of Dunham et al. 1980,
  *Science* 210:1243) has been re-derived with modern limb data, landing essentially on the modern
  cluster, not on the Watts-era value.

Net contested state: the *space-based* literature capped true cycle variation an order of magnitude
below the eclipse ΔR fluctuations a decade before Dunham et al. 2016; the eclipse-variation claim
survives mainly inside the IOTA/Sigismondi literature; and since 2026 the archive's table is
additionally under a published data-consistency cloud. What no sceptic has done is attack the
archive on its own ground — the limb datum. The challenges are all "space says the Sun doesn't do
that," never "your ΔR values are Watts artefacts, and here are the corrected ones."

---

## VERDICT — the seam is NARROWED, but still OPEN

- **Closed/narrowed parts:** (i) prediction and reduction *practice* migrated a decade ago
  (Kaguya in Occult by ~2010; LOLA-only since Feb 2021) — "the field still uses Watts" is false for
  new work and must never be claimed; (ii) every well-observed eclipse since 2010 already has a
  modern-limb radius, clustering at 959.92–960.02″; (iii) the historical flank is being re-derived
  piecemeal (1715 in 2026; 1560/1567 in 2026); (iv) the archive's credibility is already damaged in
  print (Hayakawa et al. 2026's exclusion), so "first to question the archive" is also not available.
- **Still open — the core:** nobody has published a Watts→Kaguya/LOLA correction applied across the
  Dunham et al. (2016) ΔR table, nor any re-reduction of a substantial subset of the 1970–2015 IOTA
  bead series. The archive's own authors proposed exactly this in 2014/2015/2016 as future work and
  never executed it; Sôma announced the same intent in 2012 and never published the series. The
  specific, load-bearing artefact — the ΔR series as printed, and the cycle-proxy conclusion drawn
  from it — remains un-audited on its own terms.

## SURVIVING NOVELTY CLAIM (tightest defensible form)

> "Dunham, Sofia, Guhl & Herald (2016) published the IOTA Baily's-bead ΔR series (1970–2015)
> reduced against Watts (1963), and stated that a consistent re-analysis with Kaguya/LRO limb
> profiles was needed. That re-analysis was never published. This work is the first to apply a
> uniform Watts→modern-limb differential correction to the full published ΔR series and to test,
> under pre-registered rules, whether its claimed solar-cycle correlation and its mean level
> survive the removal of the Watts datum."

Every clause of that is sourced above. Anything stronger — "first modern-limb eclipse radius,"
"the field still reduces with Watts," "first to doubt the archive" — is contradicted by (b), (c)
and (e) respectively.

## WHAT RESULTS.md MUST CITE OR CONCEDE

1. **Dunham et al. 2016, §4** — the re-analysis was the archive authors' own stated future work;
   this project executes their programme, it does not ambush it. Frame accordingly.
2. **Hayakawa et al. 2026 (ApJL, Clavius)** — concede that D+16's table was already publicly
   flagged for "considerable data offsets with their probable source articles" and excluded from a
   refereed compilation. Our transcription of the ΔR table should be checked against the "probable
   source articles" (Fiala et al. 1994 and the per-eclipse papers) wherever the two disagree, and
   any such disagreement reported — Hayakawa's remark makes this a known hazard, not a detail.
3. **Hayakawa et al. 2026 (1715; arXiv:2604.24503)** — 959.98 ± 0.23″ for 1715 with modern
   topography; cite as the re-derived historical anchor and as prior art for single-event
   re-derivation.
4. **Rozelot & Kosovichev 2026, §2.5** — the "eclipse astrometry revival" framing and the seismic
   radius as the field's current best determination; position Q2's comparators accordingly.
5. **Bush, Emilio & Kuhn 2010** — the <23 mas p2p space-based cap: any Q1 "SURVIVES" verdict must
   explicitly confront the order-of-magnitude tension and the definition difference (eclipse
   extinction edge vs MDI inflection-point radius) rather than claim a detected physical variation.
6. **Lamy et al. 2015; Quaglia et al. 2021; Guhl 2023; Quaglia 2024 (JOA); Guhl & Tegtmeier 2018**
   — the modern-limb single-eclipse cluster (959.92–960.02″) already exists; Q2's result is a test
   of the *corrected archive* against this cluster, not a new radius measurement.
7. **Kilcik et al. 2009** — the Watts-era 959.22 ± 0.04″ outlier and its 19-eclipse compilation;
   the corrected series should be compared against it explicitly, since it is the archive-era
   literature's own most discordant product.
8. **Morrison & Appleby 1981** — Watts datum systematics up to 0.4″ were published in 1981; the
   correction's *plausibility* is not novel, only its application to this series is.
9. **Occult release notes (4.12.2/4.12.3, Feb 2021) and IOTA 2026 guidance** — concede the
   prediction-side migration; the "959.63″ is still the prediction standard" clause stands on
   Quaglia et al. 2021 and Wright & Young 2024 (*AJ* 168:163, §6.4), and should be stated as an
   almanac/de-facto standard, with Irwin's 2024 map (959.95″) noted as the first prominent break.
10. **Dunham's IOTA pages (2023/2025)** — the custodian community has itself de-emphasized
    bead-derived diameters; cite when framing impact (the audit closes out a programme its owners
    have wound down, which cuts both ways and should be said plainly).
