import json,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parents[1]
s=(P/'scripts/download.py').read_text().split('\nout=[]')[0]
ns={'__file__':str(P/'scripts/download.py')};exec(compile(s,'download_defs','exec'),ns)
c=json.loads((P/'research/catalog.json').read_text());keys=json.loads((P/'research/full_search_download_keys.json').read_text())
todo=[r for r in c if r['key'] in keys and not r.get('local_pdf')];out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for r in ex.map(ns['worker'],todo):
  out.append(r);print(len(out),len(todo),r['key'],r['download_status'],flush=True)
  (P/'research/full_search_downloads.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('DONE',sum(bool(r.get('local_pdf')) for r in out),flush=True)
