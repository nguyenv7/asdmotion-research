"""Repeatable public data download and SHA-256 manifest. Existing files preserved."""
from pathlib import Path
import argparse, hashlib, json, datetime
import gdown
ROOT=Path(__file__).resolve().parents[1]
FILES={'dataset.pkl':'13t1tO4ZxTKmQG-w6fTy3hHQy8gX1bopl',
       'asdpose.zip':'1MiNIhlf4mL-vRW1ub2TP3nCYzfMW0bYt',
       'model.pth':'1PuPXu6pfBYjz0G6NvWOEUQ_RvedvinAE'}
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--manifest-only',action='store_true'); a=parser.parse_args()
    rows=[]
    for name,id_ in FILES.items():
        p=ROOT/'data/raw'/name; p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists() and not a.manifest_only:
            gdown.download(id=id_,output=str(p),resume=True)
        row={'file':str(p.relative_to(ROOT)),'url':f'https://drive.google.com/file/d/{id_}/view',
             'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'present' if p.exists() else 'missing'}
        if p.exists():
            with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
            row.update(bytes=p.stat().st_size,sha256=sha)
        rows.append(row)
    (ROOT/'data/raw/manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
if __name__=='__main__': main()
