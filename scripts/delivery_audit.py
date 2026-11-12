# coding: utf-8
from pathlib import Path
import json,re,hashlib,collections
import fitz
P=Path(__file__).resolve().parents[1]
c=json.loads((P/'research/catalog.json').read_text());v=json.loads((P/'research/reading_notes/verified.json').read_text());b={r['key']:r for r in c}
sp=P/'research/remaining_screen/screening.json'
screen={r['key']:r for r in json.loads(sp.read_text())['records']} if sp.exists() else {}
legacy_screen_count=len(screen)
extra=P/'research/synthesis_continuation/added_screening.json'
if extra.exists():screen.update({r['key']:r for r in json.loads(extra.read_text())['records']})
unique=[r for r in c if not r.get('duplicate_of') and r.get('eligibility')!='排除']
errors=[];cited=set();manifest=[];allfiles={}
for f in sorted((P/'papers').glob('*.pdf')):
 try:
  data=f.read_bytes();d=fitz.open(stream=data,filetype='pdf');item={'path':str(f.relative_to(P)),'bytes':len(data),'pages':len(d),'sha256':hashlib.sha256(data).hexdigest()};allfiles[item['path']]=item;manifest.append(item)
 except Exception as e:errors.append('PDF '+str(f)+': '+str(e))
for r in c:
 if r.get('local_pdf'):
  f=allfiles.get(r['local_pdf'])
  if not f:errors.append('missing '+r['key']+': '+r['local_pdf'])
  elif r.get('sha256') and f['sha256']!=r['sha256']:errors.append('hash mismatch '+r['key'])
for p in (P/'sections').rglob('*.tex'):
 if p.name=='07_catalog.tex':continue
 for ks in re.findall(r'\\cite\w*\{([^}]+)\}',p.read_text()):cited.update(ks.split(','))
for k in cited:
 if k not in v:errors.append('cited without full reading: '+k)
for k in v:
 if k not in b or not b[k].get('local_pdf'):errors.append('full read without PDF: '+k)
 if b.get(k,{}).get('duplicate_of'):errors.append('duplicate counted as full read: '+k)
for p in [*P.glob('*.tex'),*(P/'sections').rglob('*.tex')]:
 if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',p.read_text()):errors.append('control character '+str(p))
backlog=[]
for r in unique:
 if r['key'] not in v:
  backlog.append({'key':r['key'],'title':r['title'],'year':r.get('year'),
   'next_action':'核对全文身份、资格筛选、阅读全文和图表' if r.get('local_pdf') else '寻找合法公开匹配全文，再资格筛选和核读',
   'local_pdf':r.get('local_pdf',''),'doi':r.get('doi',''),'scope':r.get('scope',''),
   'screening_route':screen.get(r['key'],{}).get('route',''),
   'screening_reason':screen.get(r['key'],{}).get('reason','')})
(P/'research/pdf_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(P/'research/backlog.json').write_text(json.dumps(backlog,ensure_ascii=False,indent=2))
d=fitz.open(P/'main.pdf');links=collections.Counter();badlinks=[];outside=[];fonts=set()
for i,p in enumerate(d):
 for f in p.get_fonts():fonts.add(f[3])
 for ln in p.get_links():
  links[str(ln.get('kind'))]+=1
  if ln.get('kind') in (fitz.LINK_LAUNCH,fitz.LINK_GOTOR):
   fn=ln.get('file','');
   if fn and not (P/fn).exists():badlinks.append({'page':i+1,'file':fn})
  if ln.get('kind')==fitz.LINK_NAMED and not (0<=ln.get('page',-1)<len(d)):
   errors.append('unresolved internal destination: '+str(ln.get('nameddest')))
 for block in p.get_text('blocks'):
  x0,y0,x1,y1=block[:4]
  if x0<15 or x1>p.rect.width-15 or y0<10 or y1>p.rect.height-10:outside.append({'page':i+1,'bbox':list(block[:4]),'text':block[4][:80]})
log=(P/'main.log').read_text(errors='replace')
problem_lines=[s for s in log.splitlines() if any(t in s for t in ['Overfull','Missing character','undefined','! LaTeX Error'])]
errors+=['broken PDF local link '+str(x) for x in badlinks]
report={'date':'2026-11-12','raw_records':len(c),'unique_nonexcluded_candidates':len(unique),
 'candidate_records_with_pdf':sum(bool(r.get('local_pdf')) for r in unique),'verified_full_reads':len(v),
 'remaining_candidates':len(backlog),'physical_pdf_files_in_papers':len(manifest),'report_pages':len(d),
 'remaining_batch_title_metadata_screened':legacy_screen_count,
 'additional_citation_chase_records':len(screen)-legacy_screen_count,
 'priority_still_unread':sum(r['screening_route'].startswith('优先') for r in backlog),
 'priority_still_unread_with_pdf':sum(r['screening_route'].startswith('优先') and bool(r['local_pdf']) for r in backlog),
 'cited_keys':sorted(cited),'full_read_keys':sorted(v),'links_by_pymupdf_kind':dict(links),
 'fonts':sorted(fonts),'latex_layout_or_reference_warnings':problem_lines,'near_page_edge_text':outside,'errors':errors,
 'limitations':['候选未全部全文筛选；下载未全部人工确认身份；不代表全量调研完成','视觉抽检与全文页边界检查，非论文模拟复现']}
(P/'research/qa/delivery_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:report[k] for k in ['raw_records','unique_nonexcluded_candidates','candidate_records_with_pdf','verified_full_reads','remaining_candidates','report_pages','latex_layout_or_reference_warnings','errors']},ensure_ascii=False,indent=2))
# Rendering samples is independent of reading original papers.
for n in [1,2,3,7,10,13,20,26,27,28,36,37,44,50,55,57,65,85,105,len(d)-3,len(d)]:
 if 1<=n<=len(d):d[n-1].get_pixmap(matrix=fitz.Matrix(1.35,1.35)).save(P/f'research/qa/final_p{n}.png')
if errors or problem_lines:raise SystemExit(1)
