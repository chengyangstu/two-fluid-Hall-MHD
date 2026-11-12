# coding: utf-8
from pathlib import Path
import json,requests,fitz,hashlib
P=Path(__file__).resolve().parents[1]
p=P/'research/catalog.json';c=json.loads(p.read_text())
for r in c:
 if r['key']=='L140':r['duplicate_of']='Sullivan2009'
 if r['key']=='E423':r['duplicate_of']='L153'
 if r['key']=='L279':
  r['mismatched_pdf']=r['local_pdf'];r['local_pdf']=''
  r['download_status']='已排除错配PDF，待取得正确学位论文'
 if r['key']=='E397':
  r['eligibility']='排除'
  r['exclusion_reason']='实为APS新闻稿，不是研究论文；数据库误把正文当题名'
 if r['key']=='E392':
  r['eligibility']='补充资料';r['scope']='会议海报／PIC对照'
 if r['key']=='L196':
  r['scope']='会议报告幻灯片，非完整论文';r['type']='presentation'
 if r['key']=='L057':
  url='https://farside.ph.utexas.edu/Papers/1.1640378.pdf'
  data=requests.get(url,timeout=40).content;d=fitz.open(stream=data,filetype='pdf')
  assert '937' in d[0].get_text() and '1.1640378' in d[0].get_text()[:550]
  (P/'papers/L057.pdf').write_bytes(data)
  (P/'research/text/L057.txt').write_text('\n'.join(v.get_text() for v in d))
  r.update(download_url=url,pages=len(d),sha256=hashlib.sha256(data).hexdigest())
  r['identity_audit']='已改正相似题名错配，首页DOI与题名确认'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2))
p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
v['Sullivan2009']=dict(
 pages_read='arXiv0905.4765v3 1-11全部',
 figures_checked='图1-13；图4-6、8-13视觉复核',
 model='等温压缩性双流体；参考密度常系数B′惯性；超电阻断线，密度和动量另含四阶扩散。',
 parameters='周期12.8di方盒、512²、dx.025；四岛正弦平衡、总温1、beta最小11.45、V0.1；全部初始电流由离子携带；'
 'mu4=5.1e-7；扫描eta_H约3.9e-5至3.9e-3及mi/me25-200；另盒6.4和25.6。',
 finding='无惯性扫描L_e约eta_H^(1/3)，delta_e约eta_H^(4/9)，局地归一化率随eta_H变，而原始率和全局归一化率约.1-.2且弱依赖；'
 '惯性扫描长度可按(me/mi)^(3/8)，厚度近1/3幂，长宽比弱变化。',
 limitation='无惯性超电阻扫描最长仍不到di，未复现动力学长约10di片及大量次级岛；最低eta层接近网格不可靠；'
 '3/8与1/3在一数量级质量窗无法区分；真实质量比15de长度和1de宽度为外推；边界、导引与惯性超电阻同时重要区未扫描。',
 assessment='重要发现是电子层长度也依赖断线机制，以及局地与全局归一化可能给出不同表述；不是Hall成功复现任意长电子层的证明。',
 status='正文完整阅读；核心图与参数核验')
p.write_text(json.dumps(v,ensure_ascii=False,indent=2));print('READ',len(v))
