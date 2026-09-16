"""Create a split only from an explicit, externally verified subject mapping.

Input CSV: identifier, subject_id, partition (train/validation/test).
Do not feed guessed identifier prefixes to this script as a verified mapping.
"""
from pathlib import Path
import argparse, json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mapping',type=Path,required=True); args=ap.parse_args()
    inv=pd.read_csv(ROOT/'data/processed/clip_inventory.csv',dtype={'identifier':str})
    mapping=pd.read_csv(args.mapping,dtype=str)
    required={'identifier','subject_id','partition'}
    if not required.issubset(mapping): raise ValueError('Need identifier, subject_id, partition')
    if mapping[list(required)].isna().any().any(): raise ValueError('Missing mapping values')
    if mapping.identifier.duplicated().any(): raise ValueError('Duplicate mapping identifiers')
    if not set(mapping.partition)<= {'train','validation','test'}: raise ValueError('Unknown partition')
    merged=inv.merge(mapping,on='identifier',how='left',validate='many_to_one')
    if merged.subject_id.isna().any(): raise ValueError('Incomplete subject mapping')
    if merged.groupby('subject_id').partition.nunique().max()!=1: raise ValueError('Subject leakage')
    observed=merged.loc[~merged.all_zero_coordinates]
    if len(observed) and observed.groupby('coordinates_sha256').partition.nunique().max()!=1:
        raise ValueError('Identical nonzero coordinates across partitions')
    if set(merged.partition)!={'train','validation','test'}: raise ValueError('All three partitions required')
    merged.to_csv(ROOT/'data/processed/verified_split_manifest.csv',index=False)
    print(merged.groupby('partition').agg(clips=('identifier','size'),subjects=('subject_id','nunique')))
if __name__=='__main__': main()
