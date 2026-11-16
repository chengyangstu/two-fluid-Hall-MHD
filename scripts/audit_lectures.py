#!/usr/bin/env python3
# coding: utf-8
"""Audit standalone lecture PDFs and optionally render every page with Poppler.
Run after latexmk. Requires PyMuPDF and Pillow; --render additionally pdftoppm.
Visual review is a human/agent step, not asserted by this script.
"""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess
import fitz
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('lecture',choices=['Lecture-HallMHD','Lecture-TM']);p.add_argument('--render',action='store_true');a=p.parse_args()
d=root/a.lecture;pdf=d/'main.pdf';doc=fitz.open(pdf)
log=(d/'main.log').read_text(errors='replace')
bad=[line for line in log.splitlines() if re.search(r'Overfull|Missing character|undefined|multiply defined|^!',line)]
texfiles=[d/'main.tex',d/'preamble.tex']+sorted((d/'chapters').glob('*.tex'))
control=[]
for f in texfiles:
 for n,l in enumerate(f.read_bytes().split(b'\n'),1):
  if any(c<32 and c!=9 for c in l):control.append(f'{f.relative_to(root)}:{n}')
labels=[];cites=[];figs=[]
for f in texfiles:
 s=f.read_text();labels+=re.findall(r'\\label\{([^}]+)\}',s)
 for c in re.findall(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}',s):cites+=c.split(',')
 figs+=re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',s)
aux=(d/'main.aux').read_text();usedrefs=re.findall(r'\\bibcite\{([^}]+)\}',aux)
missing_cites=sorted(set(cites)-set(usedrefs));missing_figs=[f for f in figs if not(d/f).is_file()]
textbounds=[]
for i,page in enumerate(doc):
 for b in page.get_text('blocks'):
  if b[0]<-1 or b[1]<-1 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1:textbounds.append({'page':i+1,'bbox':list(b[:4])})
linktypes={}
for page in doc:
 for link in page.get_links():linktypes[str(link['kind'])]=linktypes.get(str(link['kind']),0)+1
report=dict(pdf=str(pdf.relative_to(root)),pages=len(doc),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),figures=len(figs),bibliography_entries=len(usedrefs),labels=len(labels),duplicate_labels=sorted({x for x in labels if labels.count(x)>1}),log_errors=bad,control_characters=control,missing_citations=missing_cites,missing_figures=missing_figs,external_text_bounds=textbounds,link_counts=linktypes,visual_review='See separate editorial_review.json; script does not assert visual review.')
(d/'research/pdf_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
assert not(bad or control or missing_cites or missing_figs or textbounds or report['duplicate_labels'])
if a.render:
 qa=d/'research/qa';qa.mkdir(exist_ok=True)
 poppler=shutil.which('pdftoppm')
 if not poppler:raise RuntimeError('pdftoppm not available')
 probe=subprocess.run([poppler,'-f','1','-l','1','-r','90','-png',str(pdf),str(qa/'probe')],capture_output=True,text=True)
 if probe.returncode or 'Syntax Error' in probe.stderr:
  renderer={'engine':'PyMuPDF','reason':'Poppler preflight failed; available runtime lacks working CJK language mapping','poppler_stderr':probe.stderr}
  for i,page in enumerate(doc):page.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(qa/f'page-{i+1:02d}.png')
 else:
  subprocess.run([poppler,'-r','90','-png',str(pdf),str(qa/'page')],check=True)
  renderer={'engine':'Poppler','reason':'preflight passed'}
 (d/'research/render_record.json').write_text(json.dumps(renderer,ensure_ascii=False,indent=2)+'\n')
 pages=sorted((f for f in qa.glob('page-*.png') if int(f.stem.split('-')[-1])<=len(doc)),key=lambda f:int(f.stem.split('-')[-1]))
 for first in range(0,len(pages),9):
  sheet=Image.new('RGB',(1350,1974),'#d8dee3');draw=ImageDraw.Draw(sheet)
  for j,f in enumerate(pages[first:first+9]):
   im=Image.open(f);im.thumbnail((434,616));x=(j%3)*450+(450-im.width)//2;y=(j//3)*658+25
   sheet.paste(im,(x,y));draw.text(((j%3)*450+12,(j//3)*658+6),f'PDF page {first+j+1}',fill='black')
  sheet.save(qa/f'contact-{first//9+1:02d}.png')
