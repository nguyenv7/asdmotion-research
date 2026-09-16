# Open questions and concrete next requests

These are research questions to resolve, not requests that have been sent. The author-contact draft below can be reviewed and sent later by the user.

## Blocking an exact reproduction

1. Which exact version of `dataset.pkl` corresponds to the 2024 published experiments? The current download has 36,930 records rather than 36,000. What additions/exclusions explain the change?
2. What do the labeled identifier's first three tokens mean? How do they map to `asdpose.zip/db.csv` child_id, assessment, assessment_index, camera_index? The clip prefixes have 329 distinct first tokens; the continuous metadata has 241 child IDs.
3. Why are all negative clips stored at 25 fps and most positive clips at 30 fps? Were videos resampled, metadata relabeled, or extraction paths mixed? What are the actual source timestamps?
4. Are start_frame/end_frame actually seconds or another time convention? What padding/trimming and inclusive/exclusive endpoints produced arrays roughly two seconds longer than their difference?
5. Are the released train/test partitions the exact published 220/21-child partitions? Where are the original held-out subject list and a separate validation split?
6. Where are complete continuous-event annotations, subtype labels and reannotation outcomes? Can selected clips be mapped unambiguously to full recordings, including negative coverage?
7. What explains 883 paper camera recordings versus 914 archive files, 319 paper assessments versus 318 archive metadata groups, and 71 versus 70 PLS assessments?
8. Which training commit/config/checkpoint generated the publication? The current template, fork and supplement disagree on epochs, schedule and split names. What selection procedure chose architecture/checkpoint/threshold?

## Measurement quality questions

- What is the meaning of all-zero poses, child-detection failures and confidence values outside [0,1] in continuous records? Which frames are outside the room/occluded vs extraction failures?
- Are skeleton confidence values calibrated or postprocessed? Is `adjust` a frame alignment offset, and what event time base should accompany it?
- Which coordinate order and shape convention apply across mixed stored dimensions? Is there camera calibration or synchronization information?
- Are movement labels mutually exclusive, multilabel, exhaustive, or partially coded? How were Other, Playing with object, and Tapping judged stereotypical?
- Can the original annotator disagreements, subtype reliability and exclusion rules be provided?
- Can deidentified age/sex/assessment/clinical-score tables be linked under appropriate terms? Current records do not supply those individual clinical variables.

## Draft author inquiry — not sent

We are investigating ASDMotion with an initial focus on reproducible skeleton-data measurement. We downloaded the currently linked labeled file and continuous archive on 16 September 2026 (hashes attached in our manifest). Before reproducing or extending the model, could you clarify the release version, identifier-to-participant/recording crosswalk, timing units and padding, frame-rate preprocessing, and exact publication split/configuration?

Our audit found 36,930 labeled records (8,267 positive / 28,663 negative), whereas the paper describes 36,000 selected segments. All negative clips store 25 fps and 6,520 positive clips store 30 fps. The continuous archive contains 914 recordings with 241 explicit child IDs. We would also appreciate the complete continuous annotations and missing-pose handling convention, if available. We are treating these as version/provenance questions and are not assuming they reflect errors in the published experiment.

## Feasibility after answers

- Without participant mapping: descriptive release analysis and code repair are possible; validated child-generalization claims are not.
- Without aligned continuous labels: clip reliability is possible; full-session event/burden error is not.
- Without appropriate comparison cohorts: ASD diagnostic discrimination is not testable.
- Without clinical covariates: demographic/severity associations are not testable from the release alone.
