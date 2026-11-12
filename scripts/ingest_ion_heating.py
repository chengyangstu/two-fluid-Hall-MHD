"""Explicit, idempotent import of completed heating readings; not a search script."""
from pathlib import Path
import json, hashlib, re
import pymupdf
P=Path(__file__).resolve().parents[1]
T=P/'specific problems/离子加热问题'
Q=P/'research/ion_heating'; Q.mkdir(exist_ok=True)
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=read(P/'research/catalog.json'); v=read(P/'research/reading_notes/verified.json')
baseline=Q/'baseline.json'
if not baseline.exists():
 write(baseline,{'date':'2026-11-12','verified_keys':list(v),'catalog_keys':[r['key'] for r in c],
  'pdf_paths':[p.relative_to(P).as_posix() for p in sorted((P/'papers').glob('*.pdf')) if p.name not in {
  'Kaptanoglu2020.pdf','Kaptanoglu2020_accepted.pdf','TS6FEC2025.pdf','F679.pdf','F674_published.pdf',
  'Yoo2017Heating.pdf','Yoon2018Heating.pdf','F743.pdf','Yoon2023PhaseSpace.pdf','Tanabe2015MAST.pdf',
  'Loureiro2013Heating.pdf','Numata2015Heating.pdf','Finelli2021.pdf','Che2014Buneman.pdf','TenBarge2019MMS.pdf'}],
  'baseline_pdf_count':324,'baseline_volume_pages':[94,162,20],
  'note':'Baseline verified/catalog captured before this importer; 15 downloaded files excluded from PDF baseline by explicit filename.'})
b=read(baseline); by={r['key']:r for r in c}
groups=[('hall_fluid',read(T/'reading_notes/hall_fluid_records.json')['full_text_records']),
 ('experiment',read(T/'reading_notes/experiment_records.json')),
 ('closure',list(read(T/'reading_notes/closure_records.json')['records'].values()))]
records=[]; changes=read(Q/'metadata_changes.json') if (Q/'metadata_changes.json').exists() else []
for branch,rr in groups:
 summaries_path=T/f'reading_notes/{branch}_summaries_zh.json'
 summaries=read(summaries_path) if summaries_path.exists() else {}
 for r in rr:
  k=r['key']; path=P/r['local_pdf']; data=path.read_bytes()
  assert data.startswith(b'%PDF-'),path
  with pymupdf.open(path) as d: pages=len(d)
  assert hashlib.sha256(data).hexdigest()==r['sha256'],k
  assert pages==r.get('page_count',r.get('pages')),k
  doi=r.get('doi','')
  duplicate=[z['key'] for z in c if doi and z.get('doi','').lower()==doi.lower() and z['key']!=k]
  assert not duplicate,(k,duplicate)
  old=by.get(k)
  if old is None:
   old={'key':k,'id':k,'source':'2026-11-12离子/电子加热专题：原文及稳定来源核对',
    'selection':'种子追引及定向检索后完成所记录版本全文核读','urls':[],'landing_urls':[]}
   c.append(old);by[k]=old
  title=re.sub(r'a\)$','',r['title']) if k=='F674' else r['title']
  for field,value in [('title',title),('authors',r['authors']),('year',r['year']),('doi',doi),('journal',r.get('journal',old.get('journal','')))]:
   if old.get(field) not in (None,'',value): changes.append({'key':k,'field':field,'before':old.get(field),'after':value})
   old[field]=value
  if old.get('local_pdf') and old['local_pdf']!=r['local_pdf']:
   prior={x:old[x] for x in ['local_pdf','pages','sha256','download_url'] if x in old}
   prev=old.setdefault('previous_versions',[])
   if not any(x['local_pdf']==prior['local_pdf'] for x in prev):prev.append(prior)
  sources=r.get('sources',r.get('landing_urls',[]))
  for f in ['source_url','pdf_url']:
   if r.get(f): sources=[*sources,r[f]]
  if doi:sources=['https://doi.org/'+doi,*sources]
  old['landing_urls']=list(dict.fromkeys([*old.get('landing_urls',[]),*sources]))
  old.update(local_pdf=r['local_pdf'],pages=pages,sha256=r['sha256'],
   read_status='全文及关键图表已核读',download_status='匹配全文与关键PDF页面已人工核验',
   identity_checked='核读版本题名、作者、正文和关键图式；独立补充/正式版缺口见专题记录',
   scope=r['model'],heating_review_record=f'specific problems/离子加热问题/reading_notes/{branch}_records.json')
  version=r.get('version_read',r.get('version',''))
  old['heating_review_version']=version
  if k=='Kaptanoglu2020':
   earlier=P/'papers/Kaptanoglu2020.pdf'
   prev=old.setdefault('previous_versions',[])
   if not any(x['local_pdf']=='papers/Kaptanoglu2020.pdf' for x in prev):
    with pymupdf.open(earlier) as d:early_pages=len(d)
    prev.append({'local_pdf':'papers/Kaptanoglu2020.pdf','pages':early_pages,
     'sha256':hashlib.sha256(earlier.read_bytes()).hexdigest(),
     'source_url':'https://arxiv.org/abs/2003.00557','title':'Advanced modeling for the HIT-SI Experiment',
     'read_status':'本轮仅阅读PDF第1–11页，不作为另一篇全文核读'})
  note={f:r.get(f,'') for f in ['pages_read','figures_checked','model','parameters','finding','limitation','assessment']}
  if branch=='experiment':
   note.update(pages_read=f'所记录版本全部{pages}个PDF物理页；正文、方法、结果、讨论、图表、参考文献及适用文内附录均核读。',
    figures_checked='直接查看PDF物理页'+','.join(map(str,r['visual_verification']['physical_pdf_pages']))+'；'+r['visual_verification']['figures_equations'],
    parameters=r['model_method_parameters'],finding='；'.join(r['results_within_scope']),limitation='；'.join(r['limitations']),
    assessment='实验或动理学/轨道证据，不能计为纯Hall双温模拟；比例及机制边界详见独立加热专题。')
  if not note['assessment']:note['assessment']='模型身份、温度/能量/熵产区别及跨文献判断见独立加热专题；不把本篇单独作为普适分配定律。'
  note.update(summaries.get(k,{}))
  if k in summaries:old['scope']=summaries[k]['model']
  note.update(status='全文及关键图表已核读',read_date='2026-11-12',
   topic_note=f'specific problems/离子加热问题/reading_notes/{branch}_review.md',version_read=version)
  is_new=k not in b['verified_keys']
  if is_new:v[k]=note
  else:v[k]['heating_recheck']='2026-11-12；'+note['topic_note']
  records.append({'key':k,'new_full_read':is_new,'branch':branch,'pages':pages,'version':version,
   'local_pdf':r['local_pdf'],'doi':doi,'model':r['model'],'note':note['topic_note'],'sha256':r['sha256']})
v['F635']['heating_recheck']='2026-11-12；specific problems/离子加热问题/reading_notes/F635_note.json；10页完整复读，不增计'
write(P/'research/catalog.json',c);write(P/'research/reading_notes/verified.json',v)
write(Q/'metadata_changes.json',changes)
batch={'date':'2026-11-12','baseline_full_reads':len(b['verified_keys']),
 'new_full_reads':sum(r['new_full_read'] for r in records),'rechecked_full_reads':sum(not r['new_full_read'] for r in records),
 'current_full_reads':len(v),'read_main_version_pages':sum(r['pages'] for r in records),
 'new_full_read_main_version_pages':sum(r['pages'] for r in records if r['new_full_read']),
 'additional_root_recheck':{'key':'F635','pages':10,'new_full_read':False,'note':'reading_notes/F635_note.json'},
 'new_pdf_files':sorted(p.relative_to(P).as_posix() for p in (P/'papers').glob('*.pdf') if p.relative_to(P).as_posix() not in b['pdf_paths']),
 'records':records,'limits':'Counts include experiments, PIC/GK/hybrid comparators and one conference manuscript; not independent Hall simulations. Kaptanoglu earlier 21-page version not fully read.'}
write(T/'batch_manifest.json',batch)
print(json.dumps({k:batch[k] for k in ['new_full_reads','rechecked_full_reads','current_full_reads','read_main_version_pages','new_full_read_main_version_pages']},ensure_ascii=False))
