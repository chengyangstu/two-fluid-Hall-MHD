# coding: utf-8
"""Apply only the metadata corrections independently checked in the 39-paper batch."""
import json,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
p=P/'research/catalog.json';c=json.loads(p.read_text());by={r['key']:r for r in c}
updates={
 'L204':(2001,'Earth, Planets and Space','https://link.springer.com/article/10.1186/BF03353262'),
 'F766':(2001,'Earth, Planets and Space','https://link.springer.com/article/10.1186/BF03353269'),
 'E459':(2005,'Physics of Plasmas','https://doi.org/10.1063/1.1829064'),
 'L156':(2011,'Communications in Computational Physics','https://global-sci.com/cicp/article/download/5781/11498/12728'),
 'L210':(2016,'Journal of Geophysical Research: Space Physics','https://doi.org/10.1002/2015JA021975'),
 'L243':(2019,'Computer Physics Communications','https://www.sciencedirect.com/science/article/abs/pii/S0010465519300372')}
audit=[]
for k,(y,j,url) in updates.items():
 r=by[k]
 if 'metadata_before_101_review' not in r:r['metadata_before_101_review']={x:r.get(x) for x in ['year','journal']}
 r.update(year=y,journal=j)
 r['metadata_verification_source']=url
 audit.append({'key':k,'previous':r['metadata_before_101_review'],'year':y,'journal':j,'source':url,'basis':'全文首页/卷期与出版方入口；实际阅读版本见独立核读档案'})
by['L268']['authors'][0]='Chen Shi'
by['E474']['arxiv']='2110.03052'
# BibTeX comma notation keeps compound family names intact in citations.
family_names={'D. Del Sarto':'Del Sarto, D.','Daniele Del Sarto':'Del Sarto, Daniele',
 'Isaac Alonso Asensio':'Alonso Asensio, Isaac','Alejandro Alvarez Laguna':'Alvarez Laguna, Alejandro',
 'J. Graf von der Pahlen':'Graf von der Pahlen, J.'}
for r in c:
 if r['key'] in ['L049','L210','E459','L230','L243']:
  r['authors']=[family_names.get(a,a) for a in r['authors']]
p.write_text(json.dumps(c,ensure_ascii=False,indent=2))
(P/'research/read_to_101/metadata_corrections.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
q=P/'sections/01_selected_models.tex'
q.write_text(re.sub(r'(?<!\\)qquad',r'\\qquad',q.read_text()))
q=P/'scripts/delivery_audit.py';q.write_text(q.read_text().replace("'date':'2026-11-10'","'date':'2026-11-11'"))
print('Metadata corrected; selected-paper sections connected.')
