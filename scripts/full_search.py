import requests,json,time,concurrent.futures,subprocess,urllib.parse
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
P=Path(__file__).resolve().parents[1];s=requests.Session();s.mount('https://',HTTPAdapter(max_retries=Retry(total=2,backoff_factor=.5)))
qs=['"Hall MHD" AND (reconnection OR tearing)', '"Hall magnetohydrodynamic" AND (reconnection OR tearing)', '"two-fluid" AND "magnetic reconnection"', '"electron magnetohydrodynamics" AND reconnection', '"electron inertia" AND reconnection', '"gyrofluid" AND reconnection']
raw=P/'research/raw/full_search';raw.mkdir(exist_ok=True)
select='id,doi,title,publication_year,publication_date,type,authorships,primary_location,locations,abstract_inverted_index,cited_by_count'
def run(q):
 out=[];n=1;err='';total=0
 try:
  while True:
   f=raw/f'q{qs.index(q)}_{n}.json'
   if f.exists():d=json.loads(f.read_text())
   else:
    url='https://api.openalex.org/works?'+urllib.parse.urlencode({'search':q,'filter':'to_publication_date:2026-11-10','per-page':50,'page':n,'select':select})
    r=subprocess.run(['curl','-f','-sS','-L','--max-time','60','--connect-timeout','10',url],capture_output=True,timeout=65)
    if r.returncode:raise RuntimeError(r.stderr.decode()[:300])
    d=json.loads(r.stdout);f.write_text(json.dumps(d,ensure_ascii=False))
   rs=d.get('results',[]);out+=rs;total=d.get('meta',{}).get('count',0)
   print(q,n,len(out),total,flush=True)
   if len(out)>=total or not rs:break
   n+=1;time.sleep(.25)
 except Exception as e:err=str(e)
 return out,dict(terms=q,field='fulltext search',returned=len(out),total=total,error=err,exhausted=not err and len(out)>=total)
rows={};logs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for rs,l in ex.map(run,qs):
  logs.append(l)
  for r in rs:rows[r['id']]=r
(P/'research/full_search_log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2))
(P/'research/full_openalex.json').write_text(json.dumps(list(rows.values()),ensure_ascii=False))
print('DONE',len(rows),flush=True)
