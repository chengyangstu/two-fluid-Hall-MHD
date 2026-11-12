"""Remove transient signed URL credentials from public search metadata, with an audit."""
from pathlib import Path
import json,gzip,hashlib
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
def scrub(value,changes,path=''):
 if isinstance(value,dict):return {k:scrub(v,changes,path+'/'+k) for k,v in value.items()}
 if isinstance(value,list):return [scrub(v,changes,path+'/'+str(i)) for i,v in enumerate(value)]
 if isinstance(value,str) and value.startswith(('https://','http://')):
  u=urlsplit(value);params=parse_qsl(u.query,keep_blank_values=True)
  sensitive=lambda k:k.lower().startswith('x-amz-') or k.lower() in {'awsaccesskeyid','signature','access_token','token','credential','password','secret','session'}
  removed=[k for k,v in params if sensitive(k)]
  if removed:
   changes.append({'field':path,'host':u.hostname,'removed_query_keys':removed,
    'original_url_sha256':hashlib.sha256(value.encode()).hexdigest(),
    'note':'Temporary signed-URL authentication removed; DOI/landing metadata retained. Unsigned PDF endpoint is not asserted accessible.'})
   return urlunsplit((u.scheme,u.netloc,u.path,urlencode([(k,v) for k,v in params if not sensitive(k)]),u.fragment))
 return value
if __name__=='__main__':
 p=Path(__file__).resolve().parents[1]/'specific problems/离子加热问题/search'
 f=p/'openalex_works.json.gz';before=hashlib.sha256(f.read_bytes()).hexdigest()
 with gzip.open(f,'rt',encoding='utf-8') as stream:data=json.load(stream)
 changes=[];clean=scrub(data,changes)
 if changes:
  with gzip.open(f,'wt',encoding='utf-8') as stream:json.dump(clean,stream,ensure_ascii=False)
  record={'date':'2026-11-12','archive_sha256_before':before,'archive_sha256_after':hashlib.sha256(f.read_bytes()).hexdigest(),
   'changes':changes,'policy':'Publication hygiene only; bibliographic and scientific metadata not altered.'}
  (p/'publication_cleanup.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Transient signed URL occurrences cleaned:',len(changes))
