# Automated Analysis of Stereotypical Movements in Videos of Children With Autism Spectrum Disorder — Detailed Explainer

Tal Barami, Liora Manelis-Baram, Hadas Kaiser, Michal Ilan, Aviv Slobodkin, Ofri Hadashi, Dor Hadad, Danel Waissengreen, Tanya Nitzan, Idan Menashe, Analya Michaelovsky, Michal Begin, Ditza A. Zachor, Yair Sadaka, Judah Koler, Dikla Zagdon, Gal Meiri, Omri Azencot, Andrei Sharf, and Ilan Dinstein. JAMA Network Open, 2024;7(9):e2432851, published September 12, 2024. DOI: [10.1001/jamanetworkopen.2024.32851](https://doi.org/10.1001/jamanetworkopen.2024.32851). Principal institutions include Ben-Gurion University of the Negev, the Azrieli National Centre for Autism and Neurodevelopment Research, and collaborating Israeli clinical centres. [pp.1,9–10, Author Affiliations]

Metadata: product: Codex; execution_location: Local; capabilities_used: filesystem, Python/PyMuPDF, official literature repositories; audit_mode: sequential-single-agent. Source acquisition date: 2026-09-16. Main PDF: `references/papers/Barami2024_JAMA.pdf`; supplements: `Barami2024_supplement1.pdf` and `Barami2024_supplement2.pdf` in that directory. Full abstract/body quotation was deliberately replaced with a paraphrased explanation because the user requested a summary. Page numbers below refer to the printed PDF page, not a browser page.

Scope: this document explains the publication. The current downloaded release must not be assumed identical to the paper's experiments; the project's separate data audit has found differing record counts, mixed frame rates and missing-pose patterns. Keep publication claims and release measurements as separate evidence records until their versions are reconciled.

## Abstract — paraphrased

The paper develops an automated tool to find and quantify stereotypical motor movements (SMMs) in lengthy clinical videos of children already diagnosed with autism spectrum disorder (ASD). Its released dataset is called ASDPose; its algorithm is called ASDMotion. The cohort comprises 241 selected children, 319 assessments and 883 camera recordings totalling 580 camera-hours. The pipeline identifies the child's 2D skeleton, predicts SMM scores from motion sequences, and converts window scores into frame labels and episode summaries. The headline precision of 66.82% and recall of 92.53% belong to the reannotation analysis described below. They should be interpreted with that evaluation design attached. [pp.1,3–4,7,9]

The abstract's age and male count reproduce the training-group entries, although its sentence refers to the entire cohort. This report keeps training and test demographics separate instead of silently treating those entries as pooled cohort demographics. [p.1, Abstract; p.4, Table]

## Introduction

SMMs are repetitive movements such as hand flapping, rocking, jumping and spinning. They form part of restricted and repetitive behaviours, one ASD symptom domain. The paper explicitly states that SMMs are neither present in every person with ASD nor exclusive to ASD; it also describes their potential self-regulatory function. Consequently, detecting an SMM is a behavioural measurement task, and is not equivalent to making an ASD diagnosis or establishing that a movement should be reduced. [p.2, Introduction]

The scientific target is heterogeneous, relatively rare movements embedded in long recordings of naturally behaving children. This differs from classifying the type of an already selected short positive clip. Two key challenges motivate the architecture: multiple people are visible, so the child's identity must be selected; and different children perform different forms of stereotypy, so the detector must learn a broad positive category against diverse ordinary movements. [p.2, Introduction]

## Methods

### Participants

Children were recruited during 2017–2021 through ANCAN, which connects Ben-Gurion University with eight clinical sites. All had DSM-5 ASD diagnoses and an ADOS-2 assessment. Inclusion additionally required a score of at least 2 on item D2 or on the relevant D4/D5 stereotypical-behaviour item. Ages were 1.4–8.0 years. This is an ASD cohort selected for evidence of repetitive behaviour, rather than a diagnostic screening sample of ASD and non-ASD children. Ethics approvals and parental informed consent are reported. [p.3, Methods/Participants]

The training group had 220 children, with 172 males and 48 females, and mean age 3.97 years (SD 1.30). The test group had 21 children, with 15 males and 6 females, and mean age 4.32 (SD 1.39). Hebrew/Arabic primary-language counts were 192/28 in training and 15/6 in testing. ADOS-2 total, social-affect and restricted/repetitive-behaviour calibrated severity scores were described; cognitive and language scores were available for subsets. Those clinical measurements are descriptive characterisation, not the binary recognition target. [p.4, Table]

![Original demographic table on source page 4](../images-from-papers/Barami2024_JAMA-page4.png)

Original source page, preserved without reconstructing its table. Note the source inconsistencies listed at the end of this explainer. [p.4, Table]

### Behavioral Assessment Recordings and Computing Hardware

The hierarchy is 241 children → 319 assessments → 883 camera recordings → 580 hours of footage. Each child contributed one or two assessments; each assessment was recorded by two to four cameras. The assessment types were 226 ADOS-2, 71 PLS-4 language assessments, and 22 developmental/cognitive assessments, equally divided between Mullen and WPPSI-III. Cameras recorded 1080 × 1920 images at 30 frames/s. The reported development machine had two RTX3090 GPUs, a 32-core Threadripper PRO 3975WX CPU and 264 GB RAM. [p.3, Behavioral Assessment Recordings and Computing Hardware]

Interpretive clarification: camera footage duration is not independent child-observation duration when different cameras record the same assessment. Likewise, camera views and derived clips are nested observations, not additional independent children. This follows from the reported acquisition hierarchy. [p.3]

### Pose Estimation and Skeleton Tracking

OpenPose extracts 17 joint positions in 2D for every detected person per frame. A pretrained spatial-temporal affinity-field tracker maintains skeleton identities over time, without additional tracking training on this cohort. The resulting skeletal representation preserves body geometry and movement while discarding the RGB appearance supplied to the original pose estimator. [p.3, Pose Estimation and Skeleton Tracking]

### Manual Annotation of SMMs and the Child's Skeleton

Undergraduate annotators were trained by a clinician with over 15 years' experience. They reviewed all 580 hours, marked event start/end, movement category and the child's skeleton identity. The annotation interface also marks camera views in which the child is visible. There were 7,352 annotated positive segments, described as covering 21.14 hours, approximately 3.5% of footage; the reported mean segment length was 9.89 seconds (SD 9.56). [p.3, Manual Annotation; Supplement 1 p.2, eFigure 1]

The 13 annotated categories were clapping, hand flapping, finger flicking, tapping, spinning, pacing, jumping, toe walking, body rocking, tremor-like movements, playing with an object, head movement and other. All were pooled into a single SMM class for the model. Some labels therefore depend on fine finger movement or object-use context that a coarse body skeleton may not fully retain; this latter representation concern is a methodological inference, not a tested result of this paper. [Supplement 1 pp.5–6, eFigure 4/eTable 1]

### Child Detection

A COCO-pretrained YOLOv5 was trained to distinguish children from adults using 30,000 frames sampled from annotated positive segments. The child was manually identified in those data. The paper reports an 80/20 training/test division for this detector and 95% precision with 92% recall for child bounding boxes. It does not establish in the main text that this detector's split was child-disjoint. [pp.3–4, Child Detection]

At application time, YOLO boxes and skeleton boxes are matched by intersection-over-union; labels are transferred to skeletons. Unmatched YOLO boxes are discarded, and an unmatched skeleton is labelled adult. All subsequent recognition uses the selected child skeleton. This means identity selection precedes and constrains the motion classifier. [Supplement 1 p.3, eFigure 2]

### SMM Identification Algorithm

The authors sampled 28,648 negative segments, matching the distribution of positive segment lengths. The training split had 6,597 positives and 24,923 negatives from 220 children/295 assessments. The remaining 21 children/24 assessments formed the test set, including 755 positive segments. The paper does not describe a separate independent validation cohort in these methods. [p.4, SMM Identification Algorithm]

ASDMotion uses PoseConv3D pretrained on Kinetics-400. A training sample spans 200 source frames (about 6.7 seconds). The model receives a volume of 48 2D joint heatmaps; heat values reflect OpenPose joint confidence, and 3D convolutions learn patterns across space and time. Here “3D” refers to two image axes plus time, not measured 3D anatomical coordinates. Training used batch size 64, stochastic gradient descent and 100 epochs, with 83.49 minutes per epoch reported for the selected model. The exact frame-sampling and augmentation implementation must be checked in the released configuration. [p.4; Supplement 1 pp.7–8]

The supplement compares the chosen pretrained model with PoseC3D without this pretraining, ST-GCN and 2S-AGCN. ST-GCN represents joints and their spatial/temporal relations as a graph. 2S-AGCN combines separate joint and bone streams. The chosen model had the largest reported precision and recall, at higher training cost. This is evidence for this experimental configuration, not proof that heatmap networks universally outperform graph networks. The supplement explicitly states the same test set was used in comparing and selecting the models. [Supplement 1 pp.7–8, eTable 3]

![Original comparison and architectural description](../images-from-papers/Barami2024_supplement1-page8.png)

Original eTable 3 is preserved rather than retyped. Its numeric columns are precision, recall and epoch time, even though the table caption additionally mentions accuracy and mean-class accuracy. [Supplement 1 p.8]

### Testing the Algorithm

The complete test recordings were scanned with 200-frame windows and a 30-frame step, giving 170-frame overlap. Each window receives an SMM score. Each frame inherits the maximum score from every window covering it. A threshold of 0.85 turns frame scores into binary labels; consecutive positive frames are joined into episodes. The authors call the threshold arbitrary and examine thresholds from 0.5 to 0.9. [p.4, Testing; p.5, Initial Accuracy]

For an explicit pedagogical formalisation, let $t$ denote a frame, $W_k$ the set of frames in window $k$, $s_k$ the model score of that window, $q_t$ the merged frame score, $\tau$ the chosen threshold, and $\widehat y_t$ the predicted binary frame label. Let $\mathbf 1[\cdot]$ be 1 when its condition holds and 0 otherwise. The paper's procedure can be expressed as:

$$q_t=\max_{k:t\in W_k}s_k,\qquad \widehat y_t=\mathbf 1[q_t\ge\tau],\qquad\tau=0.85.$$

These are explanatory equations derived from the verbal procedure, not equations printed in the paper. Handling of frames with no valid covering window, missing child poses, or video-end padding must be checked in code rather than inferred from this formula. [p.4; Supplement 1 p.4, eFigure 3]

Precision means the fraction of predicted positive frames that are annotated positive; recall means the fraction of annotated positive frames predicted positive. Denote true-positive, false-positive, false-negative and true-negative frame counts by $TP,FP,FN,TN$, respectively. For a specified evaluation population:

$$\operatorname{precision}=\frac{TP}{TP+FP},\quad\operatorname{recall}=\frac{TP}{TP+FN},\quad\operatorname{specificity}=\frac{TN}{TN+FP},\quad\operatorname{NPV}=\frac{TN}{TN+FN}.$$

These definitions explain the reported metric terminology. The paper begins with frame-level evaluation and later evaluates selected reannotated segments; these are different evaluation populations. The exact aggregation/weighting and effective denominators of the reported reannotation summaries cannot be reconstructed from the published percentages alone. [pp.5,7, Testing/Results; p.7, Figure 2 caption]

### Statistical Analysis

The authors use Mann–Whitney tests for sex comparisons in precision/recall, independent-sample t tests for age and clinical-score comparisons, Pearson/Spearman/concordance correlations for agreement between model and annotation summaries, and Cohen's kappa plus percent agreement for annotator reliability. Precision/recall intervals are described as based on standard error of the mean; Pearson intervals use 1,000 bootstrap resamples. The paper does not provide enough detail here to recover all interval calculations or clustering choices exactly. [p.5, Statistical Analysis]

## Results

### Initial Accuracy of the Algorithm

On the initial annotation of the held-out 24 assessments/21 children, frame-level precision was 36.64% (95% CI 29.97%–49.99%) and recall 87.72% (84.22%–94.22%) at threshold 0.85. High recall coexisted with many apparent false positives. Male/female analyses involved only 15 and 6 children, respectively; absence of a significant difference is the reported finding, not a demonstration of demographic equivalence. [p.5, Initial Accuracy]

### Reannotation and Interrater Reliability of the Test Data

The authors selected 1,456 short segments with equal counts from the original true-positive, false-positive, true-negative and false-negative strata. Two independent annotators were blinded to original human and model labels. They agreed on 90% of segment labels, with Cohen's $\kappa=0.76$. A segment was then treated as positive if either annotator labelled it positive. Of the original apparent false-positive segments, 51% were judged true positive on reinspection; 9.8% of original false negatives were judged true negative. [pp.5–7, Reannotation]

On this reannotation analysis, precision was 66.82% (95% CI 55.28%–72.05%) and recall 92.53% (81.09%–95.10%). Specificity was 95.45% (94.31%–96.91%) and negative predictive value 99% (99%–100%). These percentages must not be described as event-level detection probability or ordinary classification accuracy. Nor should they be presented as an independently and exhaustively reannotated evaluation of every frame in all continuous test videos: the methods describe selected segments. [p.7, Results; p.7, Figure 2]

![Original accuracy figure and surrounding evaluation description](../images-from-papers/Barami2024_JAMA-page7.png)

### Accuracy of SMM Quantification per Assessment and Child

Against reannotated data, the number/rate measure had Pearson $r=0.80$, Spearman $\rho=0.80$ and concordance correlation coefficient 0.70. Proportion of assessment time with SMMs had Pearson $r=0.88$, Spearman $\rho=0.87$ and concordance 0.73; reported P values were below .001. Pearson intervals were 0.67–0.93 and 0.74–0.96, respectively. Figure 3 presents SMMs per minute and percentage of time per assessment, with 24 assessment observations (correlation degrees of freedom 22). It does not provide 241 independent outcome comparisons. [p.7, Quantification; p.8, Figure 3]

## Discussion

The authors interpret the reannotation result as evidence that people miss rare movements when screening long videos and that automation can assist behavioural quantification. Their goal is broad SMM detection rather than a fixed taxonomy of movement classes. They distinguish ASDPose's clinically characterised cohort and long recordings from smaller collections of preselected Internet videos. [pp.7–9, Discussion]

### Previous SMM-Related Datasets and ASDPose

The paper states that ASDPose releases skeleton data, demographic/clinical information, positive annotations and split information; raw videos are excluded for privacy. Supplement 2 identifies the GitHub repository as the access point, says deidentified participant data and analytical code are available, and states availability for everyone and any purpose. Actual files available at the pinned repository/release must still be inventoried separately; a publication's data-availability statement does not itself prove a particular download is complete. [p.9; Supplement 2 p.1]

### Limitations

The authors identify substantial computation/storage needs and privacy constraints, uncertain generalisation beyond young ASD children in clinical assessments, limited female representation, lack of movement-subtype classification, untested onset/offset accuracy, and the need to develop intensity/severity measures beyond the present summaries. These are stated limitations, rather than established failures on unseen populations. [p.9, Limitations]

## Conclusions

The contribution is a practical skeleton-based SMM measurement pipeline and a larger clinically characterised motion dataset. The paper proposes future use in studying developmental trajectories and neural/physiological mechanisms, but the present study does not validate those downstream mechanisms or an ASD diagnostic model. [p.9, Conclusions]

## Source inconsistencies and methodological reading notes

The following separates direct observations about the source from research implications inferred during this analysis.

1. Demographics: the abstract and Results opening report 172 males and mean age 3.97 as though describing 241 children, but the table assigns these to the 220-child training group. The table counts imply 187 males in the full cohort (172 + 15); this is our arithmetic, not a corrected value supplied by the authors. The training female percentage printed as 22.82% is inconsistent with 48/220 (21.82%). Use counts and split-specific ages until participant metadata resolves this. [pp.1,4–5]
2. Clinical-score missingness: the table lists cognitive data for 183 + 16 participants but a t-test degrees of freedom of 214; PLS data for 148 + 9 but degrees of freedom 174. Those do not match ordinary two-group tests on exactly those listed counts. Do not reconstruct sample sizes from those test statistics. [p.4, Table]
3. Event duration: 7,352 × 9.89 seconds is approximately 20.20 hours, whereas the text states 21.14 hours. Rounding of a two-decimal mean alone does not explain the difference; counting/view conventions or a reporting error remain unresolved. [p.3, Manual Annotation; calculation by this analysis]
4. Aggregation: main-text median rate/time proportion are 0.12 events/min and 1.55%, whereas Supplement 1 eTable 2 reports 0.1 and 1.4%. Main text describes assessment summaries and the supplement describes video summaries, which may explain the difference, but the source does not explicitly reconcile it. Keep the denominators separate. [p.5; Supplement 1 p.7]
5. Reannotation sampling: balancing original error strata intentionally changes the composition of reviewed segments. The exact weighting needed to recover deployment-population predictive values is not documented in the main methods. The final precision and NPV therefore require that sampling context; a random or exhaustive independently reviewed subset would answer a different validation question. This is an evaluation-design inference. [pp.5–7]
6. Model selection: the same held-out children were used for the four-model comparison that motivated architecture choice. Future work should reserve an additional untouched test cohort and make threshold/model choices within training/validation data. This recommendation follows from the stated selection protocol; the paper does not report the proposed redesign. [Supplement 1 p.8]
7. Confidence intervals and chance language: the printed precision intervals are asymmetric around the stated point values despite the brief standard-error description. Also, expected chance recall depends on the positive prediction rate, not solely on how rare SMMs are. The source's blanket chance-level wording should not replace an explicit null model. These are reporting/methodology cautions, not a reanalysis of participant-level results. [p.5, Testing/Statistical Analysis]

## Audit and source assets

audit_mode: sequential-single-agent. Completed checks: bibliography/abstract, introduction, cohort and hierarchy, all method subsections, both evaluation populations, assessment correlations, discussion/limitations, numerical source discrepancies, and source-list/download verification. Audit record: `subagent-reviews/paper-source-audit.md`. The bundled figure extractor returned zero images; fallback `scripts/extract_paper_assets.py` renders unmodified source pages with figures/tables, avoiding reconstruction. The manifest records source/page locations.

## Source list

[Barami et al., 2024/09] Barami T, Manelis-Baram L, Kaiser H, et al. “Automated Analysis of Stereotypical Movements in Videos of Children With Autism Spectrum Disorder.” JAMA Network Open. [DOI](https://doi.org/10.1001/jamanetworkopen.2024.32851); [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11393723/). Main analysis uses the locally downloaded original PDF.

[Barami Supplement 1, 2024/09] Supplemental Online Content, eFigures 1–4, eTables 1–3 and eReferences. [Publisher-deposited PDF](https://pmc.ncbi.nlm.nih.gov/articles/instance/11393723/bin/jamanetwopen-e2432851-s001.pdf). Retrieved through the [Europe PMC supplementary archive](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11393723/supplementaryFiles) after direct PMC PDF URLs returned HTML browser challenges.

[Barami Supplement 2, 2024/09] Data Sharing Statement. [Publisher-deposited PDF](https://pmc.ncbi.nlm.nih.gov/articles/instance/11393723/bin/jamanetwopen-e2432851-s002.pdf). Retrieved in the same verified Europe PMC archive.
