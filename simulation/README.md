# Simulation

Everything the reported numbers are computed from.

| Path | Contents |
| --- | --- |
| `code/` | the analyses, and one `verify_*.py` for each of them |
| `configs/` | the protocol of every analysis, each with a SHA-256 freeze record beside its results |
| `results/` | the frozen outputs that every reported value is read from |
| `public_data/` | manifests identifying the original-author files, which `code/fetch_author_sources.py` downloads here |

Each analysis reads one protocol from `configs/` and refuses to run if that file differs from the hash
recorded with its results, so a protocol cannot be changed after the fact without the change being visible.
Each has a verifier in `code/` that recomputes the values it reports and asserts they agree.

`code/pipeline_checks.py` holds eight checks. Four of them run here: generated text is LF-only, the
stimulation schedules are the pilot's, the pilot result files carry the fields the analyses read, and
per-cell normalisation uses only frames before the model origin. The other four read the manuscript sources
and the prospective validation kit, neither of which is part of this repository, and report themselves as
skipped.

Run everything from the repository root with `python scripts/reproduce.py --mode verify`; see the root
`README.md`.
