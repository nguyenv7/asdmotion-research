"""Profile the complete released clip file without fitting a classifier.

Run: .venv/Scripts/python.exe scripts/01_profile_dataset.py
Identifier prefixes are candidate grouping keys, not verified subject IDs.
"""
from pathlib import Path
import sys, json, hashlib, collections, argparse
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import numpy as np
import pandas as pd
from asdmotion_research.io import load_numeric_pickle

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=ROOT/'data/raw/dataset.pkl')
    args = ap.parse_args()
    out = ROOT/'data/processed'; out.mkdir(parents=True, exist_ok=True)
    data = load_numeric_pickle(args.input)
    print('Top level:', type(data), flush=True)
    records = data['annotations'] if isinstance(data, dict) else data
    structure = {'top_keys': list(data) if isinstance(data, dict) else None,
                 'record_count':len(records), 'first_record_fields':{}, 'other_top_level':{}}
    for k,v in records[0].items():
        structure['first_record_fields'][k] = {'type':type(v).__name__, 'shape':list(v.shape) if hasattr(v,'shape') else None,
                                               'example': str(v)[:300] if not isinstance(v,np.ndarray) else None}
    if isinstance(data,dict):
        for k,v in data.items():
            if k!='annotations': structure['other_top_level'][k] = {'type':type(v).__name__, 'length':len(v) if hasattr(v,'__len__') else None, 'preview':str(v)[:2500]}
    split = data.get('split',{}) if isinstance(data,dict) else {}
    split_sets = {k:set(v) for k,v in split.items()}
    structure['split_membership_counts']={k:len(v) for k,v in split_sets.items()}
    structure['other_top_level'].pop('split',None)
    rows=[]; joint_counts=np.zeros(17,dtype=np.int64); joint_low=np.zeros(17,dtype=np.int64)
    for i,r in enumerate(records):
        kp=np.asarray(r['keypoint']); score=np.asarray(r['keypoint_score'])
        original_ndim=kp.ndim
        if kp.ndim==4 and kp.shape[0]==1: kp=kp[0]; score=score[0]
        if kp.ndim!=3 or kp.shape[-2:]!=(17,2):
            raise ValueError(f'Unexpected skeleton shape at {i}: {kp.shape}')
        valid=np.isfinite(kp).all(-1)&np.isfinite(score)&(score>0)
        visible=valid&(score>=0.2)
        joint_counts += np.isfinite(score).sum(0)
        joint_low += (score<0.2).sum(0)
        adjacent=visible[1:]&visible[:-1]
        delta=np.linalg.norm(np.diff(kp,axis=0),axis=-1)
        speed=delta[adjacent]
        ident=str(r.get('identifier',r.get('frame_dir',i)))
        fps=float(r.get('fps',30)); frames=kp.shape[0]
        parts=ident.split('_')
        row={'record_index':i,'identifier':ident,'action_name':str(r.get('action_name','unknown')),
             'binary_label':r.get('binary_label',r.get('label',None)), 'frames':frames,'fps':fps,
             'duration_s':frames/fps,'start_frame':r.get('start_frame'), 'end_frame':r.get('end_frame'),
             'candidate_subject':parts[0],'candidate_session':'_'.join(parts[:2]),'candidate_video':'_'.join(parts[:3]),
             'keypoint_dtype':str(kp.dtype),'score_dtype':str(score.dtype),'img_shape':str(r.get('img_shape')),
             'original_keypoint_ndim':original_ndim,
             'score_outside_unit_interval_count':int(((score<0)|(score>1)).sum()),
             'nonfinite_score_count':int((~np.isfinite(score)).sum()),
             'declared_frames':r.get('total_frames'),
             'declared_frame_count_matches':r.get('total_frames')==frames,
             'all_zero_coordinates':bool((kp==0).all()),'all_zero_confidence':bool((score==0).all()),
             'split_membership':'|'.join(sorted(k for k,v in split_sets.items() if ident in v)),
             'nonfinite_coordinate_fraction':float((~np.isfinite(kp)).mean()),
             'zero_confidence_fraction':float((score==0).mean()),'low_confidence_fraction':float((score<0.2).mean()),
             'mean_confidence':float(np.nanmean(score)),
             'visible_joint_step_median_px':float(np.median(speed)) if len(speed) else None,
             'visible_joint_step_p99_px':float(np.quantile(speed,.99)) if len(speed) else None,
             'coordinates_sha256':hashlib.sha256(kp.tobytes()).hexdigest(),
             'pose_and_confidence_sha256':hashlib.sha256(kp.tobytes()+score.tobytes()).hexdigest()}
        rows.append(row)
        if i%5000==0: print(f'Profiled {i}/{len(records)}',flush=True)
    df=pd.DataFrame(rows); df.to_csv(out/'clip_inventory.csv',index=False)
    summary={'records':len(df),'binary_labels':df.binary_label.value_counts(dropna=False).to_dict(),
             'split_clip_counts':df.split_membership.value_counts(dropna=False).to_dict(),
             'all_zero_coordinate_clips':int(df.all_zero_coordinates.sum()),
             'all_zero_confidence_clips':int(df.all_zero_confidence.sum()),
             'declared_frame_count_mismatches':int((~df.declared_frame_count_matches).sum()),
             'original_keypoint_ndim_counts':df.original_keypoint_ndim.value_counts().to_dict(),
             'score_outside_unit_interval_count':int(df.score_outside_unit_interval_count.sum()),
             'nonfinite_score_count':int(df.nonfinite_score_count.sum()),
             'movement_labels':df.action_name.value_counts().to_dict(),
             'candidate_subject_count':df.candidate_subject.nunique(),'candidate_session_count':df.candidate_session.nunique(),
             'candidate_video_count':df.candidate_video.nunique(), 'fps_counts':df.fps.value_counts().to_dict(),
             'total_clip_hours_not_unique_recording_hours':df.duration_s.sum()/3600,
             'duplicate_identifiers':int(df.identifier.duplicated().sum()),
             'duplicate_coordinate_arrays':int(df.coordinates_sha256.duplicated().sum()),
             'duplicate_pose_and_confidence_arrays':int(df.pose_and_confidence_sha256.duplicated().sum()),
             'duration_seconds':df.duration_s.describe(percentiles=[.01,.25,.5,.75,.95,.99]).to_dict(),
             'confidence_by_clip':df[['zero_confidence_fraction','low_confidence_fraction','mean_confidence']].describe().to_dict(),
             'joint_fraction_score_below_02':(joint_low/np.maximum(joint_counts,1)).tolist(),
             'grouping_status':'Identifier prefixes are inferred; official mapping required before claims of subject independence.',
             'confidence_threshold_status':'0.2 is an analyst-chosen audit threshold, not a calibrated probability.'}
    split_audit={}
    for name,subset in df.groupby('split_membership'):
        split_audit[name]={'records':len(subset),'labels':subset.binary_label.value_counts().to_dict(),
                           'candidate_subjects':subset.candidate_subject.nunique(),
                           'all_zero_confidence_clips':int(subset.all_zero_confidence.sum())}
    if len(split_sets)==2:
        a,b=list(split_sets)
        left=df[df.split_membership.eq(a)]; right=df[df.split_membership.eq(b)]
        split_audit['overlap']={'identifier_members':len(split_sets[a]&split_sets[b]),
                               'candidate_subjects':len(set(left.candidate_subject)&set(right.candidate_subject)),
                               'coordinate_hashes':len(set(left.coordinates_sha256)&set(right.coordinates_sha256)),
                               'pose_and_confidence_hashes':len(set(left.pose_and_confidence_sha256)&set(right.pose_and_confidence_sha256)),
                               'nonzero_coordinate_hashes':len(set(left.loc[~left.all_zero_coordinates,'coordinates_sha256'])&set(right.loc[~right.all_zero_coordinates,'coordinates_sha256']))}
    for name,obj in [('dataset_structure',structure),('dataset_summary',summary),('released_split_audit',split_audit)]:
        (out/f'{name}.json').write_text(json.dumps(obj,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x)),encoding='utf-8')
    df.groupby(['action_name','binary_label']).agg(clips=('frames','size'),hours=('duration_s',lambda x:x.sum()/3600),median_seconds=('duration_s','median'),mean_low_confidence=('low_confidence_fraction','mean')).to_csv(out/'label_summary.csv')
    print(json.dumps(summary,indent=2,default=str),flush=True)


if __name__=='__main__': main()
