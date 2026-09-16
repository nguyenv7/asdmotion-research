"""Descriptive metadata-only rules; no model fitting or threshold search.

This is a release integrity check, not an estimate of clinical or motion performance.
The rules are motivated by EDA on the same release: test results are therefore
post-hoc descriptive checks, not untouched-holdout generalization estimates.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, balanced_accuracy_score, precision_score, recall_score, f1_score
ROOT=Path(__file__).resolve().parents[1]

def summarize(y,p):
    return {'n':len(y),'confusion_matrix_rows_true_cols_pred_0_1':confusion_matrix(y,p,labels=[0,1]).tolist(),
            'precision':precision_score(y,p,zero_division=0),'recall':recall_score(y,p,zero_division=0),
            'f1':f1_score(y,p,zero_division=0),'balanced_accuracy':balanced_accuracy_score(y,p)}

def main():
    d=pd.read_csv(ROOT/'data/processed/clip_inventory.csv')
    result={'scope':'Post-hoc descriptive release audit, not a held-out clinical benchmark.', 'rules':{}}
    for partition,g in [('all',d),*list(d.groupby('split_membership'))]:
        result['rules'][partition]={'fps_30_predicts_positive':summarize(g.binary_label,(g.fps==30).astype(int)),
                                   'any_pose_predicts_positive':summarize(g.binary_label,(~g.all_zero_coordinates).astype(int))}
    result['boundary_duration_difference_top']= {str(k):int(v) for k,v in (d.duration_s-(d.end_frame-d.start_frame)).round(3).value_counts().head(10).items()}
    result['multi_label_clips']=int(d.action_name.str.contains(',').sum())
    result['notes']=['The original model need not explicitly ingest fps to be affected by correlated extraction artifacts.',
        'Temporal resampling cannot recover missing spatial information or undo selection bias.',
        'Recorded start_frame/end_frame are not trustworthy frame indices: units and padding need author confirmation.',
        'No inference about ASD diagnosis is possible from the absence of a non-ASD comparison cohort.']
    (ROOT/'data/processed/shortcut_audit.json').write_text(json.dumps(result,indent=2))
    pd.crosstab([d.split_membership,d.fps],d.binary_label).to_csv(ROOT/'data/processed/fps_label_crosstab.csv')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
