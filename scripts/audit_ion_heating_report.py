"""Audit links, sources, layout and render every topical report page for inspection."""
from pathlib import Path
import json,re,hashlib
import pymupdf
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];T=P/'specific problems/离子加热问题';Q=P/'research/ion_heating'
R=Q/'renders';R.mkdir(exist_ok=True)
doc=pymupdf.open(T/'report.pdf');errors=[];links=0
for page in doc:
 for block in page.get_text('blocks'):
  if block[0]<15 or block[2]>page.rect.width-15 or block[1]<10 or block[3]>page.rect.height-10:
   errors.append({'page':page.number+1,'type':'page edge','text':block[4][:90]})
 for link in page.get_links():
  links+=1
  if link.get('file') and not (T/link['file']).exists():errors.append({'page':page.number+1,'type':'missing file','file':link['file']})
  if link['kind']==pymupdf.LINK_NAMED and not 0<=link.get('page',-1)<len(doc):errors.append({'page':page.number+1,'type':'unresolved destination','link':str(link)})
log=(T/'report.log').read_text(encoding='utf-8',errors='replace')
warnings=[line for line in log.splitlines() if any(x in line for x in ['Overfull','Missing character','undefined','multiply defined','! LaTeX Error'])]
if warnings:errors.append({'type':'TeX warnings','warnings':warnings})
source=(T/'report.tex').read_text(encoding='utf-8');v=json.loads((P/'research/reading_notes/verified.json').read_text(encoding='utf-8'))
keys={k for ks in re.findall(r'\\cite\w*\{([^}]+)\}',source) for k in ks.split(',')}
if keys-set(v):errors.append({'type':'unverified citations','keys':sorted(keys-set(v))})
for page in doc:page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(R/f'topic_p{page.number+1}.png')
contacts=[]
for start in range(0,len(doc),4):
 canvas=Image.new('RGB',(1280,1840),'#d8d8d8');draw=ImageDraw.Draw(canvas)
 for j,n in enumerate(range(start,min(start+4,len(doc)))):
  im=Image.open(R/f'topic_p{n+1}.png');im.thumbnail((615,875));x=j%2*640;y=j//2*920
  canvas.paste(im,(x+12,y+30));draw.text((x+12,y+8),f'Topic PDF page {n+1}',fill='black')
 path=R/f'topic_contact_{start//4+1}.png';canvas.save(path);contacts.append(path.relative_to(P).as_posix())
record={'date':'2026-11-12','file':(T/'report.pdf').relative_to(P).as_posix(),'pages':len(doc),
 'sha256':hashlib.sha256((T/'report.pdf').read_bytes()).hexdigest(),'cited_verified_keys':sorted(keys),
 'links':links,'warnings':warnings,'errors':errors,'rendered_pages':list(range(1,len(doc)+1)),'contact_sheets':contacts,
 'visual_inspection':'See visual_review.json; rendering alone is not visual inspection.'}
(Q/'topic_audit.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'pages':len(doc),'cited_full_reads':len(keys),'links':links,'errors':errors},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
