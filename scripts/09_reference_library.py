"""Build a reusable BibTeX library and integrity manifest for source PDFs."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def esc(s):
    return s.replace('&',r'\&').replace('_',r'\_').replace('%',r'\%')
def main():
    sources=json.loads((ROOT/'references/literature_sources.json').read_text(encoding='utf-8'))
    sources.append({'id':'duan2022','authors':'Haodong Duan; Yue Zhao; Kai Chen; Dahua Lin; Bo Dai',
       'title':'Revisiting Skeleton-Based Action Recognition','date':'2022-06','venue':'Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition',
       'url':'https://openaccess.thecvf.com/content/CVPR2022/html/Duan_Revisiting_Skeleton-Based_Action_Recognition_CVPR_2022_paper.html'})
    bib=[]
    for s in sources:
        authors=s['authors'].replace('; et al.','; others').replace('; ',' and ')
        fields={'author':authors,'title':'{'+s['title']+'}','year':s['date'][:4],'journal':s['venue'],'url':s['url']}
        if s.get('doi'): fields['doi']=s['doi']
        bib.append('@article{'+s['id']+',\n'+',\n'.join(f'  {k} = {{{esc(v)}}}' for k,v in fields.items())+'\n}')
    (ROOT/'references/references.bib').write_text('\n\n'.join(bib)+'\n',encoding='utf-8')
    rows=[]
    for p in sorted((ROOT/'references/papers').glob('*.pdf')):
        with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
        rows.append({'file':str(p.relative_to(ROOT)), 'bytes':p.stat().st_size,'sha256':sha})
    (ROOT/'references/papers/local_pdf_manifest.json').write_text(json.dumps(rows,indent=2))
    print(f'Wrote {len(sources)} BibTeX entries, hashed {len(rows)} PDFs.')
if __name__=='__main__': main()
