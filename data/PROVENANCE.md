# Data provenance — eclipse-radius audit

All datasets were acquired openly on 2026-11-17. `data/` is gitignored
except this file; every derived number in RESULTS.md is reproducible by
re-running `scripts/` on the files below as archived.

## 1. Published ΔR table — `data/dunham2016_table.csv`
- **Source:** Dunham, D. W., Sofia, S., Guhl, K. & Herald, D.,
  "Solar diameter measurements from eclipses as a solar variability
  proxy", *Proc. IAU Symposium 320* (2016), pp. 351–353.
- **URL:** open Cambridge PDF via resolve.cambridge.org (content id
  S1743921316000417a), archived as `data/dunham2016.pdf` (4 pp.).
- **Content:** the ΔR archive is the paper's **Figure 1 (p. 352)** — a
  plotted table, not machine-readable text. It was rendered at 300 dpi
  (`data/fig1page-2.png`) and transcribed by eye into the CSV: 27 events,
  1715-05-03 … 2006-03-29, each with type, number of observations,
  method, ΔR (arcsec, relative to 959.63″ at 1 au) and formal σ.
  The IOTA-era (≥1970) subset has 20 events, matching the paper's
  "20 annular and total solar eclipses".
- **Paper statements relied on:** the table was "analyzed with lunar
  limb data from 'The Marginal Zone of the Moon' Watts (1963)" (p. 352);
  most beads are defined by features in the lunar polar regions;
  Fig. 2's analysis used beads "within 30 degrees of the lunar north
  and south poles"; the authors' own assessed *real* errors are
  ±0.2″ (video era) and ±0.4″ (visual era), vs formal σ's ~4× smaller;
  §4 explicitly calls for "a consistent re-analysis of the observations
  using the much more accurate lunar profile data … from the Japanese
  Kaguya and NASA's LRO" — the audit this project performs at the
  published-ΔR level.
- **Transcription verification (2026-11-17, second pass):** after the
  novelty audit flagged Hayakawa et al. (2026)'s exclusion of this
  table over "considerable data offsets with their probable source
  articles", every transcribed value was re-read against the rendered
  Figure 1 image digit-for-digit. The transcription is exact as
  published (including the one-decimal values −0.5, +0.2, +0.4). The
  disagreements with Fiala et al. (1994) logged in
  `outputs/crosscheck_sources.csv` are therefore genuine differences
  between the 2016 re-reduction (WinOccult/Solrad 2-parameter
  solutions on beads within 30° of the poles, per Dunham's IAU GA
  2015 talk) and its 1994 source, not digitization errors.
- **Raw bead timings:** not openly downloadable (held in the IOTA /
  Occult observation archives; no public per-bead table found). This
  limit is declared in PREDICTION.md §4.2 and RESULTS.md; the audit
  works at the level of the published ΔR values, per the registered
  design.

## 2. Watts (1963) limb profiles — `data/watts.dat.gz` → `data/watts_grid.npz`
- **Source:** VizieR catalogue **VI/122**, "The Marginal Zone of the
  Moon (Watts 1963)", digitised by HMNAO (late 1960s) and converted to
  grid format by USNO (early 1970s).
- **URL:** https://vizier.cfa.harvard.edu/vizier/ftp/cats/vi/122/watts.dat.gz
  (24 MB gz; 79,617,600 bytes decompressed = 13,269,600 × 6-byte
  records, exactly as the catalogue ReadMe specifies).
- **Format** (catalogue ReadMe + `doc.txt`, Herald 2006, both archived
  as `data/watts_ReadMe.txt` and fetched from the same directory):
  6-byte fields — signed height in 0.01″ (Fortran I4, space-padded),
  accuracy codes a, b. Blocks: 91 longitude librations (+9°…−9°),
  81 latitude librations (+8°…−8°), 1800 Watts angles (0°…359.8°),
  all at 0.2° steps; plus the documented trailing zero block
  (verified present and all-zero by `scripts/parse_watts.py`).
- **Frame notes (doc.txt §6):** heights are for the Moon's mean
  distance (384,400 km); the Watts Angle zero point is offset from the
  axis angle by +0.21° (Scott 1988: 0.214°), and an inclination term
  −0.022·cos(elongation from ascending node) applies when converting
  axis angle → Watts angle (Watts used I = 1.564° vs the modern
  1.542°). Both are applied in `scripts/correct_and_test.py`.
  Known defects carried by the dataset's own documentation: the
  Cassini regions near the poles are poorly covered (northern limb at
  positive latitude libration reads too low in WA 345–355°), and the
  WA = 36.0° chart in the USNO file was erroneous and was replaced by
  Herald with manually read values (doc.txt §5).

## 3. Modern limb profiles — `data/LDEM_128.IMG` → `data/lola_profiles.npz`
- **Registered plan vs. what happened:** PREDICTION.md §2(b) named
  Herald's Kaguya (SELENE) LALT reduction to Watts-format profiles
  (Occult 4 distribution) as the modern comparator. That dataset's
  distribution channel no longer exists: Occult 4.12.2 (Feb 2021)
  disabled its download "in anticipation of removing all support",
  and 4.12.3 removed Kaguya support entirely — *"It is fully
  superseded by the LOLA dataset"* (IOTA release notes). The
  standalone "Kaguya For Eclipses" file (Herald 2009; blocks over
  L ±9°, B ±1.6°, 1800 axis-angle values) survives only as a ReadMe
  in the Occult GitBook help files; the data file itself could not be
  obtained from any open source. The audit therefore uses **LOLA**
  directly — the successor dataset the ecosystem itself adopted.
  This substitution is declared as a forced deviation in RESULTS.md.
- **Source:** NASA PDS Geosciences Node, LRO LOLA GDR,
  product **LDEM_128** (LRO-L-LOLA-4-GDR-V1.0, V3.0, created
  2017-09-15): global radius grid, 128 px/deg (236.901 m/px),
  23040 × 46080 int16, radius = DN × 0.5 + 1,737,400 m, Mean-Earth /
  polar-axis frame of DE421.
- **URL:** https://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/lola_gdr/cylindrical/img/LDEM_128.IMG
  (2,123,366,400 bytes, exactly 23040 × 92160 as the label specifies);
  label archived as `data/ldem_128.lbl`.
- **Reduction:** `scripts/extract_lola_profiles.py` builds silhouette
  profiles (max projected radius per 0.2° axis-angle bin, ±14° band
  about the limb plane) at each event's libration, expressed as
  angular height above the 1737.4 km reference sphere at the Moon's
  mean distance 384,398.55 km — the same convention as Herald's
  Kaguya file (heights "above a mean lunar limb centred on the centre
  of mass, with the moon being at its mean distance").
- **Relation to the registered SLDEM2015 spot-check:** SLDEM2015
  covers only ±60° latitude and cannot see the polar limb zones this
  audit is about; LDEM_128 (full polar coverage) is used instead and
  the substitution is declared. LDEM's polar grid cells are filled
  with the GMT `surface` interpolator where LOLA tracks are sparse
  (label DESCRIPTION) — a declared caveat for the polar windows.
- **Referencing (datum) note:** `lola_profiles.npz` heights are
  relative to the LDEM 1737.4 km reference sphere. The ΔR bookkeeping
  is done on the reduction framework's adopted mean limb — the
  classical eclipse constant k = 0.2725076 (Earth radii 6378.137 km,
  mean distance 384,398.55 km → mean-limb radius 1738.091 km), the
  constants printed in Herald's Kaguya Watts-format ReadMe. The
  constant offset between the two datums, 0.3707″, is applied in
  `scripts/correct_and_test.py` (REFERENCE_TERM) so that Watts and
  LOLA heights are compared on a common datum before differencing.
  External validation of this referencing: for 1715, Fiala et al.
  (1994)'s Watts-era ΔR (+0.48) minus Hayakawa et al. (2026)'s
  modern-topography re-derivation (ΔR = +0.35) implies a limb
  correction of +0.13″; this pipeline's δ̄ for 1715 is +0.166″.

## 4. Ephemeris — `data/de440.bsp`
- **Source:** JPL DE440 via the URL used by skyfield's loader,
  https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440.bsp
  (119,799,808 bytes; coverage 1549–2650). Downloaded with curl after
  skyfield's own downloader failed on the proxy's TLS chain; the file
  is the unmodified JPL kernel.
- **Use:** `scripts/event_geometry.py` — greatest-eclipse instant
  (minimum geocentric Sun–Moon separation) and optical libration
  (l, b) at that instant, using the IAU 2009 mean lunar rotation
  elements (Archinal et al. 2011). Validation: for 2006-03-29 the
  computed greatest eclipse is 10:11:18 UTC vs Espenak's published
  10:11:17.6 UT (NASA/TP-2004-212762 Besselian elements page), and
  the computed geocentric libration (l = +2.21°, b = −0.38°) is
  consistent with the bulletin's topocentric value at a central-line
  site (l = +2.07°, b = −0.13° at 10:30 UT).

## 5. Cycle proxy — `data/silso_yearly.csv` (+ `data/silso_daily.csv`)
- **Source:** WDC-SILSO, Royal Observatory of Belgium, Sunspot Number
  v2.0, yearly mean total sunspot number (1700–present).
- **URL:** https://www.sidc.be/SILSO/DATA/SN_y_tot_V2.0.csv
  Licence CC BY-NC 4.0; credit: "Source: WDC-SILSO, Royal Observatory
  of Belgium, Brussels", doi:10.24414/qnza-ac80.
- Values used are the yearly means for each event's calendar year
  (e.g. 1715: 45.0 — based on sparse early observations, flagged in
  RESULTS.md; 1970: 148.0; 1999: 136.3; 2006: 24.7). The daily file
  (sndtotcsv.php) was also archived but is not used by the registered
  analysis.

## 6. Software environment
- Project venv `~/workspace/eclipse-radius/.venv`: Python 3.12,
  numpy, scipy 1.18.1, skyfield 1.55, jplephem. All scripts run under
  it (`.venv/bin/python scripts/<name>.py`).

## 7. Cross-check sources (transcription audit, 2026-11-17)
Used only for the RESULTS.md cross-check log and the labelled
Fiala-substitution sensitivity; the primary correction uses Dunham
et al. (2016) values for all 27 events (see PROVENANCE §1).
- **Fiala, Dunham & Sofia 1994**, *Solar Phys.* 152:97–104, ΔR table
  as reproduced in Sigismondi 2008, *AIP Conf. Proc.* 966:341–348,
  Table 1 ("from Fiala et al. (1994) + our data") — 9 overlapping
  events (1715, 1925, 1976, 1979, 1980, 1981, 1983, 1984, 1987-09-23).
  Cross-verified against the second reproduction in Sigismondi 2008,
  "Measures of Solar Diameter with Eclipses: Data Analysis,
  Problems and Perspectives", Table 1 (agrees on all shared rows
  except 1715's σ: 0.20 there vs 0.02 in AIP 966 — a typo in one
  reproduction; 0.20 adopted, matching Dunham 2016's σ).
  Access route: the ICRA PDFs (icra.it/solar/) are no longer served
  by the rebuilt site; the texts were read via the search engine's
  cached extraction of those exact URLs on 2026-11-17. The extracted
  values are preserved in `outputs/crosscheck_sources.csv`.
- **Thompson / IOTA intermediate analyses** for the 1994 and 1999
  eclipses, as reported in *Occultation Newsletter* 13(3), 2008
  (Dunham's programme status report): 1994-05-10 ΔR = −0.27 ± 0.02;
  1999-08-11 ΔR = +0.06 ± 0.06.
- **Sigismondi 2008** (AIP 966) own analyses: 2005-10-03 southern
  limit ΔR = 0.00 ± 0.17; 2006-03-29 (Egypt beads) ΔR ≈ 0.00…−0.01
  ± 0.17 (the latter from the companion data-analysis paper).
- **Kilcik, Sigismondi, Rozelot & Guhl 2009**, *Solar Phys.*
  257:237–250: 2006-03-29 radius 959.22 ± 0.04″ (ΔR = −0.41).
- **Hayakawa, Sôma, Rozelot et al. 2026** (ApJL; and the companion
  1715 paper, arXiv:2604.24503): compiled constraints 1715 ≥ 959.91″,
  1925 = 960.14 ± 0.08″; modern-topography re-derivation of Halley's
  1715 eclipse, 959.98 ± 0.23″. Values as reported in NOVELTY_AUDIT.md
  §(e)/(f) (the audit read the IOPscience abstract page and indexed
  full text; the publisher PDF timed out on fetch — its caveat, kept).
