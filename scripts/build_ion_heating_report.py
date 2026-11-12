"""Generate the heating report's evidence index/bibliography, then compile."""
from pathlib import Path
import json,re,csv,subprocess,shutil,hashlib
P=Path(__file__).resolve().parents[1];T=P/'specific problems/离子加热问题';Q=P/'research/ion_heating'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
c={r['key']:r for r in read(P/'research/catalog.json')};v=read(P/'research/reading_notes/verified.json')
b=read(T/'batch_manifest.json'); records={r['key']:r for r in b['records']}
def tex(s):
 d={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
 return ''.join(d.get(x,x) for x in str(s))
source=(T/'report.tex').read_text(encoding='utf-8')
keys=list(dict.fromkeys(k for group in re.findall(r'\\cite\w*\{([^}]+)\}',source) for k in group.split(',')))
assert set(keys)<=set(v),sorted(set(keys)-set(v))
(T/'batch_stats.tex').write_text(
 f'本轮新增全文核读{b["new_full_reads"]}篇，新增核读主版本共{b["new_full_read_main_version_pages"]}个PDF物理页；\\\\[5pt]\n'
 f'三分支完整重读{b["rechecked_full_reads"]}篇，另由主代理重读F635；新增{len(b["new_pdf_files"])}个原文PDF（含版本）。\\\\[5pt]\n'
 f'全仓库全文核读由{b["baseline_full_reads"]}增至{b["current_full_reads"]}篇。\n',encoding='utf-8')
lines=['本附录按正文首次引用排序。所有引文均已列入全库核读档案；本轮未重新通读的旧证据明确标识。点击本地PDF需保持完整目录结构。详细阅读笔记含方法、参数、图式、限制及未取得材料。\n']
bib=[];matrix=[]
for k in keys:
 r=c[k];rec=records.get(k);version=r.get('heating_review_version','原库登记版本')
 label='本轮新增全文核读' if rec and rec['new_full_read'] else '本轮完整重读' if rec or k=='F635' else '复用原库已核读档案，本轮未重新全文阅读'
 note=rec['note'] if rec else 'specific problems/离子加热问题/reading_notes/F635_note.json' if k=='F635' else 'research/reading_notes/verified.json'
 lines += [r'\paragraph{'+tex(k)+'（'+str(r['year'])+r'）}\label{paper:'+k+'}',
  tex(r['title'])+'。'+tex(label)+'；主版本'+str(r['pages'])+'个PDF物理页。',
  tex(version)+'。'+r'\href{run:../../'+r['local_pdf']+r'}{打开本地原文}。',
  r'笔记：\path{'+note.replace('specific problems/离子加热问题/','')+r'}。\par\smallskip']
 fields={'author':' and '.join(tex(a) for a in r['authors']), 'title':'{'+tex(r['title'])+'}',
 'year':r['year'],'journal':tex(r.get('journal','')),'doi':r.get('doi',''),
 'url':'https://doi.org/'+r['doi'] if r.get('doi') else next(iter(r.get('landing_urls',[])),''),
 'note':r'文献键：\texttt{'+tex(k)+r'}；\hyperref[paper:'+k+r']{版本与笔记}；\href{run:../../'+r['local_pdf']+r'}{本地PDF}'}
 bib.append('@article{'+k+',\n'+',\n'.join('  '+a+' = {'+str(z)+'}' for a,z in fields.items() if z)+'\n}\n')
 matrix.append({'key':k,'title':r['title'],'year':r['year'],'doi':r.get('doi',''),'model':v[k]['model'],
  'reading_status':label,'local_pdf':r['local_pdf'],'version':version,'pages':r['pages'],'finding':v[k]['finding'],
  'limitation':v[k]['limitation'],'locators':v[k]['figures_checked'],'note':note})
(T/'evidence_index.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(T/'references.bib').write_text('\n'.join(bib),encoding='utf-8')
with (T/'evidence_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(matrix[0]));w.writeheader();w.writerows(matrix)
for i,args in enumerate([['xelatex','-interaction=nonstopmode','-halt-on-error','report.tex'],['bibtex','report'],
 ['xelatex','-interaction=nonstopmode','-halt-on-error','report.tex'],['xelatex','-interaction=nonstopmode','-halt-on-error','report.tex']]):
 args[0]=shutil.which(args[0]) or args[0]
 with (Q/f'topic_build_{i}.log').open('w',encoding='utf-8') as f:r=subprocess.run(args,cwd=T,stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError(f'Topic build failed: research/ion_heating/topic_build_{i}.log')
print('Compiled',T/'report.pdf','cited verified works',len(keys))
