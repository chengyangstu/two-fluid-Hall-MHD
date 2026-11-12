# coding: utf-8
"""Build three independently numbered volumes, preserving source provenance."""
from pathlib import Path
import re, json, hashlib, subprocess, shutil

P=Path(__file__).resolve().parents[1]
O=P/'分卷';O.mkdir(exist_ok=True)
QA=P/'research/split_reports';QA.mkdir(parents=True,exist_ok=True)
ids=['01_theory_numerics','02_paper_results','03_solved_open']
titles=['理论与数值基础','不同文章的结果','已解决与未解决的问题']
short=['基础卷','结果卷','问题卷']
provenance={}
full_read_count=len(json.loads((P/'research/reading_notes/verified.json').read_text()))

def flatten(path):
    p=P/path
    provenance[str(path)]=hashlib.sha256(p.read_bytes()).hexdigest()
    return re.sub(r'\\input\{([^}]+)\}',lambda m:flatten(m[1]+'.tex'),p.read_text())

def join(paths):return '\n\n'.join(flatten('sections/'+x+'.tex') for x in paths)

core=flatten('sections/08_core_guide.tex')
start=core.index(r'\section{最核心的方程是什么}')
cut=core.index(r'\section{实验看到了什么')
end=core.index(r'\paragraph{如何回到详细学习。}')
guide=(r'\chapter{核心方程、模型变种与实现导航}\label{ch:core-guide}'+'\n'
       '本章把本卷第1章推导和第2章算法压缩成可反复查阅的总览。实验依据在《不同文章的结果》，适用条件及逐文献问题总结在《已解决与未解决的问题》。\n'
       +core[start:cut])
summary=(r'\chapter{实验依据、适用条件与已解决和未解决的问题}\label{ch:summary}'+'\n'
         '本章先汇总实验依据与模型适用条件，再把每项已解决结果和未决问题对应到具体论文。完整方程和算法见《理论与数值基础》，逐篇核读档案见《不同文章的结果》。后半卷进一步展开模型边界与研究设计。\n'
         +core[cut:end])
bodies=[
 join(['01_models','02_numerics','02_synthesis_numerics'])+'\n'+guide,
 join(['03_findings','05_experiments','05_selected_experiments','05_remaining_experiments',
       '05_synthesis_experiments','06_search','07_catalog']),
 summary+'\n'+join(['04_open','04_selected_open','04_remaining_open','04_synthesis_open'])
]

# Every scientific section in the compiled master is assigned exactly once.
master_labels=set(re.findall(r'\\label\{([^}]+)\}',flatten('main.tex')))
ownership={}
for vol,body in enumerate(bodies):
    for key in re.findall(r'\\label\{([^}]+)\}',body):
        assert key not in ownership,('duplicate label',key)
        ownership[key]=vol
assert not master_labels-set(ownership),('unassigned labels',master_labels-set(ownership))
oldchap={1:(0,1),2:(0,2),3:(1,1),4:(2,2),5:(1,2),6:(1,3),7:(1,4),8:(0,3)}
cn={v:i for i,v in enumerate('零一二三四五六七八九')}
link_counts=[0,0,0]

def transform(s,vol):
    s=s.replace('第1、2章',('第1、2章' if vol==0 else '《理论与数值基础》第1、2章'))
    def chapter(m):
        n=cn[m[1]] if m[1] in cn else int(m[1])
        target,num=oldchap[n]
        tail=m[2] or ''
        prefix='' if target==vol else '《'+titles[target]+'》'
        return prefix+'第'+str(num)+tail+m[3]
    # Apply only to source prose, before introducing new cross-volume refs.
    s=re.sub(r'第([1-8一二三四五六七八])((?:\.\d+)*)(章|节)',chapter,s)
    def ref(m):
        kind,key=m[1],m[2]
        if key not in ownership:raise ValueError('unknown reference '+key)
        target=ownership[key]
        if target==vol:return m[0]
        link_counts[vol]+=1
        return short[target]+r'~\@REF@'+kind+'{V'+str(target+1)+'-'+key+'}'
    s=re.sub(r'\\(eqref|pageref|ref)\{([^}]+)\}',ref,s)
    # Mark the destination volume without ambiguous local chapter numbers.
    for dest in range(3):
        prefix='《'+titles[dest]+'》'
        s=s.replace('第'+short[dest]+r'~\@REF@ref',prefix+r'第\@REF@ref')
        s=s.replace('式'+short[dest]+r'~\@REF@eqref',prefix+r'式\@REF@eqref')
        s=s.replace(prefix+'第1章'+prefix+'第',prefix+'第')
        s=s.replace(prefix+'第1章'+prefix+'式',prefix+'式')
    s=s.replace(r'\@REF@', '\\')
    def hyper(m):
        key=m[1]
        if key not in ownership:raise ValueError('unknown hyperref '+key)
        target=ownership[key]
        if target==vol:return m[0]
        link_counts[vol]+=1
        return r'\hyperref[V'+str(target+1)+'-'+key+']'
    s=re.sub(r'\\hyperref\[([^]]+)\]',hyper,s)
    s=s.replace(r'\href{run:papers/',r'\href{run:../papers/')
    s=s.replace('本报告《','《')
    return s

base=(P/'preamble.tex').read_text()
(O/'preamble.tex').write_text(base)
frontnotes=[
 '本卷保留全部模型推导、完整离子/电子方程、双流体到Hall MHD的约化、数值方法与参数细节；所有详细推导集中在第1章。第3章可先读，用于把核心方程和实现流程对应起来。',
 f'本卷先按七条问题线串联论文结果，再给实验对照、检索边界及{full_read_count}篇逐篇全文核读档案。未核读候选单列，不作为研究结论证据。',
 '本卷逐项列出已解决结果与未解决问题，标明作者、年份、稳定文献键及可点击引文；原文缺口与本报告综合判断分别标注。后半卷保留更详细的模型边界、争议与可检验研究设计。'
]
for i,body in enumerate(bodies):
    header=r'\documentclass[UTF8,a4paper,11pt,openany,fontset=fandol]{ctexbook}'+'\n'
    header+=r'\usepackage{xr}'+'\n'+r'\input{preamble}'+'\n'
    for j in range(3):
        if i!=j:header+=r'\externaldocument[V'+str(j+1)+r'-][nocite]{'+ids[j]+'}['+ids[j]+'.pdf]\n'
    header+=r'\hypersetup{pdftitle={Hall MHD与双流体磁重联：'+titles[i]+'}}\n'
    header+=r'\begin{document}\frontmatter\begin{titlepage}\vspace*{22mm}'+'\n'
    header+=r'{\sffamily\Large Hall MHD 与双流体磁重联调研\par}\vspace{14mm}'+'\n'
    header+=r'{\sffamily\Huge\bfseries\color{ink}'+titles[i]+r'\par}\vspace{10mm}'+'\n'
    header+=r'{\sffamily\large 三卷本 · 第'+str(i+1)+r'卷\par}\vfill'+'\n'
    header+='分卷更新：2026年11月12日。\\\\[5pt]\n'
    header+=f'全文核读证据：{full_read_count}篇，核读更新至2026年11月12日。\\\\[5pt]\n'
    header+=frontnotes[i]+'\n'+r'\end{titlepage}\chapter*{本卷阅读与查阅方式}'+'\n'
    header+=frontnotes[i]+'\n\n'
    header+='三卷分别编排目录和参考文献，文献键保持一致；同一论文在不同卷的引文编号可能不同。标明“基础卷、结果卷、问题卷”的交叉引用会跳转到对应PDF；各卷应保存在同一目录。若阅读器限制跨文件跳转，可按卷名和章节/公式号查阅。全部原文位于项目根目录的papers文件夹。\n\n'
    header+=r'总索引：\href{run:../paper_index.html}{打开可搜索文献索引}。'+'\n'
    for j in range(3):
        if i!=j:header+=r'\par\href{run:'+ids[j]+r'.pdf}{打开《'+titles[j]+r'》}。'+'\n'
    header+=r'\tableofcontents\mainmatter'+'\n'
    (O/(ids[i]+'.tex')).write_text(header+transform(body,i)+'\n'+r'\backmatter\bibliographystyle{unsrtnat}\bibliography{'+ids[i]+r'}\end{document}'+'\n')
    (O/(ids[i]+'.bib')).write_text(transform((P/'references.bib').read_text(),i))

manifest={'date':'2026-11-12','titles':dict(zip(ids,titles)),'source_hashes':provenance,
          'all_master_labels_preserved':True,'label_ownership':ownership,
          'cross_volume_reference_counts':link_counts,
          'omitted_text':f'Only the former combined-cover reading directions and the final repeated reading-route paragraph; scientific sections, {full_read_count} dossiers and candidate inventory retained.',
          'full_read_count':full_read_count}
(QA/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('Generated three volumes; labels preserved:',len(ownership),flush=True)

def tex_tool(name):
    found=shutil.which(name)
    fallback=Path('/Library/TeX/texbin')/name
    if found:return found
    if fallback.is_file():return str(fallback)
    raise RuntimeError('Missing TeX tool: '+name+'; install TeX Live / MacTeX and add its bin directory to PATH.')
tex=tex_tool('xelatex');bib=tex_tool('bibtex')
def run(args,log):
    with (QA/log).open('w') as f:
        r=subprocess.run(args,cwd=O,stdout=f,stderr=subprocess.STDOUT)
    if r.returncode:raise RuntimeError('Build failed: '+str(QA/log))
# First create all .aux files. Subsequent passes resolve cross-volume references.
for name in ids:run([tex,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],name+'_pass0.log')
for name in ids:run([bib,name],name+'_bibtex.log')
for step in range(1,4):
    for name in ids:run([tex,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],name+f'_pass{step}.log')
    print('Resolved build pass',step,flush=True)
print('Completed three PDFs',flush=True)

# XeTeX may encode xr links as Launch("file.pdf#nameddest=...").
# Convert these to portable GoToR actions with verified destination pages.
import fitz
destinations={}
for name in ids:
    with fitz.open(O/(name+'.pdf')) as doc:
        destinations[name+'.pdf']=doc.resolve_names()
fixed=[]
for name in ids:
    path=O/(name+'.pdf')
    doc=fitz.open(path);changed=False
    for page in doc:
        for link in page.get_links():
            target=link.get('file','')
            if '#nameddest=' in target:
                filename,dest=target.split('#nameddest=',1)
                entry=destinations[filename][dest]
                new=dict(link,kind=fitz.LINK_GOTOR,file=filename,page=entry['page'],to=fitz.Point(0,0),zoom=0)
                page.update_link(new);changed=True
                fixed.append({'source':name+'.pdf','source_page':page.number+1,
                              'target':filename,'destination':dest,'target_page':entry['page']+1})
            elif target.endswith('.html') and link['kind']!=fitz.LINK_LAUNCH:
                page.update_link(dict(link,kind=fitz.LINK_LAUNCH,file=target));changed=True
    if changed:doc.saveIncr()
    doc.close()
(QA/'cross_volume_links.json').write_text(json.dumps(fixed,ensure_ascii=False,indent=2))
print('Verified and normalized cross-volume links:',len(fixed),flush=True)
