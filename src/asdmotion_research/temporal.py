"""Explicit half-open interval semantics for future event evaluation."""
import numpy as np


def aggregate_windows(starts, ends, scores, n_frames, reduction='max'):
    """Return frame scores and coverage; uncovered frames are NaN, never negatives."""
    if reduction not in {'max','mean'}: raise ValueError(reduction)
    output=np.full(n_frames,-np.inf) if reduction=='max' else np.zeros(n_frames)
    coverage=np.zeros(n_frames,dtype=int)
    if not (len(starts)==len(ends)==len(scores)): raise ValueError('Length mismatch')
    for s,e,p in zip(starts,ends,scores):
        if not (0<=s<e<=n_frames): raise ValueError('Invalid half-open interval')
        if not np.isfinite(p): raise ValueError('Nonfinite score')
        if reduction=='max': output[s:e]=np.maximum(output[s:e],p)
        else: output[s:e]+=p
        coverage[s:e]+=1
    if reduction=='mean': output=np.divide(output,coverage,out=np.full(n_frames,np.nan),where=coverage>0)
    output[coverage==0]=np.nan
    return output,coverage


def extract_events(scores, threshold=.85):
    """Return [start,end) runs, treating missing coverage as a break."""
    active=np.isfinite(scores)&(np.asarray(scores)>=threshold)
    edges=np.diff(np.r_[False,active,False].astype(int))
    return list(zip(np.where(edges==1)[0].tolist(),np.where(edges==-1)[0].tolist()))


def interval_iou(a,b):
    intersection=max(0,min(a[1],b[1])-max(a[0],b[0]))
    union=(a[1]-a[0])+(b[1]-b[0])-intersection
    return intersection/union if union else 0.
