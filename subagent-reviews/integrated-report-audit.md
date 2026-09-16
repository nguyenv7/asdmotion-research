# Integrated report audit

Audit date: 2026-09-16. Mode: sequential-single-agent independent audit within parent multi-agent workflow. Files read: `docs/latex/main.tex`, `data.tex`, `understanding.tex`, `research_plan.tex`; original main paper and supplements; processed clip summaries and inventory; source profile, split, shortcut, motion-example and temporal-helper code. No integrated report files were modified by this audit.

## Overall assessment

The integrated narrative correctly separates SMM recognition from ASD diagnosis, release measurements from paper claims, clip counts from independent children, and initial continuous testing from selected reannotation. All numerical release claims checked against the processed inventory agree. The confound-controlled, quality-aware research direction is appropriately presented as a proposal, with continuous burden, clinical associations and diagnosis conditional on missing evidence.

Three corrections are recommended before final compilation: include scored-frame coverage in the burden denominator; describe joint-level low confidence rather than unsupported joint-level missingness; and revise the grouped-split hash gate or its documented unusable-data policy so all-zero placeholder arrays do not masquerade as shared real movements. Smaller mathematical/wording clarifications follow.

## Findings and concrete fixes

### 1. Burden denominator must exclude unscored frames, not only poor pose

Location: `docs/latex/understanding.tex:73`.

Earlier text correctly leaves frames without any model window unknown. The burden formula then defines `o_t` only by whether the child is observable. A child can have a valid pose in an uncovered frame, leaving `z_t` undefined. If downstream code silently turns that unknown into zero while retaining it in observed time, burden is biased downward.

Suggested replacement: define `o_t` as 1 only when the child passes the predefined visibility/quality rule **and** a finite frame prediction exists. Define `D` with a sum over frames satisfying `o_t=1` rather than multiplying zero by potentially undefined/NaN `z_t`. `O` is valid scored observation time. If pose coverage and algorithm coverage differ, report both; otherwise label `C` valid scored coverage explicitly. Retain the existing requirement to report low coverage.

### 2. Joint-position statement uses low-confidence data, not zero/missing data

Location: `docs/latex/data.tex:52`.

The source statistic `joint_fraction_score_below_02` counts joint scores below 0.2; it does not separately report zero-confidence fractions for each joint. Thus “Missing joints are disproportionately common at wrists, knees and ankles” is stronger than the data used to support it.

Suggested replacement: “Low-confidence joint estimates (score below 0.2) are more frequent at wrists, knees and ankles than at shoulders.” Explain these are joint-frame weighted fractions, unlike the preceding mean of clip-level fractions. Source: `scripts/01_profile_dataset.py`, lines defining `joint_low`, `joint_counts` and their ratio; `dataset_summary.json`.

### 3. Split gate currently treats all-zero placeholders as coordinate leakage

Locations: `docs/latex/research_plan.tex:11`; `scripts/03_make_grouped_splits.py`, unconditional `groupby('coordinates_sha256')` overlap rejection.

The split checker rejects every shared coordinate hash across partitions. Yet the audit explicitly established that the 43 shared hashes in the released split are all-zero arrays, not evidence of repeated real motion. A verified child-disjoint mapping may therefore be blocked solely because unusable clips of equal length share zero bytes.

Recommended implementation policy: retain all-zero clips in an explicitly marked unusable-data stratum; report their overlap separately, and apply the movement-leakage blocking gate only to nonzero coordinate arrays. Alternatively require and document an explicit prior unusable-data exclusion decision and retain a record of exclusions by participant and label. Do not silently remove these clips or force unrelated children together just because they share zero arrays. Update the plan's description to match the selected policy. This audit does not alter the helper.

### 4. Define unavailable/degenerate motion features

Locations: `docs/latex/understanding.tex:7`, `:15`, `:31`.

The tutorial correctly retains missingness but should explicitly say normalization is undefined when no valid shoulder-width observations exist (or scale is nonpositive), energy is undefined when the usable adjacent-pair set is empty, and normalized autocorrelation is undefined for a constant trajectory. Those cases occur naturally in this release and should remain missing/unusable rather than zero. Define `T` as the number of samples in the contiguous valid interval and restrict lag to the valid range. These are interpretation requirements, not requests for a larger implementation or additional model training.

### 5. Distinguish split identifier-set count from row count

Location: `docs/latex/data.tex:34`.

The reported 32,179 training records is correct. The actual unique train identifier count in `dataset_structure.json` is 32,177; the difference arises from two repeated identifier strings, each associated with different arrays. The duplicate section already explains the issue, but a short parenthetical “32,177 unique identifier strings” near the split count would prevent readers interpreting the structural summary as contradictory. Test rows and identifiers both equal 4,751.

### 6. Limit person-axis statement to checked evidence or preserve shape inventory

Location: `docs/latex/data.tex:17`.

The displayed first record certainly has no person axis. The profiler normalizes either three-dimensional arrays or singleton-person four-dimensional arrays before saving its inventory, so the processed output by itself does not demonstrate that every original clip record lacks that axis. Suggested conservative wording: “This example has no explicit person axis; the profiler accepts either that layout or a singleton-person axis.” If the author independently verified all original shapes, the stronger statement can remain with that evidence recorded.

### 7. Continuous-archive completion statement must follow the in-flight audit

Locations: `docs/latex/main.tex` provenance section; `docs/latex/archive_facts.tex`; Phase 0/1 of the plan.

At audit time `archive_summary.json` records full ZIP inventory/CRC plus one sample schema, and `archive_facts.tex` is still a placeholder. This is consistent with the main text's limited sample-schema wording, but the final report should replace the placeholder and describe the independent full continuous-profile scope only after the archive agent's output completes. Do not equate child-only axis metadata with validated identity tracking. The clip-to-continuous crosswalk remains unresolved even if the continuous manifest names participants.

## Numerical checks completed

- Raw file sizes match `data/raw/manifest.json`: labeled pickle 5,094,311,994 bytes; archive 7,846,880,820 bytes; checkpoint 24,235,571 bytes.
- Total clip rows 36,930; negatives 28,663; positives 8,267 = 22.3856% (22.39% rounded).
- Training rows 32,179 including 7,210 positives; test rows 4,751 including 1,057 positives. Candidate first-token groups 289/40 with no overlap. First-two/three-token grouping totals 372/1,116; no claim these are confirmed participant/session/video identities.
- All four cells in each split/fps crosstab match CSV. FPS-only precision is exactly 1.0 and recall is 6,520/8,267 = 0.7886779 (78.87%); this is explicitly post-hoc descriptive and not compared as if it were the paper's frame metric.
- All-zero coordinates and all-zero confidence flags coincide in every row: 3,276 clips, of which 3,264 negatives and 12 positives; percentages 11.3875% and 0.1452% support printed rounding.
- Mean of clip zero-confidence fractions 0.4088782; mean below-0.2 fraction 0.4612534. The report correctly calls them clip-level means rather than all-frame weighted fractions.
- Duration minimum/median/IQR/maximum and positive/negative medians match JSON/CSV. Clip duration sum is 134.31723 hours, properly distinguished from unique camera or participant hours.
- Exactly 24,961 CSV rows have duration minus boundary difference equal to 2.0 seconds; the additional rounded groups 9,416 at 2.04 and 2,184 at 2.033 match the shortcut output. Padding interpretation remains labelled a hypothesis.
- There are 1,572 comma-separated label strings. `NoAction` and binary label 0 coincide in every row. Combined strings require atomization rather than treating every ordered string as a unique biological class.
- Two duplicate identifier strings have different coordinate hashes. There are 3,221 repeated coordinate-array hashes beyond first occurrences. Shared hashes across train/test total 43, all zero-coordinate arrays; nonzero cross-split coordinate hashes total zero.
- No declared frame-count mismatches; every listed coordinate dtype is float64. The source first-record values and shapes match the report.

## Paper and algorithm interpretation checks

- Original paper cohort hierarchy, selected ASD/SMM cohort, camera-hours interpretation and 220/21 subject split agree with the source. Release first-token counts remain explicitly unverified.
- Initial precision/recall 36.64%/87.72% versus selected-reannotation 66.82%/92.53% are correctly distinguished.
- The 200-frame, 30-frame-step, maximum-overlap aggregation explanation matches paper page 4. Half-open indexing in the tutorial is clearly a new formalization and appropriate for code.
- The heatmap formula is labelled illustrative, and source config verifies 17 channels, 48 sampled frames, score-weighted targets, cropping/resizing and left/right-aware flips. “3D” is correctly two spatial axes plus time, not physical-depth coordinates.
- Event count, rate, burden, calibration, subgroup and subject-bootstrap requirements are proposals rather than claims already tested. The dossier does not claim model training, historical reproduction or clinical inference.
- The paper's model comparison reused the held-out cohort for selecting the best architecture; the proposed extra validation/test separation is therefore well motivated, with proper distinction from the historical protocol.

## Suggested disposition

Apply findings 1–3 before final delivery. Apply mathematical clarification 4 and the brief count/shape clarifications if convenient. Wait for the archive agent's verified summary before replacing the placeholder or broadening completion claims. No integrated files were modified by this audit.

## Main-author resolution
All material findings were addressed: observable-and-scored frame set, low-confidence wording, nonzero-only duplicate-motion gate, undefined-feature cases, unique-ID distinction, and original-axis dimensions confirmed by a final complete clip audit. Continuous profiling now covers all 914 members. Final LaTeX build has no overfull-box or unresolved-reference warnings; all 27 pages were rendered and reviewed.
