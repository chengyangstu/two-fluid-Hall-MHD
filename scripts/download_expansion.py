import ast,json,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parents[1]
s=(P/'scripts/download.py').read_text().split('\nout=[]')[0]
ns={'__file__':str(P/'scripts/download.py')};exec(compile(s,'download_defs','exec'),ns)
c=json.loads((P/'research/catalog.json').read_text())
# Separate result file so ongoing review state cannot be overwritten.
todo=[r for r in c if not r.get('local_pdf') and r['key'].startswith('E')];out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for r in ex.map(ns['worker'],todo):
  out.append(r);print(len(out),len(todo),r['key'],r['download_status'],flush=True)
  (P/'research/new_downloads.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('DONE',sum(bool(r.get('local_pdf')) for r in out),flush=True)
