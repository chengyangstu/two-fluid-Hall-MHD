# coding: utf-8
"""Reorganize all existing finding blocks, with an explicit preservation audit."""
from pathlib import Path
import re,json,hashlib
P=Path(__file__).resolve().parents[1];W=P/'research/synthesis_continuation'
plan=json.loads((W/'story_plan.json').read_text())
units={};sources={}
for filename,prefix,levels in [
 ('03_findings','B','section'),('03_continuation_findings','C','section'),
 ('03_selected_findings','S','section|subsection'),('03_remaining_findings','R','section|subsection')]:
 s=(W/'before/sections'/f'{filename}.tex').read_text()
 s=re.sub(r'\\input\{sections/03_[^}]+\}\s*','',s)
 ms=list(re.finditer(r'\\('+levels+r')\{([^}]+)\}',s))
 for i,m in enumerate(ms):
  key=f'{prefix}{i}';block=s[m.start():ms[i+1].start() if i+1<len(ms) else len(s)].strip()
  if m[1]=='section':
   block=block.replace(r'\subsection{',r'\subsubsection{').replace(r'\section{',r'\subsection{')
  units[key]=block;sources[key]=dict(source=filename,title=m[2])
# Remove obsolete batch introductions, preserving all scientific content.
excluded=['B0','S0','S4','S8','R0']
for key in excluded: del units[key]
# A former adjacent section is farther away after regrouping.
for key in units:
 units[key]=units[key].replace('与下一节的大系统结果存在','与后文的大系统结果存在')
units['S2'],q=units['S2'].split('\n\\citet{L089}',1)
units['S2q']=r'\subsection{四极Hall场的理论结构怎样接受实验检验}'+'\n\\citet{L089}'+q
units['B26'],q=units['B26'].split('\n\\subsubsection{“Hall电流耗散”不是Hall项直接加热}',1)
units['B26h']=r'\subsection{“Hall电流耗散”不是Hall项直接加热}'+q
new=(P/'sections/synthesis/new_findings.tex').read_text()
ms=list(re.finditer(r'\\subsection\{([^}]+)\}',new))
newids=['Nclosure','Nfinite','Nheating','Nnested','Nexperiment']
assert len(ms)==len(newids)
for i,m in enumerate(ms):units[newids[i]]=new[m.start():ms[i+1].start() if i+1<len(ms) else len(new)].strip()
assigned=[u for g in plan for u in g['units']]
assert len(assigned)==len(set(assigned)), 'duplicate block'
assert set(assigned)==set(units), (set(units)-set(assigned),set(assigned)-set(units))
outdir=P/'sections/synthesis';outdir.mkdir(exist_ok=True)
audit=[]
for g in plan:
 s=r'\section{'+g['title']+r'}\label{story:'+g['id']+'}\n'
 s+=g['intro']+'\n\n'
 for key in g['units']:
  s+=units[key].strip()+'\n\n'
  audit.append(dict(unit=key,story=g['id'],sha256=hashlib.sha256(units[key].encode()).hexdigest(),**sources.get(key,{})))
 s+=r'\paragraph{这一线索走到了哪里。}'+g['outro']+'\n'
 (outdir/('03_'+g['id']+'.tex')).write_text(s)
overview=r'''\chapter{重要重联问题与研究脉络}\label{ch:findings}
\label{sec:remaining-findings}
本章按问题重新编排已经核读的研究，而不按下载或续读批次罗列。各条线先说明前一组结果留下了什么问题，再比较后续模型怎样回答；原有的参数、反例和证据限制仍保留。这里的连接是本报告的\textbf{问题导向阅读顺序}，除明确说明的前序研究外，不冒称已经核实所有作者间的直接引用关系。

先区分四种问题：磁通是否改变拓扑；已经启动的局地层有多快；全系统多久完成重联；能量怎样进入不同物种及自由度。回答第二种问题的成功不能自动推广到其余三种。尤其要区分峰值、准稳态与时间平均，以及局地上游场和初始全局场归一化。

\begin{longtable}{P{24mm}P{85mm}P{38mm}}
\toprule 问题线 & 文献之间的推进关系 & 继续阅读入口\\\midrule\endfirsthead
\toprule 问题线 & 文献之间的推进关系 & 继续阅读入口\\\midrule\endhead
局地快率 & 两流体/GEM基准 → 色散解释 → 无快速色散波反例与压力机制 & 第\ref{story:fast}节\\
局地到全局 & 未选定层长 → 动态供磁与背压 → 岛合并、驱动和尺寸效应 & 第\ref{story:global}节\\
启动与状态 & 惯性尖化/非线性加速 → Hall内层与递归磁岛 → 往复、间歇及关停 & 第\ref{story:onset}节\\
压力与热流 & 总率相近但结构不同 → 各向异性/十矩 → 热流、模态与闭合迁移 & 第\ref{story:closure}节\\
第三维 & 孤立X线 → 扩展与历史 → 有限活跃长度 → 三维模式与湍流状态 & 第\ref{story:three}节\\
能量与热化 & 同谱不同粒子参与 → 电子独有重联 → 分物种功、相混合与熵 & 第\ref{story:energy}节\\
可观测证据 & 四极场 → 嵌套与多物种歧义 → 电势/流速/温度的联合检验 & 第\ref{story:diagnostic}节\\
\bottomrule
\end{longtable}

\paragraph{怎样把叙述反查到论文。}
每节引文可跳到参考文献，再进入第7章的稳定文献键档案及本地PDF。末章每篇还标出本章的问题线；模型基础与算法文献另列为“模型与数值可信度”，主要对应第1、2章。HTML索引同时支持按问题线筛选。模型推导均在第一章；本章涉及PIC、混合动理学或实验时明确保留身份，不把它们改称Hall流体模拟。
'''
# Use correct TeX row breaks, without embedding shell quoting.
overview=overview.replace(r'入口\\\midrule',r'入口\\\midrule')
(P/'sections/03_findings.tex').write_text(overview+'\n'+'\n'.join(r'\input{sections/synthesis/03_'+g['id']+'}' for g in plan)+'\n')
(W/'reorganization_audit.json').write_text(json.dumps({'preserved_scientific_blocks':len(assigned),'obsolete_batch_intros_removed':excluded,'blocks':audit},ensure_ascii=False,indent=2))
print('Organized',len(assigned),'blocks into',len(plan),'problem storylines')
