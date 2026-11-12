import requests,json,re,hashlib,concurrent.futures,time,shutil,warnings
from pathlib import Path
from urllib.parse import urljoin
import fitz
from bs4 import BeautifulSoup
warnings.filterwarnings('ignore');P=Path(__file__).resolve().parents[1];C=json.loads((P/'research/catalog.json').read_text())
# previously acquired PDFs are copied only when their recorded DOI matches
local={}
for f in (P.parent/'Reconnection知识库').rglob('*manifest*.json'):
 try:
  data=json.loads(f.read_text())
  if not isinstance(data,list):continue
  for r in data:
   if not isinstance(r,dict):continue
   d=(r.get('doi') or '').lower();lp=r.get('local_pdf')
   if d and lp:
    for root in [f.parent,f.parent.parent,f.parent.parent.parent]:
     fp=root/lp
     if fp.is_file() and fp.suffix=='.pdf':local[d]=fp;break
 except:pass
extra={
'Biskamp1997':['https://ireap.umd.edu/Theory/Publications/pub97-11.pdf'],
'Ren2005':['https://mrx.pppl.gov/Publications/ren05prl.pdf'],
'Shay2004':['https://www.physics.udel.edu/~shay/papers/ShayM.2004.PhPl.11.2199.pdf'],
'Cassak2010':['https://www.physics.udel.edu/~shay/papers/CassakP.2010.PhPl.17.062105.Shay.pdf'],
'Cassak2006':['https://www.physics.udel.edu/~shay/papers/CassakP.2006.ApJ.644.L145L128.Shay.pdf'],
'Hakim2008':['https://ammar-hakim.org/_static/files/Hakim_jfe_2008.pdf'],
'Birn2001':['https://www.physics.udel.edu/~shay/papers/BirnJ.2001.JGR.106.3715.Shay.pdf'],
'Baalrud2011':['https://plasmatheory.engin.umich.edu/wp-content/uploads/sites/519/2021/01/BaalrudPOP2011c.pdf']}
def valid(data):
 if not data.startswith(b'%PDF'):return None
 try:
  d=fitz.open(stream=data,filetype='pdf');txt='\n'.join(p.get_text() for p in d);return len(d),txt
 except:return None

def worker(r):
 key=r['key'];path=P/'papers'/f'{key}.pdf';tries=[];success=None;src=''
 if path.exists():success=valid(path.read_bytes());src=r.get('download_url','cached')
 if not success and r['doi'] in local:
  fp=local[r['doi']];data=fp.read_bytes();success=valid(data)
  if success:path.write_bytes(data);src='local:'+str(fp)
 urls=extra.get(key,[])+r['urls'];d=r['doi']
 if r.get('arxiv'):urls.insert(0,'https://arxiv.org/pdf/'+r['arxiv'])
 # DOI metadata supplies potential publisher fulltext, not fabricated success
 if d.startswith('10.1103/'):urls.append('https://journals.aps.org/'+('prl' if 'physrevlett' in d else 'pre')+'/pdf/'+d)
 urls=list(dict.fromkeys(urls))
 def attempt(u):
  try:
   rr=requests.get(u,timeout=(8,20),headers={'User-Agent':'Academic literature retrieval (local research)'},allow_redirects=True)
   res=valid(rr.content) if rr.status_code==200 else None
   tries.append({'url':u,'http':rr.status_code,'bytes':len(rr.content),'pdf':bool(res)})
   return rr,res
  except Exception as e:tries.append({'url':u,'error':str(e)[:160]});return None,None
 if not success:
  for url in urls[:7]:
   rr,res=attempt(url)
   if res:success=res;path.write_bytes(rr.content);src=rr.url;break
 # Follow explicit citation_pdf_url and PDF anchors on known landing pages
 if not success:
  lands=r.get('landing_urls',[])[:3]
  if d:lands+=['https://doi.org/'+d]
  for u in list(dict.fromkeys(lands))[:3]:
   rr,res=attempt(u)
   if res:success=res;path.write_bytes(rr.content);src=rr.url;break
   if rr is None or rr.status_code!=200:continue
   soup=BeautifulSoup(rr.text,'html.parser');m=soup.find('meta',attrs={'name':'citation_pdf_url'})
   links=([urljoin(rr.url,m.get('content'))] if m and m.get('content') else [])
   links += [urljoin(rr.url,a['href']) for a in soup.find_all('a',href=True) if '.pdf' in a['href'].lower() and ('pdf' in a.get_text().lower() or 'download' in a.get_text().lower())][:2]
   for v in links[:2]:
    rr2,res2=attempt(v)
    if res2:success=res2;path.write_bytes(rr2.content);src=rr2.url;break
   if success:break
 if success:
  n,txt=success;r.update(download_status='PDF已取得，自动可解析',local_pdf=str(path.relative_to(P)),pages=n,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),download_url=src)
  (P/'research/text'/f'{key}.txt').write_text(txt)
  # lexical identity check uses title words on first pages; manual core audit remains separate
  words=re.findall(r'[a-z]{4,}',r['title'].lower());first=txt[:14000].lower();ratio=sum(w in first for w in words)/max(1,len(words));r['identity_title_ratio']=round(ratio,3)
  if ratio<.6:r['download_status']='PDF待人工身份核对'
 else:r.update(download_status='未取得公开PDF',local_pdf='',pages=0)
 r['download_attempts']=tries
 return r
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
 for i,r in enumerate(ex.map(worker,C)):
  out.append(r);print(i+1,len(C),r['key'],r['download_status'],r.get('pages'),flush=True)
  if len(out)%10==0:(P/'research/download_progress.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(P/'research/catalog.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('DONE PDFs',sum(bool(r['local_pdf']) for r in out),flush=True)
