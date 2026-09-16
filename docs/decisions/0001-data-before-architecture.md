# Decision 0001: establish release validity before model selection

Date: 2026-09-16. Status: accepted for initial study design.

The task prioritizes understanding data. Full-clip inspection found label-associated fps and missingness, undocumented timing conventions, and counts different from the publication. The continuous archive supplies explicit child IDs but has no verified crosswalk to the labeled-file identifiers.

Decision: retain all originals, report discrepancies, implement reproducible quality controls, and defer predictive-model claims until a valid grouping and evaluation contract is available. Perform metadata-only rules as post-hoc diagnostics, labeled as such. Propose confidence-aware SMM recognition and later burden estimation; do not turn this dataset into an ASD diagnostic benchmark.

Evidence:`data/processed/dataset_summary.json`,`released_split_audit.json`,`shortcut_audit.json`,`continuous_summary.json`; Barami2024Methods/Testing/Limitations; pinned source audit.

Revisit when release provenance, timing and subject mapping are verified. Record any alternative interpretation and the evidence that supports it.
