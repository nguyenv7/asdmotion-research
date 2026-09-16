"""Render every report page, contact sheets and page-boundary checks."""
from pathlib import Path
import json
import pymupdf
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def main():
    folder=ROOT/'outputs/latex/qa'; folder.mkdir(parents=True,exist_ok=True)
    doc=pymupdf.open(ROOT/'outputs/latex/main.pdf'); warnings=[]; thumbs=[]
    for n,page in enumerate(doc):
        pix=page.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25),alpha=False)
        pix.save(folder/f'page_{n+1:02d}.png')
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        im.thumbnail((310,439)); canvas=Image.new('RGB',(330,470),'#e8eaec')
        canvas.paste(im,((330-im.width)//2,20)); ImageDraw.Draw(canvas).text((10,452),f'Page {n+1}',fill='black'); thumbs.append(canvas)
        text=page.get_text()
        if '??' in text: warnings.append({'page':n+1,'issue':'unresolved-reference-like text'})
        for b in page.get_text('blocks'):
            if b[0]<0 or b[1]<0 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1:
                warnings.append({'page':n+1,'issue':'text outside page','bounds':list(b[:4])})
    for start in range(0,len(thumbs),6):
        sheet=Image.new('RGB',(990,940),'white')
        for j,t in enumerate(thumbs[start:start+6]): sheet.paste(t,((j%3)*330,(j//3)*470))
        sheet.save(folder/f'contact_{start//6+1:02d}.png')
    (folder/'qa.json').write_text(json.dumps({'pages':len(doc),'automatic_warnings':warnings,'visual_review':'Contact sheets and selected full pages must be reviewed separately.'},indent=2))
    print(f'Rendered {len(doc)} pages; automatic warnings: {len(warnings)}')
if __name__=='__main__': main()
