# coding: utf-8
from pathlib import Path
import json,re,hashlib,collections
import fitz
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];O=P/'分卷';Q=P/'research/split_reports'
V=json.loads((P/'research/reading_notes/verified.json').read_text())
manifest=json.loads((Q/'manifest.json').read_text())
reports=[];errors=[];rendered=[]
samples={
 '01_theory_numerics':[1,2,10,21,84,85,86,88],
 '02_paper_results':[1,2,8,29,39,128,152,162],
 '03_solved_open':[1,2,4,5,6,7,8,13,14,20]
}
for stem,title in manifest['titles'].items():
    path=O/(stem+'.pdf');doc=fitz.open(path);counts=collections.Counter();fonts=set();edge=[]
    for page in doc:
        for font in page.get_fonts():fonts.add(font[3])
        for b in page.get_text('blocks'):
            if b[0]<15 or b[2]>page.rect.width-15 or b[1]<10 or b[3]>page.rect.height-10:
                edge.append({'page':page.number+1,'bbox':list(b[:4]),'text':b[4][:80]})
        for link in page.get_links():
            counts[link['kind']]+=1
            if link['kind']==fitz.LINK_NAMED and not (0<=link.get('page',-1)<len(doc)):
                errors.append([stem,page.number+1,'unresolved local destination',link])
            if link.get('file'):
                target=O/link['file']
                if not target.exists():errors.append([stem,page.number+1,'missing file',link['file']])
                elif link['kind']==fitz.LINK_GOTOR and target.suffix.lower()=='.pdf':
                    with fitz.open(target) as other:
                        if not 0<=link.get('page',-1)<len(other):
                            errors.append([stem,page.number+1,'bad target page',link])
    log=(O/(stem+'.log')).read_text(errors='replace')
    warnings=[line for line in log.splitlines() if any(w in line for w in ['Overfull','Missing character','undefined','! LaTeX Error','multiply defined'])]
    if warnings:errors.append([stem,'TeX warnings',warnings])
    if edge:errors.append([stem,'page edge',edge])
    body=(O/(stem+'.tex')).read_text()
    cites=set()
    for keys in re.findall(r'\\cite\w*\{([^}]+)\}',body):cites.update(keys.split(','))
    if not cites<=set(V):errors.append([stem,'unverified citations',sorted(cites-set(V))])
    if stem=='02_paper_results':
        dossier=set(re.findall(r'\\label\{paper:([^}]+)\}',body))
        assert dossier==set(V),(len(dossier),len(V))
    reports.append({'file':str(path.relative_to(P)),'title':title,'pages':len(doc),
                    'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'chapters':[x for x in doc.get_toc() if x[0]==1],
                    'links':dict(counts),'fonts':sorted(fonts),'cited_full_reads':len(cites),
                    'latex_warnings':warnings,'near_page_edges':edge})
    for n in samples[stem]:
        out=Q/f'{stem}_p{n}.png'
        doc[n-1].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(out)
        rendered.append((stem,n,out))
for k in range(0,len(rendered),4):
    chunk=rendered[k:k+4];canvas=Image.new('RGB',(1240,900*((len(chunk)+1)//2)),'#ddd');draw=ImageDraw.Draw(canvas)
    for j,(stem,n,path) in enumerate(chunk):
        im=Image.open(path);im.thumbnail((600,850));x=j%2*620;y=j//2*900
        canvas.paste(im,(x+10,y+30));draw.text((x+10,y+8),f'{stem}, PDF page {n}',fill='black')
    canvas.save(Q/f'contact_{k//4+1}.png')
record={'date':'2026-11-12','volumes':reports,'errors':errors,'full_read_dossiers_preserved':122,
        'all_master_labels_preserved':manifest['all_master_labels_preserved'],
        'rendered_samples':[[s,n] for s,n,p in rendered]}
(Q/'audit.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
print(json.dumps({'volumes':[(r['title'],r['pages']) for r in reports],'errors':errors},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
