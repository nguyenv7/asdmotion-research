"""Generate data-quality and motion summaries from phase 1 inventory."""
from pathlib import Path
import json, os
import numpy as np
import pandas as pd
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parents[1]/'tmp/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
def main():
    df=pd.read_csv(ROOT/'data/processed/clip_inventory.csv')
    out=ROOT/'reports/figures'; out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    counts=df.action_name.str.split(',').explode().value_counts()
    counts.iloc[::-1].plot.barh(ax=ax[0,0],color='#306b87')
    ax[0,0].set(title='Atomic label occurrences (multi-label)',xlabel='Clips (not independent children)')
    for label,g in df.groupby('binary_label'):
        ax[0,1].hist(g.duration_s,bins=np.linspace(0,min(60,df.duration_s.max()),50),histtype='step',label=f'label {label}')
    ax[0,1].set(title='Clip duration',xlabel='Seconds (display truncated at 60 s)',ylabel='Clips'); ax[0,1].legend()
    for label,g in df.groupby('binary_label'):
        ax[1,0].hist(g.low_confidence_fraction,bins=np.linspace(0,1,40),histtype='step',density=True,label=f'label {label}')
    ax[1,0].set(title='Confidence missingness by binary label',xlabel='Fraction of joints with score < 0.2',ylabel='Density'); ax[1,0].legend()
    n=df.groupby('candidate_subject').size().sort_values(ascending=False)
    ax[1,1].bar(np.arange(len(n)),n,color='#306b87')
    ax[1,1].set(title='Contribution imbalance by inferred first ID token',xlabel='Candidate group rank (mapping unverified)',ylabel='Clips')
    fig.savefig(out/'release_overview.png',dpi=180); fig.savefig(out/'release_overview.pdf'); plt.close(fig)
    cols=['duration_s','low_confidence_fraction','mean_confidence','visible_joint_step_median_px','visible_joint_step_p99_px']
    df.groupby('binary_label')[cols].agg(['median','mean','std']).to_csv(ROOT/'data/processed/quality_motion_by_label.csv')
    warnings=[]
    if df.binary_label.isna().any(): warnings.append('Missing binary labels')
    if df.nonfinite_coordinate_fraction.gt(0).any(): warnings.append('Nonfinite coordinate values present')
    duplicates=df[df.coordinates_sha256.duplicated(False)]
    duplicates.to_csv(ROOT/'data/processed/exact_coordinate_duplicates.csv',index=False)
    # Metadata differences that can make a naive clip classifier appear better than motion recognition.
    groups=df.groupby('candidate_subject').agg(clips=('identifier','size'),positive_fraction=('binary_label','mean'),hours=('duration_s',lambda x:x.sum()/3600))
    groups.to_csv(ROOT/'data/processed/candidate_group_summary.csv')
    (ROOT/'data/processed/eda_notes.json').write_text(json.dumps({'warnings':warnings,
        'clip_population_only':True,'inference':'No ASD diagnostic discrimination or subject-independent model performance estimated.',
        'pixel_motion_warning':'Raw pixel displacement depends on camera distance, crop, fps and pose jitter. It is not anatomical velocity.',
        'confidence_warning':'Confidence is pose-estimator confidence, not behavior certainty or missing-at-random evidence.'},indent=2))
    print('Wrote descriptive tables and release_overview figure.')
if __name__=='__main__': main()
