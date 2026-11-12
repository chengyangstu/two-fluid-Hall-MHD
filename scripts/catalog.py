import requests,json,re,unicodedata,csv,difflib,concurrent.futures
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
P=Path(__file__).resolve().parents[1]
s=requests.Session();s.mount('https://',HTTPAdapter(max_retries=Retry(total=2,backoff_factor=.5)))
O=json.loads((P/'research/openalex.json').read_text());A=json.loads((P/'research/arxiv.json').read_text())
def norm(t):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower())
def doi(d):return (d or '').lower().replace('https://doi.org/','').replace('http://dx.doi.org/','')
def abstract(x):
 z=x.get('abstract_inverted_index') or {}; items=[(i,w) for w,inds in z.items() for i in inds];return ' '.join(w for i,w in sorted(items))
def convert(x):return dict(title=x['title'],authors=[a['author']['display_name'] for a in x.get('authorships',[])],year=x['publication_year'],date=x.get('publication_date',''),doi=doi(x.get('doi')),abstract=abstract(x),journal=((x.get('primary_location') or {}).get('source') or {}).get('display_name',''),urls=[l['pdf_url'] for l in x.get('locations',[]) if l.get('pdf_url')],landing_urls=[l['landing_page_url'] for l in x.get('locations',[]) if l.get('landing_page_url')],openalex=x['id'],source='OpenAlex',cited_by=x.get('cited_by_count',0),type=x.get('type',''),arxiv='',queries=x.get('queries',[]))
seeds={
'Birn2001':'10.1029/1999JA900449','Biskamp1995':'10.1103/PhysRevLett.75.3850','Biskamp1997':'10.1063/1.872211','Shay2001':'10.1029/1999JA001007','Ma2001':'10.1029/1999JA001004','Otto2001':'10.1029/1999JA001005','BirnHesse2001':'10.1029/1999JA001001','Cassak2005':'10.1103/PhysRevLett.95.235002','Cassak2006':'10.1086/505690','Cassak2010':'10.1063/1.3435269','Cassak2008':'10.1029/2008GL035268','Huang2011':'10.1063/1.3606363','Baalrud2011':'10.1063/1.3633473','Huang2024':'10.1063/5.0216561','Wang2015':'10.1063/1.4906063','Ng2015':'10.1063/1.4935302','Ng2017':'10.1063/1.4993195','Ng2020':'10.1063/5.0012067','Closure2026':'10.1029/2026JA035250','Cassak2015':'10.1063/1.4908545','Knoll2006':'10.1103/PhysRevLett.96.135001','Sullivan2009':'10.1063/1.3251423','Huba2004':'10.1103/PhysRevLett.93.175003','Huba2002':'10.1063/1.1514970','HubaGuide2004':'10.1063/1.1834592','Ren2005':'10.1103/PhysRevLett.95.055003','Yamada2006':'10.1063/1.2203950','Yoo2018':'10.1038/s41467-018-07680-2','GuideExp2012':'10.1103/PhysRevLett.109.165002','Dorfman2008':'10.1063/1.2904600','Stanier2013':'10.1063/1.4830104','Andres2016':'10.1063/1.4942418','Andres2014':'10.1063/1.4890021','Simakov2008':'10.1103/PhysRevLett.101.105003','Malyshkin2008':'10.1103/PhysRevLett.101.225001','Malyshkin2009':'10.1103/PhysRevLett.103.235004','Sullivan2010':'10.1063/1.3518752','Shepherd2012':'10.1029/2012JA017867','Arnold2008':'10.1016/j.cpc.2007.11.018','Toth2008':'10.1016/j.jcp.2008.04.010','Hakim2008':'10.1007/s10894-007-9116-z','Rogers2001':'10.1103/PhysRevLett.87.195004','Ottaviani1993':'10.1103/PhysRevLett.71.3802','Grasso2001':'10.1103/PhysRevLett.86.5051','Shay2004':'10.1063/1.1705650','Cassak2007':'10.1063/1.2795630','Arshad2026':'10.1029/2026JA035547','Teh2026':'10.1029/2026JA035335','Huang2026':'10.1080/10420150.2025.2598789'}
# metadata from DOI endpoints; no guessed titles used as factual bibliography
bydoi={doi(x.get('doi')):x for x in O if x.get('doi')}
records=[]
for key,d in seeds.items():
 d=doi(d)
 if d in bydoi:r=convert(bydoi[d])
 else:
  f=P/'research/raw'/f'crossref_{key}.json'
  try:
   if f.exists():x=json.loads(f.read_text())
   else:
    resp=s.get('https://api.crossref.org/works/'+d,timeout=25);resp.raise_for_status();x=resp.json()['message'];f.write_text(json.dumps(x,ensure_ascii=False))
   r=dict(title=x['title'][0],authors=[' '.join([a.get('given',''),a.get('family','')]).strip() for a in x.get('author',[])],year=x.get('published',x.get('issued'))['date-parts'][0][0],doi=d,abstract=re.sub('<[^>]*>','',x.get('abstract','')),journal=(x.get('container-title') or [''])[0],urls=[z['URL'] for z in x.get('link',[]) if 'pdf' in z.get('content-type','')],landing_urls=['https://doi.org/'+d],source='Crossref',type='article',arxiv='',cited_by=0,date='')
  except Exception as e:print('SEED FAIL',key,d,str(e),flush=True);continue
 r['key']=key;r['selection']='核心／方法／比较证据';records.append(r)
# Include title-explicit literature; distinguish observations and adjacent models later
for x in O:
 t=x['title'] or ''; ab=abstract(x)
 direct=bool(re.search(r'reconnect|tearing',t,re.I) and re.search(r'hall|two.fluid|ten.moment|electron inertia|electron magnetohydrodynamic|closure|gyrofluid',t,re.I))
 model=bool(re.search(r'reconnect|tearing',t,re.I) and re.search(r'(hall.mhd|hall magnetohydrodynamic|two.fluid|ten.moment|electron magnetohydrodynamic|gyrofluid).{0,90}(simulat|model|equation)|(?:simulat|model|equation).{0,90}(hall.mhd|hall magnetohydrodynamic|two.fluid|ten.moment|electron magnetohydrodynamic|gyrofluid)',ab,re.I))
 if not(direct or model):continue
 if x.get('type') not in ('article','preprint','dissertation','book-chapter'):continue
 if not x.get('doi') and not any(l.get('pdf_url') for l in x.get('locations',[])):continue
 r=convert(x);r['selection']='题名直接相关' if direct else '摘要模型相关';records.append(r)
# arxiv add strict title plus methods and explicitly model simulation abstracts
for a in A:
 t=a['title'];ab=a['abstract']
 if not (re.search(r'reconnect|tearing',t,re.I) and re.search(r'Hall|two.fluid|ten.moment|electron inertia|EMHD|electron magnetohydrodynamic|closure|gyrofluid',t,re.I) or re.search(r'(solver|numerical method|Galerkin).*?(Hall|two.fluid)|(Hall|two.fluid).*?(solver|numerical method)',t,re.I)):continue
 if re.search('quantum.Hall|coronal rain|partially ionized|chromospher|stratified atmosphere',t,re.I):scope='邻近主题，需区分离子电子与离子中性双流体'
 else:scope='题名直接相关'
 records.append(dict(title=t,authors=a['authors'],year=int(a['date'][:4]),date=a['date'][:10],doi=doi(a['doi']),abstract=ab,journal=a['journal'] or 'arXiv preprint',urls=['https://arxiv.org/pdf/'+a['arxiv']],landing_urls=['https://arxiv.org/abs/'+a['arxiv']],source='arXiv',arxiv=a['arxiv'],type='preprint',selection=scope,cited_by=0))
# deduplicate titles and canonical DOIs, preserve core record
unique=[]
for r in records:
 match=next((u for u in unique if (r['doi'] and r['doi']==u['doi']) or norm(r['title'])==norm(u['title']) or difflib.SequenceMatcher(None,norm(r['title']),norm(u['title'])).ratio()>.965),None)
 if match:
  match['urls']=list(dict.fromkeys(match['urls']+r['urls']));match['landing_urls']=list(dict.fromkeys(match['landing_urls']+r['landing_urls']))
  if not match.get('abstract'):match['abstract']=r['abstract']
  if not match.get('arxiv'):match['arxiv']=r.get('arxiv','')
 else:unique.append(r)
# identify arxiv variants against full A, even where paper title does not contain model
for r in unique:
 for a in A:
  if (r['doi'] and doi(a['doi'])==r['doi']) or difflib.SequenceMatcher(None,norm(r['title']),norm(a['title'])).ratio()>.94:
   r['arxiv']=a['arxiv'];r['urls'].insert(0,'https://arxiv.org/pdf/'+a['arxiv']);r['abstract']=r['abstract'] or a['abstract'];break
for i,r in enumerate(sorted(unique,key=lambda r:(r['year'],r['title']))):
 r.setdefault('key',f'L{i+1:03d}');r['id']=f'H{i+1:03d}';r['urls']=list(dict.fromkeys(r['urls']))
 t=r['title'].lower();ab=r['abstract'].lower()
 r['scope']='实验／观测' if re.search(r'experiment|laboratory|observation|measurement|geotail|cluster|mms|themis',t) else '模拟／理论／方法'
 if re.search(r'chromospher|partially ionized|stratified atmosphere|dusty|relativistic|pair plasma',t):r['scope']='扩展边界：中性／多组分／相对论／对等离子体'
 if r['doi'].startswith('10.5194/egusphere-egu') or r['type']=='dissertation':r['scope']='会议摘要／学位论文，证据单列'
 r['read_status']='摘要待核' if r['abstract'] else '仅元数据，待取得摘要／全文'
unique.sort(key=lambda r:r['id'])
(P/'research/catalog.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2))
with (P/'research/all_candidates.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['source','id','year','title','doi','selected'])
 for x in O:w.writerow(['OpenAlex',x['id'],x['publication_year'],x['title'],x.get('doi'),any(norm(x['title'] or '')==norm(r['title']) for r in unique)])
 for a in A:w.writerow(['arXiv',a['arxiv'],a['date'][:4],a['title'],a['doi'],any(a['arxiv']==r.get('arxiv') for r in unique)])
print('CATALOG',len(unique),flush=True)
for r in unique:
 if not r['key'].startswith('L'):print(r['key'],r['title'],r['doi'],flush=True)
