# coding: utf-8
"""Merge explicitly recorded full reads; preserve the previous screening snapshot."""
from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parents[1]
W=P/'research/synthesis_continuation'
def read(p): return json.loads(p.read_text())
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
c=read(P/'research/catalog.json')
v=read(P/'research/reading_notes/verified.json')
by={r['key']:r for r in c}
new_records=[
 ('Yoo2013',2013,'Observation of Ion Acceleration and Heating during Collisionless Magnetic Reconnection in a Laboratory Plasma',
  ['Jongsoo Yoo','Masaaki Yamada','Hantao Ji','Clayton E. Myers'],'10.1103/PhysRevLett.110.215007','Physical Review Letters','实验／观测'),
 ('Ohia2012',2012,'Demonstration of Anisotropic Fluid Closure Capturing the Kinetic Structure of Magnetic Reconnection',
  ['O. Ohia','J. Egedal','V. S. Lukin','W. Daughton','A. Le'],'10.1103/PhysRevLett.109.115004','Physical Review Letters','待全文分类'),
 ('Ohia2015',2015,'Scaling laws for magnetic reconnection, set by regulation of the electron pressure anisotropy to the firehose threshold',
  ['O. Ohia','J. Egedal','V. S. Lukin','W. Daughton','A. Le'],'10.1002/2015GL067117','Geophysical Research Letters','待全文分类'),
 ('Jain2009',2009,'Electron scale structures in collisionless magnetic reconnection',
  ['Neeraj Jain','A. Surjalal Sharma'],'10.1063/1.3134045','Physics of Plasmas','待全文分类')
]
for key,year,title,authors,doi,journal,scope in new_records:
 if key in by: continue
 assert not any(r.get('doi','').lower()==doi.lower() for r in c),doi
 r=dict(key=key,id=key,title=title,authors=authors,year=year,doi=doi,journal=journal,
        source='全文参考文献追踪及出版社书目核对',scope=scope,
        selection='续筛发现的前序或实验连接文献；资格与内容以全文核读为准',
        read_status='未全文阅读',download_status='尚未取得匹配全文',local_pdf='',
        landing_urls=['https://doi.org/'+doi],arxiv='',urls=[])
 c.append(r);by[key]=r
downloads=read(W/'downloads.json')
for d in downloads:
 r=by[d['key']]
 if r.get('local_pdf') and r['local_pdf']!=d['local_pdf']:
  hist=r.setdefault('previous_versions',[])
  if not any(h['local_pdf']==r['local_pdf'] for h in hist):
   hist.append({k:r.get(k) for k in ['local_pdf','pages','sha256','download_url']})
 r.update(local_pdf=d['local_pdf'],pages=d['pages'],sha256=d['sha256'],
          download_url=d['url'],download_status='匹配全文及首页身份已人工核验')
notes=read(W/'notes/new_full_reads.json')
for k,n in notes.items():
 assert (P/by[k]['local_pdf']).is_file()
 v[k]=n;by[k]['read_status']=n['status'];by[k]['identity_checked']='首页题名、作者、版本及全文人工核对'
 by[k]['scope']={'F659':'动理学对照','F792':'动理学对照','F611':'混合模型／闭合对照','L213':'EMHD／观测对照','L272':'理论／动理学对照','Yoo2013':'实验／观测'}[k]
 write(W/'notes'/f'{k}_note.json',n)
# All 107 pre-existing priority titles/metadata were reviewed in this continuation.
oldv=read(W/'before/research/reading_notes/verified.json')
oldc=read(W/'before/research/catalog.json');oldby={r['key']:r for r in oldc}
screen=read(P/'research/remaining_screen/screening.json')['records']
priority=[s for s in screen if s['route'].startswith('优先') and s['key'] not in oldv and not oldby[s['key']].get('duplicate_of') and oldby[s['key']].get('eligibility')!='排除']
assert len(priority)==107
next_queue={
 'L181':'与有限长X线PIC对照的直接Hall模型；需先取得全文。',
 'E461':'电子独有重联的EMHD撕裂渐近理论，补充线性分支边界。',
 'E466':'与E461相连的数值本征与实验参数检验。',
 'F578':'新β标度候选；需核读排序、扫描路径与适用范围。',
 'F760':'电子温度各向异性与强导场撕裂，连接状态方程与启动。',
 'E550':'磁尾电子层结状结构观测候选；核查三维重建及模型适用性。',
 'F771':'三维混合Vlasov电子独有重联及离子加热，检验二维外推。',
 'F629':'KH诱导重联模型比较，检验闭合与驱动可移植性。',
 'F759':'高率与弱离子出流关系，核查归一化与F741比较。',
 'L231':'EMHD撕裂/保面模区分，避免将所有不稳定性都当作断线。',
 'F732':'导引场电子压力实验检验；优先寻找公开全文。',
 'L306':'实验电子独有重联的Hall磁场候选；补充多尺度诊断。'}
rescreen=[]
for s in priority:
 k=s['key'];r=by[k]
 rescreen.append(dict(key=k,title=r['title'],year=r['year'],
  screening_level='题名、已有书目与前序初筛理由复核；未读正文者不作内容结论',
  route='本次完成全文核读' if k in notes else ('下一批重点' if k in next_queue else '保留原优先队列'),
  reason=notes[k]['assessment'] if k in notes else next_queue.get(k,'本次未取得足以改变原优先级的全文证据；保留，不据题名排除。'),
  local_pdf=r.get('local_pdf',''),full_read=k in v))
write(W/'priority_rescreen.json',{'date':'2026-11-11','baseline_priority':107,'records':rescreen})
added_screen=[]
for k,reason in [('Yoo2013','从L272回引直接测量，核验面内电场加速和下游升温。'),
 ('Ohia2012','F611引用的直接双流体各向异性闭合前序论文，需核读后才能评价。'),
 ('Ohia2015','F611引用的各向异性饱和与电子加热标度前序论文，待全文核验。'),
 ('Jain2009','L213所依赖的EMHD数值与嵌套四极前序论文，补齐方法细节。')]:
  added_screen.append(dict(key=k,title=by[k]['title'],year=by[k]['year'],screening_level='参考文献追踪与书目核对',
     route='优先获取或核读',reason=reason,local_pdf=by[k].get('local_pdf',''),full_read=k in v))
write(W/'added_screening.json',{'records':added_screen})
write(P/'research/catalog.json',c);write(P/'research/reading_notes/verified.json',v)
write(W/'progress.json',{'date':'2026-11-11','baseline_full_reads':116,'new_full_reads':list(notes),
 'new_full_read_count':len(notes),'new_primary_version_physical_pages':58,
 'total_full_reads':len(v),'priority_titles_rescreened':107,'new_catalog_records':[a[0] for a in new_records],
 'new_downloads':[d['local_pdf'] for d in downloads],
 'reading_boundary':'正文、方法、结果、讨论、文内附录（本批均无）和参考文献；关键图表直接核验；引用的前序方法未取得者明确保留缺口。',
 'not_completed':'未完成全部候选的全文资格筛选和阅读；新增Ohia2012、Ohia2015、Jain2009仅书目追踪，未作为结论证据。'})
print('merged',len(notes),'new full reads; total',len(v),'catalog',len(c))
