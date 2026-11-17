# Eclipse Reduction — Code

**Code for the re-reduction of the historical solar-eclipse archive against
modern lunar topography (LOLA): solar radius 959.494 ± 0.044″, and a probable
sign error in the canonical Dunham (2016) series.**

Manuscript: https://github.com/atharva-chourey-lab/eclipse-radius

## What this code does

- `scripts/parse_watts.py` — parses the Watts (1963) lunar-limb charts into a
  sampling grid.
- `scripts/extract_lola_profiles.py` — extracts lunar-limb silhouettes from the
  LOLA LDEM_128 digital elevation model.
- `scripts/validate_frames.py` — establishes the Watts frame/sign conventions
  empirically (the conventions used by the main analysis are documented in its
  output and in `RESULTS.md`).
- `scripts/event_geometry.py` — computes per-event geometry (libration,
  position-angle windows) for the historical eclipse archive.
- `scripts/correct_and_test.py` — the main analysis, implementing
  `PREDICTION.md` exactly as registered: applies the Watts→LOLA correction
  (mean +0.100″; south +0.271″, north −0.071″) to the published series, runs the
  registered Q1/Q2 tests, and compares the Fiala (1994) and Dunham (2016)
  archives event-by-event (they differ on 7 of 9 overlaps, with five sign flips).

Committed outputs: `outputs/corrected_series.csv`, `outputs/event_geometry.csv`,
`outputs/crosscheck_sources.csv`, `outputs/q1_q2_results.json`. The Dunham
Fig. 1 extraction is tabled in `data/dunham2016_table.csv`.

## How to run

```bash
python3 scripts/parse_watts.py
python3 scripts/extract_lola_profiles.py
python3 scripts/correct_and_test.py
```

Requires Python 3 with numpy/scipy (see script imports).

## Data — not redistributed

The large source files are **not** in this repository: the LOLA LDEM_128 DEM
(~2 GB, NASA/PDS), the JPL DE440 ephemeris (`.bsp`), and the raw Watts data
file. `data/PROVENANCE.md` records exactly where each comes from and how it was
processed; the small derived profile file `data/lola_profiles.npz` is included
so the main analysis can run without re-extracting from the full DEM. The
publisher PDF of Dunham (2016) is likewise not redistributed.

## Status

Research code as run for the manuscript — the registered analysis, not a
general eclipse-reduction package. `NOVELTY_AUDIT.md` records the prior-art
position (including Morrison, Stephenson & Parkinson 1988).

## Authorship and licence

**Author:** Atharva Chourey, Atharva Chourey Lab (independent research lab)

The Atharva Chourey Lab is a human–AI collaboration: Atharva Chourey works with
Lapis (Muse), an AI research partner. All results are framed as the
collaboration's.

Code in this repository is released under the **MIT License** (see `LICENSE`).
The associated manuscripts are published separately under CC BY 4.0 — the code
licence and the paper licence are deliberately different.
