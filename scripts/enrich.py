import json,requests,fitz,re,hashlib,concurrent.futures,shutil,warnings
from pathlib import Path
warnings.filterwarnings('ignore');P=Path(__file__).resolve().parents[1];C=json.loads((P/'research/catalog.json').read_text())
# Correct a DOI detected by title verification; retain audit trail
r=next(x for x in C if x['key']=='Toth2008');r.update(title='Hall magnetohydrodynamics on block-adaptive grids',authors=['Gábor Tóth','Yingjuan Ma','Tamas I. Gombosi'],doi='10.1016/j.jcp.2008.04.010',journal='Journal of Computational Physics',year=2008,abstract='',urls=['https://public.websites.umich.edu/~gtoth/Papers/Toth2008_hall.pdf'],local_pdf='',download_status='待重试',correction='Initial DOI 10.1016/j.jcp.2008.01.011 resolved to unrelated paper; corrected after checking author PDF and publisher metadata.')
def norm(t):return re.sub('[^a-z0-9]','',t.lower())
def save(r,data,url):
 d=fitz.open(stream=data,filetype='pdf');txt='\n'.join(p.get_text() for p in d);f=P/'papers'/(r['key']+'.pdf');f.write_bytes(data);(P/'research/text'/(r['key']+'.txt')).write_text(txt);r.update(local_pdf=str(f.relative_to(P)),pages=len(d),download_url=url,sha256=hashlib.sha256(data).hexdigest(),download_status='PDF已取得，题名匹配',identity_title_ratio=1.0)
# local fulltext matching strictly title, not reference DOI
for m in json.loads((P/'research/local_matches.json').read_text()):
 r=next((x for x in C if x['key']==m['key']),None)
 if not r or r.get('local_pdf'):continue
 data=Path(m['path']).read_bytes();d=fitz.open(stream=data,filetype='pdf');text=d[0].get_text()
 if norm(r['title']) in norm(text):save(r,data,'local:'+m['path']);print('LOCAL',r['key'],flush=True)
links=json.loads((P/'research/author_pdf_links.json').read_text())
links += [{'url':'https://terpconnect.umd.edu/~drake/publications/reconnection/rogers01.pdf','context':''},{'url':r['urls'][0],'context':''}]
# supplemental exact public URLs from web research
links += [{'url':'https://public.websites.umich.edu/~gtoth/Papers/Toth2008_hall.pdf','context':''}]
def fetch(link):
 try:
  rr=requests.get(link['url'],timeout=(8,30));data=rr.content
  if not data.startswith(b'%PDF'):return None
  d=fitz.open(stream=data,filetype='pdf');first=d[0].get_text();return link['url'],data,first
 except:return None
# download only when index text or filename suggests an author's relevant year, plus core explicit URLs
wanted=[]
for l in links:
 u=l['url'];ctx=l['context']
 match=False
 for r in C:
  if r.get('local_pdf'):continue
  surname=(r['authors'][0].split()[-1].lower() if r['authors'] else '')
  if norm(r['title']) in norm(ctx) or surname and surname[:5] in u.lower() and str(r['year']) in u:match=True;break
 if match or any(x in u for x in ['rogers01','Toth2008_hall']):wanted.append(l)
print('TRY AUTHOR LINKS',len(wanted),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for result in ex.map(fetch,wanted):
  if not result:continue
  url,data,first=result;nf=norm(first)
  for r in C:
   if r.get('local_pdf'):continue
   if norm(r['title']) in nf:
    save(r,data,url);print('MATCH',r['key'],flush=True)
(P/'research/catalog.json').write_text(json.dumps(C,ensure_ascii=False,indent=2));print('TOTAL',sum(bool(x.get('local_pdf')) for x in C),flush=True)
