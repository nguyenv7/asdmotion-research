"""Render three real clips and a clearly labeled synthetic aggregation example."""
from pathlib import Path
import os,sys,json
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/matplotlib'))
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from asdmotion_research.io import load_numeric_pickle
from asdmotion_research.temporal import aggregate_windows
EDGES=[(5,6),(5,7),(7,9),(6,8),(8,10),(5,11),(6,12),(11,12),(11,13),(13,15),(12,14),(14,16)]
def main():
    inv=pd.read_csv(ROOT/'data/processed/clip_inventory.csv')
    selections=[]
    for name,label in [('Hand flapping',1),('Body rocking',1),('NoAction',0)]:
        subset=inv[(inv.action_name==name)&inv.duration_s.between(5,15)]
        selections.append(int(subset.sort_values(['low_confidence_fraction','record_index']).iloc[0].record_index))
    data=load_numeric_pickle(ROOT/'data/raw/dataset.pkl')['annotations']
    fig,axes=plt.subplots(3,5,figsize=(12,7),layout='constrained'); detail=[]
    for row,i in enumerate(selections):
        r=data[i]; kp=r['keypoint']; c=r['keypoint_score']; fps=r['fps']
        if kp.ndim==4: kp=kp[0];c=c[0]
        valid=c>=.2; pts=kp[valid]; lo=pts.min(0)-15; hi=pts.max(0)+15
        for col,t in enumerate(np.linspace(0,len(kp)-1,5,dtype=int)):
            ax=axes[row,col]
            for a,b in EDGES:
                if valid[t,a] and valid[t,b]: ax.plot(kp[t,[a,b],0],kp[t,[a,b],1],color='#286983',lw=2)
            ax.scatter(kp[t,valid[t],0],kp[t,valid[t],1],s=10,color='#c66b39')
            ax.set(xlim=(lo[0],hi[0]),ylim=(hi[1],lo[1]),title=f'{t/fps:.2f} s');ax.set_aspect('equal');ax.axis('off')
            if col==0: ax.text(-.12,.5,r['action_name'],rotation=90,transform=ax.transAxes,va='center')
        detail.append({'record_index':i,'identifier':r['identifier'],'selection':'minimum low-confidence fraction within label and 5-15s duration; intentionally favorable examples'})
    fig.suptitle('Real released skeleton clips: five sampled frames each\nNot a validation of the label; low-confidence joints omitted (score < 0.2)',fontsize=12)
    out=ROOT/'reports/figures'; fig.savefig(out/'motion_examples.png',dpi=180);fig.savefig(out/'motion_examples.pdf');plt.close(fig)
    fig,axes=plt.subplots(3,1,figsize=(11,7),layout='constrained')
    for ax,i in zip(axes,selections):
        r=data[i]; kp=r['keypoint'];c=r['keypoint_score'];fps=r['fps']
        shoulder=np.linalg.norm(kp[:,5]-kp[:,6],axis=-1)
        use=(c[:,5]>=.2)&(c[:,6]>=.2)&(shoulder>0)
        scale=np.median(shoulder[use]); center=(kp[:,5]+kp[:,6])/2
        for j,name in [(9,'Left wrist'),(10,'Right wrist')]:
            y=(kp[:,j,1]-center[:,1])/scale
            y[~(use&(c[:,j]>=.2))]=np.nan
            ax.plot(np.arange(len(y))/fps,y,label=name,lw=1)
        ax.set(title=r['action_name'],xlabel='Seconds from clip start',ylabel='Wrist height /\nshoulder width');ax.legend(loc='upper right')
    fig.suptitle('Confidence-masked, body-relative trajectories; gaps remain missing')
    fig.savefig(out/'wrist_trajectories.png',dpi=180);fig.savefig(out/'wrist_trajectories.pdf');plt.close(fig)
    (ROOT/'data/processed/motion_example_manifest.json').write_text(json.dumps(detail,indent=2))
    starts=[0,30,60,90]; ends=[200,230,260,290]; scores=[.1,.9,.2,.1]
    maximum,coverage=aggregate_windows(starts,ends,scores,300,'max')
    mean,_=aggregate_windows(starts,ends,scores,300,'mean')
    fig,ax=plt.subplots(figsize=(10,3),layout='constrained')
    ax.plot(np.arange(300)/30,maximum,label='Maximum');ax.plot(np.arange(300)/30,mean,label='Mean')
    ax.axhline(.85,ls='--',color='black',lw=1,label='Threshold 0.85')
    ax.set(title='Synthetic score example: one positive window spreads over 6.67 seconds',xlabel='Time (s)',ylabel='Score',ylim=(0,1));ax.legend(ncol=3)
    fig.savefig(out/'aggregation_demo.pdf');fig.savefig(out/'aggregation_demo.png',dpi=180);plt.close(fig)
    print('Real examples and synthetic aggregation diagram written.')
if __name__=='__main__': main()
