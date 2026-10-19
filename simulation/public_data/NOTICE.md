# Third-party sources

The analyses in this repository read measured time courses and model files produced by other authors. **Those
files are not redistributed here.** This directory keeps only the manifests that identify them, and
`simulation/code/fetch_author_sources.py` downloads them from their original location and checks every byte
against the recorded hashes.

The MIT licence at the repository root covers this repository's own code and the results it produces. It does
not cover the downloaded files.

## What is downloaded

| Manifest | Files | What they are |
| --- | --- | --- |
| `fgf2_source_manifest.json` | 47 | B3 model definition, measurement model, parameter bounds, posterior and the pilot's measured conditions |
| `fgf2_expanded_source_manifest.json` | 56 | the measured conditions and simulation exports added for the expanded fresh test |
| `fgf2_b3_source_manifest.json` | 3 | the authors' B3 posterior and simulation summaries |

Each entry records the file's path, its Git blob SHA, its size in bytes, its source URL and the date it was
retrieved. The fetcher writes a file only when the downloaded bytes reproduce the recorded blob SHA, so a run
that completes proves the analysis is reading the same inputs the reported numbers came from.

## Where they come from

All files are taken at the pinned commit `5c917abda0618d75c00c9cab45f24ed893dd71f1` of the paper-linked
repository [`Mijan/LFNS_MSB`](https://github.com/Mijan/LFNS_MSB), branch `MSB_version`, which accompanies:

> Y. Blum, J. Mikelson, M. Dobrzyński, H. Ryu, M.-A. Jacques, N. L. Jeon, M. Khammash and O. Pertz,
> "Temporal perturbation of ERK dynamics reveals network architecture of FGF2/MAPK signaling",
> *Molecular Systems Biology* 15(11), 2019, e8947. DOI [10.15252/msb.20198947](https://doi.org/10.15252/msb.20198947)

The associated data record is M. Dobrzyński (contributor Y. Blum), Mendeley Data v2, 2020-05-13,
DOI [10.17632/ccnxn84w8z.2](https://doi.org/10.17632/ccnxn84w8z.2), licensed **CC BY 4.0**.

## Why they are fetched rather than included

The paper is open access and the Mendeley data record is CC BY 4.0, which permits redistribution with
attribution. The `Mijan/LFNS_MSB` repository, however, carries **no licence at its root**, so there is no
explicit grant to redistribute the model and inference files it holds. Fetching them from the pinned commit
avoids redistributing anything while keeping the analysis exactly reproducible.

If you obtain these files another way, place them under `fgf2_author_repository/` with the paths the manifests
list; the fetcher will then verify them in place without downloading anything.
