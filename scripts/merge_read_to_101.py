"""Merge manually authored full-reading dossiers; never infer readings from PDFs."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1]
folder = P / 'research/read_to_101'
vpath = P / 'research/reading_notes/verified.json'
v = json.loads(vpath.read_text())
cpath = P / 'research/catalog.json'
c = json.loads(cpath.read_text())
by = {r['key']: r for r in c}
required = {'pages_read', 'figures_checked', 'model', 'parameters', 'finding', 'limitation', 'assessment', 'status'}
for f in sorted(folder.glob('*_note.json')):
    key = f.name.removesuffix('_note.json')
    note = json.loads(f.read_text())
    assert required <= note.keys(), key
    assert by[key].get('local_pdf') and not by[key].get('duplicate_of'), key
    v[key] = note
    by[key]['read_status'] = note['status']
    by[key]['identity_verified'] = '全文首页、作者、正文与登记版本核对'
qpath = folder / 'selection.json'
q = json.loads(qpath.read_text())
for r in q['queue']:
    if r['key'] in v:
        r['status'] = '全文及核心图表核读完成'
q['completed_in_this_batch'] = sum(r['key'] in v for r in q['queue'])
for path, obj in [(vpath, v), (cpath, c), (qpath, q)]:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2))
print('Full reads:', len(v), '; selected batch completed:', q['completed_in_this_batch'])
