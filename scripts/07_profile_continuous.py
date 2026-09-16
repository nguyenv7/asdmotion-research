"""Profile all continuous-recording pickle members, one at a time, inside ZIP.

Reads numeric pickles with the project's restricted unpickler. Does not extract
or modify the archive. Camera-stream duration must not be called unique child
observation time; recordings from multiple cameras overlap in real time.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys
import time
import zipfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from asdmotion_research.io import NumpyUnpickler


def describe(values):
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if not len(values):
        return None
    return dict(zip(['min', 'p25', 'median', 'p75', 'max'],
                    map(float, np.quantile(values, [0,.25,.5,.75,1]))))


def profile_record(record):
    kp = np.asarray(record['keypoint'])
    score = np.asarray(record['keypoint_score'])
    if kp.ndim != 4 or kp.shape[-2:] != (17,2) or score.shape != kp.shape[:-1]:
        raise ValueError(f'Unexpected pose shapes {kp.shape}, {score.shape}')
    m, t, j, c = kp.shape
    zero_frame = np.all(kp == 0, axis=(0,2,3))
    zero_score_frame = np.all(score == 0, axis=(0,2))
    finite = np.isfinite(score)
    finite_count = int(finite.sum())
    safe_score = np.where(finite, score, 0)
    joint_sum = safe_score.sum(axis=(0,1), dtype=np.float64)
    joint_count = finite.sum(axis=(0,1))
    fps = float(record.get('fps', np.nan))
    frame_count = record.get('frame_count')
    declared_length = record.get('length_seconds')
    bbox = record.get('child_bbox')
    child_score = record.get('child_detection_score')
    row = {
        'person_slots':m, 'pose_frames':t, 'joints':j,
        'coordinate_dtype':str(kp.dtype), 'score_dtype':str(score.dtype),
        'keypoint_shape':json.dumps(list(kp.shape)),
        'keypoint_score_shape':json.dumps(list(score.shape)),
        'original_shape':json.dumps(list(record.get('original_shape', []))),
        'fps':fps, 'frame_count':frame_count, 'length_seconds':declared_length,
        'pose_duration_seconds': t/fps if fps > 0 else None,
        'adjust':record.get('adjust'), 'field_names':json.dumps(sorted(record)),
        'frame_count_matches_pose': bool(frame_count == t),
        'all_zero_coordinate_frames':int(zero_frame.sum()),
        'all_zero_coordinate_frame_fraction':float(zero_frame.mean()) if t else None,
        'all_zero_score_frames':int(zero_score_frame.sum()),
        'all_zero_score_frame_fraction':float(zero_score_frame.mean()) if t else None,
        'coordinate_nonfinite_values':int((~np.isfinite(kp)).sum()),
        'score_nonfinite_values':int((~finite).sum()),
        'confidence_mean_all':float(safe_score.sum(dtype=np.float64)/finite_count) if finite_count else None,
        'confidence_zero_fraction':float(np.mean(score == 0)),
        'confidence_below_01_fraction':float(np.mean(score < .1)),
        'confidence_above_05_fraction':float(np.mean(score > .5)),
        'confidence_outside_0_1_values':int(((score < 0)|(score > 1)).sum()),
        'child_bbox_shape':json.dumps(list(np.shape(bbox))) if bbox is not None else None,
        'child_detection_score_shape':json.dumps(list(np.shape(child_score))) if child_score is not None else None,
    }
    if child_score is not None:
        cs = np.asarray(child_score)
        row.update(child_detection_score_mean=float(np.nanmean(cs)),
                   child_detection_score_zero_fraction=float(np.mean(cs == 0)),
                   child_detection_score_above_01_fraction=float(np.mean(cs > .1)))
    else:
        row.update(child_detection_score_mean=None, child_detection_score_zero_fraction=None,
                   child_detection_score_above_01_fraction=None)
    for idx in range(17):
        row[f'joint_{idx:02d}_confidence_mean'] = float(joint_sum[idx]/joint_count[idx]) if joint_count[idx] else None
    return row, joint_sum, joint_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=ROOT/'data/raw/asdpose.zip')
    parser.add_argument('--manifest', type=Path, default=ROOT/'data/interim/archive_metadata.csv')
    parser.add_argument('--out', type=Path, default=ROOT/'data/processed')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(args.manifest)
    by_name = {str(r['filename']):r for r in manifest.to_dict('records')}
    rows, failures = [], []
    total_joint_sum = np.zeros(17, dtype=np.float64)
    total_joint_count = np.zeros(17, dtype=np.int64)
    start = time.time()
    inventory_path = args.out/'continuous_inventory.csv'
    with zipfile.ZipFile(args.archive) as archive, inventory_path.open('w', newline='', encoding='utf-8') as output:
        members = sorted([x for x in archive.infolist() if x.filename.endswith('.pkl')], key=lambda x:x.filename)
        writer = None
        for index, member in enumerate(members, 1):
            try:
                with archive.open(member) as stream:
                    record = NumpyUnpickler(stream).load()
                row, js, jc = profile_record(record)
                del record
                stem = Path(member.filename).stem
                meta = by_name.get(stem, {})
                row = {'member':member.filename, 'filename':stem,
                       'archive_uncompressed_bytes':member.file_size,
                       'manifest_match':stem in by_name,
                       'child_id':meta.get('child_id'), 'assessment':meta.get('assessment'),
                       'assessment_index':meta.get('assessment_index'),
                       'camera_index':meta.get('camera_index'), **row}
                if writer is None:
                    writer = csv.DictWriter(output, fieldnames=list(row))
                    writer.writeheader()
                writer.writerow(row)
                rows.append(row)
                total_joint_sum += js
                total_joint_count += jc
            except Exception as exc:
                failures.append({'member':member.filename, 'error':f'{type(exc).__name__}: {exc}'})
            if index % 25 == 0 or index == len(members):
                output.flush()
                print(f'{index}/{len(members)} members; failures={len(failures)}; elapsed={time.time()-start:.1f}s', flush=True)
    df = pd.DataFrame(rows)
    member_names = set(df.filename)
    manifest_names = set(manifest.filename.astype(str))
    assessments = manifest.drop_duplicates(['child_id','assessment','assessment_index'])
    total_frames = int(df.pose_frames.sum())
    summary = {
        'archive':str(args.archive), 'manifest':str(args.manifest),
        'method':'One archive member at a time; restricted NumPy unpickler; no extraction; joint confidence includes zero/missing entries.',
        'profiled_members':len(df), 'failed_members':failures,
        'elapsed_seconds':time.time()-start, 'manifest_rows':len(manifest),
        'manifest_unique_children':int(manifest.child_id.nunique()),
        'manifest_unique_assessments':len(assessments),
        'manifest_assessment_counts':assessments.assessment.value_counts().to_dict(),
        'manifest_duplicate_filenames':int(manifest.filename.duplicated().sum()),
        'members_without_manifest':sorted(member_names-manifest_names),
        'manifest_without_members':sorted(manifest_names-member_names),
        'total_pose_frames':total_frames,
        'fps_member_counts':df.fps.value_counts().sort_index().to_dict(),
        'fps_rounded_member_counts':df.fps.round().value_counts().sort_index().to_dict(),
        'fps_distribution':describe(df.fps),
        'shape_member_counts':df.original_shape.value_counts().to_dict(),
        'person_slots_member_counts':df.person_slots.value_counts().to_dict(),
        'coordinate_dtype_member_counts':df.coordinate_dtype.value_counts().to_dict(),
        'field_schema_member_counts':df.field_names.value_counts().to_dict(),
        'total_camera_stream_hours':float(df.pose_duration_seconds.sum()/3600),
        'total_declared_camera_stream_hours':float(df.length_seconds.sum()/3600),
        'camera_duration_seconds_distribution':describe(df.pose_duration_seconds),
        'frame_count_mismatches':int((~df.frame_count_matches_pose).sum()),
        'frame_count_minus_pose_minus_adjust_nonzero':int(((df.frame_count-df.pose_frames-df.adjust) != 0).sum()),
        'adjust_member_counts':df.adjust.value_counts().sort_index().to_dict(),
        'max_abs_duration_difference_seconds':float((df.pose_duration_seconds-df.length_seconds).abs().max()),
        'all_zero_coordinate_frames':int(df.all_zero_coordinate_frames.sum()),
        'all_zero_coordinate_frame_fraction_weighted':float(df.all_zero_coordinate_frames.sum()/total_frames),
        'all_zero_score_frames':int(df.all_zero_score_frames.sum()),
        'all_zero_score_frame_fraction_weighted':float(df.all_zero_score_frames.sum()/total_frames),
        'zero_pose_fraction_per_recording_distribution':describe(df.all_zero_coordinate_frame_fraction),
        'all_zero_pose_recordings':int((df.all_zero_coordinate_frames == df.pose_frames).sum()),
        'coordinate_nonfinite_values':int(df.coordinate_nonfinite_values.sum()),
        'score_nonfinite_values':int(df.score_nonfinite_values.sum()),
        'confidence_outside_0_1_values':int(df.confidence_outside_0_1_values.sum()),
        'joint_confidence_mean_weighted':np.divide(total_joint_sum, total_joint_count,
                                                  out=np.zeros(17), where=total_joint_count>0).tolist(),
        'confidence_mean_per_recording_distribution':describe(df.confidence_mean_all),
        'paper_comparison': {'paper_children':241, 'paper_assessments':319,
                             'paper_camera_recordings':883, 'paper_assessment_counts':{'ADOS':226,'PLS':71,'Cognitive':22},
                             'note':'Release inventory differs from paper denominators; not silently harmonized. Camera hours include simultaneous viewpoints.'},
        'label_mapping_status':'Mapping from annotated-clip identifiers to these explicit child/assessment/camera identities is not verified.',
    }
    (args.out/'continuous_summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['profiled_members','failed_members','total_pose_frames','total_camera_stream_hours','all_zero_coordinate_frame_fraction_weighted']}, indent=2), flush=True)
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
