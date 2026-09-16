"""Inventory continuous skeleton archive, read one representative numeric member.

No extraction or unsafe checkpoint deserialization. ZIP CRC validation streams all bytes.
"""
from pathlib import Path
import zipfile,json,sys,collections,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from asdmotion_research.io import NumpyUnpickler
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check-crc',action='store_true'); args=ap.parse_args()
    p=ROOT/'data/raw/asdpose.zip'
    with zipfile.ZipFile(p) as z:
        members=[i for i in z.infolist() if not i.is_dir()]
        report={'member_count':len(members),'uncompressed_bytes':sum(i.file_size for i in members),
                'extensions':dict(collections.Counter(Path(i.filename).suffix for i in members)),
                'first_members':[{'name':i.filename,'bytes':i.file_size} for i in members[:12]],'crc_check':'not requested'}
        (ROOT/'data/processed/archive_inventory.json').write_text(json.dumps([{'name':i.filename,'bytes':i.file_size,'crc32':i.CRC} for i in members],indent=2))
        candidates=sorted([i for i in members if i.filename.endswith('.pkl')],key=lambda i:i.file_size)
        if candidates:
            member=candidates[len(candidates)//2]
            with z.open(member) as f: obj=NumpyUnpickler(f).load()
            report['sample_member']=member.filename
            report['sample_schema']={k:{'type':type(v).__name__,'shape':list(v.shape) if hasattr(v,'shape') else None,
                'preview':str(v)[:500] if not hasattr(v,'shape') else None} for k,v in obj.items()} if isinstance(obj,dict) else {'type':type(obj).__name__}
        if args.check_crc:
            bad=z.testzip(); report['crc_check']='passed' if bad is None else f'failed: {bad}'
        (ROOT/'data/processed/archive_summary.json').write_text(json.dumps(report,indent=2))
        print(json.dumps(report,indent=2))
if __name__=='__main__': main()
