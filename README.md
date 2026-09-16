# ASDMotion research workspace

Data-first investigation of [Dinstein-Lab/ASDMotion](https://github.com/Dinstein-Lab/ASDMotion), started 2026-09-16.

Start with the compiled dossier in `outputs/latex/main.pdf` (source: `docs/latex/main.tex`). Then read `docs/PROJECT_STATE.md` and `docs/OPEN_QUESTIONS.md`. These files preserve the state needed to continue without conversation history.

## Repository scope and raw video

This Git repository includes code, research documentation, LaTeX source, the small compiled report and summary figures. **Datasets, processed data tables, checkpoints, downloaded papers, source copies and temporary files are local-only.** Owner-hosted download links are in [data/README.md](data/README.md); upstream references are in [references/UPSTREAM.md](references/UPSTREAM.md).

The public ASDPose release **does not include raw RGB video**. The [paper, page 9](https://doi.org/10.1001/jamanetworkopen.2024.32851), states that raw video is excluded to maintain privacy. The available files contain skeleton trajectories and metadata.

The directory tree below describes the full local workspace; ignored download/analysis directories are regenerated after cloning. Links to local JSON/CSV evidence in the reports are reproduction paths and are intentionally not hosted in Git.

The first finding is a release mismatch and acquisition confounding, not a new model score. The current labeled file has 36,930 clips; every negative is tagged 25 fps, while 6,520 positives are tagged 30 fps. Missing-pose patterns also differ by label. These observations must be reconciled before interpreting model performance. See `data/processed/shortcut_audit.json` and the report for qualifications.

## Structure

```text
configs/                  Analysis definitions and experiment template
data/raw/                 Original downloads and SHA-256 manifest; immutable inputs
data/interim/             Extracted small metadata; rebuildable
data/processed/           Clip/recording inventories, quality and split audits
docs/latex/               Modular LaTeX source
docs/decisions/           Decisions with reasons and evidence
docs/PROJECT_STATE.md     Completed work, limits, continuation entry point
docs/OPEN_QUESTIONS.md    Unresolved release/mapping questions
external/ASDMotion-main/  Unmodified upstream source snapshot
images-from-papers/       Original source-page renders, not redrawn figures
references/papers/        Original/related papers and download manifests
references/source_snapshots/  Commit records and fork source
reports/                  Human-readable paper, code and literature analyses
reports/figures/          Generated release plots and real motion examples
scripts/                  Numbered reproducible analysis steps
src/asdmotion_research/   Restricted numeric-pickle IO and temporal primitives
tests/                    Semantic tests and upstream counterexamples
outputs/latex/            Compiled report
logs/                     Analysis and compilation logs
subagent-reviews/         Independent source/audit notes
```

## Run the completed analyses

The existing `.venv` uses Python 3.12 and CPU analysis libraries. It is not an environment for the old MMAction2/OpenPose stack. `requirements-analysis-lock.txt` pins portable analysis dependencies. The full local runtime inventory `requirements-lock.txt` remains ignored because it includes machine-specific packages; `requirements.txt` is the smaller dependency specification.

```powershell
# From this folder, reuse the already prepared environment:
& .venv/Scripts/python.exe scripts/01_profile_dataset.py
& .venv/Scripts/python.exe scripts/02_descriptive_analysis.py
& .venv/Scripts/python.exe scripts/04_shortcut_audit.py
& .venv/Scripts/python.exe scripts/05_inspect_archive.py --check-crc
& .venv/Scripts/python.exe scripts/06_motion_examples.py
& .venv/Scripts/python.exe scripts/07_profile_continuous.py
& .venv/Scripts/python.exe -m unittest discover -s tests -v
```

`01` and `06` load the roughly 5 GB labeled pickle into memory. Run them sequentially; allow memory overhead. `07` streams one recording at a time from the compressed archive and avoids extracting roughly 28 GB. `05 --check-crc` reads/decompresses the full archive to verify ZIP integrity. None of these train a model.

On another machine:

```powershell
python -m venv .venv
& .venv/Scripts/python.exe -m pip install -r requirements.txt
& .venv/Scripts/python.exe scripts/fetch_upstream.py
& .venv/Scripts/python.exe scripts/00_download.py
```

Downloads are about 13 GB in total. Existing completed downloads are preserved; `--manifest-only` hashes them without downloading. Partial downloads are resumed by gdown. The custom unpickler allows only the numeric NumPy globals observed in this release; it does not execute the model checkpoint and is not a general-purpose resource sandbox.

Before committing or pushing, run `python scripts/check_git_payload.py` after staging. It rejects data/model blobs and files larger than 1 MB. The local datasets are never deleted by this Git setup.

## Future split creation is deliberately explicit

`scripts/03_make_grouped_splits.py --mapping PATH` requires a CSV with `identifier,subject_id,partition`, using verified subject identities and `train/validation/test`. It refuses missing mappings, subject overlap and nonzero exact-coordinate overlap across partitions. Identifier prefixes in the clip inventory are candidate groups, not verified identities. The current release split is preserved and audited; it is not silently rewritten.

There are all-zero arrays shared across the released split. They are missing-data collisions, so the split validator does not treat them as duplicate observed motion. A future experiment must still state its unusable-record policy and report exclusions/coverage by child and label.

## Build the report

```powershell
./scripts/build_report.ps1
```

The script uses a PATH Tectonic or the installed Codex LaTeX plugin, with `-Tectonic` available for an explicit path. Tectonic may need network access for packages on a fresh machine. Edit the section `.tex` files, then rebuild. `references/references.bib` is provided for future manuscripts; this dossier uses a small inline author-year bibliography and direct primary-source links.

## Evidence conventions

- **Paper-reported:** a claim from the publication, with page/section attribution.
- **Measured release property:** a statistic from the downloaded file and saved analysis output.
- **Source-code observation:** behavior at pinned snapshots, with line references or tests.
- **Proposal/inference:** a new hypothesis or interpretation requiring validation.

SMM-negative is not non-ASD. Clip hours are not unique participant hours. Neither downloaded data nor a passing test establishes clinical validity. No neural-network training or published-score reproduction has been claimed.
