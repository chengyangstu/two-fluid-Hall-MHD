import requests,json,time,re,concurrent.futures,xml.etree.ElementTree as ET
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
requests_session=requests.Session()
requests_session.mount("https://",HTTPAdapter(max_retries=Retry(total=3,backoff_factor=1)))
requests.get=requests_session.get
from pathlib import Path
P=Path(__file__).resolve().parents[1]; raw=P/'research/raw'; raw.mkdir(exist_ok=True)
queries=['Hall magnetic reconnection','two fluid magnetic reconnection','electron inertia reconnection','ten moment reconnection','Hall plasmoid reconnection','Hall reconnection guide field','Hall reconnection experiment','Hall reconnection numerical method','two fluid tearing mode','Hall reconnection three dimensional','Hall reconnection sawtooth','electron magnetohydrodynamic reconnection']
log=[]; records={}
def run(q):
 f=raw/('openalex_'+str(queries.index(q))+'.json')
 try:
  if f.exists(): d=json.loads(f.read_text())
  else:
   r=requests.get('https://api.openalex.org/works',params={'search':q,'per-page':200,'filter':'to_publication_date:2026-11-10'},timeout=50);r.raise_for_status();d=r.json();f.write_text(json.dumps(d,ensure_ascii=False))
  return q,d,None
 except Exception as e:return q,{},str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for q,d,e in ex.map(run,queries):
  log.append({'database':'OpenAlex','query':q,'total':d.get('meta',{}).get('count'),'returned':len(d.get('results',[])),'error':e,'cap':200})
  for a in d.get('results',[]):
   k=a['id']; a.setdefault('queries',[]).append(q)
   if k in records: records[k]['queries']+=a['queries']
   else: records[k]=a
  print(q,len(d.get('results',[])),e,flush=True)
# arXiv broad boolean union, fetch all accessible pages
q='all:reconnection AND (all:Hall OR all:"two-fluid" OR all:"two fluid" OR all:"ten-moment" OR all:"electron inertia" OR all:"electron magnetohydrodynamics")'
ars=[]; ns={'a':'http://www.w3.org/2005/Atom','ar':'http://arxiv.org/schemas/atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
for start in range(0,2000,200):
 f=raw/f'arxiv_{start}.xml'
 try:
  if f.exists(): s=f.read_text()
  else:
   time.sleep(3);r=requests.get('https://export.arxiv.org/api/query',params={'search_query':q,'start':start,'max_results':200,'sortBy':'submittedDate','sortOrder':'descending'},timeout=90);r.raise_for_status();s=r.text;f.write_text(s)
  root=ET.fromstring(s);es=root.findall('a:entry',ns); total=int(root.findtext('o:totalResults','0',ns));print('arxiv',start,total,len(es),flush=True)
  for e in es:
   aid=e.findtext('a:id','',ns).split('/abs/')[-1];date=e.findtext('a:published','',ns)
   if date[:10]>'2026-11-10':continue
   ars.append({'arxiv':re.sub(r'v\d+$','',aid),'version':aid,'title':' '.join(e.findtext('a:title','',ns).split()),'abstract':' '.join(e.findtext('a:summary','',ns).split()),'authors':[x.text for x in e.findall('a:author/a:name',ns)],'date':date,'doi':e.findtext('ar:doi','',ns),'journal':e.findtext('ar:journal_ref','',ns)})
  if start+len(es)>=total or not es:break
 except Exception as e:log.append({'database':'arXiv','query':q,'start':start,'error':str(e)});break
log.append({'database':'arXiv','query':q,'returned':len(ars)})
(P/'research/openalex.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2))
(P/'research/arxiv.json').write_text(json.dumps(ars,ensure_ascii=False,indent=2))
(P/'research/search_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
print('DONE',len(records),len(ars),flush=True)
