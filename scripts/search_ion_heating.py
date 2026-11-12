# coding: utf-8
"""Reproducible topic search and one-hop seed citation harvest (metadata only)."""
import json, time, gzip
from pathlib import Path
import requests
from sanitize_heating_metadata import scrub

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'specific problems/离子加热问题/search'
OUT.mkdir(parents=True, exist_ok=True)
DATE = '2026-11-12'
SEEDS = {'Yoo2013':'10.1103/PhysRevLett.110.215007',
         'L272':'10.1063/5.0040374', 'E512':'10.1063/1.3628639'}
QUERIES = ['Hall MHD ion electron heating', 'two fluid reconnection heating',
           'two temperature Hall MHD', 'electron magnetohydrodynamic reconnection heating',
           'ten moment reconnection heating', 'Landau fluid reconnection heating',
           'gyrofluid reconnection heating', 'Hall reconnection energy partition',
           'two fluid local plasma heating', 'Hall MHD viscous Ohmic heating']
S = requests.Session()
S.headers['User-Agent'] = 'Hall-MHD-literature-research/1.0'
works, logs, edges = {}, [], []
publication_cleanup=[]

def save(name, data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def compact(w):
    return scrub({k:w.get(k) for k in ['id','doi','title','publication_year','publication_date',
        'type','authorships','primary_location','best_oa_location','open_access',
        'referenced_works','cited_by_count','abstract_inverted_index']},publication_cleanup,w.get('id',''))

def get(endpoint, params=None):
    r=S.get('https://api.openalex.org/works'+endpoint,params=params,timeout=45)
    r.raise_for_status()
    return r.json()

def harvest(label, params):
    page=1; seen=set(); count=None
    while True:
        try:
            data=get('',dict(params, page=page, **{'per-page':200}))
        except Exception as e:
            logs.append({'date':DATE,'label':label,'params':params,'page':page,'error':str(e),'complete':False})
            break
        batch=data.get('results',[]); count=data['meta']['count']
        for w in batch:
            works[w['id']]=compact(w); seen.add(w['id'])
        logs.append({'date':DATE,'label':label,'params':params,'page':page,'reported_count':count,
                     'returned':len(batch),'meta':data['meta']})
        if len(batch)<200 or page*200>=count: break
        page+=1; time.sleep(.1)
    return sorted(seen), count

seed_records={}
for key,doi in SEEDS.items():
    try:
        seed=get('/https://doi.org/'+doi); sid=seed['id']; works[sid]=compact(seed)
        refs=seed.get('referenced_works',[])
        # Fetch reference metadata in OR batches, preserving explicit graph direction.
        for start in range(0,len(refs),40):
            ids='|'.join(x.rsplit('/',1)[-1] for x in refs[start:start+40])
            harvest(key+':references',{'filter':'openalex_id:'+ids})
        cited,count=harvest(key+':cited_by',{'filter':f'cites:{sid.rsplit("/",1)[-1]},to_publication_date:{DATE}'})
        edges.extend({'from':sid,'to':rid,'basis':'OpenAlex referenced_works','seed':key} for rid in refs)
        edges.extend({'from':rid,'to':sid,'basis':'OpenAlex cites filter','seed':key} for rid in cited)
        seed_records[key]={'id':sid,'doi':doi,'reference_count':len(refs),
                           'citing_reported':count,'citing_retrieved':len(cited)}
        print(key,seed_records[key],flush=True)
    except Exception as e:
        logs.append({'date':DATE,'label':key,'error':str(e),'complete':False})
    save('openalex_progress.json',{'seeds':seed_records,'logs':logs})

query_matches={}
for q in QUERIES:
    ids,count=harvest(q,{'search':q,'filter':f'to_publication_date:{DATE}'})
    query_matches[q]={'reported_count':count,'retrieved':len(ids),'ids':ids}
    print(q,len(ids),count,flush=True)
    save('openalex_progress.json',{'seeds':seed_records,'logs':logs})

with gzip.open(OUT/'openalex_works.json.gz','wt',encoding='utf-8') as f:
    json.dump(list(works.values()),f,ensure_ascii=False)
save('citation_edges.json',edges)
save('publication_cleanup_search.json',{'date':DATE,'changes':publication_cleanup})
save('openalex_search.json',{'date':DATE,'database':'OpenAlex','seeds':seed_records,
    'queries':query_matches,'logs':logs,'unique_works':len(works),
    'boundary':'One-hop database citations plus keyword queries. Metadata is not full-text verification; database coverage and missing references remain limitations.'})
print('unique',len(works),'edges',len(edges),flush=True)
