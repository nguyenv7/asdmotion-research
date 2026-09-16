# Project state

Updated: 2026-09-16. Product: Codex desktop. Execution: Local Windows. Source-audit mode: parallel-subagents.

## Objective

Understand the ASDMotion data, measurement and algorithm pipeline before choosing a research direction. Build durable code, LaTeX documentation and a primary-source literature map.

## Completed

- Downloaded the ASDMotion source archive at recorded commit `f699dc7b7af5726df5d8e79161d192eac22cfafb`; preserved the unmodified snapshot and ZIP. Git HTTPS helper was unavailable, so a ZIP/API snapshot was used.
- Downloaded all three public data/model files, with sizes and SHA-256 in `data/raw/manifest.json`.
- Downloaded Barami 2024 paper and Supplements 1/2; archived source text and unmodified page renders.
- Profiled every labeled clip, including shapes, fps, labels, quality, duplicates, release split and candidate ID grouping.
- Inventoried and CRC-validated the continuous archive; ran a per-recording profile and inspected its explicit metadata table. See `continuous_summary.json` for the exact final results.
- Generated real skeleton examples, normalized wrist traces, descriptive plots and a clearly synthetic temporal aggregation demonstration.
- Reproduced ten upstream defects/edge cases in isolated counterexample tests; added six tests for our numeric reader and temporal utilities.
- Searched recent primary literature and distinguished actual reuse from citation. No independent reuse of released ASDPose files was verified within the search scope.
- Authored and compiled the 27-page LaTeX dossier plus separate paper/code/literature Markdown reports. The final PDF was rendered and visually checked; no clipped/overlapping content or unresolved references were found. See outputs/latex/qa/qa.json and docs/execution_ledger.json.

## Critical findings to retain

1. Labeled release: 36,930 records, 8,267 positive, 28,663 negative. This differs from paper counts.
2. fps: all negatives 25; positives 1,747 at 25 and 6,520 at 30. This allows strong post-hoc metadata-only separation.
3. All-zero pose clips: 3,276, including 3,264 negative and 12 positive. Keep missingness explicit.
4. Release train/test has 32,179 / 4,751 records and 289 / 40 distinct first-ID-token groups; those group meanings are unverified. Do not label them actual child counts.
5. Continuous ZIP has 914 pickles and db.csv with explicit 241 child IDs, 318 assessments, 914 camera records. Labeled-to-continuous crosswalk is unresolved. Its 599.77 camera-hours include 32.18% all-zero pose frames.
6. Boundary names start_frame/end_frame are misleading if treated literally: differences largely match clip seconds minus approximately 2 seconds. Units/padding require confirmation.
7. Paper headline precision/recall 66.82% / 92.53% uses selected reannotated segments; initial continuous-test frame precision/recall 36.64% / 87.72%.
8. Current upstream is not a verified paper-era environment. Confirmed code bugs do not prove those bugs affected published results.

## Not done / not claimed

No GPU model execution/training, reproduction of published scores, diagnostic classifier, clinical associations, complete event-label alignment, verified clip participant crosswalk, or outside contact. The checkpoint was downloaded but not loaded. No site was published and no author was emailed.

## Next entry point

Read the dossier's measured-data section, then `OPEN_QUESTIONS.md`. Obtain or validate release version, participant/timing mappings and continuous annotations. Implement a canonical manifest and a verified subject-disjoint validation split. Run metadata/quality controls before comparing motion models. Full-session burden evaluation is conditional on exhaustive aligned event labels and observation coverage.

## Rebuild

Public repository: https://github.com/nguyenv7/asdmotion-research (created and initial research commit pushed 2026-09-16). Initial research commit: `9ab4aa9`. Publication audit passed: 66 files, approximately 1.27 MB total, no dataset/model blobs, every file below 1 MB. All 16 semantic/unit checks passed. The publication policy is in decision 0002. Raw downloads, derived record-level outputs, downloaded papers and source snapshots remain local; owner links and manifests are versioned. See README.md for rehydrating a fresh clone. Raw videos are not publicly released (paper p. 9).

Commands are in README.md. Logs and JSON/CSV outputs capture actual results. `scripts/build_report.ps1` builds LaTeX. Update this file when new evidence resolves an open question; never replace an unresolved inference with an asserted fact solely because it is convenient for code.
