# coding: utf-8
from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
W=P/'research/synthesis_continuation'
v=json.loads((P/'research/reading_notes/verified.json').read_text())
plan=json.loads((W/'story_plan.json').read_text())
names={'fast':'局地快率与必要条件','global':'层长、驱动与全局完成',
 'onset':'启动、爆发与磁岛','closure':'压力、热流与闭合',
 'three':'三维传播与有限X线','energy':'电子独有重联与热化',
 'diagnostic':'实验与可区分诊断','foundation':'模型与数值可信度'}
def keys(s):
 return {k for group in re.findall(r'\\cite\w*\{([^}]+)\}',s) for k in group.split(',')}
def expanded(path,seen=None):
 seen=set() if seen is None else seen
 if path in seen:return ''
 seen.add(path);s=path.read_text()
 return s+'\n'+'\n'.join(expanded(P/(f+'.tex'),seen) for f in re.findall(r'\\input\{([^}]+)\}',s))
membership={k:[] for k in v}
for g in plan:
 for k in keys((P/'sections/synthesis'/('03_'+g['id']+'.tex')).read_text()):
  assert k in v,k
  membership[k].append(g['id'])
# Method and experiment papers are not forced into a finding they do not claim.
foundation=keys(expanded(P/'sections/01_models.tex'))|keys(expanded(P/'sections/02_numerics.tex'))
experiments=set()
for f in (P/'sections').glob('05_*.tex'):experiments |= keys(f.read_text())
for k in v:
 if k in foundation and not membership[k]:membership[k].append('foundation')
 if k in experiments and 'diagnostic' not in membership[k]:membership[k].append('diagnostic')
unknown=[k for k,gs in membership.items() if not gs]
assert not unknown,unknown
data={'stories':[dict(id=k,name=n,label='ch:numerics' if k=='foundation' else 'story:'+k) for k,n in names.items()],
      'papers':{k:{'stories':gs,'primary':gs[0]} for k,gs in membership.items()}}
(W/'paper_story_map.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('Mapped',len(membership),'full-read papers:',{g:sum(g in gs for gs in membership.values()) for g in names})
