# coding: utf-8
import json,re,csv,html,unicodedata
from pathlib import Path
P=Path(__file__).resolve().parents[1]
c=json.loads((P/'research/catalog.json').read_text())
v=json.loads((P/'research/reading_notes/verified.json').read_text())
screen_path=P/'research/remaining_screen/screening.json'
screened={r['key']:r for r in json.loads(screen_path.read_text())['records']} if screen_path.exists() else {}
current={f.name.removesuffix('_note.json') for f in (P/'research/remaining_screen/notes').glob('*_note.json')}
def tex(s):
 d={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
 out=''.join(d.get(x,x) for x in str(s)).replace('−','-').replace('′',"'").replace('″',"''").replace(',', ', ').replace(';', '; ')
 # Preserve exponent semantics without relying on rare Unicode font glyphs.
 out=re.sub('[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ᵀ]+',lambda m:r'\textsuperscript{'+unicodedata.normalize('NFKC',m.group()).replace('−','-')+'}',out)
 out=re.sub('[₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎]+',lambda m:r'\textsubscript{'+unicodedata.normalize('NFKC',m.group()).replace('−','-')+'}',out)
 for char,cmd in {'∇':'nabla','∈':'in','∝':'propto','∫':'int','≪':'ll','≫':'gg','≲':'lesssim','≳':'gtrsim'}.items():
  out=out.replace(char,r'\ensuremath{'+chr(92)+cmd+'}')
 return out
def link(r):
 if r.get('doi'):return 'https://doi.org/'+r['doi']
 if r.get('arxiv'):return 'https://arxiv.org/abs/'+r['arxiv']
 return next(iter(r.get('landing_urls',[])), '')
for r in c:
 if r['key'] in v:r['read_status']=v[r['key']]['status']
 if r.get('duplicate_of'):r['read_status']='版本重复，见 '+r['duplicate_of']
 if r.get('eligibility')=='排除':r['read_status']='排除：'+r['exclusion_reason']
(P/'research/catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2))
unique=[r for r in c if not r.get('duplicate_of') and r.get('eligibility')!='排除']
npdf=sum(bool(r.get('local_pdf')) for r in unique)
(P/'sections/stats.tex').write_text(
 r'\textbf{持续核读工作稿，不代表全量调研已完成。}\\[5pt]'+'\n'+
 f'原始候选登记{len(c)}条；非重复且非排除记录{len(unique)}条；其中{npdf}条已关联可解析PDF（未全部人工核验）。'+r'\\[5pt]'+'\n'+
 f'完成全文与关键图表核读{len(v)}篇；其余条目不作为本文研究结论的证据。\n')
bib=[]
for r in c:
 fields={'author':' and '.join(tex(a) for a in r.get('authors',[])) or 'Unknown',
 'title':'{'+tex(r['title'])+'}','year':r.get('year',''),
 'journal':tex(r.get('journal') or r.get('source','')), 'url':link(r)}
 if r.get('doi'):fields['doi']=r['doi']
 if r.get('arxiv'):fields['eprint']=r['arxiv']
 if r['key'] in v:
  fields['note']=r'文献键：\texttt{'+tex(r['key'])+r'}；\hyperref[paper:'+r['key']+r']{全文核读档案}'
  if r.get('local_pdf'):fields['note']+=r'；\href{run:'+r['local_pdf']+r'}{本地PDF}'
 bib.append('@article{'+r['key']+',\n'+',\n'.join('  '+k+' = {'+str(z)+'}' for k,z in fields.items() if z)+'\n}\n')
(P/'references.bib').write_text('\n'.join(bib))
lines=[r'\chapter{逐篇核读档案与全量候选索引}\label{ch:catalog}',
 '本章前半部分是已完成正文与关键图表核对的文献档案；后半部分是尚未完成核读或待进一步筛选的候选目录。待核目录的题名、年份与链接是检索信息，不等于对其方法、发现或相关性的确认。',
 r'\section{如何反查本地原文}',
 r'文献键是稳定检索标识。各档案提供本地PDF链接、DOI或版本入口和页码。PDF阅读器可能限制相对文件链接，可直接在项目的 papers 文件夹打开对应文件；完整路径及全部状态也在 paper\_index.html 和 paper\_index.csv 中。']
bykey={r['key']:r for r in c}
labels=[('model','实际模型'),('parameters','计算／实验细节'),('finding','核实的发现'),('limitation','限制与未完成问题'),('assessment','本报告判断')]
for key,n in sorted(v.items(),key=lambda kv:(bykey[kv[0]].get('year',0),kv[0])):
 r=bykey[key]
 lines += [r'\section{'+tex(key)+'：'+tex(r.get('year',''))+r'年}\label{paper:'+key+'}',
 r'\textbf{'+tex(r['title'])+r'}\citep{'+key+'}\\',
 tex('; '.join(r.get('authors',[])))+'.',
 r'\textsf{核读范围：}'+tex(n['pages_read'])+r'；\textsf{图表：}'+tex(n['figures_checked'])+'.']
 if r.get('local_pdf'):lines.append(r'\href{run:'+r['local_pdf']+r'}{打开本地PDF：\texttt{'+tex(r['local_pdf'])+'}}'+r'\quad\href{'+link(r)+'}{DOI／版本入口}')
 for field,label in labels:lines.append(r'\paragraph{'+label+'}'+tex(n[field]))
lines += [r'\Needspace{10\baselineskip}',r'\section{未完成核读的候选：不据此作内容结论}',
 r'\small\begin{longtable}{P{24mm}P{97mm}P{27mm}}',
 r'\toprule 文献键／年份 & 题名与原始入口 & 当前状态\\\midrule\endfirsthead',
 r'\toprule 文献键／年份 & 题名与原始入口 & 当前状态\\\midrule\endhead']
for r in sorted(c,key=lambda r:(r.get('year',0),r['title'])):
 if r['key'] in v:continue
 status='有PDF，待核读' if r.get('local_pdf') else '未获匹配全文'
 if r.get('duplicate_of'):status='重复：'+r['duplicate_of']
 if r.get('eligibility')=='排除':status='排除：非论文'
 if r['key'] in ['E392','L196']:status='海报／幻灯片'
 title=tex(r['title']);url=link(r)
 if url:title=r'\href{'+url+'}{'+title+'}'
 lines.append(tex(r['key'])+' / '+str(r.get('year',''))+' & '+title+' & '+tex(status)+r'\\')
lines.append(r'\bottomrule\end{longtable}\normalsize')
(P/'sections/07_catalog.tex').write_text('\n\n'.join(lines))
fields=['key','year','title','authors','doi','arxiv','scope','read_status','download_status','local_pdf','duplicate_of','exclusion_reason','screening_level','screening_route','screening_reason','current_full_read_batch']
with (P/'paper_index.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in c:
  row={k:r.get(k,'') for k in fields};row['authors']='; '.join(r.get('authors',[]))
  sc=screened.get(r['key'],{})
  row.update(screening_level=sc.get('screening_level',''),screening_route=sc.get('route',''),screening_reason=sc.get('reason',''),current_full_read_batch='是' if r['key'] in current else '')
  w.writerow(row)
rows=[]
selection_path=P/'research/read_to_101/selection.json'
selected={r['key'] for r in json.loads(selection_path.read_text())['queue']} if selection_path.exists() else set()
for r in c:
 k=r['key'];note=v.get(k);local='<a href="'+html.escape(r['local_pdf'])+'">本地 PDF</a>' if r.get('local_pdf') else '未获匹配全文'
 nt=''
 if note:nt='<details><summary>阅读全文核读档案</summary><p><b>核读范围：</b>'+html.escape(note['pages_read'])+'</p><p><b>图表：</b>'+html.escape(note['figures_checked'])+'</p>'+''.join('<p><b>'+lab+'：</b>'+html.escape(note[fl])+'</p>' for fl,lab in labels)+'</details>'
 sc=screened.get(k)
 priority=bool(sc and sc.get('route','').startswith('优先') and not note and not r.get('duplicate_of') and r.get('eligibility')!='排除')
 if sc:nt+='<details class="screen"><summary>查看初筛理由（不等于全文结论）</summary><p>'+html.escape(sc['route'])+'：'+html.escape(sc['reason'])+'</p></details>'
 attrs={'read':bool(note),'selected':k in selected,'current':k in current,'screened':bool(sc),'priority':priority}
 rows.append('<tr '+ ' '.join('data-'+a+'="'+('1' if val else '0')+'"' for a,val in attrs.items())+'><td>'+html.escape(k)+'</td><td>'+str(r.get('year',''))+'</td><td><a href="'+html.escape(link(r))+'">'+html.escape(r['title'])+'</a>'+nt+'</td><td>'+local+'</td><td>'+html.escape(r['read_status'])+'</td></tr>')
page='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>Hall MHD与双流体重联文献索引</title>
<style>body{max-width:1400px;margin:40px auto;padding:0 24px;font:16px/1.65 system-ui;color:#17384a}h1{font-size:28px}input{padding:12px;width:90%;border:1px solid #abc;border-radius:5px}table{border-collapse:collapse;width:100%;margin-top:25px}td,th{padding:12px;text-align:left;border-bottom:1px solid #dce3e7;vertical-align:top}td:first-child{white-space:nowrap}a{color:#1c668a}details{font-size:14px;color:#304854}summary{cursor:pointer}thead{background:#eef4f6;position:sticky;top:0}</style>
<h1>Hall MHD 与双流体重联 · 文献索引</h1><p>持续核读工作稿；下载不等于读完。全文核读的文章有可展开的证据档案，其余不据摘要作结论。</p>
<label for="scope">阅读范围：</label><select id="scope" style="font:inherit;padding:8px;margin:0 0 14px 8px"><option value="all">全部登记</option><option value="read">已全文核读</option><option value="current">本轮续读15篇</option><option value="selected">上一轮精选39篇</option><option value="screened">本轮初筛698条</option><option value="priority">优先队列中仍未读</option></select>
<input id="q" placeholder="检索题名、年份、状态或要点；完整文献键优先精确匹配"><p id="count"></p><table><thead><tr><th>文献键</th><th>年份</th><th>题名与档案</th><th>全文</th><th>状态</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table><script>
const rows=[...document.querySelectorAll('tbody tr')];const keys=new Set(rows.map(r=>r.cells[0].textContent.toLowerCase()));function filter(){const q=document.querySelector('#q').value.trim().toLowerCase();const s=document.querySelector('#scope').value;const exactKey=keys.has(q);let n=0;rows.forEach(r=>{const matches=exactKey?r.cells[0].textContent.toLowerCase()===q:r.textContent.toLowerCase().includes(q);const ok=matches&&(s==='all'||r.dataset[s]==='1');r.hidden=!ok;if(ok)n++});document.querySelector('#count').textContent=`显示 ${n} / ${rows.length} 条登记记录`;}document.querySelector('#q').addEventListener('input',filter);document.querySelector('#scope').addEventListener('change',filter);filter();</script></html>'''
(P/'paper_index.html').write_text(page)
print('records',len(c),'unique candidates',len(unique),'matching PDFs',npdf,'full read',len(v))
