import json,requests,fitz,hashlib,time,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sources={
'Huba2004':['https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.93.175003/fulltext'],
'Simakov2008':['https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.101.105003/fulltext'],
'Knoll2006':['https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.96.135001/fulltext'],
'Grasso2001':['https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.86.5051/fulltext'],
'L014':['https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.80.4430/fulltext'],
'L108':['https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.99.235001/fulltext'],
'F646':['https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.87.265003/fulltext'],
'F732':['https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.118.125002/fulltext'],
'Otto2001':['https://articles.adsabs.harvard.edu/pdf/2001JGR...106.3751O'],
'L193':['https://mrx.pppl.gov/Publications/tharp13pop.pdf'],
}
def run(item):
 k,urls=item;tries=[]
 for u in urls:
  try:
   r=requests.get(u,timeout=(8,35));t={'url':u,'http':r.status_code,'bytes':len(r.content)};tries.append(t)
   if r.status_code==200 and r.content.startswith(b'%PDF'):
    d=fitz.open(stream=r.content,filetype='pdf');fp=P/'papers'/f'{k}_retrieved.pdf';fp.write_bytes(r.content)
    text=''.join('\n=== PAGE '+str(i+1)+' ===\n'+pg.get_text() for i,pg in enumerate(d));(P/'research/text'/f'{k}_retrieved.txt').write_text(text)
    return k,{'local_pdf':str(fp.relative_to(P)),'pages':len(d),'sha256':hashlib.sha256(r.content).hexdigest(),'download_url':r.url,'download_status':'PDF已取得，待人工身份核对','download_attempts_continuation':tries},d[0].get_text()[:800]
  except Exception as e:tries.append({'url':u,'error':str(e)[:180]})
 return k,{'download_attempts_continuation':tries},''
result=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for x in pool.map(run,sources.items()):
  result.append(x);print(x[0],x[1].get('pages'),x[2][:500],flush=True)
(P/'research/raw/core_retrieval_continuation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
c=json.loads((P/'research/catalog.json').read_text());b={r['key']:r for r in c}
for k,patch,first in result:b[k].update(patch)
(P/'research/catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2))
