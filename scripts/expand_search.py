"""Paginated precise queries; append only, never overwrite review/download state."""
import requests,json,time,re,unicodedata,concurrent.futures
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
P=Path(__file__).resolve().parents[1];s=requests.Session();s.mount('https://',HTTPAdapter(max_retries=Retry(total=3,backoff_factor=1)))
qs=['"Hall MHD" AND (reconnection OR tearing)','"Hall magnetohydrodynamic" AND (reconnection OR tearing)','"two-fluid" AND "magnetic reconnection"','"electron magnetohydrodynamics" AND reconnection','"electron inertia" AND reconnection','"ten-moment" AND reconnection','"five-moment" AND reconnection','"Hall" AND "sawtooth"']
raw=P/'research/raw/expanded';raw.mkdir(exist_ok=True)
def run(q):
 allr=[];cur='*';i=0;err='';count=0
 try:
  while cur:
   f=raw/f'q{qs.index(q)}_{i}.json'
   if f.exists():d=json.loads(f.read_text())
   else:
    r=s.get('https://api.openalex.org/works',params={'search':q,'filter':'to_publication_date:2026-11-10','per-page':200,'cursor':cur},timeout=45);r.raise_for_status();d=r.json();f.write_text(json.dumps(d,ensure_ascii=False))
   rs=d.get('results',[]);allr+=rs;count=d.get('meta',{}).get('count');cur=d.get('meta',{}).get('next_cursor');i+=1
   print(q,i,len(allr),count,flush=True)
   if not rs:break
   time.sleep(.15)
 except Exception as e:err=str(e)
 return allr,dict(query=q,total=count,returned=len(allr),pages=i,error=err,exhausted=not bool(err) and len(allr)>=count)
rows={};logs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for rs,log in ex.map(run,qs):
  logs.append(log)
  for r in rs:rows[r['id']]=r
(P/'research/expanded_search_log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2))
(P/'research/expanded_openalex.json').write_text(json.dumps(list(rows.values()),ensure_ascii=False))
print('TOTAL UNIQUE',len(rows),flush=True)
