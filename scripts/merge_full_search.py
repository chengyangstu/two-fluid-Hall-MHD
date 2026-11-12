# coding: utf-8
import json,re,unicodedata
from pathlib import Path
P=Path(__file__).resolve().parents[1]
f=P/'research/catalog.json';c=json.loads(f.read_text())
raw=json.loads((P/'research/full_openalex.json').read_text())
def norm(t):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',t or '').encode('ascii','ignore').decode().lower())
def doi(d):return (d or '').lower().replace('https://doi.org/','')
def abstract(x):return ' '.join(w for i,w in sorted((i,w) for w,inds in (x.get('abstract_inverted_index') or {}).items() for i in inds))
added=[];changed=[];matches=0
for x in raw:
 t=x.get('title') or '';a=abstract(x)
 if not(re.search('reconnect|tearing',t,re.I) and re.search('hall|two.fluid|ten.moment|five.moment|electron inertia|electron magnetohydrodynamic|closure|gyrofluid',t+' '+a,re.I)):continue
 if x.get('type') not in ['article','preprint','dissertation','book-chapter','review']:continue
 if x.get('publication_date','')>'2026-11-10':continue
 d=doi(x.get('doi'));nt=norm(t)
 match=next((r for r in c if (d and d==r.get('doi')) or x['id']==r.get('openalex') or (nt==norm(r['title']) and not(d and r.get('doi') and d!=r['doi']))),None)
 urls=[l['pdf_url'] for l in x.get('locations',[]) if l.get('pdf_url')]
 lands=[l['landing_page_url'] for l in x.get('locations',[]) if l.get('landing_page_url')]
 if match:
  matches+=1
  if not match.get('local_pdf') and set(urls)-set(match.get('urls',[])):changed.append(match['key'])
  match['urls']=list(dict.fromkeys(match.get('urls',[])+urls));match['landing_urls']=list(dict.fromkeys(match.get('landing_urls',[])+lands));continue
 i=len(c)+1
 r=dict(id=f'H{i:03d}',key=f'F{i:03d}',title=t,authors=[a['author']['display_name'] for a in x.get('authorships',[])],year=x.get('publication_year'),date=x.get('publication_date',''),doi=d,abstract=a,journal=((x.get('primary_location') or {}).get('source') or {}).get('display_name',''),urls=urls,landing_urls=lands,openalex=x['id'],source='OpenAlex complete-page full search',cited_by=x.get('cited_by_count',0),type=x.get('type'),arxiv='',selection='全文检索增补候选，待相关性筛选',scope='待全文分类',read_status='未全文阅读',download_status='待下载',local_pdf='',pages=0)
 c.append(r);added.append(r['key'])
f.write_text(json.dumps(c,ensure_ascii=False,indent=2))
(P/'research/full_search_download_keys.json').write_text(json.dumps(list(dict.fromkeys(added+changed))))
print('raw unique',len(raw),'added',len(added),'new links',len(changed),'total',len(c))
