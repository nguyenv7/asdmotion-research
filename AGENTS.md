# Persistent research working instructions

Read README.md, docs/PROJECT_STATE.md, docs/OPEN_QUESTIONS.md and the most recent decision record before extending this workspace.

- Preserve raw downloads and upstream source. Save repairs in a separate fork or patch with provenance.
- Separate paper claims, current-release measurements, code behavior and proposed interpretations.
- Do not infer participant identity or timing units from the labeled filename convention without validation. The continuous archive's db.csv has explicit child IDs; its crosswalk to the labeled release is unresolved.
- SMM labels are not ASD diagnostic labels. Do not invent individual clinical metadata from aggregate paper statistics.
- Preserve missing-pose masks. Zero confidence does not establish absence of behavior.
- Record source hashes, split manifests, dependencies, random seeds, model selection and denominator definitions for experiments.
- Keep model training and a modern analysis environment separate. Run relevant semantic tests after code changes.
- Update PROJECT_STATE.md and the decision log when evidence or task status changes. Keep proposed work labeled as not run.
- Inspect rendered PDFs after report edits. Do not claim a completed model benchmark unless it actually ran.
