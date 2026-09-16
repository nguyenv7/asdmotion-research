# Survey of ASD motion research and ASDPose reuse

Date: 2026-09-16  
Scope: ASDMotion/ASDPose reuse, and selected 2024–2026 primary studies examining stereotypy, motor control, social interaction, and measurement reliability. This is a focused scoping search, not a systematic review.  
Product: Codex; execution_location: Local; capabilities_used: web search, publisher/author sources, local PDF downloads; audit_mode: parallel-subagents at project level, sequential-single-agent for this literature subtask.  
Evidence rule: a citation to Barami et al. is not evidence that a study trained or evaluated on ASDPose. Proposed experiments below are our research suggestions, not published ASDPose results.

## Table of Contents

1. [Dataset reuse audit](#1-dataset-reuse-audit)
2. [Primary studies by perspective](#2-primary-studies-by-perspective)
3. [Data and method comparison](#3-data-and-method-comparison)
4. [Research directions proposed for this project](#4-research-directions-proposed-for-this-project)
5. [Search log and investigation limits](#5-search-log-and-investigation-limits)
6. [Source register](#6-source-register)

## 1. Dataset reuse audit

**No independent reuse of the released ASDPose data was verified in this search.** This is a search outcome, not proof that no reuse exists. Exact-name searches mostly returned the repository, original article, supplements, and author pages. Broad citing-paper searches found relevant successors, but their described datasets differed. Search strings and limitations are retained in Section 5.

The original release addresses SMM detection and quantification within an autistic cohort. Its skeleton-only sharing policy excludes raw video. [JAMA Network Open (2024/09), dataset discussion](https://doi.org/10.1001/jamanetworkopen.2024.32851).

```text
ASDPose does not include the raw video.
```
[JAMA Network Open (2024/09), Previous SMM-Related Datasets and ASDPose](https://doi.org/10.1001/jamanetworkopen.2024.32851)

| Candidate | Relationship verified in the inspected source | Reuse decision |
|---|---|---|
| Barami et al. 2024 | Original dataset and algorithm publication | Original use, not an independent replication |
| MBaye et al. 2025/2026 | Separate Groden Center pose/accelerometer cohort | Different data |
| Lemler et al. 2025 | Frankfurt intervention trial observations | Different data |
| Freud et al. 2025 | Cites Barami; separately collected grasping trajectories | Citation, not ASDPose reuse |
| Amraee et al. 2026 | Cites Barami; autism-center functional-behavior recordings | Citation, not ASDPose reuse |
| Stenum et al. 2026 | Cites Barami; separate toddler bubble-play recordings | Citation, not ASDPose reuse |
| Manelis-Baram et al. 2025 | Related research group; facial video analysis with controls | No verified use of the released ASDPose files; possible source-cohort overlap was not established |

Evidence for these decisions is the Methods/data descriptions linked in Section 2. Do not merge these cohorts merely because they share investigators, diagnostic instruments, or clinical settings.

## 2. Primary studies by perspective

### Original reference: detecting heterogeneous SMM

**Barami et al. establishes the starting task: find movement episodes, then measure their burden.** ASDPose contains 319 assessments from 241 autistic children, with 7,352 annotated SMM segments; ASDMotion uses pretrained PoseC3D. [JAMA Network Open (2024/09), Methods and dataset discussion](https://doi.org/10.1001/jamanetworkopen.2024.32851).

Authors: Tal Barami, Liora Manelis-Baram, Hadas Kaiser and colleagues; Ben-Gurion University/Azrieli autism research consortium. Venue/date: JAMA Network Open 7(9), e2432851, 2024-09-12. Citation count: not independently verified. Detailed pipeline and cohort analysis belong in the companion data report.

### Periodicity: interpretable recurrence instead of only learned appearance

**MBaye et al. extracts periodicity features from pose trajectories and accelerometers, then uses simple classifiers.** The detailed 2025 preprint analyzes six participants aged 12–20, with 4–6 fps videos, higher-rate accelerometry, four-second windows, and subject-held-out evaluation. The accepted, peer-reviewed article appeared on 2026-07-24; its publisher page currently labels it an early accepted version. Detailed methodological statements here are attributed to the preprint rather than assumed unchanged. [Scientific Reports (2026/07), abstract/version notice](https://doi.org/10.1038/s41598-026-60095-8); [bioRxiv (2025/09), Methods/Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424721/).

```text
low-dimensional, interpretable feature vectors
```
[Scientific Reports (2026/07), abstract](https://doi.org/10.1038/s41598-026-60095-8)

Authors: Austin A. MBaye, Jose A. Perea, Christopher J. Tralie, Matthew S. Goodwin; Northeastern University and Ursinus College. Citation count: unavailable. Limitation for interpretation: six participants and low video sampling rate in the preprint; strong rhythmicity is the targeted representation.

### Multi-label behavior: concurrent movement types and honest generalization

**Lemler et al. tests simultaneous flapping and jumping labels on unseen children.** OpenPose and an LSTM analyze 15-frame sequences from 52 autistic preschoolers in 12-minute BOSCC free-play videos. Nested subject-wise validation gives macro accuracy 0.702 but macro F1 0.318. The distinction between accuracy and minority-event recovery is material. [Autism Research (2025/03), Methods and Table 7](https://onlinelibrary.wiley.com/doi/10.1002/aur.70020).

```text
ensuring no subject was split between folds
```
[Autism Research (2025/03), Nested Cross-Validation](https://onlinelibrary.wiley.com/doi/10.1002/aur.70020)

Authors: Christian Lemler, Solvejg K. Kleber, Leonie Polzer, Naisan Raji, Janina Kitzerow-Cleven, Ziyon Kim, Simeon Platte, Christine M. Freitag, Nico Bast; Goethe-University/University Hospital Frankfurt. Online: 2025-03-14; issue 18(4):833–844. Citation count: unavailable.

### Multimodal action classes: RGB, flow, and body structure

**Zhang et al. studies recognition of six movement classes using complementary visual and skeletal information.** APMFNet combines visual-motion learning, skeleton-relation mining, and cross-modality attention on ACSA653 (653 videos). [IEEE JBHI (2025/03), abstract](https://pubmed.ncbi.nlm.nih.gov/40030496/).

```text
653 videos across six classes
```
[IEEE JBHI (2025/03), abstract](https://pubmed.ncbi.nlm.nih.gov/40030496/)

Authors: Baiqiao Zhang, Yanran Yuan, Wei Qin, Xiangxian Li, Weiying Liu, Wenxin Yao, Yulong Bian, Juan Liu; Shandong University and Jining No.1 People's Hospital, as identified in the [author manuscript](https://baiqiaozhang.cc/assets/files/JBHI_revision.pdf). Venue: IEEE JBHI 29(3):2020–2033; DOI carries 2024, journal issue March 2025. Citation count: unavailable. Do not compare clip-class accuracy directly with long-recording event detection; the author manuscript is retained for further protocol audit.

### Social interaction: dyadic synchrony and clinical comparison groups

**Koehler et al. examines movement between patient and clinician, rather than only within one body.** A motion-energy synchrony SVM distinguished 56 autistic participants from 38 clinical controls with balanced accuracy 63.4%. The authors explicitly discuss possible clinician-behavior/context effects and lack of significant clinical-rating associations. [Scientific Reports (2024/03), Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC10920641/).

```text
the clinician’s total amount of body movement
```
[Scientific Reports (2024/03), Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC10920641/)

Authors: Jana C. Koehler, Mark S. Dong, Da-Young Song, Gaeun Bong, Nikolaos Koutsouleris, Hee-Jeong Yoo, Christine M. Falter-Wagner; LMU Munich/LMU University Hospital and Seoul National University collaborators. Venue/date: Scientific Reports 14:5663, 2024-03-07. Citation count: unavailable.

### Mechanistic motor function: synchronized EEG and 3D motion

**Paulo et al. releases Move4AS to study motor imitation and its neural correlates.** The dataset contains 14 clinical and 20 control participants, dancing/walking tasks, up to 16-channel EEG, marker-based 3D motion, and clinical characterization. Technical validation includes motion normalization and a CSP–LDA classification baseline. [Scientific Data (2025/06), Abstract and Technical Validation](https://www.nature.com/articles/s41597-025-05313-0).

```text
motor imitation tasks - dancing and walking
```
[Scientific Data (2025/06), abstract](https://www.nature.com/articles/s41597-025-05313-0.pdf)

Authors: João Ruivo Paulo, Teresa Sousa, João Perdiz, Lara Pereira, Mariette Vasen, Susana Mouga, Gabriel Pires, Miguel Castelo-Branco; University of Coimbra, NOVA Lisbon, Jena/KIT, and Polytechnic Institute of Tomar. Venue/date: Scientific Data 12:959, 2025-06-07. Citation count: not independently refreshed. This is a separate experimental multimodal dataset, not an ASDPose extension.

### Fine motor control: grasping kinematics

**Freud et al. studies purposeful movement with two finger markers.** In 59 young adults, subject-wise cross-validation of grasping features exceeded 84% accuracy; the authors report subject-level AUC above 0.95 and trial-level AUC above 0.85. Their sample was restricted to young adults with normal-range IQ, which limits generalization. [Autism Research (2025/05), Results/Limitations](https://pmc.ncbi.nlm.nih.gov/articles/PMC12166512/).

```text
two markers placed on the thumb and index finger
```
[Autism Research (2025/05), abstract](https://pubmed.ncbi.nlm.nih.gov/40323705/)

Authors: Erez Freud, Zoha Ahmad, Eitan Shelef, Bat Sheva Hadad; York University, University of Pittsburgh, University of Haifa. Online: 2025-05-05; Autism Research 18(6):1170–1181. Citation count: unavailable. Their citation of Barami concerns related work; their experiment is not ASDPose reuse.

### Measurement reliability: facial expression quantity versus timing

**Manelis-Baram et al. finds that tool choice changes facial-expression measurements without producing a group difference in total expression quantity.** They compare iMotions, FaceReader, and Py-Feat on 100 verbal children, including 72 autistic children and 28 controls, during ADOS-2 assessments. The authors identify quality, timing, and context as aspects their quantity analysis does not resolve. [Molecular Autism (2025/10), abstract](https://pmc.ncbi.nlm.nih.gov/articles/PMC12512823/).

```text
quality, timing, or social context
```
[Molecular Autism (2025/10), Limitations](https://pmc.ncbi.nlm.nih.gov/articles/PMC12512823/)

Authors: Liora Manelis-Baram, Tal Barami, Michal Ilan, Gal Meiri, Idan Menashe, Elizabeth Soskin, Carmel Sofer, Ilan Dinstein; Ben-Gurion University/Azrieli center collaborators. Venue/date: Molecular Autism 16:50, 2025-10-09. Citation count: unavailable. Same research group does not establish identical participants or reuse of released skeleton files.

### Event kinematics: amplitude versus frequency and averaging

**Stenum et al. distinguishes movement quality from occurrence.** AlphaPose analyses of 81 segments from 28 toddlers (14 per group) found an amplitude difference at event level, but not after event averaging; frequency did not differ. [Developmental Science (2026/03), abstract](https://pubmed.ncbi.nlm.nih.gov/41885203/).

```text
A data use agreement will be required.
```
[Developmental Science (2026/03), Data Availability](https://onlinelibrary.wiley.com/doi/10.1111/desc.70176)

Authors: Jan Stenum, Elizabeth Eiler, Ryan T. Roemmich, Rebecca Landa, Rachel Reetzke; Johns Hopkins/Kennedy Krieger. First online: 2026-03-26; May issue 29(3):e70176. Data require author request and agreement. Barami is cited; this is a separate cohort. Citation count: unavailable. Evidence inspected: publisher abstract, metadata, references, and availability statement; full PDF not obtained. [Publisher record](https://onlinelibrary.wiley.com/doi/10.1111/desc.70176).

### Semantic context: zero-shot vision-language classification

**Amraee et al. uses contextual visual descriptions for high-impact behaviors.** The CVPR 2026 workshop paper evaluates 40 separate autism-center clips (10–15 seconds): non-aggressive behavior, self-injury, aggression toward others, and property destruction. CLIP/KMeans selects keyframes; Qwen3-VL descriptions feed prompted LLM classifiers. [CVPR Workshops (2026/06), Sections 3–4](https://openaccess.thecvf.com/content/CVPR2026W/CV4Smalls/papers/Amraee_Toward_Automated_Behavior_Understanding_in_Autism_A_Zero-Shot_Vision-Language_Model_CVPRW_2026_paper.pdf).

```text
a total dataset size of 40 video clips
```
[CVPR Workshops (2026/06), Section 3.4](https://openaccess.thecvf.com/content/CVPR2026W/CV4Smalls/papers/Amraee_Toward_Automated_Behavior_Understanding_in_Autism_A_Zero-Shot_Vision-Language_Model_CVPRW_2026_paper.pdf)

Authors: Somaieh Amraee, Ashutosh Singh, Aston McCullough, Mindy Scheithauer, Matthew Goodwin, Sarah Ostadabbas; Northeastern and Emory Universities. Citation count: unavailable. This small curated evaluation does not establish long-recording detection or clinical deployment; Barami appears in related work, not as its evaluation dataset.

## 3. Data and method comparison

Facts in the first four columns refer to the corresponding primary-study entry above. The final column contains **our assessment of applicability**, not a reported transfer result.

| Study | View of the data | Prediction/measurement target | Algorithm family | ASDPose feasibility assessment |
|---|---|---|---|---|
| Barami | Long 2D pose streams | SMM episodes and burden | Pose heatmaps + 3D CNN | Direct baseline |
| MBaye | Recurring landmark/sensor trajectories | Repetition strength; SMM | Persistent homology + simple classifier | Promising if confidence/missingness is modeled |
| Lemler | Simultaneous body actions | Multiple behavior labels | LSTM | Requires valid subtype labels, not only binary SMM |
| Zhang | Appearance, motion, skeletal relations | Six action classes | RGB/flow/skeleton fusion | Only the skeletal branch is available locally |
| Koehler | Interpersonal timing | ASD versus clinical controls | Motion energy + SVM | Needs reliable persistent adult/child tracks and controls |
| Paulo | Neural–motor coupling | Imitation/motor function | EEG and 3D motion analysis | New modality/data required |
| Freud | Goal-directed finger motion | Group classification | Kinematic feature classifiers | Body joints cannot substitute for finger markers |
| Manelis-Baram | Facial expression timing/quantity | Measurement agreement/group contrasts | Facial analysis tools | RGB/facial detail required |
| Stenum | Within-event kinematics | Amplitude/frequency group comparisons | AlphaPose + statistical analysis | Test trajectory detail and aggregation explicitly |
| Amraee | Person–object–social context | Semantic behavior categories | VLM + LLM | Raw visual context unavailable in skeleton release |

## 4. Research directions proposed for this project

The following is our experimental design advice. None of the expected outcomes is claimed as established by the papers.

**Recommended first direction: reliable measurement of SMM burden under pose uncertainty.** A defensible study would ask: *How much of the apparent movement signal and its relationship to clinical variables survives missingness, tracking errors, subject-held-out evaluation, and threshold calibration?* This makes the downloaded data audit the first experiment, rather than treating a large neural network as the starting point.

**Current feasibility gate:** the inspected training release contains 36,930 clips, and the local EDA explicitly describes a clip-only population. It does not by itself establish full-recording burden, event prevalence, or a clinically usable continuous-time denominator. The schema contains `start_frame`/`end_frame`, but their interpretation must be reconciled with sequence lengths and source recordings before temporal reconstruction. See the local [dataset summary](../data/processed/dataset_summary.json), [schema](../data/processed/dataset_structure.json), and [EDA caveats](../data/processed/eda_notes.json). Full-session burden remains conditional on acquiring and validating the pending continuous archive, complete interval labels, timing units, and child/session mapping. Until then, the directly feasible research stage is **clip-level measurement reliability and representation analysis**; avoid labeling clip accuracy as burden validation.

| Phase | Question | Minimum experiment | Decision/evidence to preserve |
|---|---|---|---|
| 0: identify units | What is independent: frame, window, session, child? | Validate boundary units and mappings; obtain continuous recordings/labels for burden; freeze subject-disjoint manifests | No child/session crosses training, tuning, or final test; no burden claim from selected clips |
| 1: observability | Which joints and time intervals are measurable? | Joint confidence, missing runs, track jumps, view/scale summaries | Retain valid-time masks; never count invisible time as confirmed absence |
| 2: descriptive motion | Is recurrence distinguishable from amount of motion? | Compare energy, autocorrelation, spectral concentration, and recurrence features | Measure behavior-specific failure cases and confidence dependence |
| 3: baseline reproduction | What does the original detector achieve with the available release? | Fixed split, original label rule/windowing; document deviations | Segment/event precision–recall, duration error, errors per hour |
| 4: robust improvement | Does explicit uncertainty improve unseen-child performance? | Baseline versus confidence masking, confidence-aware features, multi-scale temporal aggregation | Child-bootstrap intervals, calibration, abstention coverage, compute cost |
| 5: phenotype | Are reliable motion summaries associated with available clinical scores? | Child/session-level models with prespecified age/sex and repeated-measure handling | Effect sizes and uncertainty; exploratory associations, no causal claims |
| 6: external validity | Does the method survive a new sensor/cohort/context? | Harmonize a separate corpus and freeze its evaluation protocol | Explicit joint mapping, sample-rate/label differences, external degradation |

**A compact, interpretable comparison is a useful first paper candidate.** Compare energy-only logistic regression, temporal periodicity features with a small classifier, and PoseC3D, using the same children, annotations, and evaluation rules. Add topological features only if they improve over ordinary autocorrelation/spectral baselines. Define the contribution around robustness or interpretable error mechanisms rather than presumed novelty of an algorithm family.

**The highest-risk shortcut is diagnostic classification using an autistic-only corpus.** Before proposing ASD-versus-non-ASD prediction, require a separately consented and clinically characterized comparison group and a protocol matched for recording context. SMM recognition labels and diagnostic labels answer different questions. Similarly, predicting a total clinical score from a component behavior requires checking whether the target assessment already includes that behavior; otherwise apparent validation may partly be circular.

**Move toward subtype and temporal-context work only after checking labels.** The local release does contain action names and comma-separated combinations, including hand flapping, jumping, and fingers; these are candidate subtype targets, but their ontology, concurrency meaning, and reliability require audit before multi-label training. A finger-related label does not add finger coordinates to the observed 17-joint body representation. [Local dataset summary](../data/processed/dataset_summary.json); [schema](../data/processed/dataset_structure.json). If repeated sessions exist but intervention/exposure data do not, changes over time can be described but should not be called treatment effects. Social synchrony is a later direction contingent on identifiable and consistently tracked partners; facial, object-context, and EEG questions need different data.

**Proposed Stenum-inspired test:** retain event-level motion distributions rather than only averaging all activity per child. Compare wrist/body amplitude and recurrence conditional on joint confidence and subtype labels; treat body-skeleton wrist motion as a proxy, not as validated fine-hand kinematics. Account for clustering within child/session. This is our proposed transfer experiment, not a published ASDPose result.

**Hard negative review should drive model choice.** Predefine candidate errors: periodic ordinary play, rocking-like camera/track motion, weak or aperiodic SMM, occluded wrists, overlapping people, short bouts, and starts/ends between inference windows. Test which are observable from skeletons alone. Persist both quantitative strata and representative deidentified trajectory plots. An unresolvable semantic distinction should be documented as a representation limit, not hidden with aggregate accuracy.

## 5. Search log and investigation limits

Search date: 2026-09-16. Searches were conducted through web search with verification in publisher, PMC/PubMed, conference, author, and repository sources. English titles and dataset names were the useful discovery terms. No contact with authors was made.

| Search family | Representative exact query | Outcome |
|---|---|---|
| Exact dataset | `"ASDMotion"`; `"ASDPose"` | Original repo/article/supplements; no independent reuse verified |
| Dated reuse | `"ASDMotion" "2025"`; `"ASDMotion" "2026"`; `"ASDPose" 2025 2026` | No verified independent training/evaluation |
| Citation neighborhood | `"Automated Analysis of Stereotypical" "2026"`; `"Barami" "autism" "2025"` | Facial comparison and VLM/kinematics related work |
| Alternative representations | `autism motor stereotypy skeleton 2025 dataset deep learning synchrony 2024` | Multi-label, multimodal, synchrony, and topology studies |
| Version verification | `"Automated quantification of stereotypical motor movements in autism using persistent homology" "2026" nature` | Verified July 2026 accepted peer-reviewed publication |
| Context and measurement | Exact facial-expression, Move4AS, and grasping titles | Primary full texts/abstracts and author PDFs |
| Toddler event kinematics | `"Quantifying Repetitive Hand Flapping Kinematics"`; DOI `10.1111/desc.70176` | Publisher verified first-online date, citation to Barami, and request/DUA data access |

Completed checks: dataset identity separated from citations; preprint and accepted-paper versions separated; primary URLs retained; authors/affiliations/venues/dates recorded; measurements not compared across incompatible tasks; our proposals separated from results; exact snippets kept under 25 words per source; headings checked against content; PDF signature and SHA-256 checks on downloads.

Limitations: this is not an exhaustive forward-citation database export, systematic review, or complete 2026 census. Search indexing can miss reuse that does not name the release. Citation counts were not reliably refreshed and are marked unavailable rather than inferred from accesses or reference-list length. Authors' institutional affiliations describe the paper context and may differ from current employment. Some publisher endpoints returned access challenges; four public PDFs downloaded successfully on the first authorized network attempt, while failures and URLs are saved in `references/papers/literature_downloads.json`. Only the official abstract and version notice of the 2026 topology article were inspected; detailed methodology comes from its clearly labeled 2025 preprint. Full-text assessments rely partly on search-indexed primary-source text when direct page opening failed. Raw clinical videos were not downloaded. For external reuse, verify each dataset's own access and consent conditions.

## 6. Source register

[JAMA Network Open, 2024/09] Barami, T., Manelis-Baram, L., Kaiser, H., et al. “Automated Analysis of Stereotypical Movements in Videos of Children With Autism Spectrum Disorder.” JAMA Network Open. https://doi.org/10.1001/jamanetworkopen.2024.32851

[Scientific Reports, 2026/07] MBaye, A. A., Perea, J. A., Tralie, C. J., Goodwin, M. S. “Automated quantification of stereotypical motor movements in autism using persistent homology.” Scientific Reports, accepted early version. https://doi.org/10.1038/s41598-026-60095-8

[bioRxiv, 2025/09] MBaye, A. A., et al. Same-title preprint, version 1, 2025-09-05. https://doi.org/10.1101/2025.09.03.674008

[Autism Research—Lemler, 2025/03] Lemler, C., et al. “Semi-Automated Multi-Label Classification of Autistic Mannerisms by Machine Learning on Post Hoc Skeletal Tracking.” Autism Research. https://doi.org/10.1002/aur.70020

[IEEE JBHI, 2025/03] Zhang, B., et al. “Enhancing Recognition of Stereotyped Movements in ASD Children Through Action Pattern Mining and Multi-Channel Fusion.” IEEE Journal of Biomedical and Health Informatics. https://doi.org/10.1109/JBHI.2024.3511601

[Scientific Reports—Koehler, 2024/03] Koehler, J. C., et al. “Classifying autism in a clinical population based on motion synchrony: a proof-of-concept study using real-life diagnostic interviews.” Scientific Reports. https://doi.org/10.1038/s41598-024-56098-y

[Scientific Data, 2025/06] Paulo, J. R., et al. “A Multimodal Dataset Addressing Motor Function in Autism.” Scientific Data. https://doi.org/10.1038/s41597-025-05313-0

[Autism Research—Freud, 2025/05] Freud, E., Ahmad, Z., Shelef, E., Hadad, B. S. “Effective Autism Classification Through Grasping Kinematics.” Autism Research. https://doi.org/10.1002/aur.70049

[Molecular Autism, 2025/10] Manelis-Baram, L., et al. “Comparing three algorithms of automated facial expression analysis in autistic children: different sensitivities but consistent proportions.” Molecular Autism. https://doi.org/10.1186/s13229-025-00685-x

[Developmental Science, 2026/03] Stenum, J., et al. “Quantifying Repetitive Hand Flapping Kinematics in Autistic and Non-Autistic Toddlers Using Video-Based Pose Estimation.” Developmental Science. https://doi.org/10.1111/desc.70176

[CVPR Workshops, 2026/06] Amraee, S., Singh, A., McCullough, A., Scheithauer, M., Goodwin, M., Ostadabbas, S. “Toward Automated Behavior Understanding in Autism: A Zero-Shot Vision-Language Model Approach.” CVPR Workshops, CV4Smalls. https://openaccess.thecvf.com/content/CVPR2026W/CV4Smalls/papers/Amraee_Toward_Automated_Behavior_Understanding_in_Autism_A_Zero-Shot_Vision-Language_Model_CVPRW_2026_paper.pdf
