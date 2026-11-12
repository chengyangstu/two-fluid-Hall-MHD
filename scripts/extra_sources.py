import requests,json,re,concurrent.futures,difflib,hashlib,warnings
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import fitz
warnings.filterwarnings('ignore');P=Path(__file__).resolve().parents[1];C=json.loads((P/'research/catalog.json').read_text());out=[]
urls=['https://www.physics.udel.edu/~shay/publications.html','https://www.physics.udel.edu/~shay/papers/','https://ireap.umd.edu/Theory/publications.htm','https://terpconnect.umd.edu/~drake/publications/','https://paulcassak.sandbox.wvu.edu/publications','https://mrx.pppl.gov/Publications/publications.html','https://public.websites.umich.edu/~gtoth/Papers/']
for i,u in enumerate(urls):
 try:
  rr=requests.get(u,timeout=25);(P/'research/raw'/f'author_{i}.html').write_text(rr.text);s=BeautifulSoup(rr.text,'html.parser')
  for a in s.find_all('a',href=True):
   link=urljoin(rr.url,a['href'])
   if '.pdf' not in link.lower():continue
   context=a.parent.get_text(' ',strip=True)
   if len(context)<80 and a.parent.parent:context=a.parent.parent.get_text(' ',strip=True)
   out.append({'url':link,'context':context[:1600]})
  print(u,rr.status_code,len(out),flush=True)
 except Exception as e:print(e,flush=True)
(P/'research/author_pdf_links.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
# Local PDF DOI and title identity mapping, avoid unrelated books
hits=[]
for f in (P.parent/'Reconnection知识库').rglob('*.pdf'):
 if 'literature' not in str(f):continue
 try:
  d=fitz.open(f);text=' '.join(d[i].get_text() for i in range(min(2,len(d))));norm=re.sub('[^a-z0-9]','',text.lower())
  for r in C:
   title=re.sub('[^a-z0-9]','',r['title'].lower());doi=r['doi'].lower()
   if len(title)>30 and title in norm or doi and doi in text.lower():hits.append({'key':r['key'],'path':str(f)} )
 except:pass
(P/'research/local_matches.json').write_text(json.dumps(hits,ensure_ascii=False,indent=2));print('LOCAL',len(hits),flush=True)
