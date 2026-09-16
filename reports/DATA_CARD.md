# ASDMotion / ASDPose: measured release card

Audit date: 2026-09-16. Raw versions are identified by [`manifest.json`](../data/raw/manifest.json). This is a local-file audit; publication facts and release measurements are different evidence types.

## Contents

1. [Task and population](#task-and-population)
2. [Labeled clips](#labeled-clips)
3. [Continuous recordings](#continuous-recordings)
4. [Research implications](#research-implications)
5. [Reproduction and remaining work](#reproduction-and-remaining-work)

## Task and population

The original study detects stereotypical motor movements (SMMs) in a selected ASD cohort. A negative movement label does not mean a non-ASD child. The study does not establish diagnostic discrimination or the psychological function of a movement. [Barami et al. (2024/09), Introduction/Methods](https://doi.org/10.1001/jamanetworkopen.2024.32851).

## Labeled clips

All 36,930 records in `dataset.pkl` were inspected. There are 8,267 positive and 28,663 negative clips, each with a `[T,17,2]` coordinate array, `[T,17]` confidence, movement label, fps, identifier and boundary metadata. The release differs from the paper's stated 36,000 selected segments. [Measured dataset summary](../data/processed/dataset_summary.json); [schema](../data/processed/dataset_structure.json).

| Property | Measured result | Interpretation |
|---|---:|---|
| Train / test rows | 32,179 / 4,751 | No distinct validation set supplied |
| First-token groups | 289 / 40 | Disjoint, but not verified participant identities |
| 25-fps negatives / positives | 28,663 / 1,747 | Acquisition is associated with label |
| 30-fps negatives / positives | 0 / 6,520 | fps alone can identify many positives |
| All-zero poses | 3,264 negative / 12 positive | Missingness is also associated with label |
| Median duration | 12 seconds | Positive 8.04 s vs negative 13.04 s |
| Repeated identifiers | 2 beyond first occurrence | Correspond to different arrays; retain record_index |
| Exact-coordinate cross-split hashes | 43 | All are zero arrays; no nonzero duplicate hash crossed |
| Multi-label clips | 1,572 | Comma-separated movement names need multilabel parsing |
| Confidence outside [0,1] | 49,851 entries | Scores cannot be assumed bounded probabilities |

Sources: [split audit](../data/processed/released_split_audit.json), [fps table](../data/processed/fps_label_crosstab.csv), [shortcut audit](../data/processed/shortcut_audit.json), [quality summary](../data/processed/quality_motion_by_label.csv), [dataset summary](../data/processed/dataset_summary.json).

The post-hoc rule “30 fps predicts positive” gives precision 1.000 and recall 0.789 on the full release without inspecting motion. This is a descriptive integrity check chosen after seeing the data, not an untouched holdout benchmark. It does not show that the published model learned this specific rule. [Rule implementation](../scripts/04_shortcut_audit.py).

The fields called start_frame/end_frame do not behave like array-frame indices. For most records, array duration minus the difference is approximately two seconds. Second-based annotation plus padding is a plausible interpretation requiring validation, not an established conversion rule. [Timing diagnostic](../data/processed/shortcut_audit.json).

## Continuous recordings

Every numeric file in the continuous ZIP was successfully decoded; the full ZIP CRC check passed. The archive has 914 skeleton recordings plus `db.csv`, with 241 explicit child IDs and 318 assessment groups. The explicit metadata table is useful but does not establish its crosswalk to the separate labeled-file identifiers. [Archive inventory](../data/processed/archive_summary.json); [continuous summary](../data/processed/continuous_summary.json).

The continuous release has 62,698,358 pose frames and 599.77 camera-stream hours. About 32.18% of frames are all-zero; two streams are entirely zero. Every stream has one person slot `[1,T,17,2]`. Stored frame rates are often fractional, ranging from 21.6949 to 30.3008. [Complete recording profile](../data/processed/continuous_inventory.csv).

Declared frame_count differs from array length in 234 recordings; all differences match the stored adjust field. This accounting identity does not reveal which timestamps were changed. There are 176,069 out-of-range confidence entries and no nonfinite coordinates/confidence. [Continuous summary](../data/processed/continuous_summary.json).

## Research implications

Proposed priority: test whether recognition survives acquisition and quality controls before comparing larger models. Preserve low-visibility time as unobserved; do not turn it into evidence of no SMM. Compare body-relative motion and periodicity with quality-only and metadata-only diagnostic controls. Establish verified child-disjoint evaluation first.

Full-session burden needs exhaustive aligned labels, synchronization/duplicate-camera rules and an observable-time denominator. Clip-level subtype analysis is feasible in principle, but labels such as Fingers do not provide finger-joint coordinates. Diagnostic, causal, emotional-function and treatment claims need additional observations and study design. These are our methodological conclusions, not new clinical findings.

## Reproduction and remaining work

Run the numbered scripts listed in [README](../README.md). Our 16 tests passed, including 10 counterexamples reproducing upstream defects; those passing tests do not mean the upstream is fixed. No GPU training or original-score reproduction ran. [Test log](../logs/tests.log); [source audit](pipeline_audit.md).

The strongest unresolved dependencies are the release-version explanation, verified labeled-to-continuous participant crosswalk, timing/padding semantics and complete event annotation. Questions are saved in [OPEN_QUESTIONS](../docs/OPEN_QUESTIONS.md). Recent research is indexed separately in [literature_survey.md](literature_survey.md); independent reuse of the released files was not verified within that search.
