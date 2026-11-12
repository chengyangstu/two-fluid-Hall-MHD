"""Record title/bibliographic triage, never infer full-paper reading."""
import json, csv, collections
from pathlib import Path
P=Path(__file__).resolve().parents[1]
R=P/'research/remaining_screen'
rows=json.loads((R/'baseline.json').read_text())
groups={
 '基础与早期争议':'L001 L002 L005 Biskamp1995 L008 L012 L014 L018 Otto2001 BirnHesse2001 Ma2001 L030 Grasso2001 Huba2002 Huba2004 HubaGuide2004 L056 L062 L064 L074 Knoll2006 L082 Yamada2006 L092 L095 L102 L108 Simakov2008 L133 L152 Sullivan2010 F646 F647 F648 F730 F764',
 '三维、流剪切与全局耦合':'L054 L071 L181 L205 L206 L211 L223 L241 L287 F624 F629 F659 F693 F700 F792',
 '压力闭合、磁岛与新尺度':'L177 L220 L227 L272 L283 L314 L319 E461 E466 E473 E504 E546 F578 F589 F592 F600 F606 F625 F655 F741 F759 F760 F771 F788 F798',
 '实验和观测检验':'L026 L055 L093 L103 L158 L188 L190 L213 L226 L228 L235 L239 L261 L306 E334 E508 E550 F626 F674 F679 F703 F718 F724 F732 F793 F794',
 '数值与模型实现':'L038 L050 L066 L115 L139 L150 L153 L164 L183 L231 L247 L301 L309 L320 E514 E537 E556 F559 F611 F746'
}
priority={k:g for g,ks in groups.items() for k in ks.split()}
meetings={'Bulletin of the American Physical Society','APS','AGUFM','EGUGA','AGU Spring Meeting Abstracts'}
out=[]
for x in rows:
 k=x['key']; j=x.get('journal','');typ=x.get('type','')
 if k in priority:
  route='优先获取或核读';reason=priority[k]+'：题名/书目提示可能补足已有报告，重要性待正文核定'
 elif j in meetings or typ=='presentation':
  route='会议记录追溯';reason='书目来源为会议摘要或报告；保留线索并追踪正式论文，不作为独立全文证据'
 elif typ=='dissertation' or x.get('pages',0)>100:
  route='长文或学位资料';reason='需核对文献类型并关联正式论文；不按页数或重复版本凑数'
 elif typ in {'review','book-chapter'}:
  route='综述与章节';reason='适合追踪引文；原创新现象须回到原始研究'
 elif any(w in x['title'].lower() for w in ['relativistic','electron-positron','pair plasma','quantum','black hole','neutron star','dust','partially ionized','chromospher','weakly ionized']):
  route='模型边界待全文确认';reason='可能属于相对论、对等离子体、中性或多物种；与电子—离子双流体区别后决定纳入位置'
 else:
  route='保留待全文核读';reason='不能仅凭题名判定价值或排除；需正文核对实际模型、参数及现象'
 out.append(dict(key=k,year=x.get('year'),title=x['title'],screening_level='题名与书目信息初筛',route=route,reason=reason,local_pdf=x.get('local_pdf',''),full_read=False))
(R/'screening.json').write_text(json.dumps({'date':'2026-11-11','baseline_count':698,'scope':'698条全部完成题名/书目初筛；不等于摘要筛查、资格终审或全文读完。未读条目不用于正文结论。','records':out},ensure_ascii=False,indent=2))
with (R/'screening.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print(collections.Counter(x['route'] for x in out))
