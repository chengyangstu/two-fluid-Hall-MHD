"""Produce a traceable candidate ledger; title heuristics do not certify relevance."""
from pathlib import Path
import json,gzip,csv,re
P=Path(__file__).resolve().parents[1];T=P/'specific problems/离子加热问题';S=T/'search'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
with gzip.open(S/'openalex_works.json.gz','rt',encoding='utf-8') as f:works=json.load(f)
edges=read(S/'citation_edges.json');ids={e[x] for e in edges for x in ('from','to')}
c=read(P/'research/catalog.json');v=read(P/'research/reading_notes/verified.json')
def doi(s):return (s or '').lower().removeprefix('https://doi.org/').removeprefix('http://dx.doi.org/')
bydoi={doi(r['doi']):r for r in c if r.get('doi')}
bykey={r['key']:r for r in c}; rows={}
for r in works:
 if r['id'] not in ids:continue
 d=doi(r.get('doi'));old=bydoi.get(d,{});k=old.get('key','')
 title=r.get('title','');flag=bool(re.search(r'heat|energy|fluid|Hall|moment|closure',title,re.I))
 rows[d or r['id']]={'openalex':r['id'],'key':k,'doi':d,'title':title,'year':r.get('publication_year',''),
  'source':'OpenAlex seed one-hop graph','screening':'仅自动题名优先提示，未人工确认相关性' if flag else '引文图节点，未以题名排除',
  'full_read_status':'全库已全文核读（查看具体批次）' if k in v else '尚未全文核读',
  'local_pdf':old.get('local_pdf',''),'priority_hint':str(flag),'detail':''}
for filename,field in [('hall_fluid_search.json','candidates'),('experiment_search.json','candidates_not_read_by_this_agent'),('closure_search.json','candidate_backlog_not_full_read_this_branch')]:
 for r in read(S/filename)[field]:
  d=doi(r.get('doi'));k=r.get('key',r.get('existing_key','')) or ''
  old=bydoi.get(d,bykey.get(k,{}));k=old.get('key',k)
  identity=d or k or r['title']
  z=rows.setdefault(identity,{'openalex':'','key':k,'doi':d,'title':r.get('title',old.get('title','')),
   'year':r.get('year',old.get('year','')),'source':'','screening':'','full_read_status':'','local_pdf':old.get('local_pdf',''),'priority_hint':'True','detail':''})
  z['source']+='; '+filename;z['key']=k
  z['screening']='分支定向追踪；具体状态与理由见detail，不据标题确认科学结论'
  z['full_read_status']='全库已全文核读（查看具体批次）' if k in v else '尚未全文核读'
  z['detail']+=(('; ' if z['detail'] else '')+json.dumps(r,ensure_ascii=False))
with (T/'candidate_screening.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(next(iter(rows.values()))));w.writeheader();w.writerows(rows.values())
summary={'date':'2026-11-12','raw_unique_metadata':len(works),'one_hop_nodes':len(ids),'one_hop_edges':len(edges),
 'ledger_rows_after_merging_targeted_candidates':len(rows),'full_read_entries_in_ledger':sum(bool(r['key'] in v) for r in rows.values()),
 'limits':'Unranked graph nodes were not excluded. Title matching is an automated hint only. Broad 16020 metadata hits were not all manually screened. Refer to branch logs for manually traced candidates.'}
(S/'screening_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(summary)
