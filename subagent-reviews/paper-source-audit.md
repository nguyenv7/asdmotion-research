# Paper source audit

audit_mode: sequential-single-agent

## Overall assessment

The paper explainer and LaTeX fragment are grounded in the 12-page original article and both downloaded supplements. Original source inconsistencies are flagged rather than silently corrected. Main text uses paraphrase under the user's request for a summary; no long quotations were reproduced.

## Findings

- Bibliography and abstract: checked author names, title, venue/date/DOI against PDF pages 1 and 9–10. Abstract demographics are training-group values; report corrects the interpretation without claiming an author-issued correction.
- Introduction: verified SMM/ASD distinction and self-regulation discussion on page 2; no ASD-diagnosis claim added.
- Methods: verified cohort criteria, assessment hierarchy, child detector, skeleton tracking, clip counts, sliding windows, threshold and statistical methods on pages 3–5. Supplement pages 3–4 and 7–8 verify detector matching and 48-frame heatmap volume.
- Results: verified initial continuous frame precision/recall and all final intervals, 1,456-segment stratified sampling, two independent annotators, OR-positive adjudication, agreement and kappa. Explicitly distinguishes selected reannotation from whole-stream reannotation.
- Quantification: page 7 text says number per assessment; page 8 figure says rate per minute. Report says count/rate and identifies the plotted rate. Correlations use 24 assessments, with degrees of freedom 22.
- Limitations/discussion: verified page 9, including absence of raw video and absence of validated boundary accuracy.
- Supplement: eTable 3 reports precision, recall, epoch time despite expanded caption; models chosen on same test cohort are noted. Fine-tuned/pretrained terminology is normalized cautiously.
- Source inconsistencies: demographic percentages, clinical-score sample counts versus t degrees of freedom, positive-hours arithmetic and aggregation medians confirmed against original text. Main reference 43 is SSBD, not Kinetics; supplement provides Kinetics citation.
- Assets: standard extraction script returned zero images; unmodified full-page source rendering used instead. Stored supplemental PDFs are valid (9 and 1 pages); original article is 12 pages.

## Suggested edits

Applied before delivery: precise evaluation-population caveat, definition of every displayed-equation symbol, no pooled demographic claim using the abstract numbers, explicit designation of methodological inferences. Remaining task outside this source audit: reconcile article numbers with the downloaded dataset and code, which the parent task is performing.
