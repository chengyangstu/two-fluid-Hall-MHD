# coding: utf-8
"""Merge only manually read papers; preserve the 101-paper delivery and versions."""
import json, hashlib, shutil
from pathlib import Path
import fitz
P=Path(__file__).resolve().parents[1]
B=P/'research/remaining_screen'
backup=B/'before_update'
backup.mkdir(exist_ok=True)
for rel in ['main.pdf','main.tex','README.md','research/catalog.json','research/reading_notes/verified.json']:
    target=backup/rel.replace('/','__')
    if not target.exists(): shutil.copy2(P/rel,target)
c=json.loads((P/'research/catalog.json').read_text())
v=json.loads((P/'research/reading_notes/verified.json').read_text())
by={r['key']:r for r in c}
notes={f.name.split('_')[0]:json.loads(f.read_text()) for f in sorted((B/'notes').glob('*_note.json'))}
assert len(notes)==15
n=notes['L314']
n['limitation']=n['limitation'].replace('图12极小de在固定真实质量比下对应超出低β排序；必须限定可信区间。','图11/12轴标签写de²，图注却写de且行列方向相反，参数解释不唯一；若按极小de且固定真实质量比理解，会超出低β排序。未经原始输入澄清不作定量跨区间比较。')
(B/'notes/L314_note.json').write_text(json.dumps(n,ensure_ascii=False,indent=2))
changes=[]
for key in ['F802','F803']:
    r=by[key]
    if not r.get('duplicate_of'):
        changes.append({'key':key,'operation':'merge_version','canonical':'E473','evidence':'相同题名、六位作者、研究摘要与出版链；arXiv:2502.10219v1、CPC DOI、SSRN5201132；未把不同版本计成独立研究。'})
    r['duplicate_of']='E473'
    r['duplicate_evidence']='2026-11-11核对作者、题名、arXiv及CPC/SSRN出版入口；同一GREENY代码论文的版本，内容修改未全部逐项核实。'
e=by['E473']
e['doi']='10.1016/j.cpc.2025.109807'
e['journal']='Computer Physics Communications'
e['arxiv']='2502.10219'
e['volume']='316';e['article_number']='109807'
e['read_version']='arXiv:2502.10219v1 (2025-02-14); journal revision not fully read'
for key,arxiv in {'L314':'2603.06234','F589':'2203.14268','F600':'2604.18787','F606':'2507.11904','F625':'1303.0442','F655':'2605.11139','F703':'2412.02556','F788':'2406.08951'}.items(): by[key]['arxiv']=arxiv
r=by['F788']
if r['local_pdf']!='papers/F788_published.pdf':
    r.setdefault('version_history',[]).append({k:r.get(k) for k in ['local_pdf','pages','sha256','download_url']})
r['local_pdf']='papers/F788_published.pdf'
r['download_url']=(B/'F788_download_url.txt').read_text().strip()
r['pages']=len(fitz.open(P/r['local_pdf']))
r['sha256']=hashlib.sha256((P/r['local_pdf']).read_bytes()).hexdigest()
r['read_version']='Published JFM 1007, A4 (2025), 10 pages; earlier arXiv version also read'
r['authors']=['García Morillo, José María','Alexandros Alexakis']
for key,n in notes.items():
    assert by[key].get('local_pdf')
    assert all(n.get(k) for k in ['pages_read','figures_checked','model','parameters','finding','limitation','assessment','status'])
    n['status']='全文及关键图表已核读'
    v[key]=n
    by[key]['read_status']=n['status']
    by[key]['selection']='剩余候选全面题名筛查后的重点全文核读'
    by[key]['read_batch']='remaining_screen_2026-11-11'
    if key in ['L190','L227','F703']: by[key]['scope']='实验／空间观测对照'
    elif key in ['F589','F606','F741','F788']: by[key]['scope']='理论／动力学或MHD对照，非独立Hall模拟'
    elif key=='L283': by[key]['scope']='扩展边界：尘埃三物种PIC对照'
    elif key in ['F625','F655']: by[key]['scope']='混合动力学／流体电子对照'
    else: by[key]['scope']='Hall／扩展MHD／双流体／gyrofluid模拟与理论'
(P/'research/catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2))
(P/'research/reading_notes/verified.json').write_text(json.dumps(v,ensure_ascii=False,indent=2))
if changes:(B/'version_corrections.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
screen=json.loads((B/'screening.json').read_text())
# Preserve initial screening as a dated snapshot; separately publish current follow-up.
unique=[r for r in c if not r.get('duplicate_of') and r.get('eligibility')!='排除']
summary={'date':'2026-11-11','baseline_remaining':698,'screened_at_title_metadata_level':698,
 'new_full_reads':list(notes),'new_full_read_count':len(notes),'total_full_reads':len(v),
 'newly_merged_version_records':['F802','F803'],'remaining_candidates':sum(r['key'] not in v for r in unique),
 'new_downloads':['papers/F788_published.pdf'],
 'reading_scope':'正文、方法、结果、讨论、参考文献与文内适用附录；独立补充材料未取得时在逐篇档案明示。',
 'not_completed':'未完成所有剩余候选的全文资格判定、下载和阅读。'}
(B/'progress.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
