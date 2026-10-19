# Cellular Receiver Reuse in Molecular Communication

Analysis code, frozen protocols and frozen results behind the paper *Cellular Receiver Reuse in Molecular
Communication: Response Prediction and Calibrated Waiting*. The manuscript itself is not part of this
repository; everything here is the computation it reports.

The work asks how long a transmitter must wait before stimulating the same living cell again. A cell used as a
molecular receiver keeps a biochemical trace of the previous command, so its response to the next one is weaker
until it recovers. Two questions follow, and they rest on different evidence:

| Question | Evidence |
| --- | --- |
| Can the response be predicted? | measured single-cell FGF2–ERK trajectories |
| Can a waiting rule meet a reliability requirement? | simulation of the published B3 signalling model |

Every analysis was frozen in its own protocol, with a SHA-256 record, **before its single run**, and each one has
a verification script that recomputes its reported values. The freeze records are in `simulation/configs/`, and
each result file repeats the hash of the protocol that produced it.

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux, macOS
pip install -r requirements.txt

python simulation/code/fetch_author_sources.py    # once; the only step that needs the network
python scripts/reproduce.py --mode verify
```

The first command downloads the 106 original-author files the analyses read and checks every one against the
Git blob SHA recorded in the manifests. They are not redistributed here; see
[`simulation/public_data/NOTICE.md`](simulation/public_data/NOTICE.md) for what they are, where they come from
and why. Files already present and matching are left alone, so re-running it costs nothing.

`--mode verify` is the default. It runs 33 steps: the per-analysis verification scripts, the protocol and design
audits, synthetic end-to-end checks, and the pipeline checks. (The full repository runs two more, which
compile the manuscript.) It recomputes the reported values from the frozen
results and compares them against `reproduction/reference_metrics.json`. On the recorded run that was 48,039
compared entries with a maximum absolute error of 9.0e-17, in 21.6 minutes.

A step that fails writes its own log under `reproduction/logs/`, and `reproduction/run_report.json` records the
whole run together with the environment it ran in.

## Layout

| Path | Contents |
| --- | --- |
| `simulation/code/` | the analyses and one `verify_*.py` per analysis |
| `simulation/configs/` | frozen protocols and their SHA-256 freeze records |
| `simulation/results/` | the frozen outputs every reported number is read from |
| `simulation/public_data/` | manifests for the author files, which the fetcher downloads here |
| `reproduction/` | `run_report.json` and `reference_metrics.json` from the recorded run |
| `scripts/reproduce.py` | the entry point above |

## What this repository can and cannot check

`simulation/code/pipeline_checks.py` holds eight checks. Four of them run here:

- generated text is LF-only, so hashes match on every platform;
- the stimulation schedules are the pilot's, and single pulses start at the export origin;
- the pilot result files carry the fields the analyses read;
- per-cell normalisation uses only frames before the model origin.

The other four are skipped and say so, because their inputs are outside this repository: two read the manuscript
sources, to confirm that every number printed with four or more decimals equals a frozen value and that every
table and figure it includes exists; two read the prospective validation kit. A run here therefore prints
`pipeline checks passed (4 checks; 4 skipped, their inputs are not in this checkout)`.

`--mode full` re-runs the analyses from the raw data instead of verifying the saved ones. It also rebuilds the
manuscript's tables and figures, and that builder is not part of this repository, so use `--mode verify` here.

## Line endings

`.gitattributes` forces `* text=auto eol=lf`. Source files are verified by Git blob and SHA-256 hashes, so text
has to be byte-identical on every platform; the Windows default `core.autocrlf=true` would rewrite line endings
on checkout and fail those checks in a fresh clone.

## Data provenance

The measured time courses and the B3 posterior exports are the work of other authors and are downloaded, not
redistributed:

> Y. Blum, J. Mikelson, M. Dobrzyński, H. Ryu, M.-A. Jacques, N. L. Jeon, M. Khammash and O. Pertz,
> "Temporal perturbation of ERK dynamics reveals network architecture of FGF2/MAPK signaling",
> *Molecular Systems Biology* 15(11), 2019, e8947. DOI [10.15252/msb.20198947](https://doi.org/10.15252/msb.20198947)

with the associated Mendeley Data record (M. Dobrzyński, contributor Y. Blum, v2, 2020-05-13,
DOI [10.17632/ccnxn84w8z.2](https://doi.org/10.17632/ccnxn84w8z.2), CC BY 4.0) and the paper-linked repository
[`Mijan/LFNS_MSB`](https://github.com/Mijan/LFNS_MSB), branch `MSB_version`, pinned commit
`5c917abda0618d75c00c9cab45f24ed893dd71f1`. This work uses a numerical subset: no microscopy images and not the
full Mendeley archive. Author files keep their original paths and names.

## Licence

The code in this repository and the results it produces are released under the [MIT licence](LICENSE).

The licence does **not** cover the author files the fetcher downloads into
`simulation/public_data/fgf2_author_repository/`. They are not redistributed here, and
[`simulation/public_data/NOTICE.md`](simulation/public_data/NOTICE.md) records their provenance and terms: the
paper is open access and the Mendeley data record is CC BY 4.0, while the `Mijan/LFNS_MSB` repository carries no
licence at its root, which is why this repository fetches those files instead of shipping them.

## Environment

The recorded run used Python 3.13.3, NumPy 2.3.2, pandas 2.3.2, Matplotlib 3.10.6 and openpyxl 3.1.5; the exact
environment of any run is written to `reproduction/run_report.json`, and the pilot's historical environment is
in `simulation/results/fgf2_pilot/runtime_versions.json`.

Batched B3 simulations use a process pool sized to the CPU count. On a loaded machine a worker can be killed and
the step then fails with `BrokenProcessPool`; re-running that step succeeds.
